# codex.md

## Objective
Analyze the relationship between **Sales (SPD)** and **Quality Scores** using the Health sheet from the provided Excel file.

The goal is to:
- Identify correlation between SPD and overall Quality Score
- Break down Quality Score into sub-parameters
- Identify which sub-parameters most influence sales performance
- Highlight improvement areas

---

## Data Source
- File: Correlation __ OMNI - SPD_CES __ Mar2026.xlsx
- Sheet: **Health**

---

## Key Metrics

### Target Variable
- **SPD (Sales Per Day / Sales Performance)**

### Quality Score (Overall)
- Overall Quality Score column

### Sub-Parameters
1. Listening & Understanding Needs
2. Product Knowledge and Explanation
3. Transaction
4. Acknowledge & Empathise
5. Language, Tone and Professionalism

---

## Analysis Steps

### Step 1: Data Preparation
- Load Health sheet
- Clean column names (trim spaces, standardize)
- Handle missing/null values
- Convert all score columns to numeric

### Step 2: Exploratory Analysis
- Summary statistics (mean, median, std)
- Distribution of SPD and Quality Score
- Check for outliers

### Step 3: Correlation Analysis

#### 3.1 Overall Correlation
- Calculate correlation between:
  - SPD vs Overall Quality Score

#### 3.2 Sub-Parameter Correlation
- Calculate correlation between SPD and each sub-parameter:
  - SPD vs Listening & Understanding Needs
  - SPD vs Product Knowledge and Explanation
  - SPD vs Transaction
  - SPD vs Acknowledge & Empathise
  - SPD vs Language, Tone and Professionalism

- Use Pearson correlation coefficient

---

### Step 4: Impact Analysis
- Rank sub-parameters based on correlation strength with SPD
- Identify:
  - Strong positive drivers (high correlation)
  - Weak or no impact areas
  - Negative correlations (if any)

---

### Step 5: Segmentation Analysis
- Bucket agents into SPD bands (Low, Medium, High)
- Compare average sub-parameter scores across buckets

---

### Step 6: Visualization
Create the following charts:
- Correlation heatmap
- Scatter plots:
  - SPD vs Overall Quality
  - SPD vs each sub-parameter
- Bar chart of correlation values

---

## Expected Outputs

### 1. Correlation Table
| Parameter | Correlation with SPD |
|----------|----------------------|
| Overall Quality | X |
| Listening & Understanding | X |
| Product Knowledge | X |
| Transaction | X |
| Empathy | X |
| Language & Tone | X |

### 2. Key Insights
- Top 2–3 drivers of sales performance
- Lowest contributing parameter
- Any surprising trends

### 3. Recommendations
- Focus areas for training
- Behavioural gaps impacting sales

---

## Sample Python Workflow

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data
file_path = "Correlation __ OMNI - SPD_CES __ Mar2026.xlsx"
df = pd.read_excel(file_path, sheet_name="Health")

# Clean columns
df.columns = df.columns.str.strip()

# Define columns
spd_col = "SPD"
quality_col = "Quality Score"
sub_params = [
    "Listening & Understanding Needs",
    "Product Knowledge and Explanation",
    "Transaction",
    "Acknowledge & Empathise",
    "Language, Tone and Professionalism"
]

# Convert to numeric
cols = [spd_col, quality_col] + sub_params
for col in cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Drop missing
analysis_df = df[cols].dropna()

# Correlation
corr = analysis_df.corr()

# Extract SPD correlations
spd_corr = corr[spd_col].sort_values(ascending=False)
print(spd_corr)

# Heatmap
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title("Correlation Matrix")
plt.show()

# Scatter plots
for col in sub_params:
    sns.scatterplot(data=analysis_df, x=col, y=spd_col)
    plt.title(f"SPD vs {col}")
    plt.show()
```

---

## Interpretation Guide

| Correlation Value | Meaning |
|------------------|--------|
| 0.7 to 1.0 | Strong impact |
| 0.4 to 0.7 | Moderate impact |
| 0.1 to 0.4 | Weak impact |
| 0 to 0.1 | No impact |

---

## Final Outcome
This analysis will clearly answer:
- Does quality drive sales?
- Which behaviors actually move SPD?
- Where should training investment go?

---

## Notes
- Ensure column names exactly match sheet
- Validate SPD definition before analysis
- Check if weighting exists in quality score

