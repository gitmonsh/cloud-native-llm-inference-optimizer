# EKS Module

## Purpose

This module will create the Amazon EKS cluster.

It will include:

- EKS cluster
- cluster IAM role
- node IAM roles
- Kubernetes access configuration
- cluster outputs

## Cost Note

EKS has an hourly control plane cost while the cluster exists.

The project should only create the EKS cluster when actively testing.