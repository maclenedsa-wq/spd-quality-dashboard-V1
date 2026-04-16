from __future__ import annotations

import argparse
import os
from pathlib import Path

import pandas as pd

from historical_data import (
    HISTORICAL_DATA_FILE,
    HISTORICAL_SCHEMA,
    load_google_service_account_info,
    parse_snapshot_date,
    parse_spreadsheet_id,
    standardize_snapshot_frame,
    ensure_data_directories,
    write_sync_status,
)


def load_existing_history() -> pd.DataFrame:
    if not HISTORICAL_DATA_FILE.exists():
        return pd.DataFrame(columns=HISTORICAL_SCHEMA)
    history = pd.read_csv(HISTORICAL_DATA_FILE, parse_dates=["Snapshot Date", "Ingested At"])
    for column in HISTORICAL_SCHEMA:
        if column not in history.columns:
            history[column] = pd.NA
    return history[HISTORICAL_SCHEMA].copy()


def infer_snapshot_date(source_name: str, explicit_date: str | None) -> pd.Timestamp:
    if explicit_date:
        parsed = pd.to_datetime(explicit_date, errors="coerce")
        if pd.isna(parsed):
            raise ValueError(f"Invalid --snapshot-date value: {explicit_date}")
        return parsed.normalize()

    parsed = parse_snapshot_date(source_name)
    if parsed is None:
        return pd.Timestamp.now(tz="Asia/Kolkata").normalize().tz_localize(None)
    return parsed


def ingest_excel_file(path: Path, sheet_name: str, snapshot_date: pd.Timestamp) -> pd.DataFrame:
    frame = pd.read_excel(path, sheet_name=sheet_name, engine="openpyxl")
    return standardize_snapshot_frame(frame, snapshot_date=snapshot_date, source_name=path.name)


def fetch_google_sheet(spreadsheet_id: str, sheet_name: str, cell_range: str | None) -> pd.DataFrame:
    credentials_info = load_google_service_account_info()
    if not credentials_info:
        raise RuntimeError(
            "Google service account credentials were not found. Set GOOGLE_SERVICE_ACCOUNT_JSON "
            "or GOOGLE_SERVICE_ACCOUNT_FILE before using --source google-sheet."
        )

    try:
        from google.oauth2.service_account import Credentials
        from googleapiclient.discovery import build
    except ImportError as exc:
        raise RuntimeError(
            "Google API dependencies are missing. Install google-api-python-client and google-auth."
        ) from exc

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets.readonly",
        "https://www.googleapis.com/auth/drive.readonly",
    ]
    credentials = Credentials.from_service_account_info(credentials_info, scopes=scopes)
    service = build("sheets", "v4", credentials=credentials, cache_discovery=False)

    target_range = sheet_name if not cell_range else f"{sheet_name}!{cell_range}"
    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=spreadsheet_id, range=target_range)
        .execute()
    )
    values = result.get("values", [])
    if not values:
        raise ValueError(f"No rows returned from spreadsheet '{spreadsheet_id}' sheet '{target_range}'.")

    headers = [str(item).strip() for item in values[0]]
    rows = values[1:]
    width = len(headers)
    normalized_rows: list[list[str | None]] = []
    for row in rows:
        padded = list(row[:width]) + [None] * max(0, width - len(row))
        normalized_rows.append(padded[:width])
    return pd.DataFrame(normalized_rows, columns=headers)


def ingest_google_sheet(
    spreadsheet_id: str,
    sheet_name: str,
    cell_range: str | None,
    snapshot_date: pd.Timestamp,
    source_label: str,
) -> pd.DataFrame:
    frame = fetch_google_sheet(spreadsheet_id, sheet_name, cell_range)
    return standardize_snapshot_frame(frame, snapshot_date=snapshot_date, source_name=source_label)


