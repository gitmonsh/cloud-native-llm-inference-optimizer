output "aws_region" {
  description = "AWS region for the development environment."
  value       = var.aws_region
}

output "cluster_name" {
  description = "Planned EKS cluster name."
  value       = local.cluster_name
}