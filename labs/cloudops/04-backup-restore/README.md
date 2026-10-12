# 04-backup-restore — Backups, restore, and recovery objectives

Status: scenario defined; code and infrastructure not implemented.

## Objective and coverage

Recover synthetic task data and evidence after accidental changes.

Exam domains: Reliability and business continuity. This mapping is a study aid, not a claim of complete exam coverage.

## Prerequisites

Complete [readiness](../../00-readiness/README.md). Use synthetic data in a dedicated sandbox. Prepare the specification, required service access, deployment plan, and cleanup plan before provisioning. If reusing resources from a prior scenario, document their ownership and do not remove them until dependents are finished.

## Build

1. Enable DynamoDB PITR and S3 versioning on dedicated resources.
2. Seed timestamped records and objects.
3. Define target RPO and RTO.
4. Restore DynamoDB into a new table.
5. Verify indexes/settings and explicitly switch the lab application's table reference.
6. Recover an earlier S3 version.

## Failure drill

Modify or delete one synthetic item and object only after confirming a recoverable backup/version. Measure the entire restore and cutover.

Make one change at a time. Capture the original configuration, investigate before applying a fix, and restore the baseline.

## Pass criteria

Recovered data matches the chosen recovery point; the app reads the restored table; measured RPO/RTO are documented; restore omissions are identified.

Save request results, relevant log/metric excerpts, and recovery verification using [the evidence template](../../evidence-template.md). Include at least one successful path and one failure path.

## Cleanup

Revert application configuration before removing restored/original tables; remove bucket versions and backup artifacts deliberately.

Verify deletion in the Console or through read-only CLI queries. Check retained logs, backups, keys, artifacts, network interfaces, and storage. Confirm the resource prefix before any deletion.

## Cost considerations

PITR, restored tables, backups, and noncurrent object versions add cost; TTL is not a backup mechanism.

## Review questions

- Which component caused the observed failure, and what evidence proves it?
- Which identity performed each action, and which permission allowed it?
- What happens when the request or event is retried?
- What remains billable after the exercise?
- How would you reproduce the result without the walkthrough?

