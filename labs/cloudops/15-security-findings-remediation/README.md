# 15-security-findings-remediation - Security findings, access analysis, and compliance

Status: scenario defined; code and infrastructure not implemented.

## Objective and coverage

Triage sample findings and verify least-privilege remediation.

Exam domains: Security and compliance; Automation. This scenario addresses gaps in the initial track; it does not establish complete exam coverage.

## Prerequisites

Complete [readiness](../../00-readiness/README.md). CloudOps-05; authorized sandbox security service configuration. Account support features may require a review-only substitute.

Use synthetic data and dedicated sandbox resources. Specify, review, and validate the resource plan before provisioning. Split larger scenarios into separate sessions. Record any design-only or simulated extension separately from hands-on evidence.

## Build

1. Use IAM Access Analyzer and the policy simulator on dedicated lab identities; explain external access findings versus effective runtime permissions.
2. Enable selected GuardDuty, Inspector, and Security Hub capabilities in the sandbox with a documented cost/retention plan.
3. Generate supported sample findings rather than malicious activity, trace them through the finding workflow, and classify severity/resource/owner.
4. Configure a narrowly scoped Config conformance exercise and review Trusted Advisor checks available to the account's support plan.
5. Implement a finding-to-remediation workflow with explicit resource/tag preconditions, then test it on a harmless lab policy drift.
6. Review data classification, secret storage, KMS policy/encryption failures, and ACM certificate lifecycle with synthetic data.

## Failure drill

Use a sample finding to test routing and a separate real, harmless lab policy change to test remediation. Simulate a deny and explain why the policy simulator alone is insufficient proof.

Capture the original configuration, introduce one failure at a time, and restore the baseline after each drill.

## Pass criteria

Sample findings are clearly labeled, unauthorized access is denied in a runtime check, remediation touches only owned fixtures, and compliance status reflects the corrected configuration.

Save sanitized commands, measured results, and recovery evidence using [the evidence template](../../evidence-template.md). Completion requires the implemented path and failure path to pass; discussion-only extensions do not count as deployed validation.

## Cleanup

Remove remediation triggers and policies, scoped Config resources, dedicated analyzers, and newly enabled lab service integrations/detectors where appropriate; preserve existing security coverage.

Confirm account, Region, resource prefix, ownership, and dependencies before deletion. Verify removal through read-only queries and account billing/resource views; note intentionally retained resources.

## Cost considerations

Security scanning, detector ingestion, Config evaluations, optional support-plan features, and logs.

Budget alerts do not cap spending. Record a stop time and inspect retained resources after the session.

## Review questions

- What evidence distinguishes the failure from a similar symptom?
- Which identity and policy boundary control each action?
- What guarantees apply to ordering, retries, data consistency, or recovery?
- What changed in the measured behavior and cost?
- Which exercises were hands-on, simulated, or design-only?

