locals {
  log_group_name    = "/aws/lambda/${var.function_name}"
  role_name         = "${var.function_name}-execution-role"
  alarm_name        = "${var.function_name}-error-alarm"
  source_file       = "${path.module}/../src/lambda_function.py"
  retention_in_days = 1
}