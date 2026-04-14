from __future__ import annotations

import streamlit as st
import numpy as np
import pandas as pd
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="OMNI SPD Decision System",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🚀 App Loaded Successfully")
st.write("v2 deployment fix")

DATA_FILE = Path(__file__).parent / "data.xlsx"
SHEET_NAME = "Health"

BG = "#F4F7FB"
SURFACE = "#FFFFFF"
TEXT = "#111827"
MUTED = "#5F6B7A"
GREEN = "#0F9D58"
RED = "#D93025"
AMBER = "#B45309"
BLUE = "#2563EB"
TEAL = "#0F766E"
SLATE = "#CBD5E1"
NAVY = "#0F172A"

PARAMETERS = {
    "Listening & Understanding Needs": "Listening",
    "Product Knowledge and Explanation": "Product Knowledge",
    "Transaction": "Transaction",
    "Acknowledge & Empathise": "Empathise",
    "Language, Tone and Professionalism": "Language Tone Professionalism",
}
KEY_DRIVER_ORDER = [
    "Listening & Understanding Needs",
    "Transaction",
    "Acknowledge & Empathise",
]


def inject_css() -> None:
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: radial-gradient(circle at top left, #FFFFFF 0%, {BG} 55%);
            color: {TEXT};
        }}
        .block-container {{
            padding-top: 1.2rem;
            padding-bottom: 2rem;
            max-width: 1500px;
        }}
        .hero-card {{
            background: linear-gradient(135deg, {NAVY} 0%, #1E3A8A 100%);
            color: #FFFFFF;
            border-radius: 24px;
            padding: 1.25rem 1.35rem;
            margin-bottom: 1rem;
            box-shadow: 0 16px 40px rgba(15, 23, 42, 0.18);
        }}
        .hero-title {{
            font-size: 1.35rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
        }}
        .hero-sub {{
            font-size: 0.92rem;
            color: rgba(255,255,255,0.78);
        }}
        .metric-card {{
            background: {SURFACE};
            border: 1px solid #E5E7EB;
            border-radius: 18px;
            padding: 1rem 1.05rem;
            min-height: 126px;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
        }}
        .metric-label {{
            color: {MUTED};
            font-size: 0.80rem;
            letter-spacing: 0.02em;
            margin-bottom: 0.35rem;
        }}
        .metric-value {{
            color: {TEXT};
            font-size: 1.85rem;
            font-weight: 700;
            line-height: 1.08;
        }}
        .metric-sub {{
            color: {MUTED};
            font-size: 0.82rem;
            margin-top: 0.45rem;
            line-height: 1.35;
        }}
        .section-card {{
            background: {SURFACE};
            border: 1px solid #E5E7EB;
            border-radius: 20px;
            padding: 1rem 1rem 0.65rem 1rem;
            box-shadow: 0 10px 28px rgba(15, 23, 42, 0.05);
            margin-bottom: 1rem;
        }}
        .insight-card {{
            background: linear-gradient(135deg, #FFFFFF 0%, #F0F7FF 100%);
            border: 1px solid #D8E5F7;
            border-radius: 20px;
            padding: 1rem 1.05rem;
            min-height: 455px;
        }}
        .section-title {{
            color: {TEXT};
            font-size: 1rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }}
        .tiny-label {{
            color: {MUTED};
            font-size: 0.74rem;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            margin-bottom: 0.25rem;
        }}
        .insight-line {{
            color: {TEXT};
            font-size: 0.95rem;
            line-height: 1.55;
            margin-bottom: 0.75rem;
        }}
        .pill {{
            display: inline-block;
            padding: 0.28rem 0.6rem;
            border-radius: 999px;
            margin-right: 0.35rem;
            margin-bottom: 0.35rem;
            font-size: 0.76rem;
            font-weight: 700;
        }}
        .pill-green {{
            background: #DCFCE7;
            color: #166534;
        }}
        .pill-red {{
            background: #FEE2E2;
            color: #991B1B;
        }}
        .pill-amber {{
            background: #FEF3C7;
            color: #92400E;
        }}
        .action-card {{
            background: {SURFACE};
            border: 1px solid #E5E7EB;
            border-left: 5px solid {BLUE};
            border-radius: 20px;
            padding: 1rem 1.05rem;
            box-shadow: 0 10px 28px rgba(15, 23, 42, 0.05);
            min-height: 250px;
        }}
        .action-title {{
            color: {TEXT};
            font-size: 1rem;
            font-weight: 700;
            margin-bottom: 0.6rem;
        }}
        .action-body {{
            color: {TEXT};
            font-size: 0.94rem;
            line-height: 1.55;
        }}
        .small-note {{
            color: {MUTED};
            font-size: 0.8rem;
            line-height: 1.45;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    df = pd.read_excel(DATA_FILE, sheet_name=SHEET_NAME)
    df = df.rename(
        columns={
            "Advisor": "Agent Name",
            "Team Leader": "Team / Vendor",
            "SPD/Agent": "SPD",
            "Quality Score": "Overall Quality Score",
            "Listening & Understanding Needs": "Listening",
            "Product Knowledge and Explanation": "Product Knowledge",
            "Acknowledge & Empathise": "Empathise",
            "Language, Tone and Professionalism": "Language Tone Professionalism",
        }
    )

    text_columns = ["Campaign", "Team / Vendor", "ECN", "Agent Name"]
    numeric_columns = ["SPD", "Overall Quality Score", *PARAMETERS.values()]

    for column in text_columns:
        if column in df.columns:
            df[column] = df[column].astype("string").str.strip()

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    df = df[df["Agent Name"].notna()].copy()
    df["Is Outlier SPD"] = df["SPD"] > 3

    valid_spd = df["SPD"].dropna()
    p30 = valid_spd.quantile(0.30, interpolation="linear")
    p70 = valid_spd.quantile(0.70, interpolation="linear")
    df["SPD Band"] = pd.cut(
        df["SPD"],
        bins=[-np.inf, p30, p70, np.inf],
        labels=["Low", "Medium", "High"],
        include_lowest=True,
    ).astype("string")

    return df


def safe_corr(df: pd.DataFrame, x_col: str, y_col: str) -> float:
    pair = df[[x_col, y_col]].dropna()
    if len(pair) < 3:
        return np.nan
    x = pair[x_col].astype(float).to_numpy()
    y = pair[y_col].astype(float).to_numpy()
    if np.std(x) == 0 or np.std(y) == 0:
        return np.nan
    return float(np.corrcoef(x, y)[0, 1])


def format_pct(value: float) -> str:
    if pd.isna(value):
        return "-"
    return f"{value:.1f}%"


def normalize(series: pd.Series) -> pd.Series:
    series = series.astype(float)
    if series.isna().all():
        return pd.Series([0.0] * len(series), index=series.index)
    min_v = series.min()
    max_v = series.max()
    if pd.isna(min_v) or pd.isna(max_v) or max_v == min_v:
        return pd.Series([0.5] * len(series), index=series.index)
    return (series - min_v) / (max_v - min_v)


def add_trendline(fig: go.Figure, df: pd.DataFrame, x_col: str, y_col: str, row=None, col=None) -> None:
    pair = df[[x_col, y_col]].dropna().sort_values(x_col)
    if len(pair) < 2:
        return
    slope, intercept = np.polyfit(pair[x_col], pair[y_col], deg=1)
    x_vals = np.array([pair[x_col].min(), pair[x_col].max()])
    y_vals = slope * x_vals + intercept
    trace = go.Scatter(
        x=x_vals,
        y=y_vals,
        mode="lines",
        line=dict(color=BLUE, width=2, dash="dash"),
        showlegend=False,
        hoverinfo="skip",
    )
    if row is None or col is None:
        fig.add_trace(trace)
    else:
        fig.add_trace(trace, row=row, col=col)


def hero(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="hero-card">
            <div class="hero-title">Sales Performance Dashboard</div>
            <div class="hero-sub">OMNI Co-relation</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def metric_card(label: str, value: str, subtext: str = "") -> None:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-sub">{subtext}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_open() -> None:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)


def section_close() -> None:
    st.markdown("</div>", unsafe_allow_html=True)


def filter_data(df: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    st.sidebar.title("OMNI Decision System")
    st.sidebar.caption("Executive version")
    st.sidebar.markdown("## Filters")

    teams = sorted(df["Team / Vendor"].dropna().unique().tolist())
    agents = sorted(df["Agent Name"].dropna().unique().tolist())
    campaigns = sorted(df["Campaign"].dropna().unique().tolist())

    selected_team = st.sidebar.multiselect("Team / Vendor", teams)
    selected_agents = st.sidebar.multiselect("Agent Name", agents)
    selected_band = st.sidebar.multiselect(
        "SPD Band",
        ["Low", "Medium", "High"],
        default=["Low", "Medium", "High"],
    )
    selected_campaign = st.sidebar.multiselect("Campaign", campaigns)
    outlier_mode = st.sidebar.radio(
        "Analytical view",
        ["Outlier-adjusted view", "Raw view"],
        help="Outlier-adjusted excludes SPD values above 3 to keep the driver model more stable.",
    )

    filtered = df.copy()
    if selected_team:
        filtered = filtered[filtered["Team / Vendor"].isin(selected_team)]
    if selected_agents:
        filtered = filtered[filtered["Agent Name"].isin(selected_agents)]
    if selected_band:
        filtered = filtered[filtered["SPD Band"].isin(selected_band)]
    if selected_campaign:
        filtered = filtered[filtered["Campaign"].isin(selected_campaign)]
    if outlier_mode == "Outlier-adjusted view":
        filtered = filtered[~filtered["Is Outlier SPD"]]

    st.sidebar.markdown("---")
    st.sidebar.caption(
        f"{filtered['Agent Name'].nunique()} agents | {filtered['Team / Vendor'].nunique()} teams | {filtered['SPD'].notna().sum()} SPD rows"
    )
    return filtered, outlier_mode


def get_parameter_metrics(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for label, column in PARAMETERS.items():
        high = df.loc[df["SPD Band"] == "High", column].mean()
        low = df.loc[df["SPD Band"] == "Low", column].mean()
        gap = high - low
        gap_pct = (gap / low * 100) if pd.notna(low) and low not in (0, np.nan) else np.nan
        corr = safe_corr(df, "SPD", column)
        variance_pct = (df[column].std() / df[column].mean() * 100) if df[column].mean() else np.nan
        rows.append(
            {
                "Parameter": label,
                "Column": column,
                "Average Score": df[column].mean(),
                "Correlation": corr,
                "SPD Variance Explained %": (corr ** 2 * 100) if pd.notna(corr) else np.nan,
                "High SPD Avg": high,
                "Low SPD Avg": low,
                "Gap": gap,
                "Gap %": gap_pct,
                "Variance %": variance_pct,
            }
        )

    metrics = pd.DataFrame(rows)
    metrics["Corr Score"] = normalize(metrics["Correlation"].fillna(metrics["Correlation"].min()))
    metrics["Gap Score"] = normalize(metrics["Gap"].fillna(metrics["Gap"].min()))
    metrics["Low Score Penalty"] = normalize((100 - metrics["Average Score"]).fillna(0))
    metrics["Driver Score"] = (
        metrics["Corr Score"] * 0.5
        + metrics["Gap Score"] * 0.3
        + metrics["Low Score Penalty"] * 0.2
    ) * 100
    metrics["Action Priority"] = np.select(
        [
            (metrics["Driver Score"] >= 70) & (metrics["Average Score"] < 86),
            (metrics["Driver Score"] >= 55),
        ],
        ["Fix Now", "Coach Next"],
        default="Sustain",
    )
    return metrics.sort_values(["Driver Score", "Correlation"], ascending=False).reset_index(drop=True)


def get_team_metrics(df: pd.DataFrame, parameter_metrics: pd.DataFrame) -> pd.DataFrame:
    rows = []
    driver_cols = parameter_metrics.sort_values("Driver Score", ascending=False).head(3)["Column"].tolist()
    high_spd = df["SPD"].quantile(0.7) if df["SPD"].notna().any() else np.nan

    for team, group in df.groupby("Team / Vendor", dropna=False):
        if len(group) == 0:
            continue
        parameter_means = group[list(PARAMETERS.values())].mean().astype(float)
        if parameter_means.isna().all():
            weakest_label = "No valid parameter score"
        else:
            weakest_idx = parameter_means.idxmin()
            weakest_label = next(label for label, col in PARAMETERS.items() if col == weakest_idx)
        consistency_values = [group[col].std() for col in PARAMETERS.values()]
        consistency = (
            float(np.nanmean(consistency_values))
            if any(pd.notna(v) for v in consistency_values)
            else np.nan
        )
        low_driver_values = [group[col].mean() for col in driver_cols] if driver_cols else []
        low_driver = (
            float(np.nanmean(low_driver_values))
            if any(pd.notna(v) for v in low_driver_values)
            else np.nan
        )
        risk_parts = []
        if group["SPD"].mean() <= df["SPD"].quantile(0.3):
            risk_parts.append("Low SPD")
        if consistency >= np.nanmean([df[col].std() for col in PARAMETERS.values()]):
            risk_parts.append("Inconsistent execution")
        if pd.notna(low_driver) and low_driver < df[driver_cols].mean().mean():
            risk_parts.append("Weak driver behaviors")
        risk_flag = ", ".join(risk_parts) if risk_parts else "Stable"

        rows.append(
            {
                "Team / Vendor": team,
                "Avg SPD": group["SPD"].mean(),
                "Avg Quality": group["Overall Quality Score"].mean(),
                "Agents": group["Agent Name"].nunique(),
                "Consistency Score": consistency,
                "Weakest Parameter": weakest_label,
                "Top Driver Index": low_driver,
                "High SPD Share %": (group["SPD"] >= high_spd).mean() * 100 if pd.notna(high_spd) else np.nan,
                "Risk Flag": risk_flag,
            }
        )

    team_metrics = pd.DataFrame(rows)
    if team_metrics.empty:
        return team_metrics

    team_metrics["Priority Score"] = (
        normalize((team_metrics["Avg SPD"].max() - team_metrics["Avg SPD"]).fillna(0)) * 0.5
        + normalize(team_metrics["Consistency Score"].fillna(0)) * 0.3
        + normalize((team_metrics["Top Driver Index"].max() - team_metrics["Top Driver Index"]).fillna(0)) * 0.2
    ) * 100
    return team_metrics.sort_values(["Priority Score", "Avg SPD"], ascending=[False, True]).reset_index(drop=True)


def get_agent_risks(df: pd.DataFrame, parameter_metrics: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()

    top3 = parameter_metrics.sort_values("Driver Score", ascending=False).head(3)
    high_group = df[df["SPD Band"] == "High"]
    if high_group.empty:
        high_group = df.copy()

    benchmark = {row["Column"]: high_group[row["Column"]].mean() for _, row in top3.iterrows()}
    low_cut = df["SPD"].quantile(0.3)

    rows = []
    for _, row in df.iterrows():
        gap_cols = []
        total_gap = 0.0
        for _, driver in top3.iterrows():
            col = driver["Column"]
            label = driver["Parameter"]
            target = benchmark.get(col, np.nan)
            gap = target - row[col] if pd.notna(target) and pd.notna(row[col]) else 0
            if gap > 0.6:
                gap_cols.append(label)
            total_gap += max(gap, 0)

        if row["SPD"] <= low_cut and total_gap >= 1.5:
            bucket = "Fix Now"
            owner = "Manager + Training"
        elif row["SPD"] <= low_cut:
            bucket = "Coach Now"
            owner = "Manager"
        elif total_gap >= 1.5:
            bucket = "Monitor"
            owner = "Training"
        else:
            bucket = "Sustain"
            owner = "Manager"

        rows.append(
            {
                "Agent Name": row["Agent Name"],
                "Team / Vendor": row["Team / Vendor"],
                "SPD": row["SPD"],
                "SPD Band": row["SPD Band"],
                "Priority Bucket": bucket,
                "Owner": owner,
                "Gap Score": total_gap,
                "Coach On": ", ".join(gap_cols[:2]) if gap_cols else "Maintain current behaviors",
                "Overall Quality Score": row["Overall Quality Score"],
            }
        )

    risks = pd.DataFrame(rows)
    order = ["Fix Now", "Coach Now", "Monitor", "Sustain"]
    risks["Priority Bucket"] = pd.Categorical(risks["Priority Bucket"], order, ordered=True)
    return risks.sort_values(["Priority Bucket", "Gap Score", "SPD"], ascending=[True, False, True]).reset_index(drop=True)


def selection_label(df: pd.DataFrame) -> str:
    teams = sorted(df["Team / Vendor"].dropna().unique().tolist())
    if len(teams) == 1:
        return teams[0]
    if len(teams) > 1:
        return f"{len(teams)} teams selected"
    return "Current filter selection"


def decision_snapshot(
    df: pd.DataFrame,
    parameter_metrics: pd.DataFrame,
    team_metrics: pd.DataFrame,
    outlier_mode: str,
) -> dict[str, str]:
    top_driver = parameter_metrics.iloc[0]
    lowest_parameter = parameter_metrics.sort_values("Average Score").iloc[0]
    weakest_driver = parameter_metrics.sort_values("Correlation").iloc[0]
    highest_gap = parameter_metrics.sort_values("Gap", ascending=False).iloc[0]
    primary_team = team_metrics.iloc[0]["Team / Vendor"] if not team_metrics.empty else "No team"

    what = (
        f"SPD averages {df['SPD'].mean():.2f} in the current selection, while the strongest behavioral driver is "
        f"{top_driver['Parameter']}."
    )
    why = (
        f"High performers outperform low performers most on {highest_gap['Parameter']} "
        f"({highest_gap['Gap %']:.1f}% gap), while {lowest_parameter['Parameter']} is the lowest absolute quality score."
    )
    next_step = (
        f"Prioritize {lowest_parameter['Parameter']} for training, review execution stability in {primary_team}, "
        f"and coach managers on {', '.join(KEY_DRIVER_ORDER[:2])}."
    )
    caveat = (
        "Outlier-adjusted view is active, so the dashboard is prioritizing the stable underlying pattern."
        if outlier_mode == "Outlier-adjusted view"
        else "Raw view is active, so one extreme SPD outlier may distort the driver ranking."
    )
    return {
        "what": what,
        "why": why,
        "next": next_step,
        "caveat": caveat,
        "top_driver": top_driver["Parameter"],
        "weakest_driver": weakest_driver["Parameter"],
        "lowest_parameter": lowest_parameter["Parameter"],
    }


def render_insight_panel(snapshot: dict[str, str], parameter_metrics: pd.DataFrame) -> None:
    top_two = parameter_metrics.head(2)["Parameter"].tolist()
    weak = snapshot["lowest_parameter"]
    st.markdown(
        f"""
        <div class="insight-card">
            <div class="section-title">What / Why / What Next</div>
            <div class="tiny-label">What is happening</div>
            <div class="insight-line">{snapshot["what"]}</div>
            <div class="tiny-label">Why it is happening</div>
            <div class="insight-line">{snapshot["why"]}</div>
            <div class="tiny-label">What should be done</div>
            <div class="insight-line">{snapshot["next"]}</div>
            <div class="tiny-label">Analytical note</div>
            <div class="insight-line">{snapshot["caveat"]}</div>
            <div style="margin-top:0.6rem;">
                {''.join(f'<span class="pill pill-green">{item}</span>' for item in top_two)}
                <span class="pill pill-red">{weak}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def executive_brief_page(
    df: pd.DataFrame,
    parameter_metrics: pd.DataFrame,
    team_metrics: pd.DataFrame,
    outlier_mode: str,
) -> None:
    snapshot = decision_snapshot(df, parameter_metrics, team_metrics, outlier_mode)
    hero(
        "Executive Brief",
        f"{selection_label(df)} | {outlier_mode} | Decision focus: what is happening, why, and what leadership should do next",
    )

    strongest = parameter_metrics.iloc[0]
    weakest = parameter_metrics.sort_values("Average Score").iloc[0]
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Avg SPD", f"{df['SPD'].mean():.2f}", "Current sales productivity")
    with c2:
        metric_card("Avg Quality Score", f"{df['Overall Quality Score'].mean():.2f}", "Quality is not the full story")
    with c3:
        metric_card(
            "Strongest Driver",
            strongest["Parameter"],
            f"Driver score {strongest['Driver Score']:.0f} | variance explained {strongest['SPD Variance Explained %']:.1f}%",
        )
    with c4:
        metric_card(
            "Weakest Driver",
            weakest["Parameter"],
            f"Lowest average score {weakest['Average Score']:.2f}",
        )

    left, right = st.columns([1.75, 1.0], gap="large")
    with left:
        section_open()
        scatter_df = df.dropna(subset=["SPD", "Overall Quality Score"]).copy()
        scatter_df["Cluster"] = np.where(scatter_df["SPD Band"] == "High", "High SPD", "Non-High SPD")
        fig = px.scatter(
            scatter_df,
            x="Overall Quality Score",
            y="SPD",
            color="SPD Band",
            symbol="Cluster",
            hover_data=["Agent Name", "Team / Vendor", "Listening", "Transaction", "Empathise"],
            color_discrete_map={"Low": RED, "Medium": BLUE, "High": GREEN},
            title="SPD vs Quality Score with High-SPD clustering",
        )
        add_trendline(fig, scatter_df, "Overall Quality Score", "SPD")
        fig.update_layout(
            paper_bgcolor=SURFACE,
            plot_bgcolor=SURFACE,
            margin=dict(l=10, r=10, t=52, b=10),
            legend_title_text="SPD Band",
        )
        st.plotly_chart(fig, use_container_width=True)
        section_close()
    with right:
        render_insight_panel(snapshot, parameter_metrics)

    section_open()
    ranking = parameter_metrics.copy().sort_values("Driver Score", ascending=True)
    ranking["Color"] = np.where(
        ranking["Action Priority"] == "Fix Now",
        RED,
        np.where(ranking["Action Priority"] == "Coach Next", AMBER, GREEN),
    )
    fig = go.Figure(
        data=[
            go.Bar(
                x=ranking["Driver Score"],
                y=ranking["Parameter"],
                orientation="h",
                marker_color=ranking["Color"],
                customdata=np.stack(
                    [
                        ranking["Correlation"].round(3),
                        ranking["Gap %"].round(1),
                        ranking["Average Score"].round(2),
                        ranking["Action Priority"],
                    ],
                    axis=-1,
                ),
                hovertemplate=(
                    "Parameter: %{y}<br>Driver score: %{x:.1f}"
                    "<br>Correlation: %{customdata[0]}"
                    "<br>High vs Low gap: %{customdata[1]}%"
                    "<br>Average score: %{customdata[2]}"
                    "<br>Priority: %{customdata[3]}<extra></extra>"
                ),
            )
        ]
    )
    fig.update_layout(
        title="Driver ranking: impact plus improvement opportunity",
        paper_bgcolor=SURFACE,
        plot_bgcolor=SURFACE,
        xaxis_title="Composite driver score",
        yaxis_title="",
        margin=dict(l=10, r=10, t=50, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)
    section_close()

    section_open()
    a, b, c = st.columns(3)
    with a:
        st.markdown("**So what?**")
        st.write(
            "SPD is not primarily a tone problem. It is moving with discovery, transaction progression, and empathy-linked conversion behavior."
        )
    with b:
        st.markdown("**What changed from the prototype?**")
        st.write(
            "The ranking now blends correlation, High-vs-Low gaps, and weak absolute scores, so leaders see where intervention will matter most."
        )
    with c:
        st.markdown("**What next?**")
        st.write(
            f"Give Training ownership of `{snapshot['lowest_parameter']}`, Ops ownership of the highest-risk team, and Managers ownership of `{snapshot['top_driver']}` coaching."
        )
    section_close()


def root_cause_page(df: pd.DataFrame, parameter_metrics: pd.DataFrame, team_metrics: pd.DataFrame) -> None:
    hero(
        "Root Cause",
        f"{selection_label(df)} | Locate where SPD is breaking: team, agent, parameter, or execution consistency",
    )

    section_open()
    gap_df = parameter_metrics.copy().sort_values("Gap", ascending=True)
    fig = go.Figure()
    fig.add_bar(
        x=gap_df["Low SPD Avg"],
        y=gap_df["Parameter"],
        orientation="h",
        name="Low SPD",
        marker_color=RED,
    )
    fig.add_bar(
        x=gap_df["High SPD Avg"],
        y=gap_df["Parameter"],
        orientation="h",
        name="High SPD",
        marker_color=GREEN,
    )
    fig.update_layout(
        title="Gap analysis: how high performers differ from low performers",
        barmode="group",
        paper_bgcolor=SURFACE,
        plot_bgcolor=SURFACE,
        xaxis_title="Average score",
        yaxis_title="",
        margin=dict(l=10, r=10, t=50, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)
    section_close()

    c1, c2 = st.columns([1.15, 1.0], gap="large")
    with c1:
        section_open()
        heat = (
            df.groupby("Team / Vendor")[list(PARAMETERS.values())]
            .mean()
            .rename(columns={v: k for k, v in PARAMETERS.items()})
        )
        heat = heat.reindex(team_metrics["Team / Vendor"].tolist()) if not team_metrics.empty else heat
        heat_fig = go.Figure(
            data=go.Heatmap(
                z=heat.values,
                x=heat.columns.tolist(),
                y=heat.index.tolist(),
                colorscale=[[0, "#FEE2E2"], [0.5, "#F8FAFC"], [1, "#DCFCE7"]],
                hovertemplate="Team: %{y}<br>Parameter: %{x}<br>Avg Score: %{z:.2f}<extra></extra>",
            )
        )
        heat_fig.update_layout(
            title="Team-by-parameter heatmap",
            paper_bgcolor=SURFACE,
            plot_bgcolor=SURFACE,
            margin=dict(l=10, r=10, t=50, b=10),
        )
        st.plotly_chart(heat_fig, use_container_width=True)
        section_close()

    with c2:
        section_open()
        split_by = st.selectbox(
            "Decomposition-style view",
            ["Team / Vendor", "Agent Name", "Overall Quality Score", *PARAMETERS.values()],
            key="decomp",
        )
        grp = df.groupby(split_by, dropna=False)["SPD"].mean().reset_index().dropna()
        grp = grp.sort_values("SPD", ascending=False).head(15)
        decomp = px.bar(
            grp,
            x="SPD",
            y=split_by,
            orientation="h",
            color="SPD",
            color_continuous_scale=[[0, RED], [0.5, BLUE], [1, GREEN]],
            title=f"SPD broken down by {split_by}",
        )
        decomp.update_layout(
            paper_bgcolor=SURFACE,
            plot_bgcolor=SURFACE,
            coloraxis_showscale=False,
            margin=dict(l=10, r=10, t=50, b=10),
        )
        decomp.update_yaxes(categoryorder="total ascending")
        st.plotly_chart(decomp, use_container_width=True)
        section_close()

    section_open()
    failure = team_metrics.copy()
    if not failure.empty:
        failure["Red Flag"] = np.select(
            [
                failure["Priority Score"] >= 70,
                failure["Priority Score"] >= 50,
            ],
            ["Red", "Amber"],
            default="Green",
        )
        st.dataframe(
            failure[
                [
                    "Team / Vendor",
                    "Avg SPD",
                    "Avg Quality",
                    "Weakest Parameter",
                    "Consistency Score",
                    "Risk Flag",
                    "Priority Score",
                    "Red Flag",
                ]
            ].style.format(
                {
                    "Avg SPD": "{:.2f}",
                    "Avg Quality": "{:.2f}",
                    "Consistency Score": "{:.2f}",
                    "Priority Score": "{:.1f}",
                }
            ),
            use_container_width=True,
            height=290,
        )
    else:
        st.info("Not enough team data for failure panel.")
    section_close()

    section_open()
    lead_team = team_metrics.iloc[0] if not team_metrics.empty else None
    if lead_team is not None:
        st.markdown("**So what?**")
        st.write(
            f"`{lead_team['Team / Vendor']}` is the primary root-cause pocket in the current selection, driven by `{lead_team['Weakest Parameter']}` and a consistency score of {lead_team['Consistency Score']:.2f}."
        )
        st.markdown("**What next?**")
        st.write(
            "Ops should check process adherence and tooling friction first, then Managers should coach the top driver gaps for that team."
        )
    section_close()


def action_center_page(
    df: pd.DataFrame,
    parameter_metrics: pd.DataFrame,
    team_metrics: pd.DataFrame,
    agent_risks: pd.DataFrame,
) -> None:
    hero(
        "Action Center",
        f"{selection_label(df)} | Function-specific action plans for Training, Operations, and Managers",
    )

    lowest_score = parameter_metrics.sort_values("Average Score").iloc[0]
    top_driver = parameter_metrics.iloc[0]
    team_issue = team_metrics.iloc[0] if not team_metrics.empty else None

    training_col, ops_col, mgr_col = st.columns(3, gap="large")

    with training_col:
        st.markdown(
            f"""
            <div class="action-card" style="border-left-color:{RED}">
                <div class="action-title">Training View</div>
                <div class="tiny-label">Priority skill gap</div>
                <div class="insight-line">{lowest_score["Parameter"]}</div>
                <div class="tiny-label">Highest impact behavior</div>
                <div class="insight-line">{top_driver["Parameter"]}</div>
                <div class="action-body">
                    Training should prioritize <b>{lowest_score["Parameter"]}</b> because it is the weakest quality behavior,
                    while reinforcing <b>{top_driver["Parameter"]}</b> because it explains approximately
                    <b>{top_driver["SPD Variance Explained %"]:.1f}%</b> of SPD variance in the current view.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with ops_col:
        ops_text = "Not enough team data."
        if team_issue is not None:
            ops_text = (
                f"Team <b>{team_issue['Team / Vendor']}</b> shows the biggest delivery breakdown, especially in "
                f"<b>{team_issue['Weakest Parameter']}</b>. The combination of low SPD and a consistency score of "
                f"<b>{team_issue['Consistency Score']:.2f}</b> points to a process or calibration issue, not just capability."
            )
        st.markdown(
            f"""
            <div class="action-card" style="border-left-color:{AMBER}">
                <div class="action-title">Operations View</div>
                <div class="tiny-label">Team inconsistency focus</div>
                <div class="action-body">{ops_text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with mgr_col:
        manager_focus = agent_risks[agent_risks["Priority Bucket"].isin(["Fix Now", "Coach Now"])].head(5)
        coach_line = ", ".join(KEY_DRIVER_ORDER[:2])
        extra = (
            f"{len(manager_focus)} agents need immediate intervention."
            if not manager_focus.empty
            else "No immediate coaching cluster under current filters."
        )
        st.markdown(
            f"""
            <div class="action-card" style="border-left-color:{GREEN}">
                <div class="action-title">Manager Coaching View</div>
                <div class="tiny-label">Coaching priority</div>
                <div class="action-body">
                    Managers should coach low-SPD agents on <b>{coach_line}</b> and <b>{KEY_DRIVER_ORDER[2]}</b> to improve discovery,
                    empathy handling, and progression to sale. {extra}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    c1, c2 = st.columns([1.2, 1.15], gap="large")
    with c1:
        section_open()
        radar_rows = []
        for label, column in PARAMETERS.items():
            for band in ["High", "Low"]:
                subset = df[df["SPD Band"] == band]
                radar_rows.append({"Parameter": label, "SPD Band": band, "Score": subset[column].mean()})
        radar_df = pd.DataFrame(radar_rows)
        radar = px.line_polar(
            radar_df,
            r="Score",
            theta="Parameter",
            color="SPD Band",
            line_close=True,
            color_discrete_map={"High": GREEN, "Low": RED},
            title="High vs Low SPD behavioral profile",
        )
        radar.update_traces(fill="toself")
        radar.update_layout(
            paper_bgcolor=SURFACE,
            polar=dict(bgcolor=SURFACE),
            margin=dict(l=10, r=10, t=50, b=10),
        )
        st.plotly_chart(radar, use_container_width=True)
        section_close()

    with c2:
        section_open()
        driver_opportunity = parameter_metrics.copy().sort_values("Driver Score", ascending=False)
        opp = px.scatter(
            driver_opportunity,
            x="Average Score",
            y="Driver Score",
            size="Gap",
            color="Action Priority",
            text="Parameter",
            color_discrete_map={"Fix Now": RED, "Coach Next": AMBER, "Sustain": GREEN},
            title="Intervention matrix: impact vs current score",
        )
        opp.update_traces(textposition="top center")
        opp.update_layout(
            paper_bgcolor=SURFACE,
            plot_bgcolor=SURFACE,
            xaxis_title="Current average score",
            yaxis_title="Driver score",
            margin=dict(l=10, r=10, t=50, b=10),
        )
        st.plotly_chart(opp, use_container_width=True)
        section_close()

    section_open()
    priority_agents = agent_risks.copy()
    if not priority_agents.empty:
        st.dataframe(
            priority_agents[
                [
                    "Agent Name",
                    "Team / Vendor",
                    "SPD",
                    "SPD Band",
                    "Priority Bucket",
                    "Owner",
                    "Coach On",
                    "Gap Score",
                ]
            ].style.format({"SPD": "{:.2f}", "Gap Score": "{:.2f}"}),
            use_container_width=True,
            height=300,
        )
    else:
        st.info("No agent risk signals available under the current filters.")
    section_close()

    section_open()
    st.markdown("**What should each function do next?**")
    st.write(
        f"Training should redesign refreshers around `{lowest_score['Parameter']}` and `{top_driver['Parameter']}`. "
        f"Operations should review process stability in `{team_issue['Team / Vendor']}` if team signals are present. "
        f"Managers should work the `Fix Now` and `Coach Now` population first, not spread coaching evenly."
        if team_issue is not None
        else "Training should lead on the lowest-score and highest-impact parameters, while Managers focus first on the highest-risk agents."
    )
    section_close()


def diagnostics_page(df: pd.DataFrame, parameter_metrics: pd.DataFrame) -> None:
    hero(
        "Diagnostics",
        f"{selection_label(df)} | Detailed evidence for validation and coaching drill-down",
    )

    c1, c2 = st.columns([1.0, 1.65], gap="large")
    with c1:
        section_open()
        driver_table = parameter_metrics[
            ["Parameter", "Average Score", "Correlation", "Gap %", "Driver Score", "Action Priority"]
        ].copy()
        st.dataframe(
            driver_table.style.format(
                {
                    "Average Score": "{:.2f}",
                    "Correlation": "{:.3f}",
                    "Gap %": "{:.1f}",
                    "Driver Score": "{:.1f}",
                }
            ),
            use_container_width=True,
            height=320,
        )
        section_close()

    with c2:
        section_open()
        fig = make_subplots(
            rows=2,
            cols=3,
            subplot_titles=list(PARAMETERS.keys()) + [""],
            horizontal_spacing=0.08,
            vertical_spacing=0.16,
        )
        positions = [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2)]
        for (label, column), (row, col) in zip(PARAMETERS.items(), positions):
            pair = df.dropna(subset=[column, "SPD"])
            fig.add_trace(
                go.Scatter(
                    x=pair[column],
                    y=pair["SPD"],
                    mode="markers",
                    marker=dict(color=BLUE, size=8, opacity=0.72),
                    customdata=np.stack([pair["Agent Name"], pair["Team / Vendor"]], axis=-1),
                    hovertemplate=(
                        f"{label}<br>Score: %{{x:.2f}}<br>SPD: %{{y:.2f}}"
                        "<br>Agent: %{customdata[0]}<br>Team: %{customdata[1]}<extra></extra>"
                    ),
                    showlegend=False,
                ),
                row=row,
                col=col,
            )
            add_trendline(fig, pair, column, "SPD", row=row, col=col)
            fig.update_xaxes(title_text="Parameter score", row=row, col=col)
            fig.update_yaxes(title_text="SPD", row=row, col=col)
        fig.update_layout(
            title="Parameter-by-parameter SPD relationship",
            paper_bgcolor=SURFACE,
            plot_bgcolor=SURFACE,
            height=650,
            margin=dict(l=10, r=10, t=55, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)
        section_close()


def main() -> None:
    inject_css()
    df = load_data()
    filtered, outlier_mode = filter_data(df)

    st.write("Checkpoint 2")

    if filtered.empty:
        st.warning("No data available for the current filters. Adjust the slicers to continue.")
        return

    parameter_metrics = get_parameter_metrics(filtered)
    team_metrics = get_team_metrics(filtered, parameter_metrics)
    agent_risks = get_agent_risks(filtered, parameter_metrics)

    page = st.sidebar.radio(
        "Navigation",
        ["Executive Brief", "Root Cause", "Action Center", "Diagnostics"],
    )

    if page == "Executive Brief":
        executive_brief_page(filtered, parameter_metrics, team_metrics, outlier_mode)
    elif page == "Root Cause":
        root_cause_page(filtered, parameter_metrics, team_metrics)
    elif page == "Action Center":
        action_center_page(filtered, parameter_metrics, team_metrics, agent_risks)
    else:
        diagnostics_page(filtered, parameter_metrics)


if __name__ == "__main__":
    main()
