# Topic 25: AWS CDK in Python

<!-- TOC -->

- [Topic 25: AWS CDK in Python](#topic-25-aws-cdk-in-python)
  - [What changed in the 2026 edition](#what-changed-in-the-2026-edition)
  - [Exam coverage](#exam-coverage)
  - [Cost and cleanup](#cost-and-cleanup)
  - [Guidance](#guidance)
  - [Conventions](#conventions)
  - [Lesson 25.1: From templates to code](#lesson-251-from-templates-to-code)
    - [Principle 25.1](#principle-251)
    - [Practice 25.1](#practice-251)
      - [Lab 25.1.1: Toolchain and a new app](#lab-2511-toolchain-and-a-new-app)
      - [Lab 25.1.2: Synthesize without an account](#lab-2512-synthesize-without-an-account)
      - [Lab 25.1.3: Bootstrap the lab account](#lab-2513-bootstrap-the-lab-account)
      - [Lab 25.1.4: Deploy, diff, destroy](#lab-2514-deploy-diff-destroy)
    - [Retrospective 25.1](#retrospective-251)
  - [Lesson 25.2: Constructs](#lesson-252-constructs)
    - [Principle 25.2](#principle-252)
    - [Practice 25.2](#practice-252)
      - [Lab 25.2.1: One bucket, two levels, one escape hatch](#lab-2521-one-bucket-two-levels-one-escape-hatch)
      - [Lab 25.2.2: An L3 pattern you only synthesize](#lab-2522-an-l3-pattern-you-only-synthesize)
      - [Lab 25.2.3: Your own construct](#lab-2523-your-own-construct)
    - [Retrospective 25.2](#retrospective-252)
  - [Lesson 25.3: Environments, context and assets](#lesson-253-environments-context-and-assets)
    - [Principle 25.3](#principle-253)
    - [Practice 25.3](#practice-253)
      - [Lab 25.3.1: Environment-agnostic and environment-specific](#lab-2531-environment-agnostic-and-environment-specific)
      - [Lab 25.3.2: Context values and lookups](#lab-2532-context-values-and-lookups)
      - [Lab 25.3.3: Assets](#lab-2533-assets)
    - [Retrospective 25.3](#retrospective-253)
  - [Lesson 25.4: Aspects and compliance](#lesson-254-aspects-and-compliance)
    - [Principle 25.4](#principle-254)
    - [Practice 25.4](#practice-254)
      - [Lab 25.4.1: Tags on everything](#lab-2541-tags-on-everything)
      - [Lab 25.4.2: A guardrail aspect](#lab-2542-a-guardrail-aspect)
      - [Lab 25.4.3: cdk-nag](#lab-2543-cdk-nag)
    - [Retrospective 25.4](#retrospective-254)
  - [Lesson 25.5: Testing infrastructure code](#lesson-255-testing-infrastructure-code)
    - [Principle 25.5](#principle-255)
    - [Practice 25.5](#practice-255)
      - [Lab 25.5.1: Fine-grained assertions](#lab-2551-fine-grained-assertions)
      - [Lab 25.5.2: Test what your construct promises](#lab-2552-test-what-your-construct-promises)
      - [Lab 25.5.3: Tests in the loop](#lab-2553-tests-in-the-loop)
    - [Retrospective 25.5](#retrospective-255)
  - [Lesson 25.6: Apps with more than one stack](#lesson-256-apps-with-more-than-one-stack)
    - [Principle 25.6](#principle-256)
    - [Practice 25.6](#practice-256)
      - [Lab 25.6.1: Pass an object between stacks](#lab-2561-pass-an-object-between-stacks)
      - [Lab 25.6.2: The deadly embrace](#lab-2562-the-deadly-embrace)
      - [Lab 25.6.3: Decouple with Parameter Store](#lab-2563-decouple-with-parameter-store)
    - [Retrospective 25.6](#retrospective-256)
  - [Lesson 25.7: Adopting and delivering CDK](#lesson-257-adopting-and-delivering-cdk)
    - [Principle 25.7](#principle-257)
    - [Practice 25.7](#practice-257)
      - [Lab 25.7.1: Import a bucket you made by hand](#lab-2571-import-a-bucket-you-made-by-hand)
      - [Lab 25.7.2: Migrate a Lesson 1 template](#lab-2572-migrate-a-lesson-1-template)
      - [Lab 25.7.3: Deploy from GitHub Actions (stretch)](#lab-2573-deploy-from-github-actions-stretch)
      - [Lab 25.7.4: CDK Pipelines (stretch)](#lab-2574-cdk-pipelines-stretch)
      - [Lab 25.7.5: Clean up the module](#lab-2575-clean-up-the-module)
    - [Retrospective 25.7](#retrospective-257)
  - [Further Reading](#further-reading)

<!-- /TOC -->

## What changed in the 2026 edition

- **New module.** The 2022 course taught CloudFormation (module 01), SAM
  (module 16) and Terraform (module 17), but not the AWS Cloud
  Development Kit. CDK is named in the CloudOps (SOA-C03, Skill 3.1.2)
  and DevOps Pro (DOP-C02, Task 2.1) exam guides, and it's how many teams
  now write CloudFormation. The course uses **Python**, the language the
  rest of the course scripts in.
- **CDK v2 only.** CDK v1 reached end of support on June 1, 2023. Older
  blog posts that `pip install aws-cdk.aws-s3` one package per service
  are v1; in v2 everything is in the single `aws-cdk-lib` package.
- **The CLI and the library are versioned separately.** Since February
  2025 the CDK CLI has its own version line (2.1000.0 and up) while
  `aws-cdk-lib` stays on 2.x (2.2xx at the time of writing). A newer CLI
  always works with an older library; an older CLI may refuse a newer
  library's cloud assembly.
- **Node.js 22 or later** is required for the CLI, whatever language
  your app is in.
- **The CLI collects anonymous telemetry by default** (CLI 2.1100.0 and
  later). Lab 25.1.1 shows how to check and opt out.
- **New CLI commands** that older material won't mention: `cdk drift`,
  `cdk gc` (garbage-collects old assets from the bootstrap bucket),
  `cdk refactor` (renames and moves resources without replacing them,
  using CloudFormation stack refactoring), `cdk orphan`, `cdk flags`, and
  `cdk migrate` (turns a template, a stack or scanned resources into a
  CDK app). `cdk diff` now creates a read-only change set by default,
  so it reports replacements accurately.
- **cdk-nag 3.x is a validation plugin, not an aspect.** Most tutorials
  show `Aspects.of(app).add(AwsSolutionsChecks())` and
  `NagSuppressions`; version 3 registers with `Validations.of(app)` and
  suppresses with `Validations.of(construct).acknowledge(...)`.
- **CDK for Terraform (CDKTF) was archived by HashiCorp in December
  2025.** If a team wants "CDK, but Terraform", the options are now HCL
  (module 17) or the AWS CDK.

## Exam coverage

| Exam | Domain / task statement |
|---|---|
| SOA-C03 | Domain 3: Deployment, Provisioning, and Automation (Skill 3.1.2: create and manage AWS resources by using CloudFormation and the AWS CDK; Skill 3.1.3: identify and remediate deployment issues; Skill 3.1.6: third-party tools such as Terraform, for the comparison) |
| DVA-C02 → C03 | Domain 3: Deployment (Task 3.1: prepare application artifacts; Skill 3.3.4: implement and deploy infrastructure as code templates; Skill 3.4.3: update existing IaC templates; Skill 3.4.7: orchestrated workflows to deploy code to different environments) |
| DVA-C02 → C03 | Domain 1: Development with AWS Services (Skill 1.1.7: write and run unit tests in development environments). C03 guide publishes 2026-10-27 and adds GenAI / agent topics |
| DOP-C02 | Domain 2: Configuration Management and IaC (Task 2.1: composing and deploying IaC templates, including AWS CDK; implementing governance controls and security standards in reusable IaC, including AWS CDK) |
| DOP-C02 | Domain 1: SDLC Automation (Task 1.1: CI/CD pipelines; Task 1.2: automating unit tests and security scans in pipelines) |

## Cost and cleanup

Almost everything this module deploys is free or costs cents. Two things
need attention: the **bootstrap stack**, which outlives every app you
destroy, and the **L3 pattern** in Lab 25.2.2, which you synthesize but
must not deploy.

- **The bootstrap stack (`CDKToolkit`)** holds an S3 bucket for file
  assets, an ECR repository for container image assets, five IAM roles
  and an SSM parameter. The roles and parameter are free. You pay for
  storage in the bucket and the repository, which for this module's
  small Lambda bundles is a few cents a month. The bucket is versioned,
  so old asset versions stay until `cdk gc` or a lifecycle rule removes
  them. The current template creates no customer managed KMS key; older
  bootstrap stacks did, at about $1 a month each.
- **`cdk destroy` doesn't remove the bootstrap stack**, and deleting
  the bootstrap stack doesn't remove its bucket: the bucket has
  `DeletionPolicy: Retain`. The ECR repository is deleted with the stack
  only if it's empty. [Lab 25.7.5](#lab-2575-clean-up-the-module) walks
  through removing all of it, and the order that works.
- **Retained resources.** L2 constructs default stateful resources to
  `RemovalPolicy.RETAIN`: an S3 bucket, and the log group CDK now creates
  for each Lambda function, survive `cdk destroy`. Lab 25.1.4 shows it;
  Lab 25.7.5 finds and removes the leftovers.
- **Lab 25.2.2 is synthesize-only.** The pattern it uses would create a
  load balancer, two NAT gateways and two Elastic IPs, all billed
  hourly. Don't deploy it.
- **Stretch labs.** A CDK Pipeline (Lab 25.7.4) uses CodePipeline V2,
  billed at $0.002 per action execution minute after 100 free minutes a
  month, plus CodeBuild minutes for every synth, asset publish and
  self-mutation. GitHub Actions (Lab 25.7.3) uses GitHub's minutes, not
  AWS's.
- **Cleanup:** [Lab 25.7.5](#lab-2575-clean-up-the-module) destroys
  every app, removes retained buckets and log groups, the GitHub OIDC
  role, the pipeline, and then, if you choose, the bootstrap stack and
  its retained bucket.

<!-- VERIFY: CodePipeline V2 price and free minutes were read from the
pricing page in September 2026 (us-east-1 figures); check us-east-2. -->

## Guidance

- Explore the official docs! See the
  [AWS CDK v2 Developer Guide](https://docs.aws.amazon.com/cdk/v2/guide/home.html),
  especially
  [Working with the AWS CDK in Python](https://docs.aws.amazon.com/cdk/v2/guide/work-with-cdk-python.html),
  the [CDK CLI reference](https://docs.aws.amazon.com/cdk/v2/guide/cli.html),
  the [Python API reference](https://docs.aws.amazon.com/cdk/api/v2/python/)
  and the [Construct Library overview](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-construct-library.html).

- Read [Best practices for developing and deploying cloud infrastructure
  with the AWS
  CDK](https://docs.aws.amazon.com/cdk/v2/guide/best-practices.html)
  before Lesson 25.3 and again at the end. Several retrospective
  questions come from it.

- Keep the [CloudFormation Template
  Reference](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/introduction.html)
  open. CDK writes CloudFormation; when the Python API is unclear, the
  resource's CloudFormation page usually explains the property.

- Avoid using other sites like stackoverflow.com for answers \-- part
  of the skill set you're building is finding answers straight from
  the source, AWS.

- Explore your curiosity. Try to understand why things work the way
  they do. Read more of the documentation than just what you need to
  find the answers.

## Conventions

- **Profile and Region.** Everything runs in the lab account in
  `us-east-2` with the `lab` profile. Run `export AWS_PROFILE=lab` in
  each shell, or pass `--profile lab` to `cdk`. Don't hard-code a Region
  or account ID in your app; Lesson 25.3 shows the right way to say
  where a stack goes.
- **Placeholders.** Examples use `123456789012` for the lab account.
  Keep real account IDs out of your repository, including
  `cdk.context.json` (Lab 25.3.2 explains why that file needs a look
  before you commit it).
- **Names and tags** include your identifier. Every stack gets the tags
  `owner=<you>` and `topic=25` (Lab 25.4.1 does it once for the whole
  app), so Lab 25.7.5 can find what's left.
- **Your repository.** Keep your CDK app in `25-aws-cdk/` of your lab
  repository. Commit `cdk.json`, `cdk.context.json`, `requirements*.txt`
  and your code; never commit `cdk.out/` or `.venv/`. `cdk init` writes a
  `.gitignore` that already excludes them.
- **CloudFormation stays the engine.** You'll still read templates,
  change sets and stack events. When a deploy fails, the stack events in
  the CloudFormation console or `aws cloudformation describe-stack-events`
  tell you why, exactly as in module 01.

## Lesson 25.1: From templates to code

### Principle 25.1

*The CDK is a program that writes CloudFormation. You get loops,
functions, classes and tests, but what gets deployed is still a
template, a stack and a change set.*

### Practice 25.1

A CDK **app** is a tree of **constructs**. The root is an `App`; its
children are **stacks** (each becomes one CloudFormation stack); their
children are the resources and higher-level constructs you write.
Running the app (`cdk synth`) walks that tree and writes a **cloud
assembly** in `cdk.out/`: one CloudFormation template per stack, plus
manifests that describe the **assets** (files and Docker images) the
templates depend on. `cdk deploy` uploads the assets and deploys each
template as a stack.

Read [AWS CDK apps](https://docs.aws.amazon.com/cdk/v2/guide/apps.html),
[Introduction to AWS CDK
stacks](https://docs.aws.amazon.com/cdk/v2/guide/stacks.html) and [AWS CDK
Constructs](https://docs.aws.amazon.com/cdk/v2/guide/constructs.html)
before you start.

You have now met three ways to write infrastructure as code in this
course. Keep this table in mind; the retrospectives come back to it.

| | CloudFormation (module 01) | AWS CDK (this module) | Terraform (module 17) |
|---|---|---|---|
| You write | YAML templates | Python (or TypeScript, Java, C#, Go) that synthesizes templates | HCL |
| Deployment engine | CloudFormation | CloudFormation | Terraform CLI calling AWS APIs through a provider |
| Where state lives | The stack, inside CloudFormation | The stack, inside CloudFormation | A state file you store and lock (S3 with `use_lockfile`) |
| Preview a change | Change set | `cdk diff` (creates a change set) | `terraform plan` |
| Reuse | Nested stacks, modules, macros | Constructs published as libraries | Modules from a registry |
| Bring existing resources in | Resource import, IaC generator | `cdk import`, `cdk migrate` | `import` blocks |
| Find drift | Drift detection | `cdk drift` | `terraform plan` |
| Rename without replacing | Stack refactoring | `cdk refactor` | `moved` blocks |
| Unit tests | cfn-lint and Guard check the template | `aws_cdk.assertions` against the synthesized template | `terraform test` |
| Per-account setup | None | `cdk bootstrap` once per account and Region | A state bucket |

#### Lab 25.1.1: Toolchain and a new app

- Install [Node.js 22 or
  later](https://docs.aws.amazon.com/cdk/v2/guide/prerequisites.html)
  (an active LTS release) and Python 3.12 or 3.13. Then install the CDK
  CLI with `npm install -g aws-cdk`, or run it without installing through
  `npx aws-cdk`. Run `cdk --version`.

- Read [Configure AWS CDK CLI
  telemetry](https://docs.aws.amazon.com/cdk/v2/guide/cli-telemetry.html).
  Run `cdk cli-telemetry --status`. Decide whether to opt out, and write
  down which of the documented methods you used, if any.

- In `25-aws-cdk/` of your lab repository, make a directory named
  `lab25` and run `cdk init app --language python` inside it. Create and
  activate the virtual environment it tells you about and install
  `requirements.txt` and `requirements-dev.txt`.

- Tour what `init` created: `app.py`, the `lab25/lab25_stack.py` module,
  `cdk.json`, `requirements.txt` and the test under `tests/unit/`. In
  `cdk.json`, find the `app` key and the long `context` block of feature
  flags. Run `cdk flags` and read [Feature
  flags](https://docs.aws.amazon.com/cdk/v2/guide/featureflags.html).

- Compare `cdk --version` with the `aws-cdk-lib` version `pip` installed,
  and read [AWS CDK
  versioning](https://docs.aws.amazon.com/cdk/v2/guide/versioning.html).

##### Question: Two version numbers

_Why are the CLI and the library versioned separately? If your teammate
has an older CLI than the `aws-cdk-lib` in `requirements.txt`, what
happens when they deploy, and which of the two should a pipeline pin?_

##### Question: What a feature flag protects

_A new `cdk init` project turns dozens of flags on; an app created three
years ago has them off. Why doesn't the CDK just change the defaults for
everyone? Pick one flag from your `cdk.json` and explain what it changes
in the synthesized template._

#### Lab 25.1.2: Synthesize without an account

- In `Lab25Stack`, add one S3 bucket using `aws_s3.Bucket`, with
  versioning on. Leave the stack's `env` unset, as `init` wrote it.

- Run `cdk synth` with **no AWS credentials at all** (for example,
  `AWS_PROFILE=` and no SSO session). It should still work. Find the
  template in `cdk.out/`, and the one `cdk synth` printed.

- Compare it with the template you wrote in Lab 1.1.1. Note the
  logical ID CDK chose for the bucket, the `DeletionPolicy`, the
  `AWS::CDK::Metadata` resource, and the `BootstrapVersion` parameter and
  its rule.

- Run `cfn-lint` on the synthesized template. It should be clean; you'll
  run it again when the templates grow.

- Run the test `init` generated (`python -m pytest`), then read it. It
  is commented out; you'll write real tests in Lesson 25.5.

##### Question: Logical IDs

_Where does the suffix on the bucket's logical ID come from? Read
[Identifiers and the AWS
CDK](https://docs.aws.amazon.com/cdk/v2/guide/identifiers.html). What
happens to the deployed bucket if you rename the construct ID from
`Notes` to `NotesBucket`, or move the bucket into a construct of its
own? (Lesson 25.7 comes back to this.)_

##### Question: What synth needs

_`cdk synth` worked with no credentials. What would make it need them?
Name two things you could add to the stack that would break synthesis
without an account._

#### Lab 25.1.3: Bootstrap the lab account

Before the CDK can deploy anything into an account and Region, it needs
a few resources there: somewhere to upload assets and roles to deploy
with. That's the **bootstrap stack**, deployed once per environment.

- Read [AWS CDK
  bootstrapping](https://docs.aws.amazon.com/cdk/v2/guide/bootstrapping.html)
  and [Bootstrap your
  environment](https://docs.aws.amazon.com/cdk/v2/guide/bootstrapping-env.html).

- Before you deploy anything, look at what you're about to deploy:
  `cdk bootstrap --show-template > bootstrap-template.yaml`. Don't commit
  it. Find:
  - the staging bucket, its name pattern, its lifecycle rules and its
    `DeletionPolicy`;
  - the ECR repository and its lifecycle policy;
  - the five IAM roles, and which of them CloudFormation itself assumes;
  - the `CloudFormationExecutionPolicies` parameter, and the policy the
    execution role gets when it's empty;
  - the SSM parameter that records the bootstrap version.

- Bootstrap the lab account in `us-east-2` with the `lab` profile. Tag
  the stack (`--tags owner=<you> --tags topic=25`) and turn on
  `--termination-protection`, as the docs recommend.

- List what was created: `aws cloudformation describe-stack-resources
  --stack-name CDKToolkit`, and read the version with `aws ssm
  get-parameter --name /cdk-bootstrap/hnb659fds/version`.

##### Question: The execution role

_By default the CloudFormation execution role has `AdministratorAccess`.
Your Identity Center role in the lab account is probably an administrator
too. Once bootstrapped, who can deploy what? Read [Customize AWS CDK
bootstrapping](https://docs.aws.amazon.com/cdk/v2/guide/bootstrapping-customizing.html):
what would `--cloudformation-execution-policies` with a narrower policy
change, and what would break?_

##### Question: The qualifier

_Every bootstrap resource name contains `hnb659fds`. What is it, and
when would you bootstrap with a different `--qualifier`?_

#### Lab 25.1.4: Deploy, diff, destroy

- `cdk deploy`. Watch the progress output, then find the same stack in
  `aws cloudformation describe-stacks`. Which role did CloudFormation
  use (`RoleARN`)?

- Add a tag or a lifecycle rule to the bucket and run `cdk diff`. Read
  the [`cdk diff` reference](https://docs.aws.amazon.com/cdk/v2/guide/ref-cli-cmd-diff.html):
  what did it create to compute the diff, and with which role? Deploy.

- Change something that forces replacement, such as the bucket name
  (add `bucket_name` with your identifier). Run `cdk diff` again and find
  where it says so. Don't deploy it; revert.

- Put an object in the bucket, then `cdk destroy`. Is the bucket gone?
  Look at the `DeletionPolicy` in the template you synthesized.

- Change the bucket to `removal_policy=RemovalPolicy.DESTROY` and
  `auto_delete_objects=True`, synthesize, and look at what that added to
  the template. Deploy, put an object in, destroy again. Delete the
  bucket that the first destroy left behind.

##### Question: Retain by default

_Why does the CDK retain buckets by default when a plain
`AWS::S3::Bucket` in module 01 was deleted with its stack? What did
`auto_delete_objects` add to your stack to be able to empty the bucket,
and would you use it in production?_

##### Question: diff and change sets

_Module 01 had you create and read change sets by hand. What does
`cdk diff` show that a change set's `describe-change-set` output
doesn't, and the other way round? What does `cdk deploy
--method=prepare-change-set` let you do?_

### Retrospective 25.1

#### Question: Where the state lives

_Terraform (module 17) keeps state in a file you have to store, lock and
protect. Where is the CDK's state? What's in `cdk.out/`, and what would
you lose if you deleted it? What would you lose if someone deleted the
`CDKToolkit` stack?_

## Lesson 25.2: Constructs

### Principle 25.2

*Constructs are the unit of reuse. Low-level ones map one-to-one onto
CloudFormation; higher-level ones encode someone's decisions, so read
what they create before you trust them.*

### Practice 25.2

The Construct Library has three levels:

- **L1** constructs are generated from the CloudFormation resource
  specification. `s3.CfnBucket` is exactly `AWS::S3::Bucket`, with the
  same properties and no defaults of its own.
- **L2** constructs, such as `s3.Bucket`, add sensible defaults, helper
  methods (`grant_read`, `add_event_notification`) and types instead of
  strings.
- **L3** constructs, or *patterns*, combine several resources into one
  architecture, such as a load-balanced Fargate service.

When an L2 doesn't expose a property, you reach down to its L1 with an
**escape hatch**. Read [Resources and the AWS
CDK](https://docs.aws.amazon.com/cdk/v2/guide/resources.html) and
[Customize constructs from the AWS Construct
Library](https://docs.aws.amazon.com/cdk/v2/guide/cfn-layer.html).

#### Lab 25.2.1: One bucket, two levels, one escape hatch

- In a new stack, `ConstructLevelsStack`, add one bucket with
  `s3.CfnBucket` and one with `s3.Bucket(..., enforce_ssl=True,
  versioned=True)`. Synthesize and compare the two in the template. What
  did the L2 add that you didn't ask for? What would you have to write to
  get the same result at L1?

- Look at the `Bucket` L2 in the [Python API
  reference](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_s3/Bucket.html)
  and pick a CloudFormation property of `AWS::S3::Bucket` it doesn't
  expose. Set it with an escape hatch: get the L1 through
  `bucket.node.default_child` and set the property on it, or use
  `add_property_override`.

- Synthesize and check the property is in the template. Run `cfn-lint`.

##### Question: Escape hatch or raw override

_What's the difference between setting a property on the L1 object and
calling `add_property_override`? Which one does the CDK check for you,
and which would let you write a typo that only CloudFormation catches?_

#### Lab 25.2.2: An L3 pattern you only synthesize

**Don't deploy this stack.** It exists to show what one line of CDK can
cost.

- In a separate stack, add an
  [`ApplicationLoadBalancedFargateService`](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_ecs_patterns/README.html)
  running a public image such as `public.ecr.aws/nginx/nginx`, with no
  other properties.

- Synthesize it. Count the resources in its template by type (a few
  lines of `jq` or Python over the JSON).

- Find the NAT gateways, Elastic IPs and the load balancer. Using the
  [Amazon VPC pricing](https://aws.amazon.com/vpc/pricing/) and Elastic
  Load Balancing pricing pages, estimate what this stack would cost per
  day in `us-east-2` if you deployed it and forgot it.

- Find the properties that would let you pass in an existing VPC or
  control the NAT gateways. Then remove the stack from `app.py`.

##### Question: Reading before trusting

_The pattern made a VPC because you didn't give it one. What other
decisions did it make for you (subnets, security group rules, logging,
health checks)? How would you find out, before deploying, what a
third-party construct from
[Construct Hub](https://constructs.dev/) will create?_

#### Lab 25.2.3: Your own construct

Write an L3 of your own: a class that extends `Construct` and is used
like any library construct. Lessons 25.3 to 25.5 build on it.

- Create `lab25/notes_intake.py` with a construct `NotesIntake` that
  creates:
  - an S3 bucket, versioned, with SSL enforced;
  - a Python 3.13 Lambda function (code comes in Lab 25.3.3; use
    `lambda_.Code.from_inline` for now) that the bucket notifies when an
    object is created under `incoming/`;
  - read access for the function to that bucket, and nothing more.

- Let the caller pass options through a small set of keyword arguments
  (for example, how many days to keep noncurrent versions), and expose
  the bucket and function as read-only attributes so other code can use
  them.

- Use it from `Lab25Stack` and deploy. Upload a file under `incoming/`
  and find the invocation in the function's logs (`aws logs tail`).

##### Question: What grant_read wrote

_Look at the IAM policy `grant_read` generated. Which actions and
resources did it allow? Is it least privilege for what your function
does? How would you narrow it, and what would you give up?_

##### Question: Props and defaults

_Your construct made choices (runtime, versioning, SSL) that its callers
can't change. Which of those should be options, and which should be
fixed so every team using it gets them? How is this different from a
CloudFormation module or a Terraform module's variables?_

### Retrospective 25.2

#### Question: Constructs, modules and nested stacks

_You've now seen four ways to package infrastructure for reuse:
CloudFormation nested stacks, CloudFormation modules, Terraform modules
and CDK constructs. For each, where does the reusable piece live, how is
a new version released, and what does a consumer have to do to upgrade?_

## Lesson 25.3: Environments, context and assets

### Principle 25.3

*A stack either knows where it's going or it doesn't. Decide on purpose:
environment-agnostic stacks deploy anywhere, environment-specific ones
can look things up, and both should be reproducible from what's in the
repository.*

### Practice 25.3

An **environment** is an account plus a Region. A stack without `env`
is **environment-agnostic**: its template uses pseudo-parameters such as
`AWS::Region`, and it can be deployed anywhere, but it can't look
anything up at synthesis time. A stack with `env` is
**environment-specific**: the CDK knows the account and Region while it
synthesizes, can query them (the VPC, the AZs, an SSM parameter), and
caches what it found as **context** in `cdk.json`'s sibling
`cdk.context.json`. **Assets** are local files or Docker images the
stack needs at deploy time: the CLI builds and uploads them to the
bootstrap bucket or repository and wires their location into the
template.

Read [Environments for the AWS
CDK](https://docs.aws.amazon.com/cdk/v2/guide/environments.html),
[Context values and the AWS
CDK](https://docs.aws.amazon.com/cdk/v2/guide/context.html) and [Assets
and the AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/assets.html).

#### Lab 25.3.1: Environment-agnostic and environment-specific

- In `Lab25Stack`, add a `CfnOutput` of `self.availability_zones` joined
  into one string, and synthesize. What did the AZs become in the
  template?

- Now make the stack environment-specific, taking the account and Region
  from the CLI: `env=cdk.Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"),
  region=os.getenv("CDK_DEFAULT_REGION"))`. Synthesize with the `lab`
  profile. What are the AZs now? Look in `cdk.context.json`.

- Synthesize again with no credentials. Why does it still work?

- Read [Configure environments to use with the AWS
  CDK](https://docs.aws.amazon.com/cdk/v2/guide/configure-env.html).
  Where do `CDK_DEFAULT_ACCOUNT` and `CDK_DEFAULT_REGION` come from, and
  what's the difference between them and `CDK_DEPLOY_ACCOUNT` in the
  docs' examples?

##### Question: Agnostic or specific

_The docs recommend environment-specific stacks for production. Why,
given that environment-agnostic templates are more portable? When would
you still choose agnostic? Compare with Lesson 1.3, where one template
went to several Regions._

#### Lab 25.3.2: Context values and lookups

- Take your identifier from context instead of hard-coding it: read it
  with `self.node.try_get_context("owner")`, fail synthesis with a clear
  message if it's missing, and supply it once in `cdk.json` and once with
  `cdk synth -c owner=<you>`. Which one wins?

- Use it to name the stack (`stack_name=f"{owner}-lab25"`) and to add a
  second instance of the stack for a `test` stage, chosen with
  `-c stage=test`. Both deploy from the same app; the construct IDs must
  differ.

- Look up the latest Amazon Linux 2023 AMI **two ways** and output both:
  - `ssm.StringParameter.value_from_lookup` on
    `/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64`;
  - `ec2.MachineImage.latest_amazon_linux2023()` and its `get_image`.

  Synthesize and compare how each appears in the template, and what each
  added to `cdk.context.json`.

- Try the first one in an environment-agnostic stack. Read the error.

- Run `cdk context`, then `cdk context --reset <key>` for the AMI entry,
  and synthesize again.

##### Question: Committing cdk.context.json

_The docs tell you to commit `cdk.context.json`. Why is caching lookups
at synthesis time safer than doing them at deploy time? What's in the
file that a public repository shouldn't show, and what will you do about
it? (Check the file before every commit in this module.)_

##### Question: Synthesis time or deploy time

_One AMI lookup is resolved when you synthesize, the other when
CloudFormation deploys. For an Auto Scaling group, which would you want,
and why? What happens to each when AWS publishes a new AMI tomorrow?_

#### Lab 25.3.3: Assets

- Move the function code from Lab 25.2.3 into a directory,
  `lambda/notes_intake/`, and load it with `lambda_.Code.from_asset`.
  Have it log the bucket and key it was invoked for, as structured JSON.

- Synthesize. In `cdk.out/`, find the asset directory and the
  `*.assets.json` manifest. Match the asset hash to the `S3Key` in the
  function's `Code` in the template.

- Deploy, then list the bootstrap bucket. Change one line of the
  function, deploy again, and list it again.

- Try `cdk deploy --hotswap` after another small code change. Read [the
  `cdk deploy`
  reference](https://docs.aws.amazon.com/cdk/v2/guide/ref-cli-cmd-deploy.html)
  on hotswap: what did it skip, and what does that do to drift?

- Run `cfn-lint` on the template again. Lambda functions and the
  auto-delete custom resource (if you kept it) usually bring warnings
  about redundant `DependsOn`. Whose code generated them, and what would you do about
  warnings you can't fix in your own code?

- Run `cdk gc --unstable=gc --action=print` and read [`cdk
  gc`](https://docs.aws.amazon.com/cdk/v2/guide/ref-cli-cmd-gc.html).
  How many unused assets does it find?

*Optional: add a container image asset (`DockerImageAsset` or
`lambda_.DockerImageCode.from_image_asset`) to see the ECR side of
bootstrapping. It needs Docker locally and leaves images in the
bootstrap repository; Lab 25.7.5 has to remove them.*

##### Question: Old assets

_Every code change uploads a new object to the bootstrap bucket. What
removes the old ones: the bucket's lifecycle rules, `cdk gc`, or
nothing? Why doesn't `cdk gc` delete an asset the moment no template
uses it (look at `--rollback-buffer-days`)?_

### Retrospective 25.3

#### Question: One template or many

_Lesson 1.3 deployed one parameterized template to many Regions. A CDK
app with environment-specific stacks synthesizes a different template for
every environment. What does each approach make easier: reviewing a
change, rolling back, proving that test and production are the same?
Which would you choose for a team with three accounts?_

## Lesson 25.4: Aspects and compliance

### Principle 25.4

*Rules that apply to everything shouldn't be repeated on everything.
Aspects visit the whole construct tree, so you can tag it, check it or
fix it in one place, and fail the build before a bad template exists.*

### Practice 25.4

An **aspect** is an object with a `visit(node)` method. Registered with
`Aspects.of(scope).add(...)`, it is called for every construct in that
scope during synthesis, after your code has run. **Mutating** aspects
change constructs (the CDK's own tagging is one). **Read-only** aspects
inspect them and add error or warning **annotations**; an error stops
synthesis. Priorities control the order: mutating aspects run first,
read-only ones last, so a checker sees the tags a tagger added.

Separately, **validation plugins** run on the synthesized templates.
The CDK adds a default plugin that checks templates with CloudFormation's
own rules, and you can add others, such as cdk-nag.

Read [Aspects and the AWS
CDK](https://docs.aws.amazon.com/cdk/v2/guide/aspects.html), [Tags and
the AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/tagging.html) and
[AWS CDK validation at synthesis
time](https://docs.aws.amazon.com/cdk/v2/guide/policy-validation-synthesis.html).

#### Lab 25.4.1: Tags on everything

- In `app.py`, tag the whole app once: `cdk.Tags.of(app).add("owner",
  owner)` and `topic=25`.

- Synthesize and check that the bucket, the function, the IAM role and
  the log group all carry the tags. Which resources in your templates
  didn't get them, and why?

- Exclude one resource type from one tag with `exclude_resource_types`,
  and check the result.

- Deploy, then find everything with
  `aws resourcegroupstaggingapi get-resources --tag-filters
  Key=topic,Values=25`. Does the list include the stack itself?

##### Question: Tags on the stack

_CloudFormation propagates stack-level tags to resources that support
them. `Tags.of(app)` tags each resource in the template. What's the
practical difference? Which of the two does the bootstrap stack get from
your `--tags`?_

#### Lab 25.4.2: A guardrail aspect

The starter gives you the tests first. You write the aspects until the
tests pass.

- Copy [starter/lab25/guardrails.py](starter/lab25/guardrails.py) to
  `lab25/guardrails.py` and
  [starter/tests/unit/test_guardrails.py](starter/tests/unit/test_guardrails.py)
  to `tests/unit/`. Run `python -m pytest`: three tests fail.

- Implement `RequireTags` and `AllowedLambdaRuntimes` as the comments
  and tests describe. Both are read-only: they add error annotations and
  never change a resource.

- Register both on the app in `app.py` with
  `priority=cdk.AspectPriority.READONLY`, allowing only the runtimes the
  course uses. Synthesize: it should pass.

- Remove the `topic` tag from `app.py` and synthesize. Read the output,
  then put the tag back.

- Change your function's runtime to `PYTHON_3_9` and synthesize. Put it
  back.

##### Question: Order matters

_Register `RequireTags` with no priority, before the `Tags.of(app)`
calls, and synthesize: it still passes. Now write a test that does the
same in a bare `cdk.App()`: it fails. Look up the default of the
`priority` argument in the `Aspects` API reference, and find the
`@aws-cdk/core:aspectPrioritiesMutating` flag in your `cdk.json`. Why do
the two runs differ? What does that tell you about feature flags in unit
tests?_

##### Question: Fix or fail

_Your aspect fails the build when a tag is missing. It could add the tag
instead. When is a mutating aspect the better choice, and when does
silently fixing things hide a problem?_

#### Lab 25.4.3: cdk-nag

[cdk-nag](https://github.com/cdklabs/cdk-nag) checks your app against
rule packs such as *AWS Solutions*, *NIST 800-53* and *HIPAA*. (Its name
comes from cfn_nag, a template linter originally from Stelligent, the
company that wrote this course.)

- Add `cdk-nag` to `requirements.txt`. In `app.py`, register the AWS
  Solutions pack as a validation plugin:
  `cdk.Validations.of(app).add_plugins(AwsSolutionsChecks(app))`. If you
  find examples that use `Aspects.of(app).add(AwsSolutionsChecks())` and
  `NagSuppressions`, they're for cdk-nag 2.x; read the "Migrating from
  v2" section of the cdk-nag README.

- Synthesize. For each finding, decide: fix it in your construct, or
  acknowledge it with a reason using
  `cdk.Validations.of(construct).acknowledge(cdk.Acknowledgment(id=...,
  reason=...))`. Acknowledge at the narrowest scope that works.

- Find the findings about the IAM policy `grant_read` generated. Is the
  finding right? Fix or acknowledge it, and write down why.

- Find `validation-report.json` in `cdk.out/`. What would a pipeline do
  with it?

##### Question: Acknowledged is not fixed

_A reviewer sees ten acknowledgments in your pull request. What makes a
reason acceptable? Where would you keep a list of rules your
organization never allows anyone to acknowledge?_

### Retrospective 25.4

#### Question: Where compliance checks belong

_You've now met five places to check that "every bucket enforces SSL":
a CDK aspect or cdk-nag (at synthesis), cfn-lint or Guard (on the
template, Lab 1.4.1), a CloudFormation Hook (at deploy time), and an AWS
Config rule (after deployment, module 26). Which catches a bucket
someone created in the console? Which gives a developer the fastest
feedback? Which would you keep if you could have only two?_

## Lesson 25.5: Testing infrastructure code

### Principle 25.5

*Test the template your code produces, not the code itself. A good
infrastructure test states a property that must hold, such as "this
function can only read that bucket", and fails when a refactor breaks
it.*

### Practice 25.5

The `aws_cdk.assertions` module synthesizes a stack in memory and lets
you assert on the result: `Template` for resources, properties, outputs
and counts, `Annotations` for errors and warnings, `Match` for partial
matching and `Capture` for pulling values out to check them further.
These are unit tests: they run in seconds, need no AWS account, and fit
in any CI job. They can't tell you whether the stack deploys or the
application works; that takes integration tests against a real
deployment.

Read [Test AWS CDK
applications](https://docs.aws.amazon.com/cdk/v2/guide/testing.html) and
the [assertions module
README](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.assertions/README.html).

#### Lab 25.5.1: Fine-grained assertions

Write `tests/unit/test_lab25_stack.py` (replace what `init` generated):

- Use a pytest fixture that builds a fresh `App` and `Lab25Stack` for
  each test, with the context your stack needs (`owner`). Why a fresh
  `App` each time? Which settings from `cdk.json` does an `App` created
  in a test not see?

- Assert that there is exactly one `AWS::Lambda::Function` of *your*
  function's runtime (hint: `auto_delete_objects` adds another), that the
  bucket has versioning enabled (`has_resource_properties` with
  `Match.object_like`), and that the bucket policy denies requests
  without TLS.

- Assert that every resource that supports tags has `owner` and
  `topic` (use `find_resources` or `all_resources_properties`).

- Break each property in the stack in turn and watch the right test fail.

##### Question: Brittle or useful

_A test that asserts the exact logical ID of the bucket breaks when you
rename a construct. A test that asserts "some bucket has versioning"
passes when you add a second, unversioned bucket. How do you write
assertions that are neither?_

#### Lab 25.5.2: Test what your construct promises

Test `NotesIntake` on its own, in a bare `Stack`, not through
`Lab25Stack`:

- Use `Capture` to pull the function's IAM policy statements out of the
  template, and assert the function has read access to the bucket and no
  `s3:Put*` or `s3:Delete*` actions.

- Assert the bucket notification is filtered on the `incoming/` prefix.
  (Find which resource CDK used to configure bucket notifications before
  you write the assertion.)

- Assert that any option you exposed in Lab 25.2.3 changes the template
  the way it should, including its default.

- Add a test with `Annotations` that proves your guardrail aspect
  reports an untagged `NotesIntake`.

##### Question: Snapshot tests

_The docs also describe snapshot tests, which compare the whole template
with a stored copy. What do they catch that your fine-grained tests
don't? Why do teams that adopt them often end up approving snapshot
changes without reading them?_

#### Lab 25.5.3: Tests in the loop

- Make `cdk synth` run your tests first, so nobody deploys an untested
  app: look at what `cdk.json` can run before synthesis, or at a
  `Makefile` target. Decide which, and say why.

- Run `cdk diff --security-only` after changing the construct to grant
  write access. What does it report, and where in a pipeline would you
  want that?

- Change the grant back. Run the full test suite and `cdk synth` one
  last time before moving on.

##### Question: The integration test you didn't write

_Your unit tests prove the template is right. What could still go wrong
when you deploy it (think quotas, names already taken, service-linked
roles, SCPs from module 19)? Read the
[integ-tests](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.integ_tests_alpha/README.html)
module's README: what would an integration test for `NotesIntake` do,
and what would it cost to run on every pull request?_

### Retrospective 25.5

#### Question: What unit tests can't catch

_DOP-C02 asks where different kinds of tests belong in a pipeline. For
this app, place unit tests, cdk-nag, `cdk diff --security-only`, an
integration test, and a manual approval. Which stages block a merge, and
which block a production deployment?_

## Lesson 25.6: Apps with more than one stack

### Principle 25.6

*Stacks are units of deployment, not of organization. Split them where
the lifecycles differ, and know that every reference between stacks is a
CloudFormation export you'll have to unwind later.*

### Practice 25.6

In module 01 you exported a value from one stack and imported it into
another by hand. In CDK, you pass an object from one stack's constructor
to another's, and the CDK writes the `Export` and `Fn::ImportValue` for
you, and makes the consuming stack depend on the producing one. That's
convenient until you try to remove the reference: CloudFormation won't
let a stack delete an export another stack still imports. Read the
[stacks](https://docs.aws.amazon.com/cdk/v2/guide/stacks.html) page
section on references between stacks, and the [best
practices](https://docs.aws.amazon.com/cdk/v2/guide/best-practices.html)
on stateful resources.

#### Lab 25.6.1: Pass an object between stacks

- Split your app into two stacks: `StorageStack` with the bucket, and
  `ProcessingStack` with the function, which receives the bucket as a
  constructor argument. (Keep `NotesIntake` working, or have it accept an
  existing bucket.)

- Synthesize and find the `Outputs` with `Export` in one template and
  the `Fn::ImportValue` in the other. Compare the export names with the
  ones you wrote in Lab 1.2.2.

- `cdk list` shows the stacks; `cdk deploy --all` deploys them. In what
  order, and why?

- `aws cloudformation list-exports` and `list-imports` for the export.

##### Question: Bucket notifications across stacks

_If the bucket in `StorageStack` notifies the function in
`ProcessingStack`, which stack has to know about the other? Draw the
reference. What happens if both stacks need something from each other?_

#### Lab 25.6.2: The deadly embrace

- Change `ProcessingStack` so it no longer uses the bucket (for example,
  comment out the grant and the notification). Run `cdk deploy --all`.
  Read the error.

- Why did it happen? `StorageStack` deploys first, and the CDK removed
  the export because nothing uses it any more, but `ProcessingStack`
  still imports it.

- Fix it in two deployments: first keep the export alive in
  `StorageStack` with `self.export_value(...)` while deploying the change
  to `ProcessingStack`; then remove the `export_value` and deploy again.

- Restore the reference if you want to keep it.

##### Question: Same problem, three tools

_How did you get out of the same situation in Lab 1.2.4? What would the
equivalent be in Terraform, which has no exports? Which of the three
makes it easiest to see the dependency before it bites?_

#### Lab 25.6.3: Decouple with Parameter Store

- Replace the direct reference with a Parameter Store parameter:
  `StorageStack` writes the bucket name to
  `/<you>/lab25/notes-bucket-name`, and `ProcessingStack` reads it with
  `ssm.StringParameter.value_for_string_parameter`, then imports the
  bucket with `s3.Bucket.from_bucket_name`.

- Synthesize: the export is gone. Deploy both stacks, then deploy only
  `ProcessingStack` with `--exclusively`.

- What can you no longer do with an imported bucket that you could with
  the one you owned (for example, add a notification)?

##### Question: Cross-Region references

_Stacks in different Regions can't use exports at all. Read about
`cross_region_references` in the
[`Stack` API reference](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk/Stack.html).
What does the CDK deploy to make it work, and why would you hesitate to
use it?_

### Retrospective 25.6

#### Question: Stacks as deployment units

_A team has one stack per AWS service: a "network" stack, a "lambda"
stack, a "dynamodb" stack. Using the best practices guide, explain what
goes wrong as the app grows, and propose a split by lifecycle instead.
Where would the stateful resources go, and what protects them?_

## Lesson 25.7: Adopting and delivering CDK

### Principle 25.7

*Most CDK code is written for accounts that already have things in them.
Bring existing resources under the CDK without replacing them, and
deploy from a pipeline, not from a laptop.*

### Practice 25.7

`cdk import` adopts existing resources into a stack using
CloudFormation resource import (Lab 1.4.4). `cdk migrate` turns a
template, a deployed stack or scanned resources into a new CDK app of
L1 constructs, using the IaC generator for scans. `cdk refactor` renames
and moves resources between stacks without replacing them, using
CloudFormation stack refactoring. `cdk drift` runs drift detection.
Then the app needs a way to deploy that isn't your terminal: a GitHub
Actions workflow, or a CDK Pipeline that updates itself.

Read [Migrate existing resources and AWS CloudFormation templates to
the AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/migrate.html) and
the references for [`cdk
import`](https://docs.aws.amazon.com/cdk/v2/guide/ref-cli-cmd-import.html),
[`cdk
drift`](https://docs.aws.amazon.com/cdk/v2/guide/ref-cli-cmd-drift.html)
and [`cdk
refactor`](https://docs.aws.amazon.com/cdk/v2/guide/ref-cli-cmd-refactor.html).
`cdk migrate` and `cdk refactor` are in preview.

#### Lab 25.7.1: Import a bucket you made by hand

- Create a bucket with the S3 CLI, named with your identifier, with
  versioning on and one tag.

- Run `cdk diff` on `StorageStack` to make sure there are no pending
  changes. Then add an `s3.Bucket` that models what exists exactly:
  name, versioning and the tag. Add nothing else, not even
  `enforce_ssl`: an import can only add the resources being imported,
  and `enforce_ssl` would add a new bucket policy resource.

- Run `cdk import StorageStack` and give it the bucket name when asked.
  Try `--record-resource-mapping` first to see what it will do.

- Run `cdk drift StorageStack`. Change the bucket's tags with the S3 CLI
  and run it again.

- Now add `enforce_ssl=True` and the lifecycle rules you want, and deploy
  normally. The bucket is managed by the CDK from here on.

##### Question: What import doesn't check

_The reference says import doesn't check that your construct's
properties match the real resource. What happens on the next deploy if
they don't? What would you check before importing a bucket that holds
production data?_

#### Lab 25.7.2: Migrate a Lesson 1 template

- Pick a template from module 01, such as the single-bucket template
  from Lesson 1.3. Outside your app, run
  `cdk migrate --from-path <template> --stack-name <you>-lab25-migrated --language python`.

- Read what it generated. Every resource is an L1. Where did your
  parameters and conditions go?

- Synthesize the migrated app and diff its template against the
  original. What changed?

- Replace the L1 bucket with an L2 `s3.Bucket`. Synthesize and compare
  the logical IDs. If this stack were deployed, what would the change do
  to the bucket?

- Deploy the original L1 version, make the L2 change, and run `cdk
  refactor --unstable=refactor --dry-run`. Does it recognize the rename?
  If it doesn't, read why in the refactor docs, and decide whether
  `override_logical_id` on the L1 is the better fix.
  <!-- VERIFY: whether cdk refactor maps an L1-to-L2 swap (same resource
  type, new logical ID, changed properties) or rejects it as a
  modification; the reference says it rejects property changes. -->

##### Question: Migrate or rewrite

_`cdk migrate` gets you a working app in minutes, all L1. When is that
worth it, and when would you rather write the app from scratch with L2
constructs and import the stateful resources?_

#### Lab 25.7.3: Deploy from GitHub Actions (stretch)

Deploy your app from a GitHub Actions workflow, with no long-lived AWS
keys anywhere.

- Read GitHub's [Configuring OpenID Connect in Amazon Web
  Services](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws)
  and IAM's [Create an OpenID Connect (OIDC) identity
  provider](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html).

- Write a small, separate CDK stack (or a CloudFormation template) with
  the OIDC provider for `token.actions.githubusercontent.com` and a role
  that trusts only your repository's `main` branch. Give the role one
  permission: `sts:AssumeRole` on the bootstrap roles
  (`arn:aws:iam::<account>:role/cdk-hnb659fds-*`). Why is that enough to
  deploy, and why is it better than attaching `AdministratorAccess`?
  Look at the bootstrap roles' trust policies in your
  `bootstrap-template.yaml` for any other STS action the CLI needs.

- Write a workflow that, on a push to `main`, sets up Node and Python,
  installs your requirements, runs `pytest`, then `cdk deploy --all
  --require-approval never`, using
  [aws-actions/configure-aws-credentials](https://github.com/aws-actions/configure-aws-credentials)
  with `role-to-assume`. On pull requests, run the tests and `cdk diff`
  only.

- Push a change and watch it deploy.

##### Question: Who can deploy

_Anyone who can merge to `main` can now change your lab account. What
stops a pull request from a fork from deploying? What would you add
before pointing this at a production account?_

#### Lab 25.7.4: CDK Pipelines (stretch)

*This creates a CodePipeline V2 pipeline and CodeBuild projects that
bill per minute. Delete it the same day.*

A [CDK
Pipeline](https://docs.aws.amazon.com/cdk/v2/guide/cdk-pipeline.html) is
a CodePipeline that synthesizes your app, publishes its assets, deploys
its stages and, first, updates itself when you change the pipeline code.

- Read the [CDK Pipelines API
  README](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/README.html).
  Put your stacks in a `Stage` subclass.

- Create a `PipelineStack` with `pipelines.CodePipeline`. Use
  `CodePipelineSource.connection` with a CodeConnections connection to
  your GitHub repository (reuse the one from module 12, or [create
  one](https://docs.aws.amazon.com/dtconsole/latest/userguide/connections-create-github.html);
  the GitHub handshake needs the console). Never use a GitHub token.
  Check that the pipeline type is V2: the
  `@aws-cdk/aws-codepipeline:defaultPipelineTypeToV2` flag decides it, or
  set `pipeline_type` yourself.

- Deploy the pipeline stack once from your terminal. After that, push to
  `main` and watch it update itself and deploy your stage.

- Add a `ShellStep` after the stage that checks something about the
  deployed app, such as uploading a test object and finding the log
  line.

##### Question: GitHub Actions or CDK Pipelines

_Compare Lab 25.7.3 and this lab: where do the credentials live, what
does each cost, how does each deploy to a second account, and what
happens when the pipeline definition itself changes?_

#### Lab 25.7.5: Clean up the module

Remove everything the module created. Work through the list in order;
several steps depend on the one before.

- **Stretch labs:** delete the pipeline stack (and its artifact bucket
  if it was retained), the CodeConnections connection if you made it
  just for this module, and the GitHub OIDC stack. Remove the workflow
  or disable it, so the next push doesn't redeploy what you're deleting.

- **Apps:** `cdk destroy --all` in your app and in the migrated app.
  Delete any stack you deployed another way.

- **Leftovers:** list what's still tagged `topic=25`
  (`aws resourcegroupstaggingapi get-resources --tag-filters
  Key=topic,Values=25`) and look for:
  - buckets left by `RemovalPolicy.RETAIN`, including the imported one
    from Lab 25.7.1. Empty and delete them.
  - Lambda log groups (`aws logs describe-log-groups
    --log-group-name-prefix /aws/lambda/`) that the CDK retained.
  - the Parameter Store parameter from Lab 25.6.3, if a stack didn't own
    it.

  *Tip for next time: `cdk.RemovalPolicies.of(scope).destroy()` sets
  `DESTROY` on everything in a scope, which suits a lab stack and
  nothing else.*

- **Bootstrap stack (decide first).** Other modules may use the CDK
  later, and re-bootstrapping takes a minute, so either keep it or
  remove it; write down which and why. To remove it:
  1. Check nothing else in the account still uses it: no CDK stacks
     left in `aws cloudformation list-stacks` in `us-east-2`.
  2. Delete every image in the `cdk-hnb659fds-container-assets-…`
     repository (`aws ecr list-images`, `batch-delete-image`), or the
     stack deletion will fail on the repository.
  3. Turn off termination protection (`aws cloudformation
     update-termination-protection --no-enable-termination-protection
     --stack-name CDKToolkit`), delete the stack and wait for
     `DELETE_COMPLETE`.
  4. The staging bucket is still there, because of its `Retain` policy.
     It's versioned, so emptying it means deleting every object
     **version and delete marker**, not just the current objects
     (`aws s3api list-object-versions` and `delete-objects`, or a few
     lines of boto3). Then delete the bucket.
  5. Confirm: `aws ssm get-parameter --name
     /cdk-bootstrap/hnb659fds/version` returns `ParameterNotFound`, and
     `aws iam list-roles` shows no `cdk-hnb659fds-` roles.

- **Your repository:** make sure `cdk.out/`, `.venv/` and
  `bootstrap-template.yaml` aren't committed, and that `cdk.context.json`
  contains nothing you wouldn't publish.

##### Question: Half a bootstrap

_What happens if you delete the `CDKToolkit` stack but leave its
bucket, then run `cdk bootstrap` again? What happens if aws-nuke
(module 19) deletes the bucket but a stack still points at it, and you
run `cdk deploy`? How would you recover from each?_

### Retrospective 25.7

#### Question: CloudFormation, CDK or Terraform

_Use the table from Practice 25.1. For each situation, pick one of
CloudFormation YAML, CDK or Terraform and justify it: (a) a small team of
Python developers building serverless apps only on AWS; (b) a platform
team managing AWS, a DNS provider and a SaaS monitoring tool; (c) a
security team publishing account baselines that must be readable by
auditors; (d) the templates behind a Service Catalog product. Where would
you mix them?_

#### Question: Bootstrapping an organization

_In a real organization with dozens of accounts, nobody runs `cdk
bootstrap` by hand. How would you bootstrap every account in the
`Workloads` OU, with a narrower execution policy and a pipeline account
trusted to deploy (`--trust`)? Read the bootstrapping docs' pointer to
StackSets and compare with module 19's Control Tower lab._

## Further Reading

- [Best practices for using the AWS CDK in TypeScript to create IaC
  projects](https://docs.aws.amazon.com/prescriptive-guidance/latest/best-practices-cdk-typescript-iac/introduction.html)
  (AWS Prescriptive Guidance): most of it applies to Python too.
- [Preserve deployed resources when refactoring CDK
  code](https://docs.aws.amazon.com/cdk/v2/guide/refactor.html) and
  [CloudFormation stack
  refactoring](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stack-refactoring.html).
- [Mixins](https://docs.aws.amazon.com/cdk/v2/guide/mixins.html): a
  newer, explicit alternative to aspects for adding features to specific
  constructs.
- [Import an existing AWS CloudFormation
  template](https://docs.aws.amazon.com/cdk/v2/guide/use-cfn-template.html)
  with `cloudformation-include`, to run cdk-nag or your aspects over a
  template you didn't write in CDK.
- The [bootstrap
  template](https://github.com/aws/aws-cdk-cli/blob/main/packages/aws-cdk/lib/api/bootstrap/bootstrap-template.yaml)
  on GitHub, and its version history in the bootstrapping docs.
- [Construct Hub](https://constructs.dev/): third-party and AWS
  construct libraries, with their API docs.
- The [archived CDK for
  Terraform](https://github.com/hashicorp/terraform-cdk) repository and
  its deprecation notice, for context on module 17.
