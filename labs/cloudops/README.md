# CloudOps Engineer Associate track

Complete [readiness](../00-readiness/README.md) first. Each scenario has its own resource boundary and cleanup checklist. Start with [CloudOps-01's Console walkthrough](01-monitoring-incidents/walkthrough.md), which includes a locally tested fixture. Remaining implementations will be added one scenario at a time.

| Scenario | Topic | Exam domains |
| --- | --- | --- |
| [01-monitoring-incidents](01-monitoring-incidents/README.md) | Monitoring, alarms, and incident response | Monitoring and optimization |
| [02-vpc-private-access](02-vpc-private-access/README.md) | VPC networking and private access | Networking and content delivery; Security |
| [03-ec2-alb-autoscaling](03-ec2-alb-autoscaling/README.md) | EC2, load balancing, and Auto Scaling | Reliability; Deployment; Monitoring |
| [04-backup-restore](04-backup-restore/README.md) | Backups, restore, and recovery objectives | Reliability and business continuity |
| [05-security-audit](05-security-audit/README.md) | Audit, compliance checks, and remediation | Security and compliance; Monitoring |
| [06-cloudformation-automation](06-cloudformation-automation/README.md) | CloudFormation, drift, and operational automation | Deployment, provisioning, and automation |
| [07-dns-cloudfront](07-dns-cloudfront/README.md) | DNS, TLS, and content delivery | Networking and content delivery; Monitoring |
| [08-rds-storage-recovery](08-rds-storage-recovery/README.md) | RDS, EBS, and storage operations | Reliability; Monitoring; Security |
| [09-containers-images](09-containers-images/README.md) | ECS, ECR, AMIs, and image operations | Deployment; Monitoring; Reliability |
| [10-multi-account-cdk-stacksets](10-multi-account-cdk-stacksets/README.md) | Organizations, SCPs, CDK, StackSets, and sharing | Security; Deployment |
| [11-advanced-monitoring](11-advanced-monitoring/README.md) | CloudWatch agent, composite alarms, and shared visibility | Monitoring; Automation |
| [12-storage-database-performance](12-storage-database-performance/README.md) | Storage, caching, and database performance | Monitoring and optimization; Reliability |
| [13-automated-disaster-recovery](13-automated-disaster-recovery/README.md) | AWS Backup and cross-Region disaster recovery | Reliability and business continuity; Automation |
| [14-advanced-networking-dns](14-advanced-networking-dns/README.md) | Multi-VPC, IPv6, DNS, and network protection | Networking and content delivery; Security |
| [15-security-findings-remediation](15-security-findings-remediation/README.md) | Security findings, access analysis, and compliance | Security and compliance; Automation |

See [the gap coverage map](../coverage.md) for missing-topic mappings and [extension tasks](../extensions.md) for existing labs.

## How to study

Start in order; reuse a previous lab's resources only when dependencies and ownership are documented. Later labs may use a tiny standalone fixture instead. Build first, then introduce one failure at a time and restore the baseline after each drill. Save sanitized evidence and repeat without step-by-step guidance.

Before implementation, write reviewable specifications and acceptance criteria as described in [the lab guide](../README.md). Confirm language, account configuration, and scenario-specific networking or domain prerequisites at that point.

