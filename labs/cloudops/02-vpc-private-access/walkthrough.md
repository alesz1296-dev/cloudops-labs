# CloudOps-02 console walkthrough

Build and test a private path from an EC2 client to a private API Gateway REST API backed by Lambda. Use `us-east-1`, a unique prefix such as `cloudops-02-<suffix>`, synthetic data, and a dedicated sandbox account. Record your own IDs and timestamps in [evidence.md](evidence.md).

## 1. Confirm the design and readiness

The EC2 client has no public IPv4 address. Systems Manager manages it through three private interface endpoints. A separate `execute-api` interface endpoint carries the application request to the private API Gateway API.

Confirm permissions for VPC, EC2, IAM pass-role, Systems Manager, VPC endpoints, Lambda, API Gateway, and CloudWatch Logs. Do not add a NAT gateway, internet gateway, bastion host, or public IP to solve a connectivity problem.

## 2. Create the VPC and private subnets

1. Open **VPC → Your VPCs → Create VPC**.
2. Create a VPC named `cloudops-02-<suffix>-vpc` with CIDR `10.62.0.0/16`.
3. Enable **DNS resolution** and **DNS hostnames**.
4. Create two private subnets in different Availability Zones, for example one in `us-east-1a` and one in `us-east-1b`.
5. A wizard may allocate `/20` ranges instead of the example `/24` ranges. Record the actual CIDRs shown in the console.
6. Associate both subnets with route tables containing only the local VPC route. Do not add an internet gateway or NAT gateway.

Record the VPC ID, subnet IDs, AZs, route-table IDs, and NACL IDs.

## 3. Create security groups in the correct VPC

Create both groups in `cloudops-02-<suffix>-vpc`. Check each group’s **VPC ID** before creating references.

### Client security group

- Name: `cloudops-02-<suffix>-client`
- Inbound rules: none
- Outbound: TCP 443 to `0.0.0.0/0` or approved endpoint CIDRs

### Endpoint security group

- Name: `cloudops-02-<suffix>-endpoint`
- Inbound: **HTTPS**, TCP 443, source `cloudops-02-<suffix>-client`
- Outbound: approved return traffic, normally the default outbound rule

If the client group is missing from the source selector, the groups are probably in different VPCs. Do not enter an SG ID into an existing CIDR rule; delete the CIDR rule and create a new security-group source rule.

## 4. Create the EC2 client and IAM role

1. Open **IAM → Roles → Create role**.
2. Select the **EC2** trusted service and the **EC2 Role for AWS Systems Manager** use case.
3. Attach `AmazonSSMManagedInstanceCore`.
4. Name the role `cloudops-02-<suffix>-ssm-role` and create it.
5. In **EC2 → Launch instance**, choose a small approved AMI with the SSM Agent, the lab VPC, and one private subnet.
6. Disable public IPv4 assignment.
7. Attach the client security group and the `cloudops-02-<suffix>-ssm-role` instance profile.
8. Leave function URL, public access, and other unnecessary exposure disabled.

Record the instance ID, private IP, subnet, AMI/platform, instance profile, and role policy.

## 5. Create the three SSM interface endpoints

Create each endpoint in **VPC → Endpoints → Create endpoint**:

- `com.amazonaws.us-east-1.ssm`
- `com.amazonaws.us-east-1.ssmmessages`
- `com.amazonaws.us-east-1.ec2messages`

For each endpoint:

1. Choose **AWS services** and the exact service above.
2. Choose **Interface** endpoint type.
3. Select the lab VPC.
4. Select both private subnets.
5. Enable **Private DNS name** and choose IPv4.
6. Attach only `cloudops-02-<suffix>-endpoint`.
7. Create the endpoint and wait for **Available**.

An S3 gateway endpoint does not replace these three SSM endpoints. Record endpoint IDs, ENIs, DNS names, subnets, and security groups.

## 6. Verify Systems Manager registration

1. Open **Systems Manager → Fleet Manager** in `us-east-1`.
2. If the instance is not listed, verify all three endpoints are Available, the endpoint SG allows inbound 443 from the client SG, the client SG allows outbound 443, and the IAM role is attached.
3. Stop and start the EC2 instance after the role and endpoints are ready.
4. Wait 5–10 minutes and refresh Fleet Manager.
5. Start a **Session Manager** session and verify a shell opens.

The SSM endpoints provide private instance management; they are separate from the application endpoint created later.

## 7. Create and test the Lambda function

1. Open **Lambda → Functions → Create function**.
2. Choose **Author from scratch**.
3. Name it `cloudops-02-<suffix>-handler`.
4. Choose a supported Python 3.x runtime, such as Python 3.14 if offered.
5. Leave architecture as x86_64 and leave Durable execution, EC2 capacity provider, custom role, Function URL, VPC, code signing, KMS, and tenant isolation disabled.
6. Use the default Lambda-created execution role with basic CloudWatch Logs permissions.
7. Create the function.
8. In the **Code** tab, replace `lambda_function.py` with:

