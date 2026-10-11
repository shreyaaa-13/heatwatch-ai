# Experiment 7: Cloud Resource Optimization

## Objective
To inspect resource utilization and evaluate the effect of reducing CPU and memory requests and limits for the HEATWATCH AI application deployed on Kubernetes.

## Environment
- Application: HEATWATCH AI
- Containerization: Docker
- Orchestration: Kubernetes on Docker Desktop
- Monitoring command: `docker stats --no-stream`
- Kubernetes deployment: `heatwave-deployment`

## Baseline Configuration
| Resource | Request | Limit |
|---|---:|---:|
| CPU | 100m | 500m |
| Memory | 128Mi | 512Mi |

Baseline container usage observed:
- CPU: 0.55%
- Memory: 128.2 MiB

## Optimized Configuration
| Resource | Request | Limit |
|---|---:|---:|
| CPU | 50m | 250m |
| Memory | 96Mi | 256Mi |

The deployment was successfully updated and verified using `kubectl rollout status deployment/heatwave-deployment`.

## After-Change Measurements
Observed container usage after the update:
- CPU: 0.71%
- Memory: 130.4 MiB

The readings are point-in-time measurements and may vary with workload. In this sample, actual CPU and memory usage did not decrease after reducing the Kubernetes resource requests and limits. The change reduced the configured resource allocation but did not demonstrate a measured reduction in runtime usage.

## Verification
- Deployment restored to 3/3 available replicas.
- All three pods reached `1/1 Running`.
- All three pods showed zero restarts in the verification screenshot.
- Final CPU and memory requests and limits were checked using `kubectl`.

## Evidence
1. `01_baseline_resource_usage.png` — baseline Docker resource usage.
2. `02_kubernetes_replicas_healthy.png` — three healthy Kubernetes replicas.
3. `03_optimized_resource_limits.png` — final Kubernetes resource settings.

## Conclusion
Kubernetes resource requests and limits were reduced, and the deployment was successfully rolled out with three healthy replicas. However, the sampled runtime CPU and memory usage increased slightly. Further repeated measurements under comparable workloads would be needed to determine whether the change improves resource efficiency or application performance.

Note: The usage measurements are snapshots, not a controlled performance benchmark. The HEATWATCH application uses synthetic educational data.
