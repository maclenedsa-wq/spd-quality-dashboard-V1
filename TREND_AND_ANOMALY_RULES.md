# Trend And Anomaly Rules

This document defines the first set of momentum and anomaly rules to activate once multiple snapshot dates exist in the historical dataset.

## Activation Threshold

`2 snapshots`

- latest vs previous comparison
- simple delta cards

`4 snapshots`

- usable momentum scoring
- improving vs declining ranking
- early anomaly warnings

`8+ snapshots`

- more stable anomaly thresholds
- forecast-ready patterns

## Core Trend Metrics

- SPD change vs previous snapshot
- quality change vs previous snapshot
- positive intent change
- payment completion change
- unresolved risk change
- follow-up required change

## Team Momentum Rules

`Improving team`

- latest SPD greater than previous SPD
- and unresolved risk is flat or improving

`Declining team`

- latest SPD lower than previous SPD
- and unresolved risk is worsening

`High volatility team`

- SPD direction changes sharply across recent snapshots
- or quality/SPD movement becomes inconsistent

## Early Anomaly Rules

These should be rule-based first.

`SPD drop anomaly`

- latest SPD falls more than a chosen threshold vs previous snapshot
- suggested starting threshold: `-0.20`

`Quality drop anomaly`

- latest quality score falls more than a chosen threshold
- suggested starting threshold: `-1.50`

`Unresolved spike anomaly`

- unresolved risk rate increases materially vs previous snapshot
- suggested starting threshold: `+3 percentage points`

`Payment completion drop anomaly`

- payment completion rate falls materially vs previous snapshot
- suggested starting threshold: `-3 percentage points`

`Follow-up leakage anomaly`

- positive intent rises but payment completion does not improve
- and follow-up required increases

## Recommended Dashboard Flags

`Green`

- improving SPD
- stable or improving unresolved risk

`Amber`

- mixed movement
- one negative signal without major breakdown

`Red`

- SPD declining
- unresolved risk worsening
- payment completion falling

## First Trend Narrative Logic

Once at least 2 snapshots exist, the dashboard should summarize:

- what improved
- what worsened
- which team moved the most
- whether the business is becoming healthier or riskier

Example narrative:

- SPD improved by `0.12` vs the previous snapshot, but unresolved risk rose by `2.5pp`, suggesting productivity is improving while resolution quality is weakening.

## Future Phase 3 Upgrade Path

Once enough snapshots exist, these rules can evolve into:

- rolling averages
- z-score based anomaly detection
- forecast confidence bands
- expected trend baselines
- auto-generated anomaly explanations
