# AWS CLI equivalent

This section repeats the Console exercise from PowerShell. Use a dedicated sandbox profile and `us-east-1`. Do not paste credentials into files.

## 1. Configure and verify the profile

Run the interactive setup once:

```powershell
aws configure sso
aws sso login --profile YOUR_PROFILE
aws sts get-caller-identity --profile YOUR_PROFILE
```

Set session variables:

```powershell
$Profile = "YOUR_PROFILE"
$Region = "us-east-1"
$Suffix = "yourname"
$FunctionName = "cloudops-01-monitoring-$Suffix"
$LogGroup = "/aws/lambda/$FunctionName"
$RoleName = "$FunctionName-execution-role"
$AlarmName = "$FunctionName-errors"
$AccountId = aws sts get-caller-identity --profile $Profile --query Account --output text
```

## 2. Create logging resources

```powershell
aws logs create-log-group `
  --log-group-name $LogGroup `
  --region $Region `
  --profile $Profile

aws logs put-retention-policy `
  --log-group-name $LogGroup `
  --retention-in-days 1 `
  --region $Region `
  --profile $Profile
```

Create `trust-policy.json` with the Lambda service as the trusted principal:

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {"Service": "lambda.amazonaws.com"},
    "Action": "sts:AssumeRole"
  }]
}
```

```powershell
aws iam create-role `
  --role-name $RoleName `
  --assume-role-policy-document file://trust-policy.json `
  --profile $Profile
```

Create `logging-policy.json`. The execution role can create streams and publish events only to this lab group:

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["logs:CreateLogStream", "logs:PutLogEvents"],
    "Resource": "arn:aws:logs:us-east-1:YOUR_ACCOUNT_ID:log-group:/aws/lambda/cloudops-01-monitoring:*"
  }]
}
```

Replace `YOUR_ACCOUNT_ID`, then attach the policy:

```powershell
aws iam put-role-policy `
  --role-name $RoleName `
  --policy-name "$FunctionName-logging" `
  --policy-document file://logging-policy.json `
  --profile $Profile

Start-Sleep -Seconds 10
```

## 3. Package and deploy the function

```powershell
Compress-Archive `
  -Path labs/cloudops/01-monitoring-incidents/src/lambda_function.py `
  -DestinationPath cloudops-01-monitoring.zip `
  -Force

$RoleArn = aws iam get-role `
  --role-name $RoleName `
  --query Role.Arn `
  --output text `
  --profile $Profile
```

```powershell
aws lambda create-function `
  --function-name $FunctionName `
  --runtime python3.12 `
  --handler lambda_function.lambda_handler `
  --role $RoleArn `
  --zip-file fileb://cloudops-01-monitoring.zip `
  --memory-size 128 `
  --timeout 3 `
  --region $Region `
  --profile $Profile
```

If the function already exists, update the code instead:

```powershell
aws lambda update-function-code `
  --function-name $FunctionName `
  --zip-file fileb://cloudops-01-monitoring.zip `
  --region $Region `
  --profile $Profile
```

## 4. Invoke success and failure events

Create the two payloads:

```powershell
'{"fail": false}' | Set-Content success.json
'{"fail": true}' | Set-Content failure.json
```

Success invocation:

```powershell
aws lambda invoke `
  --function-name $FunctionName `
  --payload fileb://success.json `
  --cli-binary-format raw-in-base64-out `
  success-response.json `
  --region $Region `
  --profile $Profile

Get-Content success-response.json
```

Failure invocation. Run this command three times:

```powershell
aws lambda invoke `
  --function-name $FunctionName `
  --payload fileb://failure.json `
  --cli-binary-format raw-in-base64-out `
  failure-response.json `
  --region $Region `
  --profile $Profile
```

## 5. Create and inspect the alarm

The metric name is `Errors`. The alarm name is `cloudops-01-monitoring-errors`.

```powershell
aws cloudwatch put-metric-alarm `
  --alarm-name $AlarmName `
  --alarm-description "Lambda errors for the CloudOps-01 lab" `
  --namespace AWS/Lambda `
  --metric-name Errors `
  --dimensions Name=FunctionName,Value=$FunctionName `
  --statistic Sum `
  --period 60 `
  --evaluation-periods 1 `
  --datapoints-to-alarm 1 `
  --threshold 1 `
  --comparison-operator GreaterThanOrEqualToThreshold `
  --treat-missing-data notBreaching `
  --region $Region `
  --profile $Profile
```

```powershell
aws cloudwatch describe-alarms `
  --alarm-names $AlarmName `
  --query "MetricAlarms[0].[AlarmName,StateValue,MetricName,Namespace,Threshold]" `
  --output table `
  --region $Region `
  --profile $Profile
```

## 6. Inspect metrics and logs

```powershell
$Start = (Get-Date).ToUniversalTime().AddMinutes(-15).ToString("o")
$End = (Get-Date).ToUniversalTime().ToString("o")

aws cloudwatch get-metric-statistics `
  --namespace AWS/Lambda `
  --metric-name Errors `
  --dimensions Name=FunctionName,Value=$FunctionName `
  --start-time $Start `
  --end-time $End `
  --period 60 `
  --statistics Sum `
  --region $Region `
  --profile $Profile

aws logs tail $LogGroup `
  --since 30m `
  --format short `
  --region $Region `
  --profile $Profile
```

## 7. Recover and verify OK

```powershell
aws lambda invoke `
  --function-name $FunctionName `
  --payload fileb://success.json `
  --cli-binary-format raw-in-base64-out `
  recovery-response.json `
  --region $Region `
  --profile $Profile
```

Run the recovery command three times, wait for the one-minute evaluation, and inspect the alarm again:

```powershell
aws cloudwatch describe-alarms `
  --alarm-names $AlarmName `
  --query "MetricAlarms[0].[AlarmName,StateValue,StateReason]" `
  --output table `
  --region $Region `
  --profile $Profile
```

Expected progression: `OK` or `INSUFFICIENT_DATA` -> `ALARM` -> `OK`.

## Optional SNS notification extension

This extension is outside the core lab. Create and confirm the subscription before attaching it to the alarm.

```powershell
$TopicArn = aws sns create-topic --name "$FunctionName-alerts" --region $Region --profile $Profile --query TopicArn --output text
aws sns subscribe --topic-arn $TopicArn --protocol email --notification-endpoint YOUR_EMAIL --region $Region --profile $Profile
aws cloudwatch put-metric-alarm --alarm-name $AlarmName --alarm-actions $TopicArn --region $Region --profile $Profile
```

Remove the alarm action, subscription, and topic after testing. Do not commit email addresses or subscription tokens.

## 8. Clean up

```powershell
aws cloudwatch delete-alarms --alarm-names $AlarmName --region $Region --profile $Profile
aws lambda delete-function --function-name $FunctionName --region $Region --profile $Profile
aws logs delete-log-group --log-group-name $LogGroup --region $Region --profile $Profile
aws iam delete-role-policy --role-name $RoleName --policy-name "$FunctionName-logging" --profile $Profile
aws iam delete-role --role-name $RoleName --profile $Profile
```

SNS notifications are out of scope. Create the dashboard with the Console or Terraform repeat, then delete all suffixed resources during cleanup.
