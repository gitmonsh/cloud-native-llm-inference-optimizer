# Networking Module

## Purpose

This module will create the networking foundation for the AWS deployment.

It will include:

- VPC
- public subnets
- private subnets
- route tables
- internet gateway
- NAT gateway if needed
- security group foundations

## Cost Note

NAT gateways can create hourly cost.

For early development, the networking design should avoid unnecessary NAT gateway usage where possible.