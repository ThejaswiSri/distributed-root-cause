
# Distributed Service Health Monitor

## Overview

A Python-based distributed systems simulation project that monitors service health, tracks response latency, simulates service failures, and identifies potential root causes through dependency-aware analysis.

The project includes an interactive Streamlit dashboard with failure injection, dependency failure propagation, persistent incident history, latency monitoring, and rule-based service failure risk estimation.

## Features

- Monitor the health of multiple distributed services.
- Simulate service response times and failures.
- Detect unhealthy services using latency thresholds.
- Model dependencies between distributed services.
- Simulate direct and indirect dependency failure propagation.
- Inject controlled failures into individual services.
- Recover services after simulated failures.
- Identify potential root causes using dependency-aware analysis.
- Display service health metrics and latency through a live Streamlit dashboard.
- Automatically refresh monitoring results every 3 seconds.
- Display healthy, unhealthy, and affected service counts.
- Maintain persistent incident history using JSON storage.
- Track recent latency measurements for each service.
- Estimate service failure risk using recent latency measurements.
- Classify service risk as Low, Medium, or High.
- Include automated tests using Pytest.

## Technologies Used

- Python 3.11
- Streamlit
- Pandas
- Pytest
- Git
- GitHub

## Project Structure

```text
distributed-root-cause/
│
├── main.py
├── dashboard.py
├── test_main.py
├── incident_history.json
├── README.md
└── .gitignore
```

Note: `incident_history.json` is generated automatically when incidents are recorded.

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/ThejaswiSri/distributed-root-cause.git
cd distributed-root-cause
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
python -m pip install streamlit pandas pytest
```

### 5. Run the dashboard

```bash
python -m streamlit run dashboard.py
```

Open the local URL displayed in your terminal to access the dashboard.

## Running Automated Tests

Run the following command from the project directory:

```bash
python -m pytest -v
```

The automated tests cover:

- Normal service health.
- Database failure detection.
- High latency during a simulated database failure.
- Direct and indirect dependency failure propagation.
- Recovery to normal service health.
- Handling of invalid service names.

## Failure Risk Estimation

The project uses a rule-based approach to estimate service failure risk from recent latency measurements.

- **Low Risk:** Average latency below 250 ms.
- **Medium Risk:** Average latency from 250 ms to below 350 ms.
- **High Risk:** Average latency of 350 ms or above.
- At least three measurements are required before a risk estimate is available.

The latest five measurements are used when available.

This is a heuristic-based risk estimator, not a trained machine-learning model.

## Incident History

Incident events are stored in `incident_history.json` so that failure and recovery records remain available after restarting the dashboard.

The dashboard records:
- Failure injection events.
- Service recovery events.
- Event timestamps.
- The affected service.

## Project Status

**Working prototype — Version 1.0 preparation.**

The project currently provides simulated distributed service monitoring, dependency-aware failure propagation, root-cause analysis, persistent incident recording, and latency-based risk estimation.

Service health and latency are simulated using Python. The risk estimator uses recent simulated latency measurements rather than real production telemetry.

## Future Improvements

- Integrate real service health endpoints.
- Improve latency trend analysis.
- Explore machine-learning-based failure prediction.
- Expand root-cause analysis.
- Add more comprehensive monitoring and reporting.

## Author

Thejaswi
