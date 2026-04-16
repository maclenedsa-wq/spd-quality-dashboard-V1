from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from historical_data import (
    HISTORICAL_DATA_FILE,
    HISTORICAL_SCHEMA,
    ensure_data_directories,
    parse_snapshot_date,
    standardize_snapshot_frame,
)


def load_existing_history() -> pd.DataFrame:
    if not HISTORICAL_DATA_FILE.exists():
        return pd.DataFrame(columns=HISTORICAL_SCHEMA)
    history = pd.read_csv(HISTORICAL_DATA_FILE, parse_dates=["Snapshot Date", "Ingested At"])
    for column in HISTORICAL_SCHEMA:
        if column not in history.columns:
            history[column] = pd.NA
    return history[HISTORICAL_SCHEMA].copy()


def infer_snapshot_date(path: Path, explicit_date: str | None) -> pd.Timestamp:
    if explicit_date:
        parsed = pd.to_datetime(explicit_date, errors="coerce")
        if pd.isna(parsed):
            raise ValueError(f"Invalid --snapshot-date value: {explicit_date}")
        return parsed.normalize()

    parsed = parse_snapshot_date(path.name)
    if parsed is None:
        raise ValueError(
            f"Could not infer snapshot date from filename '{path.name}'. "
            "Use --snapshot-date YYYY-MM-DD."
        )
    return parsed


def ingest_file(path: Path, sheet_name: str, snapshot_date: pd.Timestamp) -> pd.DataFrame:
    frame = pd.read_excel(path, sheet_name=sheet_name, engine="openpyxl")
    return standardize_snapshot_frame(frame, snapshot_date=snapshot_date, source_name=path.name)


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest dated SPD snapshot files into historical_spd_data.csv")
    parser.add_argument("paths", nargs="+", help="One or more Excel snapshot files to ingest")
    parser.add_argument("--sheet-name", default="Health", help="Sheet to read from each workbook")
    parser.add_argument(
        "--snapshot-date",
        default=None,
        help="Optional snapshot date (YYYY-MM-DD). If omitted, the script tries to infer it from the filename.",
    )
    args = parser.parse_args()

    ensure_data_directories()
    existing = load_existing_history()
    ingested_frames: list[pd.DataFrame] = []

    for raw_path in args.paths:
        path = Path(raw_path).expanduser().resolve()
        if not path.exists():
            raise FileNotFoundError(f"Input file not found: {path}")
        snapshot_date = infer_snapshot_date(path, args.snapshot_date)
        ingested_frames.append(ingest_file(path, args.sheet_name, snapshot_date))

    new_rows = pd.concat(ingested_frames, ignore_index=True) if ingested_frames else pd.DataFrame(columns=HISTORICAL_SCHEMA)
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

    print(f"Historical dataset saved to: {HISTORICAL_DATA_FILE}")
    print(f"Rows written: {len(combined)}")
    print(f"New rows considered: {len(new_rows)}")
    print(f"Duplicates removed: {before - len(combined)}")
    print("Snapshot dates in dataset:")
    for value in combined["Snapshot Date"].dropna().astype("string").unique().tolist():
        print(f"  - {value}")


if __name__ == "__main__":
    main()
