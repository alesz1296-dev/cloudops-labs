data "archive_file" "lambda" {
  type        = "zip"
  source_file = local.source_file
  output_path = "${path.module}/lambda.zip"
}

resource "aws_lambda_function" "monitoring" {
  function_name    = var.function_name
  role             = aws_iam_role.lambda_execution_role.arn
  runtime          = "python3.12"
  handler          = "lambda_function.lambda_handler"
  filename         = data.archive_file.lambda.output_path
  source_code_hash = data.archive_file.lambda.output_base64sha256
  memory_size      = 128
  timeout          = 3
  depends_on       = [aws_cloudwatch_log_group.lambda]
}