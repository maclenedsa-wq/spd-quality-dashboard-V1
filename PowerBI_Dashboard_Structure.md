# OMNI SPD Decision System

## Executive Intent
This is not a reporting dashboard. It is a decision system for senior leadership to answer three questions:

1. What is happening to SPD
2. Why it is happening
3. What Training, Operations, and Managers should do next

Source used:
- Excel: `Correlation __ OMNI - SPD_CES __ Mar2026 (1).xlsx`
- Sheet: `Health`
- Working population with valid SPD: `56` advisor records

## What The Data Says

### Baseline
- Avg SPD: `1.67`
- Avg Quality Score: `86.96`
- SPD P30: `1.25`
- SPD P70: `1.80`

### Critical analytical caveat
- Raw correlations are negative because one extreme outlier materially distorts the model:
  - `Chandana M` with SPD `7.00` and Quality Score `79.68`
- Therefore the dashboard must support:
  - `Raw View`
  - `Outlier Adjusted View`

### Driver readout
Raw correlation with SPD:

| Driver | Correlation |
|---|---:|
| Quality Score | -0.218 |
| Listening & Understanding Needs | -0.106 |
| Product Knowledge and Explanation | -0.209 |
| Transaction | -0.328 |
| Acknowledge & Empathise | -0.074 |
| Language, Tone and Professionalism | -0.297 |

Outlier-adjusted correlation with SPD:

| Driver | Correlation |
|---|---:|
| Listening & Understanding Needs | 0.236 |
| Transaction | 0.222 |
| Acknowledge & Empathise | 0.200 |
| Quality Score | 0.165 |
| Product Knowledge and Explanation | 0.155 |
| Language, Tone and Professionalism | 0.097 |

### High vs Low SPD gaps
Using outlier-adjusted data:

| Parameter | High SPD Avg | Low SPD Avg | Gap | Gap % vs Low SPD |
|---|---:|---:|---:|---:|
| Listening & Understanding Needs | 87.42 | 86.30 | 1.12 | 1.3% |
| Product Knowledge and Explanation | 84.72 | 83.80 | 0.92 | 1.1% |
| Transaction | 86.81 | 85.70 | 1.11 | 1.3% |
| Acknowledge & Empathise | 85.29 | 83.98 | 1.32 | 1.6% |
| Language, Tone and Professionalism | 91.60 | 91.39 | 0.22 | 0.2% |
| Quality Score | 87.03 | 86.23 | 0.80 | 0.9% |

### So what
- High SPD is not being driven by broad-based quality score inflation.
- The real differentiators are conversational and conversion-critical behaviors:
  - `Listening & Understanding Needs`
  - `Transaction`
  - `Acknowledge & Empathise`
- `Language, Tone and Professionalism` is already high and relatively flat, so it is not the highest-return coaching lever.
- `Product Knowledge and Explanation` is the lowest-scoring quality dimension overall and should be treated as the biggest L&D gap.

### Team signal
- Lowest average SPD team: `Mohammed Sadiq Sharieff` at `1.04`
- Highest average SPD team in current file: `Vikram Kumar majhi` at `1.80`
- Largest consistency issues appear in:
  - `Jithin CJ` on `Empathise`
  - `Ashil Simon` on `Product Knowledge`, `Listening`, and `Transaction`

## Page-Wise Power BI Layout

## Page 1: Executive Insight Page

### Objective
Give leadership a one-screen answer to:
- Are we winning or losing on SPD
- Which quality behaviors matter most
- What action should leadership sponsor

### 12-column wireframe

#### Row 1: KPI Strip
- Col 1-3: `Avg SPD`
- Col 4-6: `Avg Quality Score`
- Col 7-9: `Strongest Driver`
- Col 10-12: `Weakest Driver`

#### Row 2: Core Story
- Col 1-7: Scatter plot `SPD vs Quality Score`
  - X-axis: `Quality Score`
  - Y-axis: `SPD`
  - Legend: `SPD Band`
  - Detail: `Agent Name`
  - Analytics: trend line
  - Add toggle/bookmark:
    - `Raw View`
    - `Outlier Adjusted View`
- Col 8-12: Insight panel
  - Dynamic narrative text, not a static text box
  - Must state:
    - what is happening
    - why it is happening
    - what to do next

#### Row 3: Driver Ranking
- Col 1-12: Horizontal bar chart
  - Axis: parameter
  - Value: correlation with SPD
  - Sorted descending
  - Conditional color:
    - green positive
    - red negative
    - grey neutral

