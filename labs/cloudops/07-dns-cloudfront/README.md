# 07-dns-cloudfront — DNS, TLS, and content delivery

Status: scenario defined; code and infrastructure not implemented.

## Objective and coverage

Serve private-origin static content through CloudFront and diagnose caching behavior.

Exam domains: Networking and content delivery; Monitoring. This mapping is a study aid, not a claim of complete exam coverage.

## Prerequisites

Complete [readiness](../../00-readiness/README.md). Use synthetic data in a dedicated sandbox. Prepare the specification, required service access, deployment plan, and cleanup plan before provisioning. If reusing resources from a prior scenario, document their ownership and do not remove them until dependents are finished.

## Build

1. Use a dedicated S3 origin with Origin Access Control.
2. Keep direct bucket access blocked.
3. Inspect cache headers and TTL behavior.
4. Invalidate an updated object.
5. If an owned domain is available, add Route 53 alias records and an ACM certificate in the region required by CloudFront.
6. Otherwise use the distribution hostname and study DNS separately.

## Failure drill

Request a missing object, then create a controlled origin-permission denial. Compare origin access failures with cached responses and DNS resolution.

Make one change at a time. Capture the original configuration, investigate before applying a fix, and restore the baseline.

## Pass criteria

The distribution serves allowed content; direct anonymous S3 access fails; stale content behavior is explained; a restored origin permission recovers service after cache behavior is accounted for.

Save request results, relevant log/metric excerpts, and recovery verification using [the evidence template](../../evidence-template.md). Include at least one successful path and one failure path.

## Cleanup

Disable/delete the distribution following service prerequisites; remove lab records, certificate if unused, bucket contents, and bucket; retain an existing owned domain.

Verify deletion in the Console or through read-only CLI queries. Check retained logs, backups, keys, artifacts, network interfaces, and storage. Confirm the resource prefix before any deletion.

## Cost considerations

CloudFront requests/transfer, invalidations, hosted zones, and optional domain registration.

## Review questions

- Which component caused the observed failure, and what evidence proves it?
- Which identity performed each action, and which permission allowed it?
- What happens when the request or event is retried?
- What remains billable after the exercise?
- How would you reproduce the result without the walkthrough?

