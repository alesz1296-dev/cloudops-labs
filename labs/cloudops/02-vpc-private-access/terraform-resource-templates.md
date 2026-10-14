# CloudOps-02 Terraform resource templates

Copy these templates into the matching `.tf` files and replace placeholders before applying. Terraform creates resources from dependencies, not file order.

## 1. Provider and common locals

```hcl
provider "aws" {
  region = var.aws_region
}

locals {
  name_prefix   = "cloudops-02-${var.prefix}"
  function_name = coalesce(var.function_name, "${local.name_prefix}-handler")

  common_tags = {
    Project     = var.project_name
    Track       = "CloudOps"
    Lab         = "vpc-private-access"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}
```

## 2. Variables

```hcl
variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "prefix" {
  description = "Unique student suffix."
  type        = string
}

variable "vpc_cidr" {
  type    = string
  default = "10.62.0.0/16"
}

variable "availability_zones" {
  type    = list(string)
  default = ["us-east-1a", "us-east-1b"]
}

variable "client_subnet_az" {
  type    = string
  default = "us-east-1b"
}

variable "ami_id" {
  description = "Approved SSM-supported AMI for the selected Region."
  type        = string
}

variable "instance_type" {
  type    = string
  default = "t3.micro"
}
```

## 3. VPC, subnets, and route table

```hcl
resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-vpc"
  })
}

resource "aws_subnet" "private" {
  for_each = {
    for index, az in var.availability_zones : az => index
  }

  vpc_id            = aws_vpc.main.id
  availability_zone = each.key
  cidr_block        = cidrsubnet(var.vpc_cidr, 4, each.value)

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-subnet-private-${each.key}"
    Tier = "private"
  })
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.main.id

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-rtb-private"
  })
}

resource "aws_route_table_association" "private" {
  for_each = aws_subnet.private

  subnet_id      = each.value.id
  route_table_id = aws_route_table.private.id
}
```

## 4. Security groups

```hcl
resource "aws_security_group" "client" {
  name        = "${local.name_prefix}-client"
  description = "Private EC2 client security group"
  vpc_id      = aws_vpc.main.id

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-client"
  })
}

resource "aws_vpc_security_group_egress_rule" "client_https" {
  security_group_id = aws_security_group.client.id
  ip_protocol       = "tcp"
  from_port         = 443
  to_port           = 443
  cidr_ipv4         = var.vpc_cidr
}

resource "aws_security_group" "endpoint" {
  name        = "${local.name_prefix}-endpoint"
  description = "Interface endpoint security group"
  vpc_id      = aws_vpc.main.id

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-endpoint"
  })
}

resource "aws_vpc_security_group_ingress_rule" "endpoint_https" {
  security_group_id            = aws_security_group.endpoint.id
  referenced_security_group_id = aws_security_group.client.id
  ip_protocol                  = "tcp"
  from_port                   = 443
  to_port                     = 443
}

resource "aws_vpc_security_group_egress_rule" "endpoint" {
  security_group_id = aws_security_group.endpoint.id
  ip_protocol       = "-1"
  cidr_ipv4        = var.vpc_cidr
}
```

## 5. EC2 IAM role and instance profile

```hcl
data "aws_iam_policy_document" "ec2_assume_role" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "ssm_client" {
  name               = "${local.name_prefix}-ssm-role"
  assume_role_policy = data.aws_iam_policy_document.ec2_assume_role.json
}

resource "aws_iam_role_policy_attachment" "ssm_client" {
  role       = aws_iam_role.ssm_client.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
}

resource "aws_iam_instance_profile" "ssm_client" {
  name = "${local.name_prefix}-ssm-profile"
  role = aws_iam_role.ssm_client.name
}
```

## 6. SSM interface endpoints

```hcl
locals {
  ssm_services = toset(["ssm", "ssmmessages", "ec2messages"])
}

resource "aws_vpc_endpoint" "ssm" {
  for_each = local.ssm_services

  vpc_id              = aws_vpc.main.id
  service_name        = "com.amazonaws.${var.aws_region}.${each.key}"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = [for subnet in aws_subnet.private : subnet.id]
  security_group_ids  = [aws_security_group.endpoint.id]
  private_dns_enabled = true

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-${each.key}-endpoint"
  })
}
```

## 7. EC2 private client

```hcl
resource "aws_instance" "ssm_client" {
  ami                         = var.ami_id
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.private[var.client_subnet_az].id
  vpc_security_group_ids      = [aws_security_group.client.id]
  iam_instance_profile        = aws_iam_instance_profile.ssm_client.name
  associate_public_ip_address = false

  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"
    http_put_response_hop_limit = 2
  }

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-private-client"
  })
}
```

## 8. Lambda execution role and function