### Leadership message on this page
- Raw view suggests inverse quality-SPD relationship, but this is distorted by one extreme SPD outlier.
- Once adjusted, the strongest SPD drivers are `Listening`, `Transaction`, and `Empathise`.
- This means the issue is less about “overall quality” and more about whether calls convert through need discovery, confident progression, and emotional handling.

## Page 2: Root Cause Analysis

### Objective
Show where performance breaks down by team, agent, and parameter.

### 12-column wireframe

#### Left filter rail: Col 1-2
- Slicer: `Agent Name`
- Slicer: `Team / Vendor`
- Slicer: `SPD Band`
- Toggle: `Raw View / Outlier Adjusted View`

#### Main area: Col 3-12

##### Row 1
- Col 3-12: Gap analysis chart
  - Clustered horizontal bars
  - Series 1: High SPD average
  - Series 2: Low SPD average
  - Delta label: High minus Low
  - Key message:
    - `Empathise` has the biggest gap
    - `Listening` and `Transaction` are next

##### Row 2
- Col 3-7: Team vs parameter heatmap
  - Rows: `Team / Vendor`
  - Columns: parameters
  - Values: average parameter score
  - Conditional formatting based on z-score or traffic-light bands
- Col 8-12: Decomposition tree
  - Analyze: `Avg SPD`
  - Explain by:
    - `Quality Score`
    - `Listening`
    - `Product Knowledge`
    - `Transaction`
    - `Empathise`
    - `Language Tone Professionalism`
    - `Team / Vendor`
    - `Agent Name`

##### Row 3
- Col 3-12: Failure panel table
  - Columns:
    - Team / Agent
    - SPD
    - Lowest parameter
    - Gap to high performers
    - Risk flag
  - Conditional icons:
    - red flag if low SPD and low top-driver score
    - amber if low SPD but quality stable
    - green if high SPD and consistent

### Root-cause message on this page
- Team underperformance is not uniform; it clusters around a few behaviors.
- `Mohammed Sadiq Sharieff` is the largest SPD concern.
- `Jithin CJ` shows an empathy stability problem.
- `Ashil Simon` shows broader execution inconsistency across product knowledge, listening, and transaction flow.

## Page 3: Action Dashboard

### Objective
Turn diagnosis into explicit actions by function.

### 12-column wireframe

#### Section 1: Training View
- Col 1-12
- Visuals:
  - Card: `Lowest Scoring Parameter`
  - Card: `Highest Impact Parameter`
  - Gap bar: high vs low SPD for priority parameters
  - Smart narrative block

Training page message:
- `Product Knowledge and Explanation` is the lowest-scoring parameter.
- `Listening & Understanding Needs` is the highest-impact behavioral driver.
- Implication:
  - L&D should not run generic communication refreshers.
  - L&D should build focused modules on discovery, objection-linked need diagnosis, and confident product explanation.

#### Section 2: Operations View
- Col 1-12
- Visuals:
  - Team variance matrix
  - Parameter consistency chart by team
  - Narrative block

Operations page message:
- `Jithin CJ` and `Ashil Simon` show the strongest intra-team variation, suggesting process adherence or enablement inconsistency rather than a pure skill issue.
- Ops should investigate:
  - call flow compliance
  - supervisor calibration
  - tool/process friction during transaction handling

#### Section 3: Manager Coaching View
- Col 1-12
- Visuals:
  - Low-SPD agent segmentation table
  - Radar chart: High vs Low SPD
  - Narrative block

Manager message:
- Managers should coach low-SPD agents first on:
  - `Listening & Understanding Needs`
  - `Acknowledge & Empathise`
  - `Transaction`
- Coaching should be targeted to closing discovery gaps, handling concern signals, and progressing the sale cleanly.

## Mandatory DAX Measures

## 1. Calculated Column
```DAX
SPD Band =
VAR P30 =
    PERCENTILEX.INC ( ALL ( Health ), Health[SPD], 0.3 )
VAR P70 =
    PERCENTILEX.INC ( ALL ( Health ), Health[SPD], 0.7 )
RETURN
    SWITCH (
        TRUE (),
        ISBLANK ( Health[SPD] ), BLANK (),
        Health[SPD] < P30, "Low",
        Health[SPD] < P70, "Medium",
        "High"
    )
```

## 2. Base Measures
```DAX
Avg SPD =
AVERAGE ( Health[SPD] )

Avg Quality =
AVERAGE ( Health[Quality Score] )

Avg Listening =
AVERAGE ( Health[Listening & Understanding Needs] )

Avg Product Knowledge =
AVERAGE ( Health[Product Knowledge and Explanation] )

Avg Transaction =
AVERAGE ( Health[Transaction] )

Avg Empathise =
AVERAGE ( Health[Acknowledge & Empathise] )

Avg Language Tone =
AVERAGE ( Health[Language, Tone and Professionalism] )
```