def combine_and_save(existing: pd.DataFrame, new_rows: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    combined = pd.concat([existing, new_rows], ignore_index=True)
    combined["Dedup Key"] = (
        combined["Snapshot Date"].astype("string")
        + "||"
        + combined["Campaign"].astype("string")
        + "||"
        + combined["ECN"].fillna(combined["Agent Name"]).astype("string")
    )
    before = len(combined)
    combined = combined.drop_duplicates(subset=["Dedup Key"], keep="last").drop(columns=["Dedup Key"])
    combined = combined.sort_values(["Snapshot Date", "Campaign", "Team / Vendor", "Agent Name"]).reset_index(drop=True)
    combined.to_csv(HISTORICAL_DATA_FILE, index=False)
    return combined, before - len(combined)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Ingest dated SPD snapshots into historical_spd_data.csv")
    parser.add_argument("paths", nargs="*", help="Excel snapshot files to ingest when using --source excel")
    parser.add_argument(
        "--source",
        choices=["excel", "google-sheet"],
        default="excel",
        help="Ingest from local Excel files or directly from Google Sheets.",
    )
    parser.add_argument("--sheet-name", default=os.getenv("GOOGLE_SHEETS_WORKSHEET", "Health"), help="Worksheet to read.")
    parser.add_argument(
        "--sheet-range",
        default=os.getenv("GOOGLE_SHEETS_RANGE"),
        help="Optional A1 range within the worksheet, for example A:Z.",
    )
    parser.add_argument(
        "--snapshot-date",
        default=None,
        help="Optional snapshot date (YYYY-MM-DD). If omitted, inferred from file name or defaults to today's IST date for Google Sheets.",
    )
    parser.add_argument(
        "--spreadsheet-id",
        default=os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID"),
        help="Google spreadsheet ID. Can also be provided as GOOGLE_SHEETS_SPREADSHEET_ID.",
    )
    parser.add_argument(
        "--spreadsheet-url",
        default=os.getenv("GOOGLE_SHEETS_URL"),
        help="Google spreadsheet URL. Useful instead of --spreadsheet-id.",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    ensure_data_directories()
    existing = load_existing_history()

    if args.source == "excel":
        if not args.paths:
            raise ValueError("At least one Excel path is required when --source excel is used.")
        ingested_frames: list[pd.DataFrame] = []
        for raw_path in args.paths:
            path = Path(raw_path).expanduser().resolve()
            if not path.exists():
                raise FileNotFoundError(f"Input file not found: {path}")
            snapshot_date = infer_snapshot_date(path.name, args.snapshot_date)
            ingested_frames.append(ingest_excel_file(path, args.sheet_name, snapshot_date))
        new_rows = pd.concat(ingested_frames, ignore_index=True)
        source_label = ", ".join([Path(item).name for item in args.paths])
    else:
        spreadsheet_id = parse_spreadsheet_id(args.spreadsheet_url) or parse_spreadsheet_id(args.spreadsheet_id)
        if not spreadsheet_id:
            raise ValueError("Provide --spreadsheet-id or --spreadsheet-url when --source google-sheet is used.")
        snapshot_date = infer_snapshot_date(spreadsheet_id, args.snapshot_date)
        source_label = f"google-sheet:{spreadsheet_id}:{args.sheet_name}"
        new_rows = ingest_google_sheet(
            spreadsheet_id=spreadsheet_id,
            sheet_name=args.sheet_name,
            cell_range=args.sheet_range,
            snapshot_date=snapshot_date,
            source_label=source_label,
        )

    combined, duplicates_removed = combine_and_save(existing, new_rows)
    sync_payload = {
        "status": "success",
        "source_type": args.source,
        "source_label": source_label,
        "worksheet": args.sheet_name,
        "sheet_range": args.sheet_range,
        "spreadsheet_id": parse_spreadsheet_id(args.spreadsheet_url) or parse_spreadsheet_id(args.spreadsheet_id),
        "last_sync_at": pd.Timestamp.utcnow(),
        "latest_snapshot_date": combined["Snapshot Date"].max() if not combined.empty else pd.NaT,
        "rows_written": int(len(combined)),
        "new_rows_considered": int(len(new_rows)),
        "duplicates_removed": int(duplicates_removed),
        "snapshot_dates": [str(value) for value in combined["Snapshot Date"].dropna().astype("string").unique().tolist()],
    }
    write_sync_status(sync_payload)

    print(f"Historical dataset saved to: {HISTORICAL_DATA_FILE}")
    print(f"Rows written: {len(combined)}")
    print(f"New rows considered: {len(new_rows)}")
    print(f"Duplicates removed: {duplicates_removed}")
    print("Snapshot dates in dataset:")
    for value in combined["Snapshot Date"].dropna().astype("string").unique().tolist():
        print(f"  - {value}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        write_sync_status(
            {
                "status": "failed",
                "last_sync_at": pd.Timestamp.utcnow(),
                "error": str(exc),
            }
        )
        raise
