# CloudOps-01: Console walkthrough

Region: us-east-1. Estimated study time: 60-90 minutes plus setup. No CLI profile is needed. Labels may vary slightly as the AWS Console changes.

## 1. Confirm readiness

Sign in to a dedicated nonproduction account. Check the account identity in the Console and select **US East (N. Virginia)** (`us-east-1`). Record the account and Region in private notes, choose a budget alert and cleanup time, and use synthetic inputs only. No AWS CLI profile is required for this Console-first exercise.

Use a unique suffix in every name, for example cloudops-01-monitoring-alex. Record the exact names before creating resources. Record resource names and ownership; use Project, Track, Lab, and Owner tags where supported.

## 2. Create the log group and execution role

In **CloudWatch → Logs → Log groups**, choose **Create log group**. Enter exactly:

```text
/aws/lambda/cloudops-01-monitoring
```

Set **Retention setting** to **1 day**, then create the group. Do not create a group named only `cloudops-01-monitoring`; Lambda uses the `/aws/lambda/<function-name>` pattern.

In **IAM → Roles**, choose **Create role**, select **AWS service → Lambda**, and create a dedicated role. Attach an inline policy containing only `logs:CreateLogStream` and `logs:PutLogEvents`, scoped to the streams in your lab group:

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

Replace `YOUR_ACCOUNT_ID` and any name suffix. The group already exists, so the runtime needs no `logs:CreateLogGroup` permission. Lambda trust uses the service principal `lambda.amazonaws.com` and `sts:AssumeRole`. The learner's own permissions to create and pass the role are separate. If you use a suffix, change the function name, log-group name, policy ARN, and all later metric dimensions consistently.

## 3. Deploy the tiny workload

In **Lambda → Functions → Create function**, choose **Author from scratch**:

- Name: cloudops-01-monitoring-<suffix>.
- Runtime: a currently supported Python runtime, such as the current Python 3.x option shown by the Console.
- Execution role: the dedicated role above.
- Memory: 128 MB; timeout: three seconds.
- No function URL, API, VPC attachment, external triggers, or provisioned concurrency.

After the function opens, select the **Code** tab, open `lambda_function.py`, replace its contents with [the handler](src/lambda_function.py), and choose **Deploy**. Keep the handler setting `lambda_function.lambda_handler`. Keep Lambda's default logging configuration; the handler emits structured JSON lines through `print()`.

Save two private Console test events:

Success:

```json
{"fail": false}
```

Failure:

```json
{"fail": true}
```

Run the **success** event once. The response should contain `"ok": true` and a `request_id`. Open **Monitor → View CloudWatch logs**, select the newest stream, and confirm the same request ID appears in a JSON log line with `"outcome": "success"`. If logs are missing, inspect the group name, Region, execution role, and stream permissions before continuing.

## 4. Build the dashboard

In **CloudWatch → Metrics → All metrics → Lambda → By Function Name**, select the row whose dimension is exactly `FunctionName = ____________________`. Do not select an account-wide aggregate or another function/alias. Add these four widgets to a new dashboard named `cloudops-01-monitoring`:

| Metric | Statistic | Period |
| --- | --- | --- |
| Invocations | Sum | 1 minute |
| Errors | Sum | 1 minute |
| Throttles | Sum | 1 minute |
| Duration | Average | 1 minute |

Metrics may take several minutes to appear. Before the first invocation, the graph may show **No data available**; that is expected.

## 5. Create an Errors alarm

From the selected `Errors` metric, choose **Create alarm**. On **Specify metric and conditions**, use:

- Namespace: `AWS/Lambda`.
- **Metric name: `Errors`**. Do not enter the alarm name here.
- Dimension: `FunctionName = ____________________`.
- Statistic: `Sum`; period: `1 minute`.
- Threshold type: `Static`; condition: `Greater/Equal`.
- Threshold value: `1`.
- Evaluation: `1 out of 1` datapoints/evaluation periods.
- Additional configuration → missing data: **Treat missing data as not breaching**.

On **Configure actions**, keep the alarm state trigger as **In alarm**. Leave alarm actions empty; SNS notifications are outside this lab. For a separate production exercise, choose **Create new topic**, use the topic name `cloudops-01-monitoring-alerts`, and enter an email address you control. Choose **Add notification**. The alarm can work without email, so you may leave this section empty if you do not want the extension.

