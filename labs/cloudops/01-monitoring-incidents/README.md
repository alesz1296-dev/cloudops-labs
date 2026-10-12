# 01-monitoring-incidents — Monitoring, alarms, and incident response

Status: Console walkthrough and locally tested Python fixture prepared; AWS execution pending. Terraform repeat not implemented.

Start with [the guided Console walkthrough](walkthrough.md), then repeat it with the [AWS CLI equivalent](cli-equivalent.md) or the separate [Terraform implementation guide](terraform-guide.md). See the [visual guide](visual-guide.md) and [saved evidence](evidence.md). The specification and acceptance criteria are in [the lab spec](../../../specs/cert-labs-cloudops-01/spec.md).

## Objective and coverage

Operate a small API or Lambda with an actionable error alarm.

Exam domains: Monitoring and optimization. This mapping is a study aid, not a claim of complete exam coverage.

## Prerequisites

Complete [readiness](../../00-readiness/README.md). Use synthetic data in a dedicated sandbox. Prepare the specification, required service access, deployment plan, and cleanup plan before provisioning. If reusing resources from a prior scenario, document their ownership and do not remove them until dependents are finished.

## Build

1. Create structured logs, a Logs Insights query, and a dashboard for errors, duration, and throttles.
2. Configure an alarm and optional SNS subscription.
3. Document missing-data handling and a response runbook.

## Failure drill

Generate a bounded series of errors, then stop traffic. Investigate using metrics and logs, recover the application, and observe the alarm return to OK.

Make one change at a time. Capture the original configuration, investigate before applying a fix, and restore the baseline.

## Pass criteria

Alarm behavior matches its period and threshold; the notification reaches a confirmed subscription if enabled; the runbook leads to a verified recovery.

Save request results, relevant log/metric excerpts, and recovery verification using [the evidence template](../../evidence-template.md). Include at least one successful path and one failure path.

## Cleanup

Remove alarms, dashboard, subscription, topic, and lab log groups after saving sanitized evidence.

Verify deletion in the Console or through read-only CLI queries. Check retained logs, backups, keys, artifacts, network interfaces, and storage. Confirm the resource prefix before any deletion.

## Cost considerations

Dashboards, alarms, notifications, and logs can incur charges.

## Review questions

- Which component caused the observed failure, and what evidence proves it?
- Which identity performed each action, and which permission allowed it?
- What happens when the request or event is retried?
- What remains billable after the exercise?
- How would you reproduce the result without the walkthrough?

