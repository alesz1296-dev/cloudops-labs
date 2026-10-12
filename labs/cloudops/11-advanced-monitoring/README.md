# 11-advanced-monitoring - CloudWatch agent, composite alarms, and shared visibility

Status: scenario defined; code and infrastructure not implemented.

## Objective and coverage

Collect OS-level signals and diagnose an incident across resource boundaries.

Exam domains: Monitoring; Automation. This scenario addresses gaps in the initial track; it does not establish complete exam coverage.

## Prerequisites

Complete [readiness](../../00-readiness/README.md). CloudOps-01 and an SSM-managed fixture; second Region/account only for the corresponding extension.

Use synthetic data and dedicated sandbox resources. Specify, review, and validate the resource plan before provisioning. Split larger scenarios into separate sessions. Record any design-only or simulated extension separately from hands-on evidence.

## Build

1. Configure the CloudWatch agent on a disposable SSM-managed EC2 instance to collect memory, disk, and application logs with explicit retention.
2. Create metric filters and custom metrics; compare dimensions and aggregation against default EC2 metrics.
3. Create child alarms and a composite alarm, documenting missing-data behavior and which alarm types support each chosen action.
4. Create a cross-Region dashboard and, if a second approved account exists, configure supported cross-account observability.
5. Route a child alarm event through EventBridge to a bounded SSM/Lambda remediation with preconditions and postchecks.
6. Compare container metrics/logs from CloudOps-09; optionally inspect Prometheus metrics using a supported collector.

## Failure drill

Stop the agent, then fill a small disposable data-volume directory up to a preselected safe threshold. Restore each before continuing; never fill the root filesystem.

Capture the original configuration, introduce one failure at a time, and restore the baseline after each drill.

## Pass criteria

OS metrics are distinct from default service metrics, composite behavior matches child states, remediation acts only on the tagged fixture, and missing telemetry is detectable.

Save sanitized commands, measured results, and recovery evidence using [the evidence template](../../evidence-template.md). Completion requires the implemented path and failure path to pass; discussion-only extensions do not count as deployed validation.

## Cleanup

Disable remediation triggers, remove lab monitoring links, agents/configuration, alarms, dashboards, custom log groups, and owned fixtures.

Confirm account, Region, resource prefix, ownership, and dependencies before deletion. Verify removal through read-only queries and account billing/resource views; note intentionally retained resources.

## Cost considerations

Custom metrics/dimensions, logs, dashboards, cross-Region transfer, and optional Prometheus ingestion.

Budget alerts do not cap spending. Record a stop time and inspect retained resources after the session.

## Review questions

- What evidence distinguishes the failure from a similar symptom?
- Which identity and policy boundary control each action?
- What guarantees apply to ordering, retries, data consistency, or recovery?
- What changed in the measured behavior and cost?
- Which exercises were hands-on, simulated, or design-only?

