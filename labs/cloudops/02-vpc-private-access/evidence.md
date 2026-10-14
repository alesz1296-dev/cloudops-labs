# Evidence and completion checklist

Use this as a student worksheet. Record real IDs and timestamps privately, then sanitize the copy used for published notes.

## Preparation

- [ ] Account, region `us-east-1`, profile, prefix, and cleanup deadline recorded.
- [ ] VPC/subnet CIDRs and Availability Zones recorded.
- [ ] SSM connectivity prerequisite verified.

## Baseline

- [ ] VPC, subnet, route-table, security-group, client, endpoint, API, stage, Lambda, and log-group IDs recorded.
- [ ] Endpoint has private DNS enabled and both private subnets selected.
- [ ] DNS lookup output saved.
- [ ] Successful `curl -i` response, status, body, request ID, and timestamp saved.
- [ ] Lambda/API log event saved.

## Failure A â€” transport

- [ ] Original endpoint security-group rule captured.
- [ ] HTTPS ingress removed and one test performed.
- [ ] DNS still resolved; connection failure and timestamp recorded.
- [ ] Security groups/NACLs/flow logs inspected.
- [ ] Rule restored and successful request reproduced.

## Failure B â€” policy

- [ ] Original endpoint/API policy saved.
- [ ] One explicit deny applied and one test performed.
- [ ] Authorization-style response and API log recorded.
- [ ] Policy restored and successful request reproduced.

## Student explanation

- [ ] Explain whether each failure was DNS, transport, endpoint policy, API resource policy, or application authorization.
- [ ] Explain which observation proves recovery.
- [ ] Record the remaining billable resources before cleanup.

## Cleanup

- [ ] API, Lambda, client, endpoint, ENIs, security groups, subnets, route table, and VPC deleted in order.
- [ ] Read-only inventory shows no resources with the lab prefix.
- [ ] No NAT gateway, public IPv4, EBS volume, snapshot, or retained log group remains unexpectedly.
- [ ] Final cleanup timestamp and notes recorded.

## Student evidence: VPC, endpoints, EC2, and SSM

Record the values from your own console. Do not copy another account's IDs.

- [ ] Region confirmed: `________________`
- [ ] VPC name/ID and CIDR: `________________`
- [ ] DNS resolution and hostnames enabled: `________________`
- [ ] Private subnet IDs, AZs, and CIDRs: `________________`
- [ ] Client security-group ID and VPC ID: `________________`
- [ ] Endpoint security-group ID and VPC ID: `________________`
- [ ] Endpoint SG inbound HTTPS 443 source is the client SG: `________________`
- [ ] Client SG outbound rule: `________________`
- [ ] SSM endpoint IDs for `ssm`, `ssmmessages`, and `ec2messages`: `________________`
- [ ] All three endpoint statuses are Available: `________________`
- [ ] EC2 instance ID, private IP, subnet, and AMI/platform: `________________`
- [ ] IAM instance-profile name and attached `AmazonSSMManagedInstanceCore` policy: `________________`
- [ ] Managed-node ID and ping status after stop/start: `________________`
- [ ] Session Manager session opened successfully: `________________`

Explain how the VPC, endpoint DNS, security groups, IAM role, and SSM agent combine to provide private management without a public IP:

`______________________________________________________________________________`

## Lambda and private API evidence

- [ ] Lambda function name and ARN: `________________`
- [ ] Runtime and architecture: `________________`
- [ ] Execution-role name: `________________`
- [ ] CloudWatch log-group name: `________________`
- [ ] Handler code deployed and test event used: `________________`
- [ ] Lambda test returned HTTP status `200`: `________________`
- [ ] API Gateway type is **Private**: `________________`
- [ ] API ID, `GET /health` resource, and `sandbox` stage (the console may display it as `Sandbox`; use the exact displayed case in the invoke URL): `________________`
- [ ] API Gateway integration target and invoke permission: `________________`
- [ ] Private DNS name and successful response body: `________________`

## Completed reference run

Use these results to understand the expected evidence shape. Record your own IDs and timestamps in the blanks above.

- [x] Private EC2 registered as a Systems Manager managed node after stop/start.
- [x] Session Manager shell opened without a public IP.
- [x] Lambda direct test returned `200` with the synthetic `cloudops-02 / ok` response.
- [x] Private API resource policy saved and API redeployed to the `Sandbox` stage.
- [x] Execute-API interface endpoint had both private subnets associated and private DNS enabled.
- [x] DNS resolved the API hostname to private `10.62.x.x` addresses.
- [x] Verbose curl completed TLS and returned `HTTP/1.1 200 OK`.
- [x] Final response body was `{"lab":"cloudops-02","status":"ok"}`.

## Troubleshooting evidence to capture

For any failure, record the observation and the check that isolated it:

| Observation | Check to record | Result |
|---|---|---|
| Client SG missing from endpoint-rule selector | Compare client and endpoint VPC IDs | `________________` |
| Endpoint has no DNS entries | Check endpoint subnet associations | `________________` |
| API hostname returns NXDOMAIN | Check private DNS and API VPC endpoint association | `________________` |
| TCP 443 connection times out | Check endpoint SG attachment and HTTPS 443 source | `________________` |
| API returns 403 | Check resource policy, endpoint policy, and deployment | `________________` |
| API returns 200 | Record request ID, timestamp, and Lambda log event | `________________` |


