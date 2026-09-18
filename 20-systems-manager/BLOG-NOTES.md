# Blog notes: Topic 20, Systems Manager

## Working title

Operations without SSH: running an EC2 fleet with Systems Manager and a
golden AMI pipeline in 2026

## Hook

Most tutorials stop at "use Session Manager instead of SSH" and then log in
to fix things by hand, which is the old habit without the port. The
CloudOps exam (SOA-C03) and real operations expect more: every session
logged, commands run across a fleet by tag with rate limits, desired state
enforced on a schedule, patches approved by policy and installed in a
window, procedures written as runbooks, and servers launched from an image
that was already patched and hardened. Systems Manager has also changed a
lot since most blog posts were written. Patch policies replaced patch groups
as the recommended setup, Change Manager and Incident Manager closed to new
customers, and in June 2026 the advanced-instances tier for non-EC2 servers
went away. This post builds the whole loop on two small instances for a
few dollars.

## Key points

1. **Session Manager is an audit tool as well as an access tool.** One
   preferences document per Region sends session logs to S3 and CloudWatch
   Logs, sets idle and maximum timeouts, and picks the Run As user.
   `ssm:SessionDocumentAccessCheck` limits a role to port forwarding only.
   Port forwarding through an instance to a private host replaces a bastion.
2. **Documents, targets, rate control.** Run Command, State Manager and
   Automation all run SSM documents against targets chosen by tag, with
   `max-concurrency` and `max-errors`. A narrow custom Command document with
   validated parameters is a better thing to hand a support team than
   `AWS-RunShellScript`.
3. **State Manager keeps things true.** An association fixes drift on a
   schedule and reports compliance. Inventory is itself an association, and
   resource data sync plus Athena turns it into a queryable record of the
   fleet.
4. **Patching is baseline + schedule + report.** A custom AL2023 baseline
   (approval delays, reject lists, compliance levels), a scan before
   installing, and a maintenance window that installs on dev only. Then
   compare the default baseline, patch groups and patch policies.
5. **Runbooks turn procedures into code.** Run AWS-owned runbooks across
   tagged targets with rate control and an execution preview. Then write a
   snapshot → patch → health-check runbook with a failure path and a
   Python 3.12 `aws:executeScript` step, and schedule it from the
   maintenance window.
6. **Golden AMIs close the loop.** An Image Builder pipeline takes its
   parent image from the AL2023 public parameter, applies `update-linux`,
   the STIG component and a custom component, tests the result, and writes
   the new AMI ID to an SSM parameter the fleet template reads. No AMI ID
   is ever typed by hand.

## Gotchas readers will hit

- The **instance** writes session logs, command output and inventory sync
  data, so the instance role needs the S3 and CloudWatch Logs permissions,
  not the person starting the session.
- Session preferences are per Region. A session in another Region isn't
  logged unless that Region has its own preferences document.
- Port-forwarding sessions aren't logged: Session Manager only carries the
  bytes.
- Remote-host port forwarding needs a network path from the instance to
  the target. With no inbound rules, it times out until you add a
  security-group-referencing rule.
- `ssm:StartSession` without `ssm:SessionDocumentAccessCheck` also grants
  the default shell document.
- Two inventory associations that both target by tag conflict and fail. The
  unified console's setup creates its own inventory association.
- Patch groups aren't offered in the console for account-Region pairs that
  never used them before patch policies arrived in December 2022.
- On AL2023, Patch Manager patches from the latest versioned repository,
  whatever release the instance is locked to.
- Image Builder component and recipe versions are immutable. Every change
  means a version bump in the template.
- Image Builder's service-linked role can write only parameters under
  `/imagebuilder/`. Use a custom execution role, which also keeps SCPs and
  RCPs in force.
- Deleting Image Builder resources, even the image, doesn't deregister the
  AMI or delete its snapshot. The output parameter survives stack deletion
  too.
- The advanced-instances tier no longer exists. Old posts and practice
  questions that mention it describe pricing before June 2026.

## Exam objectives supported

- SOA-C03 Domain 1: Skill 1.2.3 (custom and predefined Automation
  runbooks)
- SOA-C03 Domain 3: Skill 3.1.1 (AMIs with EC2 Image Builder) and
  Skill 3.2.1 (Systems Manager for operational automation)
- SOA-C03 Domain 4: Security and Compliance (session logging, patch
  compliance)
- DOP-C02 Domain 2: Task 2.3 (inventory, configuration and patch management
  at scale; State Manager)
- DOP-C02 Domains 5 and 6: configuration changes in response to events;
  automation for security controls

## Material to capture while doing the labs

- A session log excerpt from S3 next to the matching CloudTrail
  `StartSession` event (account ID redacted).
- The preferences JSON and the tunnel role's policy with its
  `SessionDocumentAccessCheck` condition.
- `describe-instance-patch-states` output for dev and prod before and after
  the maintenance window.
- The `<you>-SafePatch` runbook, and a screenshot of an execution that took
  the failure path.
- A diagram: public AL2023 parameter → Image Builder pipeline (update, STIG,
  custom component, test) → `/<you>/ami/al2023-hardened` → fleet stack.
- Build time and cost of one pipeline run, and the snapshot size of the
  resulting AMI.
