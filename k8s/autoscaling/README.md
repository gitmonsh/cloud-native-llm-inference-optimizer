# Autoscaling

## Purpose

This folder contains autoscaling configuration for the inference service.

The first version uses a basic Kubernetes HorizontalPodAutoscaler.

Later versions will move toward LLM-specific autoscaling based on inference metrics.

## Current File

| File | Purpose |
|---|---|
| `local-inference-hpa.yml` | Basic HPA for the local inference deployment |

## Current HPA Behavior

The first HPA scales the local inference deployment from 1 to 3 replicas based on CPU utilization.

This is useful as a Kubernetes autoscaling foundation, but it is not the final optimization strategy.

## Final Autoscaling Goal

The final project should use inference-specific signals such as:

- queue depth
- time to first token
- request latency
- tokens per second
- GPU utilization

A stronger autoscaling policy could look like:

Scale up when:

queue_depth > 20  
and p95_time_to_first_token > 1.5 seconds  
for 2 minutes

Scale down when:

queue_depth is near 0  
and GPU utilization < 25%  
for 10-15 minutes

## Important Note

CPU-based autoscaling is only a starting point.

The main goal of this project is to show why LLM inference needs workload-specific autoscaling instead of generic web-app autoscaling.