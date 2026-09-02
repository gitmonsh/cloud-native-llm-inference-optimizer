# Local Inference Simulator

## Purpose

This folder contains a local FastAPI-based LLM inference simulator.

The simulator is used for free local development before deploying to AWS.

It helps test:

- inference request flow
- latency tracking
- token counting
- simulated queue depth
- simulated GPU utilization
- Prometheus metrics
- load generator behavior
- cost calculator workflow

## Important Note

This simulator does not represent real GPU performance.

It is only used to validate the local benchmark pipeline.

Real batching behavior, GPU utilization, and cold-start behavior will be tested later on AWS using vLLM on GPU instances.

## Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/health` | GET | Checks whether the server is running |
| `/generate` | POST | Simulates an LLM inference request |
| `/metrics` | GET | Exposes Prometheus-style metrics |

## Run The Server

From the project root, install dependencies:

pip install -r local-inference/requirements.txt

Start the server:

uvicorn local-inference.server:app --reload --port 8000

Health check:

http://127.0.0.1:8000/health

Metrics:

http://127.0.0.1:8000/metrics

## Example Request

curl -X POST http://127.0.0.1:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Explain why GPU autoscaling is hard for LLM inference","max_tokens":80}'

## Metrics Exposed

| Metric | Meaning |
|---|---|
| `llm_requests_total` | Total inference requests processed |
| `llm_tokens_total` | Total simulated input and output tokens |
| `llm_request_latency_seconds` | End-to-end request latency |
| `llm_time_to_first_token_seconds` | Simulated time to first token |
| `llm_queue_depth` | Simulated inference queue depth |
| `llm_gpu_utilization_percent` | Simulated GPU utilization |

## Why This Exists

The full AWS GPU deployment costs money, so local simulation lets us build and test most of the project safely before running a short paid AWS benchmark.