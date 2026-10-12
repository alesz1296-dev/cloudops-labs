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

## Failure A — transport

- [ ] Original endpoint security-group rule captured.
- [ ] HTTPS ingress removed and one test performed.
- [ ] DNS still resolved; connection failure and timestamp recorded.
- [ ] Security groups/NACLs/flow logs inspected.
- [ ] Rule restored and successful request reproduced.

## Failure B — policy

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
