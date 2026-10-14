output "vpc_id" {
  description = "Lab VPC ID."
  value       = aws_vpc.main.id
}

output "private_subnet_ids" {
  description = "Private subnet IDs keyed by Availability Zone."
  value       = { for az, subnet in aws_subnet.private : az => subnet.id }
}

output "private_route_table_id" {
  description = "Private route table ID."
  value       = aws_route_table.private.id
}

output "client_security_group_id" {
  description = "Client security group ID."
  value       = aws_security_group.client.id
}

output "endpoint_security_group_id" {
  description = "Interface endpoint security group ID."
  value       = aws_security_group.endpoint.id
}

output "ssm_role_name" {
  description = "EC2 Systems Manager IAM role name."
  value       = aws_iam_role.ssm_client.name
}

output "ssm_instance_profile_name" {
  description = "EC2 Systems Manager instance profile name."
  value       = aws_iam_instance_profile.ssm_client.name
}

output "instance_id" {
  description = "Private EC2 client instance ID."
  value       = aws_instance.ssm_client.id
}

output "instance_private_ip" {
  description = "Private IP address of the EC2 client."
  value       = aws_instance.ssm_client.private_ip
}

output "ssm_endpoint_ids" {
  description = "SSM interface endpoint IDs keyed by service suffix."
  value       = { for service, endpoint in aws_vpc_endpoint.ssm_services : service => endpoint.id }
}

output "execute_api_endpoint_id" {
  description = "Execute-API interface endpoint ID."
  value       = aws_vpc_endpoint.execute_api.id
}

output "lambda_function_name" {
  description = "Lambda function name."
  value       = aws_lambda_function.handler.function_name
}

output "lambda_function_arn" {
  description = "Lambda function ARN."
  value       = aws_lambda_function.handler.arn
}

output "lambda_log_group_name" {
  description = "Lambda CloudWatch log group name."
  value       = aws_cloudwatch_log_group.lambda.name
}

output "api_id" {
  description = "Private API Gateway REST API ID."
  value       = aws_api_gateway_rest_api.private.id
}

output "api_stage_name" {
  description = "Private API Gateway stage name."
  value       = aws_api_gateway_stage.private.stage_name
}

output "api_invoke_url" {
  description = "Private API Gateway invoke URL."
  value       = "https://${aws_api_gateway_rest_api.private.id}.execute-api.${var.aws_region}.amazonaws.com/${aws_api_gateway_stage.private.stage_name}"
}
