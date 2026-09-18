# Topic 19: Multi-Account Foundation

<!-- TOC -->

- [Topic 19: Multi-Account Foundation](#topic-19-multi-account-foundation)
  - [What changed in the 2026 edition](#what-changed-in-the-2026-edition)
  - [Exam coverage](#exam-coverage)
  - [Cost and cleanup](#cost-and-cleanup)
  - [Guidance](#guidance)
  - [Conventions](#conventions)
  - [Lesson 19.1: Organizations and your lab account](#lesson-191-organizations-and-your-lab-account)
    - [Principle 19.1](#principle-191)
    - [Practice 19.1](#practice-191)
      - [Lab 19.1.1: Create or inspect the organization](#lab-1911-create-or-inspect-the-organization)
      - [Lab 19.1.2: Organizational units](#lab-1912-organizational-units)
      - [Lab 19.1.3: Create the lab account](#lab-1913-create-the-lab-account)
      - [Lab 19.1.4: Break-glass access with OrganizationAccountAccessRole](#lab-1914-break-glass-access-with-organizationaccountaccessrole)
      - [Lab 19.1.5: Everyday access with IAM Identity Center](#lab-1915-everyday-access-with-iam-identity-center)
      - [Lab 19.1.6: Centralize root access (optional)](#lab-1916-centralize-root-access-optional)
    - [Retrospective 19.1](#retrospective-191)
  - [Lesson 19.2: Guardrails with SCPs and RCPs](#lesson-192-guardrails-with-scps-and-rcps)
    - [Principle 19.2](#principle-192)
    - [Practice 19.2](#practice-192)
      - [Lab 19.2.1: Turn on service control policies](#lab-1921-turn-on-service-control-policies)
      - [Lab 19.2.2: A region guardrail](#lab-1922-a-region-guardrail)
      - [Lab 19.2.3: A baseline guardrail you write](#lab-1923-a-baseline-guardrail-you-write)
      - [Lab 19.2.4: The account SCPs can't touch](#lab-1924-the-account-scps-cant-touch)
      - [Lab 19.2.5: Resource control policies](#lab-1925-resource-control-policies)
      - [Lab 19.2.6: Tag policies (optional)](#lab-1926-tag-policies-optional)
    - [Retrospective 19.2](#retrospective-192)
  - [Lesson 19.3: Governance at scale](#lesson-193-governance-at-scale)
    - [Principle 19.3](#principle-193)
    - [Practice 19.3](#practice-193)
      - [Lab 19.3.1: Share a prefix list with AWS RAM](#lab-1931-share-a-prefix-list-with-aws-ram)
      - [Lab 19.3.2: Trusted access and delegated administrators](#lab-1932-trusted-access-and-delegated-administrators)
      - [Lab 19.3.3: Control Tower, on paper](#lab-1933-control-tower-on-paper)
    - [Retrospective 19.3](#retrospective-193)
  - [Lesson 19.4: Cost safety across accounts](#lesson-194-cost-safety-across-accounts)
    - [Principle 19.4](#principle-194)
    - [Practice 19.4](#practice-194)
      - [Lab 19.4.1: One bill, many accounts](#lab-1941-one-bill-many-accounts)
      - [Lab 19.4.2: Budgets that see the whole organization](#lab-1942-budgets-that-see-the-whole-organization)
      - [Lab 19.4.3: Point cleanup tooling at the lab account only](#lab-1943-point-cleanup-tooling-at-the-lab-account-only)
      - [Lab 19.4.4: Clean up the module](#lab-1944-clean-up-the-module)
    - [Retrospective 19.4](#retrospective-194)
  - [Further Reading](#further-reading)

<!-- /TOC -->

## What changed in the 2026 edition

- **New module.** The 2022 course assumed a shared, weekly-cleaned company
  sandbox. The 2026 edition is done by one person in their own AWS account,
  so every lab now runs in a dedicated **lab account** that this module
  creates. That is why it comes early in Phase 1, right after module 03.
- Multi-account design is tested on SAA, CloudOps, DevOps Pro, Solutions
  Architect Pro and Security Specialty, and the 2022 course never taught it.
- It covers features that did not exist in 2022: resource control policies
  (November 2024), centrally managed root access for member accounts
  (November 2024), declarative policies (December 2024), and Control Tower
  landing zone 4.0 with optional service integrations and a
  controls-dedicated experience (November 2025).
- IAM Identity Center with `aws configure sso` is the way into the lab
  account. The management account's `OrganizationAccountAccessRole` is
  treated as a break-glass path, not something you use every day.

## Exam coverage

| Exam | Domain / task statement |
|---|---|
| SAA-C03 | Domain 1: Design Secure Architectures (Task 1.1: secure access to AWS resources, including multi-account strategy and SCPs) |
| SOA-C03 | Domain 4: Security and Compliance |
| DOP-C02 | Domain 6: Security and Compliance |
| SAP-C02 → C03 | Domain 1: Design Solutions for Organizational Complexity (C03 guide publishes 2026-10-27 and adds GenAI / agent topics) |
| SCS-C03 | Domain 6: Security Foundations and Governance |

## Cost and cleanup

- **Free:** AWS Organizations, service control policies (SCPs), resource
  control policies (RCPs), tag policies, AWS RAM, IAM Identity Center,
  consolidated billing, and budgets without actions. Customer-managed
  prefix lists (Lab 19.3.1) have no charge.
- **Creating an organization ends the AWS Free Tier credits and free
  account plan** for accounts on the post-July-2025 Free Tier. The account
  is moved to a paid plan immediately. If you are still spending Free Tier
  credits, decide whether that matters before Lab 19.1.1.
  <!-- VERIFY: whether accounts on the legacy 12-month Free Tier keep it
  (historically shared once across the organization). -->
- **Control Tower** has no charge of its own, but the landing zone turns on
  AWS Config, CloudTrail, S3 log storage, SNS and more, and it creates extra
  accounts. That is why Lab 19.3.3 is reading only, with a hands-on part
  that is optional and at your own cost.
- **Small charges:** the test S3 bucket in Lab 19.2.5 (pennies), each Cost
  Explorer API call in Lab 19.4.1 ($0.01 per request).
- **Accounts are the one thing that is slow to undo.** A closed member
  account stays in the organization in a `CLOSED` state for a 90-day
  post-closure period, and during that time it still counts toward the
  organization's account quota (10 by default, possibly lower for new
  organizations). Closures also have their own quota: the greater of 20%
  of your member accounts or 250, capped at 1,000, in a rolling 30 days,
  with at most three closures in progress at once. An account you created
  can't be removed from the organization until it is at least four days
  old. Create only the one lab account this module asks for.
- **Cleanup:** [Lab 19.4.4](#lab-1944-clean-up-the-module) removes the
  test resources. The organization, the lab account, the Identity Center
  assignment, the guardrail SCPs and the budgets **stay**: every later
  module depends on them.

## Guidance

- Explore the official docs! See the AWS Organizations
  [User Guide](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_introduction.html),
  [API Reference](https://docs.aws.amazon.com/organizations/latest/APIReference/Welcome.html),
  [CLI Reference](https://docs.aws.amazon.com/cli/latest/reference/organizations/index.html)
  and
  [CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-organizations-policy.html)
  docs, and the user guides for
  [IAM Identity Center](https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html),
  [AWS RAM](https://docs.aws.amazon.com/ram/latest/userguide/what-is.html)
  and
  [AWS Control Tower](https://docs.aws.amazon.com/controltower/latest/userguide/what-is-control-tower.html).

- Read the whitepaper
  [Organizing Your AWS Environment Using Multiple Accounts](https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/organizing-your-aws-environment.html)
  before you design your OUs. It is the source for most of the patterns
  the exams ask about.

- Avoid using other sites like stackoverflow.com for answers \-- part
  of the skill set you're building is finding answers straight from
  the source, AWS.

- Explore your curiosity. Try to understand why things work the way
  they do. Read more of the documentation than just what you need to
  find the answers.

## Conventions

- **Two profiles.** You finish module 00 with a CLI profile for your own
  account, which this module turns into the organization's *management
  account*. This README calls that profile `mgmt`; use whatever name you
  gave it. By the end of Lesson 19.1 you also have a `lab` profile for the
  new lab account, with region `us-east-2`. After this module, **every lab
  in the course uses the `lab` profile.**
- **Organizations is a global service** hosted in `us-east-1`. Its CLI
  commands work from a `us-east-2` profile; you don't need `--region`. The
  same goes for IAM, Budgets and Cost Explorer.
- **Placeholders.** Examples use `444455556666` for the management account,
  `111122223333` for the lab account, `o-exampleorgid` for the organization
  and `you+aws-lab@example.com` for email. Your repository copy of this
  README should not contain your real account IDs or email addresses
  either: write `<lab-account-id>` in your answers.
- **SCPs and RCPs are JSON, not CloudFormation.** Keep them in
  [policies/](policies/) and create them with `aws organizations
  create-policy --content file://...`.
- DO use the AWS CLI rather than the console, except where a step says the
  console is required.

## Lesson 19.1: Organizations and your lab account

### Principle 19.1

*An AWS account is the strongest isolation boundary AWS offers, and AWS
Organizations makes accounts cheap enough to use one per purpose.*

### Practice 19.1

Nothing in one AWS account can reach into another unless someone grants
it. That makes an account a far better sandbox than any naming convention
or tag. An organization adds three things on top: one bill for all the
accounts, a hierarchy of organizational units (OUs) to hang policy on, and
a trusted way for the management account to create and govern member
accounts.

In these labs you'll turn your module 00 account into the management
account of a small organization, create a lab account inside it, and set
up two ways to reach the lab account: a break-glass role and everyday
IAM Identity Center access. Keep the management account for billing,
identity and governance only. From here on, nothing you build for the
course lives there.

#### Lab 19.1.1: Create or inspect the organization

You may already have an organization. When module 00 enabled IAM Identity
Center, the console offered to create one for you, since an organization
instance of Identity Center requires AWS Organizations.

- Using the `mgmt` profile, describe your organization. If the call says
  your account isn't in an organization, create one with **all features**
  enabled.

- Read [consolidated billing vs. all features](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_getting-started_concepts.html)
  and confirm which feature set your organization uses.

- List the organization's roots and accounts. Note the root ID (`r-...`);
  you'll need it in the next lab.

##### Question: Feature sets

_What can an organization with all features do that one with only
consolidated billing can't? Which of those do you need for this module?_

##### Question: The management account

_Read [Best practices for the management
account](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_best-practices_mgmt-acct.html).
Why do AWS and this course say not to run workloads in the management
account? Give at least two reasons, one of them about SCPs._

#### Lab 19.1.2: Organizational units

Design a small OU structure and create it with the CLI.

- Create two OUs under the root:
  - `Sandbox` for accounts where anything may be deleted at any time.
    Your lab account goes here.
  - `Workloads` for accounts that would hold real, long-lived things. It
    stays empty in this course, but it gives your guardrails somewhere
    different to point.

- Tag each OU with an `owner` tag containing your identifier.

- List the OUs under the root to confirm.

*The whitepaper above recommends more OUs (Security, Infrastructure,
Suspended, Policy Staging and so on). Two are enough for a solo learner.
Read the whitepaper's list anyway: the exams expect you to know it.*

##### Question: OU or account

_Policies can be attached to the root, to an OU, or to a single account.
Why is attaching them to OUs usually the better choice?_

#### Lab 19.1.3: Create the lab account

Create a member account with
[`aws organizations create-account`](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_create.html).

- **Email.** Every AWS account needs a root email address that no other
  AWS account uses, now or in the future. Even a closed account keeps its
  address. If your mail provider supports plus addressing, use it:
  `you+aws-lab@example.com` arrives in the inbox of `you@example.com` but
  is a different address to AWS. Check that your provider delivers
  plus-addressed mail before you rely on it.

- **Name.** Give the account a name that includes your identifier, such as
  `<you>-lab`.

- **Role name.** Leave the default (`OrganizationAccountAccessRole`).

- **Tags.** Add `owner` and `purpose=training` tags at creation time.

- Account creation is asynchronous. Poll
  `describe-create-account-status` with the request ID until the state is
  `SUCCEEDED`, then record the new account ID (outside the repository).

- New accounts are always created under the root. Move yours into the
  `Sandbox` OU with `move-account`.

##### Question: Root user of the new account

_The new account has a root user, but you never set a password for it.
How would you sign in as that root user if you ever had to? What should
you do with its credentials now? (Lab 19.1.6 offers a better answer.)_

#### Lab 19.1.4: Break-glass access with OrganizationAccountAccessRole

Organizations created a role in the lab account that trusts the
management account. Use it once, the way you'd use it in an emergency.

- Read [Accessing a member account that has
  OrganizationAccountAccessRole](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_access-cross-account-role.html)
  and [Using an IAM role in the AWS
  CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-role.html).

- Add a profile named `lab-breakglass` to `~/.aws/config` that uses
  `role_arn` and `source_profile = mgmt`. Do not copy temporary keys
  anywhere.

- Run `aws sts get-caller-identity --profile lab-breakglass` and confirm
  the account ID is the lab account's.

- Still using that profile, show the role's trust policy and its attached
  managed policies.

##### Question: Who is trusted

_Which principal does the role's trust policy name? What does that mean for
who, in the management account, can become an administrator of the lab
account?_

#### Lab 19.1.5: Everyday access with IAM Identity Center

Break-glass access proves the account works. For daily use you want
short-lived credentials tied to your Identity Center user, as in module 00.

- If Identity Center isn't enabled yet, enable an **organization
  instance** in the management account. This one-time step needs the
  console. The Region you choose becomes the Identity Center Region and
  can't be changed without deleting the instance. `us-east-2` is a good
  choice if you're starting fresh; if module 00 already enabled it
  somewhere else, keep that.

- Create a permission set for the lab, for example `LabAdmin`, with the
  AWS managed policy `AdministratorAccess` and a session duration of a
  few hours. Later labs create IAM roles, so the lab account really does
  need administrator access; the guardrails in Lesson 19.2 are what keep
  it in bounds.

- Assign your Identity Center user to the lab account with that
  permission set. Try this with the `sso-admin` CLI commands
  (`create-permission-set`, `attach-managed-policy-to-permission-set`,
  `create-account-assignment`) rather than the console, and poll the
  assignment status until it succeeds.

- Run `aws configure sso` again. Reuse your existing SSO session, pick the
  lab account and the `LabAdmin` role, set the default Region to
  `us-east-2`, and name the profile `lab`. See [Configuring IAM Identity
  Center authentication with the AWS
  CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sso.html).

- `aws sso login --profile lab`, then `aws sts get-caller-identity
  --profile lab`. Compare the ARN with the one from Lab 19.1.4.

- Make `lab` your default for the rest of the course (for example,
  `export AWS_PROFILE=lab` in your shell profile).

##### Question: Two roles into one account

_Both `lab-breakglass` and `lab` land you in the lab account as an
administrator. List the differences: who can use each, how long the
credentials last, where the role came from, and what CloudTrail records
as the identity. Which would you disable first if your management
account credentials leaked?_

#### Lab 19.1.6: Centralize root access (optional)

Since November 2024 the management account can remove root user
credentials from member accounts and perform the few root-only tasks on
their behalf.

- Read [Centralize root access for member
  accounts](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-enable-root-access.html).

- Enable trusted access for IAM in Organizations, then turn on root
  credentials management and privileged root actions with the CLI.

- Audit the lab account's root user credentials. What does it have?

##### Question: No root password

_If the lab account has no root password, how would you recover from a
bucket policy that denies everyone, including the account's own
administrators?_

### Retrospective 19.1

#### Question: Closing an account

_You won't close the lab account in this course. Work out the process
anyway from the docs
([Closing a member account](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_close.html),
[Close an AWS account](https://docs.aws.amazon.com/accounts/latest/reference/manage-acct-closing.html),
[Quotas](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_reference_limits.html)):_

- _Which CLI command closes a member account, and from which account?_
- _What happens during the 90-day post-closure period? Can the account be
  reopened, and how?_
- _Does a closed account still count toward your organization's account
  quota? How many closures does the closure quota allow?_
- _Why should you change the root email address before closing an
  account you might want to recreate?_
- _Why do many organizations move an account into a `Suspended` OU,
  with an SCP that denies everything, before they close it?_

#### Task: Organization as code

_Everything in this lesson was done with the CLI. Read the
CloudFormation resource types `AWS::Organizations::OrganizationalUnit`,
`AWS::Organizations::Account` and `AWS::Organizations::Policy`. Sketch
(don't deploy) how your OUs and the policies from Lesson 19.2 could be a
stack in the management account. What would you **not** want to manage
that way, and why?_
<!-- VERIFY: whether AWS::Organizations::* stacks must be deployed in
us-east-1. -->

## Lesson 19.2: Guardrails with SCPs and RCPs

### Principle 19.2

*Organization policies set the maximum permissions in member accounts.
They never grant anything, and they never apply to the management
account.*

### Practice 19.2

A request in a member account is allowed only if every applicable policy
allows it. Service control policies (SCPs) cap what the account's
**principals** (its users and roles, including the root user) can do.
Resource control policies (RCPs), added in November 2024, cap what
**anyone**, including principals from outside the organization, can do to
the account's **resources**. Neither one grants access: an identity
policy or a resource policy still has to do that. Neither one applies to
the management account or to service-linked roles.

Read these before you start:

- [SCP evaluation](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps_evaluation.html)
- [RCP evaluation](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_rcps_evaluation.html)
- [Understanding SCPs and RCPs](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_authorization_policies.html)
- [Policy evaluation logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html)

These labs use the **deny-list** strategy: leave the AWS managed
`FullAWSAccess` SCP attached everywhere and add targeted `Deny`
statements. Every guardrail gets a positive test (what should still
work) and a negative test (what should now fail), the same discipline as
Lesson 3.3.

*Attach policies to the `Sandbox` OU or the lab account, never to the
root, until you've tested them. A bad SCP on the root can lock every
member account at once.*

#### Lab 19.2.1: Turn on service control policies

- Enable the `SERVICE_CONTROL_POLICY` policy type on the root.

- List the SCPs that now exist and the targets `FullAWSAccess` is
  attached to.

- Show the SCPs attached directly to the lab account, then those
  attached to the `Sandbox` OU and to the root.

##### Question: Why FullAWSAccess

_What would happen to every principal in the lab account if you detached
`FullAWSAccess` from the `Sandbox` OU and attached nothing in its place?
Why does AWS attach it automatically?_

#### Lab 19.2.2: A region guardrail

The course runs in `us-east-2`, with `us-east-1` allowed for global
services and the few features pinned there (CloudFront certificates,
billing). A region guardrail makes a typo in `--region` fail instead of
quietly creating resources you'll forget to clean up.

- Read the starter policy [policies/scp-region-guardrail.json](policies/scp-region-guardrail.json)
  and AWS's region example in
  [SCP examples](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps_examples.html).
  Find out why it uses `NotAction` and why services like IAM, STS,
  Organizations and CloudFront are on the list.

- Create the SCP with the CLI and attach it to the `Sandbox` OU.

- Test it with the `lab` profile. This is a lab about Regions, so pass
  `--region` explicitly:
  - Positive: `aws ec2 describe-availability-zones --region us-east-2`
  - Positive: `aws ec2 describe-availability-zones --region us-east-1`
  - Positive: `aws iam list-roles` and `aws sts get-caller-identity
    --region eu-west-1`
  - Negative: `aws ec2 describe-availability-zones --region eu-west-1`

- Read the whole error message from the negative test.

<!-- VERIFY: the exact AccessDenied wording ("...with an explicit deny in
a service control policy") in the current CLI output. -->

##### Question: What the error says

_What in the error message tells you an SCP caused the denial rather than
a missing IAM permission? Why does that matter when you're debugging a
failed CloudFormation stack in a later module?_

##### Question: The exemption list

_Both allowed Regions include `us-east-1`, where most global services are
served from. With that in mind, which entries on the `NotAction` list are
doing real work here, and when would the list matter more? The AWS
example says it "might not include all of the latest global AWS services
or operations": how would you find out that a new service needed
adding?_

#### Lab 19.2.3: A baseline guardrail you write

Write a second SCP yourself, as `policies/scp-lab-baseline.json`, with
one `Deny` statement per rule and a meaningful `Sid` for each:

- **Stay in the organization:** deny `organizations:LeaveOrganization`.
- **Protect audit logs:** deny the CloudTrail actions that stop, delete or
  weaken a trail (`StopLogging`, `DeleteTrail`, `UpdateTrail`,
  `PutEventSelectors`).
- **Protect the break-glass role:** deny changes to
  `OrganizationAccountAccessRole` (updating its trust policy, attaching or
  detaching policies, deleting it).

Use the
[SCP syntax](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps_syntax.html)
page and the
[aws-samples SCP examples](https://github.com/aws-samples/service-control-policy-examples)
for reference, but write the policy yourself. Validate it with
`aws accessanalyzer validate-policy --policy-type SERVICE_CONTROL_POLICY`
before you create it. Attach it to the `Sandbox` OU.

Test each rule with the `lab` profile. Before you run the negative test
for leaving the organization, confirm from the management account that
the SCP is attached to `Sandbox` and that the lab account is in
`Sandbox`.

- Negative: `aws organizations leave-organization`
- Negative: `aws cloudtrail stop-logging --name <you>-no-such-trail`
- Negative: `aws iam attach-role-policy` on
  `OrganizationAccountAccessRole`
- Positive: `aws cloudtrail describe-trails`, and attaching a managed
  policy to a throwaway role you create for the test (delete it after)

##### Question: A trail that doesn't exist

_The CloudTrail negative test names a trail that doesn't exist. Did you
get `AccessDenied` or `TrailNotFoundException`? What does that tell you
about when the SCP is evaluated relative to the service looking up the
resource?_
<!-- VERIFY: which error is returned for a nonexistent trail under a
deny SCP. The question works either way, but the model answer depends
on it. -->

##### Question: Your own cleanup

_Suppose a later lab creates a CloudTrail trail in the lab account. Your
baseline SCP now stops you, and `OrganizationAccountAccessRole`, from
deleting it. How would you let a trusted role clean it up without
removing the guardrail for everyone? (Look at the `aws:PrincipalARN`
condition in the aws-samples policies.)_

#### Lab 19.2.4: The account SCPs can't touch

- Run the negative test from Lab 19.2.2 with the `mgmt` profile:
  `aws ec2 describe-availability-zones --region eu-west-1`.

- Explain the result.

##### Question: Guarding the management account

_If SCPs can't restrict the management account, what does protect it?
List at least three controls that apply to a solo learner._

#### Lab 19.2.5: Resource control policies

SCPs limit what your principals can do. RCPs limit what can be done to
your resources, whoever asks. RCPs support a growing list of services
([supported services](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_rcps.html#rcp-supported-services));
this lab uses S3.

- Enable the `RESOURCE_CONTROL_POLICY` policy type. Look at the
  `RCPFullAWSAccess` policy that is now attached everywhere.

- Read the
  [RCP syntax](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_rcps_syntax.html)
  page. Note what's different from an SCP: `Principal` must be `"*"`,
  customer-managed RCPs can only `Deny`, `NotAction` isn't supported, and
  `Action` can't be a bare `"*"`.

- Write `policies/rcp-require-tls.json`: deny all S3 actions when the
  request isn't sent over TLS. Attach it to the `Sandbox` OU.

- In the lab account, create a bucket named with your identifier and put
  a small object in it.
  - Positive: `aws s3 ls s3://<bucket>/`
  - Negative: the same command with
    `--endpoint-url http://s3.us-east-2.amazonaws.com`
  <!-- VERIFY: that the CLI sends the request over plain HTTP with an
  http:// endpoint URL and that S3 returns AccessDenied citing the RCP. -->

- Now read the identity-perimeter starter,
  [policies/rcp-identity-perimeter-starter.json](policies/rcp-identity-perimeter-starter.json),
  and AWS's fuller version in the
  [data perimeter policy examples](https://github.com/aws-samples/data-perimeter-policy-examples/tree/main/resource_control_policies).
  Replace `o-exampleorgid` with your organization ID (in your local copy,
  not in a commit), create it and attach it to the `Sandbox` OU.

- Give your bucket a bucket policy that allows `s3:GetObject` to the
  management account. With the `mgmt` profile, read the object. It
  should work: the management account is inside the organization.

##### Question: Testing the perimeter

_You can't easily run the negative test for the identity perimeter,
because every principal you own is inside your organization. What would
the negative test be, and what result would you expect? What does
`aws:PrincipalIsAWSService` exempt, and what would break without it?_

##### Question: SCP or RCP

_For each of these, say whether you'd use an SCP, an RCP or both:
(a) nobody in the lab account may create IAM users; (b) no one outside
the organization may read objects in lab-account buckets, even if a
bucket policy says otherwise; (c) all S3 requests to lab-account buckets
must use TLS._

#### Lab 19.2.6: Tag policies (optional)

- Read [Tag policies](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_tag-policies.html).
- Enable the tag policy type and write one that standardises the
  capitalisation of your `owner` tag key. Attach it to `Sandbox`.
- Find out what a tag policy does **not** enforce. How would you require
  that every new EC2 instance has an `owner` tag? (Hint: an SCP with
  `aws:RequestTag` and a `Null` condition.)

### Retrospective 19.2

#### Question: Where the deny came from

_A request in the lab account is denied. Walk through, in order, every
policy type that could have caused it: SCPs, RCPs, permission boundaries,
identity policies, resource policies and session policies. For each,
where would you look to confirm it?_

#### Question: Deny-list or allow-list

_This module used a deny list (keep `FullAWSAccess`, add denies). What
would an allow-list strategy look like, and why is it harder to live
with in a lab account?_

#### Question: Looking ahead

_Module 28 uses Amazon Bedrock. Cross-Region inference profiles can
route a request to a Region your region guardrail denies. Read the
"with Bedrock CRIS support" variant in the aws-samples region controls
and explain what it changes._
<!-- VERIFY: which Regions the US cross-Region inference profiles route
to in 2026, and whether the SCP is evaluated against the destination
Region. -->

#### Task: Policies in version control

_Your SCPs and RCPs now live in `policies/`. Write a short script (or a
Makefile target) that validates every policy in that directory with IAM
Access Analyzer and prints its size against the quota for its type.
Run it before every `update-policy`._

## Lesson 19.3: Governance at scale

### Principle 19.3

*Share resources, delegate administration and automate the landing zone
instead of rebuilding the same things in every account.*

### Practice 19.3

Once there is more than one account, three questions come up quickly.
How do accounts use a common resource without copying it? AWS RAM
shares it. Who administers an organization-wide service without
touching the management account? A delegated administrator. How do
new accounts get a consistent baseline? AWS Control Tower, or your own
automation that does the same job.

A solo learner needs very little of this, and Control Tower costs money.
Lab 19.3.1 is hands-on and free; Labs 19.3.2 and 19.3.3 are mostly
reading and questions.

#### Lab 19.3.1: Share a prefix list with AWS RAM

A customer-managed prefix list is a named set of CIDR blocks that
security groups and route tables can reference. It's free, it's regional
and it can be shared, which makes it a good first RAM share.

- Read [Sharing your AWS
  resources](https://docs.aws.amazon.com/ram/latest/userguide/getting-started-sharing.html)
  and [Share customer-managed prefix
  lists](https://docs.aws.amazon.com/vpc/latest/userguide/sharing-managed-prefix-lists.html).

- From the management account, enable RAM sharing with your
  organization.

- In the management account, in `us-east-2`, create a prefix list named
  with your identifier containing one or two documentation CIDRs (for
  example `198.51.100.0/24`).

- Create a resource share for it with the `Sandbox` **OU** as the
  principal, and don't allow external principals.

- With the `lab` profile:
  - Positive: list the resource shares shared with you and describe the
    prefix list.
  - Positive: create a security group in the lab account's default VPC
    with an inbound rule that references the prefix list.
  - Negative: try to add an entry to the prefix list.

##### Question: Sharing with an OU

_You shared with the `Sandbox` OU instead of the lab account ID. What
happens when you add a second sandbox account? What happens to the
security group rule if you delete the resource share?_

##### Question: Which account owns it

_This lab broke the "nothing in the management account" rule for a free
resource. In a real organization, which account would own shared
networking resources like this, and why not the management account?_

#### Lab 19.3.2: Trusted access and delegated administrators

- List the AWS services that have trusted access to your organization.
  Explain why each one is there (you enabled some of them in this module,
  sometimes without noticing).

- List the delegated administrators (probably none).

- Read [Delegated administrator for AWS
  Organizations](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_delegate_policies.html)
  and [Delegated administration in IAM Identity
  Center](https://docs.aws.amazon.com/singlesignon/latest/userguide/delegated-admin.html).
  Don't register one. Your only member account is a sandbox that gets
  wiped, so it is the wrong place for administration.

##### Question: Why delegate

_In an organization with dedicated Security and Shared Services accounts,
which services would you delegate, and to which account? What can a
delegated administrator for Identity Center still not do?_

#### Lab 19.3.3: Control Tower, on paper

Control Tower builds a *landing zone*, a governed multi-account
environment, on top of Organizations. It uses the pieces from this
module and adds automation around them.

Read:

- [What is AWS Control
  Tower?](https://docs.aws.amazon.com/controltower/latest/userguide/what-is-control-tower.html)
- [About AWS accounts in AWS Control
  Tower](https://docs.aws.amazon.com/controltower/latest/userguide/accounts.html)
- [About controls](https://docs.aws.amazon.com/controltower/latest/controlreference/controls.html)
  (preventive, detective and proactive)
- [Landing zone 4.0 key
  changes](https://docs.aws.amazon.com/controltower/latest/userguide/key-changes-lz-v4.html)
  and the [controls-dedicated
  experience](https://docs.aws.amazon.com/controltower/latest/userguide/controls-dedicated-env-getting-started.html)
- [Pricing](https://docs.aws.amazon.com/controltower/latest/userguide/pricing.html)
  and [Decommission a landing
  zone](https://docs.aws.amazon.com/controltower/latest/userguide/decommission-landing-zone.html)

Then answer the questions below. **Hands-on is optional and at your own
cost.** A full landing zone creates more member accounts (each needs
another unique email and counts toward your 10-account quota) and turns on
AWS Config and CloudTrail. Undoing it means decommissioning the landing
zone and closing accounts that then sit out a 90-day post-closure period.
If you do want hands-on time, the controls-dedicated experience, enabling
one *preventive* control on the `Sandbox` OU, is the smallest footprint.
<!-- VERIFY: that the controls-dedicated experience creates no additional
accounts and that preventive controls carry no charge. -->

##### Question: Controls map to what you built

_Control Tower's preventive controls, detective controls and proactive
controls are each implemented with a service you've met or will meet in
this course. Name the service behind each type. Which of them did you
build by hand in Lesson 19.2?_

##### Question: Landing zone accounts

_Which shared accounts does a classic landing zone create, and what
does each one hold? What did landing zone 4.0 make optional?_

##### Question: Would you use it

_For a solo learner with one lab account, what would Control Tower add
over this module, and what would it cost? When does it start to pay for
itself?_

### Retrospective 19.3

#### Question: Sharing or peering

_RAM can share a VPC subnet with another account in the organization (VPC
sharing). Compare that with giving each account its own VPC and
connecting them. Which is simpler to operate, and which isolates
failures and blast radius better?_

## Lesson 19.4: Cost safety across accounts

### Principle 19.4

*One bill, one budget and one blast radius: spending is seen from the
management account, and destruction is aimed only at the lab account.*

### Practice 19.4

Consolidated billing puts every member account's charges on the
management account's bill, so the management account is where you watch
spending. Destructive tooling such as aws-nuke works the other way round:
it must only ever reach the lab account. The account boundary you built
in Lesson 19.1 is what makes that safe. Credentials for the lab account
simply can't touch the management account.

#### Lab 19.4.1: One bill, many accounts

- Read [Consolidating billing for AWS
  Organizations](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/consolidated-billing.html).

- From the management account, get this month's cost grouped by linked
  account with `aws ce get-cost-and-usage`. (Each Cost Explorer API call
  costs $0.01.)

- With the `lab` profile, try the same call. Compare what each account
  can see.

##### Question: Who pays

_Which account receives the invoice? If the lab account ran up a large
bill, whose payment method is charged?_

#### Lab 19.4.2: Budgets that see the whole organization

Module 00 created a budget. Make sure it covers the lab account, and add
one aimed only at the lab.

- Read [Creating a
  budget](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-create.html).
  Budgets is a global service; its API lives in `us-east-1`.

- From the management account, confirm your module 00 budget has no
  linked-account filter, so it covers everyone.

- Create a second monthly cost budget, named with your identifier, that
  filters to the lab account's linked-account ID. Add notifications at
  50%, 80% and 100% of actual spend and at 100% of forecast. Use JSON
  files for `--budget` and `--notifications-with-subscribers`, and keep
  the email address out of the files you commit.

##### Question: Budget in the member account

_Could you create the lab budget from inside the lab account instead?
What would it see, and why is the management account the better place
for a budget that has to survive a cleanup run in the lab account?_

#### Lab 19.4.3: Point cleanup tooling at the lab account only

The rule for the rest of the course: **account-wide cleanup tooling runs
only against the lab account.**
[aws-nuke](https://github.com/ekristen/aws-nuke) is the usual tool. The
maintained version is the `ekristen/aws-nuke` fork; the original
`rebuy-de` repository was archived in October 2024.

- With the `lab` profile, give the lab account an IAM account alias that
  includes your identifier. aws-nuke refuses to run against an account
  without an alias, and asks you to type the alias to confirm.

- Write an aws-nuke config **outside your repository** (it contains
  account IDs) that:
  - puts the management account ID in the `blocklist`;
  - lists only the lab account under `accounts`;
  - covers `global`, `us-east-2` and `us-east-1`;
  - filters out what must survive: `OrganizationAccountAccessRole`, the
    `AWSReservedSSO_*` roles Identity Center manages, and the account
    alias.

- Run it **without** `--no-dry-run` and read the list of what it would
  delete. Don't run it for real now.

<!-- VERIFY: current aws-nuke config keys and filter syntax for the
Identity Center roles; whether presets cover service-linked roles. -->

##### Question: Belt and braces

_List every layer that stops aws-nuke from deleting something in your
management account: the config, the tool's own checks, the credentials
you give it, the account boundary. If you could keep only one, which
would it be and why?_

#### Lab 19.4.4: Clean up the module

Remove the test resources, and keep the foundation.

- **Delete:** the security group from Lab 19.3.1, the RAM resource
  share, the prefix list, and the S3 bucket and object from Lab 19.2.5.

- **Detach and delete** the identity-perimeter RCP. Some AWS features,
  such as log delivery to S3 from some services and Regions, reach your
  bucket as an AWS-owned account rather than a service principal, and
  a strict perimeter would block them in later modules. (The AWS example
  has placeholders for exactly these accounts.) Keep the TLS RCP.

- **Keep:** the organization, both OUs, the lab account in `Sandbox`, the
  `LabAdmin` assignment and `lab` profile, the region and baseline SCPs,
  and both budgets.

- Confirm with `list-policies-for-target` on the `Sandbox` OU that only
  the policies you meant to keep are attached.

### Retrospective 19.4

#### Question: What the account boundary bought you

_Go back to module 00's cleanup tooling and to the "cleaned every weekend"
sandbox described in [WORKFLOW.md](../WORKFLOW.md). What can you now do
in the lab account that you'd never risk in an account holding your real
infrastructure?_

## Further Reading

- [Organizing Your AWS Environment Using Multiple
  Accounts](https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/organizing-your-aws-environment.html)
  (whitepaper)
- [Building a Data Perimeter on
  AWS](https://docs.aws.amazon.com/whitepapers/latest/building-a-data-perimeter-on-aws/building-a-data-perimeter-on-aws.html)
  (whitepaper) and the
  [data perimeter policy examples](https://github.com/aws-samples/data-perimeter-policy-examples)
- [Declarative policies](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_declarative.html):
  enforce service configuration, such as IMDSv2 defaults or blocking public
  AMI sharing, across the organization. Compare them with SCPs.
- [aws-samples SCP examples](https://github.com/aws-samples/service-control-policy-examples)
  and [RCP examples](https://github.com/aws-samples/resource-control-policy-examples)
- [AWS services that you can use with AWS
  Organizations](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_integrate_services_list.html)
- [Updating the root user email address for a member
  account](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_accounts_update_primary_email.html)
  from the management account.
