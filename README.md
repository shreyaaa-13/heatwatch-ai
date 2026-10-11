# HEATWATCH AI — Heatwave Intelligence Center

**A cloud-native heatwave monitoring dashboard demonstrating containerization, orchestration, performance simulation, and resource optimization.**

## Overview

HEATWATCH AI is an educational prototype designed to demonstrate how a heatwave-monitoring dashboard can be developed and deployed using cloud computing technologies.

The application uses synthetic weather data to display regional temperature information, heat-risk classifications, hotspot rankings, charts, and advisory messages. The project combines a Python-based dashboard with Docker containerization, Kubernetes deployment, CloudAnalyst simulation, and Kubernetes resource right-sizing.

> **Disclaimer:** This project uses synthetic educational data. It is not an official weather forecasting service and must not be used for real-world heatwave warnings or emergency decisions.

## Objectives

- Develop an interactive heatwave-monitoring dashboard.
- Visualize regional weather data and heat-risk classifications.
- Package the application using Docker.
- Publish the container image to Docker Hub.
- Deploy and manage the application using Kubernetes.
- Compare baseline and high-load scenarios through CloudAnalyst simulations.
- Explore Kubernetes CPU and memory resource right-sizing.

## Features

- **Dashboard:** Summary cards, regional information, charts, and heat-risk visualizations.
- **Regional analysis:** Displays information for Nagpur, Pune, Nashik, and Mumbai.
- **Risk classification:** Presents illustrative heat-risk categories and hotspot rankings.
- **Advisories:** Displays educational advisory messages based on the application's risk logic.
- **Data validation:** Processes and checks the input dataset.
- **Containerization:** Packages the application and dependencies into a Docker image.
- **Orchestration:** Uses Kubernetes Deployments, Pods, Services, and health probes.
- **Performance simulation:** Compares baseline and high-load scenarios in CloudAnalyst.
- **Resource right-sizing:** Demonstrates changes to Kubernetes CPU and memory requests and limits.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Interactive dashboard |
| Pandas | Data processing |
| Plotly | Data visualization |
| Docker | Application containerization |
| Docker Hub | Container image storage |
| Kubernetes | Container orchestration |
| CloudAnalyst | Cloud workload simulation |
| Pytest | Application testing |
| Git and GitHub | Source-code version control |

## Project Structure

```text
Heatwave-CloudProject/
├── app.py
├── data_processor.py
├── predictor.py
├── advisory.py
├── requirements.txt
├── Dockerfile
├── .gitignore
├── data/
│   └── weather_data.csv
├── kubernetes/
│   ├── deployment.yaml
│   └── service.yaml
├── tests/
│   └── test_app.py
└── Results/
    ├── Experiment_3/
    ├── Experiment_6/
    └── Experiment_7/
```

*The structure above illustrates the main project files and evidence folders. Keep only entries that actually exist in your repository.*

## Getting Started

### Prerequisites

Install the following software:

- Python
- Git
- Docker Desktop (for containerization)
- Docker Desktop Kubernetes (for the local Kubernetes experiment)

### 1. Clone the Repository

```bash
git clone https://github.com/shreyaaa-13/heatwatch-ai.git
cd heatwatch-ai
```

### 2. Create a Virtual Environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the Dashboard

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal, typically `http://localhost:8501`.

## Docker Deployment

The Docker image was published to Docker Hub.

**Image:** `atharvbadhe01/heatwave-intelligence:1.0`

Pull the image:

```bash
docker pull atharvbadhe01/heatwave-intelligence:1.0
```

Run the container:

```bash
docker run --name heatwave-dashboard -p 8501:8501 atharvbadhe01/heatwave-intelligence:1.0
```

Open `http://localhost:8501` in your browser.

If the container name is already in use, remove or rename the existing container before running another container with that name.

## Kubernetes Deployment

The project includes Kubernetes configuration files:

- `kubernetes/deployment.yaml`
- `kubernetes/service.yaml`

With Docker Desktop Kubernetes enabled, apply the configuration:

```bash
kubectl apply -f kubernetes/deployment.yaml
kubectl apply -f kubernetes/service.yaml
```

Check the deployment and Pods:

```bash
kubectl get deployments
kubectl get pods
kubectl get services
```

To access the dashboard locally through port forwarding:

```bash
kubectl port-forward service/heatwave-service 8503:8501
```

Open `http://localhost:8503` while the port-forward command is running.

The Service is configured with NodePort `30081`, but direct access through that port was unsuccessful in the tested local environment. Port forwarding was used to verify dashboard access.

## CloudAnalyst Simulation

CloudAnalyst was used to compare two simulated workloads:

- **Baseline scenario:** 2,000 peak users and 200 off-peak users.
- **High-load scenario:** 4,000 peak users and 400 off-peak users.

Recorded average overall response times were 300.06 ms for the baseline scenario and 300.39 ms for the high-load scenario.

These values are **simulation results**, not measurements from the live dashboard or guarantees of real cloud-provider performance.

## Kubernetes Resource Right-Sizing

The deployment's CPU and memory settings were adjusted as follows:

| Resource setting | Initial | Updated |
|---|---:|---:|
| CPU request | 100m | 50m |
| Memory request | 128Mi | 96Mi |
| CPU limit | 500m | 250m |
| Memory limit | 512Mi | 256Mi |

The updated configuration was applied, and the deployment rollout and application replicas were checked. Recorded runtime snapshots showed a slight increase in CPU and memory usage after the change, so an improvement in resource efficiency was not established. Repeated measurements under comparable workloads would be needed for a reliable comparison.

## Testing

The project's test suite was run using Pytest.

```bash
python -m pytest -v
```

The recorded test run completed with **9 tests passing**. Run the command again in your current environment to verify the result.

## Experiments Covered

| Experiment | Description |
|---|---|
| Experiment 2 | Docker containerization and Docker Hub publishing |
| Experiment 3 | Kubernetes deployment and application access |
| Experiment 6 | CloudAnalyst baseline and high-load simulation |
| Experiment 7 | Kubernetes resource right-sizing and verification |

Supporting screenshots and reports can be placed in the `Results/` directory if included in the repository.

## Limitations

- The weather dataset is synthetic and intended for educational demonstration.
- The dashboard does not provide official weather forecasts or warnings.
- CloudAnalyst results are simulation-based.
- Resource-usage observations were snapshots rather than controlled benchmarks.
- The local NodePort access configuration was not verified successfully; port forwarding was used instead.
- Production use would require validated meteorological data, appropriate security controls, monitoring, and further testing.

## Future Scope

- Integrate validated meteorological data sources.
- Evaluate risk classification against real-world datasets.
- Deploy the dashboard to a suitable cloud hosting environment.
- Add monitoring, logging, and alerting.
- Evaluate Kubernetes autoscaling under different workloads.
- Perform controlled performance and resource-utilization benchmarks.

## Repository and Docker Image

- **GitHub:** https://github.com/shreyaaa-13/heatwatch-ai
- **Docker Hub:** https://hub.docker.com/r/atharvbadhe01/heatwave-intelligence

## Author

**Project:** HEATWATCH AI — Heatwave Intelligence Center

**Course:** Cloud Computing

**Institution:** K. J. Somaiya School of Engineering, Somaiya Vidyavihar University

## License

No license has been added to this repository. Contact the repository owner before reusing or redistributing this project's code.
