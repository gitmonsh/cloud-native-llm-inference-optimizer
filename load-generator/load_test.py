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


def get_delay(pattern: str, request_index: int, base_delay: float) -> float:
    if pattern == "steady":
        return base_delay

    if pattern == "burst":
        # Every 10 requests, send a fast burst. Then pause longer.
        if request_index % 10 < 7:
            return 0.05
        return 1.0

    if pattern == "cooldown":
        # Start fast, then gradually slow down.
        return base_delay + (request_index * 0.05)

    raise ValueError(f"Unsupported traffic pattern: {pattern}")


def run_load_test(
    url: str,
    requests_count: int,
    delay_seconds: float,
    max_tokens: int,
    output_file: str,
    pattern: str,
):
    results = []

    print(f"traffic_pattern={pattern}")
    print(f"requests={requests_count}")
    print(f"output_file={output_file}")

    for index in range(requests_count):
        try:
            result = send_request(url, max_tokens)
            results.append(result)

            print(
                f"request={index + 1}/{requests_count} "
                f"latency={result['latency_seconds']:.3f}s "
                f"ttft={result['time_to_first_token_seconds']:.3f}s "
                f"tokens={result['output_tokens']} "
                f"gpu={result['simulated_gpu_utilization']:.1f}%"
            )
        except Exception as error:
            print(f"request={index + 1}/{requests_count} failed error={error}")

        delay = get_delay(pattern, index, delay_seconds)
        time.sleep(delay)

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
        help="Base delay between requests in seconds",
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

    parser.add_argument(
        "--pattern",
        choices=["steady", "burst", "cooldown"],
        default="steady",
        help="Traffic pattern to generate",
    )

    args = parser.parse_args()

    run_load_test(
        url=args.url,
        requests_count=args.requests,
        delay_seconds=args.delay,
        max_tokens=args.max_tokens,
        output_file=args.output,
        pattern=args.pattern,
    )


if __name__ == "__main__":
    main()