If the Console warns that the SNS endpoint is pending confirmation, open the AWS subscription email and click **Confirm subscription**. Refresh the alarm page and confirm the subscription is no longer pending. A pending subscription does not receive alarm messages.

On **Add alarm details**, set the alarm name to `cloudops-01-monitoring-errors`. The metric remains `Errors`; `cloudops-01-monitoring-errors` is only the alarm name. Optionally add tags such as `Project=content-failures-api`, `Track=CloudOps`, `Lab=cloudops-01-monitoring`, and `Environment=sandbox`. Create the alarm.

The initial alarm state may be `OK` or `INSUFFICIENT_DATA`. Both can be normal while CloudWatch is waiting for datapoints. Run another success event and allow a few minutes for metric publication and alarm evaluation; do not manually force the alarm state.

## Optional SNS notification extension

SNS is optional and outside the core pass criteria. Create a topic named `cloudops-01-monitoring-<suffix>-alerts`, add an email subscription, confirm it from the email, and attach it to the alarm's In alarm action. Cause one controlled failure and verify the notification. During cleanup, remove the alarm action, subscription, and topic. A pending subscription will not receive messages.

## 6. Cause and investigate the incident

Run the **failure** event three times, synchronously, with no loop or background generator. Stop traffic and wait for metric publication and alarm evaluation.

The handler deliberately raises RuntimeError. Returning a JSON object containing statusCode 500 would be a successful Lambda invocation and would not test this native Errors alarm.

Find an ALARM transition in alarm history and examine the triggering datapoint. In Logs Insights, select the lab group and a time window covering your tests:

```text
fields @timestamp, @message
| parse @message /"request_id": "(?<lab_request_id>[^"]+)"/
| parse @message /"outcome": "(?<lab_outcome>[^"]+)"/
| filter lab_outcome = "failure"
| sort @timestamp desc
| limit 20
```

Link one failure log to its invocation request ID and explain the source of the error. Inspect Errors, Invocations, and Throttles separately. No throttling is deliberately generated in this first drill.

If `ALARM` does not appear, check the function and Region, metric name (`Errors`), `FunctionName` dimension, `Sum` versus `Average`, time range, period, threshold, and actual raised exceptions. Generate at most one additional failure after correcting the configuration. Do not force the alarm state manually as a substitute.

## 7. Recover and prove it

Select the success event and invoke three times after the failure period. Verify successful responses and success logs, then observe an eventual OK transition.

Record the ALARM and OK timestamps and the successful recovery requests. Older breaching datapoints can affect evaluation briefly. An alarm configured with notBreaching can also return to OK after traffic stops; idle OK alone does not prove workload recovery.

Optional exercise: edit the alarm and change missing-data treatment to **Missing**, stop traffic, and observe eventual `INSUFFICIENT_DATA` after usable datapoints age out. Restore **Treat missing data as not breaching** and verify the setting.

## 8. Save evidence and clean up

Copy [the evidence template](../../evidence-template.md) into private notes. Capture the dashboard, alarm configuration/history, sanitized failure/recovery logs, and optional confirmed notification.

Once those are saved, manually remove only the owned alarm, dashboard, subscription/topic, function, log group, role/policy, and saved test events with the function. Log retention does not remove dashboards or alarms. Recheck resource lists and note any retained resource.

## Completion checklist

- [ ] Sandbox account, Region, budget, names, and cleanup time confirmed.
- [ ] Success response and structured log verified.
- [ ] Dashboard shows the correct metrics and dimensions.
- [ ] Actual function errors cause ALARM.
- [ ] Root cause demonstrated through request-correlated logs.
- [ ] Successful recovery invocations verified; subsequent OK recorded.
- [ ] Missing-data behavior explained.
- [ ] SNS remains out of scope for this lab.
- [ ] Owned resources removed and cleanup verified.

## Local fixture verification

From the repository root, with a working Python installation:

```powershell
python -B -m unittest discover -s labs/cloudops/01-monitoring-incidents/tests -v
```

These checks validate local behavior only. AWS permissions, alarm transitions, notifications, and cleanup require the Console exercise.
