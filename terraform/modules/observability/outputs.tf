output "eks_cluster_log_group_name" {
  description = "CloudWatch log group name for EKS cluster logs."
  value       = aws_cloudwatch_log_group.eks_cluster.name
}

output "log_retention_days" {
  description = "CloudWatch log retention in days."
  value       = var.log_retention_days
}