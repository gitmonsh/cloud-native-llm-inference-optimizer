# Benchmark Methodology

## Goal

The goal of the benchmark is to compare a naive LLM inference deployment against an optimized deployment.

We want to measure whether the optimized setup can reduce cost while keeping latency acceptable.

Main question:

Can we lower cost per token without making user experience worse?

## Compared Setups

| Setup | Description |
|---|---|
| Naive Baseline | Fixed GPU capacity, always running, basic vLLM configuration |
| Optimized Deployment | Autoscaling enabled, tuned vLLM settings, scale-down during idle periods, cold-start measurement |

## Why This Benchmark Matters

The benchmark numbers are one of the most important parts of this project.

Interviewers may ask:

- How did you measure the results?
- Did both tests use the same traffic?
- Did both tests use the same model?
- Was the cost calculation fair?
- Did you include cold-start delay?
- Did you measure p95 and p99 latency?

So both test runs must use the same conditions.

## Fairness Rules

Both the naive and optimized deployments must use the same:

- AWS region
- model
- prompt dataset
- traffic pattern
- test duration
- success criteria
- measurement scripts

If we change any of these, the comparison may not be fair.

## Traffic Patterns

The load generator should support different traffic patterns.

| Traffic Pattern | Meaning |
|---|---|
| Steady traffic | Same number of requests over time |
| Bursty traffic | Sudden spikes followed by quiet periods |
| Diurnal traffic | Simulates traffic changing throughout the day |
| Cooldown traffic | Traffic drops after a spike to test scale-down |

The main benchmark should use bursty traffic because LLM workloads are often unpredictable.

## Metrics To Collect

| Metric | Why It Matters |
|---|---|
| Total requests | Shows workload size |
| Successful requests | Shows reliability |
| Failed requests | Shows error rate |
| Input tokens | Helps normalize workload |
| Output tokens | Used for throughput and cost calculations |
| p50 latency | Typical response time |
| p95 latency | Slow-user experience |
| p99 latency | Worst-case latency |
| Time to first token | How fast streaming response begins |
| Tokens per second | Model throughput |
| Queue depth | Shows whether the model is overloaded |
| GPU utilization | Shows how efficiently the GPU is used |
| Cold-start time | Shows how long scaling takes |
| Estimated cloud cost | Shows business impact |
| Cost per 1,000 tokens | Main cost-efficiency metric |

## Cost Calculation

The basic cost formula is:

total_compute_cost = instance_hourly_price * runtime_hours * instance_count

Cost per request:

cost_per_request = total_compute_cost / successful_requests

Cost per 1,000 tokens:

cost_per_1000_tokens = total_compute_cost / (total_tokens / 1000)

Savings percentage:

savings_percent = ((baseline_cost - optimized_cost) / baseline_cost) * 100

## Example Final Results Table

The real numbers will be filled in after testing.

| Setup | Cost | Cost per 1,000 Tokens | p95 Latency | p99 Latency | Cold-Start Time | Error Rate |
|---|---:|---:|---:|---:|---:|---:|
| Naive Baseline | TBD | TBD | TBD | TBD | N/A | TBD |
| Optimized Deployment | TBD | TBD | TBD | TBD | TBD | TBD |

## Benchmark Steps

1. Deploy the naive baseline.
2. Run the fixed traffic pattern.
3. Collect latency, token, GPU, and cost metrics.
4. Save the results.
5. Deploy the optimized version.
6. Run the same traffic pattern again.
7. Collect the same metrics.
8. Compare the results.
9. Write the final analysis.

## Interview Defense

A strong explanation should sound like this:

I used the same model, prompt dataset, traffic pattern, and test duration for both runs. The optimized setup was compared against a fixed always-on GPU baseline. I measured p50, p95, p99 latency, time to first token, queue depth, tokens per second, GPU utilization, cold-start time, and cost per 1,000 tokens.

## Key Takeaway

The benchmark is not just for showing graphs.

The benchmark proves whether the optimized system actually saves money without damaging latency.