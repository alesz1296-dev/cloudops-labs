resource "aws_vpc_endpoint" "ssm_services" {
  for_each = local.ssm_endpoint_services

  vpc_id              = aws_vpc.main.id
  service_name        = "com.amazonaws.${var.aws_region}.${each.key}"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = [for subnet in aws_subnet.private : subnet.id]
  security_group_ids  = [aws_security_group.endpoint.id]
  private_dns_enabled = true

  tags = merge(local.common_tags, {
    Name    = "${local.name_prefix}-${each.key}-endpoint"
    Service = each.key
  })
}
resource "aws_vpc_endpoint" "execute_api" {
  vpc_id              = aws_vpc.main.id
  service_name        = "com.amazonaws.${var.aws_region}.execute-api"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = [for subnet in aws_subnet.private : subnet.id]
  security_group_ids  = [aws_security_group.endpoint.id]
  private_dns_enabled = true

  tags = merge(local.common_tags, {
    Name    = "${local.name_prefix}-execute-api-endpoint"
    Service = "execute-api"
  })
}
