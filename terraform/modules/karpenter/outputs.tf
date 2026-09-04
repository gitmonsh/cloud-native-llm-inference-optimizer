output "karpenter_node_role_name" {
  description = "IAM role name for Karpenter-provisioned nodes."
  value       = aws_iam_role.karpenter_node.name
}

output "karpenter_node_instance_profile_name" {
  description = "Instance profile name for Karpenter-provisioned nodes."
  value       = aws_iam_instance_profile.karpenter_node.name
}

output "allowed_gpu_instance_types" {
  description = "Allowed GPU instance types for inference workloads."
  value       = var.gpu_instance_types
}