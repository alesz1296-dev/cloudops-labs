variable "aws_region" {
  description = "The AWS region to deploy resources in."
  type        = string
  default     = "us-east-1"
}

variable "availability_zones" {
  description = "The availability zones to deploy resources in."
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

variable "project_name" {
  description = "The name of the project."
  type        = string
  default     = "cloudops-02-vpc-private-access"
}

variable "environment" {
  type        = string
  description = "Lab laboratory environment label."
  default     = "laboratory"
}

variable "function_name" {
  description = "The name of the Lambda function."
  type        = string
  default     = null
}

variable "prefix" {
  description = "The prefix for each unique student name to avoid resource name collisions."
  type        = string
  default     = "asalazar"
}

variable "vpc_cidr" {
  description = "The CIDR block for the VPC."
  type        = string
  default     = "10.62.0.0/16"
}


# Client EC2 instance variables
variable "ami_id" {
  description = "AMI ID for the private EC2 client. Choose an approved SSM-supported AMI in the selected AWS Region."
  type        = string

  validation {
    condition     = can(regex("^ami-[0-9a-fA-F]+$", var.ami_id))
    error_message = "ami_id must be a valid AMI ID such as ami-0123456789abcdef0."
  }
}

variable "instance_type" {
  description = "EC2 instance type for the private SSM client."
  type        = string
  default     = "t3.micro"
}

#Egress policy variables
variable "endpoint_egress_cidr" {
  description = "IPv4 CIDR allowed for endpoint security-group egress."
  type        = string
  default     = "10.62.0.0/16"
}

variable "endpoint_egress_protocol" {
  description = "IP protocol for endpoint security-group egress. Use -1 for all protocols."
  type        = string
  default     = "-1"

  validation {
    condition     = var.endpoint_egress_protocol == "-1" || can(regex("^(tcp|udp|icmp|icmpv6)$", var.endpoint_egress_protocol))
    error_message = "Use -1 or a supported IP protocol such as tcp, udp, icmp, or icmpv6."
  }
}

#networking variables

variable "https_port" {
  description = "HTTPS port used by the private client and interface endpoints."
  type        = number
  default     = 443

  validation {
    condition     = var.https_port >= 1 && var.https_port <= 65535
    error_message = "https_port must be between 1 and 65535."
  }
}

variable "protocol" {
  description = "Protocol for the client egress security-group rule."
  type        = string
  default     = "tcp"

  validation {
    condition     = can(regex("^(tcp|udp|icmp|icmpv6)$", var.protocol))
    error_message = "Use a supported IP protocol such as tcp, udp, icmp, or icmpv6."
  }
}

variable "client_egress_cidr" {
  description = "IPv4 CIDR allowed for client security-group egress."
  type        = string
  default     = "10.62.0.0/16"
}


variable "client_subnet_az" {
  description = "Availability Zone for the private EC2 client."
  type        = string
  default     = "us-east-1b"

  validation {
    condition     = contains(var.availability_zones, var.client_subnet_az)
    error_message = "client_subnet_az must be one of availability_zones."
  }
}
variable "lambda_runtime" {
  description = "Lambda runtime for the CloudOps-02 handler."
  type        = string
  default     = "python3.14"
}

variable "lambda_handler" {
  description = "Lambda handler in module.function format."
  type        = string
  default     = "lambda_function.lambda_handler"
}

variable "lambda_timeout" {
  description = "Lambda timeout in seconds."
  type        = number
  default     = 3

  validation {
    condition     = var.lambda_timeout >= 1 && var.lambda_timeout <= 900
    error_message = "lambda_timeout must be between 1 and 900 seconds."
  }
}

variable "lambda_memory_size" {
  description = "Lambda memory allocation in MB."
  type        = number
  default     = 128

  validation {
    condition     = var.lambda_memory_size >= 128 && var.lambda_memory_size <= 10240
    error_message = "lambda_memory_size must be between 128 and 10240 MB."
  }
}

variable "lambda_log_retention_days" {
  description = "CloudWatch Logs retention for the Lambda function."
  type        = number
  default     = 7
}

variable "lambda_package_path" {
  description = "Path to the Lambda deployment ZIP."
  type        = string
  default     = "lambda.zip"
}

#API gateway variables
variable "api_stage_name" {
  description = "Deployment stage for the private API."
  type        = string
  default     = "sandbox"
}

