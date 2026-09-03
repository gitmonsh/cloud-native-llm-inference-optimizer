# Local Monitoring

## Purpose

This document explains the local monitoring setup used before deploying the project to AWS.

The goal is to validate the metrics pipeline for free using the local inference simulator, Prometheus, and Grafana.

## Local Monitoring Stack

| Component | Purpose |
|---|---|
| Local Inference Simulator | Exposes LLM-style metrics at `/metrics` |
| Prometheus | Scrapes and stores metrics |
| Grafana | Visualizes metrics in dashboard panels |
| Docker Compose | Runs Prometheus and Grafana locally |

## Metrics Flow

The local metrics flow is:

```text
FastAPI simulator -> /metrics -> Prometheus -> Grafana dashboard

## Prometheus

Prometheus is configured using:

k8s/monitoring/prometheus-local.yml

It scrapes the local inference simulator every 5 seconds.

Target:

host.docker.internal:8000/metrics

## Grafana

Grafana runs locally at:

http://localhost:3000

The dashboard is named:

LLM Inference Local Dashboard

## Dashboard Panels

The local dashboard includes:

| Panel | Query |
|---|---|
| Total LLM Requests | `llm_requests_total` |
| Total Tokens Generated | `llm_tokens_total` |
| Queue Depth | `llm_queue_depth` |
| Simulated GPU Utilization | `llm_gpu_utilization_percent` |
| Average Request Latency | `rate(llm_request_latency_seconds_sum[1m]) / rate(llm_request_latency_seconds_count[1m])` |
| Average TTFT | `rate(llm_time_to_first_token_seconds_sum[1m]) / rate(llm_time_to_first_token_seconds_count[1m])` |

## How To Run Locally

Terminal 1: start the local inference simulator.

uvicorn local-inference.server:app --reload --port 8000

Terminal 2: start Prometheus and Grafana.

docker compose up

Terminal 3: send burst traffic.

python load-generator/load_test.py --requests 50 --pattern burst --delay 0.1 --output results/baseline/grafana_burst_test.csv

## Validation

Prometheus target health should show:

local-llm-inference: UP

Grafana should display changing values when traffic is sent to the local inference simulator.

## Important Note

This monitoring setup validates the local metrics pipeline.

It does not prove real GPU performance. Real GPU metrics will be collected later during the AWS EKS and vLLM deployment.