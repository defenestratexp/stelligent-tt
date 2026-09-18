# Blog notes: module 01, CloudFormation

## Working title

One template, many regions: portable CloudFormation and an idempotent SDK
deployer

## Hook

The 2022 version of this lab asked for a stack in "each of the 4 American
regions", then "another US region", which doesn't exist: there are only
four commercial US regions. The fix is the actual lesson. The region list
belongs in configuration, the template takes everything region-specific
from parameters and pseudo-parameters, and the deployer must be safe to
run twice. In 2026 that last part is also what `aws cloudformation
deploy` and change sets do for you, so the post compares a hand-written
create-or-update loop with the tools that replaced it.

## Key points

- A portable template has no region, account ID or ARN in it:
  `AWS::Region`, `AWS::AccountId`, `AWS::Partition`, parameters with
  defaults, and conditions keyed on a "home region" parameter.
- Keep the region list in a config file, and filter it against the
  regions actually enabled in the account (`aws account list-regions`);
  opt-in regions and SCPs make "every region" a moving target.
- Idempotent SDK deployer: check whether the stack exists without using
  exceptions for control flow, create or update accordingly, and treat
  "No updates are to be performed" as success.
- `aws cloudformation deploy` does create-or-update through a change set;
  `describe-change-set` shows `Replacement: True` before you rename a
  bucket, not after.
- Day two: cfn-lint in the loop, drift detection for out-of-band changes,
  and the IaC generator for resources that were never in a template.
- Exports vs. IAM's global namespace: exports are regional, role names
  are account-wide, so a multi-region deploy of IAM resources collides.

## Gotchas readers will hit

- S3 bucket names are global; include region and account in the name or
  the second region fails.
- `update-stack` with no changes returns a `ValidationError`, not a
  no-op.
- Deleting stacks in creation order fails when one imports the other's
  export.
- Naming IAM resources requires `CAPABILITY_NAMED_IAM`.
- Drift detection only checks properties set explicitly in the template;
  a hand-enabled bucket versioning setting won't show up.
- Generated templates from the IaC generator come with deletion and
  replace policies worth reading before you import anything.
- `put-bucket-tagging` replaces the whole tag set.

## Exam objectives

- SOA-C03 Domain 3: Deployment, Provisioning, and Automation
- DOP-C02 Domain 2: Configuration Management and IaC (and Domain 1: SDLC
  Automation for the deployer)
- DVA-C02 Domain 3: Deployment
