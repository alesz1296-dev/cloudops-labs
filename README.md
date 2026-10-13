# AWS CloudOps Certification Labs

Hands-on study labs for AWS CloudOps engineering scenarios. Each lab is designed to be completed in a dedicated nonproduction sandbox using synthetic data.

## Study approach

Complete each lab in this order:

1. Read the lab purpose, objectives, prerequisites, and resource cheat sheet.
2. Complete the AWS Console walkthrough.
3. Repeat the scenario with the AWS CLI equivalent.
4. Repeat it with Terraform when a Terraform guide is provided.
5. Perform the failure or troubleshooting drill.
6. Record evidence and explain the observed behavior.
7. Delete the resources and verify cleanup.

Every lab should use a unique suffix, such as `alex`, in resource names. Do not use production accounts, shared VPCs, shared Terraform state, or real customer data.

## Lab catalog

| Lab | Scenario | Main topics |
|---|---|---|
| 01 | Monitoring and incident response | Lambda, CloudWatch Logs, dashboards, alarms, recovery |
| 02 | VPC private access | Private subnets, interface endpoints, private API Gateway, DNS, policies |
| 03 | EC2, ALB, and Auto Scaling | Compute, load balancing, health checks, scaling |
| 04 | Backup and restore | AWS Backup, snapshots, recovery verification |
| 05 | Security audit | IAM, CloudTrail, Config, findings, remediation |
| 06 | CloudFormation automation | Stacks, parameters, drift, rollback |
| 07 | DNS and CloudFront | Route 53, records, distributions, caching, invalidation |
| 08 | RDS and storage recovery | RDS, EBS, S3, snapshots, restore procedures |
| 09 | Container images | ECR, ECS or related image workflows, deployment troubleshooting |
| 10 | Multi-account operations | Organizations, CDK, StackSets, account boundaries |
| 11 | Advanced monitoring | Composite signals, dashboards, Logs Insights, operational response |
| 12 | Storage and database performance | Metrics, bottlenecks, scaling, tuning |
| 13 | Automated disaster recovery | Recovery objectives, replication, failover, validation |
| 14 | Advanced networking and DNS | Transit routing, Route 53 Resolver, hybrid DNS |
| 15 | Security findings remediation | Security Hub, Inspector, GuardDuty, remediation workflows |

## Repository layout

```text
labs/cloudops/
  README.md
  01-monitoring-incidents/
  02-vpc-private-access/
  03-ec2-alb-autoscaling/
  ...
```

A detailed lab can contain:

```text
README.md             Purpose, objectives, scope, and pass criteria
walkthrough.md        AWS Console procedure
cli-equivalent.md     AWS CLI or PowerShell repeat
terraform-guide.md    Terraform files and commands
evidence.md           Student evidence worksheet
visual-guide.md       Visual sequence or evidence notes
src/                  Local application or Lambda source
tests/                Local tests
events/               Safe sample events
```

## Safety and security

- Use a dedicated sandbox account in the documented Region.
- Use temporary credentials, IAM Identity Center, or an approved AWS CLI profile.
- Never commit access keys, secret keys, passwords, tokens, private keys, real email addresses, or subscription tokens.
- Never commit Terraform state, plan files, local `.tfvars`, generated ZIP packages, `.terraform/`, or credentials.
- Sanitize account IDs, ARNs, request IDs, instance IDs, endpoint IDs, and timestamps before publishing evidence.
- Review `terraform plan` before every apply.
- Use `terraform plan -destroy` and review the destroy plan before cleanup.
- Do not use wildcard deletion in shared accounts.

## Cost control

Run only the resources required for the exercise. Set a budget alert, record a cleanup deadline, and delete dashboards, alarms, log groups, endpoints, NAT gateways, instances, volumes, snapshots, and other billable resources when finished. Confirm cleanup with read-only Console or CLI queries.

## Validation before commit

From the repository root:

```powershell
git status
Get-ChildItem -Path labs -Recurse -File
Get-ChildItem -Path labs -Recurse -File | Select-String -Pattern "AKIA|aws_secret|secret_access_key|password|BEGIN PRIVATE KEY|terraform.tfstate"
git diff --check
```

Expected sensitive-file checks should be empty except for intentional placeholders such as `YOUR_ACCOUNT_ID` or `YOUR_PROFILE`.

## License and purpose

This repository is intended for personal AWS certification study and controlled sandbox practice. Review every command for account, Region, resource prefix, and cost impact before running it.
