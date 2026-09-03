#!/bin/bash

set -e

PATTERN=${1:-burst}
REQUESTS=${2:-50}
DELAY=${3:-0.1}
OUTPUT_FILE=${4:-results/baseline/local_benchmark.csv}
INSTANCE_HOURLY_PRICE=${5:-1.0}
RUNTIME_MINUTES=${6:-1}

echo "Running LLM inference benchmark"
echo "Pattern: $PATTERN"
echo "Requests: $REQUESTS"
echo "Delay: $DELAY"
echo "Output file: $OUTPUT_FILE"
echo

python load-generator/load_test.py \
  --requests "$REQUESTS" \
  --pattern "$PATTERN" \
  --delay "$DELAY" \
  --output "$OUTPUT_FILE"

echo
echo "Calculating benchmark cost"
echo

python scripts/calculate_cost.py \
  --input "$OUTPUT_FILE" \
  --instance-hourly-price "$INSTANCE_HOURLY_PRICE" \
  --runtime-minutes "$RUNTIME_MINUTES"