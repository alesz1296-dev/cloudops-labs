# Terraform section

Keep this in its own directory and state file. Do not reuse an enterprise network root or shared state.

## `versions.tf`

```hcl
terraform { required_version = ">= 1.6.0"; required_providers { aws = { source = "hashicorp/aws"; version = "~> 5.0" } } }
```

## `providers.tf`

```hcl
provider "aws" { region = var.region; profile = var.profile }
```

## `variables.tf`

```hcl
variable "profile" { type = string }
variable "region" { type = string; default = "us-east-1" }
variable "prefix" { type = string; description = "Unique learner prefix, for example cloudops-02-alex." }
variable "vpc_cidr" { type = string; default = "10.62.0.0/16" }
variable "availability_zones" { type = list(string); default = ["us-east-1a", "us-east-1b"] }
```

## `locals.tf`

```hcl
locals { common_tags = { Lab = "cloudops-02", ManagedBy = "terraform", NamePrefix = var.prefix } }
```

## `network.tf`

Create the VPC with DNS enabled, two private subnets, one local-only route table, and associations. Add tags from `local.common_tags`. Keep internet gateways and NAT out of the base plan.

## `security.tf`

Create client and endpoint security groups. The endpoint group allows TCP 443 from the client group. Keep the rule as a separate resource so the failure drill can remove and restore it safely.

## `endpoint.tf`

Create `aws_vpc_endpoint` with `vpc_endpoint_type = "Interface"`, service `com.amazonaws.${var.region}.execute-api`, both subnet IDs, endpoint security group IDs, `private_dns_enabled = true`, and an explicit policy document.

## `api.tf`

Define the disposable Lambda, its execution role, a private `aws_api_gateway_rest_api` with `endpoint_configuration { types = ["PRIVATE"]; vpc_endpoint_ids = [aws_vpc_endpoint.execute_api.id] }`, `/health` GET method, Lambda integration, deployment, and `sandbox` stage (the console may display it as `Sandbox`; use the exact displayed case in the invoke URL). Add an API resource policy restricted to the lab endpoint/account.

## `client.tf` (optional)

Define a small private EC2 instance, instance profile, and SSM role only if the sandbox already supports the required SSM connectivity. Do not add NAT implicitly.

## `outputs.tf`

Output VPC ID, subnet IDs, security-group IDs, endpoint ID, API ID, stage URL, Lambda name, and log-group name. These outputs are the IDs to record in `evidence.md`.

## `terraform.tfvars.example`

```hcl
profile = "YOUR_PROFILE"
region  = "us-east-1"
prefix  = "cloudops-02-alex"
```

## Ordered commands

```powershell
terraform init
terraform fmt -recursive
terraform validate
terraform plan -out tfplan
terraform show tfplan
terraform apply tfplan
terraform output
terraform plan -destroy -out destroy.tfplan
terraform show destroy.tfplan
terraform apply destroy.tfplan
```

Review the plan for public IPs, NAT gateways, unexpected route targets, broad policies, and resources outside the prefix before applying. Terraform plan does not change AWS; apply only the reviewed plan. Keep the generated state and plan files private. Use the same two failure drills after the baseline apply, then restore the Terraform baseline and destroy it.



## Remaining Terraform implementation plan

The next session should implement and validate these resource layers in dependency order:

### 7. IAM

- EC2 trust role
- `AmazonSSMManagedInstanceCore` policy attachment
- EC2 instance profile

### 8. SSM interface endpoints

Create Interface VPC endpoints in both private subnets with private DNS enabled and the endpoint security group:

- `com.amazonaws.us-east-1.ssm`
- `com.amazonaws.us-east-1.ssmmessages`
- `com.amazonaws.us-east-1.ec2messages`

### 9. EC2 client

- Approved AMI variable
- Private subnet ID
- Client security group
- EC2 instance profile
- No public IP address
- IMDSv2 required

### 10. Lambda

- Least-privilege execution role with CloudWatch Logs permissions
- Function using `lambda_function.lambda_handler`
- CloudWatch log group
- Synthetic `cloudops-02 / ok` response

### 11. Private API Gateway

- Private REST API
- Resource policy restricted to the lab VPC or endpoint
- `/health` resource
- `GET` method
- Lambda proxy integration
- Deployment and stage

### 12. Execute-API interface endpoint

- `com.amazonaws.us-east-1.execute-api`
- Both private subnets
- Endpoint security group
- Private DNS enabled

### 13. API endpoint association

Add the execute-api endpoint ID to the private API's `vpc_endpoint_ids` configuration. Save the API settings and redeploy after changes.

### 14. Outputs and validation

Output the VPC, subnet, route-table, security-group, IAM, endpoint, EC2, Lambda, API, stage, and log-group identifiers. Validate Fleet Manager registration, private DNS resolution, TLS connectivity, and the expected HTTP 200 response before running failure drills.
