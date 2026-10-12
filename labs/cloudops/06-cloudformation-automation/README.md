# 06-cloudformation-automation — CloudFormation, drift, and operational automation

Status: scenario defined; code and infrastructure not implemented.

## Objective and coverage

Provision a small stack and remediate predictable operational failures.

Exam domains: Deployment, provisioning, and automation. This mapping is a study aid, not a claim of complete exam coverage.

## Prerequisites

Complete [readiness](../../00-readiness/README.md). Use synthetic data in a dedicated sandbox. Prepare the specification, required service access, deployment plan, and cleanup plan before provisioning. If reusing resources from a prior scenario, document their ownership and do not remove them until dependents are finished.

## Build

1. Create a separate CloudFormation stack with an SSM-managed instance.
2. Inspect a change set.
3. Use parameters/outputs.
4. Make a supported configuration drift change and run drift detection.
5. Write an SSM Automation runbook with preconditions and postchecks.
6. Schedule a harmless check with EventBridge.

## Failure drill

Submit an update that fails in the isolated stack and observe rollback; run a bounded automation that repairs a stopped lab service.

Make one change at a time. Capture the original configuration, investigate before applying a fix, and restore the baseline.

## Pass criteria

Stack status and events explain rollback; drift is detected where supported; automation records its actions and confirms service health; credentials are absent from templates.

Save request results, relevant log/metric excerpts, and recovery verification using [the evidence template](../../evidence-template.md). Include at least one successful path and one failure path.

## Cleanup

Disable scheduled triggers, then remove automation documents, stack, and retained resources after review.

Verify deletion in the Console or through read-only CLI queries. Check retained logs, backups, keys, artifacts, network interfaces, and storage. Confirm the resource prefix before any deletion.

## Cost considerations

EC2, automation executions, and logs; avoid a permanently running scheduler.

## Review questions

- Which component caused the observed failure, and what evidence proves it?
- Which identity performed each action, and which permission allowed it?
- What happens when the request or event is retried?
- What remains billable after the exercise?
- How would you reproduce the result without the walkthrough?

