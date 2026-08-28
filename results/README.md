# Results

This folder stores benchmark outputs for the project.

## Folder Structure

| Folder | Purpose |
|---|---|
| baseline | Results from the naive baseline deployment |
| optimized | Results from the optimized autoscaling deployment |

## Current Local Test

The first local test validates the simulator, load generator, and cost calculator.

This does not represent real GPU performance. It is only used to test the local benchmark pipeline before running AWS GPU tests.

| Metric | Value |
|---|---:|
| Successful requests | 20 |
| Total tokens | 1,114 |
| Average latency | 0.585s |
| p95 latency | 0.791s |
| p99 latency | 0.844s |
| Average TTFT | 0.293s |
| p95 TTFT | 0.496s |
| Estimated compute cost | $0.016667 |
| Cost per request | $0.00083333 |
| Cost per 1,000 tokens | $0.01496110 |

## Important Note

Local results are simulated and should not be presented as real GPU benchmark numbers.

Real results will be collected later from AWS using EKS, Karpenter, and vLLM on GPU instances.