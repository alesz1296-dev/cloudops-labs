# AWS CLI equivalent (PowerShell)

Run from an approved workstation. Replace placeholders; never put credentials in this file. The commands create the network and endpoint. API Gateway/Lambda commands should reuse the tested packaging pattern from Lab 01 and must use the IDs printed by these queries.

## 1. Variables and identity

```powershell
$Profile = "YOUR_PROFILE"
$Region = "us-east-1"
$Prefix = "cloudops-02-alex"
$VpcCidr = "10.62.0.0/16"
$SubnetA = "10.62.1.0/24"
$SubnetB = "10.62.2.0/24"
$AzA = "us-east-1a"
$AzB = "us-east-1b"
$AccountId = aws sts get-caller-identity --profile $Profile --query Account --output text
aws sts get-caller-identity --profile $Profile --region $Region
```

## 2. VPC, subnets, and route table

```powershell
$VpcId = aws ec2 create-vpc --cidr-block $VpcCidr --tag-specifications "ResourceType=vpc,Tags=[{Key=Name,Value=$Prefix-vpc}]" --profile $Profile --region $Region --query Vpc.VpcId --output text
aws ec2 modify-vpc-attribute --vpc-id $VpcId --enable-dns-support '{"Value":true}' --profile $Profile --region $Region
aws ec2 modify-vpc-attribute --vpc-id $VpcId --enable-dns-hostnames '{"Value":true}' --profile $Profile --region $Region
$SubnetIdA = aws ec2 create-subnet --vpc-id $VpcId --cidr-block $SubnetA --availability-zone $AzA --tag-specifications "ResourceType=subnet,Tags=[{Key=Name,Value=$Prefix-a}]" --profile $Profile --region $Region --query Subnet.SubnetId --output text
$SubnetIdB = aws ec2 create-subnet --vpc-id $VpcId --cidr-block $SubnetB --availability-zone $AzB --tag-specifications "ResourceType=subnet,Tags=[{Key=Name,Value=$Prefix-b}]" --profile $Profile --region $Region --query Subnet.SubnetId --output text
$RouteTableId = aws ec2 create-route-table --vpc-id $VpcId --tag-specifications "ResourceType=route-table,Tags=[{Key=Name,Value=$Prefix-private}]" --profile $Profile --region $Region --query RouteTable.RouteTableId --output text
aws ec2 associate-route-table --route-table-id $RouteTableId --subnet-id $SubnetIdA --profile $Profile --region $Region
aws ec2 associate-route-table --route-table-id $RouteTableId --subnet-id $SubnetIdB --profile $Profile --region $Region
```

## 3. Security groups and endpoint

```powershell
$ClientSg = aws ec2 create-security-group --group-name "$Prefix-client" --description "CloudOps 02 client" --vpc-id $VpcId --profile $Profile --region $Region --query GroupId --output text
$EndpointSg = aws ec2 create-security-group --group-name "$Prefix-endpoint" --description "CloudOps 02 endpoint" --vpc-id $VpcId --profile $Profile --region $Region --query GroupId --output text
aws ec2 authorize-security-group-ingress --group-id $EndpointSg --protocol tcp --port 443 --source-group $ClientSg --profile $Profile --region $Region
$EndpointId = aws ec2 create-vpc-endpoint --vpc-id $VpcId --vpc-endpoint-type Interface --service-name "com.amazonaws.$Region.execute-api" --subnet-ids $SubnetIdA $SubnetIdB --security-group-ids $EndpointSg --private-dns-enabled --tag-specifications "ResourceType=vpc-endpoint,Tags=[{Key=Name,Value=$Prefix-execute-api}]" --profile $Profile --region $Region --query VpcEndpoint.VpcEndpointId --output text
aws ec2 describe-vpc-endpoints --vpc-endpoint-ids $EndpointId --profile $Profile --region $Region
```

Create the private API and Lambda using the Console first, then substitute the API ID, stage, endpoint ID, and Lambda integration values in your saved commands. This prevents accidentally publishing a public API while learning the network path.

## 4. Failure and restore commands

```powershell
aws ec2 revoke-security-group-ingress --group-id $EndpointSg --protocol tcp --port 443 --source-group $ClientSg --profile $Profile --region $Region
# run the SSM DNS/curl test once, then restore:
aws ec2 authorize-security-group-ingress --group-id $EndpointSg --protocol tcp --port 443 --source-group $ClientSg --profile $Profile --region $Region
aws ec2 modify-vpc-endpoint --vpc-endpoint-id $EndpointId --policy-document file://allow-policy.json --profile $Profile --region $Region
```

For the policy drill, save `allow-policy.json`, apply a separate deny policy, test once, and restore the saved file. Inspect endpoint, API, and CloudWatch logs before changing another layer.

## 5. Read-only verification and cleanup

```powershell
aws ec2 describe-vpcs --filters "Name=tag:Name,Values=$Prefix-*" --profile $Profile --region $Region
aws ec2 describe-vpc-endpoints --filters "Name=vpc-id,Values=$VpcId" --profile $Profile --region $Region
# After deleting API/Lambda/client and dependencies:
aws ec2 describe-network-interfaces --filters "Name=tag:Name,Values=$Prefix-*" --profile $Profile --region $Region
```

Delete only IDs recorded for this prefix and follow the dependency order in the walkthrough. Do not use a wildcard delete against a shared VPC.
