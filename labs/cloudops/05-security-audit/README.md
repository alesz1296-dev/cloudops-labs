# 05-security-audit — Audit, compliance checks, and remediation

Status: scenario defined; code and infrastructure not implemented.

## Objective and coverage

Detect and correct configuration drift in a dedicated sandbox.

Exam domains: Security and compliance; Monitoring. This mapping is a study aid, not a claim of complete exam coverage.

## Prerequisites

Complete [readiness](../../00-readiness/README.md). Use synthetic data in a dedicated sandbox. Prepare the specification, required service access, deployment plan, and cleanup plan before provisioning. If reusing resources from a prior scenario, document their ownership and do not remove them until dependents are finished.

## Build

1. Enable an appropriately scoped CloudTrail trail.
2. Inspect management events.
3. Use a scoped AWS Config rule or manual equivalent to check encryption and public access.
4. Review IAM permissions and KMS key access.
5. Document which audit events require separately enabled data-event logging.

## Failure drill

Introduce a reversible policy change that grants an unnecessary action to a lab role. Find the actor/change and restore least privilege; keep storage private throughout.

Make one change at a time. Capture the original configuration, investigate before applying a fix, and restore the baseline.

## Pass criteria

Evidence identifies actor, time, resource, and policy change; the excessive action is denied after remediation; audit retention and logging scope are explicit.

Save request results, relevant log/metric excerpts, and recovery verification using [the evidence template](../../evidence-template.md). Include at least one successful path and one failure path.

## Cleanup

Remove scoped Config resources, trail, audit storage, and temporary policies after preserving required evidence.

Verify deletion in the Console or through read-only CLI queries. Check retained logs, backups, keys, artifacts, network interfaces, and storage. Confirm the resource prefix before any deletion.

## Cost considerations

AWS Config evaluations, CloudTrail data events, storage, and KMS keys can incur charges.

## Review questions

- Which component caused the observed failure, and what evidence proves it?
- Which identity performed each action, and which permission allowed it?
- What happens when the request or event is retried?
- What remains billable after the exercise?
- How would you reproduce the result without the walkthrough?

