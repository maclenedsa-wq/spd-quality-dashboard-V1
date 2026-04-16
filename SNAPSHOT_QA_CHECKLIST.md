# Snapshot QA Checklist

Use this checklist before and after ingesting each weekly snapshot.

## Before Ingestion

`File checks`

- file is saved with date in filename
- file is placed in `data/raw/`
- file opens successfully
- correct sheet exists: `Health`

`Structure checks`

- `Campaign` column exists
- `Team Leader` or mapped team column exists
- `Advisor` column exists
- `SPD/Agent` column exists
- quality parameter columns exist
- disposition columns exist

`Content checks`

- no repeated header row inside the data body
- agent rows look real
- SPD values are numeric
- quality values are numeric
- no obvious blank dataset

## After Ingestion

`Script output checks`

- ingestion completed successfully
- snapshot date is correct
- duplicates removed count looks reasonable
- row count is plausible

`Processed data checks`

- `data/processed/historical_spd_data.csv` exists
- new snapshot date is present
- row count increased as expected
- no obvious duplicate rows for the same snapshot/agent/campaign

`Dashboard checks`

- new snapshot appears in the sidebar snapshot filter
- `Trends` page loads
- latest snapshot KPI values look plausible
- no broken pages or empty charts under normal filters

## Warning Signs

Investigate if:

- row count suddenly drops sharply
- row count suddenly doubles unexpectedly
- all values for a major KPI are blank
- many agents disappear unexpectedly
- team names change formatting between weeks
- the file contains summary rows mixed into detail rows

## Escalation Rule

Do not treat the snapshot as trustworthy until:

- ingestion succeeds
- row count is plausible
- snapshot date is correct
- dashboard renders normally