## 3. Correlation Measures
Important:
- Power BI DAX does not have a native `CORREL()` function.
- Use the Pearson correlation pattern below instead.

```DAX
Corr Quality =
VAR T =
    FILTER (
        ALLSELECTED ( Health ),
        NOT ISBLANK ( Health[SPD] )
            && NOT ISBLANK ( Health[Quality Score] )
    )
VAR AvgSPD = AVERAGEX ( T, Health[SPD] )
VAR AvgMetric = AVERAGEX ( T, Health[Quality Score] )
VAR Num =
    SUMX ( T, ( Health[SPD] - AvgSPD ) * ( Health[Quality Score] - AvgMetric ) )
VAR DenSPD =
    SUMX ( T, POWER ( Health[SPD] - AvgSPD, 2 ) )
VAR DenMetric =
    SUMX ( T, POWER ( Health[Quality Score] - AvgMetric, 2 ) )
RETURN
    DIVIDE ( Num, SQRT ( DenSPD * DenMetric ) )

Corr Listening =
VAR T =
    FILTER (
        ALLSELECTED ( Health ),
        NOT ISBLANK ( Health[SPD] )
            && NOT ISBLANK ( Health[Listening & Understanding Needs] )
    )
VAR AvgSPD = AVERAGEX ( T, Health[SPD] )
VAR AvgMetric = AVERAGEX ( T, Health[Listening & Understanding Needs] )
VAR Num =
    SUMX (
        T,
        ( Health[SPD] - AvgSPD ) * ( Health[Listening & Understanding Needs] - AvgMetric )
    )
VAR DenSPD = SUMX ( T, POWER ( Health[SPD] - AvgSPD, 2 ) )
VAR DenMetric =
    SUMX ( T, POWER ( Health[Listening & Understanding Needs] - AvgMetric, 2 ) )
RETURN
    DIVIDE ( Num, SQRT ( DenSPD * DenMetric ) )

Corr Product Knowledge =
VAR T =
    FILTER (
        ALLSELECTED ( Health ),
        NOT ISBLANK ( Health[SPD] )
            && NOT ISBLANK ( Health[Product Knowledge and Explanation] )
    )
VAR AvgSPD = AVERAGEX ( T, Health[SPD] )
VAR AvgMetric =
    AVERAGEX ( T, Health[Product Knowledge and Explanation] )
VAR Num =
    SUMX (
        T,
        ( Health[SPD] - AvgSPD )
            * ( Health[Product Knowledge and Explanation] - AvgMetric )
    )
VAR DenSPD = SUMX ( T, POWER ( Health[SPD] - AvgSPD, 2 ) )
VAR DenMetric =
    SUMX ( T, POWER ( Health[Product Knowledge and Explanation] - AvgMetric, 2 ) )
RETURN
    DIVIDE ( Num, SQRT ( DenSPD * DenMetric ) )

Corr Transaction =
VAR T =
    FILTER (
        ALLSELECTED ( Health ),
        NOT ISBLANK ( Health[SPD] )
            && NOT ISBLANK ( Health[Transaction] )
    )
VAR AvgSPD = AVERAGEX ( T, Health[SPD] )
VAR AvgMetric = AVERAGEX ( T, Health[Transaction] )
VAR Num =
    SUMX ( T, ( Health[SPD] - AvgSPD ) * ( Health[Transaction] - AvgMetric ) )
VAR DenSPD = SUMX ( T, POWER ( Health[SPD] - AvgSPD, 2 ) )
VAR DenMetric = SUMX ( T, POWER ( Health[Transaction] - AvgMetric, 2 ) )
RETURN
    DIVIDE ( Num, SQRT ( DenSPD * DenMetric ) )

Corr Empathise =
VAR T =
    FILTER (
        ALLSELECTED ( Health ),
        NOT ISBLANK ( Health[SPD] )
            && NOT ISBLANK ( Health[Acknowledge & Empathise] )
    )
VAR AvgSPD = AVERAGEX ( T, Health[SPD] )
VAR AvgMetric = AVERAGEX ( T, Health[Acknowledge & Empathise] )
VAR Num =
    SUMX (
        T,
        ( Health[SPD] - AvgSPD ) * ( Health[Acknowledge & Empathise] - AvgMetric )
    )
VAR DenSPD = SUMX ( T, POWER ( Health[SPD] - AvgSPD, 2 ) )
VAR DenMetric =
    SUMX ( T, POWER ( Health[Acknowledge & Empathise] - AvgMetric, 2 ) )
RETURN
    DIVIDE ( Num, SQRT ( DenSPD * DenMetric ) )

Corr Language Tone =
VAR T =
    FILTER (
        ALLSELECTED ( Health ),
        NOT ISBLANK ( Health[SPD] )
            && NOT ISBLANK ( Health[Language, Tone and Professionalism] )
    )
VAR AvgSPD = AVERAGEX ( T, Health[SPD] )
VAR AvgMetric =
    AVERAGEX ( T, Health[Language, Tone and Professionalism] )
VAR Num =
    SUMX (
        T,
        ( Health[SPD] - AvgSPD )
            * ( Health[Language, Tone and Professionalism] - AvgMetric )
    )
VAR DenSPD = SUMX ( T, POWER ( Health[SPD] - AvgSPD, 2 ) )
VAR DenMetric =
    SUMX ( T, POWER ( Health[Language, Tone and Professionalism] - AvgMetric, 2 ) )
RETURN
    DIVIDE ( Num, SQRT ( DenSPD * DenMetric ) )
```

