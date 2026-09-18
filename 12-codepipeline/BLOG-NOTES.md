# Blog Notes: Module 12, CodePipeline

## Working title

Protecting stateful resources in CodePipeline with change sets and manual
approval (2026 edition)

## Hook

A pipeline that can create your database can also drop it. Rename a
DynamoDB table in a CloudFormation template, push to `main`, and a
straight-through pipeline creates a new, empty table and deletes the old
one, data included, with every stage green. The classic defence is a
change set, a manual approval, and a person reading the change set before
it runs. The pattern still works in 2026, but the pipeline around it has
changed: the GitHub source is now a CodeConnections connection instead of
a personal access token, pipelines are V2 with triggers, variables and
stage rollback, and a V2 rollback turns out to be no help at all when the
thing you lost was data. This post rebuilds the pipeline and adds the
layers a tired approver needs.

## Key points

1. **Change set, approval, execute.** `CHANGE_SET_REPLACE`, a `Manual`
   approval action, `CHANGE_SET_EXECUTE`. `CHANGE_SET_REPLACE` makes a
   `CREATE` change set the first time (until it's executed, the new stack
   sits in `REVIEW_IN_PROGRESS`) and `UPDATE` ones after, so the old "first CREATE, then UPDATE" instructions are
   unnecessary. Show `describe-change-set` and the `Replacement` field
   (`True`, `False`, `Conditional`). Approve or reject from the CLI with
   `put-approval-result`. Approval actions now take `TimeoutInMinutes`
   (5 minutes to 60 days, default 7 days) and aren't billed on V2 while
   they wait.
1. **Layers that don't depend on the approver.** `DeletionPolicy` and
   `UpdateReplacePolicy: Retain`, DynamoDB `DeletionProtectionEnabled`, and
   a stack policy denying `Update:Replace` / `Update:Delete` on the table.
   Show which layer stops what, and at which point (change set creation,
   execution, cleanup).
1. **Automate the obvious check.** A V2 Commands action between
   CreateChangeSet and the approval that fails when any change has
   `Replacement: True`. The human then reviews what a query can't judge.
1. **Rollback isn't restore.** V2 stage rollback (`OnFailure: ROLLBACK`
   or `rollback-stage`) re-runs the stage with an earlier execution's
   artifacts and variables. After a table replacement that recreates the
   old *name*, not the old *data*. Rollback belongs on stateless stages;
   stateful ones need prevention and backups.
1. **The 2026 plumbing.** CodeConnections instead of a GitHub token (one
   console handshake, then everything by ARN, with
   `codeconnections:UseConnection` and `codestar-connections:UseConnection`
   on the pipeline role); V2 push triggers with file path filters so a
   monorepo doesn't redeploy the table on every README commit;
   `ExecutionMode: QUEUED` so a newer commit can't overtake the change set
   someone is reviewing.

## Gotchas readers will hit

- A connection created by the CLI or CloudFormation is `PENDING` until
  someone completes it in the console. A pipeline pointing at a pending
  connection fails at Source, and nothing about the error says "go to the
  console".
- Only the GitHub organization owner (or the repository owner, for a
  personal repository) can install the AWS Connector app.
- Connection ARNs made since July 2024 start `arn:aws:codeconnections:`;
  most examples still show `codestar-connections`. Grant both
  `UseConnection` actions or the pipeline fails with an access error.
- Adding a trigger turns off the source action's default change
  detection; `BranchName` is then only used for manual starts.
- The CloudFormation action's `RoleArn` isn't applied when executing a
  change set: the role given at change set creation is used. The pipeline
  role still needs `iam:PassRole` on it.
- Delete application stacks *before* the pipeline stack that owns their
  CloudFormation role, or the deletion fails for want of the role.
- The artifact bucket must be emptied before its stack can be deleted,
  and it grows with every execution unless it has a lifecycle rule.
- `Retain` works: after cleanup, retained tables (with deletion protection
  on) are still there, and still billing for storage.
- V2 billing is per action minute, rounded up per action. A pipeline with
  many short actions costs more than its wall-clock time suggests.

<!-- VERIFY: whether a StackPolicy in the template configuration file is
applied when the action mode is CHANGE_SET_REPLACE; confirm during Lab
12.2.4 before writing that section of the post. -->
<!-- VERIFY: whether the entry condition with a DeploymentWindow rule
fails immediately or waits for the window; record it in Lab 12.3.3. -->

## Exam objectives

- DOP-C02 Domain 1: SDLC Automation (Task 1.1 CI/CD pipelines, source
  integration, approvals; Task 1.2 automated testing in pipelines; Task
  1.4 deployment strategies and rollback)
- DOP-C02 Domain 2: Configuration Management and IaC (Task 2.1: change
  sets, protecting stateful resources)
- DVA-C02 → C03 Domain 3: Deployment (Task 3.4: deploy code with AWS
  CI/CD services, including rollbacks)
