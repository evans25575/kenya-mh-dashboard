"""
Kenya Mental Health Monitoring & Evaluation Dashboard
==================================
Streamlit application for county-level mental health monitoring.

Run:  streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Kenya MH M&E Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        color: #1a5276;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #5d6d7e;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #1a5276, #2471a3);
        padding: 1.2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
    }
    .stMetric label { font-size: 0.85rem !important; }
</style>
""", unsafe_allow_html=True)

# ── Data Loading ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("kenya_health_m_e_dataset.csv", parse_dates=["reporting_month"])
    return df

df = load_data()

# ── Sidebar Filters ───────────────────────────────────────────────────────────
st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Flag_of_Kenya.svg/320px-Flag_of_Kenya.svg.png",
    width=120,
)
st.sidebar.title("🔎 Filters")

counties = ["All Counties"] + sorted(df["county"].unique().tolist())
selected_county = st.sidebar.selectbox("County", counties)

years = ["All Years"] + sorted(df["reporting_year"].unique().tolist())
selected_year = st.sidebar.selectbox("Year", years)

quarters = ["All Quarters"] + sorted(df["reporting_quarter"].unique().tolist())
selected_quarter = st.sidebar.selectbox("Quarter", quarters)

st.sidebar.markdown("---")
st.sidebar.markdown("**Data Source:** Simulated DHIS2-style dataset  \n**Period:** Jan 2022 – Dec 2023  \n**Facilities:** 205  \n**Counties:** 41")

# ── Filter Logic ──────────────────────────────────────────────────────────────
filtered = df.copy()
if selected_county != "All Counties":
    filtered = filtered[filtered["county"] == selected_county]
if selected_year != "All Years":
    filtered = filtered[filtered["reporting_year"] == int(selected_year)]
if selected_quarter != "All Quarters":
    filtered = filtered[filtered["reporting_quarter"] == selected_quarter]

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<p class="main-header">🧠 Kenya Mental Health M&E Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Monitoring & Evaluation System — County & Facility Level Reporting</p>', unsafe_allow_html=True)

# ── KPI Row ───────────────────────────────────────────────────────────────────
col1, col2, col3, col4, col5 = st.columns(5)

total_screened   = filtered["patients_screened"].sum()
total_treated    = filtered["patients_treated"].sum()
avg_gap          = filtered["treatment_gap"].mean()
avg_rate         = filtered["treatment_rate"].mean()
total_unmet      = filtered["unmet_need"].sum()

col1.metric("🔬 Total Screened",    f"{total_screened:,}")
col2.metric("💊 Total Treated",     f"{total_treated:,}")
col3.metric("📉 Avg Treatment Gap", f"{avg_gap:.1%}")
col4.metric("✅ Avg Treatment Rate",f"{avg_rate:.1%}")
col5.metric("⚠️ Unmet Need",        f"{total_unmet:,}")

st.markdown("---")

# ── Row 1: Monthly Trend + County Comparison ──────────────────────────────────
col_a, col_b = st.columns([3, 2])

