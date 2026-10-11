# Experiment 6: CloudAnalyst Performance Simulation

## Objective
To evaluate application performance under normal and high user loads using CloudAnalyst.

## Tool Used
CloudAnalyst — cloud application performance simulation tool.

## Simulation Configurations

| Parameter | Baseline | High Load |
|---|---:|---:|
| Simulation duration | 60 minutes | 60 minutes |
| Requests per user per hour | 60 | 60 |
| Data size per request | 100 bytes | 100 bytes |
| Average peak users | 2,000 | 4,000 |
| Average off-peak users | 200 | 400 |
| Number of VMs | 5 | 5 |

## Results

| Metric | Baseline | High Load |
|---|---:|---:|
| Average overall response time | 300.056 ms | 300.391 ms |
| Minimum overall response time | 237.059 ms | 232.670 ms |
| Maximum overall response time | 369.115 ms | 373.649 ms |
| Average data-center processing time | 0.342 ms | 0.364 ms |

## Observation
The high-load simulation increased the average overall response time from 300.056 ms to 300.391 ms, a difference of approximately 0.335 ms. Average data-center processing time increased from 0.342 ms to 0.364 ms.

The simulated results show only a small change in response time under the tested conditions. These results are from CloudAnalyst simulations and are not measurements of live application traffic.

## Evidence Files
- `baseline results.pdf` — baseline simulation results.
- `highload simulation.pdf` — high-load simulation results.
- `Baseline Simulation.png` — baseline simulation screenshot.

## Conclusion
CloudAnalyst was used to compare a baseline workload with a higher user workload while keeping the number of VMs and other listed parameters unchanged. The observed response-time difference was small under the selected simulation settings.