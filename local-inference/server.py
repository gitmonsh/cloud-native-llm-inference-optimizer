import random
import time
from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
from prometheus_client import Counter, Gauge, Histogram, generate_latest
from starlette.responses import Response


app = FastAPI(title="Local LLM Inference Simulator")


REQUEST_COUNT = Counter(
    "llm_requests_total",
    "Total number of inference requests",
)

TOKEN_COUNT = Counter(
    "llm_tokens_total",
    "Total number of generated tokens",
)

REQUEST_LATENCY = Histogram(
    "llm_request_latency_seconds",
    "End-to-end request latency in seconds",
)

TIME_TO_FIRST_TOKEN = Histogram(
    "llm_time_to_first_token_seconds",
    "Time to first token in seconds",
)

QUEUE_DEPTH = Gauge(
    "llm_queue_depth",
    "Simulated number of requests waiting in the inference queue",
)

GPU_UTILIZATION = Gauge(
    "llm_gpu_utilization_percent",
    "Simulated GPU utilization percentage",
)


class GenerateRequest(BaseModel):
    prompt: str
    max_tokens: Optional[int] = 128


class GenerateResponse(BaseModel):
    response: str
    input_tokens: int
    output_tokens: int
    latency_seconds: float
    time_to_first_token_seconds: float
    simulated_gpu_utilization: float


def estimate_tokens(text: str) -> int:
    return max(1, len(text.split()))


def simulate_generation(max_tokens: int) -> tuple[int, float, float, float]:
    output_tokens = random.randint(20, max_tokens)

    queue_depth = random.randint(0, 30)
    gpu_utilization = min(95.0, 30.0 + queue_depth * 2 + random.random() * 10)

    time_to_first_token = 0.05 + queue_depth * 0.015 + random.random() * 0.05
    generation_time = output_tokens * 0.006

    total_latency = time_to_first_token + generation_time

    return output_tokens, total_latency, time_to_first_token, gpu_utilization


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/generate", response_model=GenerateResponse)
def generate(request: GenerateRequest):
    input_tokens = estimate_tokens(request.prompt)

    output_tokens, latency, ttft, gpu_utilization = simulate_generation(
        request.max_tokens or 128
    )

    simulated_queue_depth = random.randint(0, 30)

    QUEUE_DEPTH.set(simulated_queue_depth)
    GPU_UTILIZATION.set(gpu_utilization)

    start_time = time.time()
    time.sleep(latency)

    actual_latency = time.time() - start_time

    REQUEST_COUNT.inc()
    TOKEN_COUNT.inc(input_tokens + output_tokens)
    REQUEST_LATENCY.observe(actual_latency)
    TIME_TO_FIRST_TOKEN.observe(ttft)

    return GenerateResponse(
        response="This is a simulated LLM response for local development.",
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        latency_seconds=actual_latency,
        time_to_first_token_seconds=ttft,
        simulated_gpu_utilization=gpu_utilization,
    )


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")