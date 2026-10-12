variable "aws_region" {
  description = "The AWS region to deploy resources in."
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "The name of the project."
  type        = string
  default     = "cloudops-01-monitoring"
}

variable "environment" {
  type        = string
  description = "Sandbox environment label."
  default     = "sandbox"
}

variable "function_name" {
  description = "The name of the Lambda function."
  type        = string
  default     = "cloudops-01-monitoring"
}



