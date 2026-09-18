# Topic 11: Parameter Store, Secrets Manager and AppConfig

<!-- TOC -->

- [Topic 11: Parameter Store, Secrets Manager and AppConfig](#topic-11-parameter-store-secrets-manager-and-appconfig)
  - [What changed in the 2026 edition](#what-changed-in-the-2026-edition)
  - [Exam coverage](#exam-coverage)
  - [Cost and cleanup](#cost-and-cleanup)
  - [Guidance](#guidance)
  - [Lesson 11.1: Introduction to Parameter Store](#lesson-111-introduction-to-parameter-store)
    - [Principle 11.1](#principle-111)
    - [Practice 11.1](#practice-111)
      - [Lab 11.1.1: Storing data](#lab-1111-storing-data)
      - [Lab 11.1.2: Reading data](#lab-1112-reading-data)
        - [Question: Finding Parameter Resources](#question-finding-parameter-resources)
      - [Lab 11.1.3: Integration with CloudFormation](#lab-1113-integration-with-cloudformation)
        - [Question: Stale Values](#question-stale-values)
        - [Question: Parameter Types or Dynamic References?](#question-parameter-types-or-dynamic-references)
      - [Lab 11.1.4: Secure Strings](#lab-1114-secure-strings)
        - [Question: Which Key?](#question-which-key)
      - [Lab 11.1.5: Versions, Labels and Tiers](#lab-1115-versions-labels-and-tiers)
        - [Question: Downgrading](#question-downgrading)
      - [Lab 11.1.6: Clean Up the Web Server](#lab-1116-clean-up-the-web-server)
    - [Retrospective 11.1](#retrospective-111)
      - [Question: Dynamic References and Secure Strings](#question-dynamic-references-and-secure-strings)
      - [Question: Secure Strings as Stack Parameters](#question-secure-strings-as-stack-parameters)
      - [Question: What the Secure String Protected](#question-what-the-secure-string-protected)
  - [Lesson 11.2: Secrets Manager](#lesson-112-secrets-manager)
    - [Principle 11.2](#principle-112)
    - [Practice 11.2](#practice-112)
      - [Lab 11.2.1: A Secret Nobody Typed](#lab-1121-a-secret-nobody-typed)
        - [Question: NoEcho](#question-noecho)
      - [Lab 11.2.2: Dynamic References, and Where They Leak](#lab-1122-dynamic-references-and-where-they-leak)
        - [Question: Where the Value Went](#question-where-the-value-went)
      - [Lab 11.2.3: Rotation with a Lambda Function](#lab-1123-rotation-with-a-lambda-function)
        - [Question: Staging Labels](#question-staging-labels)
        - [Question: A Real setSecret](#question-a-real-setsecret)
        - [Question: Managed Rotation](#question-managed-rotation)
      - [Lab 11.2.4: Sharing a Secret Across Accounts](#lab-1124-sharing-a-secret-across-accounts)
        - [Question: Two Policies and a Key](#question-two-policies-and-a-key)
        - [Question: Block Public Policy](#question-block-public-policy)
    - [Retrospective 11.2](#retrospective-112)
      - [Question: Parameter Store or Secrets Manager?](#question-parameter-store-or-secrets-manager)
  - [Lesson 11.3: AppConfig](#lesson-113-appconfig)
    - [Principle 11.3](#principle-113)
    - [Practice 11.3](#practice-113)
      - [Lab 11.3.1: Application, Environment and Feature Flags](#lab-1131-application-environment-and-feature-flags)
        - [Question: Hosted Versions](#question-hosted-versions)
      - [Lab 11.3.2: Retrieving Configuration](#lab-1132-retrieving-configuration)
        - [Question: Empty Responses](#question-empty-responses)
      - [Lab 11.3.3: Deployment Strategies and Automatic Rollback](#lab-1133-deployment-strategies-and-automatic-rollback)
        - [Question: Bake Time](#question-bake-time)
        - [Question: What Rolled Back](#question-what-rolled-back)
      - [Lab 11.3.4: Validators](#lab-1134-validators)
        - [Question: When Validation Runs](#question-when-validation-runs)
      - [Lab 11.3.5: Feature Flags in a Lambda Function](#lab-1135-feature-flags-in-a-lambda-function)
        - [Question: The Agent](#question-the-agent)
      - [Lab 11.3.6: Clean Up](#lab-1136-clean-up)
    - [Retrospective 11.3](#retrospective-113)
      - [Question: Three Stores](#question-three-stores)
  - [Further Reading](#further-reading)

<!-- /TOC -->

## What changed in the 2026 edition

- The module now covers all three AWS places to keep configuration and
  secrets outside your code: Parameter Store (Lesson 11.1, updated),
  **Secrets Manager** (new Lesson 11.2) and **AWS AppConfig** (new Lesson
  11.3). The 2022 version mentioned Secrets Manager in one Further Reading
  bullet and didn't cover AppConfig.
- Lab 11.1.3 builds on the launch template and Auto Scaling group from
  Topic 7 ([asg_example.yaml](../07-load-balancing/asg_example.yaml),
  Amazon Linux 2023, IMDSv2) instead of the old single-instance EC2 stack.
  You view the page through Session Manager port forwarding, so the
  instances need no inbound rules and no SSH.
- Lab 11.1.4 no longer asks you to put a secure string into the template.
  The instance reads it at boot with its instance role, which is how you
  do it for real, and the retrospective asks why the template can't.
- New Lab 11.1.5: parameter versions, labels, the advanced tier and
  parameter policies.
- Lesson 11.2 covers generated secrets, CloudFormation dynamic references
  (and where their values still leak), rotation with a Lambda function,
  managed rotation, and cross-account access with a resource policy and a
  customer managed KMS key.
- Lesson 11.3 covers AppConfig applications, environments, feature flags,
  deployment strategies, automatic rollback on a CloudWatch alarm,
  validators and the AppConfig Agent. AppConfig feature flags replace
  CloudWatch Evidently, which is retired.
- Labs run in the lab account with the `lab` profile (`us-east-2`).
  Parameter names start with your identifier rather than an IAM user name.
  Console links point at the lab region, and CloudFormation links point at
  the new Template Reference.

## Exam coverage

| Exam | Domain / task statement |
|---|---|
| DVA-C02 → C03 | Domain 2: Security (Task 2.3: manage sensitive data in application code, Skill 2.3.3: secret management services; Task 2.2, Skill 2.2.6: encryption across account boundaries). C03 guide publishes 2026-10-27 and adds GenAI / agent topics |
| DVA-C02 → C03 | Domain 3: Deployment (Task 3.1, Skill 3.1.5: prepare application configurations for specific environments, for example with AWS AppConfig; Task 3.4, Skill 3.4.11: deployment strategies) |
| SOA-C03 | Domain 4: Security and Compliance (Task 4.2, Skill 4.2.4: securely store secrets by using AWS services) |
| SOA-C03 | Domain 3: Deployment, Provisioning, and Automation (Task 3.1: provision and maintain cloud resources: CloudFormation parameters and dynamic references) |
| SCS-C03 | Domain 5: Data Protection (Task 5.3, Skill 5.3.1: design management and rotation of credentials and secrets) |
| SCS-C03 | Domain 4: Identity and Access Management (Task 4.2, Skill 4.2.1: resource policies for cross-account access) |

## Cost and cleanup

- **Parameter Store standard parameters are free**: no storage charge and no
  charge for API calls at the default throughput. **Advanced parameters**
  cost **$0.05 per parameter per month**, prorated hourly, plus $0.05 per
  10,000 API interactions. Lab 11.1.5 creates one advanced parameter for a
  few minutes (a fraction of a cent). Don't turn on *higher throughput*: it
  is an account-wide setting, and then every standard parameter call is
  billed too.
- **Secrets Manager** charges **$0.40 per secret per month**, prorated
  hourly, plus **$0.05 per 10,000 API calls**. This module creates three or
  four secrets, so forgotten ones cost well under $2 a month. A secret
  scheduled for deletion isn't billed. A replica secret in another Region
  is billed as a separate secret.
- **KMS:** Lab 11.2.4 needs a customer managed key, **$1 a month** prorated
  hourly (Lab 11.1.4 can use it too, or the free AWS managed `aws/ssm` key).
  A key scheduled for deletion isn't billed; the waiting period is at least
  seven days.
- **AppConfig** bills per request: $0.0000002 per configuration request
  through the API and $0.0008 per configuration received. The labs make a
  few hundred calls at most, well under a cent. AppConfig experiments
  ($0.90 per experiment hour) are not used here.
- **The web server** in Lab 11.1.3 is a t3.micro with a public IPv4
  address, about 1.5 cents an hour, around $11 a month if forgotten. Run a
  single instance and delete the stack in Lab 11.1.6.
- **Lambda** (Labs 11.2.3 and 11.3.5) stays within the free tier at lab
  scale. The **CloudWatch alarm** in Lab 11.3.3 costs $0.10 a month.
- Lab 11.1.6 removes the web server. [Lab 11.3.6](#lab-1136-clean-up) is
  the final cleanup for everything else: stacks, parameters, secrets
  (including ones already scheduled for deletion), the KMS key and the
  AppConfig application.

## Guidance

- Explore the official docs! See the Parameter Store
  [User Guide](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html),
  [API Reference](https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_GetParameters.html),
  [CLI Reference](https://docs.aws.amazon.com/cli/latest/reference/ssm/index.html),
  and
  [CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-ssm-parameter.html)
  docs; the Secrets Manager
  [User Guide](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html)
  and
  [CLI Reference](https://docs.aws.amazon.com/cli/latest/reference/secretsmanager/index.html);
  and the AppConfig
  [User Guide](https://docs.aws.amazon.com/appconfig/latest/userguide/what-is-appconfig.html)
  and CLI references for
  [appconfig](https://docs.aws.amazon.com/cli/latest/reference/appconfig/index.html)
  and
  [appconfigdata](https://docs.aws.amazon.com/cli/latest/reference/appconfigdata/index.html).

- Avoid using other sites like stackoverflow.com for answers \-- part
  of the skill set you're building is finding answers straight from
  the source, AWS.

- Explore your curiosity. Try to understand why things work the way
  they do. Read more of the documentation than just what you need to
  find the answers.

- Work in your lab account with the `lab` profile from module 19
  (`export AWS_PROFILE=lab`). The profile sets the lab region, `us-east-2`,
  so the commands in this module don't need `--region`. The consoles are
  [Parameter Store](https://console.aws.amazon.com/systems-manager/parameters?region=us-east-2),
  [Secrets Manager](https://console.aws.amazon.com/secretsmanager/listsecrets?region=us-east-2)
  and
  [AppConfig](https://console.aws.amazon.com/systems-manager/appconfig?region=us-east-2).
  Use them to look; make changes with CloudFormation and the CLI.

- **Never put a secret value in a template, a parameter default, a
  parameter file or your Git history.** Let AWS generate it, or type it
  once into a CLI prompt. The secrets in these labs protect nothing, but
  practise as if they did.

- Don't open SSH. Reach instances with
  [Session Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html),
  as in Topics 5 to 7.

## Lesson 11.1: Introduction to Parameter Store

### Principle 11.1

*Parameter Store is a key-value store that is compelling and powerful in
its simplicity.*

### Practice 11.1

Let's start out by creating a few parameters and finding ways we can
read them. In the labs below, keep a few things in mind:

- Parameter Store keys are naturally split by `/` into a hierarchy (but
  [it's not necessary](https://aws.amazon.com/blogs/mt/organize-parameters-by-hierarchy-tags-or-amazon-cloudwatch-events-with-amazon-ec2-systems-manager-parameter-store/)).
  You can use this to namespace your keys, and IAM policies can grant
  access to a whole branch of the tree.

- Parameter Store data is unique per account and region, but not per
  availability zone. You have the lab account to yourself, but namespacing
  still matters: real accounts are shared by many applications and teams,
  and a flat namespace is hard to secure.

- Prefix your keys with `/<your-id>/stelligent-u/lab11/`, where
  `<your-id>` is the identifier you use in resource names and tags.

#### Lab 11.1.1: Storing data

Create a new CloudFormation stack that can store a handful
of data points for an engineer in Parameter Store (e.g., Name, Title, Address,
etc.). Make it generic, so that each data point is passed as a Stack parameter,
as if the stack template might be used to store info about each engineer.

- Create a sub-tree of
  [AWS::SSM::Parameter](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-ssm-parameter.html)
  resources that will store information on a single engineer.

- Every Parameter Store value type can be a string.

- At the top of the sub-tree, use a name for the engineer as your key
  value. See the [Name constraints](https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_PutParameter.html#systemsmanager-PutParameter-request-Name)
  in the PutParameter API docs for limitations. Try to enforce some
  of those limitations in your stack's [parameter properties](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html),
  too. (E.g. set an AllowedPattern and MaxLength. Can you set any
  other limitations?).

- Store all other keys under that.

- Store the engineer's team name under "team".

- Store their timezone under "timezone".

- Store their home state as a 2-letter prefix under "state".

- Store their start date under "start-date".

Lint the template with cfn-lint, then launch the stack with a parameter
file that sets information for yourself.

#### Lab 11.1.2: Reading data

Look at ways to read your parameter data.

- You can look it up in the
  [Parameter Store console](https://console.aws.amazon.com/systems-manager/parameters?region=us-east-2).

- You can read it with the API using
  [GetParameter](https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_GetParameter.html),
  [GetParameters](https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_GetParameters.html)
  and
  [GetParametersByPath](https://docs.aws.amazon.com/systems-manager/latest/APIReference/API_GetParametersByPath.html),
  for example from Python with boto3's
  [get_parameters_by_path](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_parameters_by_path.html).

- You can invoke those same API queries through the
  [aws ssm](https://docs.aws.amazon.com/cli/latest/reference/ssm/index.html)
  CLI.

Use all 3 methods to read your parameters individually and to fetch the
entire subtree with a single query. While you're at it, browse some
[public parameters](https://docs.aws.amazon.com/systems-manager/latest/userguide/parameter-store-public-parameters.html)
that AWS publishes, such as `/aws/service/ami-amazon-linux-latest/` and
`/aws/service/global-infrastructure/regions`. You've been reading one of
them since Topic 5 to find your AMI.

##### Question: Finding Parameter Resources

_When you look at your stack in the CloudFormation console, can you find
the values of your parameter resources there?_

#### Lab 11.1.3: Integration with CloudFormation

CloudFormation can use Parameter Store keys and values as
[stack parameters](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cloudformation-supplied-parameter-types.html#systems-manager-parameter-types-supported).
This gives us an incredibly convenient way to maintain stack parameters
without the hassle of updating JSON files and keeping them in sync
through S3 or git repositories.

Make a copy of [asg_example.yaml](../07-load-balancing/asg_example.yaml),
the web server starter from the Load Balancing topic. Instead of serving a
page that says "Automation for the People", make one that describes an
engineer.

- You don't need the load balancer for this lab, and you don't need three
  instances. Set the group's minimum, maximum and desired capacity to 1,
  and the `CreationPolicy` signal count to match.

- One parameter should be an `AWS::SSM::Parameter::Name` that will
  reference the top-level key of your hierarchy as set in your stack
  from lab 1.

- Accept an `AWS::SSM::Parameter::Value<String>` type for each of the
  Parameter Store values that you set in your stack from lab 1.

- Show the value of each of those stack parameters in the web page
  that nginx serves. The page lives in the launch template's
  `AWS::CloudFormation::Init` metadata, so `!Sub` is your friend.

- The web servers' security group has no inbound rules, and it should stay
  that way. To see the page, open a
  [Session Manager port forwarding session](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-sessions-start.html#sessions-start-port-forwarding)
  from port 80 on the instance to a local port, then browse to
  `http://localhost:<local-port>`. (You need the Session Manager plugin
  for the CLI.)

When you launch your stack, make sure the web page shows the values of
all the keys that you set in lab 1.

As follow-up to the question above about finding the values of your
parameter resources, read the considerations in the SSM parameter types
document linked at the start of this lab. CloudFormation shows the
*resolved* values on the stack's Parameters tab and in `describe-stacks`
and `describe-change-set`. Those are the values in use in the stack, set
when the stack was created or last updated, so they might differ from the
latest values in Parameter Store.

##### Question: Stale Values

_Change the "team" value in Parameter Store with the CLI. What does the web
page show now? What do you have to do to get the new value onto the page,
and what does CloudFormation do to the instance when you do it? (Look at
the launch template versions and the group's update policy.)_

##### Question: Parameter Types or Dynamic References?

_A [dynamic reference](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references-ssm.html)
such as `{{resolve:ssm:/<your-id>/stelligent-u/lab11/<name>/team}}` reads
the same value without a stack parameter. Rewrite one of your values that
way. Where does the resolved value show up now? What can a parameter type
do that a dynamic reference can't, and the other way around?_

#### Lab 11.1.4: Secure Strings

One of the features that makes Parameter Store *so* compelling is the
way it easily [lets you store secrets](https://docs.aws.amazon.com/systems-manager/latest/userguide/secure-string-parameter-kms-encryption.html).
When you set a key to a value, you simply reference a KMS key and mark
the value as a secret. Anybody allowed to read the parameter and use the
key can read it. As we said above, the simplicity of this service is part
of what makes it so powerful.

Store the engineer's middle name as a secret, then show it on the web page
from lab 3.

First, use the awscli to store the middle name of an engineer in the
hierarchy you created earlier.

- The middle name should be a
  [SecureString](https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-paramstore-securestring.html).
  CloudFormation can't create SecureString parameters, which is why this
  step uses the CLI.

- Store the info under the key "middle-name" within the given
  engineer's hierarchy.

- Encrypt it with either the AWS managed key `aws/ssm` (the default) or the
  customer managed key you create for Lab 11.2.4
  ([create-key](https://docs.aws.amazon.com/cli/latest/reference/kms/create-key.html)).

Then make the instance read the value when it boots:

- Give the web server's instance role permission to call `ssm:GetParameter`
  on the "middle-name" parameter only. Build the ARN from pseudo-parameters;
  don't hard-code the account ID or region.

- In the launch template's `cfn-init` metadata or user data, read the value
  with `aws ssm get-parameter --with-decryption` (AL2023 ships with the AWS
  CLI; the instance role supplies the credentials through IMDSv2) and write
  it into the page.

- Update the stack and check the page.

##### Question: Which Key?

_Did the instance role need a `kms:Decrypt` permission? Try it with both
`aws/ssm` and a customer managed key, and explain the difference. (Hint:
read each key's key policy.)_

#### Lab 11.1.5: Versions, Labels and Tiers

Parameters are versioned, and there is more than one tier.

- Change "team" two or three times with `aws ssm put-parameter --overwrite`,
  then read its history with `get-parameter-history`. How many versions
  does Parameter Store keep?

- Read an old value by
  [version and by label](https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-paramstore-labels.html):
  attach a label such as `known-good` to one version with
  `label-parameter-version`, then read `<name>:<version>` and
  `<name>:known-good`.

- Compare the
  [standard and advanced tiers](https://docs.aws.amazon.com/systems-manager/latest/userguide/parameter-store-advanced-parameters.html).
  Create one new *advanced* parameter under your prefix with an
  `Expiration` and an `ExpirationNotification`
  [parameter policy](https://docs.aws.amazon.com/systems-manager/latest/userguide/parameter-store-policies.html)
  a day or two out. Find the policy in `describe-parameters`, then delete
  the parameter: advanced parameters are billed while they exist.

##### Question: Downgrading

_Can you change an advanced parameter back to standard? Why not? What
other feature needs the advanced tier? (Look at sharing parameters with
other accounts.)_

#### Lab 11.1.6: Clean Up the Web Server

Delete the web server stack from Lab 11.1.3. Keep the parameter stack and
the "middle-name" parameter; Lesson 11.2 uses them, and standard parameters
cost nothing.

### Retrospective 11.1

#### Question: Dynamic References and Secure Strings

Read [Get a secure string value from Systems Manager Parameter Store](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references-ssm-secure-strings.html).
Why can't you use an `ssm-secure` dynamic reference to read "middle-name"
and show it in your web page?

#### Question: Secure Strings as Stack Parameters

Can you use a SecureString as an `AWS::SSM::Parameter::Value` type in a
CloudFormation stack?

#### Question: What the Secure String Protected

_You encrypted the middle name with KMS, then published it on a web page.
What did SecureString protect, and against whom? What didn't it protect?_

## Lesson 11.2: Secrets Manager

### Principle 11.2

*A secret has a lifecycle: it is generated, distributed, rotated and
revoked. Parameter Store can hold a secret; Secrets Manager also manages
its lifecycle.*

### Practice 11.2

Secure strings in Parameter Store are encrypted values and nothing more.
[Secrets Manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/intro.html)
adds what a credential needs over its life: generated values, versions
with [staging labels](https://docs.aws.amazon.com/secretsmanager/latest/userguide/whats-in-a-secret.html),
scheduled rotation, a resource policy for cross-account access, and
replication to other regions. It also costs money per secret, which is the
trade-off to weigh.

The labs create secrets with CloudFormation without anyone typing a value,
look at what CloudFormation dynamic references do with secret values, rotate
a secret with your own Lambda function, and share one with another account.

#### Lab 11.2.1: A Secret Nobody Typed

Create a stack with an
[AWS::SecretsManager::Secret](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-secretsmanager-secret.html)
for a pretend service account.

- Use `GenerateSecretString` to produce a JSON secret with a fixed
  `username` (your identifier) and a generated `password`. Choose a
  length and exclude characters that commonly break shell scripts and
  connection strings.

- Name it under a prefix such as `<your-id>/stelligent-u/lab11/` and tag
  it. Don't set `SecretString`.

- Read it back with `aws secretsmanager describe-secret` and
  `get-secret-value`. Note the secret's ARN (with its random six-character
  suffix) and the version's staging label.

- Read the same secret through Parameter Store's
  [Secrets Manager reference](https://docs.aws.amazon.com/systems-manager/latest/userguide/integration-ps-secretsmanager.html),
  `/aws/reference/secretsmanager/<secret-name>`.

##### Question: NoEcho

_The old way to get a password into a stack was a `String` parameter with
`NoEcho: true`. Where can a `NoEcho` value still end up (think parameter
files, shell history, template metadata and outputs)? What does
`GenerateSecretString` avoid?_

#### Lab 11.2.2: Dynamic References, and Where They Leak

Most tutorials pass secrets to resources with a
[Secrets Manager dynamic reference](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references-secretsmanager.html):
`{{resolve:secretsmanager:<secret-id>:SecretString:<json-key>}}`. It is the
right tool for properties such as a database password, and module 22 goes
one better by letting RDS own the password. But CloudFormation only promises
not to log the resolved value; the service that receives it may show it to
anyone who can describe the resource.

Prove it with a throwaway secret:

- In a second stack, create an `AWS::SSM::Parameter` of type `String` whose
  value is a dynamic reference to the `username` key of your Lab 11.2.1
  secret. Deploy it and read the parameter.

- Now point it at the `password` key instead, update the stack, and read
  the parameter again with `get-parameter` and in the console.

- Delete this stack when you've answered the question.

##### Question: Where the Value Went

_Where is the password now, in plaintext, and who can read it? Name two
other places a resolved secret would be just as visible (for example a
launch template's user data or a Lambda function's environment variables).
What should you pass to an application instead of the value?_

#### Lab 11.2.3: Rotation with a Lambda Function

[Rotation](https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html)
replaces a secret on a schedule, updating both the secret and the system
that checks it. RDS, Aurora, Redshift and DocumentDB offer *managed
rotation* for their master credentials, and some SaaS partners now offer it
through *managed external secrets*. Everything else rotates with a Lambda
function that Secrets Manager calls four times, once per step:
[createSecret, setSecret, testSecret and finishSecret](https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotate-secrets_lambda-functions.html).

Rotate a secret that stands for an API key of a pretend service:

- Create a second secret whose value is a single generated key (for
  example `{"api_key": "..."}`) with `GenerateSecretString`.

- Write a rotation function in Python 3.13, starting from the
  [generic rotation template](https://docs.aws.amazon.com/secretsmanager/latest/userguide/reference_available-rotation-templates.html#OTHER_rotation_templates).
  Read it and understand it rather than copying it: `createSecret`
  generates a new key into an `AWSPENDING` version, `setSecret` would
  register it with the service (your pretend service has nothing to
  update, so log that and return), `testSecret` checks the pending value
  (check its format), and `finishSecret` moves `AWSCURRENT`. Never log the
  secret value.

- Deploy the function with CloudFormation the way you did in Topic 9.
  Give its execution role only the
  [permissions rotation needs](https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets-required-permissions.html)
  on this one secret, and add a resource-based permission so that
  `secretsmanager.amazonaws.com` can invoke it (scope it to your account
  with a `SourceAccount` condition).

- Add an
  [AWS::SecretsManager::RotationSchedule](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-secretsmanager-rotationschedule.html)
  with a `RotationLambdaARN` and a `ScheduleExpression`. By default it
  rotates as soon as it's created, so the function has to work the first
  time; check the function's log group with `aws logs tail` if it doesn't.

- Rotate again on demand with `aws secretsmanager rotate-secret`, and
  watch the versions with `describe-secret` (look at `VersionIdsToStages`)
  and `list-secret-version-ids`.

##### Question: Staging Labels

_Which version carries `AWSCURRENT`, `AWSPENDING` and `AWSPREVIOUS` after
two rotations? An application that cached the old key keeps using it for a
while. What does `AWSPREVIOUS` buy it, and what does the
[alternating users strategy](https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotation-strategy.html)
add for databases?_

##### Question: A Real setSecret

_If this were a real third-party API key, what would `setSecret` and
`testSecret` have to do? What if the provider only allows one active key
at a time?_

##### Question: Managed Rotation

_Module 22 sets `ManageMasterUserPassword` on an RDS instance. Who owns that
secret, can you delete it or change its rotation schedule, and why is there
no Lambda function? What is the shortest rotation interval Secrets Manager
allows?_

#### Lab 11.2.4: Sharing a Secret Across Accounts

A secret can be read from another account if **three** things allow it:
the secret's resource policy, the KMS key's key policy, and an identity
policy in the other account. Read
[Access Secrets Manager secrets from a different account](https://docs.aws.amazon.com/secretsmanager/latest/userguide/auth-and-access_examples_cross.html)
first. Your second account is the management account from module 19
(profile `mgmt`); you only read from it and create nothing there.

- Create a customer managed KMS key in the lab account, with a key policy
  that keeps the lab account in control and lets the management account
  call `kms:Decrypt` only through Secrets Manager (`kms:ViaService`).

- Create a third secret (generated, as before) encrypted with that key. The
  AWS managed key `aws/secretsmanager` can't be used across accounts.

- Attach a resource policy with
  [AWS::SecretsManager::ResourcePolicy](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-secretsmanager-resourcepolicy.html)
  that allows only `secretsmanager:GetSecretValue`, for the management
  account as the principal. Write account IDs as parameters, never in the
  template.

- Read it from the management account:
  `aws secretsmanager get-secret-value --secret-id <full-secret-ARN>
  --profile mgmt --region us-east-2`. The full ARN is required across
  accounts; the name alone won't do.

- Before you finish, run `aws secretsmanager validate-resource-policy`
  against a policy with `"Principal": "*"` to see what it reports.

##### Question: Two Policies and a Key

_Remove each of the three permissions in turn (resource policy, key policy
statement, and, if you have an admin role in the management account,
imagine a role without `secretsmanager:GetSecretValue`). Which error do
you get each time, and which account's CloudTrail records it?_

##### Question: Block Public Policy

_The CLI's `put-resource-policy` doesn't block public policies unless you
pass `--block-public-policy`, but the CloudFormation `ResourcePolicy`
resource blocks them by default. Why does the default matter, and which
other service would flag a policy like that (see module 03)?_

### Retrospective 11.2

#### Question: Parameter Store or Secrets Manager?

_Both can hold an encrypted string. For each of these, which would you
choose and why: an RDS master password, a third-party API key that must
rotate every 30 days, a feature toggle, a database hostname, a TLS private
key shared with a partner account, and a value 6 KB long? Where does cost
decide it?_

## Lesson 11.3: AppConfig

### Principle 11.3

*Changing configuration is a deployment. Validate it, roll it out
gradually, watch it, and roll it back automatically, just like code.*

### Practice 11.3

Parameter Store and Secrets Manager hand an application the current value
of something. [AWS AppConfig](https://docs.aws.amazon.com/appconfig/latest/userguide/what-is-appconfig.html)
controls how a change *reaches* the application: a configuration profile
(feature flags or free-form data from its hosted store, Parameter Store,
Secrets Manager or S3) is deployed to an environment with a deployment
strategy, checked by validators, and rolled back if a CloudWatch alarm
fires. Applications read it through the AppConfig Agent or the
`appconfigdata` API.

AppConfig feature flags are also AWS's replacement for CloudWatch
Evidently, which is retired, and they now support multi-variant flags,
targeting rules and experiments.

#### Lab 11.3.1: Application, Environment and Feature Flags

Create a stack with:

- An
  [AWS::AppConfig::Application](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-appconfig-application.html)
  named after your identifier, and an
  [AWS::AppConfig::Environment](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-appconfig-environment.html)
  called `lab`.

- A feature flag
  [configuration profile](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-appconfig-configurationprofile.html)
  (`Type: AWS.AppConfig.FeatureFlags`, `LocationUri: hosted`).

Then create the flag data with the CLI, not in the template, because flag
values change far more often than infrastructure:

- Write a flags document in the
  [feature flag format](https://docs.aws.amazon.com/appconfig/latest/userguide/appconfig-type-reference-feature-flags.html)
  with one flag, `show-team`, disabled, and one flag with an attribute (for
  example `banner` with a `message` string and a constraint on its length).

- Store it with `aws appconfig create-hosted-configuration-version` and a
  content type of `application/json`.

##### Question: Hosted Versions

_Create a second hosted version with `show-team` enabled. Has anything
changed for an application yet? What has to happen before it does?_

#### Lab 11.3.2: Retrieving Configuration

Read the configuration the way an application does, with the
[appconfigdata](https://docs.aws.amazon.com/cli/latest/reference/appconfigdata/index.html)
API:

- Deploy version 1 to the `lab` environment with `aws appconfig
  start-deployment` and the predefined strategy
  `AppConfig.AllAtOnce`. Watch it with `get-deployment`.

- Start a session with `start-configuration-session`, then call
  `get-latest-configuration` with the token and save the output to a file.
  Call it again with the *new* token it returned.

- Deploy version 2 and poll again.

##### Question: Empty Responses

_Why was the second response empty? What does that mean for how often an
application should poll, and for the bill? Why is the old `GetConfiguration`
API not an option for feature flags?_

#### Lab 11.3.3: Deployment Strategies and Automatic Rollback

A [deployment strategy](https://docs.aws.amazon.com/appconfig/latest/userguide/appconfig-creating-deployment-strategy.html)
sets how fast a change reaches its targets (linear or exponential growth,
deployment time) and how long AppConfig watches alarms afterwards (bake
time). Compare the
[predefined strategies](https://docs.aws.amazon.com/appconfig/latest/userguide/appconfig-creating-deployment-strategy-predefined.html),
then make AppConfig roll a change back:

- In your stack, add a CloudWatch alarm on a metric of your own that
  nothing publishes (treat missing data as not breaching), an IAM role that
  AppConfig can assume to call `cloudwatch:DescribeAlarms`
  ([rollback permissions](https://docs.aws.amazon.com/appconfig/latest/userguide/setting-up-appconfig.html#getting-started-with-appconfig-cloudwatch-alarms-permissions)),
  and a `Monitors` entry on the environment.

- Add a custom
  [AWS::AppConfig::DeploymentStrategy](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-appconfig-deploymentstrategy.html):
  linear, a few minutes long, with a bake time of five minutes or so.

- Deploy a new flag version with it. Part-way through, set the alarm to
  `ALARM` with `aws cloudwatch set-alarm-state`, and watch the deployment
  with `get-deployment` until it finishes.

- Then deploy again and let it complete.

##### Question: Bake Time

_What does AppConfig do during bake time, and why is it worth waiting after
the change has reached 100% of targets?_

##### Question: What Rolled Back

_After the rollback, which version do clients receive? What would have
happened if the alarm had fired an hour after the deployment completed?_

#### Lab 11.3.4: Validators

[Validators](https://docs.aws.amazon.com/appconfig/latest/userguide/appconfig-creating-configuration-and-profile-validators.html)
stop bad data before it deploys. Feature flag profiles are checked against
the flag schema automatically, and you can add up to two validators to any
profile.

- Add a free-form configuration profile (hosted, JSON) for settings such as
  a log level and a request limit, with a JSON Schema validator that allows
  only known log levels and a sensible range of limits.

- Create one valid and one invalid hosted version, and try to deploy each.

- Optional: add a Lambda validator that enforces a rule JSON Schema can't
  express, for example "the limit may not change by more than half from
  the deployed value". It must finish within 15 seconds, and AppConfig
  needs permission to invoke it.

##### Question: When Validation Runs

_At which step did the invalid version fail: when you created it, or when
you tried to deploy it? What does that tell you about where to validate in
a pipeline?_

#### Lab 11.3.5: Feature Flags in a Lambda Function

Applications normally read AppConfig through the
[AppConfig Agent](https://docs.aws.amazon.com/appconfig/latest/userguide/appconfig-integration-lambda-extensions.html),
which polls in the background, caches the data and serves it on
`localhost:2772`. On Lambda it is an extension layer, and AWS publishes the
latest layer ARN as a public parameter: back to Lesson 11.1.

- Create a Python 3.13 function whose response depends on the `show-team`
  and `banner` flags, reading them from
  `http://localhost:2772/applications/<app>/environments/lab/configurations/<profile>`.

- Add the layer with a dynamic reference to
  `/aws/service/aws-appconfig/lambda-extension/x86/latest` (or `arm64`),
  and give the execution role `appconfig:StartConfigurationSession` and
  `appconfig:GetLatestConfiguration` on your application only.

- Invoke it, flip a flag with a new deployment, and invoke it again.

##### Question: The Agent

_How long did the function take to see the change, and which setting
controls that? What does the agent do for you that calling
`get-latest-configuration` on every invocation wouldn't, and how does that
change the bill? The same agent runs on EC2, ECS and EKS._

#### Lab 11.3.6: Clean Up

Remove everything this module created:

- Delete the AppConfig and Lambda stacks. If
  [deletion protection](https://docs.aws.amazon.com/appconfig/latest/userguide/deletion-protection.html)
  is on in your account (`aws appconfig get-account-settings`), an
  environment or profile read in the last hour can't be deleted yet: wait,
  or bypass the check deliberately.

- Delete the secrets stacks, then check with
  `aws secretsmanager list-secrets --include-planned-deletion` that no
  secret of yours is left in an active state. Delete leftovers with
  `delete-secret`; `--force-delete-without-recovery` is fine for lab data.
  <!-- VERIFY: whether deleting an AWS::SecretsManager::Secret through a
  stack deletes it immediately or schedules it with a recovery window;
  check with list-secrets --include-planned-deletion after the delete. -->

- Schedule the customer managed KMS key for deletion (seven days is the
  minimum) after the secret that uses it is gone.

- Delete the parameter stack and the parameters you created with the CLI
  ("middle-name" and any leftovers under your prefix): list them with
  `aws ssm get-parameters-by-path --path /<your-id>/stelligent-u/lab11/
  --recursive`, and make sure no advanced parameter remains.

- Delete the log groups your Lambda functions created.

### Retrospective 11.3

#### Question: Three Stores

_Sketch the configuration for a small web service: its database
credentials, a third-party API key, the database hostname, the AMI it runs,
a log level and a new checkout feature to release to 10% of users. Put each
in Parameter Store, Secrets Manager or AppConfig (or leave it in code), and
say how the application gets it and how a change reaches production._

## Further Reading

- [Organize parameters by hierarchy, tags, or Amazon CloudWatch Events](https://aws.amazon.com/blogs/mt/organize-parameters-by-hierarchy-tags-or-amazon-cloudwatch-events-with-amazon-ec2-systems-manager-parameter-store/)
  is an older post, but the hierarchy and IAM ideas still hold.

- The
  [Parameters and Secrets Lambda extension](https://docs.aws.amazon.com/systems-manager/latest/userguide/ps-integration-lambda-extensions.html)
  and the
  [Secrets Manager Agent](https://docs.aws.amazon.com/secretsmanager/latest/userguide/secrets-manager-agent.html)
  cache values locally, as the AppConfig Agent does, so functions and
  instances don't call the API on every request.

- [Managed rotation](https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotate-secrets_managed.html)
  lists the services that rotate their own secrets, and
  [managed external secrets](https://docs.aws.amazon.com/secretsmanager/latest/userguide/managed-external-secrets.html)
  extends that to SaaS partners.

- [Sharing parameters](https://docs.aws.amazon.com/systems-manager/latest/userguide/parameter-store-shared-parameters.html)
  across accounts with AWS RAM works for advanced parameters, and
  [Parameter Store throughput](https://docs.aws.amazon.com/systems-manager/latest/userguide/parameter-store-throughput.html)
  explains the default limit of 40 transactions per second and what raising
  it costs.

- [Monitoring deployments for automatic rollback](https://docs.aws.amazon.com/appconfig/latest/userguide/monitoring-deployments.html)
  and
  [AppConfig experimentation](https://docs.aws.amazon.com/appconfig/latest/userguide/appconfig-experimentation.html)
  go further with Lesson 11.3.

- The [Secrets Manager FAQ](https://aws.amazon.com/secrets-manager/faqs/)
  is a succinct summary of the service.
