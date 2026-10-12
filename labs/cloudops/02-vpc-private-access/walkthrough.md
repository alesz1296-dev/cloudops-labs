# Console walkthrough

Use `us-east-1` and a unique prefix such as `cloudops-02-alex`. Record every ID in [evidence.md](evidence.md).

## 1. Prepare

Confirm the sandbox account, region, permissions, cleanup deadline, and approved SSM connectivity. Do not use a production or shared VPC.

## 2. Create the network

In **VPC → Your VPCs**, create VPC `10.62.0.0/16`; enable DNS resolution and DNS hostnames. Create two private subnets, for example `10.62.1.0/24` and `10.62.2.0/24`, in different Availability Zones. Associate a route table containing only the local VPC route. Do not create an internet gateway or NAT gateway for the base exercise.

Create `cloudops-02-client` and `cloudops-02-endpoint` security groups. Allow TCP 443 inbound to the endpoint group only from the client group. Keep outbound rules explicit and record the initial NACL rules.

## 3. Prepare the private client

Launch a small private EC2 instance with no public IPv4 address and an instance profile containing `AmazonSSMManagedInstanceCore`, or use an already-approved private SSM client. Verify **Systems Manager → Session Manager → Start session** works before continuing. If it does not, fix the approved SSM path first; do not add an unplanned NAT gateway.

## 4. Create the private API

Create a disposable Lambda that returns `{"lab":"cloudops-02","status":"ok"}`. In **API Gateway → REST APIs**, create a **Private** API, add `GET /health`, integrate it with the Lambda, deploy stage `sandbox`, and enable execution/access logging if available. Add a resource policy that permits the intended account or VPC endpoint. Record the API ID, stage URL, Lambda name, and log group.

## 5. Create the interface endpoint

In **VPC → Endpoints**, create an endpoint for AWS service `com.amazonaws.us-east-1.execute-api`, type **Interface**. Select the lab VPC, both private subnets, the endpoint security group, and **Enable DNS name**. Start with an allow policy limited to the lab account/endpoint. Record endpoint ID, ENIs, private DNS name, and policy JSON.

## 6. Prove the baseline

Open an SSM session. Resolve the private API hostname with `nslookup` or `getent hosts`, then call the `/health` URL with `curl -i`. Save the DNS result, HTTP status, body, request ID, timestamp, and CloudWatch log event. A successful response proves the complete path, not just that the API exists.

## 7. Failure A: security group

Remove the endpoint group's inbound TCP 443 rule. Run the same DNS and `curl` checks once. DNS should continue to resolve while the HTTPS connection fails. Inspect the client and endpoint security groups, NACLs, and (if enabled) flow logs. Restore the rule and repeat the request until it succeeds.

## 8. Failure B: policy

With networking restored, add an explicit deny for the endpoint or principal in the endpoint policy or API resource policy. Run the request once and record the authorization-style response and API logs. Restore the policy and prove the baseline again. Never combine this change with the security-group drill.

## 9. Cleanup

Delete API method/stage/API, Lambda and its log group, VPC endpoint, endpoint ENIs/security groups, client instance/profile, subnets, route table, and VPC. Verify no resources with the prefix remain and record the final read-only inventory.
