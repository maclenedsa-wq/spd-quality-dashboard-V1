from __future__ import annotations

from pathlib import Path
import re

import pandas as pd


BASE_DIR = Path(__file__).parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
HISTORICAL_DATA_FILE = PROCESSED_DATA_DIR / "historical_spd_data.csv"

RENAME_MAP = {
    "Advisor": "Agent Name",
    "Team Leader": "Team / Vendor",
    "SPD/Agent": "SPD",
    "Quality Score": "Overall Quality Score",
    "Listening & Understanding Needs": "Listening",
    "Product Knowledge and Explanation": "Product Knowledge",
    "Acknowledge & Empathise": "Empathise",
    "Language, Tone and Professionalism": "Language Tone Professionalism",
    "Assisted Sales ( Highest TT >5min)": "Assisted Sales",
}

TEXT_COLUMNS = ["Campaign", "Team / Vendor", "ECN", "Agent Name"]
NUMERIC_COLUMNS = [
    "Mandays",
    "Total Attempted",
    "Total Connected",
    "Avg Talk time per day",
    "Assisted Sales",
    "SPD",
    "Overall Quality Score",
    "Listening",
    "Product Knowledge",
    "Transaction",
    "Empathise",
    "Language Tone Professionalism",
    "Positive",
    "Negative",
    "Neutral",
    ".escalated",
    ".not_interested_in_buying",
    ".payment_done",
    ".will_buy_self",
    ".positive_intent_needs_follow_up",
    ".non_material_interaction",
    ".follow_up_required",
    ".unresolved",
    ".partially_resolved",
    ".resolved",
    ".threatened_to_escalate",
]

HISTORICAL_SCHEMA = [
    "Snapshot Date",
    "Source File Name",
    "Ingested At",
    "Campaign",
    "Team / Vendor",
    "ECN",
    "Agent Name",
    "Mandays",
    "Total Attempted",
    "Total Connected",
    "Avg Talk time per day",
    "Assisted Sales",
    "SPD",
    "Overall Quality Score",
    "Listening",
    "Product Knowledge",
    "Transaction",
    "Empathise",
    "Language Tone Professionalism",
    "Positive",
    "Negative",
    "Neutral",
    ".escalated",
    ".not_interested_in_buying",
    ".payment_done",
    ".will_buy_self",
    ".positive_intent_needs_follow_up",
    ".non_material_interaction",
    ".follow_up_required",
    ".unresolved",
    ".partially_resolved",
    ".resolved",
    ".threatened_to_escalate",
]


def parse_snapshot_date(value: str | Path | None) -> pd.Timestamp | None:
    if value is None:
        return None
    text = str(value)
    match = re.search(r"(20\d{2}[-_]?([01]\d)[-_]?([0-3]\d))", text)
    if not match:
        return None
    token = match.group(1).replace("_", "-")
    if len(token) == 8 and "-" not in token:
        token = f"{token[:4]}-{token[4:6]}-{token[6:]}"
    parsed = pd.to_datetime(token, errors="coerce")
    return None if pd.isna(parsed) else parsed.normalize()


def standardize_snapshot_frame(
    df: pd.DataFrame,
    snapshot_date: pd.Timestamp,
    source_name: str,
) -> pd.DataFrame:
    normalized = df.copy()
    normalized = normalized.loc[:, ~normalized.columns.astype(str).str.startswith("Unnamed:")]
    normalized = normalized.loc[:, ~normalized.columns.astype(str).str.startswith("Correlation")]
    normalized = normalized.rename(columns=RENAME_MAP)

    for column in TEXT_COLUMNS:
        if column in normalized.columns:
            normalized[column] = normalized[column].astype("string").str.strip()

    for column in NUMERIC_COLUMNS:
        if column in normalized.columns:
            normalized[column] = pd.to_numeric(normalized[column], errors="coerce")

    normalized = normalized[normalized["Agent Name"].notna()].copy()
    normalized = normalized[
        ~normalized["Agent Name"].astype("string").str.strip().isin(["Advisor", "Agent Name"])
    ].copy()
    if "Campaign" in normalized.columns:
        normalized = normalized[
            ~normalized["Campaign"].astype("string").str.strip().isin(["Campaign"])
        ].copy()
    normalized["Snapshot Date"] = pd.to_datetime(snapshot_date).normalize()
    normalized["Source File Name"] = str(source_name)
    normalized["Ingested At"] = pd.Timestamp.utcnow().tz_localize(None)

    for column in HISTORICAL_SCHEMA:
        if column not in normalized.columns:
            normalized[column] = pd.NA

    normalized = normalized[HISTORICAL_SCHEMA].copy()
    normalized = normalized.sort_values(["Snapshot Date", "Campaign", "Team / Vendor", "Agent Name"]).reset_index(drop=True)
    return normalized


def ensure_data_directories() -> None:
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
