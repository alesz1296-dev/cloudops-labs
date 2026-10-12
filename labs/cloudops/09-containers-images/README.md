# 09-containers-images - ECS, ECR, AMIs, and image operations

Status: scenario defined; code and infrastructure not implemented.

## Objective and coverage

Operate a disposable container service and maintain reproducible machine images.

Exam domains: Deployment; Monitoring; Reliability. This scenario addresses gaps in the initial track; it does not establish complete exam coverage.

## Prerequisites

Complete [readiness](../../00-readiness/README.md). Container build tooling and sandbox network; CloudOps-03 if reusing its ALB.

Use synthetic data and dedicated sandbox resources. Specify, review, and validate the resource plan before provisioning. Split larger scenarios into separate sessions. Record any design-only or simulated extension separately from hands-on evidence.

## Build

1. Build a tiny HTTP container, publish a versioned image to ECR, and deploy an ECS Fargate service with health/readiness checks and bounded desired capacity.
2. Separate task execution and application task roles; configure logs, inspect task stop reasons, and measure service CPU/memory.
3. Perform a rolling release and inspect health during replacement; optionally compare blue/green using the supported deployment controller.
4. Enable image scanning where supported and review a synthetic or benign finding without introducing malicious images.
5. Build a small AMI with EC2 Image Builder or a reviewed manual image workflow; test it in a disposable instance and record source image and package versions.

## Failure drill

Deploy an incorrect image tag, then a failing health check in separate revisions. Recover to the known good revision.

Capture the original configuration, introduce one failure at a time, and restore the baseline after each drill.

## Pass criteria

Image pull, IAM, initialization, and health-check failures are distinguishable; service capacity recovers; image provenance and AMI launch results are recorded.

Save sanitized commands, measured results, and recovery evidence using [the evidence template](../../evidence-template.md). Completion requires the implemented path and failure path to pass; discussion-only extensions do not count as deployed validation.

## Cleanup

Scale down/delete the service and cluster resources; remove images/repository, image-building schedules/resources, AMIs and associated owned snapshots, and logs.

Confirm account, Region, resource prefix, ownership, and dependencies before deletion. Verify removal through read-only queries and account billing/resource views; note intentionally retained resources.

## Cost considerations

Fargate, load balancing, image scans/storage, image-builder EC2 instances, and snapshots.

Budget alerts do not cap spending. Record a stop time and inspect retained resources after the session.

## Review questions

- What evidence distinguishes the failure from a similar symptom?
- Which identity and policy boundary control each action?
- What guarantees apply to ordering, retries, data consistency, or recovery?
- What changed in the measured behavior and cost?
- Which exercises were hands-on, simulated, or design-only?

