# vLLM Kubernetes Manifests

## Purpose

This folder contains Kubernetes manifests for local inference testing and future GPU-backed vLLM deployment.

## Files

| File | Purpose |
|---|---|
| `local-inference-deployment.yml` | Runs the local FastAPI inference simulator |
| `local-inference-service.yml` | Exposes the local inference simulator inside Kubernetes |
| `vllm-gpu-deployment.yml` | Draft GPU-backed vLLM deployment for AWS EKS |
| `vllm-gpu-service.yml` | Service for the GPU-backed vLLM deployment |

## Local Simulator

The local simulator is used for free development and Kubernetes validation.

It does not use a real model or GPU.

## vLLM GPU Deployment

The vLLM GPU deployment is intended for AWS EKS GPU nodes.

It requests one NVIDIA GPU using:

`nvidia.com/gpu: 1`

It uses a node selector:

`workload: gpu-inference`

This means the pod should only run on GPU inference nodes.

## Important Note

Do not apply the vLLM GPU deployment locally unless the Kubernetes cluster has GPU support and access to the selected model.

The current GPU manifest is a production-direction draft and will be refined before the AWS benchmark.