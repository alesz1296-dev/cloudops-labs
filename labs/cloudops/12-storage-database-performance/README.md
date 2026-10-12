# 12-storage-database-performance - Storage, caching, and database performance

Status: scenario defined; code and infrastructure not implemented.

## Objective and coverage

Measure and improve bounded storage and database workloads.

Exam domains: Monitoring and optimization; Reliability. This scenario addresses gaps in the initial track; it does not establish complete exam coverage.

## Prerequisites

Complete [readiness](../../00-readiness/README.md). CloudOps-08; DVA-10 for the cache fixture. Select region/engine support during implementation.

Use synthetic data and dedicated sandbox resources. Specify, review, and validate the resource plan before provisioning. Split larger scenarios into separate sessions. Record any design-only or simulated extension separately from hands-on evidence.

## Build

1. Measure a small EBS workload and compare provisioned IOPS/throughput with observed limits; review gp3 and io2 selection without provisioning expensive capacity by default.
2. Mount an EFS filesystem from approved clients, verify POSIX access controls, and configure lifecycle behavior; compare FSx options through a design exercise unless a paid fixture is planned.
3. Perform a small S3 multipart upload with checksum verification and abort cleanup; configure lifecycle rules on isolated prefixes and review Transfer Acceleration and a bounded DataSync transfer.
4. Inspect current RDS database monitoring facilities, connections, slow queries, and resource saturation; test RDS Proxy only with a supported engine/configuration.
5. Compare ElastiCache hits/misses and managed database scaling behavior; use a small DynamoDB auto-scaling fixture or explain the provisioned/on-demand alternatives.
6. Document instance/network/storage bottlenecks and placement-group use cases; change one tuning parameter at a time.

## Failure drill

Create bounded connection pressure and one stale cache entry. Compare tuning results to a baseline and verify correctness after recovery.

Capture the original configuration, introduce one failure at a time, and restore the baseline after each drill.

## Pass criteria

Before/after metrics explain the bottleneck and estimated cost; stored data/checksums remain correct; cache failures have a bounded fallback; incomplete multipart uploads are removed.

Save sanitized commands, measured results, and recovery evidence using [the evidence template](../../evidence-template.md). Completion requires the implemented path and failure path to pass; discussion-only extensions do not count as deployed validation.

## Cleanup

Remove cache/proxy, transfer tasks/agents, multipart uploads, lab filesystem/mount targets, volumes, snapshots, and database fixtures; review retention before deletion.

Confirm account, Region, resource prefix, ownership, and dependencies before deletion. Verify removal through read-only queries and account billing/resource views; note intentionally retained resources.

## Cost considerations

EFS/FSx, databases/proxies, caches, provisioned storage, DataSync, and accelerated transfer can be costly; run sub-exercises separately.

Budget alerts do not cap spending. Record a stop time and inspect retained resources after the session.

## Review questions

- What evidence distinguishes the failure from a similar symptom?
- Which identity and policy boundary control each action?
- What guarantees apply to ordering, retries, data consistency, or recovery?
- What changed in the measured behavior and cost?
- Which exercises were hands-on, simulated, or design-only?

