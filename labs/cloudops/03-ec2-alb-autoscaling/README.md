# 03-ec2-alb-autoscaling — EC2, load balancing, and Auto Scaling

Status: scenario defined; code and infrastructure not implemented.

## Objective and coverage

Operate a disposable web workload across two Availability Zones.

Exam domains: Reliability; Deployment; Monitoring. This mapping is a study aid, not a claim of complete exam coverage.

## Prerequisites

Complete [readiness](../../00-readiness/README.md). Use synthetic data in a dedicated sandbox. Prepare the specification, required service access, deployment plan, and cleanup plan before provisioning. If reusing resources from a prior scenario, document their ownership and do not remove them until dependents are finished.

## Build

1. Use a launch template and Auto Scaling group behind an ALB.
2. Configure application health checks and an instance role for Systems Manager.
3. Collect instance/application metrics.
4. Test bounded scaling.
5. Distinguish EC2 status checks from ALB target health.

## Failure drill

Stop the web process on one instance, then terminate a lab instance. Observe load-balancer routing and Auto Scaling replacement.

Make one change at a time. Capture the original configuration, investigate before applying a fix, and restore the baseline.

## Pass criteria

Healthy requests continue during a single-instance failure; unhealthy targets leave rotation; desired capacity returns; scaling observations include cooldown/warmup behavior.

Save request results, relevant log/metric excerpts, and recovery verification using [the evidence template](../../evidence-template.md). Include at least one successful path and one failure path.

## Cleanup

Remove the group, ALB/listeners/target group, launch template, instances, and lab network; check EBS volumes and addresses.

Verify deletion in the Console or through read-only CLI queries. Check retained logs, backups, keys, artifacts, network interfaces, and storage. Confirm the resource prefix before any deletion.

## Cost considerations

ALB, EC2, EBS, and IPv4 charges accrue while provisioned.

## Review questions

- Which component caused the observed failure, and what evidence proves it?
- Which identity performed each action, and which permission allowed it?
- What happens when the request or event is retried?
- What remains billable after the exercise?
- How would you reproduce the result without the walkthrough?

