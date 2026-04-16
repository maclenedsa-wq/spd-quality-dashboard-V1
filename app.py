from __future__ import annotations

import streamlit as st
import numpy as np
import pandas as pd
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from historical_data import HISTORICAL_DATA_FILE, standardize_snapshot_frame

st.set_page_config(
    page_title="OMNI SPD Insights Hub",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state="expanded",
)

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

QUALITY_PARAMETERS = {
    "Listening & Understanding Needs": "Listening",
    "Product Knowledge and Explanation": "Product Knowledge",
    "Transaction": "Transaction",
    "Acknowledge & Empathise": "Empathise",
    "Language, Tone and Professionalism": "Language Tone Professionalism",
}

DETAILED_PARAMETERS = {
    "Positive": "Positive",
    "Negative": "Negative",
    "Neutral": "Neutral",
    "Escalated": ".escalated",
    "Not Interested in Buying": ".not_interested_in_buying",
    "Payment Done": ".payment_done",
    "Will Buy Self": ".will_buy_self",
    "Positive Intent Needs Follow Up": ".positive_intent_needs_follow_up",
    "Non Material Interaction": ".non_material_interaction",
    "Follow Up Required": ".follow_up_required",
    "Unresolved": ".unresolved",
    "Partially Resolved": ".partially_resolved",
    "Resolved": ".resolved",
    "Threatened to Escalate": ".threatened_to_escalate",
}

PARAMETER_GROUPS = {
    "Quality Score": QUALITY_PARAMETERS,
    "Detailed Parameters": DETAILED_PARAMETERS,
    "All Parameters": {**QUALITY_PARAMETERS, **DETAILED_PARAMETERS},
}

DEFAULT_DRIVER_FOCUS = [
    "Listening & Understanding Needs",
    "Transaction",
    "Acknowledge & Empathise",
]
THEME_BY_PARAMETER = {
    "Listening & Understanding Needs": "Need Discovery",
    "Product Knowledge and Explanation": "Product Confidence",
    "Transaction": "Conversion Flow",
    "Acknowledge & Empathise": "Emotional Handling",
    "Language, Tone and Professionalism": "Communication Hygiene",
    "Positive": "Intent Signals",
    "Negative": "Disposition Outcome",
    "Neutral": "Disposition Outcome",
    "Escalated": "Escalation Risk",
    "Not Interested in Buying": "Non-Buying Outcome",
    "Payment Done": "Closure Signals",
    "Will Buy Self": "Deferred Purchase Signals",
    "Positive Intent Needs Follow Up": "Follow Up Pipeline",
    "Non Material Interaction": "Low-Value Contact",
    "Follow Up Required": "Follow Up Pipeline",
    "Unresolved": "Resolution Risk",
    "Partially Resolved": "Resolution Progress",
    "Resolved": "Resolution Progress",
    "Threatened to Escalate": "Escalation Risk",
}
DISPLAY_LABELS = {
    "Listening & Understanding Needs": "Listening",
    "Product Knowledge and Explanation": "Product Knowledge",
    "Acknowledge & Empathise": "Empathise",
    "Language, Tone and Professionalism": "Language & Tone",
    "Positive Intent Needs Follow Up": "Positive Intent Follow Up",
    "Not Interested in Buying": "Not Interested",
    "Non Material Interaction": "Non-Material Interaction",
    "Threatened to Escalate": "Escalation Threat",
}
ROLE_VIEWS = ["Leadership", "Managers", "Training", "Operations"]
COMPARE_MODES = ["None", "Team / Vendor", "Campaign", "SPD Band"]
SIMULATION_STEPS = [-2.0, -1.0, 0.0, 1.0, 2.0]


