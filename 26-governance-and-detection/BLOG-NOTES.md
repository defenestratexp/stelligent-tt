# Blog notes: Topic 26, Governance and Detection

## Working title

Five AWS security services, one lab account, zero surprise bills:
CloudTrail, Config, GuardDuty, Inspector and the two Security Hubs in 2026

## Hook

The 2022 version of this course never switched on AWS Config, GuardDuty,
Security Hub or Inspector, yet all four are named in the 2026 CloudOps,
DevOps Pro and Security Specialty exam guides. They've also changed
underneath anyone studying from older material. Security Hub is now two
products: the original was renamed Security Hub CSPM, and a new, unified
Security Hub correlates findings into exposures and bills per resource.
Config can record daily, which sounds cheaper but costs four times as much
per item. Inspector Classic is gone, CloudTrail Lake closed to new
customers in May 2026, and GuardDuty now links findings into attack
sequences. The post walks through turning all of it on in one lab
account, seeing it work with sample findings and deliberately broken S3
buckets, and turning it all off again before the free trials end.

## Key points

1. **CloudTrail first, and out of reach.** An organization trail from the
   management account logs the lab account, which can see it but can't
   stop it. Two layers do the protecting: the organization trail's own
   rules and the module 19 SCP. Event history is free for 90 days;
   Lake is closed to new customers, so the post uses trails and Athena.
2. **Config cost is a design decision.** Record two resource types, not
   everything. Daily recording costs $0.012 per CI against $0.003 for
   continuous, so it only saves money for resources that change more
   than four times a day. Use per-type overrides.
3. **Rules, Guard and remediation.** Managed rules, a custom rule in
   CloudFormation Guard with no Lambda, an SSM Automation runbook that
   turns versioning back on, and a small conformance pack. Then show the
   drift it causes in the CloudFormation stack that created the bucket.
4. **GuardDuty is one call to enable; routing is the work.** Sample
   findings, an EventBridge rule with numeric matching to SNS, and a
   suppression rule. Suppressed findings don't reach EventBridge or
   Security Hub and aren't used by Extended Threat Detection.
5. **Inspector re-scans when a CVE appears.** An old base image against a
   current one in ECR, and a Lambda function with a pinned vulnerable
   dependency whose finding closes when you upgrade.
6. **Security Hub vs Security Hub CSPM.** What each is, what enabling the
   new one creates for you (service-linked Config recorders, including
   one in `us-east-1`, and a service-linked Access Analyzer), and why a
   delegated administrator in a Security Tooling account is the real-world
   answer.

## Gotchas readers will hit

- The trials differ: GuardDuty 30 days, Security Hub Essentials 30 days,
  Security Hub CSPM 30 days, **Inspector 15 days**, Config none. Each is
  per account and per Region.
- Only one customer-managed Config recorder per Region, and Security Hub
  adds service-linked recorders next to it. Cleanup has to find both.
- Daily recording delays change-triggered rules (and Security Hub CSPM
  change-triggered controls) by up to 24 hours. Override to continuous
  for the types your labs test.
- Security Hub CSPM enabled on its own depends on your Config recorder;
  a narrow recorder produces `WARNING` control findings and a failed
  Config.1. With the new Security Hub also on, CSPM uses its own
  service-linked recorder instead.
- Enabling Security Hub in `us-east-2` creates a recorder for global
  resources in `us-east-1`. A region SCP that denied `us-east-1` would
  get in the way.
- Automatic remediation changes resources behind CloudFormation's back;
  the stacks drift.
- A leftover module 08 trail in the lab account makes the organization
  trail a paid second copy, and the module 19 SCP stops you deleting it
  without the privileged-role exemption.
- Delegated administrators: Security Hub won't accept the management
  account as its administrator, and each service registers differently
  (AWS Config needs two service principals).

## Exam objectives supported

- SOA-C03 Domain 4: Security and Compliance (Skills 4.1.2, 4.1.5, 4.2.5)
- SOA-C03 Domain 3: Deployment, Provisioning, and Automation (Skill 3.2.1)
- DOP-C02 Domain 4: Monitoring and Logging (Task 4.2); Domain 5: Incident
  and Event Response (Task 5.2); Domain 6: Security and Compliance (Tasks
  6.2, 6.3)
- SCS-C03 Domain 1: Detection (Tasks 1.1, 1.2); Domain 2: Incident
  Response (Skills 2.1.4, 2.2.3); Domain 6: Security Foundations and
  Governance (Skills 6.1.4, 6.2.1, Task 6.3)

## Material to capture while doing the labs

- The organization trail's S3 key layout, with the organization and
  account IDs redacted.
- The `stop-logging` AccessDenied from the lab account.
- `describe-configuration-recorders` output before and after enabling
  Security Hub, showing the service-linked recorders.
- A small cost table: CIs recorded, rule evaluations and trial days left,
  from the real bill at the end of the module.
- The GuardDuty alert email from the EventBridge input transformer.
- Inspector finding counts for the old and current base images.
- A diagram of the "real organization" answer to Retrospective 26.5:
  Log Archive, Security Tooling and workload accounts, with arrows for
  where each service's data lands.
