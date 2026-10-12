# 08-rds-storage-recovery — RDS, EBS, and storage operations

Status: scenario defined; code and infrastructure not implemented.

## Objective and coverage

Recover a small relational workload and a separate instance data volume.

Exam domains: Reliability; Monitoring; Security. This mapping is a study aid, not a claim of complete exam coverage.

## Prerequisites

Complete [readiness](../../00-readiness/README.md). Use synthetic data in a dedicated sandbox. Prepare the specification, required service access, deployment plan, and cleanup plan before provisioning. If reusing resources from a prior scenario, document their ownership and do not remove them until dependents are finished.

## Build

1. Create a private disposable RDS database and approved client.
2. Seed synthetic data.
3. Take a snapshot and restore to a new DB endpoint.
4. Compare Multi-AZ availability with read replicas.
5. Separately snapshot an EC2 data EBS volume, restore/attach it, and verify file checksums.
6. Review backup retention and encryption.

## Failure drill

Change synthetic DB data after a snapshot and corrupt only a copied lab file. Recover both into new resources; optionally perform a supported failover if a Multi-AZ lab is provisioned.

Make one change at a time. Capture the original configuration, investigate before applying a fix, and restore the baseline.

## Pass criteria

Restored queries and checksums match expectations; client configuration uses the new endpoint; RPO/RTO include cutover; failover and read scaling are distinguished.

Save request results, relevant log/metric excerpts, and recovery verification using [the evidence template](../../evidence-template.md). Include at least one successful path and one failure path.

## Cleanup

Remove the restored DB, original lab DB, client, volumes, and snapshots after explicitly reviewing backup retention and final-snapshot choices.

Verify deletion in the Console or through read-only CLI queries. Check retained logs, backups, keys, artifacts, network interfaces, and storage. Confirm the resource prefix before any deletion.

## Cost considerations

RDS, Multi-AZ, EBS volumes, and snapshots can be costly; keep this exercise short.

## Review questions

- Which component caused the observed failure, and what evidence proves it?
- Which identity performed each action, and which permission allowed it?
- What happens when the request or event is retried?
- What remains billable after the exercise?
- How would you reproduce the result without the walkthrough?

