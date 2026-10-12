provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      Project     = var.project_name
      Track       = "CloudOps"
      Lab         = "cloudops-01-monitoring"
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}
