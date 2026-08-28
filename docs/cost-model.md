# Cost Model

## Goal

The goal of the cost model is to calculate how much it costs to serve LLM inference traffic.

This helps us compare the naive baseline against the optimized deployment.

The main question is:

Can autoscaling and better GPU usage reduce inference cost?

## Why Cost Matters

GPU instances are expensive.

If a GPU instance costs about $1 per hour and runs all month, it can cost around $700 or more.

For companies serving LLMs, this becomes a major cloud bill.

So instead of only measuring latency, this project also measures cost.

## Main Cost Metrics

| Metric | Formula |
|---|---|
| Total compute cost | instance_hourly_price * runtime_hours * instance_count |
| Cost per request | total_compute_cost / successful_requests |
| Cost per token | total_compute_cost / total_tokens |
| Cost per 1,000 tokens | total_compute_cost / (total_tokens / 1000) |
| Estimated monthly cost | hourly_cost * 730 |
| Savings percentage | ((baseline_cost - optimized_cost) / baseline_cost) * 100 |

## Baseline Cost

The naive baseline assumes GPU capacity stays running even when traffic is low.

Example:

If one GPU instance costs $1 per hour:

1 dollar/hour * 730 hours/month = 730 dollars/month

So one always-on GPU can cost around:

$730 per month

This is why idle GPUs are expensive.

## Optimized Cost

The optimized setup only keeps GPU capacity when it is needed.

Example:

If traffic is low at night, the system can scale down.

If traffic increases, the system scales up.

So optimized cost is based on actual runtime:

optimized_cost = sum of GPU instance hours actually used

## What We Compare

| Setup | Cost Behavior |
|---|---|
| Naive Baseline | GPU stays running even when idle |
| Optimized Deployment | GPU capacity scales based on demand |

## Example Final Cost Table

The real numbers will be filled in after testing.

| Setup | Estimated Monthly Cost | Cost per Request | Cost per 1,000 Tokens | Savings |
|---|---:|---:|---:|---:|
| Naive Baseline | TBD | TBD | TBD | 0% |
| Optimized Deployment | TBD | TBD | TBD | TBD |

## Important Notes

AWS pricing can change, so the project should record:

- AWS region
- instance type
- on-demand or spot pricing
- test duration
- number of GPU instances
- total tokens generated
- total successful requests

If we use simulated local results, we must label them as simulated.

If we use real AWS GPU results, we can label them as real benchmark results.

## Key Takeaway

The goal is not just to say the system runs.

The goal is to prove:

The optimized deployment served the same workload with lower cost while keeping latency acceptable.