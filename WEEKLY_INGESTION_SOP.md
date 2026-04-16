# Weekly Historical Snapshot Ingestion SOP

This SOP defines the weekly process for collecting, validating, and ingesting dated SPD snapshot files into the historical dataset used by the dashboard.

## Objective

Create a reliable weekly history so the dashboard can support:

- SPD trends
- team momentum
- campaign movement
- anomaly detection
- forecast-ready features

## Target Cadence

- `Weekly`

Recommended day:

- same weekday every week

Recommended naming:

- `YYYY-MM-DD_health.xlsx`

Examples:

- `2026-04-23_health.xlsx`
- `2026-04-30_health.xlsx`
- `2026-05-07_health.xlsx`

## Folder Structure

Raw files:

- `data/raw/`

Processed history:

- `data/processed/historical_spd_data.csv`

## Roles

`Ops / Analyst`

- export the weekly source file
- save the file using the date-based filename
- place the file into `data/raw/`
- run the ingestion command

`Dashboard Owner`

- verify row counts
- verify snapshot date was added correctly
- review whether new trends appear as expected
- flag schema issues or unusual data shifts

## Standard Weekly Steps

1. Export the latest weekly snapshot from the source workbook/system.
2. Save the file in `data/raw/` using the standard filename.
3. Run ingestion:

```bash
python3 ingest_history.py data/raw/2026-04-23_health.xlsx
```

If the filename does not contain a valid date:

```bash
python3 ingest_history.py data/raw/health.xlsx --snapshot-date 2026-04-23
```

4. Review the script output:
   - rows written
   - duplicates removed
   - snapshot dates in dataset
5. Open the dashboard and confirm the new snapshot appears in the `Snapshot Date` filter.
6. Review the `Trends` page.

## Expected Ingestion Output

You should see output similar to:

```text
Historical dataset saved to: .../data/processed/historical_spd_data.csv
Rows written: 112
New rows considered: 56
Duplicates removed: 0
Snapshot dates in dataset:
  - 2026-04-16 00:00:00
  - 2026-04-23 00:00:00
```

## If Something Looks Wrong

Check:

- filename date
- sheet name
- column names
- repeated header rows inside the sheet
- row counts that are too high or too low

## Good Operating Practice

- never overwrite old snapshot files in `data/raw/`
- keep one raw file per reporting date
- keep the same export logic each week
- do not rename source columns manually unless the dashboard schema is updated too

## Minimum Useful History

- `2 snapshots`: basic before/after movement
- `4 snapshots`: usable trend and momentum
- `8+ snapshots`: early anomaly logic and forecast readiness
