
import pandas as pd
import streamlit as st
import json
import os
from datetime import datetime

from main import (
    check_service_health,
    analyze_root_causes,
    predict_service_risk,
)

# Persistent incident storage
INCIDENT_FILE = "incident_history.json"


def load_incidents():
    """Load incident history from the JSON file."""
    if os.path.exists(INCIDENT_FILE):
        try:
            with open(INCIDENT_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, OSError):
            return []

    return []


def save_incidents(incidents):
    """Save incident history to the JSON file."""
    with open(INCIDENT_FILE, "w", encoding="utf-8") as file:
        json.dump(incidents, file, indent=4)


st.set_page_config(
    page_title="Distributed Service Monitor",
    page_icon="🖥️",
    layout="wide",
)

st.title("🖥️ Distributed Service Health Monitor")
st.caption("Live monitoring using the main.py health-check function")


# Initialize incident history from persistent storage
if "incident_history" not in st.session_state:
    st.session_state["incident_history"] = load_incidents()


# Initialize latency history
if "latency_history" not in st.session_state:
    st.session_state["latency_history"] = {
        service: [] for service in [
            "Database Service",
            "Authentication Service",
            "Payment Service",
            "API Gateway",
            "Notification Service",
        ]
    }


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

        incident = {
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Service": selected_service,
            "Event": "Failure Injected",
        }

        st.session_state["incident_history"].append(incident)
        save_incidents(st.session_state["incident_history"])

        st.success(f"Failure injected into {selected_service}!")


if st.button("Recover All Services"):
    previous_failure = st.session_state.get("failed_service")

    if previous_failure is not None:
        incident = {
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Service": previous_failure,
            "Event": "Service Recovered",
        }

        st.session_state["incident_history"].append(incident)
        save_incidents(st.session_state["incident_history"])

    st.session_state["failed_service"] = None
    st.success("All services recovered!")


@st.fragment(run_every=3)
def show_dashboard():

    # Get monitoring data from main.py
    failed_service = st.session_state.get("failed_service", None)
    records = check_service_health(failed_service)

    # Convert results into a DataFrame
    df = pd.DataFrame(records)

    # Store recent latency measurements for each service
    for record in records:
        service = record["Service"]
        latency = record["Latency (ms)"]

        st.session_state["latency_history"][service].append(latency)

        # Keep only the latest 10 measurements
        st.session_state["latency_history"][service] = (
            st.session_state["latency_history"][service][-10:]
        )

    # Calculate service metrics
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
        width="stretch",
        hide_index=True,
    )

    st.subheader("Service Latency")

    st.bar_chart(
        df.set_index("Service")["Latency (ms)"]
    )

    st.metric("Average Latency", f"{average_latency} ms")

    st.subheader("Root Cause Analysis")

    findings = analyze_root_causes(records)

    if findings == ["All services are operating normally."]:
        st.success("All services are operating normally.")
    else:
        for finding in findings:
            st.warning(finding)

    st.subheader("Service Status Summary")

    for record in records:
        if record["Status"] == "Unhealthy":
            st.error(f"🔴 {record['Service']}: Unhealthy")

        elif record["Status"] == "Affected":
            st.warning(
                f"🟠 {record['Service']}: Affected by dependency failure"
            )

        else:
            st.success(f"🟢 {record['Service']}: Healthy")

    # Service failure risk prediction
    st.subheader("Service Failure Risk Prediction")

    for service, history in st.session_state["latency_history"].items():
        risk = predict_service_risk(history)

        if risk == "High Risk":
            st.error(f"🔴 {service}: {risk}")

        elif risk == "Medium Risk":
            st.warning(f"🟠 {service}: {risk}")

        elif risk == "Low Risk":
            st.success(f"🟢 {service}: {risk}")

        else:
            st.info(f"ℹ️ {service}: {risk}")

    # Incident History
    st.subheader("Incident History")

    if st.session_state["incident_history"]:
        history_df = pd.DataFrame(
            st.session_state["incident_history"]
        )

        st.dataframe(
            history_df,
            width="stretch",
            hide_index=True,
        )

    else:
        st.info("No incidents recorded yet.")

    st.subheader("Service Dependency Map")

    dependency_graph = """
    digraph {
        "API Gateway" -> "Authentication Service"
        "API Gateway" -> "Payment Service"
        "Authentication Service" -> "Database Service"
        "Payment Service" -> "Database Service"
        "Notification Service" -> "Database Service"
    }
    """

    st.graphviz_chart(dependency_graph, width="stretch")


show_dashboard()