## 4. Gap Measures
```DAX
Gap Listening =
CALCULATE (
    AVERAGE ( Health[Listening & Understanding Needs] ),
    Health[SPD Band] = "High"
)
-
CALCULATE (
    AVERAGE ( Health[Listening & Understanding Needs] ),
    Health[SPD Band] = "Low"
)

Gap Product Knowledge =
CALCULATE (
    AVERAGE ( Health[Product Knowledge and Explanation] ),
    Health[SPD Band] = "High"
)
-
CALCULATE (
    AVERAGE ( Health[Product Knowledge and Explanation] ),
    Health[SPD Band] = "Low"
)

Gap Transaction =
CALCULATE (
    AVERAGE ( Health[Transaction] ),
    Health[SPD Band] = "High"
)
-
CALCULATE (
    AVERAGE ( Health[Transaction] ),
    Health[SPD Band] = "Low"
)

Gap Empathise =
CALCULATE (
    AVERAGE ( Health[Acknowledge & Empathise] ),
    Health[SPD Band] = "High"
)
-
CALCULATE (
    AVERAGE ( Health[Acknowledge & Empathise] ),
    Health[SPD Band] = "Low"
)

Gap Language Tone =
CALCULATE (
    AVERAGE ( Health[Language, Tone and Professionalism] ),
    Health[SPD Band] = "High"
)
-
CALCULATE (
    AVERAGE ( Health[Language, Tone and Professionalism] ),
    Health[SPD Band] = "Low"
)
```

## 5. Driver Ranking Table
Create a disconnected table:

```DAX
Driver Table =
DATATABLE (
    "Driver", STRING,
    {
        { "Listening & Understanding Needs" },
        { "Product Knowledge and Explanation" },
        { "Transaction" },
        { "Acknowledge & Empathise" },
        { "Language, Tone and Professionalism" },
        { "Quality Score" }
    }
)
```

```DAX
Driver Correlation =
SWITCH (
    SELECTEDVALUE ( 'Driver Table'[Driver] ),
    "Listening & Understanding Needs", [Corr Listening],
    "Product Knowledge and Explanation", [Corr Product Knowledge],
    "Transaction", [Corr Transaction],
    "Acknowledge & Empathise", [Corr Empathise],
    "Language, Tone and Professionalism", [Corr Language Tone],
    "Quality Score", [Corr Quality]
)

Driver Rank =
RANKX (
    ALLSELECTED ( 'Driver Table'[Driver] ),
    [Driver Correlation],
    ,
    DESC
)
```

## 6. Top/Bottom Driver Logic
```DAX
Top Driver Name =
MAXX (
    TOPN ( 1, ALLSELECTED ( 'Driver Table' ), [Driver Correlation], DESC ),
    'Driver Table'[Driver]
)

Weakest Driver Name =
MAXX (
    TOPN ( 1, ALLSELECTED ( 'Driver Table' ), [Driver Correlation], ASC ),
    'Driver Table'[Driver]
)

Lowest Parameter Name =
VAR T =
    UNION (
        ROW ( "Parameter", "Listening & Understanding Needs", "Score", [Avg Listening] ),
        ROW ( "Parameter", "Product Knowledge and Explanation", "Score", [Avg Product Knowledge] ),
        ROW ( "Parameter", "Transaction", "Score", [Avg Transaction] ),
        ROW ( "Parameter", "Acknowledge & Empathise", "Score", [Avg Empathise] ),
        ROW ( "Parameter", "Language, Tone and Professionalism", "Score", [Avg Language Tone] )
    )
RETURN
    MAXX ( TOPN ( 1, T, [Score], ASC ), [Parameter] )
```

