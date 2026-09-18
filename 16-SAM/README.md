# Topic 16: Serverless Application Model (SAM)

<!-- TOC -->

- [Topic 16: Serverless Application Model (SAM)](#topic-16-serverless-application-model-sam)
  - [What changed in the 2026 edition](#what-changed-in-the-2026-edition)
  - [Exam coverage](#exam-coverage)
  - [Cost and cleanup](#cost-and-cleanup)
  - [Guidance](#guidance)
  - [Lesson 16.1: Introduction to SAM](#lesson-161-introduction-to-sam)
    - [Principle 16.1](#principle-161)
    - [Practice 16.1](#practice-161)
      - [Lab 16.1.1: Creating a Serverless Application](#lab-1611-creating-a-serverless-application)
        - [Question: SAM Required Files](#question-sam-required-files)
      - [Lab 16.1.2: Exploring Events](#lab-1612-exploring-events)
      - [Lab 16.1.3: Running the Application Locally](#lab-1613-running-the-application-locally)
        - [Question: API Resource](#question-api-resource)
      - [Lab 16.1.4: Deploying the Application to AWS](#lab-1614-deploying-the-application-to-aws)
        - [Question: Where the Code Went](#question-where-the-code-went)
      - [Lab 16.1.5: A Second Environment](#lab-1615-a-second-environment)
      - [Lab 16.1.6: Iterating in the Cloud with sam sync](#lab-1616-iterating-in-the-cloud-with-sam-sync)
        - [Question: Drift](#question-drift)
    - [Retrospective 16.1](#retrospective-161)
      - [Question: Capabilities](#question-capabilities)
      - [Question: Resources Created](#question-resources-created)
  - [Lesson 16.2: Integrating Components](#lesson-162-integrating-components)
    - [Principle 16.2](#principle-162)
    - [Practice 16.2](#practice-162)
      - [Lab 16.2.1: Integrating API Gateway](#lab-1621-integrating-api-gateway)
      - [Lab 16.2.2: Integrating SQS](#lab-1622-integrating-sqs)
        - [Question: Starting an API](#question-starting-an-api)
      - [Lab 16.2.3: Continuing the Pattern](#lab-1623-continuing-the-pattern)
    - [Retrospective 16.2](#retrospective-162)
      - [Question: Push or Poll](#question-push-or-poll)
      - [Question: Policy Templates](#question-policy-templates)
  - [Lesson 16.3: Working with DynamoDB](#lesson-163-working-with-dynamodb)
    - [Principle 16.3](#principle-163)
    - [Practice 16.3](#practice-163)
      - [Lab 16.3.1: Working with DynamoDB Locally](#lab-1631-working-with-dynamodb-locally)
      - [Lab 16.3.2: Adding a DynamoDB Table Resource](#lab-1632-adding-a-dynamodb-table-resource)
        - [Question: Invoke the Function Directly](#question-invoke-the-function-directly)
      - [Lab 16.3.3: Working with DynamoDB Streams](#lab-1633-working-with-dynamodb-streams)
    - [Retrospective 16.3](#retrospective-163)
      - [Question: What Local Testing Missed](#question-what-local-testing-missed)
  - [Lesson 16.4: Deployment Strategies](#lesson-164-deployment-strategies)
    - [Principle 16.4](#principle-164)
    - [Practice 16.4](#practice-164)
      - [Lab 16.4.1: Working with the AutoPublishAlias](#lab-1641-working-with-the-autopublishalias)
        - [Question: What the API Calls](#question-what-the-api-calls)
        - [Question: A Change Without a Version](#question-a-change-without-a-version)
      - [Lab 16.4.2: Working with CodeDeploy](#lab-1642-working-with-codedeploy)
        - [Question: Who Waits for Whom](#question-who-waits-for-whom)
      - [Lab 16.4.3: Working with CodeDeploy Deployment Hooks](#lab-1643-working-with-codedeploy-deployment-hooks)
        - [Question: Hook Failures](#question-hook-failures)
        - [Question: Hook Names](#question-hook-names)
        - [Question: Missing CodeDeploy Resource](#question-missing-codedeploy-resource)
      - [Lab 16.4.4: Alarms and Automatic Rollback](#lab-1644-alarms-and-automatic-rollback)
        - [Question: Two Alarms](#question-two-alarms)
        - [Question: After the Deployment](#question-after-the-deployment)
      - [Lab 16.4.5: Clean Up](#lab-1645-clean-up)
    - [Retrospective 16.4](#retrospective-164)
      - [Question: Canary and Linear Deployment Differences](#question-canary-and-linear-deployment-differences)
      - [Question: sam sync and Safe Deployments](#question-sam-sync-and-safe-deployments)
  - [Further Reading](#further-reading)

<!-- /TOC -->

## What changed in the 2026 edition

- **Current runtimes.** The 2022 labs used `python3.7` and `nodejs8.10`,
  both long retired: Lambda won't create or update functions on them.
  Python labs now use Python 3.13 and the Node.js labs use Node.js 22.
- **AWS SDK for JavaScript v3.** The shipped CodeDeploy hook
  ([hooks/lifecycleHook.mjs](hooks/lifecycleHook.mjs)) is an ES module that
  uses `@aws-sdk/client-codedeploy` and `@aws-sdk/client-lambda`. The old
  `require('aws-sdk')` (v2) isn't included in the Node.js 18 and later
  runtimes, so the old hook fails on a current runtime with a
  missing-module error. The hook now also
  invokes the new version and reports `Failed` on any error, instead of
  always reporting success.
- **`sam deploy --guided` and `samconfig.toml`** replace creating a bucket
  with `aws s3 mb` and running `sam package` and `sam deploy
  --template-file` by hand. SAM keeps its artifacts in a managed bucket
  (the `aws-sam-cli-managed-default` stack), and the settings you choose
  are saved per environment in `samconfig.toml`. New Lab 16.1.5 deploys a
  second environment from the same template with `--config-env`.
- **New Lab 16.1.6: `sam sync`** for fast iteration against a development
  stack, and why it must never point at production.
- **`sam validate --lint`** (cfn-lint) instead of plain `sam validate`,
  and `sam logs`, `sam list` and `sam remote invoke` instead of digging
  through the console.
- **DynamoDB Local** runs on a Docker network that `sam local` joins, so
  the endpoint is the same on macOS, Windows and Linux. Tables use
  on-demand capacity. The write endpoint is a `POST`, not a `GET`.
- **The safe-deployment lesson is kept and extended.** Lesson 16.4 still
  builds up `AutoPublishAlias`, CodeDeploy traffic shifting and pre- and
  post-traffic hooks. The hook template ([codeDeployResources.yml](codeDeployResources.yml))
  is now a complete template that passes cfn-lint, and names its hooks
  with the `CodeDeployHook_` prefix the generated CodeDeploy role
  requires. New Lab 16.4.4 adds CloudWatch alarms and makes CodeDeploy
  roll a bad release back by itself. The labs shift traffic in about five
  minutes instead of the old lab's hour and a half.
- Links point at the SAM Developer Guide instead of the old GitHub
  specification pages. Labs run in the lab account with the `lab` profile
  (`us-east-2`), and the module ends with a cleanup lab that also removes
  the SAM managed bucket.

## Exam coverage

| Exam | Domain / task statement |
|---|---|
| DVA-C02 → C03 | Domain 1: Development with AWS Services (Task 1: unit tests in development environments using AWS SAM; Task 2: develop code for Lambda, event source mappings; Task 3: DynamoDB and DynamoDB Streams). C03 guide publishes 2026-10-27 and adds GenAI / agent topics |
| DVA-C02 → C03 | Domain 3: Deployment (Task 2: Lambda versions and aliases, deploying a SAM template to a different staging environment; Task 3: application test events, IaC templates; Task 4: deployment strategies such as canary, and rollbacks) |
| DOP-C02 | Domain 1: SDLC Automation (Task 1.3: build and manage artifacts; Task 1.4: deployment strategies for serverless environments, canary deployments, troubleshooting deployment issues) |
| DOP-C02 | Domain 2: Configuration Management and IaC (Task 2.1: composing and deploying AWS SAM templates) |

## Cost and cleanup

- **Almost everything here is billed per request**, and lab traffic is
  tiny: Lambda, API Gateway (REST APIs are $3.50 per million requests in
  `us-east-2`), SQS, SNS and DynamoDB on-demand tables cost fractions of a
  cent at lab scale. Nothing in this module has an hourly charge.
- **CodeDeploy** costs nothing for Lambda deployments.
- **CloudWatch alarms** (Lab 16.4.4) cost $0.10 per alarm per month,
  prorated. Delete them with the stack.
- **Log groups.** Lambda creates `/aws/lambda/<function>` log groups
  outside your stacks, and they never expire. They're small, but they
  outlive `sam delete`; the cleanup lab removes them.
- **The SAM managed bucket persists.** The first `sam deploy --guided`
  creates a CloudFormation stack named `aws-sam-cli-managed-default` with
  one versioned, encrypted S3 bucket that every SAM project in the account
  and region shares. `sam delete` removes your application stack and its
  current artifacts, but never this stack, and because the bucket is
  versioned the old artifact versions stay behind. Storage is cents a
  month. To remove it, empty the bucket *including all object versions*,
  then delete the stack; [Lab 16.4.5](#lab-1645-clean-up) shows how.
- **Local tools** (Docker containers for `sam local` and DynamoDB Local)
  cost nothing in AWS, but stop them when you're done.
- [Lab 16.4.5](#lab-1645-clean-up) is the final cleanup: every stack from
  the module, the log groups, the local containers and the managed bucket.

## Guidance

- Explore the official docs! See the SAM
  [Developer Guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html),
  the [template specification](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-specification.html)
  and the
  [CLI reference](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-command-reference.html).

- Avoid using other sites like stackoverflow.com for answers \-- part of
  the skill set you're building is finding answers straight from the
  source, AWS.

- Explore your curiosity. Try to understand why things work the way they
  do. Read more of the documentation than just what you need to find the
  answers.

- Work in your lab account with the `lab` profile from module 19
  (`export AWS_PROFILE=lab`). The SAM CLI reads the same profile, which
  sets the lab region, `us-east-2`, so no command in this module needs
  `--region`. Stack names start with `<you>`, the identifier you use in
  resource names and tags.

- Module 9 built a function, an API, versions and a weighted alias by
  hand in plain CloudFormation. This module does the same things with SAM;
  compare as you go.

- The SAM CLI sends usage telemetry by default. Set
  `SAM_CLI_TELEMETRY=0` in your shell if you'd rather it didn't.

## Lesson 16.1: Introduction to SAM

### Principle 16.1

*AWS SAM is an extension of AWS CloudFormation that simplifies serverless
application development by supplying local development tools and taking
care of a significant amount of boilerplate for serverless resource
declarations in CloudFormation templates.*

### Practice 16.1

Let's explore what SAM has to offer by using the CLI to initialize a
simple hello world application. In order to begin, the following
requirements must be met:

1. [Install Docker](https://docs.docker.com/engine/install/) (or
   [Finch](https://runfinch.com/), which the SAM CLI also supports).
   `sam local` runs your functions in containers that mimic the Lambda
   runtime.

1. [Install the AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
   with the installer for your platform, and check it with
   `sam --version`.

1. Choose a [runtime](https://docs.aws.amazon.com/lambda/latest/dg/lambda-runtimes.html)
   to base the serverless application on and install it locally. Lessons
   16.1 to 16.3 use Python 3.13; Lesson 16.4 uses Node.js 22. Check the
   runtimes table for deprecation dates: that's what broke the 2022
   version of this module.

#### Lab 16.1.1: Creating a Serverless Application

To begin working with SAM, the first thing we need to do is create a new
application.

- Use the SAM CLI to initialize a new application. Run `sam init` and
  answer its prompts: an AWS Quick Start template, the Hello World
  example, Python 3.13, the Zip package type. Name it `sam-app`. Say no to
  X-Ray tracing, CloudWatch Application Insights and structured logging for
  now.

- Look at `sam init --help`, then write down the single non-interactive
  command that creates the same project (you need `--runtime`,
  `--app-template`, `--dependency-manager`, `--package-type` and
  `--no-interactive`). Scripts and pipelines can't answer prompts.

This creates a directory, `sam-app`, that has everything needed to begin
working with SAM: the function code in `hello_world/`, unit and
integration tests in `tests/`, a sample event in `events/`, a
`template.yaml` and a `samconfig.toml`. Note that a runtime can be
specified on an individual function basis, or for all of them in the
template's `Globals` section.

Take a look at the `template.yaml` that was created. Notice the directive
at the top:

```yaml
Transform: AWS::Serverless-2016-10-31
```

This is what indicates to CloudFormation that SAM resources are being
used. Any SAM resource found in this template will be translated into
standard CloudFormation resources when the stack is deployed.

- Run `sam validate --lint`. It checks the template with cfn-lint, which
  understands the SAM transform, and needs no AWS credentials. (The
  generated `samconfig.toml` already turns `lint` on for `sam validate`.)

##### Question: SAM Required Files

_Though using `sam init` is a quick way to get started with a new project,
it is not required. What file(s) is/are required at a minimum to define a
new SAM application?_

#### Lab 16.1.2: Exploring Events

Notice that SAM has also created an `events` directory with a sample
`event.json` file. The particular event generated here is an
`apigateway aws-proxy` event.

Serverless applications are by nature highly dependent on events. It is
very important to become familiarized with using events locally. The SAM
CLI has [built in functionality](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-local-generate-event.html)
that makes working with events very easy.

- Run `sam local generate-event` to see a list of the different services
  events can be generated for.
- After reviewing the list of services, try running
  `sam local generate-event apigateway` to see a list of events that can
  be generated to mimic the Amazon API Gateway service.
- Look at the different options available for an event by using the
  `--help` flag.

  ```bash
  sam local generate-event apigateway aws-proxy --help
  ```

- Use the `sam local generate-event` command to generate a new `aws-proxy`
  API Gateway event with a custom body.
- Save this new event to a file by redirecting the output to an
  `events/custom.json` file.
- Explore the different event types and options that can be generated for
  other services.

#### Lab 16.1.3: Running the Application Locally

In order to interact with the application we can invoke Lambda functions
directly or we can spin up an API reachable at `localhost`. Both need
Docker (or Finch) running.

- Build the application, then invoke the Lambda function directly.

  ```bash
  sam build
  sam local invoke HelloWorldFunction -e events/event.json
  ```

- Start the API and curl the `/hello` endpoint integrated with the
  Lambda function.

  ```bash
  sam local start-api
  ```

  ```bash
  curl http://127.0.0.1:3000/hello
  ```

- Run the unit tests that `sam init` generated (see the project's
  `README.md` for the command). They call the handler as a plain Python
  function, with no container and no AWS. What would you still need
  `sam local` for?

It is also possible to configure
[environment variables](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/using-sam-cli-local-invoke.html)
for local development. This is incredibly useful when working with Lambda
functions that need environment variables present to perform their
function. With SAM it is possible to specify all environment variables in
a JSON file structured so each Lambda function has its specific variables
defined.

- Update the function in the template to accept an environment variable
  called `NAME` (add it under `Environment: Variables:` with a default
  value). `sam local` only overrides variables the template declares.
- Create a file called `env.json`.
- Add the following JSON to the `env.json` file. Notice that variables are
  namespaced by the Lambda function's logical ID.

  ```json
  {
    "HelloWorldFunction": {
      "NAME": "<name>"
    }
  }
  ```

- Update the function to print out the `NAME` environment variable.
- Invoke the Lambda function on its own with `--env-vars env.json`.
- Start the API with `--env-vars env.json` and access the endpoint.

Ensure that accessing the function directly via `invoke` as well as
accessing it behind an API via `start-api` both log the expected
environment variable.

##### Question: API Resource

_There was no API resource defined in the SAM template, how is it
possible to start one and call it?_

#### Lab 16.1.4: Deploying the Application to AWS

Deploying is one command. The first time, run it in guided mode:

```bash
sam build
sam deploy --guided
```

Answer the prompts: a stack name of `<you>-sam-app`, the region your
profile already sets, confirm changes before deploying, allow SAM to
create IAM roles, and save the answers to `samconfig.toml` in the default
environment. SAM warns that `HelloWorldFunction` has no authorization;
accept that for this lab, and remember that the API is public.

Watch what `sam deploy` does:

- It creates (once per account and region) the `aws-sam-cli-managed-default`
  stack and its S3 bucket, and uploads your built function there. That's
  what the old `aws s3 mb` and `sam package` steps did by hand.
  `resolve_s3 = true` in `samconfig.toml` is the setting behind it.
- It creates a CloudFormation change set and shows it to you before
  executing it.
- It prints the stack outputs when it finishes.

Now open `samconfig.toml` and read the `[default.deploy.parameters]`
section. Your next deployment is just `sam build && sam deploy`.

- Curl the `HelloWorldApi` URL from the outputs. `sam list stack-outputs`
  and `sam list endpoints` show them again later.
- Invoke the deployed function without the API:
  `sam remote invoke HelloWorldFunction -e '{}'`.
- Read its logs with `sam logs -n HelloWorldFunction --tail`, then curl
  the API again in another terminal.

##### Question: Where the Code Went

_Find your function's code package in the managed bucket
(`aws cloudformation describe-stacks --stack-name aws-sam-cli-managed-default`
tells you the bucket name). Now look at the processed template of your
stack in CloudFormation
(`aws cloudformation get-template --stack-name <you>-sam-app --template-stage Processed`).
How does the function's
`Code` property compare with `CodeUri` in your `template.yaml`, and what
did `sam deploy` do in between?_

#### Lab 16.1.5: A Second Environment

The same template usually runs in more than one place: a test or staging
stack and production. `samconfig.toml` holds settings per
[configuration environment](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-config.html).

- Add a `Parameters` section to the template with a `Stage` parameter, and
  pass it to the function as an environment variable that it returns in
  its response.
- Add a `[staging.deploy.parameters]` section to `samconfig.toml` with a
  stack name of `<you>-sam-app-staging` and a `parameter_overrides` that
  sets `Stage=staging`. Copy the other deploy settings from `default`.
- Deploy it with `sam deploy --config-env staging`, then curl both APIs.

Two stacks, one template, no copy-pasted YAML. Module 12 does the same
thing from a pipeline.

#### Lab 16.1.6: Iterating in the Cloud with sam sync

`sam local` is fast but it isn't AWS: no real IAM, no real event sources.
[`sam sync`](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/using-sam-cli-sync.html)
keeps a stack in the cloud in step with your editor.

- Start it against a *separate development stack*:

  ```bash
  sam sync --stack-name <you>-sam-app-dev --watch
  ```

  Read the warning it prints before you confirm.
- Change the function's response and save. Time how long it takes before
  `curl` against the dev stack's API shows the change. Then change the
  API path in the template and watch what `sam sync` does differently.
- Stop it with Ctrl-C.

##### Question: Drift

_Code changes reached the dev stack in seconds without a CloudFormation
deployment. How? What does that do to the stack's view of the function
(try drift detection from module 1 on the dev stack), and why does the
SAM CLI make you confirm the stack is a development stack?_

### Retrospective 16.1

#### Question: Capabilities

_`samconfig.toml` contains `capabilities = "CAPABILITY_IAM"`. Remove it
and deploy again. What happens? The template doesn't declare an IAM role,
so why is the capability needed? When would you need
`CAPABILITY_AUTO_EXPAND` too?_

#### Question: Resources Created

_What resources were created for this stack that were not explicitly
defined in the template? Compare `sam list resources` with the
[generated resources](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-specification-generated-resources.html)
page._

When you've answered, delete the three stacks from this lesson:

```bash
sam delete --stack-name <you>-sam-app
sam delete --stack-name <you>-sam-app-staging
sam delete --stack-name <you>-sam-app-dev
```

## Lesson 16.2: Integrating Components

Before we start adding more components, review the different
[resource types](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-specification-resources-and-properties.html)
SAM can enhance CloudFormation with.

### Principle 16.2

*SAM resources can coexist in the same template as standard CloudFormation
resources. Everything that works with CloudFormation works with SAM. SAM
can be used to locally simulate events that would occur on AWS.*

### Practice 16.2

#### Lab 16.2.1: Integrating API Gateway

To explore some of the ways API Gateway and Lambda interact through SAM,
create another Hello World project, called `sam-api`, with the Python
3.13 runtime.

Often times it is necessary to pass parameters in the query portion of an
API call. Accessing these variables in the Lambda function is straight
forward.

- Update the function by replacing the `body` value with
  `json.dumps(event['queryStringParameters'])` for the return value.
- Start the API and curl `localhost:3000/hello?id=1`.

The function should have returned a JSON representation of all the query
parameters. Additionally, it is possible to access the path parameters of
a request if the path is configured to accept them.

- Update the `Events` declaration on the Lambda function by changing the
  `Path` from `/hello` to `/hello/{id}`.
- Update the function by replacing the `body` value with
  `json.dumps(event['pathParameters'])` for the return value.
- Start the API and curl `localhost:3000/hello/1`.

The function should have returned a JSON representation of the path
parameters.

- Generate an event file that can be used to `invoke` the function with a
  path parameter for `id`.

#### Lab 16.2.2: Integrating SQS

In previous exercises, new projects have been created with the SAM CLI
`init` command. This time, rather than use the CLI, simply create a new
directory, `sam-sqs`, and add a `template.yaml`.

- Create a new directory, `sam-sqs`, to house the new application.
- Add a `template.yaml` file and add the appropriate declarations to
  specify this as a SAM application.
- Run `sam validate --lint` to ensure the template is valid. If it is not,
  refer to the template generated in the last lab to determine why.

Add a Lambda function and an SQS queue to handle processing the queue's
messages.

- Add an `AWS::Serverless::Function` resource named `ProcessSqsFunction`
  with a `python3.13` runtime to the application and use the following
  code:

  ```python
  def lambda_handler(event, context):
      for record in event["Records"]:
          print(record["body"])
  ```

- Add an `AWS::SQS::Queue` resource to the template.
- Reference the queue in a new
  [SQS event](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-function-sqs.html)
  on the function.
- Generate a new SQS event.

  ```bash
  sam local generate-event sqs receive-message
  ```

The SAM `invoke` command can accept an event with the `-e` flag or by
reading from stdin.

- Ensure the function behaves as expected by invoking it with the
  generated SQS event using a pipe (`|`) and by passing the `-e` argument.
- Deploy the application with `sam build` and `sam deploy --guided`
  (stack name `<you>-sam-sqs`).
- Use the AWS CLI to
  [send a message](https://docs.aws.amazon.com/cli/latest/reference/sqs/send-message.html)
  to the queue. Read the function's logs with `sam logs --tail`: are the
  results as expected?

##### Question: Starting an API

_What happens if we try to start an API locally without having one
implicitly defined?_

#### Lab 16.2.3: Continuing the Pattern

At this point it should be apparent how to create event-driven
architectures locally using SAM and generated events to mimic real world
behavior.

For this lab, build an application that logs filenames written to S3 using
SNS. Refer to [Using AWS Lambda with other services](https://docs.aws.amazon.com/lambda/latest/dg/lambda-services.html)
for examples if difficulty arises.

- Create a Lambda function that is triggered anytime a new object is added
  to a specific S3 bucket (an
  [S3 event](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-function-s3.html);
  SAM requires the bucket to be in the same template).
- Create an SNS topic and configure the Lambda function to accept its ARN
  using Lambda environment variables.
- Have the Lambda function publish a new message to the SNS topic
  containing the name of the file, with boto3's
  [`publish`](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns/client/publish.html).
  Use the ARN configured in the environment, and give the function
  permission with a policy template rather than a hand-written policy.
- Create another Lambda function that is subscribed to the SNS topic that
  will log the filename of the object originally placed in S3.
- Test each function locally with a generated event first, then deploy
  and upload a file.

If CloudFormation reports a circular dependency, look at what your
function's policy references. Does the function need any permission on
the bucket at all?

### Retrospective 16.2

#### Question: Push or Poll

_Your functions were triggered by API Gateway, SQS, S3 and SNS. Which of
those services invoke the function themselves, and for which one does
Lambda poll through an event source mapping? Where does a failed message
go in each case?_

#### Question: Policy Templates

_Find the policy template you used in the processed template of your
stack. What statement did SAM generate, and how narrow is it? When would
you use an
[`AWS::Serverless::Connector`](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/managing-permissions-connectors.html)
instead?_

When you've answered, empty the bucket from Lab 16.2.3 and delete this
lesson's stacks with `sam delete`.

## Lesson 16.3: Working with DynamoDB

### Principle 16.3

*While it is relatively simple to manipulate Lambda functions with events
and the SAM CLI locally, interacting with a service like DynamoDB poses
some difficulty. Fortunately, Amazon has created a Docker image that
enables developers to work with it locally.*

### Practice 16.3

#### Lab 16.3.1: Working with DynamoDB Locally

Getting
[DynamoDB Local](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.DownloadingAndRunning.html)
running is just a matter of running the image in a container. Put it on
its own Docker network, so that the containers `sam local` starts can
reach it by name.

- Create the network and start DynamoDB Local on it:

  ```bash
  docker network create sam-lab
  docker run -d --name dynamodb --network sam-lab -p 8000:8000 amazon/dynamodb-local
  ```

- Ensure DynamoDB is reachable from your machine.

  ```bash
  aws dynamodb list-tables --endpoint-url http://localhost:8000
  ```

The response from DynamoDB should list the (currently nonexistent) tables.
DynamoDB Local accepts any credentials; your `lab` profile is fine.

#### Lab 16.3.2: Adding a DynamoDB Table Resource

- Create a new application (stack name `<you>-sam-dynamodb`), and add an
  [`AWS::Serverless::SimpleTable`](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-simpletable.html)
  resource to the template with a primary key of `id`.
- Add an `AWS::Serverless::Function` resource called `WriteFunction`
  (Python 3.13) to create entries in the DynamoDB table.
- Update the `WriteFunction` resource to accept an environment variable,
  `TABLE_NAME`, that references the DynamoDB table. Note that because SAM
  local does not actually create a DynamoDB table, any `!Ref` will fall
  back to the logical ID of the resource.
- Add an event to the `WriteFunction` so that it will be triggered by an
  API `POST` to the `/items` path.

To ensure the function is working, have it write out the `TABLE_NAME`
environment variable to the console.

Curl the API endpoint (`curl -X POST localhost:3000/items`) using
`sam local start-api` and check the log prints the expected table name -
it should be the logical ID, not the name of a real table.

Build and deploy the application, then test it in the cloud. Ensure
everything works as it did locally by calling the endpoint and checking
the function's logs for the table name.

##### Question: Invoke the Function Directly

_What happens if we try to invoke the function directly without the API?
Can you determine a way to invoke the function directly, both locally and
in the cloud?_

Next, create the table in the local DynamoDB instance. Provided is some
JSON with a table definition, [create-table.json](create-table.json).
Replace the `<TableLogicalID>` value with the logical ID used in the SAM
template and run the following:

```bash
aws dynamodb create-table --cli-input-json file://create-table.json \
  --endpoint-url http://localhost:8000
```

Now that the table is created, update the `WriteFunction` to create
records. SAM sets `AWS_SAM_LOCAL=true` in the environment when it runs a
function locally, so the function can pick its endpoint:

```python
import os
import uuid

import boto3

if os.getenv("AWS_SAM_LOCAL"):
    dynamodb = boto3.resource("dynamodb", endpoint_url="http://dynamodb:8000")
else:
    dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])
```

`dynamodb` is the container's name on the `sam-lab` network. It resolves
only for containers on that network, so start the API with
`sam local start-api --docker-network sam-lab`. In the cloud, boto3 picks
the region up from the Lambda environment.

- Finally, add code to insert an item into the table:

  ```python
  table.put_item(Item={"id": str(uuid.uuid4())})
  ```

Run the API locally and `POST` to `/items`. If everything worked as it
should, the following command should indicate new records were indeed
added to the local table:

```bash
aws dynamodb scan --table-name <TableLogicalID> --endpoint-url http://localhost:8000
```

#### Lab 16.3.3: Working with DynamoDB Streams

After verifying the application works, implement the resources needed to
trigger a new Lambda function when stream events occur on the table.

- Create another `AWS::Serverless::Function` resource called
  `ProcessStreamEventsFunction`.
- Use the following code for the body of the
  `ProcessStreamEventsFunction`:

  ```python
  def lambda_handler(event, context):
      for record in event["Records"]:
          print(record["eventID"])
          print(record["eventName"])
  ```

- Add a `StreamSpecification` to the table resource.
- Add a
  [DynamoDB event](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-function-dynamodb.html)
  to the function that references the stream we added to the DynamoDB
  table.
- Running `sam validate --lint` at this point should indicate that the SAM
  resource `AWS::Serverless::SimpleTable` is no longer robust enough for
  the functionality required by the application. Update the resource type
  to accommodate the `StreamSpecification` property, with on-demand
  (`PAY_PER_REQUEST`) billing.

DynamoDB Local has streams, but `sam local` has no way to connect a
function to them. To test the function locally, you trigger a stream
event yourself.

- Ensure the `ProcessStreamEventsFunction` is working correctly by
  building it and invoking it locally with an event from
  `sam local generate-event dynamodb update`.

While the `WriteFunction` works locally with DynamoDB, it will need a
policy to work with DynamoDB on AWS.

- Find the
  [appropriate policy template](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-policy-templates.html)
  and add it to the function under the `Policies` property. Choose the
  narrowest one that lets it put items.

Once the policy is in place, build and deploy the application. After it
has deployed, `POST` to the `/items` endpoint.

Did the function execute properly and insert data into the DynamoDB
table? Did the stream function log the new record? If not, debug the
issue with `sam logs`.

### Retrospective 16.3

#### Question: What Local Testing Missed

_List what worked locally but needed a change, or failed, once deployed
(think IAM permissions, table names, stream triggers). Which of those
could a unit test have caught, which needed `sam local`, and which could
only show up in the cloud? Where does `sam remote invoke` against a
deployed dev stack fit?_

When you've answered, delete the stack with `sam delete`, and stop and
remove the local container: `docker rm -f dynamodb` and
`docker network rm sam-lab`.

## Lesson 16.4: Deployment Strategies

### Principle 16.4

*As best practice, it is necessary to deploy applications in a way that
minimizes risk. AWS SAM assists with this by building in different
deployment patterns for shifting traffic between old and new versions of
the application, testing the new version before and after it takes
traffic, and rolling back automatically when something goes wrong.*

### Practice 16.4

It is advisable to get familiar with the overall concept of SAM and Lambda
deployment before proceeding into this section. The following resources
will provide a solid outline of what is to be accomplished in this lesson:

- [Deploying serverless applications gradually with AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/automating-updates-to-serverless-apps.html)
- [Safe Lambda deployments](https://github.com/aws/serverless-application-model/blob/develop/docs/safe_lambda_deployments.rst)
  in the SAM repository
- [Deploy an updated Lambda function with CodeDeploy and AWS SAM](https://docs.aws.amazon.com/codedeploy/latest/userguide/tutorial-lambda-sam.html)
- Module 9, [Lab 9.3.3](../09-lambda/README.md#lab-933-versions-and-aliases),
  where you shifted traffic between versions by hand

This lesson uses Node.js 22. Create the application for all its labs
now: a Hello World project with the `nodejs22.x` runtime, stack name
`<you>-sam-deploy`.

#### Lab 16.4.1: Working with the AutoPublishAlias

Adding an
[`AutoPublishAlias`](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-function.html#sam-function-autopublishalias)
property to an `AWS::Serverless::Function` accomplishes a few things.

1. SAM detects when the function's code has changed from the previous
   deployment by comparing the function's Amazon S3 URI (and, depending
   on settings, some of its other properties).
1. If a change is detected, it creates a new version of the function and
   publishes it, making it immutable.
1. After the new version is published, it creates an alias, or points the
   existing alias, to the newly published version of the function.

- Add the `AutoPublishAlias` property to the generated function and give
  it a value of `live`.
- Build and deploy the application with `sam deploy --guided`.

After the application has been deployed, inspect the stack to view the
alias that was created.

- Find the function's physical name with `sam list resources`.
- Use `aws lambda list-aliases --function-name <function-name>` to get
  back a list of aliases.

Take note of the function version returned from the AWS CLI. After the
alias creation has been verified, alter the code in the function, then
build and deploy it again.

- List the aliases for the function again.

Notice how the alias automatically points to the newest version of
the function.

##### Question: What the API Calls

_Your API event didn't mention the alias. Look at the API Gateway
integration and the Lambda permission in the processed template: does
the API call `$LATEST`, a version or the alias? Why does that matter for
the next lab?_

##### Question: A Change Without a Version

_Add a `Greeting` template parameter and pass it to the function as an
environment variable with `!Ref`. Deploy twice with different
`--parameter-overrides` values and nothing else changed. Did the alias
move? Read the notes under `AutoPublishAlias` and
`AutoPublishAliasAllProperties` in the function reference and explain
what happened, and what serves requests through the alias now._

#### Lab 16.4.2: Working with CodeDeploy

Now that the function alias is automatically updating on deployment, SAM
can utilize different deployment strategies to shift traffic from one
version of the function to another using AWS CodeDeploy. Update the
function declaration to utilize a deployment type.

- Add a
  [`DeploymentPreference`](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-property-function-deploymentpreference.html)
  property to the function with a `Type` of `Canary10Percent5Minutes`.
- Alter the function's code so that its response shows which version
  answered (for example, change the message).
- Build and deploy the application.
- While `sam deploy` is waiting, find the deployment and follow it:

  ```bash
  aws deploy list-applications
  aws deploy list-deployments --application-name <application>
  aws deploy get-deployment --deployment-id <deployment-id>
  ```

  or open the
  [CodeDeploy console](https://console.aws.amazon.com/codesuite/codedeploy/deployments?region=us-east-2).
- Look at the alias while the canary runs:
  `aws lambda get-alias --function-name <function-name> --name live`. What
  does `RoutingConfig` say?
- Call the API in a loop and count the two responses:

  ```bash
  for i in $(seq 1 50); do curl -s "<HelloWorldApi-URL>"; echo; done | sort | uniq -c
  ```

The current status of the Lambda deployment is listed in the deployment.
Notice how traffic is shifting between the two versions of the function,
exactly as your weighted alias did in module 9, but driven by CodeDeploy.

##### Question: Who Waits for Whom

_While the canary ran, what state was your CloudFormation stack in, and
which resource was it waiting on? What does that mean for a pipeline that
runs `sam deploy`? Try `Linear10PercentEvery1Minute` too: how long does a
deployment take now?_

#### Lab 16.4.3: Working with CodeDeploy Deployment Hooks

CodeDeploy operates using hooks that are called during the deployment
lifecycle. For Lambda there are two:
[`BeforeAllowTraffic` and `AfterAllowTraffic`](https://docs.aws.amazon.com/codedeploy/latest/userguide/reference-appspec-file-structure-hooks.html#appspec-hooks-lambda),
which SAM calls `PreTraffic` and `PostTraffic` in the `Hooks` property of
the `DeploymentPreference`. By utilizing these hooks, a newly deployed
function can be verified to be working before allowing traffic and after
allowing traffic. If a hook reports a `Failed` status, the deployment is
rolled back to the previous version.

Two files are supplied:

- [hooks/lifecycleHook.mjs](hooks/lifecycleHook.mjs), a hook function for
  Node.js 22 that uses the AWS SDK for JavaScript v3. It invokes the new
  function version directly, checks the response and reports the result
  to CodeDeploy with
  [`PutLifecycleEventHookExecutionStatus`](https://docs.aws.amazon.com/codedeploy/latest/APIReference/API_PutLifecycleEventHookExecutionStatus.html).
- [codeDeployResources.yml](codeDeployResources.yml), a complete SAM
  template with two hook functions, `PreTrafficHook` and
  `PostTrafficHook`. Its `HelloWorldFunction` is a stand-in with the same
  logical ID as yours, so that the file validates on its own.

Wire them into your project:

- Copy the `hooks/` directory into your project, and copy the two hook
  resources (not the stand-in function) into your `template.yaml`. If
  your function's logical ID isn't `HelloWorldFunction`, change the
  references in the hooks.
- Read the hooks' policies and environment. Why does each hook need to
  invoke `HelloWorldFunction.Version`, and what does `!Ref` of it return?
- Add a `Hooks` property to the `DeploymentPreference` that references
  the two hook functions:

  ```yaml
  DeploymentPreference:
    Type: Canary10Percent5Minutes
    Hooks:
      PreTraffic: !Ref PreTrafficHook
      PostTraffic: !Ref PostTrafficHook
  ```

- Run `sam validate --lint` and fix any issues preventing the template
  from validating.
- Change the function's code, then build and deploy the application.
- Follow the deployment with `aws deploy get-deployment` and the hooks'
  logs with `sam logs -n PreTrafficHook --tail` (and `PostTrafficHook`).

CodeDeploy is now using the Lambda functions defined in the application
as hooks to validate the deployment. While currently the same code is
being used for the before and after traffic hooks, it is possible (and
likely) to have different code validating each hook. This is a powerful
tool that is very useful in deploying a serverless application and
ensuring the integration works as expected.

- Make the check in `validate()` worth having: the `TODO(student)` in the
  hook describes what to test. Write a separate post-traffic check that
  calls the API URL instead of the function version.

##### Question: Hook Failures

_Deploy a version whose response fails your check. What happens to the
deployment, the alias and the CloudFormation stack? What happens if a
hook never calls `PutLifecycleEventHookExecutionStatus` at all (for
example, because it crashed before reaching it), and how does the
supplied hook avoid that?_

##### Question: Hook Names

_Both hooks' names start with `CodeDeployHook_`. Rename one without the
prefix and deploy a change. What fails, and why? (Look at the managed
policy on the `CodeDeployServiceRole` that SAM generated.) What could you
do instead of following the naming convention?_

##### Question: Missing CodeDeploy Resource

_You never specified a CodeDeploy resource to handle the deployment for
the function, how did CloudFormation know to create one?_

#### Lab 16.4.4: Alarms and Automatic Rollback

Hooks test the new version on purpose. Alarms catch what the tests
missed, while real traffic is shifting. If an alarm in the
`DeploymentPreference` goes into `ALARM` during the deployment, CodeDeploy
stops it and moves the alias back.

- Read how Lambda
  [dimensions its metrics](https://docs.aws.amazon.com/lambda/latest/dg/monitoring-metrics-view.html):
  `Errors` is published per function (`FunctionName`), per alias or
  version (`Resource`, for example `<function>:live`) and per alias and
  executed version (`ExecutedVersion`). An alarm's dimensions must match a
  published combination exactly, or it watches a metric that never gets
  data. The alarm examples in the Safe Lambda deployments document show
  the combinations to use.
- Add two `AWS::CloudWatch::Alarm` resources on `Errors` (sum over 60
  seconds, greater than 0, missing data not breaching): one for the alias,
  and one for the new version only, using
  `!GetAtt HelloWorldFunction.Version.Version` for `ExecutedVersion`.
- Add both to an `Alarms` list in the `DeploymentPreference` and deploy,
  so the alarms exist before the next test.
- Now ship a bug your hooks won't catch: make the function throw an error
  when the request has a query string parameter (say, `name`). The hooks
  invoke it without one, so they pass.
- Deploy it. As soon as traffic starts to shift, call the API in a loop
  with `?name=test`, and watch `aws deploy get-deployment` and the alarm
  with `aws cloudwatch describe-alarms --alarm-names <alarm>`.
- When it's over, check where the alias points and what state the stack
  is in.

You can also stop a deployment yourself:
`aws deploy stop-deployment --deployment-id <id> --auto-rollback-enabled`.

##### Question: Two Alarms

_Why alarm on the new version as well as on the alias? During a canary,
90% of traffic still goes to the old version: what could an alias-only
alarm miss, and what would an alarm on a percentage error rate (metric
math on `Errors` and `Invocations`) do better than a count?_

##### Question: After the Deployment

_What happens if the same bug only starts failing an hour after the
deployment finished? Who rolls it back then, and how? What would a
`PostTraffic` hook have to do to catch it?_

#### Lab 16.4.5: Clean Up

Remove everything this module created.

- Delete every application stack. `sam delete` deletes the stack and the
  current artifacts it uploaded:

  ```bash
  sam delete --stack-name <you>-sam-deploy
  aws cloudformation list-stacks --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE UPDATE_ROLLBACK_COMPLETE \
    --query "StackSummaries[].StackName"
  ```

  Delete any `<you>-sam-*` stack from earlier lessons that is still listed.
- Delete the functions' log groups, which Lambda created outside your
  stacks. List them with
  `aws logs describe-log-groups --log-group-name-pattern <you>` (the
  hooks' log groups match too, because their names include the stack
  name), then remove each with `aws logs delete-log-group`.
- Stop the local containers: `docker rm -f dynamodb`,
  `docker network rm sam-lab`, and any `sam local` containers still
  running.
- Remove the SAM managed bucket, unless another SAM project in the lab
  account still deploys from it. The bucket is versioned, so emptying it
  means deleting every object version and delete marker, not just the
  current objects:

  ```bash
  BUCKET=$(aws cloudformation describe-stacks --stack-name aws-sam-cli-managed-default \
    --query "Stacks[0].Outputs[?OutputKey=='SourceBucket'].OutputValue" --output text)
  python3 -c "import boto3, sys; boto3.resource('s3').Bucket(sys.argv[1]).object_versions.delete()" "$BUCKET"
  aws cloudformation delete-stack --stack-name aws-sam-cli-managed-default
  aws cloudformation wait stack-delete-complete --stack-name aws-sam-cli-managed-default
  ```

  (The console's **Empty** button on the bucket does the same as the
  Python line.) The next `sam deploy` in this account and region creates
  the stack again.

### Retrospective 16.4

#### Question: Canary and Linear Deployment Differences

_What is the difference between canary deployments and linear
deployments? Which would you choose for a function called a few times an
hour, and why might neither tell you much at that traffic level?_

#### Question: sam sync and Safe Deployments

_What would `sam sync --watch` have done to the `live` alias in this
lesson's stack? Would your hooks and alarms have run? Where does that
leave `sam sync` in a team's workflow?_

## Further Reading

- [Generated CloudFormation resources for AWS SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-specification-generated-resources-function.html)
  lists exactly what each function property adds to your stack.
- [Working with deployment configurations in CodeDeploy](https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-configurations.html)
  covers the predefined Lambda canary and linear configurations and how to
  create your own.
- [`sam pipeline`](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-generating-example-ci-cd.html)
  generates a CI/CD pipeline for a SAM application (module 12 builds one
  by hand).
- [AWS Infrastructure Composer](https://docs.aws.amazon.com/infrastructure-composer/latest/dg/what-is-composer.html)
  draws and edits SAM templates visually, in the console or in VS Code.
- [AWS::Serverless::Application](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-resource-application.html)
  nests other SAM applications, including ones from the Serverless
  Application Repository.
- [Python virtual environments](https://docs.python.org/3/tutorial/venv.html)
  keep each project's dependencies apart while you run unit tests outside
  `sam local`.
