# Terraform

## Purpose

This folder contains Infrastructure as Code for the AWS deployment.

Terraform will be used to create and manage the AWS resources needed for the LLM inference platform.

## Environments

| Environment | Folder | Purpose |
|---|---|---|
| dev | `environments/dev` | Development AWS environment |

## Modules

| Module | Purpose |
|---|---|
| networking | VPC, subnets, routing, and networking foundation |
| eks | Amazon EKS cluster and Kubernetes access |
| karpenter | GPU-aware node provisioning for EKS |
| observability | Monitoring-related cloud resources |

## Important Cost Warning

Do not run `terraform apply` until the AWS plan has been reviewed.

Some resources, especially EKS clusters and GPU instances, can create real AWS cost.