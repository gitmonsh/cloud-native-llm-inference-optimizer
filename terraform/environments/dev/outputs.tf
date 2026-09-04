output "aws_region" {
  description = "AWS region for the development environment."
  value       = var.aws_region
}

output "cluster_name" {
  description = "Planned EKS cluster name."
  value       = local.cluster_name
}

output "vpc_id" {
  description = "Planned VPC ID."
  value       = module.networking.vpc_id
}

output "public_subnet_ids" {
  description = "Planned public subnet IDs."
  value       = module.networking.public_subnet_ids
}

output "private_subnet_ids" {
  description = "Planned private subnet IDs."
  value       = module.networking.private_subnet_ids
}

output "eks_cluster_endpoint" {
  description = "EKS cluster endpoint."
  value       = module.eks.cluster_endpoint
}

output "eks_cluster_arn" {
  description = "EKS cluster ARN."
  value       = module.eks.cluster_arn
}