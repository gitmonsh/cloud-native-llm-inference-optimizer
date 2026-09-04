# Karpenter Module

## Purpose

This module will configure Karpenter for GPU-aware node provisioning.

Karpenter will be used later to create GPU EC2 nodes only when Kubernetes workloads require them.

## Planned Responsibilities

- Karpenter IAM permissions
- Karpenter controller setup
- GPU node pool configuration
- instance type constraints
- scale-down behavior

## Cost Note

Karpenter itself helps reduce cost, but the GPU nodes it creates can be expensive.

GPU node provisioning should be tested carefully and destroyed after benchmark runs.