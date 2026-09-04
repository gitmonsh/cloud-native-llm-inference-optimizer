# Architecture

## Overview

This project runs an open-source LLM behind a cloud-native inference platform on AWS.

The system accepts user-style prompts, serves them through vLLM, collects inference metrics, and uses those metrics to make scaling decisions.

The main goal is not just to run a model. The goal is to understand and optimize the relationship between:

- inference latency
- GPU utilization
- request queue depth
- cost per token
- cold-start time
- autoscaling behavior

## High-Level Architecture

```mermaid
flowchart TD
    A["Load Generator"] --> B["AWS Load Balancer"]
    B --> C["vLLM Pods on EKS"]
    C --> D["Open-Source LLM on GPU"]
    C --> E["Prometheus Metrics"]
    E --> F["Grafana Dashboard"]
    E --> G["Autoscaling Policy"]
    G --> H["HPA or KEDA"]
    H --> I["Karpenter"]
    I --> J["GPU EC2 Nodes"]
    J --> C

## Main Components

| Component | Responsibility |
|---|---|
| Load Generator | Simulates realistic user traffic |
| AWS Load Balancer | Routes incoming requests to the inference service |
| vLLM | Serves the open-source LLM efficiently |
| EKS | Runs the Kubernetes cluster |
| GPU EC2 Nodes | Provide GPU compute for inference |
| Karpenter | Adds or removes GPU nodes based on workload demand |
| Prometheus | Collects metrics from the system |
| Grafana | Displays dashboards for latency, cost, throughput, and GPU usage |
| Autoscaling Policy | Decides when to add or remove inference capacity |
| HPA/KEDA | Applies scaling decisions inside Kubernetes |
| Terraform | Creates and manages AWS infrastructure |

Request Flow
The load generator sends prompts to the AWS Load Balancer.
The Load Balancer forwards requests to the vLLM service running on EKS.
vLLM sends the prompt through the open-source model running on a GPU node.
The model generates tokens and returns a response.
Metrics are collected during the request.
Prometheus stores the metrics.
Grafana displays the metrics in dashboards.
The autoscaling policy uses the metrics to decide whether more or fewer resources are needed.

Scaling Flow
Traffic increases.
Requests begin waiting in the inference queue.
Queue depth and time to first token increase.
Prometheus records these metrics.
HPA or KEDA scales the number of vLLM replicas.
If there is no available GPU capacity, the new pod stays pending.
Karpenter detects the pending GPU pod.
Karpenter provisions a new GPU EC2 node.
Kubernetes schedules the vLLM pod on the new node.
The container starts.
The model loads into GPU memory.
The new replica begins serving requests.
Important Design Challenge
GPU autoscaling is not instant.
A normal web app may scale in seconds, but an LLM inference workload can take minutes to become ready because the system must provision a GPU node, start the pod, pull the image, load the model, and warm up the server.
Because of this, this project measures cold-start time directly.

## Key Tradeoff

Autoscaling can reduce cost by shutting down unused GPU capacity, but aggressive scale-down can make the next traffic spike slower because new GPU capacity takes time to start.

So the project studies this tradeoff:

| Goal | Tradeoff |
|---|---|
| Lower cost | Scale down idle GPUs |
| Lower latency | Keep enough GPU capacity warm |
| Higher throughput | Use batching efficiently |
| Lower tail latency | Avoid making requests wait too long |

## Terraform Architecture

The AWS infrastructure is organized into Terraform modules.

| Module | Status | Responsibility |
|---|---|---|
| networking | Created | VPC, public subnets, private subnets, internet gateway, public routing |
| eks | Created | EKS cluster, cluster IAM role, EKS cluster policy attachment |
| karpenter | Created | Karpenter node IAM role, node instance profile, GPU instance type configuration |
| observability | Created | CloudWatch log group and log retention settings |

## Current Infrastructure Status

The Terraform configuration has been formatted and validated locally.

No AWS infrastructure has been created yet.

A full `terraform plan` requires AWS credentials because the AWS provider must query account and region information before generating the plan.

## Current Local Runtime Modes

The project currently supports three local runtime modes:

| Mode | Status | Purpose |
|---|---|---|
| Direct Python | Working | Run the simulator directly with Uvicorn |
| Docker Compose | Working | Run simulator, Prometheus, and Grafana together |
| Local Kubernetes | Working | Test Kubernetes Deployment, Service, namespace, and HPA locally |

## Remaining Production Work

The remaining production work includes:

- replacing the simulator with real vLLM serving
- configuring real GPU node provisioning on AWS
- connecting Karpenter to GPU workload scheduling
- collecting real GPU metrics
- running the final AWS benchmark
- comparing naive vs optimized cost and latency