```python
import json


def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"lab": "cloudops-02", "status": "ok"})
    }
```

9. Choose **Deploy**.
10. Confirm **Runtime settings → Handler** is `lambda_function.lambda_handler`.
11. Create a test event named `cloudops-02-health-test` with `{}` and invoke it.
12. Confirm status `200` and the expected JSON body.
13. Open **Monitor → View CloudWatch logs** and confirm `START`, `END`, and `REPORT` records.

You can also upload [lambda.zip](lambda.zip), which contains the same `lambda_function.py` file.

## 8. Create and configure the private API Gateway API

1. Open **API Gateway → REST APIs → Create API**.
2. Choose **Private REST API** and name it `cloudops-02-<suffix>-private-api`.
3. Create resource `/health`.
4. Create a `GET` method using **Lambda function** integration.
5. Select the same Region and `cloudops-02-<suffix>-handler`.
6. Keep Lambda proxy integration enabled and accept the prompt to grant API Gateway permission to invoke Lambda.
7. Deploy to a stage named `sandbox`. The console may display it as `Sandbox`; use the exact case shown in the invoke URL.

### Required resource policy

A private REST API cannot be deployed without a resource policy. In **Resource policy**, save this policy with your VPC ID:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowCallsFromLabVpc",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "execute-api:Invoke",
      "Resource": "arn:aws:execute-api:us-east-1:<account-id>:<api-id>/*",
      "Condition": {
        "StringEquals": {
          "aws:SourceVpc": "vpc-xxxxxxxxxxxxxxxxx"
        }
      }
    }
  ]
}
```

Replace `<account-id>` and `<api-id>` with the values from your API ARN before saving. After the endpoint exists, you may replace `aws:SourceVpc` with `aws:SourceVpce` and the exact execute-api endpoint ID for tighter access. Redeploy the API after every policy or API setting change.

## 9. Create and associate the execute-api interface endpoint

1. In **VPC → Endpoints → Create endpoint**, choose **AWS services**.
2. Select `com.amazonaws.us-east-1.execute-api` and **Interface**.
3. Select the lab VPC, both private subnets, IPv4, and enable private DNS.
4. Attach only the endpoint security group.
5. Create the endpoint and wait for **Available**.
6. Open **Manage subnets** and verify both private subnets are selected. An endpoint with no subnet associations has no DNS entries even if its status says Available.
7. In API Gateway **API settings**, add this endpoint ID under **VPC endpoint IDs**.
8. Save the settings and redeploy the `Sandbox` stage.

## 10. Prove the private path

From a Session Manager shell on the EC2 instance, copy the exact API ID and stage URL from API Gateway **Stages**:

```bash
nslookup <api-id>.execute-api.us-east-1.amazonaws.com
curl -i https://<api-id>.execute-api.us-east-1.amazonaws.com/<Stage>/health
```

Use the exact stage casing displayed by the console. Expected result:

```text
HTTP/1.1 200
```

```json
{"lab":"cloudops-02","status":"ok"}
```

DNS should return private `10.62.x.x` addresses. If DNS returns NXDOMAIN, check endpoint subnet associations, private DNS, VPC DNS settings, and API endpoint association. If DNS resolves but TCP 443 times out, check endpoint SG attachment, inbound HTTPS 443 from the client SG, client outbound 443, and NACLs. A `403` means networking works and the policy or deployment needs inspection.

Record the request ID, timestamp, DNS output, HTTP status, response body, and Lambda/API log event.

## 11. Optional failure drills

### Security-group failure

Remove the endpoint SG’s inbound HTTPS 443 rule and run one DNS and curl test. DNS should continue to resolve while TCP connection fails. Restore the rule and prove recovery.

### Policy failure

With networking restored, add an explicit deny in the endpoint or API resource policy and run one request. Record the authorization response and logs. Restore the policy and prove the `200` baseline again. Do not combine both failure drills.

## 12. Cleanup

1. Delete the API stage and private API.
2. Delete the Lambda function and its CloudWatch log group.
3. Delete the execute-api and three SSM interface endpoints; wait for endpoint ENIs to disappear.
4. Terminate the EC2 instance.
5. Delete the instance profile and lab IAM role.
6. Delete the client and endpoint security groups.
7. Delete private subnets, route tables, and the lab VPC.
8. Confirm no lab-prefix resources, endpoint ENIs, EBS volumes, public IPs, NAT gateways, snapshots, or log groups remain.

Do not delete pre-existing Quick Setup configurations, default security groups, or resources in another VPC.

## Completed reference run

The reference run used `us-east-1`, VPC `10.62.0.0/16`, two private subnets, a private EC2 client, three Available SSM endpoints, an execute-api endpoint with both private subnets and private DNS, a Python Lambda returning status `200`, a private API with `GET /health` at stage `Sandbox`, and a final private curl returning `HTTP/1.1 200 OK` with the synthetic JSON body. Record your own IDs and timestamps in `evidence.md`.