## 7. Variance Proxy Measures
```DAX
Listening Variance by Team =
VAR TeamAvg =
    AVERAGEX ( VALUES ( Health[Team / Vendor] ), [Avg Listening] )
RETURN
    STDEVX.P ( VALUES ( Health[Team / Vendor] ), [Avg Listening] )

Product Knowledge Variance by Team =
STDEVX.P ( VALUES ( Health[Team / Vendor] ), [Avg Product Knowledge] )

Transaction Variance by Team =
STDEVX.P ( VALUES ( Health[Team / Vendor] ), [Avg Transaction] )

Empathise Variance by Team =
STDEVX.P ( VALUES ( Health[Team / Vendor] ), [Avg Empathise] )
```

## Dynamic Insight Text Measures

## Core page insights
```DAX
Top Driver Insight =
"SPD is most strongly driven by " & [Top Driver Name]

Weakest Driver Insight =
[Weakest Driver Name] & " has the weakest relationship with SPD in the current selection"

Gap Insight =
"High performers score " &
FORMAT (
    DIVIDE ( [Gap Empathise], CALCULATE ( [Avg Empathise], Health[SPD Band] = "Low" ) ),
    "0%"
) &
" higher in Acknowledge & Empathise"
```

## Training insights
```DAX
Training Insight =
"Training should prioritize " & [Lowest Parameter Name] &
" while reinforcing " & [Top Driver Name] &
" because that combination addresses the biggest quality shortfall and the strongest SPD lever."
```

## Operations insights
```DAX
Lowest SPD Team =
MAXX (
    TOPN (
        1,
        SUMMARIZE ( Health, Health[Team / Vendor], "TeamSPD", [Avg SPD] ),
        [TeamSPD], ASC
    ),
    Health[Team / Vendor]
)

Ops Insight =
"Team " & [Lowest SPD Team] &
" is the clearest operational red flag. Review transaction flow, calibration discipline, and enablement support before treating this as a pure training problem."
```

## Manager insights
```DAX
Manager Insight =
"Managers should coach low-SPD agents on Listening & Understanding Needs, Acknowledge & Empathise, and Transaction to improve need diagnosis, confidence, and progression to sale."
```

## Smart Narrative Starter Copy
Use the Smart Narrative visual, but overwrite the bland default text with a measure-driven narrative:

> SPD is not being driven by overall quality in a simple linear way. The raw view is distorted by an extreme high-SPD outlier, but the adjusted view shows that Listening, Transaction, and Empathise are the clearest drivers of sales performance. Product Knowledge is the weakest average quality behavior, making it the biggest L&D opportunity. Team underperformance is concentrated rather than broad-based, with the largest execution concerns in Mohammed Sadiq Sharieff, and consistency risks visible in Jithin CJ and Ashil Simon.

## How To Interpret The Dashboard

### Page 1
- Use this to decide where leadership attention should go.
- If the driver ranking changes materially between Raw and Outlier Adjusted view, trust the adjusted view for action design.

### Page 2
- Use this to locate the breakdown:
  - team issue
  - agent issue
  - parameter issue
- Focus on patterns that show both:
  - low SPD
  - weak scores on top drivers

### Page 3
- Use this as the decision page:
  - Training owns lowest-scoring and highest-impact skills
  - Operations owns variance and process inconsistency
  - Managers own low-SPD coaching on discovery, empathy, and transaction progression

## Recommended Leadership Actions

### Training
- Prioritize `Product Knowledge and Explanation` as the foundational content fix.
- Build targeted reinforcement on `Listening` and `Empathise` because these are more linked to SPD movement.

### Operations
- Investigate `Mohammed Sadiq Sharieff` for systemic low-SPD conditions.
- Audit `Jithin CJ` and `Ashil Simon` for calibration, workflow consistency, and process adherence.

### Frontline Managers
- Coach low-SPD agents on:
  - discovery questioning
  - empathy handling
  - transaction confidence
- Avoid over-indexing on tone/polish coaching, because that is not the main performance bottleneck here.

## Self-Audit
- Driver identification included: `Yes`
- Gap analysis included: `Yes`
- Training, Ops, Manager actions included: `Yes`
- Dashboard answers “So what?” and “What next?” on every page: `Yes`
