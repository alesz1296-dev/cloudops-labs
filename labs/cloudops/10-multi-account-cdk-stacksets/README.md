# 10-multi-account-cdk-stacksets - Organizations, SCPs, CDK, StackSets, and sharing

Status: scenario defined; code and infrastructure not implemented.

## Objective and coverage

Deploy and govern a harmless resource across controlled sandbox boundaries.

Exam domains: Security; Deployment. This scenario addresses gaps in the initial track; it does not establish complete exam coverage.

## Prerequisites

Complete [readiness](../../00-readiness/README.md). Existing approved sandbox organization, multiple profiles, and CDK toolchain. Without them, label policy/design exercises as simulated.

Use synthetic data and dedicated sandbox resources. Specify, review, and validate the resource plan before provisioning. Split larger scenarios into separate sessions. Record any design-only or simulated extension separately from hands-on evidence.

## Build

1. Inventory an existing approved sandbox organization and permission sets; document management, delegated administrator, and member-account roles.
2. Apply a narrowly scoped SCP exercise only to a dedicated disposable OU/account with a tested recovery path; explain that an SCP limits permissions rather than granting them.
3. Author a small CDK stack and inspect its synthesized CloudFormation; compare bootstrap roles and least privilege with direct template deployment.
4. Deploy a harmless StackSet to selected sandbox accounts/Regions using an approved permission model; inspect one failed stack instance.
5. Share a supported resource through AWS RAM and confirm recipient access; distinguish a share from permissions to use the resource.

## Failure drill

In a dedicated sandbox target, deny one harmless operation with the test SCP, or simulate the policies if organizational changes are unavailable. Cause one StackSet permission failure and recover it.

Capture the original configuration, introduce one failure at a time, and restore the baseline after each drill.

## Pass criteria

Evidence distinguishes identity policies, SCPs, and resource policies; intended stack instances converge; an unrelated account has no access; recovery does not require broad permanent grants.

Save sanitized commands, measured results, and recovery evidence using [the evidence template](../../evidence-template.md). Completion requires the implemented path and failure path to pass; discussion-only extensions do not count as deployed validation.

## Cleanup

Detach only the lab SCP, remove StackSet instances before the StackSet, revoke shares, delete fixtures, and retain pre-existing organization/Identity Center/CDK bootstrap resources.

Confirm account, Region, resource prefix, ownership, and dependencies before deletion. Verify removal through read-only queries and account billing/resource views; note intentionally retained resources.

## Cost considerations

Approved organization administration and multiple accounts; resources incur charges per account/Region. Never enroll production accounts for this lab.

Budget alerts do not cap spending. Record a stop time and inspect retained resources after the session.

## Review questions

- What evidence distinguishes the failure from a similar symptom?
- Which identity and policy boundary control each action?
- What guarantees apply to ordering, retries, data consistency, or recovery?
- What changed in the measured behavior and cost?
- Which exercises were hands-on, simulated, or design-only?

