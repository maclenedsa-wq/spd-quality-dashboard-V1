# Google Sheets Daily Sync Setup

This project can now pull the latest SPD source data directly from Google Sheets and append it to the historical dataset every morning at `9:00 AM IST`.

## Architecture

The dashboard does **not** read the Google Sheet live on every page load.

Instead it uses this flow:

1. Ops updates the Google Sheet in Google Drive
2. A scheduled GitHub Actions workflow runs at `9:00 AM IST`
3. The workflow runs `ingest_history.py --source google-sheet`
4. The cleaned snapshot is appended into:
   - `data/processed/historical_spd_data.csv`
   - `data/processed/sync_status.json`
5. Streamlit reads the processed historical file

This is safer, faster, and gives us historical trend tracking automatically.

## What You Need In Google

1. Create or use a Google Cloud project
2. Enable:
   - `Google Sheets API`
   - `Google Drive API`
3. Create a `Service Account`
4. Generate a JSON key for that service account
5. Share the target Google Sheet with the service account email as a viewer

Important:
If the sheet lives in a Shared Drive, the service account must also have access through that drive or directly to the sheet.

## GitHub Secrets To Add

In your GitHub repository, add these secrets:

- `GOOGLE_SERVICE_ACCOUNT_JSON`
  - paste the full service-account JSON
- `GOOGLE_SHEETS_URL`
  - the full Google Sheets URL
- `GOOGLE_SHEETS_WORKSHEET`
  - usually `Health`
- `GOOGLE_SHEETS_RANGE`
  - optional, for example `A:Z`

## Workflow

The workflow file is:

- `.github/workflows/daily_google_sheet_sync.yml`

It runs:

- automatically every day at `9:00 AM IST`
- manually via `workflow_dispatch`

## Local Test

For local testing, create:

- `.streamlit/secrets.toml`

You can copy from:

- `.streamlit/secrets.example.toml`

Then run:

```bash
python3 ingest_history.py \
  --source google-sheet \
  --spreadsheet-url "https://docs.google.com/spreadsheets/d/your-sheet-id/edit#gid=0" \
  --sheet-name "Health" \
  --snapshot-date 2026-04-16
```

## What Gets Updated

Every successful sync updates:

- `data/processed/historical_spd_data.csv`
- `data/processed/sync_status.json`

The dashboard sidebar now shows:

- last sync time
- latest snapshot date
- sync failure message if the job breaks

## Recommended First Test

1. Add the GitHub secrets
2. Run the workflow manually once
3. Check that:
   - a new row set is appended
   - `sync_status.json` is updated
   - the Streamlit dashboard shows the new sync timestamp

## Failure Modes To Watch

- sheet tab name changed
- headers changed by Ops
- service-account access removed
- Google Sheet contains blank header rows
- required columns missing

If a sync fails, the workflow will stop and `sync_status.json` will record the error message.
