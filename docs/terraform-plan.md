# Terraform Plan Runbook

## Purpose

This document explains how to safely review Terraform changes before creating AWS resources.

The goal is to inspect the planned infrastructure and catch cost risks before running `terraform apply`.

## Important Rule

Do not run `terraform apply` until the plan has been reviewed.

## Safe Terraform Commands

These commands do not create AWS resources:

terraform init

terraform fmt

terraform validate

terraform plan

## Working Directory

Terraform commands should be run from the project root using:

terraform -chdir=terraform/environments/dev <command>

## Format Terraform

Run:

terraform -chdir=terraform/environments/dev fmt

## Initialize Terraform

Run:

terraform -chdir=terraform/environments/dev init

## Validate Terraform

Run:

terraform -chdir=terraform/environments/dev validate

Expected result:

Success! The configuration is valid.

## Generate A Plan

Run:

terraform -chdir=terraform/environments/dev plan

This shows what Terraform would create, change, or destroy.

It does not create resources by itself.

## What To Review In The Plan

Before applying, check for:

- EKS cluster
- GPU EC2 nodes
- NAT Gateway
- Load Balancer
- EBS volumes
- IAM roles and policies
- CloudWatch log groups
- unexpected resource count
- unexpected AWS region

## Current Expected Resources

At this stage, the plan may include:

- VPC
- public subnets
- private subnets
- internet gateway
- public route table
- EKS cluster
- EKS cluster IAM role
- EKS cluster policy attachment

## Cost Review

Before applying, estimate:

- hourly EKS cluster cost
- expected EC2 cost
- whether GPU nodes are included
- whether NAT Gateway is included
- expected test duration

## Apply Command

Only after review:

terraform -chdir=terraform/environments/dev apply

## Destroy Command

After testing:

terraform -chdir=terraform/environments/dev destroy

## Current Plan Status

Terraform formatting and validation succeeded.

`terraform plan` was attempted, but AWS credentials were not configured in the local terminal.

Result:

No AWS resources were created.

Error observed:

No valid credential sources found

Next requirement before a real plan:

Configure AWS credentials using AWS CLI, SSO, or environment variables.

## First Successful Plan Review

Terraform plan succeeded after AWS credentials were configured.

Plan summary:

Plan: 19 to add, 0 to change, 0 to destroy.

Cost review:

- EKS cluster is included and will create hourly cost if applied.
- No GPU EC2 instances are included yet.
- No NAT Gateway is included.
- No Load Balancer is included.
- CloudWatch log retention is set to 7 days.

Conclusion:

This plan is acceptable for a first base infrastructure test, but `terraform apply` should only be run during an active testing window.

## Important Note

This project should use local development as much as possible.

AWS deployment should be limited to short benchmark windows.