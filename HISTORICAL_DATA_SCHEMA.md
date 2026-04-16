# Historical SPD Data Schema

The historical dataset is stored at:

- `data/processed/historical_spd_data.csv`

Recommended raw drop zone:

- `data/raw/`

Each ingested row should represent:

- `1 row per agent per campaign per snapshot date`

## Required Columns

| Column | Type | Notes |
|---|---|---|
| `Snapshot Date` | date | Reporting snapshot date |
| `Source File Name` | string | Raw file used for ingestion |
| `Ingested At` | datetime | UTC timestamp when the row was processed |
| `Campaign` | string | Campaign / business unit |
| `Team / Vendor` | string | Team leader / vendor / reporting team |
| `ECN` | string | Stable employee/advisor ID when available |
| `Agent Name` | string | Advisor name |
| `Mandays` | number | Optional but useful for productivity normalization |
| `Total Attempted` | number | Optional volume metric |
| `Total Connected` | number | Optional contact metric |
| `Avg Talk time per day` | number | Optional efficiency metric |
| `Assisted Sales` | number | Optional sales-support metric |
| `SPD` | number | Core sales performance metric |
| `Overall Quality Score` | number | Quality score |
| `Listening` | number | Normalized quality parameter |
| `Product Knowledge` | number | Normalized quality parameter |
| `Transaction` | number | Normalized quality parameter |
| `Empathise` | number | Normalized quality parameter |
| `Language Tone Professionalism` | number | Normalized quality parameter |
| `Positive` | number | Disposition/flag field |
| `Negative` | number | Disposition/flag field |
| `Neutral` | number | Disposition/flag field |
| `.escalated` | number | Detailed disposition field |
| `.not_interested_in_buying` | number | Detailed disposition field |
| `.payment_done` | number | Detailed disposition field |
| `.will_buy_self` | number | Detailed disposition field |
| `.positive_intent_needs_follow_up` | number | Detailed disposition field |
| `.non_material_interaction` | number | Detailed disposition field |
| `.follow_up_required` | number | Detailed disposition field |
| `.unresolved` | number | Detailed disposition field |
| `.partially_resolved` | number | Detailed disposition field |
| `.resolved` | number | Detailed disposition field |
| `.threatened_to_escalate` | number | Detailed disposition field |

## Dedupe Rule

Rows are de-duplicated using:

- `Snapshot Date`
- `Campaign`
- `ECN` when available, else `Agent Name`

## Filename Convention

Use dated raw filenames so the ingestion script can infer the snapshot date:

- `2026-04-01_health.xlsx`
- `2026-04-08_health.xlsx`

If the filename does not contain a date, provide one explicitly:

```bash
python3 ingest_history.py path/to/file.xlsx --snapshot-date 2026-04-08
```

## Ingestion Example

```bash
python3 ingest_history.py data/raw/2026-04-01_health.xlsx
python3 ingest_history.py data/raw/2026-04-08_health.xlsx
```

After snapshots are ingested, the Streamlit app automatically switches to historical mode and enables snapshot-based filtering.
