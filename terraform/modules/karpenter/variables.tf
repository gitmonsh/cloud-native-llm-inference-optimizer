variable "cluster_name" {
  description = "Name of the EKS cluster Karpenter will manage."
  type        = string
}

variable "cluster_endpoint" {
  description = "EKS cluster endpoint."
  type        = string
}

variable "cluster_arn" {
  description = "EKS cluster ARN."
  type        = string
}

variable "private_subnet_ids" {
  description = "Private subnet IDs where Karpenter-provisioned nodes can run."
  type        = list(string)
}

variable "gpu_instance_types" {
  description = "Allowed GPU instance types for inference workloads."
  type        = list(string)
  default     = ["g5.xlarge", "g5.2xlarge"]
}