
# Experiment 2 — Docker Containerization

## Project
HEATWATCH AI — Heatwave Intelligence Center

## Objective
Package the Streamlit dashboard and its Python dependencies into a Docker image and run it in an isolated container.

## Image
heatwave-intelligence:1.0

## Container
heatwave-dashboard

## Port mapping
8501:8501

## Commands executed
- docker build -t heatwave-intelligence:1.0 .
- docker run -d --name heatwave-dashboard -p 8501:8501 heatwave-intelligence:1.0
- docker ps
- docker logs heatwave-dashboard

## Verification
The Docker image was built, and the container was started.
The dashboard and final container health status must be verified and recorded.

## Evidence
Save screenshots of:
1. Successful Docker image build
2. Running container using docker ps
3. Dashboard opened through http://localhost:8501
4. Container health status

## Limitations
The application uses synthetic demonstration weather data and a simple persistence baseline. It is not an official forecasting or warning service.
