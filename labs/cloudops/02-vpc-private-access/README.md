# 02-vpc-private-access â€” VPC networking and private access

**Status:** Study material reviewed and expanded; no infrastructure is deployed by this repository.

This lab follows the same sequence as Lab 01: prepare, build, prove the baseline, introduce one controlled failure at a time, recover, capture evidence, and clean up.

## Purpose

This lab teaches private connectivity by building and diagnosing a path from an approved SSM client to a private API Gateway REST API through an interface VPC endpoint.

## Learning objectives

- Build a VPC with private subnets, DNS, route tables, security groups, and endpoint controls.
- Explain the difference between DNS, transport, and authorization failures.
- Use an SSM client to prove a private API path without a public IP.
- Compare stateful security groups with stateless network ACLs.
- Apply, investigate, recover, and clean up a controlled failure.

## Resources created

The lab creates a VPC, two private subnets, a local-only route table, client and endpoint security groups, an optional private SSM client, an execute-api interface endpoint, a private API Gateway REST API, a disposable Lambda integration, and CloudWatch logs. NAT gateways, internet gateways, transit gateways, and public IPs are outside the base exercise.

Use a unique prefix such as `cloudops-02-<suffix>` in every resource name.

## Objective and coverage

Build a private path from an approved client to a private API Gateway REST API through an `execute-api` interface VPC endpoint. Explain whether a failure is caused by DNS, TCP/security controls, endpoint policy, API resource policy, or application authorization.

Exam domains include VPC routing and endpoints, security groups and network ACLs, private API Gateway, IAM/resource policies, Systems Manager, observability, and safe cleanup.

## Lab package

- [Detailed Console walkthrough](walkthrough.md)
- [AWS CLI equivalent](cli-equivalent.md)
- [Terraform, file by file](terraform-guide.md)
- [Evidence and completion checklist](evidence.md)

## Prerequisites and safety

1. Complete [readiness](../../00-readiness/README.md) and use a dedicated sandbox.
2. Work in `us-east-1` with a unique prefix such as `cloudops-02-<initials>`.
3. Do not attach this lab to production networking, transit gateway, Direct Connect, corporate DNS, or shared endpoints. Use synthetic data.
4. Confirm permissions for VPC, EC2/SSM, Lambda, API Gateway, CloudWatch Logs, IAM pass-role, and VPC endpoints.
5. Decide how the private client reaches Systems Manager. If there is no approved SSM endpoint or egress path, stop at the prerequisite check; do not add NAT just to make the lab work.
6. Record CIDRs, Availability Zones, endpoint ID, API ID, stage, client ID, and cleanup deadline before provisioning.

## Target topology

```text
SSM operator -> private client subnet -> execute-api interface endpoint ENIs
             -> private API Gateway REST API (sandbox) -> disposable Lambda
```

## Build and prove

1. Create one VPC with DNS resolution and hostnames enabled, two private subnets, local-only route tables, and explicit tags.
2. Create client and endpoint security groups. Allow HTTPS from the client group to the endpoint group only. Document the default NACL before changing it.
3. Launch a disposable SSM-managed client without a public IP, or use an approved private client. Verify an SSM session before testing the API.
4. Deploy a tiny Lambda returning fixed JSON and create a **private** REST API with `GET /health` and stage `sandbox` (the console may display it as `Sandbox`; use the exact displayed case in the invoke URL).
5. Create an `execute-api` interface endpoint in both private subnets, enable private DNS, attach the endpoint security group, and record its policy.
6. Restrict endpoint and API resource policies to the intended endpoint/account/principal. Save the baseline policy.
7. From the client, resolve the API hostname and call `/health`. Record DNS, status, body, request ID, and logs.

## Failure drills

Run and restore each drill separately.

**A â€” transport failure:** remove HTTPS ingress from the endpoint security group. DNS should still resolve, but the request should fail to connect. Restore the rule and prove recovery.

**B â€” policy failure:** restore networking, then deny the endpoint or principal in the endpoint/API resource policy. The request should reach the service and return an authorization-style failure. Restore the policy and prove recovery.

Optional extension: change a NACL rule, compare its stateless return-path behavior with a stateful security group, then restore it. SNS notifications are outside this lab.

## Pass criteria

- The approved client reaches the private API.
- DNS, network reachability, and policy authorization are tested separately.
- Drill A produces a transport symptom and Drill B an authorization symptom.
- Every change is restored and the baseline is reproduced.
- Evidence records IDs, timestamps, commands, responses, logs, and cleanup verification.

## Cleanup and cost control

Delete API routes/stage, Lambda, log groups, endpoint, security groups, client, instance profile, subnets, route tables, and VPC in dependency order. Verify no endpoint ENIs, EBS volumes, public IPv4 addresses, NAT gateways, log groups, or snapshots remain. Interface endpoints, EC2, IPv4 addresses, and NAT gateways are billable.

## Review questions

- Which observation distinguishes DNS failure from blocked TCP?
- Which policy evaluated the request: endpoint, API resource, or identity policy?
- Why is a security group stateful while a NACL is stateless?
- Which identity performed each action, and where is pass-role required?
- What remained billable after cleanup, and how did you verify it?

### Why the endpoints exist

The private EC2 client has no public IPv4 address. The SSM interface endpoints (`ssm`, `ssmmessages`, and `ec2messages`) provide private Systems Manager registration and Session Manager connectivity over HTTPS/TCP 443. The separate `execute-api` interface endpoint carries the application request to the private API Gateway. SSM manages the test client; `execute-api` provides the private application path.



### Lambda deployment package

The lab includes [`lambda.zip`](lambda.zip), a minimal Python deployment package containing `lambda_function.py`. Upload the ZIP when creating or updating the function and set the handler to `lambda_function.lambda_handler`. The handler returns the synthetic response `{"lab":"cloudops-02","status":"ok"}` with HTTP status `200`.

