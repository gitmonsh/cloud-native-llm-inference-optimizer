# Observability Module

## Purpose

This module will contain cloud-side observability resources.

The local version uses Prometheus and Grafana through Docker Compose.

The AWS version may include:

- CloudWatch log groups
- Prometheus-related configuration
- Grafana-related configuration
- metric export configuration

## Cost Note

CloudWatch logs and metrics can create cost depending on volume and retention.

Retention should be kept short for development.