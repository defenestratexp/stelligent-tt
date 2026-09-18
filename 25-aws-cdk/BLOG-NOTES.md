# Blog notes: Topic 25, AWS CDK in Python

## Working title

CDK in 2026 for people who already know CloudFormation: bootstrap,
aspects, tests, and the stack `cdk destroy` leaves behind

## Hook

The 2022 version of this course taught CloudFormation, SAM and
Terraform, and skipped the tool many AWS teams now use to write
CloudFormation. The CDK has moved a lot since most tutorials were
written: the CLI split from the library and jumped to version 2.1000,
it needs Node 22, it sends telemetry unless you opt out, `cdk diff`
builds a change set, and there are new commands for drift, garbage
collection, refactoring without replacement and orphaning resources.
cdk-nag 3 stopped being an aspect. And CDK for Terraform was archived
in December 2025, so "CDK" now means the AWS one. The post builds a small
Python app from `cdk init` to a GitHub Actions deploy, compares every step
with the CloudFormation and Terraform versions from earlier in the
series, and ends with the cleanup most tutorials skip: the bootstrap
stack and its retained bucket.

## Key points

1. **It's still CloudFormation.** `cdk synth` needs no AWS credentials
   for an environment-agnostic stack; the output is a template you can
   lint, diff and read. Side-by-side table: CloudFormation, CDK,
   Terraform for state, preview, reuse, import, drift, refactor, tests.
2. **Bootstrapping is infrastructure you now own.** What `CDKToolkit`
   creates (bucket, ECR repository, five roles, an SSM parameter), why
   the execution role is `AdministratorAccess` by default, and how
   `--cloudformation-execution-policies` and `--trust` change that.
3. **Read what an L3 creates before you deploy it.** One line of
   `ApplicationLoadBalancedFargateService` synthesizes 37 resources,
   including two NAT gateways and two Elastic IPs. Synthesis is a free
   cost review.
4. **Aspects for guardrails, tested first.** A read-only aspect that
   fails synthesis on a missing tag or an old Lambda runtime, with the
   pytest spec written before the code. Aspect priorities, and why a
   test `App()` doesn't see the feature flags in `cdk.json`.
5. **cdk-nag 3.x.** `Validations.of(app).add_plugins(...)` and
   `acknowledge(...)` replace `Aspects` and `NagSuppressions`. What
   `grant_read` generates and why nag flags it.
6. **Adopting CDK without replacing things.** `cdk import` for a
   hand-made bucket, `cdk migrate` for a CloudFormation template (all
   L1), and `cdk refactor` for renames. Then a deploy role for GitHub
   Actions that can only assume the bootstrap roles.

## Gotchas readers will hit

- L2 buckets, and the log groups CDK now creates for Lambda functions,
  default to `RETAIN`; `cdk destroy` leaves them. `auto_delete_objects`
  adds a custom resource Lambda to empty the bucket.
- Deleting `CDKToolkit` leaves its versioned staging bucket (Retain),
  and fails on the ECR repository if it still has images. Leaving the
  bucket then blocks the next `cdk bootstrap`, which wants the same name.
  <!-- VERIFY: the exact failure when re-bootstrapping with the old
  staging bucket still present. -->
- Bootstrap once per account **and Region**; the error when you forget
  names the missing `/cdk-bootstrap/hnb659fds/version` parameter.
- Renaming a construct ID changes the logical ID and replaces the
  resource. `cdk diff` shows it; `cdk refactor` (preview) can fix it.
- The deadly embrace: removing a cross-stack reference fails, because the
  producer drops the export before the consumer stops importing it.
  Two deploys with `export_value`.
- Context lookups are cached in `cdk.context.json`, which you should
  commit, and which contains your account ID. Scrub it for a public repo.
- `cfn-lint` warns (W3005) about `DependsOn` the CDK generates.
- cdk-nag examples on the web are mostly v2 and won't import under v3.
- `cdk gc` and `cdk refactor` need `--unstable=...`; `cdk migrate` is
  preview.
- Python test apps need a fresh `App` per test; synthesizing twice after
  changing the tree raises `ConstructTreeModifiedAfterSynth`.

## Exam objectives supported

- SOA-C03 Domain 3: Deployment, Provisioning, and Automation (Skill
  3.1.2: CloudFormation and the AWS CDK; Skill 3.1.3: deployment issues;
  Skill 3.1.6: Terraform, for the comparison)
- DVA-C02 Domain 3: Deployment (Task 3.1; Skills 3.3.4, 3.4.3, 3.4.7);
  Domain 1, Skill 1.1.7 (unit tests). Map to DVA-C03 when its guide
  publishes on 2026-10-27.
- DOP-C02 Domain 2: Configuration Management and IaC (Task 2.1: CDK named
  twice); Domain 1: SDLC Automation (Tasks 1.1, 1.2)

## Material to capture while doing the labs

- `describe-stack-resources` for `CDKToolkit`, with the account ID
  redacted.
- The synthesized template for the L1 bucket next to the L2 bucket.
- Resource counts for the L3 pattern, and the per-day cost estimate.
- Terminal output of a synthesis failed by the guardrail aspect, and the
  cdk-nag report before and after acknowledgments.
- The deadly-embrace error message verbatim.
- `cdk diff` output for a construct rename, and the `cdk refactor
  --dry-run` output for the same change.
- The GitHub Actions run log, and the IAM policy of the deploy role.
- The cleanup sequence for the bootstrap stack, with the errors you get
  if you do it in the wrong order.
