# Distributed Service Health Simulator

## Overview

A Python-based distributed systems simulation project that monitors service health, tracks latency, simulates service failures, and identifies potential root causes through dependency-aware analysis.

The project includes a live Streamlit dashboard with failure injection, dependency failure propagation, incident history, and latency-based service failure risk estimation.

## Features

- Monitor the health of multiple distributed services.
- Simulate service response times and failures.
- Detect unhealthy services using latency thresholds.
- Model dependencies between distributed services.
- Simulate direct and indirect dependency failure propagation.
- Inject controlled failures into individual services.
- Recover services after simulated failures.
- Identify possible root causes using dependency-aware analysis.
- Display service health metrics and latency through a live Streamlit dashboard.
- Automatically refresh monitoring results every 3 seconds.
- Maintain an incident history of failure and recovery events during the dashboard session.
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
├── README.md
└── .gitignore
```

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

Open the local URL displayed in your terminal to view the dashboard.

## Running Automated Tests

Run the following command from the project directory:

```bash
python -m pytest -v
```

The tests verify service health, database failure detection, dependency failure propagation, and normal service health after recovery.

## Failure Risk Estimation

The project uses a rule-based approach to estimate service failure risk from recent latency measurements.

- **Low Risk:** Average latency below 250 ms.
- **Medium Risk:** Average latency from 250 ms to below 350 ms.
- **High Risk:** Average latency of 350 ms or above.
- At least three measurements are required before a risk estimate is available.

The latest five measurements are used when available. This is a heuristic-based risk estimator, not a trained machine-learning model.

## Project Status

Currently under development.

Service health and latency are simulated using Python. Dependency propagation is based on configured service relationships. Risk estimation uses recent simulated latency measurements.

Incident history and latency history are maintained in Streamlit session state and are not permanently stored across application restarts.

## Future Improvements

- Introduce historical data storage.
- Improve latency trend analysis.
- Explore machine-learning-based failure prediction.
- Add more comprehensive root-cause analysis.
- Improve dashboard visualizations and reporting.

## Author

Thejaswi