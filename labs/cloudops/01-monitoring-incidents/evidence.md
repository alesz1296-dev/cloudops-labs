# CloudOps-01 monitoring and incident response evidence

Date: 2026-10-12 (UTC shown by AWS Console)
Region: us-east-1
Function: `cloudops-01-monitoring-<suffix>`
Alarm: `cloudops-01-monitoring-<suffix>-errors`

## Result

- [x] Lambda fixture deployed and executed.
- [x] Deliberate failure raised `RuntimeError: Deliberate CloudOps lab failure`.
- [x] Native `AWS/Lambda` `Errors` metric selected with `Sum`, one-minute period, threshold `>= 1`.
- [x] Alarm entered `In alarm` after recorded errors.
- [x] Successful invocations returned the metric to zero.
- [x] Alarm recovered to `OK`.
- [x] Missing data treatment was `Treat missing data as good (not breaching threshold)`.
- [x] Alarm actions were left empty because SNS is out of scope.
- [ ] SNS notification: out of scope for this lab.
- [ ] Resource cleanup: record completion after deleting lab resources.

## Observed configuration

```text
Namespace: AWS/Lambda
Metric name: Errors
FunctionName: cloudops-01-monitoring
Statistic: Sum
Period: 1 minute
Datapoints to alarm: 1 out of 1
Threshold: Errors >= 1
Missing data: Treat missing data as good
```

The alarm initially used the wrong metric name (`cloudops-01-monitoring-errors`) and stayed `OK` because missing data was treated as non-breaching. It was corrected to the native Lambda metric `Errors` before the incident drill.

## Failure and recovery evidence

Use this section as a worksheet. Do not publish real request IDs, account IDs, email addresses, ARNs, or timestamps. Record them privately while completing the lab, then sanitize the copy used for study notes.

### Failure correlation

- Failure test timestamp (UTC): ______________________________
- Request ID from the failing response: ______________________________
- Matching CloudWatch log stream: ______________________________
- Matching JSON log timestamp: ______________________________
- Error message observed: ______________________________
- Why this proves the exception belongs to this invocation: ______________________________

### Alarm transition

- Alarm name: ______________________________
- Time the alarm entered ALARM (UTC): ______________________________
- Triggering Errors datapoint/count: ______________________________
- Alarm history reason: ______________________________
- Evidence that the selected metric was native `AWS/Lambda` `Errors`: ______________________________

### Recovery correlation

- First successful recovery request ID: ______________________________
- Number of successful recovery invocations: ______
- Time the alarm returned to OK (UTC): ______________________________
- Matching success log evidence: ______________________________
- Explanation of why this proves workload recovery: ______________________________
- Explanation of why idle OK alone would not prove recovery: ______________________________

### Student explanation

Describe the failure path from invocation to log to metric to alarm, then describe the recovery path. Identify the exact setting or component that caused the observed state and cite the evidence used.

## Lessons

- `Errors` is the metric name; `cloudops-01-monitoring-errors` is the alarm name.
- The handler must raise an exception to create a Lambda `Errors` datapoint.
- An SNS subscription must be confirmed before email notifications work.
- Successful recovery invocations prove recovery more strongly than an idle `OK` caused by missing-data treatment.

## Cleanup record

- Alarm deleted: [ ]
- Dashboard deleted: [ ]
- SNS topic/subscription: out of scope
- Lambda deleted: [ ]
- Log group deleted: [ ]
- IAM role and inline policy deleted: [ ]
- Retained resources reviewed: [ ]
