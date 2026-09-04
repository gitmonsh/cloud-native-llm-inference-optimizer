variable "cluster_name" {
  description = "EKS cluster name used for log group naming."
  type        = string
}

variable "log_retention_days" {
  description = "CloudWatch log retention in days."
  type        = number
  default     = 7
}