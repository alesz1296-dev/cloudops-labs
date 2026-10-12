# CloudOps 01 Terraform implementation

This is a separate sandbox implementation of CloudOps-01. It does not use or modify the enterprise `infra/` root. Use a dedicated directory and state for this lab, a nonproduction account, and `us-east-1`.

The files below are shown in the order to create them. Terraform provisions the resources; the AWS CLI or Console still performs the runtime failure and recovery drill.

## 1. Directory layout

Create this layout from the repository root:

```text
labs/cloudops/01-monitoring-incidents/terraform/
  versions.tf
  providers.tf
  variables.tf
  locals.tf
  iam.tf
  logs.tf
  lambda.tf
  cloudwatch.tf
  outputs.tf
  terraform.tfvars.example
```

The Lambda source remains here:

```text
labs/cloudops/01-monitoring-incidents/src/lambda_function.py
```

## 2. `versions.tf`

Create `terraform/versions.tf`:

```hcl
terraform {
  required_version = ">= 1.9.0, < 2.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.4"
    }
  }
}
```

## 3. `providers.tf`

Create `terraform/providers.tf`:

```hcl
provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = var.project_name
      Track       = "CloudOps"
      Lab         = "cloudops-01-monitoring"
      Environment = var.environment
      ManagedBy   = "Terraform"
      Owner       = var.owner
    }
  }
}
```

The AWS provider uses the credentials selected by your AWS CLI profile or IAM Identity Center session. Do not add access keys to Terraform files.

## 4. `variables.tf`

Create `terraform/variables.tf`:

```hcl
variable "aws_region" {
  type        = string
  description = "AWS Region for the lab."
  default     = "us-east-1"
}

variable "project_name" {
  type        = string
  description = "Stable project name."
  default     = "content-failures-api"
}

variable "environment" {
  type        = string
  description = "Sandbox environment label."
  default     = "sandbox"

  validation {
    condition     = contains(["sandbox", "test"], var.environment)
    error_message = "Use sandbox or test for this exercise."
  }
}

variable "owner" {
  type        = string
  description = "Person responsible for cleanup."
}

variable "name_suffix" {
  type        = string
  description = "Unique lowercase learner suffix."
}

variable "function_name" {
  type        = string
  description = "Lambda function name."
  default     = "cloudops-01-monitoring-${var.name_suffix}"
}
```

## 5. `locals.tf`

Create `terraform/locals.tf`:

```hcl
locals {
  log_group_name = "/aws/lambda/${var.function_name}"
  role_name      = "${var.function_name}-execution-role"
  alarm_name     = "${var.function_name}-errors"
  source_file    = "${path.module}/../src/lambda_function.py"
}
```

## 6. `iam.tf`

Create `terraform/iam.tf`:

```hcl
resource "aws_iam_role" "lambda" {
  name = local.role_name

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy" "lambda_logs" {
  name = "${var.function_name}-logging"
  role = aws_iam_role.lambda.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ]
      Resource = "${aws_cloudwatch_log_group.lambda.arn}:*"
    }]
  })
}
```

The policy intentionally omits `logs:CreateLogGroup` because Terraform creates the group first.

## 7. `logs.tf`

Create `terraform/logs.tf`:

```hcl
resource "aws_cloudwatch_log_group" "lambda" {
  name              = local.log_group_name
  retention_in_days = 1
}
```

## 8. `lambda.tf`

Create `terraform/lambda.tf`:

```hcl
data "archive_file" "lambda" {
  type        = "zip"
  source_file = local.source_file
  output_path = "${path.module}/lambda.zip"
}

resource "aws_lambda_function" "monitoring" {
  function_name    = var.function_name
  role             = aws_iam_role.lambda.arn
  runtime          = "python3.12"
  handler          = "lambda_function.lambda_handler"
  filename         = data.archive_file.lambda.output_path
  source_code_hash = data.archive_file.lambda.output_base64sha256
  memory_size     = 128
  timeout         = 3

  depends_on = [aws_cloudwatch_log_group.lambda]
}
```

