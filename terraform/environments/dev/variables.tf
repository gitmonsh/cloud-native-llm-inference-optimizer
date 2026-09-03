variable "aws_region" {
  description = "AWS region for the development environment."
  type        = string
  default     = "us-west-2"
}

variable "project_name" {
  description = "Project name used for tagging and resource naming."
  type        = string
  default     = "cloud-native-llm-inference-optimizer"
}

variable "environment" {
  description = "Deployment environment name."
  type        = string
  default     = "dev"
}