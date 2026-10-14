resource "aws_security_group" "client" {
  name        = "${local.name_prefix}-client"
  description = "Security group for the private EC2 client"
  vpc_id      = aws_vpc.main.id

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-client"
  })
}

resource "aws_vpc_security_group_egress_rule" "client_https" {
  security_group_id = aws_security_group.client.id
  ip_protocol       = "tcp"
  from_port         = var.https_port
  to_port           = var.https_port
  cidr_ipv4         = var.client_egress_cidr
  description       = "HTTPS egress from EC2 client to private interface endpoints"
}

resource "aws_security_group" "endpoint" {
  name        = "${local.name_prefix}-endpoint"
  description = "Security group for VPC interface endpoints"
  vpc_id      = aws_vpc.main.id

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-endpoint"
  })
}

resource "aws_vpc_security_group_ingress_rule" "endpoint_https" {
  security_group_id            = aws_security_group.endpoint.id
  referenced_security_group_id = aws_security_group.client.id
  ip_protocol                  = var.protocol
  from_port                    = var.https_port
  to_port                      = var.https_port
  description                  = "HTTPS ingress from the private EC2 client"
}

resource "aws_vpc_security_group_egress_rule" "endpoint" {
  security_group_id = aws_security_group.endpoint.id
  ip_protocol       = var.endpoint_egress_protocol
  cidr_ipv4         = var.endpoint_egress_cidr
  description       = "Endpoint egress within the lab VPC"
}