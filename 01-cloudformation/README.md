# Topic 1: CloudFormation

<!-- TOC -->

- [Topic 1: CloudFormation](#topic-1-cloudformation)
  - [What changed in the 2026 edition](#what-changed-in-the-2026-edition)
  - [Exam coverage](#exam-coverage)
  - [Cost and cleanup](#cost-and-cleanup)
  - [Guidance](#guidance)
  - [Lesson 1.1: Introduction to CloudFormation](#lesson-11-introduction-to-cloudformation)
    - [Principle 1.1](#principle-11)
    - [Practice 1.1](#practice-11)
      - [Lab 1.1.1: CloudFormation Template Requirements](#lab-111-cloudformation-template-requirements)
      - [Lab 1.1.2: Stack Parameters](#lab-112-stack-parameters)
      - [Lab 1.1.3: Pseudo-Parameters](#lab-113-pseudo-parameters)
      - [Lab 1.1.4: Using Conditions](#lab-114-using-conditions)
      - [Lab 1.1.5: Termination Protection; Clean up](#lab-115-termination-protection-clean-up)
    - [Retrospective 1.1](#retrospective-11)
      - [Question: Why YAML](#question-why-yaml)
      - [Question: Protecting Resources](#question-protecting-resources)
      - [Task: String Substitution](#task-string-substitution)
  - [Lesson 1.2: Integration with Other AWS Resources](#lesson-12-integration-with-other-aws-resources)
    - [Principle 1.2](#principle-12)
    - [Practice 1.2](#practice-12)
      - [Lab 1.2.1: Cross-Referencing Resources within a Template](#lab-121-cross-referencing-resources-within-a-template)
      - [Lab 1.2.2: Exposing Resource Details via Exports](#lab-122-exposing-resource-details-via-exports)
      - [Lab 1.2.3: Importing another Stack's Exports](#lab-123-importing-another-stacks-exports)
      - [Lab 1.2.4: Import/Export Dependencies](#lab-124-importexport-dependencies)
    - [Retrospective 1.2](#retrospective-12)
      - [Task: Policy Tester](#task-policy-tester)
      - [Task: SSM Parameter Store](#task-ssm-parameter-store)
  - [Lesson 1.3: Portability & Staying DRY](#lesson-13-portability--staying-dry)
    - [Principle 1.3](#principle-13)
    - [Practice 1.3](#practice-13)
      - [Lab 1.3.1: Scripts and Configuration](#lab-131-scripts-and-configuration)
      - [Lab 1.3.2: Coding with AWS SDKs](#lab-132-coding-with-aws-sdks)
      - [Lab 1.3.3: Enhancing the Code](#lab-133-enhancing-the-code)
    - [Retrospective 1.3](#retrospective-13)
      - [Question: Portability](#question-portability)
      - [Task: DRYer Code](#task-dryer-code)
  - [Lesson 1.4: Changing Stacks Safely](#lesson-14-changing-stacks-safely)
    - [Principle 1.4](#principle-14)
    - [Practice 1.4](#practice-14)
      - [Lab 1.4.1: Lint Before You Deploy](#lab-141-lint-before-you-deploy)
      - [Lab 1.4.2: Change Sets and deploy](#lab-142-change-sets-and-deploy)
      - [Lab 1.4.3: Drift Detection](#lab-143-drift-detection)
      - [Lab 1.4.4: IaC Generator](#lab-144-iac-generator)
      - [Lab 1.4.5: Clean up](#lab-145-clean-up)
    - [Retrospective 1.4](#retrospective-14)
      - [Question: Preview, Detect, Reconcile](#question-preview-detect-reconcile)
  - [Further Reading](#further-reading)

<!-- /TOC -->

## What changed in the 2026 edition

- Labs run in a dedicated lab account in `us-east-2`, set once in your AWS
  profile. Commands don't pass `--region` except in the labs that are about
  regions (1.1.4 and Lesson 1.3).
- Lesson 1.2 builds an IAM *role* instead of an IAM user. With IAM Identity
  Center providing short-lived credentials, a user with access keys is the
  thing to avoid. The Exports/`ImportValue` dependency lesson is unchanged.
- Lesson 1.3 no longer asks for "the 4 American regions" plus "another US
  region" (there are only four commercial US regions). The region list lives
  in a config file; you start with two or more regions and extend the list
  without touching code.
- New Lesson 1.4 covers the day-two tools: cfn-lint (and optionally
  cfn-guard), change sets, `aws cloudformation deploy`, drift detection and
  the IaC generator.
- cfn-lint is part of the workflow from the first lab.
- The Parameter Store task uses the CLI instead of the console.
- Links updated for the split of the CloudFormation docs into a User Guide
  and a Template Reference; the third-party YAML primer was replaced with
  the YAML 1.2.2 specification.

## Exam coverage

| Exam | Domain / task statement |
|---|---|
| SOA-C03 | Domain 3: Deployment, Provisioning, and Automation |
| DOP-C02 | Domain 1: SDLC Automation |
| DOP-C02 | Domain 2: Configuration Management and IaC |
| DVA-C02 | Domain 3: Deployment (C03 adds GenAI / agent topics) |

## Cost and cleanup

- CloudFormation itself costs nothing for `AWS::*` resource types, and
  nothing this module creates has an hourly charge: empty S3 buckets, IAM
  roles and policies, and a standard-tier Parameter Store parameter are
  free. Leaving it all running costs effectively $0, but leftover stacks
  and exports clutter the lab account and block reruns that reuse the
  same names.
- Resource scans and generated templates from the IaC generator are
  not billed. <!-- VERIFY: no charge for IaC generator scans. -->
- Every lesson deletes its own stacks. [Lab 1.4.5](#lab-145-clean-up)
  is the final sweep: it deletes the remaining stacks in every region in
  your config file, the Parameter Store parameter, the generated template
  and the bucket created outside CloudFormation.

## Guidance

- All CloudFormation templates should be
  [written in YAML](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-formats.html).
  Chapter 2 of the
  [YAML 1.2.2 specification](https://yaml.org/spec/1.2.2/#chapter-2-language-overview)
  is a short, authoritative tour of the syntax.

- Do NOT copy and paste CloudFormation templates from the Internet at large

- DO use the CloudFormation
  [User Guide](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html)
  and
  [Template Reference](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/introduction.html)
  (resource types, attributes and intrinsic functions now live in the
  Template Reference)

- DO utilize every link in this document; note how the AWS documentation is
  laid out

- DO use the
  [AWS CLI for CloudFormation](https://docs.aws.amazon.com/cli/latest/reference/cloudformation/index.html)
  (NOT the Console) unless otherwise specified.

- Your AWS profile sets the lab region, `us-east-2`. Don't hard-code a
  region, account ID or ARN in a template: use parameters and
  pseudo-parameters.

- Install [cfn-lint](https://github.com/aws-cloudformation/cfn-lint)
  (`pip install cfn-lint`, or the editor plugin listed in
  [WORKFLOW.md](../WORKFLOW.md)) and lint every template before you deploy
  it.

- Include your identifier in stack names, resource names and tags.

## Lesson 1.1: Introduction to CloudFormation

### Principle 1.1

AWS CloudFormation (CFN) is the preferred way we create AWS resources at
Stelligent

### Practice 1.1

A CFN Template is essentially a set of instructions for creating AWS
resources, which includes practically everything that can be created in
AWS. At its simplest, the service accepts a Template (a YAML-based
blueprint describing the resources you want to create or update) and
creates a Stack (a set of resources created using a single template).
The resulting Stacks represent groups of resources whose life-cycles are
inherently linked.

Read through
[Template Anatomy](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-anatomy.html)
and get familiar with the basic parts of a CloudFormation template.

#### Lab 1.1.1: CloudFormation Template Requirements

Create the *most minimal CFN template possible* that can be used to
create an AWS Simple Storage Service (S3) Bucket.

- Always write your CloudFormation
  [templates in YAML](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-formats.html).

- Run `cfn-lint` against the template before you create anything. Get
  into the habit now; Lab 1.4.1 looks at what it catches.

- Launch a Stack by
  [using the AWS CLI tool](https://docs.aws.amazon.com/cli/latest/reference/cloudformation/create-stack.html)
  to run the template. Let your profile supply the lab region (`us-east-2`);
  don't pass `--region`.

- Note the output provided by creating the Stack.

- Though *functionally* unnecessary, the Description (i.e. its *purpose*)
  element documents your code's *intent*, so provide one. The Description
  key-value pair should be at the _root level_ of your template. If you place
  it under the definition of a resource, AWS will allow the template's creation
  but your description will not populate anything. See
  [here](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-anatomy.html)
  for a useful guide to the anatomy of a template as well as
  [YAML terminology](https://yaml.org/spec/1.2.2/#chapter-2-language-overview).

- Commit the template to your GitHub repository under the 01-cloudformation
  folder.

#### Lab 1.1.2: Stack Parameters

Update the same template by adding a CloudFormation
[Parameter](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html)
to the stack and use the parameter's value as the name of the S3 bucket.

- Put your parameter into a separate JSON file and pass that file to the CLI.

- Update your stack.

- Add the template changes and new parameter file to your GitHub repo.

#### Lab 1.1.3: Pseudo-Parameters

Update the same template by prefixing the name of the bucket with the
Account ID in which it is being created, no matter which account you're
running the template from (i.e., using
[pseudo-parameters](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/pseudo-parameter-reference.html)).

- Use built-in CFN
  [string functions](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/intrinsic-function-reference.html)
  to combine the two strings for the Bucket name.

- Do not hard code the Account ID. Do not use an additional parameter to
  provide the Account ID value.

- Update the stack.

- Commit the changes to your GitHub repo.

#### Lab 1.1.4: Using Conditions

Update the same template one final time. This time, use a CloudFormation
[Condition](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/conditions-section-structure.html)
to add a prefix to the name of the bucket. When the current execution
region is your lab region (`us-east-2`), prefix the bucket name with the
Account ID. When executing in all other regions, use the region
name.

- Don't hard-code `us-east-2` in the condition: take the "home" region as
  a parameter with a default, and compare it with the region the stack is
  running in.

- Update the stack that you originally deployed.

- Create a new stack _with the same stack name_, but this time
  deploying to some region other than your lab region. This lab is about
  regions, so pass `--region` explicitly. Pick a region that is enabled
  in your account (see Lesson 1.3).

- Commit the changes to your GitHub repo.

#### Lab 1.1.5: Termination Protection; Clean up

- Before deleting this lesson's Stacks, apply
  [Termination Protection](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-protect-stacks.html)
  to one of them.

- Try to delete the Stack using the AWS CLI. What happens?

- Remove termination protection and try again.

- List your S3 buckets once this lesson's Stacks have been deleted to
  ensure that the buckets in both regions are gone.

### Retrospective 1.1

#### Question: Why YAML

_Why do we prefer the YAML format for CFN templates?_

#### Question: Protecting Resources

_What else can you do to prevent resources in a stack from being deleted?_

See the
[DeletionPolicy](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-attribute-deletionpolicy.html)
and
[UpdateReplacePolicy](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-attribute-updatereplacepolicy.html)
attributes.

_How is that different from applying Termination Protection?_

#### Task: String Substitution

Demonstrate 2 ways to code string combination/substitution using
built-in CFN functions.

## Lesson 1.2: Integration with Other AWS Resources

### Principle 1.2

CloudFormation integrates well with the rest of the AWS ecosystem

### Practice 1.2

A CFN template's resources can reference: each other's attributes,
resource attributes exported from other Stacks in the same region, and
Systems Manager Parameter Store values in the same region. This provides
a way to have resources build on each other to create your AWS
ecosystem.

The labs use IAM because IAM resources are free and make dependencies
easy to see. IAM is a global service: role and policy names must be unique
across the whole account, not per region, while stack exports are
regional. Keep that in mind when you name things.

#### Lab 1.2.1: Cross-Referencing Resources within a Template

Create a CFN template that describes two resources: an
[IAM Role](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-iam-role.html),
and an
[IAM Managed Policy](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-iam-managedpolicy.html)
that controls what that role can do.

- The policy should allow access solely to 'Read' actions against all
  S3 Buckets (including listing buckets and downloading individual bucket
  contents)

- The role's trust policy should allow principals in your own account to
  assume it. Build the account principal from pseudo-parameters; don't
  hard-code the account ID.

- Attach the policy to the role via the template.

- Use a CFN Parameter to set the role's name. Find out which
  [capability](https://docs.aws.amazon.com/cli/latest/reference/cloudformation/create-stack.html)
  you must acknowledge when a template names IAM resources.

- Create the Stack.

- Optional: assume the role from your Identity Center session with
  `aws sts assume-role`, then try listing and writing to a bucket with the
  temporary credentials. Why is this safer than the IAM user with access
  keys that earlier editions of this lab created?

#### Lab 1.2.2: Exposing Resource Details via Exports

Update the template by adding a CFN
[Output](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/outputs-section-structure.html)
that exports the Managed Policy's Amazon Resource Name
([ARN](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html)).

- Update the Stack.

- [List all the Stack Exports](https://docs.aws.amazon.com/cli/latest/reference/cloudformation/list-exports.html)
  in that Stack's region.

#### Lab 1.2.3: Importing another Stack's Exports

Create a *new* CFN template that describes a second IAM Role and applies
to it the Managed Policy ARN created by and exported from the previous
Stack, using
[Fn::ImportValue](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/intrinsic-function-reference-importvalue.html).

- Create this new Stack.

- [List all the Stack Imports](https://docs.aws.amazon.com/cli/latest/reference/cloudformation/list-imports.html)
  in that stack's region.

#### Lab 1.2.4: Import/Export Dependencies

Delete your CFN stacks in the same order you created them in. Did you
succeed? If not, describe how you would _identify_ the problem, and
resolve it yourself.

### Retrospective 1.2

#### Task: Policy Tester

Show how to use the
[IAM policy simulator](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_testing-policies.html)
to demonstrate that the role cannot perform 'Put' actions on any S3
buckets. Use the CLI
([simulate-principal-policy](https://docs.aws.amazon.com/cli/latest/reference/iam/simulate-principal-policy.html))
rather than the console simulator.

#### Task: SSM Parameter Store

Using the CLI
([put-parameter](https://docs.aws.amazon.com/cli/latest/reference/ssm/put-parameter.html)),
create a Systems Manager Parameter Store parameter in the same region as
the first Stack, and provide a value for that parameter. Modify the first
Stack's template so that it uses this Parameter Store parameter value as
the IAM Role's name (look at the SSM parameter types in
[Parameters](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html)).
Recreate or update the first stack.

_If you now change the parameter's value in Parameter Store, what happens
to the stack, and when?_

Finally, tear the stack down. Keep the Parameter Store parameter until
Lab 1.4.5 or delete it now.

## Lesson 1.3: Portability & Staying DRY

### Principle 1.3

_CloudFormation templates should be portable, supporting
[Don't Repeat Yourself](http://wiki.c2.com/?DontRepeatYourself) (DRY)
practices._

### Practice 1.3

Portability refers to the ability of code (whether it's a script or an
entire application) to work in multiple execution environments. This is
achieved most often by removing hard coded configuration elements and
providing an environment-specific configuration file. For CFN templates,
portability is best provided by parameterizing the template (refer to
[AWS CloudFormation Best Practices](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/best-practices.html)
for a more thorough list of recommendations for improving your use of
CloudFormation). Some lab exercises have already demonstrated
portability (_can you point out where?_) and this lesson will focus
on it specifically.

This is the one lesson that deliberately works outside the lab region.
Use regions that are enabled in your lab account:
[`aws account list-regions`](https://docs.aws.amazon.com/cli/latest/reference/account/list-regions.html)
with `--region-opt-status-contains ENABLED ENABLED_BY_DEFAULT` lists them.
Newer regions are
[opt-in](https://docs.aws.amazon.com/accounts/latest/reference/manage-acct-regions.html)
and must be enabled first, and an SCP on your lab account (module 19) may
deny some regions outright. Empty buckets and stacks cost nothing, in any
region.

#### Lab 1.3.1: Scripts and Configuration

Create a single script that re-uses one CloudFormation template to
deploy _a single S3 bucket_.

- Use shell scripting (bash or PowerShell) to create a Stack in each
  region listed in a configuration file, using a looping construct to run
  the template the proper number of times. Start with at least two
  regions: your lab region plus any other enabled region (for example
  `us-west-1` or `ca-central-1`).

- Use an external JSON or YAML configuration file to maintain the target
  deployment region parameters. Consider using `jq` or `yq` to parse this
  file.

- Each bucket name should be of the format
  "_current-Region_-_current-Account_-_friendly-name_"
  where the "_friendly-name_" value is parameterized in the CFN template
  but has a default value.

#### Lab 1.3.2: Coding with AWS SDKs

Repeat the exercise in the previous lab, with two modifications:

- Use only a programming language
  ([Python](https://docs.aws.amazon.com/boto3/latest/guide/quickstart.html),
  [Ruby](https://docs.aws.amazon.com/sdk-for-ruby/v3/developer-guide/welcome.html)
  or
  [JavaScript (Node.js, SDK v3)](https://docs.aws.amazon.com/sdk-for-javascript/v3/developer-guide/welcome.html))
  and the corresponding SDK to repeat exactly what was done in that lab.

- Add one more region to your configuration file, one that the shell
  script never touched. The code must pick it up with no code change:
  that is the point of keeping the region list in configuration.

Also adhere to these criteria:

- The code must support updating existing stacks and creating new
  ones. This can be tricky as some SDKs require that you use a
  'try/catch' construct to determine the existence of a stack.
  (Using rescue-oriented structures for decision logic is generally
  considered a programming anti-pattern.)

- Running the code a second time with no changes must succeed. What does
  the service return when an update has nothing to change, and how does
  your code handle it?

- Use only a single shell command to execute your code script.

#### Lab 1.3.3: Enhancing the Code

Add code that provides for the deletion of your CFN stacks using the
same configuration list, and then delete the stacks using that new
functionality. Query S3 to ensure that the buckets have been deleted.

- Commit your changes to your latest branch.

### Retrospective 1.3

#### Question: Portability

_Can you list 4 features of CloudFormation that help make a CFN template
portable code?_

#### Task: DRYer Code

How reusable is your SDK-orchestration code? Did you share a single
method to load the configuration file for both stack creation/updating
(Lab 1.3.2) and deletion (Lab 1.3.3)? Did you separate the methods for
finding existing stacks from the methods that create or update those stacks?

If not, refactor your Python, Ruby or JavaScript code to work in the
manner described.

## Lesson 1.4: Changing Stacks Safely

### Principle 1.4

_Never change a stack blind: lint the template, preview the change, and
check afterwards that reality still matches the code._

### Practice 1.4

Creating a stack is the easy part. The risk is in the updates: a renamed
property that silently replaces a bucket, a hand-made change in the
console that the next deployment overwrites, or a resource someone built
by hand that you now have to bring under control. These labs work in the
lab region only, reusing the single-bucket template from Lesson 1.3.

#### Lab 1.4.1: Lint Before You Deploy

- Run [cfn-lint](https://github.com/aws-cloudformation/cfn-lint) against
  every template you have written in this module. Fix or explain each
  finding.

- Introduce two mistakes into a copy of the Lesson 1.3 template: a
  misspelled resource property, and a `!Ref` to a parameter that doesn't
  exist. Compare what cfn-lint reports with what
  [`aws cloudformation validate-template`](https://docs.aws.amazon.com/cli/latest/reference/cloudformation/validate-template.html)
  reports.

- Optional:
  [CloudFormation Guard](https://docs.aws.amazon.com/cfn-guard/latest/ug/what-is-guard.html)
  checks templates against *your* rules rather than against the resource
  specification. Write a rule that every S3 bucket must carry a tag with
  your identifier, and run it against your template.

##### Question: What the Linter Knows

_Which of your two mistakes did `validate-template` miss, and why? Where
in your workflow would you run cfn-lint so that nobody has to remember
to?_

#### Lab 1.4.2: Change Sets and deploy

- Add a tag with your identifier to the bucket in the Lesson 1.3 template
  (you'll need it in the next lab). Deploy it to the lab region with
  [`aws cloudformation deploy`](https://docs.aws.amazon.com/cli/latest/reference/cloudformation/deploy.html).
  Run the same command a second time without changes. What happens?

- Now change the tag's value, and preview the update with a
  [change set](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-changesets.html):
  `create-change-set`, then `describe-change-set`. Note the `Action` and
  `Replacement` values.

- Create a second change set that changes the _friendly-name_ parameter
  instead, and describe it. What would happen to the bucket, and to any
  objects in it, if you executed it?

- Execute the tag change set with `execute-change-set` and wait for the
  update to complete. What happened to the other change set?

- Can `deploy` read the JSON parameter file from Lab 1.1.2? What does
  `--no-execute-changeset` do?

##### Question: Create or Update

_In Lab 1.3.2 you wrote code to decide between create and update. How
does `aws cloudformation deploy` make that decision? When would you still
call `create-stack`, `update-stack` or the change set APIs directly?_

#### Lab 1.4.3: Drift Detection

- Change the bucket's tag *outside* CloudFormation, with the S3 CLI.
  `put-bucket-tagging` replaces the bucket's whole tag set, so read the
  current tags first and look at what happens to the
  `aws:cloudformation:*` tags. <!-- VERIFY: behaviour of
  put-bucket-tagging on CloudFormation's aws: system tags; switch the
  drift target to another explicitly set property if it errors. -->

- Run
  [drift detection](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-stack-drift.html)
  on the stack (`detect-stack-drift`, then
  `describe-stack-drift-detection-status` and
  `describe-stack-resource-drifts`). Find your tag change in the output.

- Now turn on bucket versioning outside CloudFormation, without adding it
  to the template, and detect drift again. Is it reported? The drift
  detection page explains why.

- Bring the stack back in line. Decide, for each change, whether the fix
  belongs in the template or in the bucket.

##### Question: Detection Isn't Correction

_What does drift detection change in your account? What happens to the
out-of-band tag change the next time you deploy the stack?_

#### Lab 1.4.4: IaC Generator

The
[IaC generator](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/generate-IaC.html)
scans resources that already exist and writes a template for them: the
usual first step in bringing hand-built infrastructure under
CloudFormation.

- Create an S3 bucket with the S3 CLI (not CloudFormation), with your
  identifier in its name.

- Start a *partial* resource scan limited to S3 buckets
  (`start-resource-scan --scan-filters`), then create a generated
  template containing only your bucket (`create-generated-template`) and
  download it (`get-generated-template`). Scans are rate-limited per day,
  so don't run a full-account scan for this.

- Lint the generated template and compare it with the one you wrote.
  What `DeletionPolicy` and `UpdateReplacePolicy` did it get, and why
  does that matter?

- Optional: bring the bucket into a stack with a
  [resource import](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/import-resources.html)
  (a change set of type `IMPORT`).

#### Lab 1.4.5: Clean up

- Delete the Lesson 1.4 stack. If you imported the bucket in Lab 1.4.4,
  delete that stack too, and check whether the bucket survived it.

- Delete the bucket you created outside CloudFormation (if it still
  exists), the generated template (`delete-generated-template`) and the
  Parameter Store parameter from Lesson 1.2.

- Run your Lab 1.3.3 delete code once more against your region list, then
  confirm with `aws cloudformation list-stacks` in each of those regions
  that nothing from this module is left, and with `list-exports` that no
  exports remain.

### Retrospective 1.4

#### Question: Preview, Detect, Reconcile

_A teammate fixed a production problem by hand in the console last week.
Using what you learned in this lesson, describe how you would find out
exactly what they changed, and how you would get that change into the
template without an outage._

## Further Reading

Related topics to extend your knowledge about CloudFormation:

- Using
  [Stack Policies](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/protect-stack-resources.html)
  to apply permissions to modify a stack

- Using
  [StackSets](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/what-is-cfnstacksets.html)
  to deploy a CloudFormation stack simultaneously across an array of
  AWS Accounts and Regions, the managed version of Lesson 1.3

- [Nested stacks](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-nested-stacks.html)
  versus exports: two ways to split a large template

- [Dynamic references](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/dynamic-references.html)
  to Parameter Store and Secrets Manager

- [Stack refactoring](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stack-refactoring.html)
  to move resources between stacks without replacing them

- [CloudFormation Hooks](https://docs.aws.amazon.com/cloudformation-cli/latest/hooks-userguide/what-is-cloudformation-hooks.html)
  to enforce rules (such as your Guard rules) at deploy time

- [Infrastructure Composer](https://docs.aws.amazon.com/infrastructure-composer/latest/dg/what-is-composer.html)
  for drawing and editing templates visually
