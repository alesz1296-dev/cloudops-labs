resource "aws_cloudwatch_log_group" "lambda" {
  name              = local.log_group_name
  retention_in_days = var.lambda_log_retention_days

  tags = merge(local.common_tags, {
    Name = local.log_group_name
  })
}

resource "aws_lambda_function" "handler" {
  function_name = local.function_name
  description   = "CloudOps-02 synthetic private API handler"
  role          = aws_iam_role.lambda_execution.arn
  handler       = var.lambda_handler
  runtime       = var.lambda_runtime
  timeout       = var.lambda_timeout
  memory_size   = var.lambda_memory_size

  filename         = "${path.module}/${var.lambda_package_path}"
  source_code_hash = filebase64sha256("${path.module}/${var.lambda_package_path}")

  tags = merge(local.common_tags, {
    Name = local.function_name
  })

  depends_on = [
    aws_iam_role_policy_attachment.lambda_basic_execution
  ]
}

