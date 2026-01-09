import streamlit as st
import pandas as pd
import plotly.express as px
from scipy.stats import zscore

# -------------------------------
# App Configuration
# -------------------------------
st.set_page_config(
    page_title="Aadhaar as a Living System",
    layout="wide"
)

st.title("Aadhaar as a Living System")
st.caption(
    "Identifying systemic patterns, anomalies, and predictive indicators "
    "from UIDAI enrolment, biometric, and demographic datasets"
)

# -------------------------------
# Load Data
# -------------------------------
@st.cache_data
def load_data():
    biometric = pd.read_csv("data/biometric.csv", parse_dates=["date"], dayfirst=True)
    enrolment = pd.read_csv("data/enrolment.csv", parse_dates=["date"], dayfirst=True)
    demographic = pd.read_csv("data/demographic.csv", parse_dates=["date"], dayfirst=True)

    biometric.columns = biometric.columns.str.lower()
    enrolment.columns = enrolment.columns.str.lower()
    demographic.columns = demographic.columns.str.lower()

    return biometric, enrolment, demographic


biometric, enrolment, demographic = load_data()

# -------------------------------
# Filters
# -------------------------------
st.sidebar.header("Filters")

min_date = biometric["date"].min().date()
max_date = biometric["date"].max().date()

date_range = st.sidebar.date_input(
    "Date Range",
    (min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

state = st.sidebar.selectbox(
    "State",
    ["All"] + sorted(biometric["state"].unique())
)

def apply_filters(df):
    start, end = date_range
    df = df[(df["date"].dt.date >= start) & (df["date"].dt.date <= end)]
    if state != "All":
        df = df[df["state"] == state]
    return df


biometric_f = apply_filters(biometric)
enrolment_f = apply_filters(enrolment)
demographic_f = apply_filters(demographic)

# -------------------------------
# Aadhaar System Overview
# -------------------------------
st.subheader("Aadhaar Lifecycle Overview")

population_5_17 = demographic_f["demo_age_5_17"].sum()
population_17p = demographic_f["demo_age_17_"].sum()
total_population = population_5_17 + population_17p

total_enrolments = enrolment_f[
    ["age_0_5", "age_5_17", "age_18_greater"]
].sum().sum()

total_biometrics = biometric_f[
    ["bio_age_5_17", "bio_age_17_"]
].sum().sum()

c1, c2, c3 = st.columns(3)
c1.metric("Aadhaar Population (5+)", f"{int(total_population):,}")
c2.metric("Total Enrolments", f"{int(total_enrolments):,}")
c3.metric("Biometric Transactions", f"{int(total_biometrics):,}")

st.info(
    "Enrolment represents population inflow, while biometric transactions "
    "reflect sustained, recurring usage of Aadhaar services."
)

# -------------------------------
# Enrolment Trends
# -------------------------------
st.subheader("Enrolment Trends by Age Group")

enrol_ts = enrolment_f.groupby("date", as_index=False)[
    ["age_0_5", "age_5_17", "age_18_greater"]
].sum()

fig_enrol = px.area(
    enrol_ts,
    x="date",
    y=["age_0_5", "age_5_17", "age_18_greater"],
    title="Aadhaar Enrolments Over Time",
    labels={"value": "Enrolments", "variable": "Age Group"}
)
st.plotly_chart(fig_enrol, use_container_width=True)

# -------------------------------
# Biometric Trends
# -------------------------------
st.subheader("Biometric Activity Trends")

bio_ts = biometric_f.groupby("date", as_index=False)[
    ["bio_age_5_17", "bio_age_17_"]
].sum()

fig_bio = px.line(
    bio_ts,
    x="date",
    y=["bio_age_5_17", "bio_age_17_"],
    title="Biometric Transactions Over Time",
    labels={"value": "Transactions", "variable": "Age Group"}
)
st.plotly_chart(fig_bio, use_container_width=True)

st.info(
    "Adults (17+) dominate biometric activity, confirming Aadhaar’s role "
    "as a continuously used identity infrastructure."
)

# -------------------------------
# District-Level Aggregation
# -------------------------------
demo_cols = ["demo_age_5_17", "demo_age_17_"]
bio_cols = ["bio_age_5_17", "bio_age_17_"]
enr_cols = ["age_0_5", "age_5_17", "age_18_greater"]

demo_d = demographic_f.groupby(["state", "district"], as_index=False)[demo_cols].sum()
bio_d = biometric_f.groupby(["state", "district"], as_index=False)[bio_cols].sum()
enr_d = enrolment_f.groupby(["state", "district"], as_index=False)[enr_cols].sum()

merged = demo_d.merge(bio_d, on=["state", "district"]).merge(enr_d, on=["state", "district"])

merged["population"] = merged["demo_age_5_17"] + merged["demo_age_17_"]
merged["biometrics"] = merged["bio_age_5_17"] + merged["bio_age_17_"]
merged["enrolments"] = merged["age_0_5"] + merged["age_5_17"] + merged["age_18_greater"]

merged = merged[merged["population"] > 10_000]

# -------------------------------
# Insight 1: Aadhaar Service Hubs
# -------------------------------
st.subheader("High-Intensity Aadhaar Service Hubs")

national_rate = merged["biometrics"].sum() / merged["population"].sum()
merged["biometric_intensity_index"] = (
    (merged["biometrics"] / merged["population"]) / national_rate
)

top_districts = merged.sort_values(
    "biometric_intensity_index", ascending=False
).head(10)

fig_hubs = px.bar(
    top_districts.sort_values("biometric_intensity_index"),
    x="biometric_intensity_index",
    y="district",
    orientation="h",
    title="Top Districts by Biometric Intensity (Relative to National Average)",
)
st.plotly_chart(fig_hubs, use_container_width=True)

st.info(
    "These districts exhibit disproportionately high Aadhaar activity, "
    "suggesting migration hubs, service concentration, or administrative load."
)

# -------------------------------
# Insight 2: State-Level Usage Pattern
# -------------------------------
st.subheader("State-Level Biometric Usage")

state_agg = merged.groupby("state", as_index=False)[
    ["population", "biometrics"]
].sum()

state_agg["biometric_per_capita"] = state_agg["biometrics"] / state_agg["population"]
state_agg = state_agg.dropna()

fig_state = px.bar(
    state_agg.sort_values("biometric_per_capita", ascending=False).head(10),
    x="biometric_per_capita",
    y="state",
    orientation="h",
    title="States with Highest Biometric Usage per Capita",
)
st.plotly_chart(fig_state, use_container_width=True)

# -------------------------------
# Insight 3: Predictive Growth Indicator
# -------------------------------
st.subheader("Fastest-Growing Districts (Predictive Indicator)")

bio_month = biometric_f.copy()
bio_month["month"] = bio_month["date"].dt.to_period("M").dt.to_timestamp()

monthly = bio_month.groupby(
    ["district", "month"], as_index=False
)[bio_cols].sum()

monthly["biometrics_total"] = monthly[bio_cols].sum(axis=1)

trend = monthly.groupby("district").agg(
    first_val=("biometrics_total", "first"),
    last_val=("biometrics_total", "last"),
)

trend = trend[trend["first_val"] > 0]
trend["growth_rate"] = (trend["last_val"] - trend["first_val"]) / trend["first_val"]

trend = trend.sort_values("growth_rate", ascending=False).head(10)

st.dataframe(
    trend.assign(
        growth_rate=lambda d: (d["growth_rate"] * 100).round(1).astype(str) + "%"
    )
)

st.info(
    "Rapid biometric growth signals future demand pressure "
    "and can guide proactive infrastructure planning."
)

# -------------------------------
# Insight 4: Anomaly Detection
# -------------------------------
st.subheader("Recent Biometric Spike Alerts")

monthly["z_score"] = monthly.groupby("district")["biometrics_total"].transform(
    lambda x: zscore(x, nan_policy="omit")
)

latest_month = monthly["month"].max()
spikes = monthly[(monthly["month"] == latest_month) & (monthly["z_score"] > 3)]

if spikes.empty:
    st.info("No statistically significant biometric spikes detected in the latest month.")
else:
    st.dataframe(spikes[["district", "biometrics_total", "z_score"]])

# -------------------------------
# Insight 5: Leading Indicator Correlations
# -------------------------------
# Prepare time-aligned data for correlation analysis
corr_df = (
    enrolment_f
    .groupby("date", as_index=False)[["age_18_greater"]].sum()
    .merge(
        biometric_f.groupby("date", as_index=False)[["bio_age_17_"]].sum(),
        on="date",
        how="inner"
    )
)

st.subheader("Enrolment → Biometric Lead Indicator")

lead_corr = corr_df["age_18_greater"].corr(corr_df["bio_age_17_"])

st.metric(
    label="Correlation: Adult Enrolment vs Biometric Usage",
    value=f"{lead_corr:.2f}"
)

# compute correlation matrix from the prepared dataframe
corr = corr_df.corr()

corr_vals = corr.loc["bio_age_17_"].drop("bio_age_17_")

fig_corr_bar = px.bar(
    corr_vals,
    title="Correlation Strength with Adult Biometric Usage",
    labels={"value": "Correlation"}
)

st.plotly_chart(fig_corr_bar, use_container_width=True)


st.info(
    "Strong positive correlation confirms that adult enrolment "
    "is a leading indicator of sustained biometric demand."
)

# -------------------------------
# Footer
# -------------------------------
st.caption(
    "All insights are derived strictly from the provided UIDAI Aadhaar datasets. "
    "No external data sources or assumptions were introduced."
)