with col_a:
    st.subheader("📅 Monthly Screening & Treatment Trends")
    monthly = (
        filtered.groupby("reporting_month")[["patients_screened", "patients_treated"]]
        .sum()
        .reset_index()
    )
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=monthly["reporting_month"], y=monthly["patients_screened"],
        name="Screened", line=dict(color="#2471a3", width=2.5),
        fill="tozeroy", fillcolor="rgba(36,113,163,0.1)"
    ))
    fig_trend.add_trace(go.Scatter(
        x=monthly["reporting_month"], y=monthly["patients_treated"],
        name="Treated", line=dict(color="#1abc9c", width=2.5),
        fill="tozeroy", fillcolor="rgba(26,188,156,0.1)"
    ))
    fig_trend.update_layout(
        height=320, margin=dict(t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
        xaxis_title="Month", yaxis_title="Patients"
    )
    st.plotly_chart(fig_trend, use_container_width=True)

with col_b:
    st.subheader("🗺️ Treatment Gap by County")
    county_gap = (
        filtered.groupby("county")["treatment_gap"]
        .mean()
        .sort_values(ascending=False)
        .head(12)
        .reset_index()
    )
    fig_gap = px.bar(
        county_gap, x="treatment_gap", y="county", orientation="h",
        color="treatment_gap",
        color_continuous_scale=["#1abc9c", "#f39c12", "#e74c3c"],
        labels={"treatment_gap": "Treatment Gap", "county": "County"},
    )
    fig_gap.update_layout(
        height=320, margin=dict(t=10, b=10),
        coloraxis_showscale=False, yaxis=dict(autorange="reversed")
    )
    st.plotly_chart(fig_gap, use_container_width=True)

# ── Row 2: Facility Table + Scatter ──────────────────────────────────────────
col_c, col_d = st.columns([2, 3])

with col_c:
    st.subheader("🏥 Facility Performance")
    facility_perf = (
        filtered.groupby("facility_name")
        .agg(
            screened=("patients_screened", "sum"),
            treated=("patients_treated", "sum"),
            gap=("treatment_gap", "mean"),
        )
        .reset_index()
        .sort_values("gap", ascending=False)
    )
    facility_perf["gap"] = facility_perf["gap"].apply(lambda x: f"{x:.1%}")
    facility_perf.columns = ["Facility", "Screened", "Treated", "Gap"]
    st.dataframe(facility_perf.head(15), use_container_width=True, height=320)

with col_d:
    st.subheader("📊 Screened vs Treated — County Scatter")
    scatter_data = (
        filtered.groupby("county")
        .agg(
            screened=("patients_screened", "sum"),
            treated=("patients_treated", "sum"),
            gap=("treatment_gap", "mean"),
            prevalence=("mental_health_prevalence", "mean"),
        )
        .reset_index()
    )
    fig_scatter = px.scatter(
        scatter_data,
        x="screened", y="treated",
        size="prevalence", color="gap",
        hover_name="county",
        color_continuous_scale=["#1abc9c", "#e74c3c"],
        labels={"screened": "Total Screened", "treated": "Total Treated", "gap": "Treatment Gap"},
        size_max=30,
    )
    fig_scatter.add_shape(
        type="line", x0=0, y0=0,
        x1=scatter_data["screened"].max(),
        y1=scatter_data["screened"].max(),
        line=dict(dash="dash", color="gray", width=1),
    )
    fig_scatter.update_layout(height=320, margin=dict(t=10, b=10))
    st.plotly_chart(fig_scatter, use_container_width=True)

# ── Row 3: Quarterly Summary ──────────────────────────────────────────────────
st.markdown("---")
st.subheader("📆 Quarterly Performance Summary")
quarterly = (
    filtered.groupby(["reporting_year", "reporting_quarter"])
    .agg(
        screened=("patients_screened", "sum"),
        treated=("patients_treated", "sum"),
        gap=("treatment_gap", "mean"),
    )
    .reset_index()
)
quarterly["period"] = quarterly["reporting_year"].astype(str) + " " + quarterly["reporting_quarter"]
quarterly["gap_pct"] = (quarterly["gap"] * 100).round(1)

fig_q = make_subplots(specs=[[{"secondary_y": True}]])
fig_q.add_trace(go.Bar(x=quarterly["period"], y=quarterly["screened"], name="Screened", marker_color="#2471a3"))
fig_q.add_trace(go.Bar(x=quarterly["period"], y=quarterly["treated"], name="Treated", marker_color="#1abc9c"))
fig_q.add_trace(go.Scatter(x=quarterly["period"], y=quarterly["gap_pct"], name="Gap %", line=dict(color="#e74c3c", width=2), mode="lines+markers"), secondary_y=True)
fig_q.update_layout(barmode="group", height=300, margin=dict(t=10, b=10), legend=dict(orientation="h"))
fig_q.update_yaxes(title_text="Patients", secondary_y=False)
fig_q.update_yaxes(title_text="Treatment Gap (%)", secondary_y=True)
st.plotly_chart(fig_q, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "**Kenya Mental Health M&E System** · Built by Evans Kiplangat · "
    "Data Analyst | Digital Health Enthusiast · "
    "[GitHub](https://github.com/evankiplangat)"
)
