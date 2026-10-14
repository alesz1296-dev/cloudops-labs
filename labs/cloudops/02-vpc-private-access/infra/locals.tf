locals {
  name_prefix      = "cloudops-02-${var.prefix}"
  function_name    = coalesce(var.function_name, "${local.name_prefix}-handler")
  ssm_role_name    = "${local.name_prefix}-ssm-role"
  lambda_role_name = "${local.function_name}-execution-role"

  log_group_name = "/aws/lambda/${local.function_name}"
  source_file    = "${path.module}/lambda_function.py"

  common_tags = {
    Project     = var.project_name
    Track       = "CloudOps"
    Lab         = "vpc-private-access"
    Environment = var.environment
    NamePrefix  = var.prefix
    ManagedBy   = "Terraform"

  }

  ssm_endpoint_services = toset([
    "ssm",
    "ssmmessages",
    "ec2messages"
  ])

}