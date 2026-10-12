# 13-automated-disaster-recovery - AWS Backup and cross-Region disaster recovery

Status: scenario defined; code and infrastructure not implemented.

## Objective and coverage

Recover a small workload in a second Region with measured RPO and RTO.

Exam domains: Reliability and business continuity; Automation. This scenario addresses gaps in the initial track; it does not establish complete exam coverage.

## Prerequisites

Complete [readiness](../../00-readiness/README.md). CloudOps-04; approved second Region and supported AWS Backup resource. Check service/Region support before implementation.

Use synthetic data and dedicated sandbox resources. Specify, review, and validate the resource plan before provisioning. Split larger scenarios into separate sessions. Record any design-only or simulated extension separately from hands-on evidence.

## Build

1. Create an AWS Backup plan, resource selection, retention schedule, and vault for a supported synthetic resource.
2. Configure a supported cross-Region backup copy with compatible encryption/access; verify a completed copy before attempting recovery.
3. Restore into isolated target resources, inspect restored configuration, reconnect the client, and verify data.
4. Write backup/restore, pilot-light, warm-standby, and active/active recovery procedures; implement backup/restore and a minimal pilot-light fixture.
5. Use a planned client endpoint/configuration switch to simulate loss of the source; measure recovery through cutover and validation.
6. Compare warm standby and active/active as design exercises unless their always-running resource cost is explicitly budgeted.

## Failure drill

Treat the source as unavailable by switching only the lab client; restore from the copied recovery point without deleting the source or disabling a Region.

Capture the original configuration, introduce one failure at a time, and restore the baseline after each drill.

## Pass criteria

The copy is recoverable, restored records match the selected point, RPO/RTO include cutover, and design-only DR strategies are clearly labeled.

Save sanitized commands, measured results, and recovery evidence using [the evidence template](../../evidence-template.md). Completion requires the implemented path and failure path to pass; discussion-only extensions do not count as deployed validation.

## Cleanup

Remove test failover routing/config, restore fixtures, schedules/selections, recovery points and vaults where deletion is allowed, and temporary policies. Avoid irreversible vault locking for this exercise.

Confirm account, Region, resource prefix, ownership, and dependencies before deletion. Verify removal through read-only queries and account billing/resource views; note intentionally retained resources.

## Cost considerations

Backup storage/copies, restore resources, cross-Region transfer, and standby compute.

Budget alerts do not cap spending. Record a stop time and inspect retained resources after the session.

## Review questions

- What evidence distinguishes the failure from a similar symptom?
- Which identity and policy boundary control each action?
- What guarantees apply to ordering, retries, data consistency, or recovery?
- What changed in the measured behavior and cost?
- Which exercises were hands-on, simulated, or design-only?

