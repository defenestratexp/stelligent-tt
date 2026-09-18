# Topic 18: Step Functions

<!-- TOC -->

- [Topic 18: Step Functions](#topic-18-step-functions)
  - [What changed in the 2026 edition](#what-changed-in-the-2026-edition)
  - [Exam coverage](#exam-coverage)
  - [Cost and cleanup](#cost-and-cleanup)
  - [Guidance](#guidance)
  - [Lesson 18.1: Introduction to Step Functions](#lesson-181-introduction-to-step-functions)
    - [Principle 18.1](#principle-181)
    - [Practice 18.1](#practice-181)
      - [Lab 18.1.1: Build a State Machine in Workflow Studio](#lab-1811-build-a-state-machine-in-workflow-studio)
        - [Question: Pass State](#question-pass-state)
        - [Question: States](#question-states)
      - [Lab 18.1.2: The Same State Machine in CloudFormation](#lab-1812-the-same-state-machine-in-cloudformation)
        - [Question: Three Ways to Ship a Definition](#question-three-ways-to-ship-a-definition)
      - [Lab 18.1.3: JSONPath and JSONata](#lab-1813-jsonpath-and-jsonata)
        - [Question: Input and Output](#question-input-and-output)
        - [Question: Variables or Output?](#question-variables-or-output)
    - [Retrospective 18.1](#retrospective-181)
      - [Question: Why a State Machine?](#question-why-a-state-machine)
  - [Lesson 18.2: Tasks and Service Integrations](#lesson-182-tasks-and-service-integrations)
    - [Principle 18.2](#principle-182)
    - [Practice 18.2](#practice-182)
      - [Lab 18.2.1: A Lambda Task](#lab-1821-a-lambda-task)
        - [Question: What Came Back](#question-what-came-back)
      - [Lab 18.2.2: No Lambda Required](#lab-1822-no-lambda-required)
        - [Question: Who Writes the Policy?](#question-who-writes-the-policy)
        - [Question: Activity State Machine](#question-activity-state-machine)
    - [Retrospective 18.2](#retrospective-182)
      - [Question: Service Integrations](#question-service-integrations)
  - [Lesson 18.3: Handling Errors with Retry and Catch](#lesson-183-handling-errors-with-retry-and-catch)
    - [Principle 18.3](#principle-183)
    - [Practice 18.3](#practice-183)
      - [Lab 18.3.1: Retry a Flaky Task](#lab-1831-retry-a-flaky-task)
        - [Question: What the Retries Cost](#question-what-the-retries-cost)
      - [Lab 18.3.2: Catch What Retry Can't Fix](#lab-1832-catch-what-retry-cant-fix)
        - [Question: Wildcards](#question-wildcards)
      - [Lab 18.3.3: Unit Test the Error Handling](#lab-1833-unit-test-the-error-handling)
        - [Question: What a Mock Proves](#question-what-a-mock-proves)
      - [Lab 18.3.4: Redrive a Failed Execution](#lab-1834-redrive-a-failed-execution)
        - [Question: What Ran Again](#question-what-ran-again)
    - [Retrospective 18.3](#retrospective-183)
      - [Question: Retry in the Workflow or in the Code?](#question-retry-in-the-workflow-or-in-the-code)
  - [Lesson 18.4: Events and Workflow Types](#lesson-184-events-and-workflow-types)
    - [Principle 18.4](#principle-184)
    - [Practice 18.4](#practice-184)
      - [Lab 18.4.1: Start an Execution from an S3 Upload](#lab-1841-start-an-execution-from-an-s3-upload)
        - [Question: No Trail Needed](#question-no-trail-needed)
      - [Lab 18.4.2: An Express Workflow](#lab-1842-an-express-workflow)
        - [Question: Twice](#question-twice)
        - [Question: A Million Uploads](#question-a-million-uploads)
      - [Lab 18.4.3: Distributed Map (Optional)](#lab-1843-distributed-map-optional)
        - [Question: Why Not Express All the Way Down?](#question-why-not-express-all-the-way-down)
      - [Lab 18.4.4: Clean Up](#lab-1844-clean-up)
    - [Retrospective 18.4](#retrospective-184)
      - [Question: Workflows](#question-workflows)
      - [Question: Other Events](#question-other-events)
  - [Further Reading](#further-reading)

<!-- /TOC -->

## What changed in the 2026 edition

- The console's "Author with code snippets" editor is gone. Lab 18.1.1 uses
  **Workflow Studio** (Design, Code and Config modes, and the **Test state**
  button), then Lab 18.1.2 moves the definition into CloudFormation, where
  the rest of the module works.
- New Lab 18.1.3 covers **JSONata**, the query language Step Functions
  added in November 2024, next to the original JSONPath. JSONata states use
  `Arguments`, `Output` and `Assign` instead of `InputPath`, `Parameters`,
  `ResultSelector`, `ResultPath` and `OutputPath`. The rest of the module is
  written in JSONata; you should still be able to read JSONPath, because
  most existing workflows and examples use it.
- Lesson 18.2 adds **direct AWS SDK integrations**. The Lambda task stays,
  but Lab 18.2.2 replaces "glue" Lambda functions with optimized
  (`arn:aws:states:::dynamodb:putItem`) and SDK
  (`arn:aws:states:::aws-sdk:ssm:getParameter`) integrations.
- New Lesson 18.3 on error handling: `Retry` with backoff, `MaxDelaySeconds`
  and jitter, `Catch` with `$states.errorOutput`, unit tests with the
  **TestState API** and its mocks (November 2025), and **redrive**.
- Lesson 18.4 starts executions from S3 through **Amazon EventBridge**
  directly. The old lab created a CloudTrail trail and a "CloudWatch Events"
  rule to see S3 uploads; S3 has sent events to EventBridge itself since
  2021, so there is no trail.
- New labs compare **Standard and Express** workflows by running the same
  definition as both, and an optional **Distributed Map** lab processes a
  prefix of S3 objects with Express child workflows.
- Lambda code uses Python 3.13. Labs run in the lab account with the `lab`
  profile (`us-east-2`), and resource names include your identifier.

## Exam coverage

| Exam | Domain / task statement |
|---|---|
| DVA-C02 → C03 | Domain 1: Development with AWS Services (Task 1.1: Skill 1.1.1 architectural patterns such as orchestration and choreography, 1.1.4 synchronous and asynchronous patterns, 1.1.5 fault-tolerant and resilient applications, 1.1.7 unit tests, 1.1.9 interact with AWS services through APIs and SDKs, 1.1.12 EventBridge event-driven patterns, 1.1.13 retry logic and error-handling patterns; Task 1.2, Skill 1.2.5: integrate Lambda functions with AWS services). C03 guide publishes 2026-10-27 and adds GenAI / agent topics |
| DVA-C02 → C03 | Domain 4: Troubleshooting and Optimization (Task 4.1, Skills 4.1.2 interpret logs and traces and 4.1.7 debug service integration issues) |
| SAA-C03 | Domain 2: Design Resilient Architectures (Task 2.1: design scalable and loosely coupled architectures: workflow orchestration with AWS Step Functions, event-driven architectures, serverless patterns; Task 2.2: distributed design patterns) |
| SAA-C03 | Domain 4: Design Cost-Optimized Architectures (choosing Standard or Express by pricing model) |

## Cost and cleanup

- **Nothing in this module has an hourly charge.** State machines, EventBridge
  rules, Lambda functions and an on-demand DynamoDB table cost nothing while
  idle. You pay for use, and lab use is pennies.
- **Standard workflows** are billed per **state transition**: $0.025 per 1,000
  after the first 4,000 each month, which are free. Every retry counts as a
  transition, and so does a redrive. A Distributed Map costs one transition
  per item.
  <!-- VERIFY: the pricing page lists the per-transition price for US East
  (N. Virginia) only; confirm us-east-2 is the same. -->
- **Express workflows** are billed per **request** ($1.00 per million) and
  **duration** ($0.00001667 per GB-second for the first 1,000 GB-hours, in
  64 MB memory steps, rounded up to 100 ms). There is no free tier. The labs
  run a few hundred executions at most: well under a cent.
- **CloudWatch Logs:** Express workflows keep no execution history unless you
  log to CloudWatch Logs, and logging level `ALL` with execution data is
  chatty. Step Functions logs are billed at the CloudWatch vended-logs
  ingestion rate (about $0.50 per GB at the first tier); set a retention
  period on every log group you create.
- **Lambda, DynamoDB on demand, S3 and a standard Parameter Store parameter**
  stay within free-tier or fractions-of-a-cent territory at lab scale.
- [Lab 18.4.4](#lab-1844-clean-up) removes everything: stacks, the bucket's
  objects, log groups, the parameter and the role the console created in
  Lab 18.1.1.

## Guidance

- Explore the official docs! See the AWS Step Functions
  [Developer Guide](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html),
  [API Reference](https://docs.aws.amazon.com/step-functions/latest/apireference/Welcome.html),
  [CLI Reference](https://docs.aws.amazon.com/cli/latest/reference/stepfunctions/index.html),
  and
  [CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-stepfunctions-statemachine.html)
  docs, and the
  [Amazon States Language specification](https://states-language.net/spec.html).

- Avoid using other sites like stackoverflow.com for answers \-- part
  of the skill set you're building is finding answers straight from
  the source, AWS.

- Explore your curiosity. Try to understand why things work the way
  they do. Read more of the documentation than just what you need to
  find the answers.

- Work in your lab account with the `lab` profile from module 19
  (`export AWS_PROFILE=lab`). The profile sets the lab region, `us-east-2`,
  so the commands in this module don't need `--region`. The
  [Step Functions console](https://console.aws.amazon.com/states/home?region=us-east-2)
  is worth keeping open: its execution graph is the fastest way to see what
  a workflow did. Build with CloudFormation and the CLI from Lab 18.1.2 on.

- Keep your definitions in your lab repository. Write them in YAML inside
  the template (`Definition:`) or as a separate `.asl.json` file, and run
  `cfn-lint` before every deploy. `cfn-lint` checks the definition against
  the States Language schema too.

- Name everything `<your-id>-lab18-...`. Examples in this module use the
  placeholder account `123456789012`; build real ARNs with `!Sub` and
  `!GetAtt`, never by hand.

## Lesson 18.1: Introduction to Step Functions

### Principle 18.1

*A state machine turns the steps of a process, and what happens between
them, into a definition you can read, version and watch run.*

### Practice 18.1

Step Functions coordinates the parts of an application as a *state machine*
(a *workflow*): a set of states, each of which does some work (`Task`),
makes a decision (`Choice`), waits (`Wait`), runs branches or items in
parallel (`Parallel`, `Map`), shapes data (`Pass`), or ends the run
(`Succeed`, `Fail`). You write it in the JSON-based
[Amazon States Language](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-amazon-states-language.html)
(ASL). Every *execution* records each state it entered and left, with its
input and output, so you can see exactly where a run went wrong.

You'll build the first state machine visually, then move the same
definition into CloudFormation, then look at the two ways to move data
between states.

#### Lab 18.1.1: Build a State Machine in Workflow Studio

[Workflow Studio](https://docs.aws.amazon.com/step-functions/latest/dg/workflow-studio.html)
is the editor in the Step Functions console (it also runs inside
Infrastructure Composer and the AWS Toolkit for VS Code). It has three
modes: **Design** (drag states onto a canvas), **Code** (edit the ASL with
a live graph) and **Config** (name, type, role, logging).

In the console, create a state machine from a blank template:

- Choose **JSONata** as the query language when the console asks (AWS
  recommends it for new workflows).

- In **Config** mode, name it `<your-id>-lab18-hello`, keep the type
  **Standard**, and let the console create a new execution role. Write down
  the role's name; you'll delete it in Lab 18.1.2.

- In **Design** mode, add a single **Pass** state.

- Give the Pass state an **Output** that takes an input property named
  `executioner` and returns:

  ```json
  {
    "executioner": "<the executioner from the input>",
    "message": "Hello AWS!"
  }
  ```

  A JSONata expression goes inside `{% %}`, and the state's input is
  `$states.input`.

- Before saving, select the state and choose **Test state** in the
  inspector. Try it with a correct input and with an input that has no
  `executioner`. What happens in the second case?

- Save, then **Start execution** with your name as the executioner. Look at
  the graph, the **Events** table and the state's input and output. Does
  the output look as expected?

- Switch to **Code** mode and use the export button to download the
  definition as JSON. Commit it to your repository.

##### Question: Pass State

_Describe the "Pass" state and what it does. Why is it useful when you're
building or testing a workflow?_

##### Question: States

_What are the other state types you can use in a state machine? Which of
them can fail, and which can't?_

#### Lab 18.1.2: The Same State Machine in CloudFormation

Recreate the state machine as code.

- Write a template with an
  [AWS::StepFunctions::StateMachine](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-stepfunctions-statemachine.html)
  and its execution role. Put the definition in the `Definition` property
  as YAML, not as a JSON string.

- The role's trust policy lets `states.amazonaws.com` assume it. Add an
  `aws:SourceAccount` condition so no other account's state machine can use
  it (the
  [confused deputy problem](https://docs.aws.amazon.com/IAM/latest/UserGuide/confused-deputy.html)).
  A Pass-only workflow needs no permissions beyond that; later labs add
  them.

- Lint, deploy, and output the state machine ARN.

- Run it from the CLI with
  [start-execution](https://docs.aws.amazon.com/cli/latest/reference/stepfunctions/start-execution.html),
  then read the result with `describe-execution` and the event list with
  `get-execution-history`.

- Delete the console-built state machine from Lab 18.1.1 and the role the
  console created for it.

##### Question: Three Ways to Ship a Definition

_The resource accepts `Definition`, `DefinitionString` and
`DefinitionS3Location`, plus `DefinitionSubstitutions`. When would you use
each? What happens to the state machine, and to executions that are
running, if you change `StateMachineType` in the template?_

#### Lab 18.1.3: JSONPath and JSONata

Step Functions has two query languages. **JSONPath** is the original: a
state's data passes through up to five fields (`InputPath`, `Parameters`,
`ResultSelector`, `ResultPath`, `OutputPath`), and keys that take a path
end in `.$`. **JSONata**
([Transforming data with JSONata](https://docs.aws.amazon.com/step-functions/latest/dg/transforming-data.html))
replaces those with `Arguments` and `Output`, reads the state's data from
`$states`, and has a full expression language: string functions, filters,
arithmetic, dates. You set `QueryLanguage` at the top of the definition
and can override it per state. If you leave it out, the default is still
JSONPath.

Add to your state machine from Lab 18.1.2:

- A second Pass state, set to `"QueryLanguage": "JSONPath"`, that produces
  the same output as the first one from the same input, using `Parameters`
  and a `.$` key. Chain the two states together.

- An `Assign` field on the first state that stores the executioner in a
  [variable](https://docs.aws.amazon.com/step-functions/latest/dg/workflow-variables.html),
  and a third state that uses it after the input has moved on.

- One JSONata expression that JSONPath can't do in a Pass state, for
  example an upper-cased name or the length of the message.

Then test each state on its own with
[TestState](https://docs.aws.amazon.com/step-functions/latest/dg/test-state-isolation.html)
from the CLI, passing a state's definition with `--definition` and
`--inspection-level DEBUG`. Compare the `inspectionData` for the JSONPath
state with the JSONata one.

##### Question: Input and Output

_Describe how input and output are handled in a JSONPath state and in a
JSONata state. Which of the five JSONPath fields does `Output` replace, and
where did `ResultPath`'s job go?_

##### Question: Variables or Output?

_A variable assigned in a state isn't visible in that state's own `Output`.
Why? When would you pass data forward in the output instead of in a
variable?_

### Retrospective 18.1

#### Question: Why a State Machine?

_You could write one Lambda function that does every step in order, or
have each function call the next. What do you gain by putting the steps in
a state machine, and what do you give up?_

## Lesson 18.2: Tasks and Service Integrations

### Principle 18.2

*A Task state can call a Lambda function, but most tasks don't need one:
Step Functions can call AWS APIs itself.*

### Practice 18.2

Lambda functions are a natural way to implement a Task: they're stateless,
quick to write, and need no server. But a function that only passes its
input to one AWS API call and returns the answer is *glue*: code to test,
patch, pay for and keep on a supported runtime, for no logic. Step Functions
has two ways to call AWS services directly:

- **Optimized integrations** for about twenty services, such as Lambda,
  DynamoDB, SQS, SNS, ECS, Glue, Bedrock and nested Step Functions
  executions. Step Functions shapes their requests and results for you, and
  some support the *Run a Job* (`.sync`) and *Wait for Callback*
  (`.waitForTaskToken`) patterns.
- **AWS SDK integrations**
  (`arn:aws:states:::aws-sdk:<service>:<apiAction>`) for over two hundred
  services and nine thousand API actions, called the way the SDK would call
  them. They support Wait for Callback but not `.sync`.

#### Lab 18.2.1: A Lambda Task

Add a Lambda function to your stack and call it from a Task state:

- A Python 3.13 function, inline in the template, that returns
  `"Hello AWS!"` and the executioner it was given. Give it its own log group
  with a retention period.

- A Task state using the optimized
  [Lambda invoke](https://docs.aws.amazon.com/step-functions/latest/dg/connect-lambda.html)
  integration (`arn:aws:states:::lambda:invoke`), with the function name and
  payload in `Arguments`.

- Grant the state machine's role `lambda:InvokeFunction` on that function
  only.

- Make the state's output just the function's return value, not the whole
  API response.

Run it and check that the execution outputs "Hello AWS!".

##### Question: What Came Back

_Look at `$states.result` for the Lambda task. What else is in it besides
your function's return value? Older definitions put the function's ARN
directly in `Resource`; how is that different?_

#### Lab 18.2.2: No Lambda Required

Now build a step that needs no function at all. The workflow should read a
greeting from Parameter Store, then save a record of the execution in
DynamoDB.

- Create a standard String parameter
  `/<your-id>/stelligent-u/lab18/greeting` with the CLI (as in Topic 11),
  and an on-demand DynamoDB table in your stack with a string partition key
  `id`.

- A Task state that reads the parameter with the **SDK integration**
  `arn:aws:states:::aws-sdk:ssm:getParameter`. Parameter names in
  `Arguments` are PascalCase (`Name`), as in the
  [SDK integration docs](https://docs.aws.amazon.com/step-functions/latest/dg/supported-services-awssdk.html).

- A Task state that writes an item with the **optimized**
  [DynamoDB integration](https://docs.aws.amazon.com/step-functions/latest/dg/connect-ddb.html)
  `arn:aws:states:::dynamodb:putItem`: an `id` from JSONata's `$uuid()`,
  the executioner, the greeting, and the execution's start time from
  `$states.context`.

- Give the role exactly `ssm:GetParameter` on the one parameter and
  `dynamodb:PutItem` on the one table. Build the ARNs with `!Sub`.

- Remove the Lambda task from the workflow if nothing uses it. (Keep the
  function in the template if you want it for Lesson 18.3.)

Run the workflow and check the item with `aws dynamodb scan`.

##### Question: Who Writes the Policy?

_When you build in the console, Step Functions generates a role policy for
optimized integrations but not for SDK integrations. Why can't it? Remove
`ssm:GetParameter` from the role, run the workflow, and note the error name
and where it appears._

##### Question: Activity State Machine

_What are some use cases for an
[activity](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-activities.html)
instead of a Lambda task? How does the
[Wait for Callback](https://docs.aws.amazon.com/step-functions/latest/dg/connect-to-resource.html#connect-wait-token)
pattern with a task token solve the same problem, and which would you pick
today?_

### Retrospective 18.2

#### Question: Service Integrations

_Pick three AWS services you've used in this course and find how a
workflow would call each: optimized integration, SDK integration or neither.
Which integration patterns (Request Response, `.sync`,
`.waitForTaskToken`) does each support? When would you still write a
Lambda function, and when would you use an
[HTTP Task](https://docs.aws.amazon.com/step-functions/latest/dg/call-https-apis.html)
to call a third-party API?_

## Lesson 18.3: Handling Errors with Retry and Catch

### Principle 18.3

*Failures are part of the workflow's definition: retry what's transient,
catch what isn't, and never let a run fail without saying why.*

### Practice 18.3

By default, any error in a state fails the whole execution. `Task`,
`Parallel` and `Map` states can declare a `Retry` list (retriers, tried in
order) and a `Catch` list (fallback transitions, used once retries are
exhausted). Errors have names: your own exception names, service errors such
as `DynamoDB.ConditionalCheckFailedException`, and the built-in `States.*`
names. Read
[Handling errors in Step Functions workflows](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html)
before you start.

#### Lab 18.3.1: Retry a Flaky Task

Write a Lambda function (Python 3.13) that fails on purpose, and a
workflow that survives it:

- The function reads a `failureRate` (0 to 1) from its input and raises a
  `TransientError` that often, using a custom exception class. If the input
  says `"permanent": true`, it raises `PermanentError` instead. Otherwise it
  returns a result.

- In the Task state, add a retrier for `TransientError` with
  `IntervalSeconds`, `BackoffRate`, `MaxAttempts`, a `MaxDelaySeconds` cap
  and `"JitterStrategy": "FULL"`.

- Add a separate retrier for the Lambda service errors that the
  [best practices](https://docs.aws.amazon.com/step-functions/latest/dg/sfn-best-practices.html#bp-lambda-serviceexception)
  recommend retrying. Workflow Studio adds one for you when you drop in a
  Lambda invoke; compare yours with it.

- Run the workflow several times with a `failureRate` of 0.5, and once with
  0.95. Find the retries in the execution history and in the console's
  **Retries & redrives** tab. How far apart were they?

##### Question: What the Retries Cost

_Count the state transitions of one execution that retried three times.
What does a retrier with `MaxAttempts: 10` and no `MaxDelaySeconds` cost in
money and in time if the error is not transient after all?_

#### Lab 18.3.2: Catch What Retry Can't Fix

Retrying a `PermanentError` wastes time. Catch it instead:

- Add a `Catch` for `PermanentError` that goes to a state that records the
  failure: write an item to your DynamoDB table with the error name and
  cause from `$states.errorOutput`. Use the catcher's `Assign` or `Output`
  to carry the error to that state.

- After recording it, end in a **Fail** state whose `Error` and `Cause`
  describe what happened, so the execution still shows as failed.

- Add a final catcher on `States.ALL` that goes to the same fallback.

- Give the Task a `TimeoutSeconds` shorter than a sleep you add to the
  function when the input asks for it, and run it. Which error name do you
  get, and which retrier or catcher handled it?

##### Question: Wildcards

_What is the difference between `States.ALL` and `States.TaskFailed`? Which
errors can't `States.ALL` catch? Why must `States.ALL` be alone and last?_

#### Lab 18.3.3: Unit Test the Error Handling

Waiting for a random failure is a slow way to test. The
[TestState API](https://docs.aws.amazon.com/step-functions/latest/dg/test-state-isolation.html)
can run one state against a **mocked** result or error, with no execution
role and no real service call.

Write a small test script (shell with `jq`, or pytest with boto3) in your
repository that calls `aws stepfunctions test-state` on your Task state
from Lab 18.3.2, with `--inspection-level DEBUG`, and asserts that:

- a mocked `TransientError` (`--mock` with an `errorOutput`) returns
  `status` `RETRIABLE`, the right `retryIndex` and a
  `retryBackoffIntervalSeconds`;

- the same error with `--state-configuration` setting `retrierRetryCount`
  to the retrier's `MaxAttempts` is no longer retried and is caught
  (`CAUGHT_ERROR`, and the `nextState` you expect);
  <!-- VERIFY: the TestState docs show retrierRetryCount for a retriable
  attempt but describe exhaustion only loosely ("increasing RetryCount
  values"); confirm the exhausted case returns CAUGHT_ERROR when running
  this lab. -->

- a mocked `PermanentError` goes straight to your fallback state;

- a mocked successful result produces the output you expect.

##### Question: What a Mock Proves

_What do these tests prove, and what can't they catch? (Think about IAM,
the function's real error names and payload shapes.) Where in a pipeline
like Topic 12's would they run?_

#### Lab 18.3.4: Redrive a Failed Execution

Some failures are fixed outside the workflow. For those, a Standard
execution can be
[redriven](https://docs.aws.amazon.com/step-functions/latest/dg/redrive-executions.html):
restarted from the state that failed, with the same input, within 14 days.

- Delete the greeting parameter from Lab 18.2.2 and start the workflow. It
  fails at the `getParameter` state (unless one of your catchers handles
  it; if it does, change which errors that catcher handles).

- Recreate the parameter, then run `aws stepfunctions redrive-execution` on
  the failed execution.

- Look at `describe-execution` and the history: the redrive count, and
  which states ran again.

##### Question: What Ran Again

_Which states did the redrive run, and which did it skip? Why can't you
redrive after you've updated the state machine's definition? What would
happen with redrive if the step before the failure weren't idempotent?_

### Retrospective 18.3

#### Question: Retry in the Workflow or in the Code?

_The SDK in your Lambda function already retries throttled calls. When do
you retry inside the function, when in the workflow, and when in both?
What goes wrong if both layers retry with long backoffs?_

## Lesson 18.4: Events and Workflow Types

### Principle 18.4

*EventBridge starts workflows when something happens; choose Standard or
Express by how long the work runs, how often it runs, and whether running
it twice is safe.*

### Practice 18.4

Most workflows aren't started by a person running the CLI. An EventBridge
rule can start a state machine when an event matches its pattern, such as
an object landing in S3, a CodePipeline stage failing or a schedule firing.
S3 sends events to EventBridge itself once you turn it on for a bucket;
no CloudTrail trail is needed.

The same definition can then run as either workflow type, and the choice
matters:

| | Standard | Express |
|---|---|---|
| Maximum duration | One year | Five minutes |
| Execution semantics | Exactly once | At least once (asynchronous), at most once (synchronous) |
| Execution history | In Step Functions for 90 days | Only in CloudWatch Logs, if you turn logging on |
| Billed by | State transition | Request, duration and memory |
| `.sync`, `.waitForTaskToken`, activities, Distributed Map | Yes | No |

Read
[Choosing workflow type](https://docs.aws.amazon.com/step-functions/latest/dg/choosing-workflow-type.html).
The type can't be changed after a state machine is created.

#### Lab 18.4.1: Start an Execution from an S3 Upload

Using the stack from the previous labs:

- Add an S3 bucket with
  [EventBridge notifications turned on](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-properties-s3-bucket-eventbridgeconfiguration.html)
  (`NotificationConfiguration` → `EventBridgeConfiguration`).

- Add an `AWS::Events::Rule` whose pattern matches `Object Created` events
  from `aws.s3` for your bucket, with keys under `incoming/` only, and a
  target that is your state machine. The target needs a role that
  EventBridge can assume with `states:StartExecution` on this state
  machine.

- Change the workflow to take the bucket and key from the event
  (`$states.input.detail`). Instead of a Lambda function returning the file
  name as in the 2022 version of this lab, use an SDK integration
  (`s3:headObject`) to get the object's size and content type, and write
  them to your table with `putItem`.

- Upload a file under `incoming/` with `aws s3 cp` and review the new
  execution: its input is the whole EventBridge event.

Follow the
[Step Functions tutorial for S3 events](https://docs.aws.amazon.com/step-functions/latest/dg/tutorial-cloudwatch-events-s3.html)
if you get stuck; it does the same thing in the console.

##### Question: No Trail Needed

_Why does the rule filter on the `incoming/` prefix? What would happen if
the workflow wrote an object back into the same bucket and prefix? How
long after you enable EventBridge on the bucket do events start arriving?_

#### Lab 18.4.2: An Express Workflow

Run the same processing as an Express workflow:

- Add a second `AWS::StepFunctions::StateMachine` with
  `StateMachineType: EXPRESS` and the same definition. (If the definition
  is in a separate file, use `DefinitionS3Location` or paste it; don't copy
  it by hand twice.)

- Give it a `LoggingConfiguration` with level `ALL` and
  `IncludeExecutionData: true`, sending to a log group whose name starts
  with `/aws/vendedlogs/states/`, with a retention period. The role needs
  the CloudWatch Logs delivery permissions listed in
  [Logging in CloudWatch Logs](https://docs.aws.amazon.com/step-functions/latest/dg/cw-logs.html).

- Run it synchronously with `aws stepfunctions start-sync-execution`, giving
  it an event like the one from Lab 18.4.1. The result comes back in the
  response.

- Run it asynchronously with `start-execution`. Where do you find what it
  did? Use `aws logs tail` on its log group.

- Point a second target of your EventBridge rule at the Express workflow,
  upload a file, and compare the two runs.

##### Question: Twice

_An asynchronous Express execution can run more than once for the same
event. What would happen to your DynamoDB table if it did? Change the
`putItem` so that running twice is harmless (hint: what should the `id`
be, and what does a `ConditionExpression` do?)._

##### Question: A Million Uploads

_Estimate the monthly cost of this workflow at one million uploads a month
as Standard and as Express, using the
[pricing page](https://aws.amazon.com/step-functions/pricing/). Assume each
execution takes 300 ms and fits in the smallest memory step. At what point
does the answer flip, and what other than price decides it?_

#### Lab 18.4.3: Distributed Map (Optional)

A
[Distributed Map](https://docs.aws.amazon.com/step-functions/latest/dg/state-map-distributed.html)
runs each item of a large dataset as its own child workflow execution, up
to 10,000 at once. It can read its items straight from S3: a listing of a
prefix, or a CSV, JSON, JSON Lines or Parquet file.

- Write a new Standard state machine whose Map state uses
  `"Mode": "DISTRIBUTED"` and `"ExecutionType": "EXPRESS"`, and an
  `ItemReader` with `arn:aws:states:::s3:listObjectsV2` over a `batch/`
  prefix of your bucket.

- The child workflow records each object's key and size in your table (the
  item is the object's metadata from the listing).

- Set `MaxConcurrency` to 5 and a `ToleratedFailurePercentage`.

- The role needs `states:StartExecution` on the state machine itself,
  `s3:ListBucket` limited to the prefix, and whatever the child workflow
  calls.

- Upload about a hundred small files under `batch/` (not `incoming/`, or
  Lab 18.4.1's rule starts a hundred executions too), start the workflow,
  and look at the **Map Run** page in the console.

##### Question: Why Not Express All the Way Down?

_Why must the parent be Standard? What does this run cost in state
transitions, and what would it cost with Standard children instead of
Express?_

#### Lab 18.4.4: Clean Up

- Empty the bucket with `aws s3 rm --recursive`, then delete your stacks.

- Delete the greeting parameter.

- Delete any log groups your functions and state machines created that
  weren't in a template (`aws logs describe-log-groups
  --log-group-name-prefix` with `/aws/lambda/<your-id>` and
  `/aws/vendedlogs/states/`).

- Check that the console-created role from Lab 18.1.1 is gone, and that
  `aws stepfunctions list-state-machines` and `aws events list-rules`
  show nothing of yours.

### Retrospective 18.4

#### Question: Workflows

_When is an Express workflow recommended instead of a Standard workflow?
Give one example of each from work you've done, and one workload that
should be neither (hint: what if it runs for more than a year, or needs
no coordination at all?)._

#### Question: Other Events

_What other events could start a state machine? Look at EventBridge
Scheduler, EventBridge Pipes, API Gateway and a CodePipeline invoke
action. Which of them can wait for a synchronous Express result?_

## Further Reading

- [Simplifying developer experience with variables and JSONata in AWS Step Functions](https://aws.amazon.com/blogs/compute/simplifying-developer-experience-with-variables-and-jsonata-in-aws-step-functions/)
  introduces the two features this edition is built on, and the
  [JSONata documentation](https://docs.jsonata.org/overview.html) covers the
  full language.

- Review
  [Step Functions best practices](https://docs.aws.amazon.com/step-functions/latest/dg/sfn-best-practices.html),
  especially timeouts, large payloads and Lambda service exceptions.

- [State machine versions](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-state-machine-version.html)
  and
  [aliases](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-state-machine-alias.html)
  let you shift traffic to a new definition gradually, like the Lambda
  deployments in Topic 16.

- [The AWS Step Functions Workshop](https://catalog.workshops.aws/stepfunctions)
  has longer exercises on error handling, the callback pattern and
  Distributed Map.

- [Serverless Land](https://serverlessland.com/workflows) collects
  workflow patterns, many of them with CloudFormation or SAM templates.
