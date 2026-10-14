data "aws_caller_identity" "current" {}

data "aws_iam_policy_document" "private_api" {
  statement {
    sid    = "AllowCallsFromLabVpc"
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
resource "aws_api_gateway_rest_api" "private" {
  name        = "${local.name_prefix}-private-api"
  description = "CloudOps-02 private REST API"

  endpoint_configuration {
    types            = ["PRIVATE"]
    vpc_endpoint_ids = [aws_vpc_endpoint.execute_api.id]
  }

  policy = data.aws_iam_policy_document.private_api.json

  tags = local.common_tags
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

  depends_on = [
    aws_api_gateway_integration.health_lambda
  ]
}

resource "aws_api_gateway_stage" "private" {
  rest_api_id   = aws_api_gateway_rest_api.private.id
  deployment_id = aws_api_gateway_deployment.private.id
  stage_name    = var.api_stage_name

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-${var.api_stage_name}"
  })
}
