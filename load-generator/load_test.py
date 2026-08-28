import argparse
import csv
import random
import time
from datetime import datetime, timezone

import requests


PROMPTS = [
    "Explain why GPU autoscaling is difficult for LLM inference.",
    "Summarize the tradeoff between batching and latency.",
    "What is cost per token in LLM serving?",
    "Explain Kubernetes autoscaling in simple terms.",
    "Why are GPUs expensive for AI workloads?",
    "Describe how Prometheus and Grafana help with observability.",
    "What is time to first token?",
    "Explain why bursty traffic is hard for inference systems.",
]


def send_request(url: str, max_tokens: int) -> dict:
    prompt = random.choice(PROMPTS)
    started_at = time.time()

    response = requests.post(
        url,
        json={"prompt": prompt, "max_tokens": max_tokens},
        timeout=30,
    )

    completed_at = time.time()
    response.raise_for_status()
    data = response.json()

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "prompt": prompt,
        "status_code": response.status_code,
        "input_tokens": data["input_tokens"],
        "output_tokens": data["output_tokens"],
        "latency_seconds": data["latency_seconds"],
        "time_to_first_token_seconds": data["time_to_first_token_seconds"],
        "simulated_gpu_utilization": data["simulated_gpu_utilization"],
        "client_observed_latency_seconds": completed_at - started_at,
    }


def run_load_test(
    url: str,
    requests_count: int,
    delay_seconds: float,
    max_tokens: int,
    output_file: str,
):
    results = []

    for index in range(requests_count):
        try:
            result = send_request(url, max_tokens)
            results.append(result)
            print(
                f"request={index + 1}/{requests_count} "
                f"latency={result['latency_seconds']:.3f}s "
                f"ttft={result['time_to_first_token_seconds']:.3f}s "
                f"tokens={result['output_tokens']}"
            )
        except Exception as error:
            print(f"request={index + 1}/{requests_count} failed error={error}")

        time.sleep(delay_seconds)

    if results:
        fieldnames = list(results[0].keys())

        with open(output_file, "w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)

    print(f"saved_results={output_file}")


def main():
    parser = argparse.ArgumentParser(description="LLM inference load generator")
    parser.add_argument(
        "--url",
        default="http://127.0.0.1:8000/generate",
        help="Inference endpoint URL",
    )
    parser.add_argument(
        "--requests",
        type=int,
        default=20,
        help="Number of requests to send",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.2,
        help="Delay between requests in seconds",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=80,
        help="Maximum output tokens per request",
    )
    parser.add_argument(
        "--output",
        default="results/baseline/local_test.csv",
        help="CSV output path",
    )

    args = parser.parse_args()

    run_load_test(
        url=args.url,
        requests_count=args.requests,
        delay_seconds=args.delay,
        max_tokens=args.max_tokens,
        output_file=args.output,
    )


if __name__ == "__main__":
    main()