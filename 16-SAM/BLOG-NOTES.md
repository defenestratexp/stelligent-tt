# Blog Notes: Module 16, SAM

## Working title

Safe Lambda deployments with SAM and CodeDeploy hooks (2026 edition)

## Hook

Most "canary deploy your Lambda function" tutorials still ship a hook
that starts with `require('aws-sdk')`, including the sample in the
CodeDeploy user guide. Put that on a current Node.js runtime and the hook
dies with a missing-module error before it can report back, and
CodeDeploy then sits waiting for an hour before it fails the deployment.
The pattern itself is better than ever: two lines of SAM
(`AutoPublishAlias` and `DeploymentPreference`) give you versions, an
alias, a CodeDeploy application, gradual traffic shifting, test hooks and
automatic rollback on a CloudWatch alarm. This post rebuilds it for Node.js
22 and the v3 SDK, and shows the rollback actually happening.

## Key points

1. **What SAM generates.** `AutoPublishAlias: live` adds an
   `AWS::Lambda::Version` and an `AWS::Lambda::Alias`, and points your
   event sources at the alias. `DeploymentPreference` adds a CodeDeploy
   application, a deployment group with auto-rollback on failure, alarm
   and manual stop, and a service role. Show the processed template.
1. **Canary vs linear, and who waits.** The predefined types
   (`Canary10Percent5Minutes`, `Linear10PercentEvery1Minute`, ...) map to
   `CodeDeployDefault.Lambda*` configurations. CloudFormation holds the
   stack in `UPDATE_IN_PROGRESS` on the alias until CodeDeploy finishes,
   so `sam deploy` (and your pipeline) waits for the whole canary.
1. **Hooks in SDK v3.** A pre-traffic hook invokes the new *version*
   directly (the alias still points at the old one), checks the result,
   and must call `PutLifecycleEventHookExecutionStatus`. Default to
   `Failed`, catch errors and always report, so a crash fails fast
   instead of after an hour.
1. **Alarms catch what hooks miss.** One alarm on the alias's `Errors`,
   one on the new version's (`ExecutedVersion`). Demo: a bug that only
   fires with a query string, which the hooks don't send; real traffic
   trips the alarm and CodeDeploy moves the alias back.
1. **Where `sam sync` fits.** It updates code through the Lambda API and
   moves the alias directly, skipping CloudFormation and CodeDeploy, so no
   hooks and no alarms. Great for a dev stack, never for production.

## Gotchas readers will hit

- Hook functions must be named `CodeDeployHook_*`: the
  `AWSCodeDeployRoleForLambda` managed policy on the role SAM generates
  only allows invoking functions with that prefix. Otherwise, supply your
  own role with `DeploymentPreference.Role`.
- The hook's execution role needs `codedeploy:PutLifecycleEventHookExecutionStatus`
  on the deployment group and `lambda:InvokeFunction` on the new version;
  SAM doesn't add either.
- A deployment that changes only a stack parameter (for example an
  environment variable set with `!Ref`) publishes no new version and moves
  no alias; the change lands on `$LATEST` only. `AutoPublishAliasAllProperties`
  doesn't help; the `AWS::LanguageExtensions` transform does.
- The very first deployment has nothing to shift from. Deploy with
  `AutoPublishAlias` first, then add `DeploymentPreference`.
- Alarm dimensions must match what Lambda publishes (`FunctionName` plus
  `Resource`, plus `ExecutedVersion` for the version alarm), or the alarm
  never gets data and never fires. `TreatMissingData: notBreaching`
  matters at lab traffic levels.
- Alarms only matter during the deployment. A bug that surfaces an hour
  later is not rolled back by CodeDeploy.
- `sam delete` leaves the `aws-sam-cli-managed-default` stack, and its
  bucket is versioned: deleted artifacts linger as noncurrent versions
  until you empty the bucket, versions and all.
- `sam local` needs the variable declared in the template before
  `--env-vars` can override it, and containers can't reach `localhost`
  services; a shared Docker network (`--docker-network`) fixes both
  DynamoDB Local and cross-platform endpoint differences.

<!-- VERIFY: capture the exact error the old v2 hook logs on nodejs22.x
(expected: Runtime.ImportModuleError, Cannot find module 'aws-sdk') and
how long CodeDeploy waits before failing, while doing Lab 16.4.3. -->

## Exam objectives

- DVA-C02 (→ C03) Domain 3: Deployment, Task 2 (Lambda versions and
  aliases, deploying a SAM template to another environment) and Task 4
  (deployment strategies such as canary, rollbacks)
- DVA-C02 (→ C03) Domain 1: Development with AWS Services, Task 1 (testing
  with AWS SAM) and Task 2 (Lambda)
- DOP-C02 Domain 1: SDLC Automation, Task 1.4 (deployment strategies for
  serverless environments, troubleshooting deployments)
- DOP-C02 Domain 2: Configuration Management and IaC, Task 2.1 (AWS SAM
  templates)
