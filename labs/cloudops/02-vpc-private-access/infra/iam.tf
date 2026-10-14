#IAM Role and Policy for EC2 Instance to communicate with Systems Manager
data "aws_iam_policy_document" "ec2_assume_role" {
  statement {
    sid     = "EC2AssumeRole"
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "ssm_client" {
  name               = local.ssm_role_name
  assume_role_policy = data.aws_iam_policy_document.ec2_assume_role.json

  tags = merge(local.common_tags, {
    Name = local.ssm_role_name
  })
}

resource "aws_iam_role_policy_attachment" "ssm_client" {
  role       = aws_iam_role.ssm_client.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore" #AmazonSSMManagedInstanceCore allows the EC2 instance to communicate with the Systems Manager service. This policy is required for the EC2 instance to be managed by Systems Manager and to use features such as Session Manager, Run Command, and Patch Manager.
}


resource "aws_iam_instance_profile" "ssm_client" {
  name = local.ssm_role_name
  role = aws_iam_role.ssm_client.name

  tags = merge(local.common_tags, {
    Name = local.ssm_role_name
  })
}

#Lambda IAM Role and Policy
data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    sid     = "LambdaAssumeRole"
    effect  = "Allow"
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "lambda_execution" {
  name               = local.lambda_role_name
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json

  tags = merge(local.common_tags, {
    Name = local.lambda_role_name
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

