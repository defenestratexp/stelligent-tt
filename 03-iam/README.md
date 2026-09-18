# Topic 3: Identity and Access Management (IAM)

<!-- TOC -->

- [Topic 3: Identity and Access Management (IAM)](#topic-3-identity-and-access-management-iam)
  - [What changed in the 2026 edition](#what-changed-in-the-2026-edition)
  - [Exam coverage](#exam-coverage)
  - [Cost and cleanup](#cost-and-cleanup)
  - [Guidance](#guidance)
  - [Lesson 3.1: Introduction to Identity and Access Management](#lesson-31-introduction-to-identity-and-access-management)
    - [Principle 3.1](#principle-31)
    - [Practice 3.1](#practice-31)
      - [Lab 3.1.1: IAM Role](#lab-311-iam-role)
      - [Lab 3.1.2: Customer Managed Policy](#lab-312-customer-managed-policy)
      - [Lab 3.1.3: Customer Managed Policy Re-Use](#lab-313-customer-managed-policy-re-use)
      - [Lab 3.1.4: AWS-Managed Policies](#lab-314-aws-managed-policies)
      - [Lab 3.1.5: Policy Simulator](#lab-315-policy-simulator)
      - [Lab 3.1.6: Clean Up](#lab-316-clean-up)
    - [Retrospective 3.1](#retrospective-31)
      - [Question: Stack Outputs](#question-stack-outputs)
      - [Task: Stack Outputs](#task-stack-outputs)
  - [Lesson 3.2: Trust Relationships & Assuming Roles](#lesson-32-trust-relationships--assuming-roles)
    - [Principle 3.2](#principle-32)
    - [Practice 3.2](#practice-32)
      - [Lab 3.2.1: Trust Policy](#lab-321-trust-policy)
      - [Lab 3.2.2: Explore the assumed role](#lab-322-explore-the-assumed-role)
      - [Lab 3.2.3: Add privileges to the role](#lab-323-add-privileges-to-the-role)
      - [Lab 3.2.4: A trust policy that survives re-provisioning](#lab-324-a-trust-policy-that-survives-re-provisioning)
      - [Lab 3.2.5: Clean up](#lab-325-clean-up)
    - [Retrospective 3.2](#retrospective-32)
      - [Question: Inline vs Customer Managed Policies](#question-inline-vs-customer-managed-policies)
      - [Question: Role Assumption](#question-role-assumption)
      - [Question: Role Chaining](#question-role-chaining)
  - [Lesson 3.3: Fine-Grained Controls With Policies](#lesson-33-fine-grained-controls-with-policies)
    - [Principle 3.3](#principle-33)
    - [Practice 3.3](#practice-33)
      - [Lab 3.3.1: Unrestricted access to a service](#lab-331-unrestricted-access-to-a-service)
      - [Lab 3.3.2: Resource restrictions](#lab-332-resource-restrictions)
      - [Lab 3.3.3: Conditional restrictions](#lab-333-conditional-restrictions)
      - [Lab 3.3.4: Validate policies with IAM Access Analyzer](#lab-334-validate-policies-with-iam-access-analyzer)
      - [Lab 3.3.5: Clean up](#lab-335-clean-up)
    - [Retrospective 3.3](#retrospective-33)
      - [Question: Positive and Negative Tests](#question-positive-and-negative-tests)
      - [Task: Positive and Negative Tests](#task-positive-and-negative-tests)
      - [Question: Limiting Uploads](#question-limiting-uploads)
      - [Task: Limiting Uploads](#task-limiting-uploads)
  - [Lesson 3.4: Permissions Boundaries and Guardrails](#lesson-34-permissions-boundaries-and-guardrails)
    - [Principle 3.4](#principle-34)
    - [Practice 3.4](#practice-34)
      - [Lab 3.4.1: A boundary caps a role](#lab-341-a-boundary-caps-a-role)
      - [Lab 3.4.2: Delegate role creation safely](#lab-342-delegate-role-creation-safely)
      - [Lab 3.4.3: Stretch: attribute-based access control](#lab-343-stretch-attribute-based-access-control)
      - [Lab 3.4.4: Clean up](#lab-344-clean-up)
    - [Retrospective 3.4](#retrospective-34)
      - [Question: Boundaries vs SCPs and RCPs](#question-boundaries-vs-scps-and-rcps)
      - [Question: Finding Unused Access](#question-finding-unused-access)
  - [Further Reading](#further-reading)

<!-- /TOC -->

## What changed in the 2026 edition

- The principal is now **you, signed in through IAM Identity Center**
  (module 00), not an IAM user. Trust policies in Lessons 3.2–3.4 trust
  your permission-set role, and Lab 3.2.4 shows why trusting its exact
  ARN is fragile and how to write a trust policy that survives
  re-provisioning.
- New Lab 3.3.4: validate every policy you write with **IAM Access
  Analyzer** (`validate-policy`) and turn a negative test into an
  automated custom policy check.
- New Lesson 3.4: **permissions boundaries**, delegated role creation,
  and an optional ABAC (tag-based) stretch lab. SCPs and RCPs are
  introduced as a forward reference to module 19.
- New retrospective items on role chaining and on finding unused access
  (Access Analyzer unused-access findings and policy generation).
- Lesson 3.2 and 3.3 each end with an explicit cleanup lab; Lab 3.2.4
  (Clean up) is now Lab 3.2.5.
- Third-party links replaced with AWS documentation;
  CloudFormation links point at the new *Template Reference* guide.
- "List the S3 buckets in us-east-1" removed: the lab region comes from
  your profile (`us-east-2`), and IAM itself is global.

## Exam coverage

| Exam | Domain / task statement |
|---|---|
| SAA-C03 | Domain 1: Design Secure Architectures (1.1 secure access) |
| SOA-C03 | Domain 4: Security and Compliance |
| SCS-C03 | Domain 4: Identity and Access Management |
| DOP-C02 | Domain 6: Security and Compliance (6.1 IAM at scale) |
| DVA-C02 | Domain 2: Security (2.1 authentication and authorization) |
| CLF-C02 | Domain 2: Security and Compliance (2.3 access management) |

<!-- VERIFY: SOA-C03 domain number for "Security and Compliance" (the C02
guide had it as Domain 4). DVA-C03 publishes 2026-10-27; C03 adds GenAI /
agent topics. -->

## Cost and cleanup

- **IAM is free** and **global**: roles and policies are not created in
  `us-east-2`, and they are visible from every region. They still count
  against account quotas and clutter the account, so delete them.
- Lessons 3.2 and 3.3 create a few small S3 buckets: effectively free,
  but CloudFormation cannot delete a bucket that still holds objects.
  Empty them first.
- IAM Access Analyzer policy validation (`validate-policy`) and policy
  generation are free. Custom policy checks (`check-access-not-granted`,
  `check-no-new-access`) cost a fraction of a cent per call. An
  **unused-access analyzer is billed per IAM role and user per month**;
  only create one if you intend to delete it the same day
  (see [Retrospective 3.4](#question-finding-unused-access)).
- Cleanup: each lesson ends with a lab that deletes its stacks. When you
  are done with the module, this should list none of your roles:

  ```shell
  aws iam list-roles --query "Roles[?contains(RoleName, '<your-id>')].RoleName"
  ```

## Guidance

- All CloudFormation templates should be written in YAML, and should
  pass `cfn-lint` before you create a stack from them.

- Do NOT copy and paste CloudFormation templates from the Internet at
  large.

- DO use the
  [CloudFormation template reference](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/introduction.html)
  and the [IAM User Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html).

- DO utilize every link in this document; note how the AWS
  documentation is laid out.

- DO use the AWS CLI for
  [CloudFormation](https://docs.aws.amazon.com/cli/latest/reference/cloudformation/),
  [IAM](https://docs.aws.amazon.com/cli/latest/reference/iam/),
  [STS](https://docs.aws.amazon.com/cli/latest/reference/sts/) and
  [Access Analyzer](https://docs.aws.amazon.com/cli/latest/reference/accessanalyzer/)
  (NOT the Console) unless otherwise specified.

- Your CLI credentials come from IAM Identity Center
  (`aws sso login --profile <your-profile>`, set up in module 00). Do not
  create IAM users or access keys for this module.

- Stacks that create IAM resources need `--capabilities CAPABILITY_IAM`,
  or `CAPABILITY_NAMED_IAM` if you give the resources explicit names.
  Include your identifier in names so you can find and clean them up.

- The lab region is `us-east-2`, set in your profile; don't pass
  `--region`. IAM is a global service, so the region only matters for the
  CloudFormation stacks, the S3 buckets and Access Analyzer.

## Lesson 3.1: Introduction to Identity and Access Management

### Principle 3.1

*Identity and Access Management (IAM) is the **authentication and authorization service**
used to control access to virtually everything in AWS.*

### Practice 3.1

IAM consists of a set of services and resources that allow individuals
(and services) to authenticate with AWS and then authorizes those
entities to perform specific activities with specific services. Like
most authentication/authorization systems, IAM deals with the *concepts*
of users, groups and permissions, but not necessarily those precise
*entities*: in 2026 the humans usually sign in through IAM Identity
Center, which hands them temporary credentials for an IAM role, and the
workloads use roles too.

#### Lab 3.1.1: IAM Role

Create a CFN template that specifies an
[IAM Role](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-iam-role.html).

- Provide values only for required attributes. (A role can't exist
  without a trust policy; for now, let the EC2 service assume it.)

- Using inline Policies, give the Role read-only access to all IAM
  resources.

- Create the Stack.

- Use the [awscli](https://docs.aws.amazon.com/cli/latest/reference/iam/)
  to query the IAM service twice:

  - List all the Roles
  - Describe the specific Role your Stack created.

#### Lab 3.1.2: Customer Managed Policy

Update the template and the corresponding Stack to make the IAM Role's
inline policy more generally usable:

- Convert the IAM Role's inline Policies array to a separate
  [customer managed policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_managed-vs-inline.html#customer-managed-policies)
  resource.

- Attach the new resource to the IAM Role.

- Update the Stack using the modified template.

#### Lab 3.1.3: Customer Managed Policy Re-Use

Update the template further to demonstrate reuse of the customer managed
policy:

- Add another IAM Role.

- Attach the customer managed policy resource to the new role.

- Be sure that you're not referencing an AWS managed policy in the
  role.

- Add/Update the Description of the customer managed policy to
  indicate the re-use of the policy.

- Update the Stack. *Did the stack update work?*

  - Query the stack to determine its state.
  - If the stack update was not successful,
    [troubleshoot and determine why](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html#update-replacement).
    Compare the *Update requires* line for `Description` and
    `ManagedPolicyName` in the
    [AWS::IAM::ManagedPolicy](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-iam-managedpolicy.html)
    reference.

#### Lab 3.1.4: AWS-Managed Policies

Replace the customer managed policy with
[AWS managed policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_managed-vs-inline.html#aws-managed-policies).

- To both roles, replace the customer managed policy reference with
  the corresponding AWS managed policy granting Read permissions to
  the IAM service.

- To the second role, add an additional AWS managed policy to grant
  Read permissions to the EC2 service.

- Update the stack.

#### Lab 3.1.5: Policy Simulator

Read about the [IAM policy simulator](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_testing-policies.html)
and practice using it.

- Using the two roles in your stack, simulate the ability of each role
  to perform the following actions (using
  [aws iam simulate-principal-policy](https://docs.aws.amazon.com/cli/latest/reference/iam/simulate-principal-policy.html)):

  - `iam:CreateRole`
  - `iam:ListRoles`
  - `iam:SimulatePrincipalPolicy`
  - `ec2:DescribeImages`
  - `ec2:RunInstances`
  - `ec2:DescribeSecurityGroups`

#### Lab 3.1.6: Clean Up

Clean up after yourself by deleting the stack.

### Retrospective 3.1

#### Question: Stack Outputs

_In Lab 3.1.5, you had to determine the Amazon Resource Names (ARN) of
the stack's two roles in order to pass those values to the CLI function.
You probably looked them up in the console or with a second CLI call.
What could you have done to your CFN template to make that unnecessary?_

#### Task: Stack Outputs

Institute that change from the Question above. Recreate the stack as per
Lab 3.1.5, and demonstrate how to retrieve the ARNs with a single
`aws cloudformation describe-stacks` call using `--query`. Delete the
stack again when you're done.

## Lesson 3.2: Trust Relationships & Assuming Roles

### Principle 3.2

*AWS service roles and other IAM principals can assume customer created
roles, enabling a principle-of-least-privilege of permissions for AWS
services and applications.*

### Practice 3.2

An IAM Role has two kinds of policies. The first we've worked with
already and this policy type (whether inline or managed) describes
permissions the role has. The second is a
[trust policy](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_terms-and-concepts.html),
describing which principals (services, roles, accounts, federated
identities) are allowed to assume that role.

For example, an AWS Lambda Function requires an execution role that
defines the permissions the function will have when it executes. To
provide those permissions, the role must trust the AWS Lambda service to
assume it, and this trust must be granted explicitly by the role.

In these labs, *you* are the principal. When you sign in through IAM
Identity Center, you are working in a session of an IAM role that
Identity Center created in the account for your permission set. Its name
starts with `AWSReservedSSO_`, and it lives under the path
`/aws-reserved/sso.amazonaws.com/`. You will trust that role, see why
doing so naively is fragile, and fix it.

#### Lab 3.2.1: Trust Policy

Find out who you are, then create a CFN template that creates an IAM
Role you can assume.

- Run `aws sts get-caller-identity`. The `Arn` it returns looks like
  this (placeholder values):

  ```text
  arn:aws:sts::123456789012:assumed-role/AWSReservedSSO_AdministratorAccess_0123456789abcdef/jdoe
  ```

  That is an STS *session* ARN, not the IAM role ARN. Find the role
  itself with
  [aws iam list-roles](https://docs.aws.amazon.com/cli/latest/reference/iam/list-roles.html)
  and `--path-prefix /aws-reserved/sso.amazonaws.com/`. Its ARN includes
  the path and, unless your Identity Center instance is in `us-east-1`,
  the Identity Center region:

  ```text
  arn:aws:iam::123456789012:role/aws-reserved/sso.amazonaws.com/us-east-2/AWSReservedSSO_AdministratorAccess_0123456789abcdef
  ```

- The role should reference the AWS managed policy ReadOnlyAccess.

- Add a trust relationship to the role that lets your permission-set
  role assume it. Pass the role ARN in as a template parameter; don't
  hard-code it.

- Create the stack.

- Using the AWS CLI, assume that new role with
  [aws sts assume-role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_use-resources.html#using-temp-creds-sdk-cli).
  If this fails, take note of the error you receive, diagnose the issue
  and fix it.

*Hint: Instead of setting up a new profile in `~/.aws/config`, use
`aws sts assume-role` and export the three values it returns
(`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`) in a
subshell. It's a valuable mechanism you'll use often through the API, and
it's good to know how to do it from the CLI as well. Run
`aws sts get-caller-identity` again to prove who you are now.*

#### Lab 3.2.2: Explore the assumed role

Test the capabilities of this new Role.

- Acting as the role, list your S3 buckets.

- Acting as this role, try to create an S3 bucket using the AWS CLI.

  - Did it succeed? It should not have!
  - If it succeeded, troubleshoot how Read access allowed the role
    to create a bucket.

#### Lab 3.2.3: Add privileges to the role

Update the CFN template to give this role the ability to upload to S3
buckets.

- Create an S3 bucket in the same template.

- Using either an inline policy or an AWS managed policy, provide the
  role with S3 full access.

- Update the stack.

- Assuming this role again, try to upload a text file to the bucket.

- If it failed, troubleshoot the error iteratively until the role is
  able to upload a file to the bucket.

#### Lab 3.2.4: A trust policy that survives re-provisioning

Read
[Referencing permission sets in resource policies](https://docs.aws.amazon.com/singlesignon/latest/userguide/referencingpermissionsets.html).
The `AWSReservedSSO_` role name ends in a random suffix. If every
assignment of your permission set to the account is removed, Identity
Center deletes the role; the next assignment creates a new role with a
**new suffix**. Your trust policy still names the old role, and IAM shows
it as an unrecognisable unique ID (`AROA...`), because the principal it
pointed at no longer exists. Nobody can assume the role any more, and in
a KMS key policy the same mistake can lock you out of the key.

(See
[IAM roles as principals](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_principal.html#principal-roles)
for why IAM stores the role's unique ID rather than its name.)

Rewrite the trust policy so that it doesn't depend on the suffix:

- Trust the account (`arn:aws:iam::<account-id>:root`, built with the
  `AWS::AccountId` pseudo-parameter) rather than one role.

- Narrow it back down with a `Condition` on the
  [aws:PrincipalArn](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html#condition-keys-principalarn)
  global condition key, using `ArnLike` and a wildcard in place of the
  suffix. (Why can't you put the wildcard in the `Principal` element
  itself?)

- Update the stack, then assume the role again and repeat one test from
  Lab 3.2.3.

- Answer inline: trusting the account root does *not* mean "anyone in
  the account". What else does a principal need before it can assume
  the role, that it didn't need when the trust policy named it
  explicitly?

#### Lab 3.2.5: Clean up

Clean up. Take the actions necessary to delete the stack, including
emptying the bucket.

### Retrospective 3.2

#### Question: Inline vs Customer Managed Policies

_In the context of an IAM role, what is the difference between
an inline policy and a customer managed policy? What are the differences
between a customer managed policy and an AWS managed policy?_

#### Question: Role Assumption

_When assuming a role, are the permissions of the initial principal
mixed with those of the role being assumed?
Describe how that could easily be demonstrated with both a positive test
(an action you expect to succeed) and a negative test (an action you
expect to be denied). The
[policy evaluation logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html)
page will help._

#### Question: Role Chaining

_Your Identity Center session is already a role session, so assuming a
second role from it is
[role chaining](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html#iam-term-role-chaining).
What is the maximum session duration you can request for the chained
role, and does the role's `MaxSessionDuration` change that? Try
`--duration-seconds 7200` and explain the result._

## Lesson 3.3: Fine-Grained Controls With Policies

### Principle 3.3

*AWS policies can provide fine-grained access control to specific
resources using specific conditions.*

### Practice 3.3

So far we have only provided service-level IAM policy controls, but IAM
policies generally should be more specific than that. For example, a
service role for an application will generally only need read/write
access to those specific resources that the application uses, and even
then that resource might only be accessible under certain conditions.
[Actions, resources, and condition keys for AWS services](https://docs.aws.amazon.com/service-authorization/latest/reference/reference_policies_actions-resources-contextkeys.html)
introduces the topic. We'll be exploring Resource restrictions and
Condition keys in this lesson, and then checking our work with IAM
Access Analyzer.

Keep in mind that not all resource types support resource-level
restrictions. See the Resource-level permissions information in
[AWS services that work with IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-services-that-work-with-iam.html)
for details.

#### Lab 3.3.1: Unrestricted access to a service

Create a CFN template that generates two S3 buckets and a Role, and
demonstrate you have full access to each bucket with this new role.

- Code a Role you can assume (use the trust policy from Lab 3.2.4) with
  a customer managed policy that allows full access to the S3 service.

- Create the stack.

- As yourself (your Identity Center session):

  - list the contents of your 2 new buckets
  - upload a file to each new bucket

- Assume the new role and repeat those two checks as that role.

#### Lab 3.3.2: Resource restrictions

Add a resource restriction to the role's policy that limits full access
to the S3 service for just one of the two buckets and allows only
read-only access to the other.

- Update the stack.

- Assume the new role and perform these steps as that role:

  - List the contents of your 2 new buckets.
  - Upload a file to each new bucket.

*Were there any errors? If so, take note of them.*

*What were the results you expected, based on the role's policy?*

#### Lab 3.3.3: Conditional restrictions

Add a conditional restriction to the role's policy. Provide a condition
that grants list access only to objects that start with "lebowski/".

- Update the stack.

- Assume the new role and perform the remaining directives as that
  role.

- Try to list a file in the root of the available bucket

  - If it *worked*, fix your policy and update the stack until this
    fails.

- Try to list that same file but now with the proper object key
  prefix.

  - If it *doesn't work*, troubleshoot why and fix either the role's
    policy or the list command syntax until you are able to
    list a file.

#### Lab 3.3.4: Validate policies with IAM Access Analyzer

The policy simulator tells you what a policy *does*. IAM Access Analyzer
[policy validation](https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-validation.html)
tells you what is *wrong* with it: errors, security warnings, general
warnings and suggestions, checked against IAM grammar and AWS best
practices.

- Save the permissions policy from Lab 3.3.3 as a JSON file (the
  template's YAML policy converted to JSON; the resolved policy is also
  available from `aws iam get-policy-version`).

- Run
  [aws accessanalyzer validate-policy](https://docs.aws.amazon.com/cli/latest/reference/accessanalyzer/validate-policy.html)
  against it with `--policy-type IDENTITY_POLICY`. Fix anything it
  reports, or explain inline why you are leaving it.

- Now break it on purpose: add a statement that uses a condition key
  the S3 actions don't support, or pairs `iam:PassRole` with
  `"Resource": "*"`, and validate again. What finding types come back?

- Validate your Lab 3.2.4 trust policy too. Which `--policy-type` fits a
  trust policy, and which `--validate-policy-resource-type`?

- Turn one of your negative tests into an automated check with
  [aws accessanalyzer check-access-not-granted](https://docs.aws.amazon.com/cli/latest/reference/accessanalyzer/check-access-not-granted.html):
  prove that the policy does *not* grant `s3:PutObject` on the
  read-only bucket. Then point it at the Lab 3.3.1 version of the policy
  and watch it fail. (Custom policy checks are billed per call; a few
  dozen calls cost well under a dollar.)

*Doing this for a whole template by hand gets old fast. Look at the
[IAM Policy Validator for AWS CloudFormation](https://github.com/awslabs/aws-cloudformation-iam-policy-validator),
which runs the same checks over every policy in a template and can fail
a pipeline. You'll want it in module 12.*

#### Lab 3.3.5: Clean up

Empty both buckets and delete the stack.

### Retrospective 3.3

#### Question: Positive and Negative Tests

_Were the tests you ran for resource- and condition-specific
restrictions exhaustive? Did you consider additional positive and/or
negative tests that could be automated in order to confirm the
permissions for the Role? Which of them could run without touching a
real bucket (the
[policy simulator](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_testing-policies.html),
[custom policy checks](https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-custom-policy-checks.html)),
and which must exercise the real API?_

#### Task: Positive and Negative Tests

Code at least one new positive and one new negative test. Script them so
that they can be re-run after every stack update, and so that the script
fails when a test result is not what you expect.

#### Question: Limiting Uploads

_Is it possible to limit uploads of objects with a specific prefix (e.g.
starting with "lebowski/") to an S3 bucket using IAM conditions? If not,
how else could this be accomplished?_

#### Task: Limiting Uploads

Research and review the best method to limit uploads with a specific
prefix to an S3 bucket.

## Lesson 3.4: Permissions Boundaries and Guardrails

### Principle 3.4

*Effective permissions are the intersection of every policy type that
applies: an identity policy grants, but a permissions boundary, an SCP
or an RCP can still cap what the grant is worth.*

### Practice 3.4

A
[permissions boundary](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html)
is a managed policy attached to a role or user that sets the *maximum*
permissions its identity policies can grant. It grants nothing on its
own. Its main use is delegation: letting a team create roles for their
own workloads without letting them create a role more powerful than
themselves.

In AWS Organizations, service control policies (SCPs) cap what
principals in an account can do, and resource control policies (RCPs)
cap what can be done to resources in an account. Both work alongside
boundaries in the same evaluation. You'll build them in module 19; here
you only need to know where they sit in
[policy evaluation logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html).

#### Lab 3.4.1: A boundary caps a role

Create a stack with:

- a customer managed policy to use as a boundary, allowing only S3 read
  actions (`s3:Get*`, `s3:List*`) and nothing else;
- one S3 bucket;
- a role you can assume, with the AWS managed policy
  `AmazonS3FullAccess` attached **and** the boundary set through the
  role's `PermissionsBoundary` property.

Then:

- Assume the role. List the bucket, then try to upload a file. Explain
  the result using the evaluation logic page.

- Run `aws iam simulate-principal-policy` for `s3:PutObject` and
  `s3:GetObject` on the role. Does the simulator take the boundary into
  account? Which field of the output tells you?

- Remove the boundary (update the stack) and repeat the upload. Put the
  boundary back.

#### Lab 3.4.2: Delegate role creation safely

This is the pattern the exams love. Add a second role to the stack, a
"delegated admin" you can assume, whose identity policy lets it:

- create roles, attach policies to them and pass them to services, but
  **only when** the new role carries your boundary (use the
  `iam:PermissionsBoundary` condition key);
- not modify or delete the boundary policy, and not remove the
  boundary from any role (`iam:DeleteRolePermissionsBoundary`).

Test it as the delegated admin:

- Negative: create a role with no boundary. It must fail.
- Negative: create a role with your boundary, then try to remove the
  boundary from it. It must fail.
- Positive: create a role with the boundary and attach
  `AdministratorAccess` to it. Assume the new role (you'll need to trust
  your Identity Center role in it) and show it still can't write to S3.

Validate the delegated admin's policy with `validate-policy` before you
deploy it. Read
[this AWS walkthrough of the pattern](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html#access_policies_boundaries-delegate)
if you get stuck, but write your own policy.

#### Lab 3.4.3: Stretch: attribute-based access control

[ABAC](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction_attribute-based-access-control.html)
grants access by matching tags instead of listing resources.

- Tag two objects in a bucket with `project=alpha` and `project=beta`.
- Write a role policy that allows `s3:GetObject` only when the object's
  `project` tag equals the principal's `project` tag
  (`${aws:PrincipalTag/project}`).
- Assume the role twice, passing a different
  [session tag](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html)
  each time (`aws sts assume-role --tags ...`). What must the trust
  policy allow before session tags work?

#### Lab 3.4.4: Clean up

Delete any roles the delegated admin created (CloudFormation doesn't
know about them), empty the bucket, and delete the stack. Then run the
role listing from [Cost and cleanup](#cost-and-cleanup) and confirm
nothing of yours is left.

### Retrospective 3.4

#### Question: Boundaries vs SCPs and RCPs

_A permissions boundary, an SCP and an RCP can all prevent an action
that an identity policy allows. For each, say what it is attached to,
who can change it, and whether it can ever grant access. If an SCP
allows `s3:*` and the boundary allows only `s3:Get*`, what can a role
with `AmazonS3FullAccess` do?_

#### Question: Finding Unused Access

_Least privilege is hard to reach by writing policies up front. Read
about Access Analyzer
[unused access findings](https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-findings.html)
and
[policy generation from CloudTrail activity](https://docs.aws.amazon.com/IAM/latest/UserGuide/access-analyzer-policy-generation.html).
What does each need before it can tell you anything (a trail, a
tracking period, time), and what does each cost? How would you use them
together to shrink the `AmazonS3FullAccess` role from Lab 3.3.1 to what
it actually used?_

*Optional: if you try either, an unused-access analyzer is billed per
role and user it monitors per month, including the `AWSReservedSSO_`
roles, so delete it
(`aws accessanalyzer delete-analyzer`) as soon as you've seen its
findings. Policy generation is free but needs a CloudTrail trail; delete
the trail and its bucket afterwards.*

<!-- VERIFY: whether the unused-access analyzer bills a partial month
when created and deleted the same day, and whether service-linked roles
are excluded from the per-role charge. -->

## Further Reading

- [Security best practices in IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html):
  be sure you're familiar with the ideas there.
- [Policy evaluation logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html)
  and its flow chart: worth knowing by heart for every exam.
- [Using IAM Access Analyzer](https://docs.aws.amazon.com/IAM/latest/UserGuide/what-is-access-analyzer.html),
  including external and internal access findings.
- [Permission sets in IAM Identity Center](https://docs.aws.amazon.com/singlesignon/latest/userguide/permissionsetsconcept.html),
  including permissions boundaries on permission sets.
- [Service control policies](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html)
  and
  [resource control policies](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_rcps.html)
  (module 19).
- [IAM JSON policy reference](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies.html),
  especially the `Principal`, `NotAction` and `Condition` elements.
