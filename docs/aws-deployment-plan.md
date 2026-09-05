# AWS Deployment Plan

## Purpose

This document explains the planned AWS deployment sequence for the production-style LLM inference platform.

The goal is to deploy only after the local simulator, monitoring pipeline, Kubernetes manifests, and Terraform configuration have been validated.

## Deployment Philosophy

AWS resources should be created only during active testing windows.

The project should avoid idle GPU cost by using short benchmark runs and destroying infrastructure immediately afterward.

## Pre-Deployment Checklist

Before deploying to AWS, confirm:

- AWS credentials are configured.
- Terraform validates successfully.
- Terraform plan has been reviewed.
- Expected AWS region is correct.
- EKS control plane cost is understood.
- GPU instance cost is understood.
- Karpenter GPU provisioning is configured.
- Cleanup plan is ready.
- Benchmark commands are ready.
- Grafana dashboard export is saved.

## Deployment Sequence

## 1. Review Terraform Plan

Run:

terraform -chdir=terraform/environments/dev plan

Review planned resources carefully before applying.

Expected infrastructure:

- VPC
- public subnets
- private subnets
- internet gateway
- route tables
- EKS cluster
- EKS IAM role
- Karpenter node IAM role
- CloudWatch log group

## 2. Apply Terraform

Only after reviewing the plan:

terraform -chdir=terraform/environments/dev apply

## 3. Configure kubectl

After EKS is created, configure local kubectl access:

aws eks update-kubeconfig \
  --region us-west-2 \
  --name cloud-native-llm-inference-optimizer-dev

## 4. Install Required Kubernetes Add-ons

Before deploying vLLM, the cluster needs:

- NVIDIA device plugin
- Karpenter controller
- metrics support
- Prometheus/Grafana or monitoring stack

## 5. Apply Namespace

Run:

kubectl apply -f k8s/namespace.yml

## 6. Apply Karpenter GPU Manifests

Update placeholders in:

- k8s/karpenter/gpu-ec2nodeclass.yml
- k8s/karpenter/gpu-nodepool.yml

Then apply:

kubectl apply -f k8s/karpenter/

## 7. Deploy vLLM

Apply:

kubectl apply -f k8s/vllm/vllm-gpu-deployment.yml
kubectl apply -f k8s/vllm/vllm-gpu-service.yml

## 8. Watch Cold Start

Track the timeline from pending pod to ready inference service:

- pod pending time
- GPU node provisioning time
- image pull time
- model load time
- readiness probe success
- first successful inference

## 9. Run Benchmark

Run the benchmark workload:

./scripts/run_benchmark.sh burst 50 0.1 results/baseline/aws_gpu_test.csv 1.0 1

The final AWS command may need a different endpoint URL once the service is exposed.

## 10. Capture Results

Save:

- benchmark CSV
- cost calculator output
- Grafana screenshots
- Prometheus metrics
- cold-start timing notes
- AWS instance pricing source

## 11. Destroy Infrastructure

After testing:

terraform -chdir=terraform/environments/dev destroy

Then verify in AWS Console that expensive resources are removed.

## First Base Infrastructure Test

A first AWS base infrastructure test was completed.

Actions performed:

- Ran Terraform apply for the base infrastructure.
- Created the EKS control plane.
- Verified the cluster reached ACTIVE status.
- Updated local kubeconfig for the EKS cluster.
- Confirmed the cluster had no worker nodes.
- Destroyed the infrastructure immediately after verification.

Result:

- EKS cluster status: ACTIVE
- Kubernetes nodes: none
- GPU nodes created: no
- Terraform destroy completed successfully
- Resources destroyed: 14

This verified the base EKS infrastructure path without starting GPU instances.

## Important Cost Note

Do not leave EKS clusters, GPU EC2 instances, load balancers, NAT gateways, or EBS volumes running after benchmark tests.

## Current Status

AWS deployment has not been run yet.

The current project state is local validation plus Terraform/Kubernetes deployment preparation.