def inject_css() -> None:
    st.markdown(
        f"""
        <style>
        [data-testid="stSidebar"] > div:first-child {{
            background: linear-gradient(180deg, #F8FBFF 0%, #EEF4FB 100%);
        }}
        .stApp {{
            background: radial-gradient(circle at top left, #FFFFFF 0%, {BG} 55%);
            color: {TEXT};
        }}
        .block-container {{
            padding-top: 0.5rem;
            padding-bottom: 2rem;
            max-width: 1460px;
        }}
        h1 {{
            display: none;
        }}
        [data-testid="stSidebar"] {{
            min-width: 300px;
            max-width: 300px;
        }}
        .hero-card {{
            background: linear-gradient(135deg, {NAVY} 0%, #1E3A8A 100%);
            color: #FFFFFF;
            border-radius: 22px;
            padding: 0.9rem 1.15rem;
            margin-bottom: 0.8rem;
            box-shadow: 0 12px 30px rgba(15, 23, 42, 0.12);
        }}
        .hero-title {{
            font-size: 1.05rem;
            font-weight: 700;
            margin-bottom: 0.12rem;
        }}
        .hero-sub {{
            font-size: 0.82rem;
            color: rgba(255,255,255,0.78);
        }}
        .page-header {{
            display: flex;
            align-items: end;
            justify-content: space-between;
            gap: 1rem;
            margin-bottom: 0.45rem;
        }}
        .page-title {{
            color: {TEXT};
            font-size: 2rem;
            font-weight: 800;
            letter-spacing: -0.03em;
            line-height: 1;
        }}
        .page-sub {{
            color: {MUTED};
            font-size: 0.84rem;
            margin-top: 0.18rem;
        }}
        .metric-card {{
            background: {SURFACE};
            border: 1px solid #E5E7EB;
            border-radius: 18px;
            padding: 0.9rem 0.95rem;
            min-height: 118px;
            box-shadow: 0 6px 20px rgba(15, 23, 42, 0.05);
        }}
        .metric-label {{
            color: {MUTED};
            font-size: 0.76rem;
            letter-spacing: 0.02em;
            margin-bottom: 0.3rem;
        }}
        .metric-value {{
            color: {TEXT};
            font-size: 1.15rem;
            font-weight: 700;
            line-height: 1.12;
            min-height: 2.55em;
        }}
        .metric-sub {{
            color: {MUTED};
            font-size: 0.78rem;
            margin-top: 0.35rem;
            line-height: 1.35;
        }}
        .section-card {{
            background: {SURFACE};
            border: 1px solid #E5E7EB;
            border-radius: 20px;
            padding: 0.85rem 0.9rem 0.45rem 0.9rem;
            box-shadow: 0 8px 22px rgba(15, 23, 42, 0.04);
            margin-bottom: 0.8rem;
        }}
        .insight-card {{
            background: linear-gradient(135deg, #FFFFFF 0%, #F0F7FF 100%);
            border: 1px solid #D8E5F7;
            border-radius: 20px;
            padding: 0.95rem 1rem;
            min-height: 100%;
        }}
        .section-title {{
            color: {TEXT};
            font-size: 0.98rem;
            font-weight: 700;
            margin-bottom: 0.45rem;
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
            font-size: 0.9rem;
            line-height: 1.48;
            margin-bottom: 0.55rem;
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
        .filter-strip {{
            background: linear-gradient(135deg, #FFFFFF 0%, #F7FAFF 100%);
            border: 1px solid #DCE7F5;
            border-radius: 18px;
            padding: 0.72rem 0.9rem 0.42rem 0.9rem;
            margin-bottom: 0.8rem;
            box-shadow: 0 6px 18px rgba(37, 99, 235, 0.06);
        }}
        .filter-chip {{
            display: inline-block;
            background: #E8F1FF;
            color: #1D4ED8;
            border: 1px solid #BFDBFE;
            border-radius: 999px;
            padding: 0.26rem 0.65rem;
            margin-right: 0.35rem;
            margin-bottom: 0.35rem;
            font-size: 0.76rem;
            font-weight: 700;
        }}
        .insight-bullet {{
            padding-left: 0.9rem;
            position: relative;
            margin-bottom: 0.65rem;
        }}
        .insight-bullet::before {{
            content: "";
            position: absolute;
            left: 0;
            top: 0.45rem;
            width: 0.38rem;
            height: 0.38rem;
            background: {BLUE};
            border-radius: 999px;
        }}
        .kpi-row {{
            margin-bottom: 0.75rem;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data(show_spinner=False)
def load_data() -> pd.DataFrame:
    if HISTORICAL_DATA_FILE.exists():
        df = pd.read_csv(HISTORICAL_DATA_FILE, parse_dates=["Snapshot Date", "Ingested At"])
        df["Data Mode"] = "Historical"
    else:
        raw_df = pd.read_excel(DATA_FILE, sheet_name=SHEET_NAME)
        df = standardize_snapshot_frame(
            raw_df,
            snapshot_date=pd.Timestamp.today().normalize(),
            source_name=DATA_FILE.name,
        )
        df["Data Mode"] = "Current Snapshot"

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
    df["Snapshot Date"] = pd.to_datetime(df["Snapshot Date"], errors="coerce")
    df["Snapshot Label"] = df["Snapshot Date"].dt.strftime("%Y-%m-%d").fillna("Current Snapshot")

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
        <div class="page-header">
            <div>
                <div class="page-title">{title}</div>
            </div>
        </div>
        <div class="hero-card">
            <div class="hero-title">OMNI SPD Insights Hub</div>
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


def display_label(label: str) -> str:
    return DISPLAY_LABELS.get(label, label)


def section_open() -> None:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)


def section_close() -> None:
    st.markdown("</div>", unsafe_allow_html=True)


def get_parameter_catalog(view_name: str) -> dict[str, str]:
    return PARAMETER_GROUPS[view_name]


def get_available_themes(parameter_catalog: dict[str, str]) -> list[str]:
    return sorted({THEME_BY_PARAMETER.get(label, "Other Behaviors") for label in parameter_catalog})


def build_catalog_from_metrics(parameter_metrics: pd.DataFrame) -> dict[str, str]:
    return {
        row["Parameter"]: row["Column"]
        for _, row in parameter_metrics[["Parameter", "Column"]].drop_duplicates().iterrows()
    }


def get_driver_focus(parameter_metrics: pd.DataFrame) -> list[str]:
    if parameter_metrics.empty:
        return []

    focus = parameter_metrics.sort_values("Driver Score", ascending=False).head(3)["Parameter"].tolist()
    if len(focus) >= 3:
        return focus
    fallbacks = [label for label in DEFAULT_DRIVER_FOCUS if label in parameter_metrics["Parameter"].tolist()]
    for label in fallbacks:
        if label not in focus:
            focus.append(label)
        if len(focus) == 3:
            break
    return focus


def summarize_driver_themes(parameter_metrics: pd.DataFrame) -> str:
    if parameter_metrics.empty:
        return "No parameter theme is available for the current filters."

    top = parameter_metrics.sort_values("Driver Score", ascending=False).head(3)["Parameter"].tolist()
    theme_counts: dict[str, int] = {}
    for label in top:
        theme = THEME_BY_PARAMETER.get(label, "Other Behaviors")
        theme_counts[theme] = theme_counts.get(theme, 0) + 1

    dominant_themes = sorted(theme_counts.items(), key=lambda item: (-item[1], item[0]))
    theme_labels = [theme for theme, _ in dominant_themes[:2]]
    weakest = parameter_metrics.sort_values("Average Score").iloc[0]["Parameter"]
    weakest_theme = THEME_BY_PARAMETER.get(weakest, "execution quality")

    if len(theme_labels) == 1:
        return (
            f"The current SPD story is being led by {theme_labels[0].lower()}, while the lowest-scoring behavior "
            f"sits in {weakest_theme.lower()}."
        )

    return (
        f"The current SPD story is clustering around {theme_labels[0].lower()} and {theme_labels[1].lower()}, "
        f"while the lowest-scoring behavior sits in {weakest_theme.lower()}."
    )


def filter_data(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, object]]:
    st.sidebar.title("OMNI Decision System")
    st.sidebar.caption(df["Data Mode"].iloc[0] if "Data Mode" in df.columns and not df.empty else "Executive version")
    st.sidebar.markdown("## Filters")

    teams = sorted(df["Team / Vendor"].dropna().unique().tolist())
    campaigns = sorted(df["Campaign"].dropna().unique().tolist())
    snapshot_labels = sorted(df["Snapshot Label"].dropna().unique().tolist(), reverse=True)

    with st.sidebar.expander("Snapshot", expanded=True):
        is_historical_mode = bool("Data Mode" in df.columns and not df.empty and df["Data Mode"].iloc[0] == "Historical")
        default_snapshot = snapshot_labels if is_historical_mode else snapshot_labels[:1] if snapshot_labels else []
        selected_snapshots = st.multiselect("Snapshot Date", snapshot_labels, default=default_snapshot)
    with st.sidebar.expander("Population", expanded=True):
        selected_campaign = st.multiselect("Campaign", campaigns)
        filtered_agents_df = df.copy()
        if selected_snapshots:
            filtered_agents_df = filtered_agents_df[filtered_agents_df["Snapshot Label"].isin(selected_snapshots)]
        if selected_campaign:
            filtered_agents_df = filtered_agents_df[filtered_agents_df["Campaign"].isin(selected_campaign)]

        available_teams = sorted(filtered_agents_df["Team / Vendor"].dropna().unique().tolist())
        selected_team = st.multiselect("Team / Vendor", available_teams)
        if selected_team:
            filtered_agents_df = filtered_agents_df[filtered_agents_df["Team / Vendor"].isin(selected_team)]

        available_agents = sorted(filtered_agents_df["Agent Name"].dropna().unique().tolist())
        selected_agents = st.multiselect("Agent Name", available_agents)

    spd_min = float(df["SPD"].min()) if df["SPD"].notna().any() else 0.0
    spd_max = float(df["SPD"].max()) if df["SPD"].notna().any() else 0.0
    quality_min = float(df["Overall Quality Score"].min()) if df["Overall Quality Score"].notna().any() else 0.0
    quality_max = float(df["Overall Quality Score"].max()) if df["Overall Quality Score"].notna().any() else 100.0

    with st.sidebar.expander("Performance", expanded=True):
        selected_band = st.multiselect(
            "SPD Band",
            ["Low", "Medium", "High"],
            default=["Low", "Medium", "High"],
        )
        spd_range = st.slider(
            "SPD range",
            min_value=float(np.floor(spd_min)),
            max_value=float(np.ceil(spd_max)),
            value=(float(np.floor(spd_min)), float(np.ceil(spd_max))),
        )
        quality_range = st.slider(
            "Quality score range",
            min_value=float(np.floor(quality_min)),
            max_value=float(np.ceil(quality_max)),
            value=(float(np.floor(quality_min)), float(np.ceil(quality_max))),
        )
        outlier_mode = st.radio(
            "Analytical view",
            ["Outlier-adjusted view", "Raw view"],
            help="Outlier-adjusted excludes SPD values above 3 to keep the driver model more stable.",
        )

    parameter_view = st.sidebar.radio(
        "Parameter scope",
        ["Quality Score", "Detailed Parameters", "All Parameters"],
        help="Switch between the original quality pillars, the additional detailed parameters, or a combined SPD driver view.",
    )
    available_themes = get_available_themes(get_parameter_catalog(parameter_view))
    with st.sidebar.expander("Analysis Lens", expanded=True):
        selected_themes = st.multiselect("Parameter themes", available_themes, default=available_themes)
        selected_priorities = st.multiselect(
            "Action priority",
            ["Fix Now", "Coach Next", "Sustain"],
            default=["Fix Now", "Coach Next", "Sustain"],
        )
        ranking_basis = st.selectbox(
            "Rank drivers by",
            ["Driver Score", "Correlation", "Gap", "Average Score"],
            help="Controls the primary sorting used in executive and diagnostic views.",
        )
        top_n = st.slider("Parameters to highlight", min_value=5, max_value=12, value=8)
        role_view = st.selectbox("Role lens", ROLE_VIEWS, help="Tailors the executive action guidance for a specific audience.")
        compare_mode = st.selectbox("Compare mode", COMPARE_MODES, help="Compare two groups side by side in the executive view.")
        compare_left = ""
        compare_right = ""
        if compare_mode != "None":
            compare_options = get_compare_options(df, compare_mode)
            if len(compare_options) >= 2:
                compare_left = st.selectbox("Compare A", compare_options, key="compare_left")
                compare_right = st.selectbox(
                    "Compare B",
                    [item for item in compare_options if item != compare_left] or compare_options,
                    key="compare_right",
                )
            else:
                st.caption("Not enough groups available for comparison under current data.")

    with st.sidebar.expander("Phase 2 Lab", expanded=False):
        st.caption("Trend-ready intelligence with current snapshot data. True historical trends need a date field or snapshots over time.")
        sim_controls = {}
        sim_parameters = get_parameter_catalog(parameter_view)
        sim_metric_names = list(sim_parameters.keys())[:3]
        for name in sim_metric_names:
            sim_controls[f"sim_{sim_parameters[name]}"] = st.select_slider(
                f"{display_label(name)} uplift",
                options=SIMULATION_STEPS,
                value=0.0,
            )

    filtered = df.copy()
    if selected_snapshots:
        filtered = filtered[filtered["Snapshot Label"].isin(selected_snapshots)]
    if selected_campaign:
        filtered = filtered[filtered["Campaign"].isin(selected_campaign)]
    if selected_team:
        filtered = filtered[filtered["Team / Vendor"].isin(selected_team)]
    if selected_agents:
        filtered = filtered[filtered["Agent Name"].isin(selected_agents)]
    if selected_band:
        filtered = filtered[filtered["SPD Band"].isin(selected_band)]
    filtered = filtered[filtered["SPD"].between(spd_range[0], spd_range[1], inclusive="both")]
    filtered = filtered[
        filtered["Overall Quality Score"].between(quality_range[0], quality_range[1], inclusive="both")
    ]
    if outlier_mode == "Outlier-adjusted view":
        filtered = filtered[~filtered["Is Outlier SPD"]]

    st.sidebar.markdown("---")
    st.sidebar.caption(
        f"{filtered['Agent Name'].nunique()} agents | {filtered['Team / Vendor'].nunique()} teams | {filtered['SPD'].notna().sum()} SPD rows"
    )
    settings = {
        "outlier_mode": outlier_mode,
        "parameter_view": parameter_view,
        "selected_campaign": selected_campaign,
        "selected_snapshots": selected_snapshots,
        "selected_team": selected_team,
        "selected_agents": selected_agents,
        "selected_band": selected_band,
        "spd_range": spd_range,
        "quality_range": quality_range,
        "selected_themes": selected_themes,
        "selected_priorities": selected_priorities,
        "ranking_basis": ranking_basis,
        "top_n": top_n,
        "role_view": role_view,
        "compare_mode": compare_mode,
        "compare_left": compare_left,
        "compare_right": compare_right,
        **sim_controls,
    }
    return filtered, settings


def apply_parameter_filters(parameter_metrics: pd.DataFrame, settings: dict[str, object]) -> pd.DataFrame:
    filtered_metrics = parameter_metrics.copy()
    selected_themes = settings["selected_themes"]
    selected_priorities = settings["selected_priorities"]
    if selected_themes:
        filtered_metrics = filtered_metrics[
            filtered_metrics["Parameter"].map(lambda value: THEME_BY_PARAMETER.get(value, "Other Behaviors")).isin(selected_themes)
        ]
    if selected_priorities:
        filtered_metrics = filtered_metrics[filtered_metrics["Action Priority"].isin(selected_priorities)]

    ranking_basis = settings["ranking_basis"]
    ascending = ranking_basis == "Average Score"
    return filtered_metrics.sort_values([ranking_basis, "Correlation"], ascending=[ascending, False]).reset_index(drop=True)


def render_filter_summary(df: pd.DataFrame, settings: dict[str, object], parameter_metrics: pd.DataFrame) -> None:
    chips = [
        f"{len(settings['selected_snapshots'])} snapshot(s)" if settings["selected_snapshots"] else "All snapshots",
        f"{settings['parameter_view']}",
        f"{settings['outlier_mode']}",
        f"{settings['role_view']} lens",
        f"SPD {settings['spd_range'][0]:.1f}-{settings['spd_range'][1]:.1f}",
        f"Quality {settings['quality_range'][0]:.0f}-{settings['quality_range'][1]:.0f}",
        f"{len(parameter_metrics)} drivers in scope",
    ]
    if settings["selected_campaign"]:
        chips.append(f"{len(settings['selected_campaign'])} campaigns")
    if settings["selected_team"]:
        chips.append(f"{len(settings['selected_team'])} teams")
    if settings["selected_agents"]:
        chips.append(f"{len(settings['selected_agents'])} agents")
    if settings["compare_mode"] != "None" and settings["compare_left"] and settings["compare_right"]:
        chips.append(f"{settings['compare_left']} vs {settings['compare_right']}")

    st.markdown(
        f"""
        <div class="filter-strip">
            <div class="tiny-label">Active analysis context</div>
            <div style="margin-top:0.2rem;">
                {''.join(f'<span class="filter-chip">{item}</span>' for item in chips)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_parameter_overview(parameter_metrics: pd.DataFrame, top_n: int) -> None:
    section_open()
    top_metrics = parameter_metrics.head(top_n).copy()
    top_metrics["Display Parameter"] = top_metrics["Parameter"].map(display_label)
    c1, c2 = st.columns([1.2, 1.0], gap="large")
    with c1:
        theme_df = (
            top_metrics.assign(Theme=top_metrics["Parameter"].map(lambda value: THEME_BY_PARAMETER.get(value, "Other Behaviors")))
            .groupby("Theme", as_index=False)
            .agg({"Driver Score": "mean", "Correlation": "mean"})
            .sort_values("Driver Score", ascending=True)
        )
        fig = px.bar(
            theme_df,
            x="Driver Score",
            y="Theme",
            orientation="h",
            color="Correlation",
            color_continuous_scale=[[0, RED], [0.5, BLUE], [1, GREEN]],
            title="Theme ranking across selected drivers",
        )
        fig.update_layout(
            paper_bgcolor=SURFACE,
            plot_bgcolor=SURFACE,
            coloraxis_showscale=False,
            margin=dict(l=10, r=10, t=50, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        insight_df = top_metrics[["Display Parameter", "Driver Score", "Correlation", "Gap %", "Action Priority"]].copy()
        insight_df = insight_df.rename(columns={"Display Parameter": "Parameter"})
        st.dataframe(
            insight_df.style.format(
                {"Driver Score": "{:.1f}", "Correlation": "{:.3f}", "Gap %": "{:.1f}"}
            ),
            use_container_width=True,
            height=320,
        )
    section_close()


def get_binary_rate(series: pd.Series) -> float:
    clean = pd.to_numeric(series, errors="coerce").dropna()
    if clean.empty:
        return np.nan
    scale = 100.0 if clean.max() <= 1.0 else 1.0
    return float(clean.mean() * scale)


def get_phase1_kpis(df: pd.DataFrame, team_metrics: pd.DataFrame, agent_risks: pd.DataFrame) -> dict[str, float | str]:
    positive_intent_rate = get_binary_rate(
        df[["Positive", ".positive_intent_needs_follow_up"]].max(axis=1)
        if {"Positive", ".positive_intent_needs_follow_up"}.issubset(df.columns)
        else pd.Series(dtype=float)
    )
    payment_completion_rate = get_binary_rate(df[".payment_done"]) if ".payment_done" in df.columns else np.nan
    follow_up_rate = get_binary_rate(df[".follow_up_required"]) if ".follow_up_required" in df.columns else np.nan
    unresolved_rate = get_binary_rate(
        df[[".unresolved", ".threatened_to_escalate", ".escalated"]].max(axis=1)
        if {".unresolved", ".threatened_to_escalate", ".escalated"}.issubset(df.columns)
        else pd.Series(dtype=float)
    )
    resolved_rate = get_binary_rate(df[".resolved"]) if ".resolved" in df.columns else np.nan
    resolution_effectiveness = resolved_rate - unresolved_rate if pd.notna(resolved_rate) and pd.notna(unresolved_rate) else np.nan
    team_consistency = 100 - normalize(team_metrics["Consistency Score"]).mean() * 100 if not team_metrics.empty else np.nan
    coaching_priority = (
        ((agent_risks["Priority Bucket"] == "Fix Now").mean() * 100)
        + ((agent_risks["Priority Bucket"] == "Coach Now").mean() * 60)
        if not agent_risks.empty
        else np.nan
    )

    return {
        "Positive Intent Rate": positive_intent_rate,
        "Payment Completion Rate": payment_completion_rate,
        "Follow-Up Rate": follow_up_rate,
        "Unresolved Risk Rate": unresolved_rate,
        "Resolution Effectiveness": resolution_effectiveness,
        "Team Consistency Index": team_consistency,
        "Coaching Priority Index": coaching_priority,
    }


def format_metric_value(value: float, suffix: str = "%", decimals: int = 1) -> str:
    if pd.isna(value):
        return "-"
    return f"{value:.{decimals}f}{suffix}"


def get_compare_options(df: pd.DataFrame, compare_mode: str) -> list[str]:
    if compare_mode == "Team / Vendor":
        return sorted(df["Team / Vendor"].dropna().unique().tolist())
    if compare_mode == "Campaign":
        return sorted(df["Campaign"].dropna().unique().tolist())
    if compare_mode == "SPD Band":
        return ["Low", "Medium", "High"]
    return []


def build_comparison_frame(df: pd.DataFrame, compare_mode: str, left_value: str, right_value: str) -> pd.DataFrame:
    if compare_mode == "None" or not left_value or not right_value:
        return pd.DataFrame()
    compare_df = df.copy()
    compare_df["Compare Group"] = np.where(compare_df[compare_mode] == left_value, left_value, compare_df[compare_mode])
    compare_df = compare_df[compare_df[compare_mode].isin([left_value, right_value])].copy()
    summary = []
    for label, group in compare_df.groupby(compare_mode):
        summary.append(
            {
                "Group": label,
                "Avg SPD": group["SPD"].mean(),
                "Avg Quality": group["Overall Quality Score"].mean(),
                "Positive Intent Rate": get_binary_rate(
                    group[["Positive", ".positive_intent_needs_follow_up"]].max(axis=1)
                ) if {"Positive", ".positive_intent_needs_follow_up"}.issubset(group.columns) else np.nan,
                "Payment Completion Rate": get_binary_rate(group[".payment_done"]) if ".payment_done" in group.columns else np.nan,
                "Unresolved Risk Rate": get_binary_rate(
                    group[[".unresolved", ".threatened_to_escalate", ".escalated"]].max(axis=1)
                ) if {".unresolved", ".threatened_to_escalate", ".escalated"}.issubset(group.columns) else np.nan,
            }
        )
    return pd.DataFrame(summary)


def get_exception_tables(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    if df.empty:
        return {}

    low_spd_cut = df["SPD"].quantile(0.3)
    high_spd_cut = df["SPD"].quantile(0.7)

    unresolved_signal = (
        df[[".unresolved", ".threatened_to_escalate", ".escalated"]].max(axis=1)
        if {".unresolved", ".threatened_to_escalate", ".escalated"}.issubset(df.columns)
        else pd.Series([np.nan] * len(df), index=df.index)
    )
    closure_signal = (
        df[[".payment_done", ".resolved"]].max(axis=1)
        if {".payment_done", ".resolved"}.issubset(df.columns)
        else pd.Series([np.nan] * len(df), index=df.index)
    )
    followup_signal = (
        df[[".follow_up_required", ".positive_intent_needs_follow_up"]].max(axis=1)
        if {".follow_up_required", ".positive_intent_needs_follow_up"}.issubset(df.columns)
        else pd.Series([np.nan] * len(df), index=df.index)
    )

    base_cols = ["Agent Name", "Team / Vendor", "SPD", "Overall Quality Score"]
    exceptions = {
        "Low SPD + High Unresolved": df.loc[(df["SPD"] <= low_spd_cut) & (unresolved_signal >= 1), base_cols].copy(),
        "High Potential + Low Closure": df.loc[(df["SPD"] >= high_spd_cut) & (closure_signal < 1), base_cols].copy(),
        "Weak Listening + Follow-Up Leakage": df.loc[(df["Listening"] < df["Listening"].median()) & (followup_signal >= 1), base_cols].copy(),
    }
    for key, table in exceptions.items():
        if not table.empty:
            exceptions[key] = table.sort_values("SPD", ascending=(key != "High Potential + Low Closure")).reset_index(drop=True)
    return exceptions


def get_role_summary(role_view: str, snapshot: dict[str, str], phase1_kpis: dict[str, float | str], team_metrics: pd.DataFrame) -> tuple[str, str]:
    lead_team = team_metrics.iloc[0]["Team / Vendor"] if not team_metrics.empty else "current focus team"
    if role_view == "Managers":
        return (
            "Managers should work the lowest-SPD coaching queue first.",
            f"Focus on follow-up leakage, unresolved risk, and the top driver gaps in {lead_team}.",
        )
    if role_view == "Training":
        return (
            "Training should prioritize the weakest high-impact behavior.",
            f"Use coaching around {snapshot['lowest_parameter']} while tracking the coaching priority index at {format_metric_value(phase1_kpis['Coaching Priority Index'])}.",
        )
    if role_view == "Operations":
        return (
            "Operations should reduce friction before adding more activity.",
            f"Watch unresolved risk at {format_metric_value(phase1_kpis['Unresolved Risk Rate'])} and review consistency breakdowns in {lead_team}.",
        )
    return (
        "Leadership should manage the business through risk, opportunity, and momentum.",
        f"Positive intent is at {format_metric_value(phase1_kpis['Positive Intent Rate'])}, while payment completion sits at {format_metric_value(phase1_kpis['Payment Completion Rate'])}.",
    )


def fit_expected_spd_model(df: pd.DataFrame, parameter_metrics: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, float]]:
    driver_metrics = parameter_metrics.head(min(4, len(parameter_metrics)))
    driver_cols = driver_metrics["Column"].tolist()
    if not driver_cols:
        result = df.copy()
        result["Expected SPD"] = np.nan
        result["SPD Gap vs Expected"] = np.nan
        return result, {"r2": np.nan, "drivers": 0}

    model_df = df.dropna(subset=["SPD", *driver_cols]).copy()
    result = df.copy()
    if len(model_df) < max(5, len(driver_cols) + 1):
        result["Expected SPD"] = np.nan
        result["SPD Gap vs Expected"] = np.nan
        return result, {"r2": np.nan, "drivers": len(driver_cols)}

    X = model_df[driver_cols].astype(float).to_numpy()
    y = model_df["SPD"].astype(float).to_numpy()
    X_aug = np.column_stack([np.ones(len(X)), X])
    coef, _, _, _ = np.linalg.lstsq(X_aug, y, rcond=None)
    predicted = X_aug @ coef
    ss_res = float(np.sum((y - predicted) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    r2 = 1 - ss_res / ss_tot if ss_tot else np.nan

    all_valid = result[driver_cols].notna().all(axis=1)
    result["Expected SPD"] = np.nan
    if all_valid.any():
        all_X = result.loc[all_valid, driver_cols].astype(float).to_numpy()
        result.loc[all_valid, "Expected SPD"] = np.column_stack([np.ones(len(all_X)), all_X]) @ coef
    result["SPD Gap vs Expected"] = result["SPD"] - result["Expected SPD"]
    return result, {"r2": r2, "drivers": len(driver_cols), "driver_cols": driver_cols}


def get_phase2_benchmarks(df: pd.DataFrame, modeled_df: pd.DataFrame) -> dict[str, float]:
    outlier_share = float(df["Is Outlier SPD"].mean() * 100) if "Is Outlier SPD" in df.columns and len(df) else np.nan
    return {
        "Median SPD": float(df["SPD"].median()) if df["SPD"].notna().any() else np.nan,
        "Top Quartile SPD": float(df["SPD"].quantile(0.75)) if df["SPD"].notna().any() else np.nan,
        "Median Quality": float(df["Overall Quality Score"].median()) if df["Overall Quality Score"].notna().any() else np.nan,
        "Top Quartile Quality": float(df["Overall Quality Score"].quantile(0.75)) if df["Overall Quality Score"].notna().any() else np.nan,
        "Sample Size": float(len(df)),
        "Outlier Share %": outlier_share,
        "Expected SPD Coverage %": float(modeled_df["Expected SPD"].notna().mean() * 100) if len(modeled_df) else np.nan,
    }


def get_confidence_summary(df: pd.DataFrame, model_meta: dict[str, float]) -> dict[str, str]:
    sample_size = len(df)
    if sample_size >= 50:
        sample_label = "High"
    elif sample_size >= 25:
        sample_label = "Medium"
    else:
        sample_label = "Low"

    r2 = model_meta.get("r2", np.nan)
    if pd.isna(r2):
        model_label = "Insufficient"
    elif r2 >= 0.35:
        model_label = "Strong"
    elif r2 >= 0.18:
        model_label = "Moderate"
    else:
        model_label = "Weak"

    outlier_share = float(df["Is Outlier SPD"].mean() * 100) if "Is Outlier SPD" in df.columns and len(df) else np.nan
    if pd.isna(outlier_share):
        outlier_label = "Unknown"
    elif outlier_share <= 5:
        outlier_label = "Stable"
    elif outlier_share <= 12:
        outlier_label = "Watch"
    else:
        outlier_label = "Sensitive"

    return {
        "Sample confidence": sample_label,
        "Model strength": model_label,
        "Outlier sensitivity": outlier_label,
        "Trend status": "Trend-ready only: no historical date field in current source",
    }


def get_phase2_segments(modeled_df: pd.DataFrame) -> pd.DataFrame:
    if modeled_df.empty or "Expected SPD" not in modeled_df.columns:
        return pd.DataFrame()

    segmented = modeled_df.dropna(subset=["SPD", "Expected SPD"]).copy()
    if segmented.empty:
        return segmented

    segmented["Performance Segment"] = np.select(
        [
            segmented["SPD Gap vs Expected"] >= 0.2,
            segmented["SPD Gap vs Expected"] <= -0.2,
        ],
        ["Outperforming Benchmark", "Below Benchmark"],
        default="On Benchmark",
    )
    return segmented


def simulate_spd_uplift(
    df: pd.DataFrame, parameter_metrics: pd.DataFrame, settings: dict[str, object]
) -> tuple[pd.DataFrame, float]:
    top3 = parameter_metrics.head(min(3, len(parameter_metrics))).copy()
    if top3.empty:
        return pd.DataFrame(), np.nan

    base_spd = float(df["SPD"].mean()) if df["SPD"].notna().any() else np.nan
    rows = []
    estimated_spd = base_spd
    for idx, row in top3.iterrows():
        key = f"sim_{row['Column']}"
        change = float(settings.get(key, 0.0))
        estimated_gain = change * float(row["Correlation"]) * 0.08 if pd.notna(row["Correlation"]) else 0.0
        estimated_spd += estimated_gain if pd.notna(estimated_spd) else 0.0
        rows.append(
            {
                "Parameter": row["Parameter"],
                "Display Parameter": display_label(row["Parameter"]),
                "Change": change,
                "Correlation": row["Correlation"],
                "Estimated SPD Impact": estimated_gain,
            }
        )
    return pd.DataFrame(rows), estimated_spd


def get_trend_summary(df: pd.DataFrame) -> pd.DataFrame:
    if "Snapshot Date" not in df.columns or df["Snapshot Date"].isna().all():
        return pd.DataFrame()

    trend = (
        df.groupby("Snapshot Date", as_index=False)
        .agg(
            {
                "SPD": "mean",
                "Overall Quality Score": "mean",
                "Positive": "mean",
                ".payment_done": "mean",
                ".unresolved": "mean",
            }
        )
        .sort_values("Snapshot Date")
    )
    if trend.empty:
        return trend
    trend["Positive Intent Rate"] = trend["Positive"] * (100 if trend["Positive"].max() <= 1 else 1)
    trend["Payment Completion Rate"] = trend[".payment_done"] * (100 if trend[".payment_done"].max() <= 1 else 1)
    trend["Unresolved Risk Rate"] = trend[".unresolved"] * (100 if trend[".unresolved"].max() <= 1 else 1)
    return trend


def get_team_momentum(df: pd.DataFrame) -> pd.DataFrame:
    if "Snapshot Date" not in df.columns or df["Snapshot Date"].nunique() < 2:
        return pd.DataFrame()

    grouped = (
        df.groupby(["Snapshot Date", "Team / Vendor"], as_index=False)["SPD"]
        .mean()
        .sort_values(["Team / Vendor", "Snapshot Date"])
    )
    latest_dates = grouped["Snapshot Date"].drop_duplicates().sort_values().tolist()
    recent_dates = latest_dates[-2:]
    compare = grouped[grouped["Snapshot Date"].isin(recent_dates)].copy()
    pivot = compare.pivot(index="Team / Vendor", columns="Snapshot Date", values="SPD").reset_index()
    if len(recent_dates) == 2:
        left, right = recent_dates
        pivot["Momentum"] = pivot[right] - pivot[left]
        pivot = pivot.rename(columns={left: "Previous SPD", right: "Latest SPD"})
    return pivot.sort_values("Momentum", ascending=False).reset_index(drop=True)


def get_parameter_metrics(df: pd.DataFrame, parameter_catalog: dict[str, str]) -> pd.DataFrame:
    rows = []
    for label, column in parameter_catalog.items():
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
    metrics["Gap Magnitude"] = metrics["Gap"].abs()
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


def get_team_metrics(
    df: pd.DataFrame, parameter_metrics: pd.DataFrame, parameter_catalog: dict[str, str]
) -> pd.DataFrame:
    rows = []
    driver_cols = parameter_metrics.sort_values("Driver Score", ascending=False).head(3)["Column"].tolist()
    high_spd = df["SPD"].quantile(0.7) if df["SPD"].notna().any() else np.nan

    for team, group in df.groupby("Team / Vendor", dropna=False):
        if len(group) == 0:
            continue
        parameter_means = group[list(parameter_catalog.values())].mean().astype(float)
        if parameter_means.isna().all():
            weakest_label = "No valid parameter score"
        else:
            weakest_idx = parameter_means.idxmin()
            weakest_label = next(label for label, col in parameter_catalog.items() if col == weakest_idx)
        consistency_values = [group[col].std() for col in parameter_catalog.values()]
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
        if consistency >= np.nanmean([df[col].std() for col in parameter_catalog.values()]):
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
    parameter_view: str,
) -> dict[str, str]:
    top_driver = parameter_metrics.iloc[0]
    lowest_parameter = parameter_metrics.sort_values("Average Score").iloc[0]
    weakest_driver = parameter_metrics.sort_values("Correlation").iloc[0]
    highest_gap = parameter_metrics.sort_values("Gap", ascending=False).iloc[0]
    primary_team = team_metrics.iloc[0]["Team / Vendor"] if not team_metrics.empty else "No team"
    focus_parameters = get_driver_focus(parameter_metrics)
    focus_line = ", ".join(focus_parameters[:2]) if len(focus_parameters) >= 2 else focus_parameters[0]

    what = (
        f"SPD averages {df['SPD'].mean():.2f} in the current selection, while the strongest driver in the {parameter_view.lower()} view is "
        f"{top_driver['Parameter']}."
    )
    why = (
        f"High performers outperform low performers most on {highest_gap['Parameter']} "
        f"({highest_gap['Gap %']:.1f}% gap), while {lowest_parameter['Parameter']} is the lowest absolute score in scope."
    )
    next_step = (
        f"Prioritize {lowest_parameter['Parameter']} for training, review execution stability in {primary_team}, "
        f"and coach managers on {focus_line} first."
    )
    caveat = (
        "Outlier-adjusted view is active, so the dashboard is prioritizing the stable underlying pattern."
        if outlier_mode == "Outlier-adjusted view"
        else "Raw view is active, so one extreme SPD outlier may distort the driver ranking."
    )
    theme_summary = summarize_driver_themes(parameter_metrics)
    return {
        "what": what,
        "why": why,
        "next": next_step,
        "caveat": caveat,
        "theme_summary": theme_summary,
        "top_driver": top_driver["Parameter"],
        "weakest_driver": weakest_driver["Parameter"],
        "lowest_parameter": lowest_parameter["Parameter"],
    }


def render_insight_panel(snapshot: dict[str, str], parameter_metrics: pd.DataFrame) -> None:
    top_two = [display_label(item) for item in parameter_metrics.head(2)["Parameter"].tolist()]
    weak = display_label(snapshot["lowest_parameter"])
    st.markdown(
        f"""
        <div class="insight-card">
            <div class="section-title">What / Why / What Next</div>
            <div class="tiny-label">Fast read</div>
            <div class="insight-bullet"><div class="tiny-label">What is happening</div><div class="insight-line">{snapshot["what"]}</div></div>
            <div class="insight-bullet"><div class="tiny-label">Why it is happening</div><div class="insight-line">{snapshot["why"]}</div></div>
            <div class="insight-bullet"><div class="tiny-label">What should be done</div><div class="insight-line">{snapshot["next"]}</div></div>
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
    modeled_df: pd.DataFrame,
    parameter_metrics: pd.DataFrame,
    team_metrics: pd.DataFrame,
    agent_risks: pd.DataFrame,
    model_meta: dict[str, float],
    outlier_mode: str,
    parameter_view: str,
    settings: dict[str, object],
) -> None:
    snapshot = decision_snapshot(df, parameter_metrics, team_metrics, outlier_mode, parameter_view)
    phase1_kpis = get_phase1_kpis(df, team_metrics, agent_risks)
    phase2_benchmarks = get_phase2_benchmarks(df, modeled_df)
    confidence = get_confidence_summary(df, model_meta)
    comparison = build_comparison_frame(
        df,
        settings["compare_mode"],
        settings["compare_left"],
        settings["compare_right"],
    )
    exceptions = get_exception_tables(df)
    role_headline, role_detail = get_role_summary(settings["role_view"], snapshot, phase1_kpis, team_metrics)
    hero(
        "Executive Brief",
        f"{selection_label(df)} | {outlier_mode} | {parameter_view} | Decision focus: what is happening, why, and what leadership should do next",
    )
    render_filter_summary(df, settings, parameter_metrics)

    weakest = parameter_metrics.sort_values("Average Score").iloc[0]
    st.markdown('<div class="kpi-row">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Avg SPD", f"{df['SPD'].mean():.2f}", "Current sales productivity")
    with c2:
        metric_card(
            "Positive Intent / Payment",
            f"{format_metric_value(phase1_kpis['Positive Intent Rate'])} / {format_metric_value(phase1_kpis['Payment Completion Rate'])}",
            "Intent creation vs closure conversion",
        )
    with c3:
        metric_card(
            "Risk / Follow-Up",
            f"{format_metric_value(phase1_kpis['Unresolved Risk Rate'])} / {format_metric_value(phase1_kpis['Follow-Up Rate'])}",
            "Unresolved risk and pending follow-up load",
        )
    with c4:
        metric_card(
            "Coaching / Consistency",
            f"{format_metric_value(phase1_kpis['Coaching Priority Index'])} / {format_metric_value(phase1_kpis['Team Consistency Index'])}",
            f"{df['Agent Name'].nunique()} agents | {len(parameter_metrics)} drivers in scope",
        )
    st.markdown("</div>", unsafe_allow_html=True)

    left, right = st.columns([2.2, 0.95], gap="medium")
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
            height=520,
        )
        st.plotly_chart(fig, use_container_width=True)
        section_close()
    with right:
        render_insight_panel(snapshot, parameter_metrics)

    section_open()
    ranking = parameter_metrics.head(int(settings["top_n"])).copy().sort_values(settings["ranking_basis"], ascending=True)
    ranking["Display Parameter"] = ranking["Parameter"].map(display_label)
    ranking["Color"] = np.where(
        ranking["Action Priority"] == "Fix Now",
        RED,
        np.where(ranking["Action Priority"] == "Coach Next", AMBER, GREEN),
    )
    fig = go.Figure(
        data=[
            go.Bar(
                x=ranking[settings["ranking_basis"]],
                y=ranking["Display Parameter"],
                orientation="h",
                marker_color=ranking["Color"],
                customdata=np.stack(
                    [
                        ranking[settings["ranking_basis"]].round(2),
                        ranking["Correlation"].round(3),
                        ranking["Gap %"].round(1),
                        ranking["Average Score"].round(2),
                        ranking["Action Priority"],
                    ],
                    axis=-1,
                ),
                hovertemplate=(
                    "Parameter: %{y}<br>Selected rank value: %{customdata[0]}"
                    "<br>Correlation: %{customdata[1]}"
                    "<br>High vs Low gap: %{customdata[2]}%"
                    "<br>Average score: %{customdata[3]}"
                    "<br>Priority: %{customdata[4]}<extra></extra>"
                ),
            )
        ]
    )
    fig.update_layout(
        title=f"Driver ranking: top {settings['top_n']} parameters in current analysis lens",
        paper_bgcolor=SURFACE,
        plot_bgcolor=SURFACE,
        xaxis_title=str(settings["ranking_basis"]),
        yaxis_title="",
        margin=dict(l=10, r=10, t=50, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)
    section_close()
    render_parameter_overview(parameter_metrics, int(settings["top_n"]))

    section_open()
    a, b, c = st.columns(3)
    with a:
        st.markdown("**So what?**")
        st.write(
            summarize_driver_themes(parameter_metrics)
        )
    with b:
        st.markdown("**Why it matters**")
        st.write(
            f"The biggest SPD gains in the {parameter_view.lower()} view will come from the highest-ranked driver cluster rather than spreading effort evenly."
        )
    with c:
        st.markdown("**What next?**")
        st.write(
            f"Give Training ownership of `{snapshot['lowest_parameter']}`, Ops ownership of the highest-risk team, and Managers ownership of `{snapshot['top_driver']}` coaching."
        )
    section_close()

    c1, c2 = st.columns([1.1, 1.0], gap="large")
    with c1:
        section_open()
        st.markdown("**Top Risks and Opportunities**")
        risk_opportunity = pd.DataFrame(
            [
                {"Signal": "Positive intent rate", "Value": format_metric_value(phase1_kpis["Positive Intent Rate"]), "Readout": "Opportunity pipeline being created"},
                {"Signal": "Payment completion rate", "Value": format_metric_value(phase1_kpis["Payment Completion Rate"]), "Readout": "Closure efficiency from current leads"},
                {"Signal": "Unresolved risk rate", "Value": format_metric_value(phase1_kpis["Unresolved Risk Rate"]), "Readout": "Calls or cases likely to drag conversion"},
                {"Signal": "Resolution effectiveness", "Value": format_metric_value(phase1_kpis["Resolution Effectiveness"]), "Readout": "Resolved minus unresolved risk balance"},
            ]
        )
        st.dataframe(risk_opportunity, use_container_width=True, height=220)
        st.markdown("**Role recommendation**")
        st.write(f"{role_headline} {role_detail}")
        section_close()
    with c2:
        section_open()
        st.markdown("**Compare Mode**")
        if comparison.empty:
            st.info("Choose a compare mode and two groups in the sidebar to unlock side-by-side comparison.")
        else:
            compare_fig = go.Figure()
            compare_fig.add_bar(name="Avg SPD", x=comparison["Group"], y=comparison["Avg SPD"], marker_color=BLUE)
            compare_fig.add_bar(name="Payment Completion Rate", x=comparison["Group"], y=comparison["Payment Completion Rate"], marker_color=GREEN)
            compare_fig.add_bar(name="Unresolved Risk Rate", x=comparison["Group"], y=comparison["Unresolved Risk Rate"], marker_color=RED)
            compare_fig.update_layout(
                barmode="group",
                paper_bgcolor=SURFACE,
                plot_bgcolor=SURFACE,
                margin=dict(l=10, r=10, t=20, b=10),
                legend_orientation="h",
                legend_y=1.1,
            )
            st.plotly_chart(compare_fig, use_container_width=True)
            st.dataframe(
                comparison.style.format(
                    {
                        "Avg SPD": "{:.2f}",
                        "Avg Quality": "{:.2f}",
                        "Positive Intent Rate": "{:.1f}",
                        "Payment Completion Rate": "{:.1f}",
                        "Unresolved Risk Rate": "{:.1f}",
                    }
                ),
                use_container_width=True,
                height=180,
            )
        section_close()

    section_open()
    st.markdown("**Phase 1 Exceptions**")
    e1, e2, e3 = st.columns(3, gap="large")
    for col, (title, table) in zip([e1, e2, e3], exceptions.items()):
        with col:
            st.markdown(f"**{title}**")
            if table.empty:
                st.caption("No exception cases in current filters.")
            else:
                st.dataframe(table.head(8).style.format({"SPD": "{:.2f}", "Overall Quality Score": "{:.2f}"}), use_container_width=True, height=220)
    section_close()

    c1, c2 = st.columns([1.0, 1.1], gap="large")
    with c1:
        section_open()
        st.markdown("**Phase 2 Confidence and Benchmarks**")
        benchmark_df = pd.DataFrame(
            [
                {"Measure": "Median SPD", "Value": f"{phase2_benchmarks['Median SPD']:.2f}" if pd.notna(phase2_benchmarks['Median SPD']) else "-"},
                {"Measure": "Top Quartile SPD", "Value": f"{phase2_benchmarks['Top Quartile SPD']:.2f}" if pd.notna(phase2_benchmarks['Top Quartile SPD']) else "-"},
                {"Measure": "Expected SPD Coverage", "Value": format_metric_value(phase2_benchmarks["Expected SPD Coverage %"])},
                {"Measure": "Outlier Share", "Value": format_metric_value(phase2_benchmarks["Outlier Share %"])},
                {"Measure": "Sample confidence", "Value": confidence["Sample confidence"]},
                {"Measure": "Model strength", "Value": confidence["Model strength"]},
            ]
        )
        st.dataframe(benchmark_df, use_container_width=True, height=245)
        st.caption(confidence["Trend status"])
        section_close()
    with c2:
        section_open()
        st.markdown("**Expected vs Actual SPD**")
        segment_df = get_phase2_segments(modeled_df)
        if segment_df.empty:
            st.info("Not enough complete rows to estimate expected SPD for this filter selection.")
        else:
            segment_summary = (
                segment_df.groupby("Performance Segment", as_index=False)
                .agg({"Agent Name": "count", "SPD Gap vs Expected": "mean"})
                .rename(columns={"Agent Name": "Agents"})
            )
            seg_fig = px.bar(
                segment_summary,
                x="Performance Segment",
                y="Agents",
                color="SPD Gap vs Expected",
                color_continuous_scale=[[0, RED], [0.5, BLUE], [1, GREEN]],
                title="Performance vs expected benchmark",
            )
            seg_fig.update_layout(
                paper_bgcolor=SURFACE,
                plot_bgcolor=SURFACE,
                coloraxis_showscale=False,
                margin=dict(l=10, r=10, t=45, b=10),
            )
            st.plotly_chart(seg_fig, use_container_width=True)
            st.dataframe(
                segment_df[["Agent Name", "Team / Vendor", "SPD", "Expected SPD", "SPD Gap vs Expected", "Performance Segment"]]
                .sort_values("SPD Gap vs Expected")
                .head(10)
                .style.format({"SPD": "{:.2f}", "Expected SPD": "{:.2f}", "SPD Gap vs Expected": "{:.2f}"}),
                use_container_width=True,
                height=210,
            )
        section_close()


def root_cause_page(
    df: pd.DataFrame,
    parameter_metrics: pd.DataFrame,
    team_metrics: pd.DataFrame,
    parameter_catalog: dict[str, str],
    parameter_view: str,
    settings: dict[str, object],
) -> None:
    hero(
        "Root Cause",
        f"{selection_label(df)} | {parameter_view} | Locate where SPD is breaking: team, agent, parameter, or execution consistency",
    )
    render_filter_summary(df, settings, parameter_metrics)

    section_open()
    gap_df = parameter_metrics.head(int(settings["top_n"])).copy().sort_values("Gap", ascending=True)
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
            df.groupby("Team / Vendor")[list(parameter_catalog.values())]
            .mean()
            .rename(columns={v: k for k, v in parameter_catalog.items()})
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
            ["Team / Vendor", "Agent Name", "Overall Quality Score", *parameter_catalog.values()],
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
    parameter_view: str,
    settings: dict[str, object],
) -> None:
    hero(
        "Action Center",
        f"{selection_label(df)} | {parameter_view} | Function-specific action plans for Training, Operations, and Managers",
    )
    render_filter_summary(df, settings, parameter_metrics)

    lowest_score = parameter_metrics.sort_values("Average Score").iloc[0]
    top_driver = parameter_metrics.iloc[0]
    team_issue = team_metrics.iloc[0] if not team_metrics.empty else None
    phase1_kpis = get_phase1_kpis(df, team_metrics, agent_risks)
    role_headline, role_detail = get_role_summary(
        settings["role_view"],
        {
            "lowest_parameter": lowest_score["Parameter"],
            "top_driver": top_driver["Parameter"],
        },
        phase1_kpis,
        team_metrics,
    )

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
        driver_focus = get_driver_focus(parameter_metrics)
        coach_line = ", ".join(driver_focus[:2])
        third_focus = driver_focus[2] if len(driver_focus) > 2 else driver_focus[-1]
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
                    Managers should coach low-SPD agents on <b>{coach_line}</b> and <b>{third_focus}</b> to improve the strongest SPD-linked behaviors in the current view. {extra}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    c1, c2 = st.columns([1.2, 1.15], gap="large")
    with c1:
        section_open()
        radar_rows = []
        radar_catalog = parameter_metrics.head(min(int(settings["top_n"]), 6))
        for _, metric_row in radar_catalog.iterrows():
            label = metric_row["Parameter"]
            column = metric_row["Column"]
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
        driver_opportunity = parameter_metrics.head(int(settings["top_n"])).copy()
        opp = px.scatter(
            driver_opportunity,
            x="Average Score",
            y="Driver Score",
            size="Gap Magnitude",
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

    section_open()
    st.markdown(f"**{settings['role_view']} Priority View**")
    st.write(role_headline)
    st.write(role_detail)
    st.dataframe(
        pd.DataFrame(
            [
                {"KPI": "Positive Intent Rate", "Value": format_metric_value(phase1_kpis["Positive Intent Rate"])},
                {"KPI": "Payment Completion Rate", "Value": format_metric_value(phase1_kpis["Payment Completion Rate"])},
                {"KPI": "Unresolved Risk Rate", "Value": format_metric_value(phase1_kpis["Unresolved Risk Rate"])},
                {"KPI": "Coaching Priority Index", "Value": format_metric_value(phase1_kpis["Coaching Priority Index"])},
            ]
        ),
        use_container_width=True,
        height=210,
    )
    section_close()


def diagnostics_page(
    df: pd.DataFrame, parameter_metrics: pd.DataFrame, parameter_view: str, settings: dict[str, object]
) -> None:
    hero(
        "Diagnostics",
        f"{selection_label(df)} | {parameter_view} | Detailed evidence for validation and coaching drill-down",
    )
    render_filter_summary(df, settings, parameter_metrics)

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
        diagnostic_options = parameter_metrics["Parameter"].tolist()
        default_parameters = diagnostic_options[: min(6, len(diagnostic_options))]
        selected_parameters = st.multiselect(
            "Diagnostic parameters",
            diagnostic_options,
            default=default_parameters,
            key="diagnostic_parameters",
        )
        selected_metrics = parameter_metrics[parameter_metrics["Parameter"].isin(selected_parameters)].copy()
        if selected_metrics.empty:
            st.info("Select at least one parameter to view SPD scatter diagnostics.")
            section_close()
            return

        chart_count = len(selected_metrics)
        cols = min(3, chart_count)
        rows = int(np.ceil(chart_count / cols))
        fig = make_subplots(
            rows=rows,
            cols=cols,
            subplot_titles=selected_metrics["Parameter"].tolist(),
            horizontal_spacing=0.08,
            vertical_spacing=0.16,
        )
        positions = [(idx // cols + 1, idx % cols + 1) for idx in range(chart_count)]
        for (_, metric_row), (row, col) in zip(selected_metrics.iterrows(), positions):
            label = metric_row["Parameter"]
            column = metric_row["Column"]
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
            height=max(420, rows * 310),
            margin=dict(l=10, r=10, t=55, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)
        section_close()


def performance_lab_page(
    df: pd.DataFrame,
    modeled_df: pd.DataFrame,
    parameter_metrics: pd.DataFrame,
    model_meta: dict[str, float],
    settings: dict[str, object],
) -> None:
    hero(
        "Performance Lab",
        "Benchmark intelligence, expected SPD modeling, and what-if simulation using current snapshot data",
    )
    render_filter_summary(df, settings, parameter_metrics)

    phase2_benchmarks = get_phase2_benchmarks(df, modeled_df)
    confidence = get_confidence_summary(df, model_meta)
    sim_df, estimated_spd = simulate_spd_uplift(df, parameter_metrics, settings)
    segment_df = get_phase2_segments(modeled_df)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Median SPD", f"{phase2_benchmarks['Median SPD']:.2f}" if pd.notna(phase2_benchmarks["Median SPD"]) else "-", "Current benchmark midpoint")
    with c2:
        metric_card("Top Quartile SPD", f"{phase2_benchmarks['Top Quartile SPD']:.2f}" if pd.notna(phase2_benchmarks["Top Quartile SPD"]) else "-", "Current aspirational benchmark")
    with c3:
        metric_card("Model Strength", confidence["Model strength"], f"Expected SPD coverage {format_metric_value(phase2_benchmarks['Expected SPD Coverage %'])}")
    with c4:
        metric_card("Simulated SPD", f"{estimated_spd:.2f}" if pd.notna(estimated_spd) else "-", "What-if uplift from Phase 2 lab controls")

    c1, c2 = st.columns([1.0, 1.1], gap="large")
    with c1:
        section_open()
        st.markdown("**Simulation Controls Readout**")
        if sim_df.empty:
            st.info("No simulation drivers available in the current parameter scope.")
        else:
            sim_df["Display Parameter"] = sim_df["Display Parameter"].fillna(sim_df["Parameter"])
            st.dataframe(
                sim_df[["Display Parameter", "Change", "Correlation", "Estimated SPD Impact"]]
                .rename(columns={"Display Parameter": "Parameter"})
                .style.format({"Change": "{:.1f}", "Correlation": "{:.3f}", "Estimated SPD Impact": "{:.2f}"}),
                use_container_width=True,
                height=220,
            )
            st.caption("Estimated SPD impact is a lightweight simulation using current correlations. It is directional, not a forecast.")
        section_close()
    with c2:
        section_open()
        st.markdown("**Confidence Readout**")
        st.dataframe(
            pd.DataFrame(
                [
                    {"Dimension": key, "Status": value}
                    for key, value in confidence.items()
                ]
            ),
            use_container_width=True,
            height=220,
        )
        section_close()

    section_open()
    st.markdown("**Performance Segmentation**")
    if segment_df.empty:
        st.info("Expected-vs-actual segmentation is not available for the current filter selection.")
    else:
        seg_fig = px.scatter(
            segment_df,
            x="Expected SPD",
            y="SPD",
            color="Performance Segment",
            hover_data=["Agent Name", "Team / Vendor", "SPD Gap vs Expected"],
            color_discrete_map={
                "Outperforming Benchmark": GREEN,
                "On Benchmark": BLUE,
                "Below Benchmark": RED,
            },
            title="Actual SPD vs expected SPD benchmark",
        )
        add_trendline(seg_fig, segment_df, "Expected SPD", "SPD")
        seg_fig.update_layout(
            paper_bgcolor=SURFACE,
            plot_bgcolor=SURFACE,
            margin=dict(l=10, r=10, t=45, b=10),
            height=460,
        )
        st.plotly_chart(seg_fig, use_container_width=True)
        st.dataframe(
            segment_df[["Agent Name", "Team / Vendor", "SPD", "Expected SPD", "SPD Gap vs Expected", "Performance Segment"]]
            .sort_values("SPD Gap vs Expected")
            .style.format({"SPD": "{:.2f}", "Expected SPD": "{:.2f}", "SPD Gap vs Expected": "{:.2f}"}),
            use_container_width=True,
            height=280,
        )
    section_close()


def trends_page(df: pd.DataFrame, settings: dict[str, object]) -> None:
    hero(
        "Trends",
        "Historical snapshot trends for SPD, quality, and sales outcome movement",
    )
    render_filter_summary(df, settings, pd.DataFrame([{"Parameter": "History", "Correlation": np.nan}]))

    trend = get_trend_summary(df)
    team_momentum = get_team_momentum(df)

    if trend.empty:
        st.warning("No snapshot history is available yet. Ingest dated snapshots to unlock true trend analysis.")
        return

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        metric_card("Snapshots", str(df["Snapshot Date"].nunique()), "Historical points in current filter")
    with c2:
        metric_card("Latest SPD", f"{trend['SPD'].iloc[-1]:.2f}", "Most recent average SPD")
    with c3:
        metric_card("Latest Quality", f"{trend['Overall Quality Score'].iloc[-1]:.2f}", "Most recent average quality score")
    with c4:
        if len(trend) >= 2:
            delta = trend["SPD"].iloc[-1] - trend["SPD"].iloc[-2]
            metric_card("SPD Change", f"{delta:+.2f}", "Latest snapshot vs previous snapshot")
        else:
            metric_card("SPD Change", "-", "Add another snapshot to see movement")

    section_open()
    if len(trend) < 2:
        st.info("Only one snapshot is available so far. The page is trend-ready; once you ingest the next dated snapshot, these visuals will show movement and momentum.")
    else:
        trend_fig = make_subplots(specs=[[{"secondary_y": True}]])
        trend_fig.add_trace(
            go.Scatter(x=trend["Snapshot Date"], y=trend["SPD"], mode="lines+markers", name="SPD", line=dict(color=BLUE, width=3)),
            secondary_y=False,
        )
        trend_fig.add_trace(
            go.Scatter(x=trend["Snapshot Date"], y=trend["Overall Quality Score"], mode="lines+markers", name="Quality", line=dict(color=GREEN, width=3)),
            secondary_y=True,
        )
        trend_fig.update_layout(
            title="SPD and Quality trend by snapshot date",
            paper_bgcolor=SURFACE,
            plot_bgcolor=SURFACE,
            margin=dict(l=10, r=10, t=45, b=10),
            height=420,
        )
        trend_fig.update_yaxes(title_text="SPD", secondary_y=False)
        trend_fig.update_yaxes(title_text="Quality Score", secondary_y=True)
        st.plotly_chart(trend_fig, use_container_width=True)
    section_close()

    c1, c2 = st.columns([1.05, 1.0], gap="large")
    with c1:
        section_open()
        outcome_fig = go.Figure()
        outcome_fig.add_trace(go.Scatter(x=trend["Snapshot Date"], y=trend["Positive Intent Rate"], mode="lines+markers", name="Positive Intent Rate", line=dict(color=GREEN, width=2)))
        outcome_fig.add_trace(go.Scatter(x=trend["Snapshot Date"], y=trend["Payment Completion Rate"], mode="lines+markers", name="Payment Completion Rate", line=dict(color=BLUE, width=2)))
        outcome_fig.add_trace(go.Scatter(x=trend["Snapshot Date"], y=trend["Unresolved Risk Rate"], mode="lines+markers", name="Unresolved Risk Rate", line=dict(color=RED, width=2)))
        outcome_fig.update_layout(
            title="Outcome trend by snapshot date",
            paper_bgcolor=SURFACE,
            plot_bgcolor=SURFACE,
            margin=dict(l=10, r=10, t=45, b=10),
            height=420,
        )
        st.plotly_chart(outcome_fig, use_container_width=True)
        section_close()
    with c2:
        section_open()
        st.markdown("**Team Momentum**")
        if team_momentum.empty:
            st.info("Team momentum will appear once at least two snapshot dates exist.")
        else:
            st.dataframe(
                team_momentum.style.format({"Previous SPD": "{:.2f}", "Latest SPD": "{:.2f}", "Momentum": "{:+.2f}"}),
                use_container_width=True,
                height=360,
            )
        section_close()


def main() -> None:
    inject_css()
    df = load_data()
    filtered, settings = filter_data(df)
    outlier_mode = settings["outlier_mode"]
    parameter_view = settings["parameter_view"]

    if filtered.empty:
        st.warning("No data available for the current filters. Adjust the slicers to continue.")
        return

    parameter_catalog = get_parameter_catalog(parameter_view)
    parameter_metrics = get_parameter_metrics(filtered, parameter_catalog)
    parameter_metrics = apply_parameter_filters(parameter_metrics, settings)
    if parameter_metrics.empty:
        st.warning("No parameter drivers match the current analysis lens. Broaden the theme or priority filters.")
        return

    selected_catalog = build_catalog_from_metrics(parameter_metrics)
    team_metrics = get_team_metrics(filtered, parameter_metrics, selected_catalog)
    agent_risks = get_agent_risks(filtered, parameter_metrics)
    modeled_df, model_meta = fit_expected_spd_model(filtered, parameter_metrics)

    page = st.sidebar.radio(
        "Navigation",
        ["Executive Brief", "Trends", "Root Cause", "Action Center", "Diagnostics", "Performance Lab"],
    )

    if page == "Executive Brief":
        executive_brief_page(filtered, modeled_df, parameter_metrics, team_metrics, agent_risks, model_meta, outlier_mode, parameter_view, settings)
    elif page == "Trends":
        trends_page(filtered, settings)
    elif page == "Root Cause":
        root_cause_page(filtered, parameter_metrics, team_metrics, selected_catalog, parameter_view, settings)
    elif page == "Action Center":
        action_center_page(filtered, parameter_metrics, team_metrics, agent_risks, parameter_view, settings)
    elif page == "Performance Lab":
        performance_lab_page(filtered, modeled_df, parameter_metrics, model_meta, settings)
    else:
        diagnostics_page(filtered, parameter_metrics, parameter_view, settings)


if __name__ == "__main__":
    main()
