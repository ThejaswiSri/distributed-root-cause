Distributed Service Health Simulator

Overview

A Python-based project that simulates the health of distributed services, monitors service latency, and identifies potential root causes of service failures through dependency-aware analysis.

Features

- Monitor the health of multiple distributed services.
- Simulate service response times and failures.
- Detect unhealthy services based on latency thresholds.
- Model dependencies between services.
- Identify possible root causes using dependency-aware analysis.
- Display service health metrics and latency through a live Streamlit dashboard.
- Automatically refresh monitoring results every 3 seconds.

Technologies Used

- Python 3.11
- Streamlit
- Pandas
- Git
- GitHub

How to Run

1. Clone the repository

git clone https://github.com/ThejaswiSri/distributed-root-cause.git
cd distributed-root-cause

2. Create a virtual environment

python -m venv .venv

3. Activate the virtual environment

Windows PowerShell:

.\.venv\Scripts\Activate.ps1

4. Install dependencies

python -m pip install streamlit pandas

5. Run the dashboard

python -m streamlit run dashboard.py

Open the local URL displayed in your terminal to view the dashboard.

Project Status

Currently under development. Service health and latency are simulated using Python. Root-cause findings are preliminary and based on configured service dependencies.

Author

Thejaswi