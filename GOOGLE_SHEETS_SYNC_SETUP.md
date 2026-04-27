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
4. Configure `Workload Identity Federation` for GitHub Actions
5. Share the target Google Sheet with the service account email as a viewer

Important:
If the sheet lives in a Shared Drive, the service account must also have access through that drive or directly to the sheet.

## GitHub Secrets To Add

In your GitHub repository, add these secrets:

- `GCP_WORKLOAD_IDENTITY_PROVIDER`
  - full provider resource name, for example `projects/123456789/locations/global/workloadIdentityPools/github/providers/my-repo`
- `GCP_SERVICE_ACCOUNT_EMAIL`
  - the service account email used by the workflow
- `GOOGLE_SHEETS_URL`
  - the full Google Sheets URL
- `GOOGLE_SHEETS_WORKSHEET`
  - usually `Health`
- `GOOGLE_SHEETS_RANGE`
  - optional, for example `A:Z`

Also confirm repository Actions can write commits:

- GitHub repository -> Settings -> Actions -> General
- Workflow permissions: `Read and write permissions`

The workflow requests `contents: write` and `id-token: write` in YAML. `contents: write`
is needed to push the refreshed CSV back to the repo. `id-token: write` is needed so
GitHub Actions can request an OIDC token and exchange it for Google credentials.

## Google Cloud Setup

This repo now uses keyless authentication for automation:

1. Create a service account for the sync, for example `github-sheet-sync`
2. Share the Google Sheet with that service account email
3. Create a workload identity pool, for example `github`
4. Create an OIDC provider in that pool for GitHub
5. Restrict the provider with an attribute condition such as:
   - `assertion.repository_owner=='YOUR_GITHUB_ORG' && assertion.ref=='refs/heads/main'`
6. Grant the GitHub external identity access to impersonate the service account with:
   - `roles/iam.workloadIdentityUser`

You can also restrict access more tightly to a single repository by using GitHub token
attributes such as `assertion.repository`.

## Local Test

For local testing, use Application Default Credentials instead of storing a long-lived key.

If your organization provides an ADC bootstrap command, run that first. Example:

```bash
bash <(curl -sSL https://storage.googleapis.com/cloud-samples-data/adc/setup_adc.sh)
```

Then run:

```bash
python3 ingest_history.py \
  --source google-sheet \
  --spreadsheet-url "https://docs.google.com/spreadsheets/d/your-sheet-id/edit#gid=0" \
  --sheet-name "Health" \
  --snapshot-date 2026-04-16
```

If you already have local ADC configured through another approved method, that works too.
The script also still accepts `GOOGLE_SERVICE_ACCOUNT_JSON` or `GOOGLE_SERVICE_ACCOUNT_FILE`
as a fallback for non-production testing.

## Workflow

The workflow file is:

- `.github/workflows/daily_google_sheet_sync.yml`

It runs:

- automatically every day at `9:00 AM IST`
- manually via `workflow_dispatch`

## What Gets Updated

Every successful sync updates:

- `data/processed/historical_spd_data.csv`
- `data/processed/sync_status.json`

Failed syncs also update `data/processed/sync_status.json` so the dashboard can show the
actual failure reason instead of silently staying stale.

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
- workload identity provider misconfigured
- service-account access removed
- Google Sheet contains blank header rows
- required columns missing

If a sync fails, the workflow will stop and `sync_status.json` will record the error message.
