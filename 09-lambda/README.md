# Topic 9: Lambda

<!-- TOC -->

- [Topic 9: Lambda](#topic-9-lambda)
  - [What changed in the 2026 edition](#what-changed-in-the-2026-edition)
  - [Exam coverage](#exam-coverage)
  - [Cost and cleanup](#cost-and-cleanup)
  - [Guidance](#guidance)
  - [Conventions](#conventions)
  - [Lesson 9.1: Lambda is a fully-managed compute resource](#lesson-91-lambda-is-a-fully-managed-compute-resource)
    - [Principle 9.1](#principle-91)
    - [Practice 9.1](#practice-91)
      - [Lab 9.1.1: Simple Lambda function](#lab-911-simple-lambda-function)
        - [Question: Where the logs went](#question-where-the-logs-went)
      - [Lab 9.1.2: The same function in CloudFormation](#lab-912-the-same-function-in-cloudformation)
        - [Question: What the role allows](#question-what-the-role-allows)
      - [Lab 9.1.3: A function URL](#lab-913-a-function-url)
        - [Question: Two permissions](#question-two-permissions)
      - [Lab 9.1.4: Lambda behind API Gateway](#lab-914-lambda-behind-api-gateway)
        - [Question: REST API or HTTP API](#question-rest-api-or-http-api)
        - [Question: Function URL or API Gateway](#question-function-url-or-api-gateway)
      - [Lab 9.1.5: Package and deploy with the CLI](#lab-915-package-and-deploy-with-the-cli)
        - [Question: Whose SDK](#question-whose-sdk)
    - [Retrospective 9.1](#retrospective-91)
      - [Task: Other ways to build it](#task-other-ways-to-build-it)
  - [Lesson 9.2: Lambda and other AWS resources](#lesson-92-lambda-and-other-aws-resources)
    - [Principle 9.2](#principle-92)
    - [Practice 9.2](#practice-92)
      - [Lab 9.2.1: Lambda with DynamoDB](#lab-921-lambda-with-dynamodb)
        - [Question: Keys for this table](#question-keys-for-this-table)
      - [Lab 9.2.2: S3 events through EventBridge](#lab-922-s3-events-through-eventbridge)
        - [Question: No trail needed](#question-no-trail-needed)
        - [Question: Delivered twice](#question-delivered-twice)
      - [Lab 9.2.3: Query data with Lambda and API Gateway](#lab-923-query-data-with-lambda-and-api-gateway)
        - [Question: Query, not Scan](#question-query-not-scan)
      - [Lab 9.2.4: Powertools for AWS Lambda](#lab-924-powertools-for-aws-lambda)
        - [Question: What Powertools replaced](#question-what-powertools-replaced)
    - [Retrospective 9.2](#retrospective-92)
      - [Question: Reacting to change](#question-reacting-to-change)
  - [Lesson 9.3: Invocations, failures and scale](#lesson-93-invocations-failures-and-scale)
    - [Principle 9.3](#principle-93)
    - [Practice 9.3](#practice-93)
      - [Lab 9.3.1: Asynchronous invocation and destinations](#lab-931-asynchronous-invocation-and-destinations)
        - [Question: Who retries](#question-who-retries)
      - [Lab 9.3.2: Concurrency and throttling](#lab-932-concurrency-and-throttling)
        - [Question: A throttled caller](#question-a-throttled-caller)
      - [Lab 9.3.3: Versions and aliases](#lab-933-versions-and-aliases)
        - [Question: Pointing at an alias](#question-pointing-at-an-alias)
      - [Lab 9.3.4: Clean up the module](#lab-934-clean-up-the-module)
    - [Retrospective 9.3](#retrospective-93)
      - [Question: Cold starts](#question-cold-starts)
      - [Question: When not Lambda](#question-when-not-lambda)
  - [Further Reading](#further-reading)

<!-- /TOC -->

## What changed in the 2026 edition

- **Cloud9 is gone.** The 2022 principle pointed at Cloud9 for testing;
  Cloud9 is closed to new customers. You test in the Lambda console, with
  `aws lambda invoke`, and over HTTP. Local emulation with `sam local`
  belongs to module 16.
- **Current runtimes.** Labs use Python 3.13 (3.12 is fine) or Node.js 22.
  Node.js code uses the AWS SDK for JavaScript v3, the only SDK included
  in the Node.js 18 and later runtimes; tutorials that
  `require('aws-sdk')` fail on them.
- **S3 events reach Lambda through EventBridge directly.** The old Lab
  9.2.2 created a CloudTrail trail so a "CloudWatch Events" rule could see
  `PutObject` calls. S3 now sends events to EventBridge itself once you
  turn it on for the bucket. No trail and no CloudTrail data-event
  charges; EventBridge bills S3 events at its data-event rate instead.
- **Function URLs** (new Lab 9.1.3) give a function an HTTPS endpoint
  without API Gateway. Since October 2025 a new function URL needs both
  `lambda:InvokeFunctionUrl` and `lambda:InvokeFunction` in the function's
  resource-based policy, which catches out older examples.
- **API Gateway: HTTP API and REST API.** Lab 9.1.4 still builds the REST
  API from the old lab, then builds the same thing as an HTTP API so you
  can compare what each costs and offers.
- **Every function gets a log group with a retention period**, declared in
  the template and wired up with the function's `LoggingConfig` (JSON log
  format, log levels). Lambda's own log groups never expire by default.
- **Powertools for AWS Lambda** (new Lab 9.2.4) for structured logging and
  metrics, installed from the AWS-published layer whose ARN you read from a
  public SSM parameter.
- **DynamoDB design moved to module 22.** This module keeps the small table
  the function writes to, and points to Lesson 22.4 for key design.
- **New Lesson 9.3** on what the Developer exam asks about most:
  synchronous and asynchronous invocation, retries, on-failure
  destinations, concurrency and throttling, versions and aliases.
- The retrospective's Claudia.js and Aegis links are gone (both projects
  are inactive). It now compares CloudFormation with SAM (module 16) and
  CDK (module 25).
- Labs run in your lab account in `us-east-2` through the `lab` profile,
  and the module ends with a cleanup lab.

## Exam coverage

| Exam | Domain / task statement |
|---|---|
| DVA-C02 → C03 | Domain 1: Development with AWS Services (Task 1.1: develop code for applications hosted on AWS: event-driven architecture, synchronous and asynchronous patterns, idempotency; Task 1.2: develop code for AWS Lambda: configuration, event sources, destinations, error handling, concurrency; Task 1.3: use data stores in application development). C03 guide publishes 2026-10-27 and adds GenAI / agent topics |
| DVA-C02 → C03 | Domain 2: Security (Task 2.1: authentication and authorization: execution roles, resource-based policies, IAM-authenticated function URLs) |
| DVA-C02 → C03 | Domain 3: Deployment (Task 3.1: prepare application artifacts: deployment packages, layers; Task 3.4: deploy code: versions and aliases) |
| DVA-C02 → C03 | Domain 4: Troubleshooting and Optimization (Task 4.2: instrument code for observability: structured logging, embedded metric format; Task 4.3: optimize applications: concurrency, memory) |
| SAA-C03 | Domain 2: Design Resilient Architectures (Task 2.1: design scalable and loosely coupled architectures: Lambda, API Gateway, EventBridge) |
| SAA-C03 | Domain 3: Design High-Performing Architectures (Task 3.2: high-performing and elastic compute solutions) |
| SAA-C03 | Domain 4: Design Cost-Optimized Architectures (Task 4.2: cost-optimized compute solutions) |
| SOA-C03 | Domain 1: Monitoring, Logging, Analysis, Remediation, and Performance Optimization (Lambda logs and metrics; Skill 1.2.2: use EventBridge to route events and troubleshoot rules) |
| SOA-C03 | Domain 3: Deployment, Provisioning, and Automation (packaging and deploying Lambda with CloudFormation) |

## Cost and cleanup

Everything in this module is pay-per-use. Left idle, it costs close to
nothing; the things that keep billing are storage and logs. Prices are for
`us-east-2` in September 2026.

- **Lambda:** $0.20 per million requests and about $0.0000167 per
  GB-second (x86). The always-free tier of 1 million requests and 400,000
  GB-seconds a month covers everything here many times over. Since August
  2025 the initialization (cold start) phase is billed too, which at lab
  scale is still nothing.
- **Provisioned concurrency and SnapStart** for Python bill while they're
  configured. No lab turns them on; if you experiment, remove them.
- **Function URLs** have no charge of their own.
- **API Gateway:** HTTP APIs are $1.00 and REST APIs $3.50 per million
  requests. New accounts get 1 million calls a month of each for 12
  months. A few hundred test calls cost a fraction of a cent either way.
- **DynamoDB** on-demand at lab scale costs fractions of a cent, and a few
  kilobytes of storage sit inside the 25 GB always-free allowance.
- **EventBridge:** S3 events are "opt-in data events", billed at $1.00 per
  million. AWS management events on the default bus are free.
- **SQS** (the on-failure destination in Lesson 9.3): the first million
  requests a month are free.
- **S3:** the upload bucket and the packaging bucket hold a few kilobytes.
- **CloudWatch Logs:** Lambda logs are billed as vended logs, starting at
  $0.50 per GB ingested. Every log group in this module gets a 7-day
  retention. The ones Lambda creates for you (the console function in Lab
  9.1.1, for example) never expire until you set a retention or delete
  them. That is the usual reason a Lambda lab keeps billing cents a month
  forever.
- **Cleanup:** [Lab 9.3.4](#lab-934-clean-up-the-module) removes
  everything this module created and checks for leftovers.

## Guidance

- Explore the official docs! See the
  [AWS Lambda Developer Guide](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html),
  the [API Gateway Developer Guide](https://docs.aws.amazon.com/apigateway/latest/developerguide/welcome.html),
  the [EventBridge User Guide](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html),
  the [Lambda](https://docs.aws.amazon.com/cli/latest/reference/lambda/index.html)
  and [API Gateway v2](https://docs.aws.amazon.com/cli/latest/reference/apigatewayv2/index.html)
  CLI references, and the CloudFormation reference for
  [AWS::Lambda::Function](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-lambda-function.html),
  [AWS::Lambda::Url](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-lambda-url.html),
  [AWS::Lambda::Permission](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-lambda-permission.html),
  [AWS::ApiGateway::RestApi](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-apigateway-restapi.html)
  and
  [AWS::ApiGatewayV2::Api](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-apigatewayv2-api.html).

- Avoid using other sites like stackoverflow.com for answers \-- part
  of the skill set you're building is finding answers straight from
  the source, AWS. Many Lambda tutorials use runtimes that were retired
  years ago (Python 3.7, Node.js 12) and the v2 JavaScript SDK.

- Explore your curiosity. Try to understand why things work the way
  they do. Read more of the documentation than just what you need to
  find the answers.

## Conventions

- **Profile and Region.** Everything runs in the lab account with the `lab`
  profile, in `us-east-2`. CLI examples don't pass `--region`.
- **Names.** Stack names, function names and log groups start with your
  identifier, shown here as `<you>`: `<you>-lambda-hello`,
  `<you>-lambda-events`, `/stelligent-u/<you>/lab09/hello`. Tag everything
  with `owner=<you>`.
- **Language.** The labs are written for Python 3.13. Node.js 22 is fine
  if you prefer it: use ES modules (`.mjs`) and the v3 SDK clients, such as
  `@aws-sdk/client-dynamodb` and `@aws-sdk/lib-dynamodb`. Whichever you
  choose, use it for the whole module.
- **Templates and code live next to your answers.** Keep your templates
  (`hello.yaml`, `events.yaml`) and function code in your copy of this
  directory. Every template must pass `cfn-lint`. There are no starter
  files: write each resource from the CloudFormation reference.
- **CLI v2 and payloads.** `aws lambda invoke` in CLI v2 treats
  `--payload` as base64 unless you pass `--cli-binary-format
  raw-in-base64-out` (or set it once with `aws configure set
  cli-binary-format raw-in-base64-out --profile lab`).
- DO continuously commit all your templates and code to the topic
  folder in your GitHub repo.

## Lesson 9.1: Lambda is a fully-managed compute resource

### Principle 9.1

*As a fully managed compute resource, Lambda can reduce all the time and
effort to configure and maintain virtual servers.*

Lambda runs your code on demand with very little configuration and no
servers to patch. You provide a handler, a runtime, a memory size and a
role; Lambda runs as many copies as there are requests and bills for the
milliseconds they run. Lambda can be paired with API Gateway, or given a
function URL of its own, to put a small HTTP service in front of the
world.

API Gateway is a fully managed service that makes it easy to create,
publish, maintain, monitor, and secure APIs at any scale. You can create
an API that acts as a "front door" for applications to access data or
functionality from your back-end services, such as workloads running on
EC2, code running on AWS Lambda, or any web application. It comes in two
flavors for this kind of work, REST APIs and HTTP APIs, which you'll
compare.

### Practice 9.1

You'll create one function by hand to see the moving parts, then build it
in CloudFormation with its log group and a role that can do only what it
needs. You'll call it three ways over HTTPS (a function URL, a REST API
and an HTTP API) and then move the code out of the template and deploy it
with `aws cloudformation package`.

#### Lab 9.1.1: Simple Lambda function

Create and test a simple AWS Lambda function using the Lambda console.
The console is the quickest way to see everything a function has; the
rest of the module uses CloudFormation and the CLI.

- Create a function named `<you>-console-hello` from scratch with the
  Python 3.13 (or Node.js 22) runtime, and let the console create a basic
  execution role.

- Update the function to return "Hello AWS!" and use the **Test** tab to
  run it with a test event you create.

- Invoke it from your terminal with
  [`aws lambda invoke`](https://docs.aws.amazon.com/cli/latest/reference/lambda/invoke.html),
  then again with `--log-type Tail` and decode the `LogResult`.

- Review the options you have for testing and running functions:
  shareable test events, the console's code editor, and the
  [ways to invoke a function](https://docs.aws.amazon.com/lambda/latest/dg/lambda-invocation.html).

- When you're done, delete the function **and** its role.

##### Question: Where the logs went

_Find this function's logs with `aws logs tail`. Which log group are they
in, who created it, and what is its retention? Is it gone now that you
deleted the function? (Delete it if not.)_

#### Lab 9.1.2: The same function in CloudFormation

Write `hello.yaml` and deploy it as `<you>-lambda-hello`:

- An `AWS::Lambda::Function` with the same "Hello AWS!" code inline
  (`Code.ZipFile`), the `python3.13` runtime, 128 MB of memory and a short
  timeout.

- An `AWS::Logs::LogGroup` named `/stelligent-u/<you>/lab09/hello` with a
  7-day retention. Point the function at it with
  [`LoggingConfig`](https://docs.aws.amazon.com/lambda/latest/dg/monitoring-cloudwatchlogs-advanced.html),
  and set the log format to JSON with an application log level of `INFO`.

- An execution role (`AWS::IAM::Role`) with a trust policy for
  `lambda.amazonaws.com` and an inline policy that allows
  `logs:CreateLogStream` and `logs:PutLogEvents` **on that log group
  only**, not the `AWSLambdaBasicExecutionRole` managed policy.

Invoke it with the CLI and read the logs with `aws logs tail`. Log a
message at `DEBUG` and one at `INFO` from your code: which ones arrive?

##### Question: What the role allows

_Read the [execution role](https://docs.aws.amazon.com/lambda/latest/dg/lambda-intro-execution-role.html)
page. What would `AWSLambdaBasicExecutionRole` have let this function do
that your inline policy doesn't? Which principal does the trust policy
name, and what would happen if another service could assume this role?_

#### Lab 9.1.3: A function URL

A [function URL](https://docs.aws.amazon.com/lambda/latest/dg/urls-configuration.html)
is a dedicated HTTPS endpoint for one function, with no API in front of
it.

- Change the function so it reads a `name` from the query string and
  returns `Hello <name>!` as JSON. Function URL events use the same
  [payload format](https://docs.aws.amazon.com/lambda/latest/dg/urls-invocation.html)
  as HTTP APIs (version 2.0).

- Add an `AWS::Lambda::Url` with `AuthType: AWS_IAM`, and output its URL.

- Call it with plain `curl`. What do you get back?

- Call it again, signed with SigV4. `curl` can sign requests itself with
  `--aws-sigv4 "aws:amz:us-east-2:lambda"`; export your `lab` session's
  temporary credentials first with
  `aws configure export-credentials --profile lab --format env` and pass
  the session token in an `x-amz-security-token` header. Look at
  `requestContext.authorizer.iam` in the event your function received.

- Now try `AuthType: NONE` in a second, throwaway function URL: read
  [Control access to Lambda function URLs](https://docs.aws.amazon.com/lambda/latest/dg/urls-auth.html)
  and add the two `AWS::Lambda::Permission` statements a public URL needs,
  using `FunctionUrlAuthType` and `InvokedViaFunctionUrl`. Call it from a
  browser. Then **remove the public URL and both permissions** before you
  move on: an open URL on a function that scales automatically is a bill
  anyone can run up.

##### Question: Two permissions

_Why does a public function URL need both `lambda:InvokeFunctionUrl` and
`lambda:InvokeFunction`, and what does the `lambda:InvokedViaFunctionUrl`
condition prevent? If you had used the console instead of CloudFormation,
who would have added those statements? What does IAM Access Analyzer say
about the function while the public URL exists?_

#### Lab 9.1.4: Lambda behind API Gateway

Use API Gateway to run the same function, first as a REST API (as in the
2022 course), then as an HTTP API.

- Add a REST API to `hello.yaml` that calls the function with a Lambda
  proxy integration on `GET /hello`. You will need to implement:

  - `AWS::ApiGateway::RestApi` (a `REGIONAL` endpoint)
  - `AWS::ApiGateway::Resource` and `AWS::ApiGateway::Method`
  - `AWS::ApiGateway::Deployment` and `AWS::ApiGateway::Stage`
  - Appropriate Lambda invoke permissions (`AWS::Lambda::Permission`),
    with a `SourceArn` that limits them to this API

- Call the API with `curl`. Then use `aws apigateway test-invoke-method`
  to call the method without deploying.

- Add an HTTP API that does the same thing: `AWS::ApiGatewayV2::Api`,
  `AWS::ApiGatewayV2::Integration` (payload format 2.0),
  `AWS::ApiGatewayV2::Route` and an auto-deploying `$default`
  `AWS::ApiGatewayV2::Stage`, plus its own `AWS::Lambda::Permission`.

- Your function now receives three event shapes (function URL, REST API
  payload 1.0, HTTP API payload 2.0). Make it read `name` correctly from
  each, and return a proper proxy response (`statusCode`, `headers`,
  `body`).

- Functions can take a JSON payload as input. Add a `POST /echo` route to
  the HTTP API that returns the JSON body it was sent, or one item from it.

##### Question: REST API or HTTP API

_Read [Choose between REST APIs and HTTP APIs](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-vs-rest.html).
Which features would push you to a REST API (name at least four), and
what does an HTTP API give you in return? How many resources did each
take in your template, and why did the REST API need a new `Deployment`
before a change went live?_

##### Question: Function URL or API Gateway

_Read [Select a method to invoke your Lambda function using an HTTP
request](https://docs.aws.amazon.com/lambda/latest/dg/furls-http-invoke-decision.html).
When is a function URL enough? Name three things you'd lose compared with
API Gateway (think throttling, custom domains, authorizers, WAF, routing
to several functions)._

#### Lab 9.1.5: Package and deploy with the CLI

Use the AWS CLI to deploy the function's code from a file instead of
inline:

- Move the in-line code to a separate file (for example
  `src/hello/app.py`) and point the function's `Code` at that directory.

- Create an S3 bucket for deployment packages (`<you>-lab09-artifacts`,
  or reuse one from an earlier module) and use
  [`aws cloudformation package`](https://docs.aws.amazon.com/cli/latest/reference/cloudformation/package.html)
  and `aws cloudformation deploy` to update the stack. Look at the
  template `package` wrote and at what it uploaded.

- Call the HTTP API to confirm it's working.

##### Question: Whose SDK

_The Python runtime includes boto3 and the Node.js runtime includes the
v3 JavaScript SDK. Read the note on runtime-included SDKs in [Lambda
runtimes](https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html).
Why does AWS recommend packaging the SDK with your code once you're no
longer using inline code? What could change under you if you don't?_

### Retrospective 9.1

#### Task: Other ways to build it

You wrote a lot of YAML for one function and two APIs. Look at how the
same thing is expressed in the
[AWS Serverless Application Model](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html)
(module 16), in the [AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/home.html)
(module 25) and in [Chalice](https://github.com/aws/chalice) (Python).
Which of the resources you wrote by hand does SAM generate for you, and
what does that save you from getting wrong?

## Lesson 9.2: Lambda and other AWS resources

### Principle 9.2

*Lambda can interact with other AWS services when using the appropriate
execution policies.*

Coupling Lambda with native AWS services allows you to create powerful
code very quickly. Other services can invoke your function when something
happens (an object lands in S3, a rule matches an event), and your
function can call other services with the permissions its role grants and
no more.

### Practice 9.2

You'll build a small event log: every object uploaded to a bucket becomes
an item in a DynamoDB table, written by a function that EventBridge
invokes. A second function, behind the HTTP API, returns the events for a
bucket. Then you'll replace hand-rolled logging with Powertools for AWS
Lambda.

Build this lesson in a new template, `events.yaml`, deployed as
`<you>-lambda-events`.

#### Lab 9.2.1: Lambda with DynamoDB

- Add an `AWS::DynamoDB::Table` named `<you>-lab09-events`, on-demand
  (`PAY_PER_REQUEST`), with `DeletionPolicy: Delete`. Design its keys for
  the question Lab 9.2.3 will ask: "all the events for one bucket, newest
  first". If you've done module 22, this is Lab 22.4.1 in miniature.

- Add a function, `<you>-lab09-writer`, with its own log group and an
  execution role that allows `dynamodb:PutItem` on that table and nothing
  else. Pass the table name in an environment variable.

- Have it take a small JSON input (for example `bucket`, `key`, `size`)
  and put an item. Create the SDK client outside the handler.

- Test it with `aws lambda invoke` and confirm the items with
  `aws dynamodb query`.

##### Question: Keys for this table

_What are your partition key and sort key, and why? What would go wrong
with the object key as the partition key? Why is the SDK client created
outside the handler?_

#### Lab 9.2.2: S3 events through EventBridge

In 2022 this lab needed a CloudTrail trail so that a rule could see S3
`PutObject` API calls. You don't need one now:
[S3 sends events to EventBridge](https://docs.aws.amazon.com/AmazonS3/latest/userguide/EventBridge.html)
itself once you turn it on for the bucket.

- Add an S3 bucket (`<you>-lab09-uploads`) to the stack, with the
  defaults from module 02 (Block Public Access, ACLs disabled), and turn
  on EventBridge delivery in its `NotificationConfiguration`.

- Add an `AWS::Events::Rule` on the default event bus that matches
  `Object Created` events from `aws.s3` for that bucket only, and targets
  the writer function. Write the pattern from a real sample event (see
  [EventBridge event message structure](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ev-events.html))
  and check it with `aws events test-event-pattern` before you deploy.

- Add the `AWS::Lambda::Permission` that lets `events.amazonaws.com`
  invoke the function, limited by `SourceArn` to your rule.

- Modify the handler to record some of the event data: bucket, key, size,
  the event `time` and the event `id`.

- Upload a few files with `aws s3 cp` and check that the function logged
  them to the table.

##### Question: No trail needed

_Compare three ways to run code when an object is uploaded: an EventBridge
rule on S3's own events (this lab), an
[S3 event notification](https://docs.aws.amazon.com/AmazonS3/latest/userguide/EventNotifications.html)
straight to Lambda, and a rule on "AWS API Call via CloudTrail" events
(the 2022 lab). For each: what does it cost, how is filtering done, how
many targets can one event reach, and what else must exist for it to
work?_

##### Question: Delivered twice

_EventBridge invokes Lambda asynchronously and delivers events at least
once. What happens in your table if the same event arrives twice? Change
the write so that a duplicate is harmless (look at condition expressions,
or at what makes a good sort key). What would make your function call
itself in a loop? Read [recursive loop
detection](https://docs.aws.amazon.com/lambda/latest/dg/invocation-recursion.html):
would Lambda catch a loop that goes through EventBridge?_

#### Lab 9.2.3: Query data with Lambda and API Gateway

Write another Lambda function that will query the DynamoDB table:

- The function takes a bucket name and returns all the events for it,
  newest first, using `Query` with a key condition, never `Scan`.

- Give it a role that allows `dynamodb:Query` on the table only.

- Add an HTTP API to `events.yaml` with a `GET /events/{bucket}` route
  that calls the function, and call it with `curl`.

- Return a clean JSON response. What do you do about DynamoDB's number
  types when you serialize them?

##### Question: Query, not Scan

_How much read capacity does your query consume for one bucket with 20
events, compared with a `Scan` of the whole table? What would you add if
the API needed "all events in the last hour, across every bucket"?
(Lesson 22.4 covers secondary indexes.)_

#### Lab 9.2.4: Powertools for AWS Lambda

[Powertools for AWS Lambda](https://docs.aws.amazon.com/powertools/python/latest/)
is an AWS-maintained library for the things every function ends up doing:
structured logging, metrics, idempotency, parsing and routing events.
It's available for Python, TypeScript, Java and .NET.

- Add the Powertools layer to both functions in `events.yaml`. Don't paste
  a layer ARN into your template: AWS publishes the current ARN in a
  public SSM parameter (see the
  [installation page](https://docs.aws.amazon.com/powertools/python/latest/getting-started/install/)),
  which you can read with a `{{resolve:ssm:...}}` dynamic reference.

- Replace your logging with Powertools
  [Logger](https://docs.aws.amazon.com/powertools/python/latest/core/logger/):
  inject the Lambda context, log the S3 key as a structured field, and set
  the service name with an environment variable.

- Use [Metrics](https://docs.aws.amazon.com/powertools/python/latest/core/metrics/)
  to publish an `ObjectsRecorded` metric (and the object size) in the
  `StudentU/<you>` namespace, then find it in CloudWatch. No
  `PutMetricData` permission is needed; ask yourself why.

- Optional: make the writer idempotent with the
  [Idempotency](https://docs.aws.amazon.com/powertools/python/latest/utilities/idempotency/)
  utility, keyed on the EventBridge event `id`, and compare it with the
  conditional write you wrote for "Delivered twice".

- Query the logs with Logs Insights (module 08), filtering on your
  structured fields.

##### Question: What Powertools replaced

_Compare Powertools Logger's output with Lambda's own JSON log format from
Lab 9.1.2. What does each add? How do the metrics reach CloudWatch
without an API call, and what would they cost at a million invocations a
day? Powertools Tracer uses the X-Ray SDK, which entered maintenance mode
in February 2026; what does AWS recommend for tracing instead?_

### Retrospective 9.2

#### Question: Reacting to change

_Can you think of practical ways an organization can use Lambda in
reaction to AWS resource changes? For two of them, name the event source,
whether it needs a CloudTrail trail, and what the function's role must be
allowed to do. When would you reach for an AWS Config rule or a Systems
Manager Automation runbook (modules 26 and 20) instead of your own
function?_

## Lesson 9.3: Invocations, failures and scale

### Principle 9.3

*How a function is invoked decides who retries it when it fails and where
a failed event ends up. Design for failure before the first one happens.*

### Practice 9.3

A synchronous caller (the CLI, API Gateway, a function URL) waits for the
result and handles errors itself. An asynchronous caller (EventBridge, S3,
SNS, `--invocation-type Event`) hands the event to Lambda's internal
queue, and Lambda retries it. Concurrency limits apply to both. These labs
make a function fail and throttle on purpose, so you can see what each
kind of caller experiences, and then publish versions so a change can be
rolled back.

Read [How Lambda handles errors and retries with asynchronous
invocation](https://docs.aws.amazon.com/lambda/latest/dg/invocation-async-error-handling.html)
first.

#### Lab 9.3.1: Asynchronous invocation and destinations

- Make the writer function raise an error when the object key starts
  with `fail/`.

- Add an SQS queue to `events.yaml` and an
  [`AWS::Lambda::EventInvokeConfig`](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-lambda-eventinvokeconfig.html)
  that sends failed invocations to it as an
  [on-failure destination](https://docs.aws.amazon.com/lambda/latest/dg/invocation-async-retain-records.html).
  Set the retry attempts and the maximum event age explicitly. The
  function's role needs `sqs:SendMessage` on the queue.

- Upload `fail/test.txt`. Watch the attempts arrive in the logs, and
  read the invocation record from the queue with `aws sqs receive-message`.

- Invoke the function directly with the CLI, synchronously and then with
  `--invocation-type Event`, with a payload that fails. Compare what the
  CLI tells you each time.

##### Question: Who retries

_How many times did Lambda run the function for the failed upload, and
how far apart? EventBridge has its own
[retry policy and dead-letter queue](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-rule-dlq.html)
for targets: when does that one apply, and when does the Lambda one? Why
is an on-failure destination more useful than a function-level
dead-letter queue?_

#### Lab 9.3.2: Concurrency and throttling

- Run `aws lambda get-account-settings`. What is your account's
  concurrency limit, and how much of it can you reserve? New accounts
  can start below the default of 1,000.
  <!-- VERIFY: current documented behaviour for reduced Lambda concurrency quotas on new accounts; the Lambda concurrency page only states the 1,000 default. -->

- Set the writer's reserved concurrency to 0 in the template (reserving
  zero works whatever your account limit is). Upload a file, and invoke
  the query function's API route after setting its reserved concurrency to
  0 too.

- Look at the `Throttles` metric for both functions, and at where the
  throttled upload event ended up.

- Put the reserved concurrency back (remove the property) and confirm both
  work again.

##### Question: A throttled caller

_What did `curl` receive from the HTTP API while the query function was
throttled, and what happened to the throttled S3 event? When would you set
reserved concurrency deliberately (think of a downstream database with a
connection limit), and how is it different from provisioned
concurrency?_

#### Lab 9.3.3: Versions and aliases

- Add an `AWS::Lambda::Version` and an `AWS::Lambda::Alias` named `live`
  for the query function, and point the HTTP API integration (and its
  permission) at the alias instead of the function.

- Change the function's response slightly and publish a second version.
  Configure the alias to send 10% of traffic to the new version with
  `RoutingConfig`, call the API a few dozen times, and count the
  responses.

- Roll back by pointing the alias at the first version only.

Read [Lambda function versions](https://docs.aws.amazon.com/lambda/latest/dg/configuration-versions.html)
and [aliases](https://docs.aws.amazon.com/lambda/latest/dg/configuration-aliases.html).
Module 16 automates this with SAM and CodeDeploy.

##### Question: Pointing at an alias

_Why does `AWS::Lambda::Version` need a new logical ID (or a changed
description) to publish a new version from CloudFormation? What breaks
if the API's permission names the function but the integration calls the
alias? Which of your function's settings are frozen in a version, and
which apply to all of them?_

#### Lab 9.3.4: Clean up the module

Delete everything this module created:

- Empty `<you>-lab09-uploads` (including any object versions), then delete
  the `<you>-lambda-events` stack. The table, queue, rule, functions,
  API and log groups go with it.

- Delete the `<you>-lambda-hello` stack. If you created the public
  function URL outside the stack, delete it and its permissions.

- Empty and delete `<you>-lab09-artifacts` if you created it for this
  module.

- Delete the log groups Lambda created by itself, starting with
  `/aws/lambda/<you>-console-hello` from Lab 9.1.1, and the console
  function's role if you didn't already.

- Check that nothing is left:
  `aws lambda list-functions`,
  `aws logs describe-log-groups --log-group-name-prefix /aws/lambda/<you>`
  and `--log-group-name-prefix /stelligent-u/<you>/lab09`,
  `aws apigatewayv2 get-apis`, `aws apigateway get-rest-apis`,
  `aws events list-rules`, `aws dynamodb list-tables`,
  `aws sqs list-queues` and `aws s3 ls`.

- Custom metrics from Lab 9.2.4 can't be deleted; they stop appearing
  two weeks after their last data point and bill only while data arrives.

### Retrospective 9.3

#### Question: Cold starts

_What happens in the init phase of the [execution environment
lifecycle](https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtime-environment.html),
and why has it been billed for managed runtimes since August 2025? Compare
three ways to reduce cold starts: smaller packages and less work at init,
[SnapStart](https://docs.aws.amazon.com/lambda/latest/dg/snapstart.html)
(Python 3.12 and later, with a cost) and provisioned concurrency. Which
would you use for the query API, and which for the writer?_

#### Question: When not Lambda

_Lambda functions run for at most 15 minutes, scale per request and bill
per millisecond. Read the
[Fargate or Lambda](https://docs.aws.amazon.com/decision-guides/latest/decision-guides/fargate-or-lambda.html)
decision guide. Name a workload you'd move off Lambda, and say where it
would go (ECS in module 13, Step Functions in module 18, or Lambda's own
[durable functions](https://docs.aws.amazon.com/lambda/latest/dg/durable-functions.html)
for long-running workflows)._

## Further Reading

- [Best practices for working with AWS
  Lambda functions](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)
- [Serverless Land](https://serverlessland.com/), maintained by AWS, has
  patterns (including EventBridge and API Gateway ones) and workshops.
- [Control which events invoke your Lambda
  function](https://docs.aws.amazon.com/lambda/latest/dg/invocation-eventfiltering.html):
  event filtering for event source mappings (SQS, Kinesis, DynamoDB
  Streams), which module 22 uses on a stream.
- [Lambda recursive loop
  detection](https://docs.aws.amazon.com/lambda/latest/dg/invocation-recursion.html)
- [Sending Lambda function logs to Amazon
  S3](https://docs.aws.amazon.com/lambda/latest/dg/logging-with-s3.html)
  and [to Firehose](https://docs.aws.amazon.com/lambda/latest/dg/logging-with-firehose.html),
  for when CloudWatch Logs isn't the right place to keep them.
- [Migrating from X-Ray instrumentation to OpenTelemetry
  instrumentation](https://docs.aws.amazon.com/xray/latest/devguide/xray-sdk-migration.html)
- Read about [Capital One's Cloud Custodian project](https://cloudcustodian.io/)
  and see how it uses AWS Lambda to react to resource changes.
