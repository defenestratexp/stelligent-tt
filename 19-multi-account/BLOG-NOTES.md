# Blog notes: Topic 19, Multi-Account Foundation

## Working title

A two-account AWS setup for learning without fear: Organizations, SCPs and
a sandbox you can nuke

## Hook

Most people learning AWS do it in the same account that holds their real
things: a domain, a backup bucket, the credit card. So every experiment
comes with a small worry about what `terraform destroy` or a cleanup
script might hit. The 2022 version of this course got around that with a
company sandbox that was wiped every weekend. A solo learner in 2026 can
build the same thing in an afternoon for nothing: turn the existing
account into an organization's management account, create one lab
account under it, fence the lab account with a few guardrail policies,
and point every destructive tool at it and nowhere else.

## Key points

1. **The account is the blast radius.** Credentials for the lab account
   can't touch the management account, whatever a config file says. That
   makes aws-nuke safe in a way tags and naming conventions never are.
2. **Two ways in, used differently.** `OrganizationAccountAccessRole` is
   break-glass. IAM Identity Center plus `aws configure sso` (profile
   `lab`, region `us-east-2`) is for every day. Compare what CloudTrail
   records for each.
3. **SCPs set a ceiling and never grant.** A region guardrail
   (`us-east-2` + `us-east-1`), deny `LeaveOrganization`, protect
   CloudTrail and the break-glass role. Test each one both ways, and read
   the AccessDenied message, which names the policy type.
4. **RCPs are the other half (new since November 2024).** SCPs limit your
   principals; RCPs limit what anyone, including outsiders, can do to your
   resources. Show a TLS-only RCP on S3 and an organization identity
   perimeter.
5. **The management account is exempt, so keep it empty.** SCPs and RCPs
   don't apply there. Run the region test there and it succeeds.
6. **Control Tower is optional.** It's free itself but not what it turns
   on. Show what it would add (Config, CloudTrail, log archive and audit
   accounts, managed controls), what landing zone 4.0 made optional, and
   why a solo learner can skip it.

## Gotchas readers will hit

- Creating an organization ends Free Tier credits and moves the account
  to a paid plan (post-July-2025 Free Tier).
- If you enabled IAM Identity Center earlier, the console may already
  have created the organization. Check with `describe-organization`
  first.
- Every account needs a globally unique root email, forever. Plus
  addressing (`you+aws-lab@...`) solves it if your provider supports it.
- Closing an account isn't instant cleanup. The 90-day post-closure
  period keeps it counting against the default 10-account quota, and a
  newly created account can't be removed from the organization for four
  days.
- New accounts land in the root, not your OU, so root-attached policies
  hit them immediately. Test SCPs on an OU first.
- `list-policies-for-target` on the account doesn't show policies
  inherited from its OU.
- Your own protective SCP will block your own cleanup, e.g. deleting a
  trail. Plan a privileged-role exemption.
- The rebuy-de aws-nuke repository is archived. Use the ekristen fork,
  which needs an account alias and a blocklist.
- A region SCP can surprise you later with Bedrock cross-Region inference
  (module 28).
- A strict identity-perimeter RCP can block AWS log delivery that arrives
  as an AWS-owned account rather than a service principal.

## Exam objectives supported

- SAA-C03 Domain 1: Design Secure Architectures (multi-account strategy,
  SCPs)
- SOA-C03 Domain 4: Security and Compliance
- DOP-C02 Domain 6: Security and Compliance
- SAP-C02/C03 Domain 1: Design Solutions for Organizational Complexity
- SCS-C03 Domain 6: Security Foundations and Governance

## Material to capture while doing the labs

- Screenshot or paste of an SCP-caused AccessDenied message and an
  RCP-caused one, side by side.
- The `~/.aws/config` shape for `mgmt`, `lab-breakglass` and `lab`, with
  IDs redacted.
- A small diagram: management account (billing, identity, policies) →
  `Sandbox` OU → lab account, with arrows for SCP, RCP and RAM share.
- The aws-nuke dry-run output count before and after a module's labs.
