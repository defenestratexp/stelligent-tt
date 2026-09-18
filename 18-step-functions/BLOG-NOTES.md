# Blog Notes: Module 18, Step Functions

## Working title

Step Functions without the glue: JSONata, SDK integrations and error
handling you can unit test

## Hook

A Step Functions tutorial from 2022 has you write a Lambda function for
nearly every step, reshape data with `InputPath`, `Parameters`,
`ResultSelector`, `ResultPath` and `OutputPath`, and add a CloudTrail trail
so a "CloudWatch Events" rule can see S3 uploads. None of that is needed
now. JSONata (November 2024) replaces the five path fields with `Arguments`
and `Output`, SDK integrations call over two hundred AWS services without a
function in between, S3 sends events to EventBridge itself, and since
November 2025 the TestState API can mock a failure and tell you which
retrier or catcher handles it. This post rebuilds the course's "hello"
workflow the 2026 way and shows how much code goes away.

## Key points

1. **JSONata versus JSONPath.** Show one state both ways: `.$` keys and
   five path fields against `{% %}` expressions in `Arguments` and
   `Output`, plus `Assign` variables. The top-level default is still
   JSONPath if you leave `QueryLanguage` out, and you can mix the two state
   by state.
1. **Delete the glue function.** A Lambda that only calls `GetParameter` or
   `PutItem` becomes a Task with `arn:aws:states:::aws-sdk:ssm:getParameter`
   or the optimized `arn:aws:states:::dynamodb:putItem`. Less code, no
   runtime upgrades, and you pay only for the state transition.
1. **Retry and Catch belong in the definition.** Backoff, `MaxDelaySeconds`
   and `JitterStrategy: FULL`; catch permanent errors and record them; end
   in a Fail state so the run still shows as failed. Then redrive a
   Standard execution from the failed step after fixing the cause.
1. **Unit test the error paths.** `aws stepfunctions test-state` with
   `--mock` and `--state-configuration` returns `RETRIABLE` or
   `CAUGHT_ERROR`, the retry index and the backoff interval, with no role
   and no real call. That's a unit test that runs in a pipeline.
1. **Standard or Express is a semantics decision, not only a price one.**
   Exactly once with 90 days of history and one-year runs, against at least
   once (asynchronous) or at most once (synchronous), five minutes, and
   history only in CloudWatch Logs. Work the cost example at a million
   executions a month.
1. **Distributed Map** for S3-scale fan-out: a Standard parent listing a
   prefix, Express children, a concurrency cap and a failure threshold.

## Gotchas readers will hit

- Workflow type can't be changed. Changing `StateMachineType` in
  CloudFormation replaces the state machine, and a fixed
  `StateMachineName` makes that update fail.
- An Express workflow with logging off leaves no trace anywhere, and
  `start-sync-execution` from the console gives up after 60 seconds (the
  CLI and SDK wait the full five minutes).
- Step Functions can't generate IAM policies for SDK integrations; the
  first run fails with an access error until you add the action yourself.
- Error names differ by integration: `DynamoDB.` for the optimized
  integration, `DynamoDb.` for the SDK one, and SDK error names always end
  in `Exception` even when the service's API reference leaves it off
  (`S3.BucketAlreadyExistsException`).
- `States.ALL` doesn't catch `States.Runtime` or `States.DataLimitExceeded`,
  and must be alone and last. `States.TaskFailed` matches everything except
  `States.Timeout`.
- A JSONata expression that evaluates to nothing (a missing field) is an
  error (`States.QueryEvaluationError`), not an empty value.
- A variable assigned in a state isn't visible in that state's own
  `Output`; `Assign` and `Output` are evaluated in parallel.
- A workflow that writes back into the bucket and prefix that triggers it
  loops. Filter the EventBridge rule by prefix.
- Objects uploaded under a Distributed Map's prefix also match any
  EventBridge rule on the bucket unless the prefixes differ.
- Every retry and every redrive is a billable state transition.

<!-- VERIFY: confirm while doing Lab 18.3.3 that retrierRetryCount equal to
MaxAttempts makes test-state report CAUGHT_ERROR, before quoting it. -->

## Exam objectives

- DVA-C02 (→ C03) Domain 1: Task 1.1 (Skills 1.1.1 orchestration, 1.1.4
  synchronous and asynchronous patterns, 1.1.5 fault tolerance, 1.1.7 unit
  tests, 1.1.9 AWS APIs and SDKs, 1.1.12 EventBridge, 1.1.13 retry logic and
  error handling) and Task 1.2 (Skill 1.2.5)
- DVA-C02 Domain 4: Task 4.1 (Skills 4.1.2 and 4.1.7)
- SAA-C03 Domain 2: Task 2.1 (workflow orchestration with Step Functions,
  event-driven and serverless architectures) and Task 2.2
- SAA-C03 Domain 4: cost-optimized design (Standard versus Express pricing)
