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

Define the disposable Lambda, its execution role, a private `aws_api_gateway_rest_api` with `endpoint_configuration { types = ["PRIVATE"]; vpc_endpoint_ids = [aws_vpc_endpoint.execute_api.id] }`, `/health` GET method, Lambda integration, deployment, and `sandbox` stage. Add an API resource policy restricted to the lab endpoint/account.

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
