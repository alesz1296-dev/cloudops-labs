# 14-advanced-networking-dns - Multi-VPC, IPv6, DNS, and network protection

Status: scenario defined; code and infrastructure not implemented.

## Objective and coverage

Explain a failed packet or DNS query across isolated network boundaries.

Exam domains: Networking and content delivery; Security. This scenario addresses gaps in the initial track; it does not establish complete exam coverage.

## Prerequisites

Complete [readiness](../../00-readiness/README.md). CloudOps-02 and CloudOps-07; an owned test domain for relevant DNS exercises. Do not purchase Direct Connect for a certification lab.

Use synthetic data and dedicated sandbox resources. Specify, review, and validate the resource plan before provisioning. Split larger scenarios into separate sessions. Record any design-only or simulated extension separately from hands-on evidence.

## Build

1. Peer two sandbox VPCs with nonoverlapping CIDRs, explicit routes, and narrow security rules; compare Transit Gateway behavior and review hybrid VPN/Direct Connect paths as diagrams unless an approved connection already exists.
2. Enable VPC Flow Logs and appropriate ELB/CloudFront access logs; correlate a bounded client request with transport and application observations.
3. Add an IPv6 subnet exercise and distinguish internet gateway, egress-only internet gateway, NAT, and endpoint routing; assess cost of each intended path.
4. Create isolated Route 53 routing-policy/health-check exercises and query logging; configure Resolver endpoint/rule forwarding only with an approved DNS target.
5. Add a scoped WAF test rule to a supported lab endpoint and inspect blocked-request logs; review Shield, DNS Firewall, and Network Firewall coverage through separate bounded or design exercises.
6. Compare Global Accelerator with CloudFront and collect network-monitoring evidence where service prerequisites are available.

## Failure drill

Remove one peer route, then block one direction with a NACL, then introduce a lab DNS record error. Run separately and explain what flow/query/access logs can and cannot prove.

Capture the original configuration, introduce one failure at a time, and restore the baseline after each drill.

## Pass criteria

Restored routes and DNS recover traffic, security-group/NACL differences are demonstrated, private addresses stay private, and design-only hybrid/protection extensions are labeled.

Save sanitized commands, measured results, and recovery evidence using [the evidence template](../../evidence-template.md). Completion requires the implemented path and failure path to pass; discussion-only extensions do not count as deployed validation.

## Cleanup

Remove routing records/checks, protection rules/logging, Resolver endpoints, peering, and owned networking in dependency order; check ENIs, public IPs, and retained logs.

Confirm account, Region, resource prefix, ownership, and dependencies before deletion. Verify removal through read-only queries and account billing/resource views; note intentionally retained resources.

## Cost considerations

Resolver endpoints, health checks, WAF, firewalls, NAT, Transit Gateway, Global Accelerator, and log ingestion can be significant; choose short independent sub-exercises.

Budget alerts do not cap spending. Record a stop time and inspect retained resources after the session.

## Review questions

- What evidence distinguishes the failure from a similar symptom?
- Which identity and policy boundary control each action?
- What guarantees apply to ordering, retries, data consistency, or recovery?
- What changed in the measured behavior and cost?
- Which exercises were hands-on, simulated, or design-only?

