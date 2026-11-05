import pandas as pd
import streamlit as st
from datetime import datetime

from main import check_service_health, analyze_root_causes

st.set_page_config(
    page_title="Distributed Service Monitor",
    page_icon="🖥️",
    layout="wide",
)

st.title("🖥️ Distributed Service Health Monitor")
st.caption("Live monitoring using the main.py health-check function")


@st.fragment(run_every=3)
def show_dashboard():

    # Get monitoring data from main.py
    records = check_service_health()

    # Convert results into a DataFrame
    df = pd.DataFrame(records)

    healthy = (df["Status"] == "Healthy").sum()
    unhealthy = (df["Status"] == "Unhealthy").sum()
    average_latency = round(df["Latency (ms)"].mean(), 2)

    st.caption(
        f"Last updated: {datetime.now().strftime('%H:%M:%S')}"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Services", len(df))
    col2.metric("Healthy Services", healthy)
    col3.metric("Unhealthy Services", unhealthy)

    st.subheader("Service Health")

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
    )

    st.subheader("Service Latency")

    st.bar_chart(
        df.set_index("Service")["Latency (ms)"]
    )

    st.metric("Average Latency", f"{average_latency} ms")

    st.subheader("Root Cause Analysis")

    findings = analyze_root_causes(records)

    if findings:
        for finding in findings:
            st.warning(finding)
    else:
        st.success("All services are operating normally.")


show_dashboard()