If the AWS Console shows a different currently supported Python runtime, use that runtime consistently in the plan and record the choice.

## 9. `cloudwatch.tf`

Create `terraform/cloudwatch.tf`:

```hcl
resource "aws_cloudwatch_metric_alarm" "errors" {
  alarm_name          = local.alarm_name
  alarm_description   = "Lambda errors for the CloudOps-01 monitoring lab."
  namespace           = "AWS/Lambda"
  metric_name         = "Errors"
  dimensions          = { FunctionName = aws_lambda_function.monitoring.function_name }
  statistic           = "Sum"
  period              = 60
  evaluation_periods  = 1
  datapoints_to_alarm = 1
  threshold           = 1
  comparison_operator = "GreaterThanOrEqualToThreshold"
  treat_missing_data  = "notBreaching"
}
```

The metric name is `Errors`. The alarm name is `cloudops-01-monitoring-errors`; they are different values.

## Optional SNS notification extension

SNS is optional and outside the core Terraform baseline. Add these resources only when practicing alarm notifications:

```hcl
variable "enable_sns" {
  type    = bool
  default = false
}

resource "aws_sns_topic" "alerts" {
  count = var.enable_sns ? 1 : 0
  name  = "${var.function_name}-alerts"
}

variable "notification_email" {
  type      = string
  default   = null
  sensitive = true
}

resource "aws_sns_topic_subscription" "email" {
  count     = var.enable_sns && var.notification_email != null ? 1 : 0
  topic_arn = aws_sns_topic.alerts[0].arn
  protocol  = "email"
  endpoint  = var.notification_email
}
```

Add the topic ARN to `alarm_actions` only when enabled:

```hcl
alarm_actions = var.enable_sns ? [aws_sns_topic.alerts[0].arn] : []
```

Confirm the subscription from the email before expecting notifications. Do not commit the email address or subscription details. Destroy the subscription and topic during cleanup.

## 10. `outputs.tf`

Create `terraform/outputs.tf`:

```hcl
output "function_name" {
  value = aws_lambda_function.monitoring.function_name
}

output "function_arn" {
  value = aws_lambda_function.monitoring.arn
}

output "log_group_name" {
  value = aws_cloudwatch_log_group.lambda.name
}

output "alarm_name" {
  value = aws_cloudwatch_metric_alarm.errors.alarm_name
}

output "execution_role_name" {
  value = aws_iam_role.lambda.name
}
```

## 11. `terraform.tfvars.example`

Create `terraform/terraform.tfvars.example`:

```hcl
aws_region   = "us-east-1"
project_name = "content-failures-api"
environment  = "sandbox"
owner        = "YOUR_NAME"
name_suffix  = "yourname"
```

Copy it to a local `terraform.tfvars`, replace `YOUR_NAME`, and do not commit the local file if it contains personal or account-specific values.

## 12. Initialize and validate

From `labs/cloudops/01-monitoring-incidents/terraform`:

```powershell
Copy-Item terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars and replace YOUR_NAME.

terraform init
terraform fmt -check
terraform validate
terraform plan -out cloudops-01.tfplan
```

Review the plan. Verify the account, Region, names, IAM policy, log retention, alarm metric, and resource count before applying.

## 13. Apply and perform the runtime drill

Apply only after reviewing the sandbox plan:

```powershell
terraform apply cloudops-01.tfplan
terraform output
```

Use the [AWS CLI equivalent](cli-equivalent.md) to invoke `fail=true`, confirm `ALARM`, invoke `fail=false`, and confirm `OK`. Terraform does not replace runtime failure testing.

## 14. Destroy and verify cleanup

```powershell
terraform plan -destroy -out cloudops-01-destroy.tfplan
terraform apply cloudops-01-destroy.tfplan
```

Confirm the plan contains only this lab's resources. Verify that the Lambda, log group, alarm, role, policy, and generated `lambda.zip` are removed as intended. Never commit `.terraform`, `terraform.tfstate`, `terraform.tfstate.backup`, `terraform.tfvars`, credentials, or secrets.
