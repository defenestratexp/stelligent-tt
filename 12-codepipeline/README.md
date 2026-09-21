# Topic 12: CodePipeline

<!-- TOC -->

- [Topic 12: CodePipeline](#topic-12-codepipeline)
  - [What changed in the 2026 edition](#what-changed-in-the-2026-edition)
  - [Exam coverage](#exam-coverage)
  - [Cost and cleanup](#cost-and-cleanup)
  - [Guidance](#guidance)
  - [Lesson 12.1: Introduction to CI/CD in AWS](#lesson-121-introduction-to-cicd-in-aws)
    - [Principle 12.1](#principle-121)
    - [Practice 12.1](#practice-121)
      - [Lab 12.1.1: Connect AWS to GitHub](#lab-1211-connect-aws-to-github)
        - [Question: Connection or Token](#question-connection-or-token)
      - [Lab 12.1.2: A Minimal V2 Pipeline](#lab-1212-a-minimal-v2-pipeline)
        - [Question: The Artifact Bucket](#question-the-artifact-bucket)
      - [Lab 12.1.3: Build and Test Stages with CodeBuild](#lab-1213-build-and-test-stages-with-codebuild)
        - [Question: Lint or Validate](#question-lint-or-validate)
    - [Retrospective 12.1](#retrospective-121)
      - [Question: CloudFormation Template](#question-cloudformation-template)
      - [Question: Pipeline Template](#question-pipeline-template)
      - [Task: Stack Deletion Order](#task-stack-deletion-order)
  - [Lesson 12.2: Pipelines Support Infrastructure as Code](#lesson-122-pipelines-support-infrastructure-as-code)
    - [Principle 12.2](#principle-122)
    - [Practice 12.2](#practice-122)
      - [Lab 12.2.1: The Application Template](#lab-1221-the-application-template)
      - [Lab 12.2.2: Deploy with a Change Set](#lab-1222-deploy-with-a-change-set)
        - [Question: Create or Update](#question-create-or-update)
      - [Lab 12.2.3: Manual Approval](#lab-1223-manual-approval)
        - [Question: What the Approver Sees](#question-what-the-approver-sees)
      - [Lab 12.2.4: Guard Rails in the Template](#lab-1224-guard-rails-in-the-template)
        - [Question: Which Layer Stopped It](#question-which-layer-stopped-it)
      - [Lab 12.2.5: Automate the Review](#lab-1225-automate-the-review)
        - [Question: Why Keep the Human](#question-why-keep-the-human)
    - [Retrospective 12.2](#retrospective-122)
      - [Question: Rename the Table](#question-rename-the-table)
  - [Lesson 12.3: V2 Pipelines](#lesson-123-v2-pipelines)
    - [Principle 12.3](#principle-123)
    - [Practice 12.3](#practice-123)
      - [Lab 12.3.1: Triggers with Branch and File Path Filters](#lab-1231-triggers-with-branch-and-file-path-filters)
        - [Question: Manual Starts](#question-manual-starts)
      - [Lab 12.3.2: Pipeline Variables and Execution Mode](#lab-1232-pipeline-variables-and-execution-mode)
        - [Question: Superseded or Queued](#question-superseded-or-queued)
      - [Lab 12.3.3: Stage Rollback and Conditions](#lab-1233-stage-rollback-and-conditions)
        - [Question: What Rollback Restores](#question-what-rollback-restores)
      - [Lab 12.3.4: Clean Up](#lab-1234-clean-up)
    - [Retrospective 12.3](#retrospective-123)
      - [Question: V1 or V2](#question-v1-or-v2)
  - [Further Reading](#further-reading)

<!-- /TOC -->

## What changed in the 2026 edition

- **GitHub source via an AWS CodeConnections connection, not a personal
  access token.** The 2022 labs had you paste a GitHub token into the
  pipeline (the "GitHub (via OAuth app)" version 1 action). That action is
  legacy, and a long-lived token in a template or parameter is the thing to
  avoid. Pipelines now use the `CodeStarSourceConnection` action with a
  connection to the AWS Connector for GitHub app. Creating the connection
  needs one trip to the console to authorize the app; everything else stays
  in the CLI. New Lab 12.1.1 does the handshake.
- **V2 pipelines.** V2 is the pipeline type to use in 2026, and several
  features only exist there: triggers with branch, tag and file path
  filters, pipeline-level variables, `QUEUED` and `PARALLEL` execution
  modes, stage rollback, stage conditions and the Commands action. The
  labs set `PipelineType: V2` explicitly, and new Lesson 12.3 covers the
  features. V2 is billed per action execution minute, not per pipeline;
  see [Cost and cleanup](#cost-and-cleanup).
- **`main`, not `master`.** Branch filters and `BranchName` use `main`,
  the default for new GitHub repositories.
- **No polling.** "Poll the repository for changes" is gone: the
  connection delivers push events, and V2 triggers decide which ones start
  the pipeline.
- **CodeBuild on a current managed image.** Build and test actions use
  `aws/codebuild/amazonlinux-x86_64-standard:5.0` (Amazon Linux 2023) with
  the Python 3.13 runtime, and lint templates with cfn-lint instead of
  `aws cloudformation validate-template`, which the 2022 Further Reading
  already called unhelpful.
- **The change set labs no longer ask for separate "CREATE" and "UPDATE"
  change sets.** The `CHANGE_SET_REPLACE` action mode creates the right type
  by itself; Lab 12.2.2 asks you to find out which one it made.
- **The stateful-resource lesson is kept and extended.** Lesson 12.2 still
  protects a DynamoDB table with a change set and a manual approval, and
  adds template guard rails (`DeletionPolicy`, `UpdateReplacePolicy`,
  deletion protection, a stack policy) and an automated replacement check
  that runs before a human is asked. The approval action now has a
  configurable timeout.
- **[bucket.yaml](bucket.yaml)** is linked from this repository instead
  of the upstream `master` branch, makes the bucket name optional, tags the
  bucket and outputs its name for the Test stage.
- Labs run in the lab account with the `lab` profile (`us-east-2`), and the
  module ends with a cleanup lab.

## Exam coverage

| Exam | Domain / task statement |
|---|---|
| DVA-C02 → C03 | Domain 3: Deployment (Task 3.3: automate deployment testing; Task 3.4: deploy code by using AWS CI/CD services, including committing code to invoke build, test and deployment actions, updating IaC templates, orchestrated workflows and rollbacks). C03 guide publishes 2026-10-27 and adds GenAI / agent topics |
| DOP-C02 | Domain 1: SDLC Automation (Task 1.1: implement CI/CD pipelines, including CodePipeline, CodeBuild, source integration and approvals; Task 1.2: integrate automated testing into pipelines; Task 1.3: build and manage artifacts; Task 1.4: deployment strategies and rollback) |
| DOP-C02 | Domain 2: Configuration Management and IaC (Task 2.1: define infrastructure as code that provisions and manages systems throughout their lifecycle, including change sets and protecting stateful resources) |

DOP-C02 leans on this module heavily: expect scenario questions about where
a pipeline's credentials live, how to gate a production change, and what a
rollback does and doesn't undo.

## Cost and cleanup

- **CodePipeline V2** is billed at $0.002 per action execution minute,
  rounded up per action, after 100 free minutes a month shared by every V2
  pipeline in the account. Manual approval actions aren't billed, so a
  pipeline waiting days for approval costs nothing while it waits. Source,
  CloudFormation, CodeBuild and Commands actions are billed for the minutes
  they run. A lab pipeline that runs a few times a day stays inside the free
  minutes or costs cents. (V1 pipelines cost $1 per active pipeline per
  month instead; the labs don't use V1.)
- **CodeBuild** bills per build minute, rounded up: $0.005 a minute for
  `general1.small` Linux, with 100 free minutes a month on `general1.small`
  or `arm1.small`. Each build in these labs takes a minute or two. The
  Commands action (Lab 12.2.5) runs on CodeBuild compute and bills the
  same way.
- **The artifact bucket** keeps a zipped copy of the source and every
  action's output for every execution, forever unless you add a lifecycle
  rule. It's a few cents a month, but CloudFormation can't delete a bucket
  that still holds objects: empty it first.
- **DynamoDB** tables in Lesson 12.2 use on-demand capacity: no charge
  while idle beyond storage, which is free at this size.
- **CodeConnections** connections have no charge of their own.
  <!-- VERIFY: no published price for connections was found; confirm they are free. -->
- **Log groups.** CodeBuild writes to `/aws/codebuild/<project>` and the
  Commands action to `/aws/codepipeline/<pipeline>`. They are created
  outside your stacks and never expire.
- **Nothing here has an hourly charge.** The cost risk is a pipeline left
  connected to a busy repository, or retained resources (Lab 12.2.4
  retains a table on purpose).
- [Lab 12.3.4](#lab-1234-clean-up) is the final cleanup: pipelines,
  application stacks, retained tables, artifact buckets, log groups and,
  if nothing else uses it, the connection.

<!-- VERIFY: CodePipeline V2 ($0.002/min, 100 free minutes) and CodeBuild
general1.small ($0.005/min) prices were read from the pricing pages in
September 2026 without a region selected; confirm the us-east-2 figures. -->

## Guidance

- Explore the official docs! See the CodePipeline
  [User Guide](https://docs.aws.amazon.com/codepipeline/latest/userguide/welcome.html),
  its [pipeline structure reference](https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-pipeline-structure.html)
  and [action structure reference](https://docs.aws.amazon.com/codepipeline/latest/userguide/action-reference.html),
  the [CodeBuild User Guide](https://docs.aws.amazon.com/codebuild/latest/userguide/welcome.html),
  the [CLI reference](https://docs.aws.amazon.com/cli/latest/reference/codepipeline/index.html),
  and the CloudFormation
  [AWS::CodePipeline::Pipeline](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-codepipeline-pipeline.html)
  resource.

- All CloudFormation templates are written in YAML. Do NOT copy and paste
  templates from the Internet at large; build them from the
  [template reference](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/introduction.html).

- Use the AWS CLI, not the console, unless a step says otherwise. One step
  in this module genuinely needs the console: authorizing the GitHub
  connection in Lab 12.1.1.

- Avoid using other sites like stackoverflow.com for answers \-- part of
  the skill set you're building is finding answers straight from the
  source, AWS.

- Work in your lab account with the `lab` profile from module 19
  (`export AWS_PROFILE=lab`). The profile sets the lab region, `us-east-2`,
  so no command here needs `--region`. Stack, pipeline and project names
  start with `<you>`, the identifier you use in resource names and tags,
  and resources carry a `topic=12` tag.

- The pipelines deploy from **your copy of this repository on GitHub** (see
  [WORKFLOW.md](../WORKFLOW.md)), on its `main` branch. You'll need to be
  the repository owner to authorize the connection.

- Run cfn-lint on every template before you deploy it.

- *HINT:* Organizing your references to critical parts of the
  documentation will probably be helpful. The action reference pages (one
  per provider) are where most answers in this module live.

## Lesson 12.1: Introduction to CI/CD in AWS

### Principle 12.1

*Pipelines are how Stelligent delivers infrastructure, software, custom
environments and processes, and just about everything else.*

### Practice 12.1

The CI/CD landscape is full of rich and full-featured tools, and no two
organizations seem to use the same tool-set. As a result, there will be
some learning curve on every project, and here we'll introduce the
AWS-native tools. CodePipeline orchestrates: it watches a source, moves
artifacts between stages, and calls other services to do the work.
CloudFormation deploys. CodeBuild runs whatever commands you need in a
managed container, and is how you extend a pipeline with custom, codified
actions.

In 2022 the complaint was that CodePipeline could only take code from
GitHub, CodeCommit and S3. Today a CodeConnections connection reaches
GitHub, GitHub Enterprise Server, GitLab (cloud and self-managed) and
Bitbucket Cloud; S3, ECR and CodeCommit remain available as sources.
What hasn't changed is the main attraction: *the ability and relative ease
with which we can codify and version a pipeline, all without running a CI
server.*

[Continuous delivery with CodePipeline](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline.html)
in the CloudFormation User Guide is the page to start from.

#### Lab 12.1.1: Connect AWS to GitHub

A [connection](https://docs.aws.amazon.com/dtconsole/latest/userguide/welcome-connections.html)
is an AWS resource that stands for an installation of the AWS Connector
app in your GitHub account. The pipeline refers to it by ARN; no token
ever appears in your templates.

- Create the connection with the CLI:
  `aws codeconnections create-connection --provider-type GitHub
  --connection-name <you>-github`. (An `AWS::CodeConnections::Connection`
  resource in its own small stack works too; keep it out of the pipeline
  stack either way, so you can delete and recreate pipelines without
  touching it.)
- Check its status with `aws codeconnections get-connection
  --connection-arn <arn>`. It is `PENDING`: a connection created from the
  CLI, an SDK or CloudFormation can't be used until someone authorizes it.
- **This step needs the console.** Follow
  [Update a pending connection](https://docs.aws.amazon.com/dtconsole/latest/userguide/connections-update.html):
  open the connection in the Developer Tools console, choose **Update
  pending connection**, authorize the AWS Connector for GitHub, and install
  the app on your GitHub account (limit it to your lab repository if you
  like). You only install the app once per GitHub account.
- Check the status again. It should now be `AVAILABLE`.
- Note the ARN's service prefix: new connections use `codeconnections`;
  older ones (and many docs examples) show `codestar-connections`. Both
  work.

##### Question: Connection or Token

_The 2022 version of this lab stored a GitHub personal access token in the
pipeline. Compare that with the connection: where does the credential
live now, who can use it (look up `codeconnections:UseConnection`), what
can it reach in GitHub, and what do you do when someone leaves the team?_

#### Lab 12.1.2: A Minimal V2 Pipeline

Code a CloudFormation template that creates a
[CodePipeline pipeline](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-codepipeline-pipeline.html)
and its minimal set of supporting resources:

- An S3 bucket for the pipeline's artifacts.

- An IAM role that trusts `codepipeline.amazonaws.com`, with the
  permissions the pipeline's actions need. The
  [CodePipeline service role](https://docs.aws.amazon.com/codepipeline/latest/userguide/how-to-custom-role.html)
  page lists them per action. Scope them to your bucket, your connection
  and your stacks, not `*`. For the connection, grant both
  `codeconnections:UseConnection` and `codestar-connections:UseConnection`;
  the [source action reference](https://docs.aws.amazon.com/codepipeline/latest/userguide/action-reference-CodestarConnectionSource.html)
  explains why.

- An IAM role that trusts `cloudformation.amazonaws.com` and can create an
  S3 bucket. The pipeline passes this role to CloudFormation, so the
  pipeline role needs `iam:PassRole` on it and nothing broader.

- The pipeline itself, with `PipelineType: V2`:
  - a **Source** stage with a `CodeStarSourceConnection` action that
    takes the connection ARN, your repository (`<github-user>/<repo>`) and
    the `main` branch as parameters;
  - a **Deploy** stage with a
    [CloudFormation action](https://docs.aws.amazon.com/codepipeline/latest/userguide/action-reference-CloudFormation.html)
    in `CREATE_UPDATE` mode that deploys [bucket.yaml](bucket.yaml) from
    the source artifact (`SourceArtifact::12-codepipeline/bucket.yaml`).

Deploy the pipeline stack with the CLI (`aws cloudformation deploy`, with
`--capabilities CAPABILITY_NAMED_IAM` if you name your roles). Creating the
pipeline starts its first execution. Follow it with
`aws codepipeline get-pipeline-state --name <you>-pipeline` and
`aws codepipeline list-pipeline-executions --pipeline-name <you>-pipeline`.

##### Question: The Artifact Bucket

_List what's in the artifact bucket after the first execution. What is
each object, and why does CodePipeline keep a copy of your source at all
when the code is already in GitHub?_

#### Lab 12.1.3: Build and Test Stages with CodeBuild

Add two stages to your pipeline, each with a single
[CodeBuild action](https://docs.aws.amazon.com/codepipeline/latest/userguide/action-reference-CodeBuild.html):

- A **Build** stage, immediately after Source, that lints the
  application template with [cfn-lint](https://github.com/aws-cloudformation/cfn-lint)
  and fails the pipeline if the template has errors.

- A **Test** stage, immediately after Deploy, that checks the application
  stack is healthy: the stack status is `CREATE_COMPLETE` or
  `UPDATE_COMPLETE`, and the bucket named in the stack's `BucketName`
  output exists (`aws s3api head-bucket`).

Make sure you understand how CodeBuild projects work before you write
them, including the resources you need:

- an IAM role that trusts `codebuild.amazonaws.com` with just enough
  permission for each project: its own log group, the artifact bucket, and
  for the Test project, read-only calls on your stack and bucket. One role
  per project keeps each one small.

- the [`AWS::CodeBuild::Project`](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-codebuild-project.html)
  resources, with `Source` and `Artifacts` of type `CODEPIPELINE`, and a
  current [managed image](https://docs.aws.amazon.com/codebuild/latest/userguide/ec2-compute-images.html):
  `aws/codebuild/amazonlinux-x86_64-standard:5.0`, compute type
  `BUILD_GENERAL1_SMALL`.

- a [buildspec](https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html)
  for each project. Keep them in your repository (for example
  `12-codepipeline/buildspec-lint.yml`) and point each project at its file;
  a buildspec is not a CloudFormation template, and the repository's
  `.cfnlintrc` already skips files named `buildspec*.yml`. Pin the runtime
  in the `install` phase (`runtime-versions` with `python: 3.13`) rather
  than taking the image's default.

The Test action needs to know the stack name. Pass it in as an
environment variable in the action's `EnvironmentVariables` configuration
rather than hard-coding it in the buildspec.

##### Question: Lint or Validate

_The 2022 lab validated the template with `aws cloudformation
validate-template`. Break the template on purpose twice: once with a YAML
syntax error, once with a misspelled property name or an invalid property
value. What does `validate-template` catch, and what does cfn-lint catch?
Which failure would you rather see in the Build stage than in Deploy?_

### Retrospective 12.1

#### Question: CloudFormation Template

_Is executing a CloudFormation template a legitimate example of an
"application"? Provide an explanation._

#### Question: Pipeline Template

_Is your pipeline template portable? Update and re-create your pipeline if
you hard-coded any of the following:_

- the name of the application stack
- the connection ARN, the repository, or the branch to track
- the S3 bucket names (the artifact bucket and the application bucket)
- the path to the template inside the repository
- anything else that would stop a teammate from deploying a second copy
  next to yours

#### Task: Stack Deletion Order

Delete your pipeline stack and leave the bucket stack alone. Once the
pipeline stack is gone, try to delete the bucket stack. What happens? The
bucket stack was created with the CloudFormation role from the pipeline
stack, and CloudFormation uses that same role to delete it. With the role
gone, the deletion fails.

To recover, recreate the pipeline stack (or just the role) and delete the
bucket stack while the role exists. To avoid this in future, keep
long-lived roles in their own stack and pass their ARNs to the others, and
delete stacks in the reverse order you created them. (Empty the artifact
bucket before deleting the pipeline stack, or that deletion fails too.)

## Lesson 12.2: Pipelines Support Infrastructure as Code

### Principle 12.2

*All AWS resources used by an application are part of that application's
infrastructure and should be versioned code, just like the application
itself, and delivered through automation pipelines.*

### Practice 12.2

Well-architected applications take advantage of existing services
wherever possible, to reduce the effort of writing and maintaining the
business logic that makes the application valuable. Although
[infrastructure as code](https://en.wikipedia.org/wiki/Infrastructure_as_code)
was originally coined for virtual servers, in AWS it describes all the
resources an application uses.

Pipelines that once built and deployed applications now deploy the whole
application stack, from networking to storage and monitoring. Some of those
resources hold data, and a pipeline that can create them can also destroy
them. This lesson is about making sure it only does that on purpose.

These labs assume we're building an inventory application that tracks
stock of bicycle parts. We won't write the application, but we will create
the DynamoDB table that holds the inventory, and deploy it with a pipeline
that won't quietly drop it.

#### Lab 12.2.1: The Application Template

Create an application template (for example
`12-codepipeline/inventory.yaml`) with:

- a DynamoDB table, as simple as possible: `ID` as the partition key,
  on-demand capacity (`PAY_PER_REQUEST`), and the table name taken from a
  parameter (you'll change it later on purpose);
- an IAM role for a fictional application that can read and write items in
  that table only. Write a small inline policy scoped to the table's ARN
  rather than attaching a broad AWS managed policy such as
  `AmazonDynamoDBFullAccess`.

Create a stack from this template with the CLI to check it works, put an
item or two in the table (`aws dynamodb put-item`), then delete the stack.

#### Lab 12.2.2: Deploy with a Change Set

Create a second pipeline (its own stack) that deploys the inventory stack
from your repository. Its **Deploy** stage has two
[CloudFormation actions](https://docs.aws.amazon.com/codepipeline/latest/userguide/action-reference-CloudFormation.html):

- **CreateChangeSet** (`ActionMode: CHANGE_SET_REPLACE`): builds a
  [change set](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-changesets.html),
  a dry run that shows *what would happen* if the stack were created or
  updated;
- **ExecuteChangeSet** (`ActionMode: CHANGE_SET_EXECUTE`, a higher
  `RunOrder`): *actually applies* the changes the change set lists.

Reuse your cfn-lint Build stage in front of Deploy if you like. Let the
pipeline run, then commit a harmless change (a tag on the table) to `main`
and let it run again.

##### Question: Create or Update

_The 2022 version of this lab asked for a 'CREATE' change set the first
time and an 'UPDATE' change set afterwards. Look at the change sets your
pipeline made (`aws cloudformation list-change-sets` while one exists, or
the stack's events). What type was each, and who decided? What state was
the stack in between the first CreateChangeSet and ExecuteChangeSet?_

#### Lab 12.2.3: Manual Approval

The previous lab created and then executed a change set, which on its own
achieves nothing that a single `CREATE_UPDATE` action wouldn't. The value
is in the gap between the two actions.

Data is often the most valuable part of an application, and we want to
protect it from accidental deletion[^1]. A template or parameter change
that renames a DynamoDB table makes CloudFormation *replace* it: create a
new, empty table and delete the old one, data included. Put a person in
the gap with a
[manual approval action](https://docs.aws.amazon.com/codepipeline/latest/userguide/approvals.html):

- Add an `Approval` action (`Category: Approval`, `Provider: Manual`)
  between CreateChangeSet and ExecuteChangeSet in the Deploy stage.
- Give the approver context: set `CustomData` to a message that includes
  the commit message and the change set name, using
  [variables](https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-variables.html)
  (give the source action a `Namespace` such as `SourceVariables` and use
  `#{SourceVariables.CommitMessage}`).
- Set `TimeoutInMinutes` on the approval action to something that fits a
  lab session, such as 60. The default is seven days; an approval that
  times out fails the execution.
- Optional: add an SNS topic (`NotificationArn`) with your email address
  subscribed, so the pipeline tells you when it's waiting.

Now use it. When the pipeline stops at the approval:

- Look at the change set: `aws cloudformation describe-change-set
  --stack-name <stack> --change-set-name <name>`. For each change, read
  `Action` and `Replacement`.
- If the change set would replace the table, reject the approval. If not,
  approve it. Do both from the CLI: find the token with
  `aws codepipeline get-pipeline-state`, then use
  `aws codepipeline put-approval-result`.

##### Question: What the Approver Sees

_`Replacement` can be `True`, `False` or `Conditional`. What does
`Conditional` mean, and should an approver treat it as safe? Who in a real
team should be allowed to call `codepipeline:PutApprovalResult` on this
action, and how would you write that policy?_

#### Lab 12.2.4: Guard Rails in the Template

A human reading a change set is one layer. Add layers that still work when
the human is tired. Add each to the inventory template, commit, and let
the pipeline deploy it (approving each harmless change):

- [`DeletionPolicy: Retain` and `UpdateReplacePolicy: Retain`](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-attribute-deletionpolicy.html)
  on the table, so CloudFormation keeps the old table when it deletes or
  replaces the resource.
- `DeletionProtectionEnabled: true` on the table, so DynamoDB itself
  refuses to delete it, whoever asks.
- A [stack policy](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/protect-stack-resources.html)
  that allows all updates except `Update:Replace` and `Update:Delete` on
  the table. A
  [template configuration file](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/continuous-delivery-codepipeline-cfn-artifacts.html)
  in your repository, named by the CreateChangeSet action's
  `TemplateConfiguration` setting, can carry parameters, tags and a stack
  policy. Move the table name parameter into one and add the policy. After
  the next run, check with `aws cloudformation get-stack-policy` whether
  the policy reached the stack; change sets are created with a different
  API call from stack updates. If it didn't, set it once with
  `aws cloudformation set-stack-policy` and note why in your answer.

<!-- VERIFY: whether the CloudFormation action applies the StackPolicy from
a template configuration file in CHANGE_SET_REPLACE mode (CreateChangeSet
has no stack policy parameter). The lab is written so either result works. -->

Then attack it: put a few items in the table, change the table name in the
template configuration file, commit, and **approve** the change set this
time. Watch the stack events.

##### Question: Which Layer Stopped It

_Which layer stopped the replacement, and at what point: creating the
change set, executing it, or cleaning up afterwards? Remove the stack
policy and try again: what happens now, and where are your items
afterwards? Which of these layers would still protect the table from
someone running `aws cloudformation delete-stack` by hand?_

#### Lab 12.2.5: Automate the Review

The replacement check you did by hand is mechanical, so let the pipeline
do it before it asks anyone. Add an action between CreateChangeSet and the
approval that fails if the change set replaces anything:

- Use the V2
  [Commands action](https://docs.aws.amazon.com/codepipeline/latest/userguide/action-reference-Commands.html)
  (`Category: Compute`, `Provider: Commands`), which runs shell commands on
  CodeBuild compute without a CodeBuild project. It runs as the pipeline's
  service role, so that role needs `cloudformation:DescribeChangeSet` on
  the stack and permission to write to the `/aws/codepipeline/<pipeline>`
  log group.
- One command is enough:
  `aws cloudformation describe-change-set` with a `--query` that counts
  changes whose `ResourceChange.Replacement` is `True`, followed by a test
  that exits non-zero if the count isn't 0. Commands must be single lines.
- Commit a rename again and watch the pipeline stop before the approval.

<!-- VERIFY: confirm the Commands action's default Linux image includes AWS
CLI v2 (the docs describe the environment type and compute type but not the
image contents). If it doesn't, use a CodeBuild action with the Lesson 12.1
image instead. -->

##### Question: Why Keep the Human

_If the automated check blocks every replacement, why keep the manual
approval? Name a change set with no replacements that you'd still want a
person to look at. Conversely, what would you need before you removed the
approval from this pipeline?_

### Retrospective 12.2

#### Question: Rename the Table

_Suppose the business really does need the table renamed. With every guard
rail from this lesson in place, write down how you'd do it without losing
data, and which steps go through the pipeline and which don't. (Look at
[resource import](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/import-resources.html)
and DynamoDB's own backup and export options.)_

## Lesson 12.3: V2 Pipelines

### Principle 12.3

*A pipeline should run only when there's something for it to do, take its
inputs explicitly, and know how to back out.*

### Practice 12.3

Your pipelines deploy from a repository that holds every module of this
course, so right now answering a question in module 13 redeploys your
DynamoDB table. V2 pipelines fix that with triggers. They also take
variables at start time, control how overlapping executions behave, and
can roll a stage back or refuse to enter it. These labs add each to the
inventory pipeline from Lesson 12.2. The
[pipeline types page](https://docs.aws.amazon.com/codepipeline/latest/userguide/pipeline-types-planning.html)
lists what only V2 can do.

#### Lab 12.3.1: Triggers with Branch and File Path Filters

- Add a `Triggers` entry to the inventory pipeline with a push
  [filter](https://docs.aws.amazon.com/codepipeline/latest/userguide/pipelines-filter.html):
  branch `main`, and file paths that include your inventory template and
  its configuration file and exclude Markdown files.
- Commit an answer to a question in this README. The pipeline shouldn't
  start. Commit a change to the inventory template. It should.
- Stretch: build a small second pipeline that only runs the cfn-lint
  Build stage, with a pull request trigger for pull requests into `main`
  that touch the same files. Open a pull request and watch it run. (A pull
  request execution uses the commit from the *source* branch, so it must
  never deploy.)

##### Question: Manual Starts

_Once a trigger is configured, the source action's `BranchName` no longer
decides which pushes start the pipeline. What is it still used for? What
happens to the default change detection on the source action when you add
a trigger?_

#### Lab 12.3.2: Pipeline Variables and Execution Mode

- Add a pipeline-level [variable](https://docs.aws.amazon.com/codepipeline/latest/userguide/tutorials-pipeline-variables.html)
  named `TableClass` with a default of `STANDARD`, and a matching
  `TableClass` parameter on the table. Pass it from the CreateChangeSet
  action's `ParameterOverrides` with `#{variables.TableClass}`.
- Start an execution with a different value:
  `aws codepipeline start-pipeline-execution --name <you>-inventory
  --variables name=TableClass,value=STANDARD_INFREQUENT_ACCESS`.
  Does the change set replace the table?
- Set `ExecutionMode: QUEUED` on the pipeline. Commit two changes in quick
  succession while an execution waits at the approval, and watch what
  happens to the second one. Then try the same with the default,
  `SUPERSEDED`.

##### Question: Superseded or Queued

_Which execution mode suits a pipeline that changes stateful resources
behind a manual approval, and why? What could go wrong with `SUPERSEDED`
if an approver is reading one change set while a newer commit arrives?
When would `PARALLEL` make sense, and why not here?_

#### Lab 12.3.3: Stage Rollback and Conditions

- Go back to the bucket pipeline from Lesson 12.1. Move the health check
  into the Deploy stage as a second action (higher `RunOrder`), and add
  `OnFailure: Result: ROLLBACK` to that stage. See
  [Configuring stage rollback](https://docs.aws.amazon.com/codepipeline/latest/userguide/stage-rollback.html).
- Commit a change that deploys but fails the check (for example, have the
  template output a name that doesn't exist, or break the check). Watch
  CodePipeline start a rollback execution of the stage using the last
  successful execution's artifacts. Try a manual rollback too, with
  `aws codepipeline rollback-stage`.
- Add a
  [stage condition](https://docs.aws.amazon.com/codepipeline/latest/userguide/stage-conditions.html)
  to the inventory pipeline's Deploy stage: a `BeforeEntry` condition
  with `Result: FAIL` and a
  [`DeploymentWindow` rule](https://docs.aws.amazon.com/codepipeline/latest/userguide/rule-reference-DeploymentWindow.html)
  whose cron expression allows only the hours you choose. Start the
  pipeline outside the window and record what the stage does, then
  override the condition.

##### Question: What Rollback Restores

_Stage rollback re-runs the stage with an earlier execution's source
revision, artifacts and variables. Imagine the inventory pipeline without
Lesson 12.2's guard rails, with `OnFailure: ROLLBACK` on Deploy, and a
commit that renamed the table. What does the rollback give you back:
the old table, its data, or neither? What does that tell you about where
rollback belongs in a pipeline that manages stateful resources?_

#### Lab 12.3.4: Clean Up

Remove everything the module created, in this order:

- **Stop new executions.** So that a push can't redeploy what you're
  deleting, block each pipeline's Deploy stage:
  `aws codepipeline disable-stage-transition --pipeline-name <pipeline>
  --stage-name Deploy --transition-type Inbound --reason cleanup`.
- **Application stacks.** Delete the bucket stack and the inventory
  stack *while the pipeline stacks still exist*: CloudFormation deletes
  them with the CloudFormation roles those stacks own (see the
  [deletion order task](#task-stack-deletion-order)). The stack policy
  doesn't block a stack deletion; deletion protection and `Retain` do
  their jobs, so the inventory stack's deletion leaves the table behind.
- **Pipeline stacks.** Empty each artifact bucket first
  (`aws s3 rm s3://<bucket> --recursive`; if you turned on versioning,
  delete every object version too), then delete the stack.
- **Retained tables.** `Retain` did its job: the inventory tables are
  still there. Turn off deletion protection
  (`aws dynamodb update-table --no-deletion-protection-enabled`), then
  delete them.
- **Log groups.** Delete `/aws/codebuild/<project>` for each project and
  `/aws/codepipeline/<pipeline>` for the Commands action
  (`aws logs describe-log-groups --log-group-name-prefix /aws/code`).
- **SNS topic** from Lab 12.2.3, if you made one.
- **Connection.** Keep it if you'll do module 25's CDK Pipelines stretch
  lab, which reuses it. Otherwise
  `aws codeconnections delete-connection --connection-arn <arn>`, and
  uninstall the AWS Connector app from your GitHub account's
  application settings if nothing else uses it.
- **Check:** `aws resourcegroupstaggingapi get-resources --tag-filters
  Key=topic,Values=12` should return nothing you still want gone.

### Retrospective 12.3

#### Question: V1 or V2

_Estimate what your inventory pipeline cost this month as a V2 pipeline
(count the action minutes in `aws codepipeline list-action-executions`,
remembering that approvals aren't billed) and what it would have cost as
V1. At what point would V1 be cheaper, and which of this lesson's features
would you give up for it?_

## Further Reading

- [CDK Pipelines](https://docs.aws.amazon.com/cdk/v2/guide/cdk-pipeline.html)
  builds a self-updating CodePipeline from CDK code; module 25's stretch
  lab uses the connection you made here.
- [`sam pipeline`](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-generating-example-ci-cd.html)
  generates a CodePipeline for a SAM application (module 16).
- [cfn-guard](https://docs.aws.amazon.com/cfn-guard/latest/ug/what-is-guard.html)
  checks templates against your own policy rules, the kind of test that
  belongs in the Build stage next to cfn-lint. [cfn_nag](https://github.com/stelligent/cfn_nag),
  mentioned in the 2022 edition, does a similar job with built-in rules.
- [Drift-aware change sets](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/drift-aware-change-sets.html)
  (November 2025) compare the new template, the last deployed template and
  the live resources, so a change set shows when a deployment would undo a
  change someone made outside CloudFormation.
- [Tutorial: use full clone with a GitHub pipeline source](https://docs.aws.amazon.com/codepipeline/latest/userguide/tutorials-github-gitclone.html)
  shows the `CODEBUILD_CLONE_REF` output format, for builds that need Git
  history.
- [Source revision overrides](https://docs.aws.amazon.com/codepipeline/latest/userguide/pipelines-trigger-source-overrides.html)
  start a V2 pipeline on a specific commit, which is another way to
  redeploy a known-good version.
- AWS CodeCommit returned to general availability in November 2025, so an
  AWS-hosted Git repository is again an option for a pipeline source. See
  the [CodeCommit User Guide](https://docs.aws.amazon.com/codecommit/latest/userguide/welcome.html).

[^1]: For the record, there are other ways of protecting AWS resources
    from being accidentally deleted, generally involving being very
    selective with access permissions. This exercise demonstrates
    mechanisms that apply more generally.
