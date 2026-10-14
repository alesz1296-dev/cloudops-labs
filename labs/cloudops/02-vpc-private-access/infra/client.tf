resource "aws_instance" "ssm_client" {
  ami                         = var.ami_id
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.private[var.client_subnet_az].id #client subnet is the second private subnet in the list
  vpc_security_group_ids      = [aws_security_group.client.id]
  iam_instance_profile        = aws_iam_instance_profile.ssm_client.name
  associate_public_ip_address = false #instance needs to be private, so no public IP address is assigned

  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"
    http_put_response_hop_limit = 2
  }

  tags = merge(local.common_tags, {
    Name = "${local.name_prefix}-private-client"
  })
}