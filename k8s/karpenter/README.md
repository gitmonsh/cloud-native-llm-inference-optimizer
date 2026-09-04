# Karpenter GPU Scheduling

## Purpose

This folder contains draft Karpenter manifests for GPU-aware node provisioning.

Karpenter will eventually create GPU EC2 nodes when the vLLM GPU pod cannot be scheduled due to missing GPU capacity.

## Files

| File | Purpose |
|---|---|
| `gpu-nodepool.yml` | Defines GPU instance requirements and scale-down behavior |
| `gpu-ec2nodeclass.yml` | Defines AWS-specific node configuration for GPU nodes |

## NodePool

The NodePool limits GPU inference nodes to the `g5` instance family.

Allowed sizes:

- `g5.xlarge`
- `g5.2xlarge`

Allowed capacity types:

- Spot
- On-demand

Spot is preferred for cost optimization, but on-demand may be needed for reliability during benchmarking.

## Scheduling Label

The NodePool applies this label:

`workload: gpu-inference`

The vLLM GPU deployment uses the same label as a node selector.

This connects the GPU workload to GPU-provisioned nodes.

## Scale-Down Behavior

The NodePool uses:

`consolidationPolicy: WhenEmpty`

This means Karpenter can remove unused GPU nodes after workloads are gone.

## Placeholders

Before applying these manifests, replace:

- `REPLACE_WITH_KARPENTER_NODE_ROLE_NAME`
- `REPLACE_WITH_CLUSTER_NAME`

These values should come from Terraform outputs.

## Important Note

Do not apply these manifests until the EKS cluster, Karpenter controller, IAM roles, and GPU node permissions are fully configured.

These files are production-direction drafts for the AWS benchmark phase.