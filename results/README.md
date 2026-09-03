# Results

This folder stores benchmark outputs for the project.

## Folder Structure

| Folder | Purpose |
|---|---|
| baseline | Results from the naive baseline deployment |
| optimized | Results from the optimized autoscaling deployment |

## Current Local Tests

The first local tests validate the simulator, load generator, traffic patterns, and cost calculator.

These results do not represent real GPU performance. They are used to test the local benchmark pipeline before running AWS GPU tests.

## Local Benchmark Summary

| Pattern | Requests | Tokens | Avg Latency | p95 Latency | p99 Latency | p95 TTFT | Cost / Request | Cost / 1K Tokens |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Steady | 10 | 517 | 0.578s | 0.838s | 0.838s | 0.498s | $0.00166667 | $0.03223727 |
| Burst | 20 | 1,093 | 0.634s | 0.856s | 0.880s | 0.523s | $0.00083333 | $0.01524855 |
| Cooldown | 15 | 827 | 0.578s | 0.952s | 0.952s | 0.528s | $0.00111111 | $0.02015316 |

## Grafana Burst Test

This test generated 50 burst-pattern requests while Prometheus and Grafana were running.

It was used to confirm that dashboard panels update when inference traffic is sent to the local simulator.

| Metric | Value |
|---|---:|
| Successful requests | 50 |
| Total tokens | 3,025 |
| Average latency | 0.629s |
| p95 latency | 0.863s |
| p99 latency | 0.995s |
| Average TTFT | 0.307s |
| p95 TTFT | 0.513s |
| Estimated compute cost | $0.016667 |
| Cost per request | $0.00033333 |
| Cost per 1,000 tokens | $0.00550964 |

## Initial Observation

The burst test processed the most tokens during the same estimated 1-minute compute window, which produced the lowest cost per request and cost per 1,000 tokens.

This is only a local simulation, but it helps validate the benchmark workflow that will later be used for AWS GPU testing.

## Docker Compose Test

This test validates that the local inference simulator, Prometheus, and Grafana can run together through Docker Compose.

| Metric | Value |
|---|---:|
| Successful requests | 20 |
| Total tokens | 1,131 |
| Average latency | 0.615s |
| p95 latency | 0.895s |
| p99 latency | 0.904s |
| Average TTFT | 0.318s |
| p95 TTFT | 0.505s |
| Estimated compute cost | $0.016667 |
| Cost per request | $0.00083333 |
| Cost per 1,000 tokens | $0.01473622 |

## Script Benchmark Test

This test validates the reusable benchmark runner script.

The script runs the load generator and then automatically calculates latency and cost metrics.

| Metric | Value |
|---|---:|
| Successful requests | 30 |
| Total tokens | 1,748 |
| Average latency | 0.601s |
| p95 latency | 0.818s |
| p99 latency | 0.866s |
| Average TTFT | 0.295s |
| p95 TTFT | 0.500s |
| Estimated compute cost | $0.016667 |
| Cost per request | $0.00055556 |
| Cost per 1,000 tokens | $0.00953471 |

## Important Note

Local results are simulated and should not be presented as real GPU benchmark numbers.

Real results will be collected later from AWS using EKS, Karpenter, and vLLM on GPU instances.