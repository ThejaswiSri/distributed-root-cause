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
st.subheader("Failure Injection")

selected_service = st.selectbox(
    "Select a service to simulate failure",
    [
        "None",
        "Database Service",
        "Authentication Service",
        "Payment Service",
        "API Gateway",
        "Notification Service",
    ],
)

if st.button("Inject Failure"):
    if selected_service == "None":
        st.warning("Please select a service first.")
    else:
        st.session_state["failed_service"] = selected_service
        st.success(f"Failure injected into {selected_service}!")

if st.button("Recover All Services"):
    st.session_state["failed_service"] = None
    st.success("All services recovered!")


@st.fragment(run_every=3)
def show_dashboard():

    # Get monitoring data from main.py
    failed_service = st.session_state.get("failed_service", None)
    records = check_service_health(failed_service)

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