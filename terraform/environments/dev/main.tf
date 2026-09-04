provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = var.project_name
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}

locals {
  cluster_name = "${var.project_name}-${var.environment}"
}

data "aws_availability_zones" "available" {
  state = "available"
}

module "networking" {
  source = "../../modules/networking"

  project_name       = var.project_name
  environment        = var.environment
  availability_zones = slice(data.aws_availability_zones.available.names, 0, 2)
}

module "eks" {
  source = "../../modules/eks"

  cluster_name       = local.cluster_name
  private_subnet_ids = module.networking.private_subnet_ids
}

module "karpenter" {
  source = "../../modules/karpenter"

  cluster_name       = module.eks.cluster_name
  cluster_endpoint   = module.eks.cluster_endpoint
  cluster_arn        = module.eks.cluster_arn
  private_subnet_ids = module.networking.private_subnet_ids
}