# AWS Cost Safety

## Purpose

This project eventually deploys GPU-backed LLM inference infrastructure on AWS.

GPU instances and EKS clusters can create real cloud costs, so this document defines safety rules before running any real AWS deployment.

## Main Cost Risks

| Resource | Why It Costs Money |
|---|---|
| EKS cluster | Has an hourly control plane cost while running |
| GPU EC2 instances | Main cost driver for LLM inference |
| NAT Gateway | Has hourly and data processing charges |
| Load Balancer | Has hourly and traffic charges |
| CloudWatch logs | Can cost money depending on log volume and retention |
| EBS volumes | Can keep costing money if left behind |

## Golden Rule

Do not run:

terraform apply

until the Terraform plan has been reviewed.

## Safe Commands

These commands are safe because they do not create AWS resources:

terraform fmt

terraform validate

terraform init

## Review Before Apply

Before applying Terraform, check:

- AWS region
- EKS cluster cost
- GPU instance type
- expected runtime
- whether spot instances are used
- whether NAT Gateway is included
- whether load balancers will be created
- whether logs have short retention
- destroy plan after testing

## Deployment Time Limit

For real AWS testing, keep the environment running only during active benchmark work.

Recommended first AWS test window:

30 to 60 minutes

Recommended maximum beginner test window:

2 to 3 hours

## Required Cleanup

After every AWS benchmark run, run:

terraform destroy

Then verify in AWS Console that these are removed:

- EKS cluster
- EC2 instances
- Load Balancers
- NAT Gateways
- EBS volumes
- CloudWatch log groups if no longer needed

## Cost Target

The project should aim to keep total AWS spend around:

$50 to $100

This assumes most development happens locally and AWS is used only for short final benchmark runs.

## Important Note

Local simulation results are free but not real GPU results.

Real cost and performance numbers should only be claimed after an AWS GPU benchmark run.