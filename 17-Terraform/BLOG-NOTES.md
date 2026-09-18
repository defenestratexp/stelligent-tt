# Blog Notes: Module 17, Terraform

## Working title

Terraform state on S3 without DynamoDB: `use_lockfile`, and the rest of
what changed since the 2022 tutorials

## Hook

For years, every "Terraform on AWS" guide started with the same
bootstrap: an S3 bucket for state and a DynamoDB table with a `LockID`
hash key for locking. Since Terraform 1.11 (February 2025) the table is
unnecessary. `use_lockfile = true` makes the S3 backend write a
`.tflock` object next to the state with an S3 conditional write, and the
DynamoDB arguments are deprecated. The same old tutorials also put
`version` in the `provider` block, write `tags { }` as a block, hard-code
AMI IDs and edit state with `terraform import` and `terraform state mv`
at a prompt. This post rebuilds the bootstrap the 2026 way, shows the
lock working, and ends with how to remove a versioned state bucket
cleanly, which most guides skip.

## Key points

1. **The new backend block.** `required_providers` in a `terraform {}`
   block, then `backend "s3"` with `encrypt = true` and `use_lockfile =
   true`. Show the lock error from a second terminal, the `.tflock`
   object in `list-objects-v2`, and `-lock-timeout`.
2. **How the lock works.** `PutObject` with `If-None-Match: *` succeeds
   only if the object doesn't exist; the lock is released by deleting
   it. IAM needs `s3:GetObject`, `s3:PutObject` and `s3:DeleteObject` on
   `<key>.tflock`. Migrating from DynamoDB: set both during the
   transition, then drop the table.
3. **Versioning is still your backup, and it collects junk.** Every lock
   and state write leaves a noncurrent version and a delete marker. A
   lifecycle rule on noncurrent versions keeps the history you need
   without keeping it forever.
4. **Change existing infrastructure in code.** `import` blocks (with
   `-generate-config-out`), `moved` blocks and `removed` blocks with
   `destroy = false` replace the old state-surgery commands with changes
   that show up in a plan and a pull request.
5. **Guardrails and tests.** Variable validation, preconditions and
   postconditions, `check` blocks (warnings, not errors) and
   `terraform test` with `mock_provider`, which runs with no AWS
   credentials at all.
6. **The licence question.** Terraform 1.6+ is BSL 1.1; OpenTofu is the
   MPL 2.0 fork in the CNCF, supports the same S3 locking, and adds
   client-side state encryption. Everything in the post works with both.

## Gotchas readers will hit

- `terraform init -migrate-state` is what moves local state into S3; a
  plain `init` after adding the backend asks the same question but is
  easy to answer wrong in a script.
- Backend blocks can't use variables or locals. Use literal values or
  `-backend-config` files.
- A state bucket that holds its own state can't be destroyed from that
  state. Migrate the state back to local first.
- `aws s3 rm --recursive` on a versioned bucket only adds delete
  markers. Emptying it means deleting every version and delete marker,
  or `force_destroy = true` applied *before* the destroy.
- A `terraform test` run with `command = plan` fails if a `check`
  block's data source depends on a value only known after apply. Under
  a mock provider, `command = apply` is free and evaluates it.
- The AWS provider marks SSM parameter values sensitive, so an output
  of an AMI ID read from SSM needs `sensitive = true` or
  `nonsensitive()`.
- Workspace state goes to `env:/<workspace>/<key>` in the bucket, so an
  IAM policy scoped to the key alone won't cover workspaces.
- Terraform doesn't roll back a failed apply. CloudFormation users
  expect it to.

<!-- VERIFY: capture the exact lock error text and the .tflock JSON while doing Lab 17.2.3, for the post. -->

## Exam objectives

- SOA-C03 Domain 3: Deployment, Provisioning, and Automation (Skill
  3.1.6: third-party tools such as Terraform and Git)
- DOP-C02 Domain 2: Configuration Management and IaC (Task 2.1) and
  Domain 1: SDLC Automation (Task 1.2: automated testing in pipelines)
