# Local Kubernetes

## Purpose

This document explains how to run the local inference simulator in a local Kubernetes cluster.

This is used before deploying to AWS EKS.

The goal is to validate:

- Kubernetes Deployment
- Kubernetes Service
- namespace isolation
- health checks
- inference endpoint
- local benchmark workflow

## Prerequisites

You need:

- Docker Desktop
- Kubernetes enabled in Docker Desktop
- kubectl installed
- local Docker image built

## Safety Check

Before applying Kubernetes manifests, confirm you are using the local Docker Desktop cluster.

Run:

kubectl config current-context

Expected output:

docker-desktop

Do not apply local test manifests if the current context points to an AWS EKS cluster.

## Build The Local Image

From the project root, run:

docker build -t local-inference:latest -f local-inference/Dockerfile .

## Deploy To Local Kubernetes

Apply the namespace:

kubectl apply -f k8s/namespace.yml

Apply the inference Deployment and Service:

kubectl apply -f k8s/vllm/local-inference-deployment.yml
kubectl apply -f k8s/vllm/local-inference-service.yml

Apply the initial HPA:

kubectl apply -f k8s/autoscaling/local-inference-hpa.yml

## Check The Deployment

Run:

kubectl get pods -n llm-inference

Expected result:

The local inference pod should show READY 1/1 and STATUS Running.

## Test The Service

Port-forward the service:

kubectl port-forward -n llm-inference service/local-inference 8082:8000

In another terminal, test health:

curl http://127.0.0.1:8082/health

Expected response:

{"status":"ok"}

Test inference:

curl -X POST http://127.0.0.1:8082/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Test local Kubernetes inference","max_tokens":50}'

## Run A Benchmark

With port-forwarding active, run:

python load-generator/load_test.py \
  --url http://127.0.0.1:8082/generate \
  --requests 20 \
  --pattern burst \
  --delay 0.1 \
  --output results/baseline/k8s_namespace_test.csv

Calculate cost:

python scripts/calculate_cost.py \
  --input results/baseline/k8s_namespace_test.csv \
  --instance-hourly-price 1.0 \
  --runtime-minutes 1

## Cleanup

To delete the local Kubernetes resources:

kubectl delete namespace llm-inference

## Important Note

This local Kubernetes deployment does not use real GPUs.

It validates Kubernetes packaging and deployment flow before moving to AWS EKS and vLLM on GPU nodes.