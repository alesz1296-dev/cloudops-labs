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
  value = aws_iam_role.lambda_execution_role.name
}