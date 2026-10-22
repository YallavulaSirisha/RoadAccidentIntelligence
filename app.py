
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Road Accident Intelligence",
    page_icon="🚦",
    layout="wide"
)

ROOT = Path(__file__).resolve().parent
DATA = ROOT

st.title("🚦 Road Accident Intelligence & Risk Analysis")
st.write("Explore accident patterns, risk levels, and road safety data.")

file = DATA / "Accidents_Featured.csv"

if not file.exists():
    st.error("Accidents_Featured.csv not found in the data folder.")
    st.stop()

df = pd.read_csv(file)

st.sidebar.header("Dashboard Filters")

if "Accident_Severity" in df.columns:
    severities = sorted(df["Accident_Severity"].dropna().unique())
    selected = st.sidebar.multiselect(
        "Accident Severity",
        severities,
        default=severities
    )
    df = df[df["Accident_Severity"].isin(selected)]

c1, c2, c3 = st.columns(3)

c1.metric("Accidents", f"{len(df):,}")
c2.metric(
    "Casualties",
    f"{df['Number_of_Casualties'].sum():,.0f}"
    if "Number_of_Casualties" in df.columns else "N/A"
)
c3.metric(
    "Vehicles Involved",
    f"{df['Number_of_Vehicles'].sum():,.0f}"
    if "Number_of_Vehicles" in df.columns else "N/A"
)

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Accidents by Severity")
    if "Accident_Severity" in df.columns:
        counts = df["Accident_Severity"].value_counts().sort_index()
        st.bar_chart(counts)

with right:
    st.subheader("Accidents by Month")
    if "Month_Name" in df.columns:
        months = [
            "January", "February", "March", "April",
            "May", "June", "July", "August",
            "September", "October", "November", "December"
        ]
        monthly = df["Month_Name"].value_counts().reindex(
            months, fill_value=0
        )
        st.bar_chart(monthly)

st.subheader("Accident Data Preview")
st.dataframe(df.head(100), use_container_width=True)

st.caption(
    "This dashboard describes recorded accidents. "
    "It does not establish individual road crash probability."
)

st.divider()

st.subheader("🗺️ Accident Hotspot Map")

map_file = ROOT / "accident_hotspot_map.html"

if map_file.exists():
    with open(map_file, "r", encoding="utf-8") as f:
        map_html = f.read()

    import streamlit.components.v1 as components
    components.html(map_html, height=600, scrolling=True)
else:
    st.warning("Hotspot map not found. Run src/hotspot_map.py first.")
 
st.divider()

st.subheader("⚠️ Accident Risk Analysis")

risk_file = DATA / "Accidents_Risk_Scored.csv"

if risk_file.exists():
    risk_df = pd.read_csv(risk_file)

    risk_counts = risk_df["Risk_Level"].value_counts().reindex(
        ["Low", "Medium", "High", "Very High"],
        fill_value=0
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Low Risk", f"{risk_counts['Low']:,}")
    c2.metric("Medium Risk", f"{risk_counts['Medium']:,}")
    c3.metric("High Risk", f"{risk_counts['High']:,}")
    c4.metric("Very High Risk", f"{risk_counts['Very High']:,}")

    st.bar_chart(risk_counts)
else:
    st.warning("Run src/risk_score.py to generate the risk data.")
    
st.sidebar.divider()
st.sidebar.subheader("About This Project")
st.sidebar.write(
    "Road Accident Intelligence & Risk Analysis System"
)
st.sidebar.caption("Academic AI & Data Science Project")

st.download_button(
    label="📥 Download Filtered Accident Data",
    data=df.to_csv(index=False).encode("utf-8"),
    file_name="filtered_accident_data.csv",
    mime="text/csv"
)

   


