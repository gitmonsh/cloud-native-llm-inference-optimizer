# Cloud-Native LLM Inference Optimizer

AWS EKS-based platform for optimizing LLM inference cost, latency, GPU utilization, and autoscaling under bursty traffic.

## Problem

LLM inference is expensive because GPU instances cost significantly more than regular CPU instances, while user traffic is often unpredictable.

If a company keeps too many GPU nodes running, it wastes money during idle periods. If it keeps too few GPU nodes running, users see high latency, timeouts, and poor reliability during traffic spikes.

This project treats LLM inference as a production cloud workload. The goal is to measure and improve the tradeoff between cost, latency, throughput, GPU utilization, and GPU cold-start time.

## Solution

This platform deploys an open-source LLM with vLLM on Amazon EKS, observes inference-specific metrics, and compares a naive always-on deployment against an optimized autoscaling deployment.

The optimized deployment uses LLM-serving signals such as queue depth, time to first token, tokens per second, and GPU utilization instead of relying only on generic CPU or memory metrics.

## MVP Scope

- Deploy one open-source model using vLLM.
- Run the serving stack on EKS.
- Use Karpenter for GPU node provisioning.
- Collect metrics with Prometheus.
- Visualize cost and performance in Grafana.
- Generate realistic bursty inference traffic.
- Implement a simple custom autoscaling policy.
- Measure GPU cold-start time from scale trigger to first successful inference.
- Compare naive vs optimized deployments using the same benchmark workload.

## Core Metrics

| Metric | Why It Matters |
|---|---|
| Request rate | Shows traffic volume |
| Queue depth | Shows whether requests are waiting |
| Time to first token | Measures streaming responsiveness |
| p50 latency | Typical user experience |
| p95 latency | Slow-user experience |
| p99 latency | Worst-case behavior |
| Tokens per second | Model throughput |
| GPU utilization | GPU efficiency |
| Cost per request | Business cost metric |
| Cost per 1,000 tokens | Main LLM inference cost metric |
| Cold-start time | GPU scale-up delay |

## Benchmark Goal

The final benchmark compares two setups:

| Setup | Description |
|---|---|
| Naive baseline | Always-on GPU capacity, basic vLLM configuration, no smart scale-down |
| Optimized deployment | Autoscaling, tuned vLLM serving settings, scale-down during idle periods, cold-start measurement |

Both runs must use the same model, prompt dataset, traffic pattern, AWS region, test duration, and success criteria.

## Current Progress

- Created project documentation foundation.
- Built local LLM inference simulator using FastAPI.
- Exposed Prometheus-style metrics at `/metrics`.
- Built load generator for sending test inference requests.
- Ran first local baseline test with 20 requests.
- Generated local benchmark CSV at `results/baseline/local_test.csv`.
- Added cost calculator for request, token, latency, and estimated compute cost analysis.

## Local Baseline Test

This first test validates the local development pipeline. It does not represent real GPU performance.

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

## Target Interview Story

Built a cloud-native LLM inference optimization platform on AWS using EKS, Karpenter, vLLM, Terraform, Prometheus, and Grafana; implemented autoscaling based on queue depth and time to first token, measured GPU cold-start delays, and benchmarked cost-per-token savings under bursty traffic.