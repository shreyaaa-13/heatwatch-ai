
import pandas as pd
import streamlit as st
import plotly.express as px

from data_processor import load_weather_data, validate_weather_data
from predictor import classify_heat_risk, forecast_next_day_baseline
from advisory import make_advisory


# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="HEATWATCH AI | Heatwave Intelligence",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

RISK_COLORS = {
    "Low": "#21D4B4",
    "Moderate": "#F3D65B",
    "High": "#FF9E43",
    "Extreme": "#FF5263",
}

AUDIENCES = {
    "Citizens": (
        "Limit strenuous outdoor activity during peak heat, drink water "
        "regularly, seek shade or a cool indoor space, and check on "
        "children and older adults."
    ),
    "Farmers": (
        "Where practical, schedule strenuous field work during cooler "
        "hours, take shaded breaks, drink water, and monitor crops "
        "and livestock for heat stress."
    ),
    "Health teams": (
        "Review heat-related illness preparedness, hydration access, "
        "cooling arrangements, and guidance for vulnerable patients."
    ),
    "Local authorities": (
        "Review local heat action plans, drinking-water access, cooling "
        "spaces, and communication arrangements for vulnerable communities."
    ),
}


# =========================================================
# CUSTOM DARK THEME
# =========================================================
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(145deg, #071521, #0b1724);
        color: #e6f2ff;
    }

    [data-testid="stSidebar"] {
        background: #101e2d;
        border-right: 1px solid #24485c;
    }

    h1, h2, h3 {
        color: #e9f7ff !important;
    }

    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #11283a, #0d1c2a);
        border: 1px solid #24485c;
        padding: 16px;
        border-radius: 14px;
    }

    [data-testid="stMetricValue"] {
        color: #43e5d3;
    }

    .hero {
        background: linear-gradient(110deg, #102d40, #0c1b29);
        border: 1px solid #28536a;
        border-radius: 18px;
        padding: 24px;
        margin-bottom: 18px;
    }

    .hero-label {
        color: #43e5d3;
        font-weight: 700;
        letter-spacing: 2px;
    }

    .small-note {
        color: #9bb4c7;
        font-size: 12px;
    }

    div[data-testid="stPlotlyChart"] {
        background: #0d1b29;
        border: 1px solid #203e52;
        border-radius: 14px;
        padding: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# LOAD AND VALIDATE DATA
# =========================================================
st.sidebar.markdown("## 🌡️ HEATWATCH AI")
st.sidebar.caption("Climate intelligence prototype")
st.sidebar.divider()

try:
    df = load_weather_data("data/weather_data.csv")

    validation_errors = validate_weather_data(df)

    if validation_errors:
        st.error(
            "Dataset validation failed:\n\n- "
            + "\n- ".join(validation_errors)
        )
        st.stop()

except Exception as exc:
    st.error(f"Unable to load the weather dataset: {exc}")
    st.stop()


# Normalize data types and remove unusable rows.
df["date"] = pd.to_datetime(df["date"], errors="coerce")

for column in [
    "latitude",
    "longitude",
    "max_temperature_c",
]:
    df[column] = pd.to_numeric(df[column], errors="coerce")

df = df.dropna(
    subset=[
        "date",
        "region",
        "latitude",
        "longitude",
        "max_temperature_c",
    ]
).copy()

if df.empty:
    st.error("No valid weather observations are available.")
    st.stop()

if "humidity_percent" not in df.columns:
    df["humidity_percent"] = None

df["risk"] = df["max_temperature_c"].apply(classify_heat_risk)


# =========================================================
# SIDEBAR FILTERS
# =========================================================
st.sidebar.subheader("Region & Filters")

all_regions = sorted(df["region"].astype(str).unique().tolist())

selected_region = st.sidebar.selectbox(
    "Choose region",
    ["All regions"] + all_regions,
)

minimum_date = df["date"].min().date()
maximum_date = df["date"].max().date()

selected_dates = st.sidebar.date_input(
    "Analysis date range",
    value=(minimum_date, maximum_date),
    min_value=minimum_date,
    max_value=maximum_date,
)

filtered = df.copy()

if selected_region != "All regions":
    filtered = filtered[
        filtered["region"] == selected_region
    ]

if isinstance(selected_dates, (tuple, list)):
    if len(selected_dates) == 2:
        start_date, end_date = selected_dates

        filtered = filtered[
            filtered["date"].dt.date.between(
                start_date,
                end_date,
            )
        ]
    elif len(selected_dates) == 1:
        filtered = filtered[
            filtered["date"].dt.date == selected_dates[0]
        ]

if filtered.empty:
    st.warning(
        "No data matches the selected filters. "
        "Choose another region or date range."
    )
    st.stop()


# Latest observation for each region, not just the latest
# date shared by all regions.
latest = (
    filtered.sort_values("date")
    .groupby("region", as_index=False)
    .tail(1)
    .copy()
)

latest["risk"] = latest["max_temperature_c"].apply(
    classify_heat_risk
)

latest = latest.sort_values(
    "max_temperature_c",
    ascending=False,
)

latest_date = filtered["date"].max()


# =========================================================
# HEADER
# =========================================================
st.markdown(
    """
    <div class="hero">
        <div class="hero-label">
            CLIMATE • ANALYTICS • EARLY WARNING
        </div>
        <h1 style="margin: 10px 0;">
            Heatwave Intelligence Center
        </h1>
        <p>
            Monitor regional temperatures, identify potential hotspots,
            and prepare heat-safety advisories.
        </p>
        <p class="small-note">
            Educational prototype · Synthetic data ·
            Not an official IMD forecast or warning
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption(
    f"Latest observation in selected data: {latest_date:%d %b %Y}"
)


# =========================================================
# SUMMARY METRICS
# =========================================================
high_risk_count = int(
    latest["risk"].isin(["High", "Extreme"]).sum()
)

peak = latest.iloc[0]

metric1, metric2, metric3, metric4 = st.columns(4)

metric1.metric(
    "Regions monitored",
    latest["region"].nunique(),
)

metric2.metric(
    "Peak temperature",
    f"{peak['max_temperature_c']:.1f} °C",
    help=f"Highest available reading: {peak['region']}",
)

metric3.metric(
    "High-risk hotspots",
    high_risk_count,
)

metric4.metric(
    "Observations analysed",
    len(filtered),
)


# =========================================================
# DASHBOARD TABS
# =========================================================
overview_tab, analytics_tab, forecast_tab, advisory_tab, data_tab = (
    st.tabs(
        [
            "🌍 Overview",
            "📊 Analytics",
            "📈 Forecast",
            "🔔 Advisories",
            "🗃️ Data & Validation",
        ]
    )
)


# =========================================================
# OVERVIEW: MAP, HOTSPOTS AND RISK DISTRIBUTION
# =========================================================
with overview_tab:
    left, right = st.columns([1.15, 1])

    with left:
        st.subheader("Regional Heat-Risk Map")
        st.caption(
            "Points show the coordinates supplied in the dataset."
        )

        map_df = latest.dropna(
            subset=[
                "latitude",
                "longitude",
                "max_temperature_c",
            ]
        ).copy()

        if not map_df.empty:
            fig_map = px.scatter(
                map_df,
                x="longitude",
                y="latitude",
                color="risk",
                size="max_temperature_c",
                hover_name="region",
                hover_data={
                    "max_temperature_c": ":.1f",
                    "humidity_percent": True,
                    "latitude": ":.3f",
                    "longitude": ":.3f",
                },
                color_discrete_map=RISK_COLORS,
                size_max=32,
                labels={
                    "longitude": "Longitude",
                    "latitude": "Latitude",
                    "risk": "Prototype risk level",
                    "max_temperature_c": "Temperature (°C)",
                    "humidity_percent": "Humidity (%)",
                },
            )

            fig_map.update_layout(
                height=400,
                paper_bgcolor="#0d1b29",
                plot_bgcolor="#0d1b29",
                font_color="#e6f2ff",
                margin=dict(l=15, r=15, t=20, b=15),
                legend_title_text="Heat risk",
            )

            fig_map.update_xaxes(
                range=[70, 82],
                title="Longitude",
                gridcolor="#244052",
                zeroline=False,
            )

            fig_map.update_yaxes(
                range=[14, 25],
                title="Latitude",
                gridcolor="#244052",
                zeroline=False,
                scaleanchor="x",
                scaleratio=1,
            )

            st.plotly_chart(
                fig_map,
                use_container_width=True,
            )

        else:
            st.info(
                "No valid coordinates are available for mapping."
            )

    with right:
        st.subheader("Hotspot Ranking")
        st.caption(
            "Regions ranked by their latest available temperatures."
        )

        ranking = latest[
            ["region", "max_temperature_c", "risk"]
        ].copy()

        ranking.insert(
            0,
            "Rank",
            range(1, len(ranking) + 1),
        )

        ranking = ranking.rename(
            columns={
                "region": "Region",
                "max_temperature_c": "Temperature (°C)",
                "risk": "Prototype risk",
            }
        )

        st.dataframe(
            ranking,
            use_container_width=True,
            hide_index=True,
        )

        st.subheader("Risk Distribution")

        risk_counts = (
            latest["risk"]
            .value_counts()
            .reindex(
                ["Low", "Moderate", "High", "Extreme"],
                fill_value=0,
            )
            .rename_axis("Risk level")
            .reset_index(name="Regions")
        )

        fig_risk = px.bar(
            risk_counts,
            x="Risk level",
            y="Regions",
            color="Risk level",
            color_discrete_map=RISK_COLORS,
        )

        fig_risk.update_layout(
            height=260,
            paper_bgcolor="#0d1b29",
            plot_bgcolor="#0d1b29",
            font_color="#e6f2ff",
            margin=dict(l=10, r=10, t=15, b=10),
            showlegend=False,
        )

        st.plotly_chart(
            fig_risk,
            use_container_width=True,
        )


# =========================================================
# ANALYTICS: TEMPERATURE TRENDS AND SUMMARY
# =========================================================
with analytics_tab:
    st.subheader("Regional Temperature Analytics")

    daily = (
        filtered.assign(
            observation_date=filtered["date"].dt.date
        )
        .groupby(
            ["observation_date", "region"],
            as_index=False,
        )["max_temperature_c"]
        .mean()
    )

    fig_trend = px.line(
        daily,
        x="observation_date",
        y="max_temperature_c",
        color="region",
        markers=True,
        labels={
            "observation_date": "Date",
            "max_temperature_c": "Maximum temperature (°C)",
            "region": "Region",
        },
    )

    fig_trend.update_layout(
        paper_bgcolor="#0d1b29",
        plot_bgcolor="#0d1b29",
        font_color="#e6f2ff",
    )

    st.plotly_chart(
        fig_trend,
        use_container_width=True,
    )

    st.subheader("Regional Summary")

    summary = (
        filtered.groupby("region")["max_temperature_c"]
        .agg(
            Average="mean",
            Minimum="min",
            Maximum="max",
        )
        .round(2)
    )

    st.dataframe(
        summary,
        use_container_width=True,
    )


# =========================================================
# FORECAST: TRANSPARENT PERSISTENCE BASELINE
# =========================================================
with forecast_tab:
    st.subheader("Next-Day Temperature Baseline")

    st.warning(
        "This is an educational persistence baseline, not a trained "
        "AI model or official IMD forecast. Each estimate equals the "
        "latest available observation for that region."
    )

    forecast_rows = []

    for region in sorted(filtered["region"].unique()):
        region_data = filtered[
            filtered["region"] == region
        ].sort_values("date")

        estimate = forecast_next_day_baseline(region_data)

        forecast_rows.append(
            {
                "Region": region,
                "Latest observed (°C)": float(
                    region_data.iloc[-1]["max_temperature_c"]
                ),
                "Baseline estimate (°C)": estimate,
                "Prototype risk": classify_heat_risk(estimate),
            }
        )

    forecast_df = pd.DataFrame(forecast_rows)

    st.dataframe(
        forecast_df,
        use_container_width=True,
        hide_index=True,
    )

    fig_forecast = px.bar(
        forecast_df,
        x="Region",
        y="Baseline estimate (°C)",
        color="Prototype risk",
        color_discrete_map=RISK_COLORS,
    )

    fig_forecast.update_layout(
        paper_bgcolor="#0d1b29",
        plot_bgcolor="#0d1b29",
        font_color="#e6f2ff",
    )

    st.plotly_chart(
        fig_forecast,
        use_container_width=True,
    )


# =========================================================
# ADVISORIES: STAKEHOLDER-SPECIFIC MESSAGES
# =========================================================
with advisory_tab:
    st.subheader("Stakeholder Advisory Composer")

    audience = st.selectbox(
        "Choose intended audience",
        list(AUDIENCES.keys()),
    )

    advisory_region = st.selectbox(
        "Choose advisory region",
        sorted(latest["region"].unique()),
    )

    selected_row = latest[
        latest["region"] == advisory_region
    ].iloc[0]

    temperature = float(
        selected_row["max_temperature_c"]
    )

    risk = str(selected_row["risk"])

    st.markdown(
        f"### {advisory_region} · {risk} prototype risk"
    )

    st.write(
        make_advisory(
            advisory_region,
            temperature,
            risk,
        )
    )

    st.info(AUDIENCES[audience])

    st.caption(
        "Educational guidance only. Follow official local authority "
        "advice during actual heat events."
    )


# =========================================================
# DATA: VALIDATION, UPLOAD AND DOWNLOAD
# =========================================================
with data_tab:
    st.subheader("Data Quality & Validation")

    data_col1, data_col2, data_col3 = st.columns(3)

    data_col1.metric(
        "Rows analysed",
        len(filtered),
    )

    data_col2.metric(
        "Regions represented",
        filtered["region"].nunique(),
    )

    data_col3.metric(
        "Missing temperatures",
        int(filtered["max_temperature_c"].isna().sum()),
    )

    st.write("**Dataset columns**")
    st.code(", ".join(df.columns.astype(str)))

    st.write("**Weather data preview**")

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True,
    )

    st.download_button(
        "Download filtered weather data",
        data=filtered.to_csv(index=False),
        file_name="heatwave_observations.csv",
        mime="text/csv",
    )

    st.divider()

    st.subheader("Test an external CSV")

    st.write(
        "Required columns: date, region, latitude, longitude, "
        "max_temperature_c. Humidity is optional."
    )

    uploaded_file = st.file_uploader(
        "Upload a CSV file",
        type=["csv"],
        key="external_weather_csv",
    )

    if uploaded_file is not None:
        try:
            uploaded_df = pd.read_csv(uploaded_file)

            upload_errors = validate_weather_data(uploaded_df)

            if upload_errors:
                st.error(
                    "Validation failed:\n\n- "
                    + "\n- ".join(upload_errors)
                )
            else:
                st.success(
                    f"Validation passed for {len(uploaded_df)} rows."
                )

                st.dataframe(
                    uploaded_df.head(20),
                    use_container_width=True,
                    hide_index=True,
                )

        except Exception as exc:
            st.error(
                f"Unable to read the uploaded CSV: {exc}"
            )


# =========================================================
# FOOTER
# =========================================================
st.divider()

st.caption(
    "HEATWATCH AI · Student coursework prototype · "
    "Synthetic demonstration data · "
    "Risk thresholds and baseline estimates are illustrative, "
    "not official IMD criteria."
)