```hcl
data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "lambda" {
  name               = "${local.name_prefix}-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/${local.function_name}"
  retention_in_days = 7
}

resource "aws_lambda_function" "handler" {
  function_name = local.function_name
  role          = aws_iam_role.lambda.arn
  runtime       = "python3.14"
  handler       = "lambda_function.lambda_handler"
  filename      = "${path.module}/lambda.zip"
  timeout       = 3
  memory_size   = 128

  source_code_hash = filebase64sha256("${path.module}/lambda.zip")

  depends_on = [aws_iam_role_policy_attachment.lambda_logs]
}
```

## 9. Private API resource policy

```hcl
data "aws_caller_identity" "current" {}

data "aws_iam_policy_document" "private_api" {
  statement {
    effect = "Allow"

    principals {
      type        = "AWS"
      identifiers = ["*"]
    }

    actions   = ["execute-api:Invoke"]
    resources = ["arn:aws:execute-api:${var.aws_region}:${data.aws_caller_identity.current.account_id}:*/*/*/*"]

    condition {
      test     = "StringEquals"
      variable = "aws:SourceVpc"
      values   = [aws_vpc.main.id]
    }
  }
}
```

## 10. Private API Gateway

```hcl
resource "aws_api_gateway_rest_api" "private" {
  name   = "${local.name_prefix}-private-api"
  policy = data.aws_iam_policy_document.private_api.json

  endpoint_configuration {
    types            = ["PRIVATE"]
    vpc_endpoint_ids = [aws_vpc_endpoint.execute_api.id]
  }
}

resource "aws_api_gateway_resource" "health" {
  rest_api_id = aws_api_gateway_rest_api.private.id
  parent_id   = aws_api_gateway_rest_api.private.root_resource_id
  path_part   = "health"
}

resource "aws_api_gateway_method" "health_get" {
  rest_api_id   = aws_api_gateway_rest_api.private.id
  resource_id   = aws_api_gateway_resource.health.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "health_lambda" {
  rest_api_id             = aws_api_gateway_rest_api.private.id
  resource_id             = aws_api_gateway_resource.health.id
  http_method             = aws_api_gateway_method.health_get.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.handler.invoke_arn
}

resource "aws_lambda_permission" "api_gateway" {
  statement_id  = "AllowPrivateApiInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.handler.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.private.execution_arn}/*/GET/health"
}
```

## 11. Execute-API endpoint

```hcl
resource "aws_vpc_endpoint" "execute_api" {
  vpc_id              = aws_vpc.main.id
  service_name        = "com.amazonaws.${var.aws_region}.execute-api"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = [for subnet in aws_subnet.private : subnet.id]
  security_group_ids  = [aws_security_group.endpoint.id]
  private_dns_enabled = true

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-execute-api-endpoint"
  })
}
```

The API association is the `vpc_endpoint_ids` value in the private REST API resource. The endpoint must have at least one subnet, preferably both private subnets, before the API can resolve private DNS.

## 12. Deployment and stage

```hcl
resource "aws_api_gateway_deployment" "private" {
  rest_api_id = aws_api_gateway_rest_api.private.id

  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.health.id,
      aws_api_gateway_method.health_get.id,
      aws_api_gateway_integration.health_lambda.id,
      aws_api_gateway_rest_api.private.policy
    ]))
  }

  lifecycle {
    create_before_destroy = true
  }

  depends_on = [aws_api_gateway_integration.health_lambda]
}

resource "aws_api_gateway_stage" "private" {
  rest_api_id   = aws_api_gateway_rest_api.private.id
  deployment_id = aws_api_gateway_deployment.private.id
  stage_name    = "sandbox"
}
```

## 13. Outputs

```hcl
output "vpc_id" {
  value = aws_vpc.main.id
}

output "private_subnet_ids" {
  value = { for az, subnet in aws_subnet.private : az => subnet.id }
}

output "ssm_endpoint_ids" {
  value = { for service, endpoint in aws_vpc_endpoint.ssm : service => endpoint.id }
}

output "execute_api_endpoint_id" {
  value = aws_vpc_endpoint.execute_api.id
}

output "instance_id" {
  value = aws_instance.ssm_client.id
}

output "lambda_function_arn" {
  value = aws_lambda_function.handler.arn
}

output "api_invoke_url" {
  value = "https://${aws_api_gateway_rest_api.private.id}.execute-api.${var.aws_region}.amazonaws.com/${aws_api_gateway_stage.private.stage_name}/health"
}
```

## 14. Validation sequence

```powershell
terraform fmt
terraform init
terraform validate
terraform plan -out lab.tfplan
terraform show lab.tfplan
terraform apply lab.tfplan
```

Verify the plan contains no public IP, NAT gateway, internet gateway, or unexpected route. After apply, open Fleet Manager, start a Session Manager session, resolve the API hostname, and call the `/health` path from the private instance.
