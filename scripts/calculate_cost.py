import argparse
import csv
import math


def percentile(values, percentile_value):
    if not values:
        return 0

    sorted_values = sorted(values)
    index = math.ceil((percentile_value / 100) * len(sorted_values)) - 1
    index = max(0, min(index, len(sorted_values) - 1))

    return sorted_values[index]


def analyze_results(input_file, instance_hourly_price, runtime_minutes):
    latencies = []
    ttfts = []
    total_tokens = 0
    successful_requests = 0

    with open(input_file, "r") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            successful_requests += 1

            input_tokens = int(row["input_tokens"])
            output_tokens = int(row["output_tokens"])
            latency = float(row["latency_seconds"])
            ttft = float(row["time_to_first_token_seconds"])

            total_tokens += input_tokens + output_tokens
            latencies.append(latency)
            ttfts.append(ttft)

    runtime_hours = runtime_minutes / 60
    total_compute_cost = instance_hourly_price * runtime_hours

    cost_per_request = (
        total_compute_cost / successful_requests if successful_requests else 0
    )

    cost_per_1000_tokens = (
        total_compute_cost / (total_tokens / 1000) if total_tokens else 0
    )

    print("Benchmark Summary")
    print("=================")
    print(f"Input file: {input_file}")
    print(f"Successful requests: {successful_requests}")
    print(f"Total tokens: {total_tokens}")
    print(f"Runtime minutes: {runtime_minutes}")
    print(f"Instance hourly price: ${instance_hourly_price:.4f}")
    print(f"Estimated compute cost: ${total_compute_cost:.6f}")
    print()
    print("Latency")
    print("=======")
    print(f"Average latency: {sum(latencies) / len(latencies):.3f}s")
    print(f"p95 latency: {percentile(latencies, 95):.3f}s")
    print(f"p99 latency: {percentile(latencies, 99):.3f}s")
    print(f"Average TTFT: {sum(ttfts) / len(ttfts):.3f}s")
    print(f"p95 TTFT: {percentile(ttfts, 95):.3f}s")
    print()
    print("Cost")
    print("====")
    print(f"Cost per request: ${cost_per_request:.8f}")
    print(f"Cost per 1,000 tokens: ${cost_per_1000_tokens:.8f}")


def main():
    parser = argparse.ArgumentParser(description="Calculate LLM benchmark cost metrics")
    parser.add_argument(
        "--input",
        required=True,
        help="Path to benchmark CSV file",
    )
    parser.add_argument(
        "--instance-hourly-price",
        type=float,
        default=1.0,
        help="Hourly instance price in USD",
    )
    parser.add_argument(
        "--runtime-minutes",
        type=float,
        required=True,
        help="Benchmark runtime in minutes",
    )

    args = parser.parse_args()

    analyze_results(
        input_file=args.input,
        instance_hourly_price=args.instance_hourly_price,
        runtime_minutes=args.runtime_minutes,
    )


if __name__ == "__main__":
    main()