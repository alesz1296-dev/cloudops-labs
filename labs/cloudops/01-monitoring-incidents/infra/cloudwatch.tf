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