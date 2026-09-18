# Blog Notes: Module 09, Lambda

## Working title

You don't need CloudTrail to react to S3 uploads: Lambda, EventBridge and
function URLs in 2026

## Hook

The 2022 version of this lab wired an S3 upload to a Lambda function the
long way round: create a CloudTrail trail, log S3 data events, and write a
"CloudWatch Events" rule on the `PutObject` API call. Today S3 sends its
own events to EventBridge once you tick one box on the bucket, a function
can have an HTTPS endpoint without API Gateway, and half the Lambda
tutorials online fail on current runtimes because they `require('aws-sdk')`
or target Python 3.7. This post rebuilds the lab on Python 3.13 and
EventBridge, compares the three ways to put HTTP in front of a function,
and then breaks the function on purpose to show where failed events go.

## Key points

1. **S3 to EventBridge, no trail.** Turn on EventBridge in the bucket's
   notification configuration, write a rule for `source: aws.s3`,
   `detail-type: Object Created` and your bucket name, and give
   `events.amazonaws.com` permission to invoke the function with a
   `SourceArn`. Compare it with direct S3 event notifications (free, one
   destination for overlapping event types and prefixes) and with the old
   CloudTrail route (a trail plus S3 data events, billed per 100,000).
1. **Three HTTP front doors.** Function URL (free, IAM or public, one
   function), HTTP API ($1.00/M, JWT authorizers, routes to many
   functions), REST API ($3.50/M, API keys and usage plans, WAF, caching,
   request validation, private endpoints). Show the resource count for each
   in CloudFormation.
1. **Public function URLs changed in October 2025.** They now need both
   `lambda:InvokeFunctionUrl` and `lambda:InvokeFunction` in the resource
   policy, ideally with the `lambda:InvokedViaFunctionUrl` condition. The
   console and SAM add both; hand-written CloudFormation from older posts
   gets a 403.
1. **Logs are a cost decision.** Declare the log group with a retention and
   point `LoggingConfig` at it, use JSON format and log levels, and scope
   the role to that one group. Lambda logs have been vended logs with
   tiered pricing since May 2025, and can go to S3 or Firehose directly.
1. **Know who retries.** Synchronous callers retry themselves; for async
   invocations Lambda retries twice and then sends the record to an
   on-failure destination (SQS, SNS, S3, Lambda, EventBridge). Reserved
   concurrency of 0 is a clean way to demonstrate throttling in any account.
1. **Powertools instead of home-grown helpers.** Logger, Metrics (EMF, no
   `PutMetricData` calls) and Idempotency, installed from the AWS-published
   layer whose ARN lives in a public SSM parameter, so the template never
   hard-codes it.

## Gotchas readers will hit

- CLI v2 `aws lambda invoke --payload '{...}'` fails with an invalid
  base64 error unless you add `--cli-binary-format raw-in-base64-out`.
- The log group Lambda creates on first invoke never expires, and deleting
  the function or the stack doesn't delete it. If the function runs before
  CloudFormation creates a log group of the same name, the stack update
  fails because the group already exists.
- API Gateway REST API changes don't go live until a new `Deployment`;
  CloudFormation doesn't make one just because a method changed.
- `AWS::Lambda::Version` publishes once. Changing the code doesn't publish
  a new version unless the resource is replaced.
- S3 events in EventBridge aren't free: they're opt-in data events at
  $1.00 per million. Still pennies, but not the "AWS events are free" line
  people repeat.
- EventBridge delivers at least once, so the writer must tolerate
  duplicates; a function that writes back into the bucket it listens to
  loops (Lambda's recursive loop detection stops some of these).
- Node.js runtimes ship SDK v3 only, and ES module handlers need `.mjs` or
  `"type": "module"`.
- Powertools Tracer depends on the X-Ray SDK, which went into maintenance
  mode in February 2026; new tracing work should use OpenTelemetry.
- A new account's Lambda concurrency quota may be lower than 1,000, so
  labs that reserve concurrency can fail with an "unreserved concurrency"
  error.

<!-- VERIFY: capture the exact error text for a public function URL that has only the lambda:InvokeFunctionUrl statement, and the HTTP status an HTTP API returns when its Lambda integration is throttled, while doing Labs 9.1.3 and 9.3.2. -->

## Exam objectives

- DVA-C02 (moving to C03) Domain 1: Development with AWS Services (Tasks
  1.1 and 1.2), Domain 2: Security (Task 2.1), Domain 3: Deployment
  (Tasks 3.1 and 3.4), Domain 4: Troubleshooting and Optimization (Tasks
  4.2 and 4.3)
- SAA-C03 Domain 2 (Task 2.1 loosely coupled architectures) and Domain 3
  (Task 3.2 elastic compute)
- SOA-C03 Domain 1 (Skill 1.2.2 EventBridge) and Domain 3: Deployment,
  Provisioning, and Automation
