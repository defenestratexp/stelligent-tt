# Topic 0: Development Environment

<!-- TOC -->

- [Topic 0: Development Environment](#topic-0-development-environment)
  - [What changed in the 2026 edition](#what-changed-in-the-2026-edition)
  - [Exam coverage](#exam-coverage)
  - [Cost and cleanup](#cost-and-cleanup)
  - [Conventions](#conventions)
  - [Before you start: which account, which region](#before-you-start-which-account-which-region)
  - [Lesson 0.1: Getting AWS credentials](#lesson-01-getting-aws-credentials)
    - [Principle 0.1](#principle-01)
    - [Practice 0.1](#practice-01)
      - [Lab 0.1.1: Secure the account and enable IAM Identity Center](#lab-011-secure-the-account-and-enable-iam-identity-center)
      - [Lab 0.1.2: AWS CLI v2 with IAM Identity Center](#lab-012-aws-cli-v2-with-iam-identity-center)
      - [Lab 0.1.3: How temporary credentials work: MFA and STS](#lab-013-how-temporary-credentials-work-mfa-and-sts)
        - [Option 1: Getting credentials via the STS command](#option-1-getting-credentials-via-the-sts-command)
        - [Exercise 0.1.3: MFA Script](#exercise-013-mfa-script)
        - [Question 0.1.3: 1](#question-013-1)
        - [Question 0.1.3: 2](#question-013-2)
        - [Question 0.1.3: 3](#question-013-3)
        - [Option 2: Using aws-vault to handle your temporary tokens](#option-2-using-aws-vault-to-handle-your-temporary-tokens)
      - [Lab 0.1.4: Retire the access key](#lab-014-retire-the-access-key)
    - [Retrospective 0.1](#retrospective-01)
      - [Question: Where did the credentials come from?](#question-where-did-the-credentials-come-from)
  - [Lesson 0.2: Cost safety](#lesson-02-cost-safety)
    - [Principle 0.2](#principle-02)
    - [Practice 0.2](#practice-02)
      - [Lab 0.2.1: A budget alert](#lab-021-a-budget-alert)
      - [Lab 0.2.2: Finding what you created](#lab-022-finding-what-you-created)
      - [Lab 0.2.3: Account-wide cleanup tooling](#lab-023-account-wide-cleanup-tooling)
    - [Retrospective 0.2](#retrospective-02)
      - [Question: Alerts are not limits](#question-alerts-are-not-limits)
  - [Lesson 0.3: Your workstation and repository](#lesson-03-your-workstation-and-repository)
    - [Principle 0.3](#principle-03)
    - [Practice 0.3](#practice-03)
      - [Lab 0.3.1: GitHub](#lab-031-github)
      - [Lab 0.3.2: Local terminal, dev container and CloudShell](#lab-032-local-terminal-dev-container-and-cloudshell)
      - [Lab 0.3.3: Clone the repository](#lab-033-clone-the-repository)
    - [Retrospective 0.3](#retrospective-03)
      - [Question: Environments](#question-environments)
      - [Task](#task)
      - [Cleanup](#cleanup)
  - [Further Reading](#further-reading)

<!-- /TOC -->

## What changed in the 2026 edition

- AWS Cloud9 is gone: it closed to new customers in July 2024. The labs now
  use a local terminal with AWS CLI v2, an optional VS Code dev container, and
  AWS CloudShell.
- IAM Identity Center with `aws configure sso` is now the main way to get CLI
  credentials. Long-lived IAM user access keys only appear in one exercise that
  shows why you shouldn't use them, and that exercise ends by deleting the key.
- The MFA + STS session-token exercise stays, because it shows how temporary
  credentials work. The example script (`scripts/n9n-autologin.sh`) was fixed.
  It no longer deletes other profiles, overwrites working credentials when STS
  fails, or leaves credentials in a world-readable file.
- aws-vault now points at the maintained ByteNess fork. The upstream 99designs
  project has been abandoned.
- New lesson on cost safety: a budget alert, finding resources by tag, and
  account-wide cleanup tooling (the maintained `ekristen/aws-nuke` fork; the
  `rebuy-de` original was archived in October 2024).
- The course now uses one lab region, `us-east-2`, and a dedicated lab account.
- Removed the hard-coded Stelligent account ID from example ARNs. Replaced
  `help.github.com` links with current `docs.github.com` pages. Branches merge
  to `main`.

## Exam coverage

| Exam | Domain / task statement |
|---|---|
| CLF-C02 | Domain 2: Security and Compliance. Task 2.3: Identify AWS access management capabilities (root user protection, MFA, IAM Identity Center, temporary credentials) |
| CLF-C02 | Domain 3: Cloud Technology and Services. Task 3.1: Define methods of deploying and operating in the AWS Cloud (console, CLI, CloudShell) |
| CLF-C02 | Domain 4: Billing, Pricing, and Support. Task 4.2: Understand resources for billing, budget, and cost management (AWS Budgets, cost allocation tags) |
| SOA-C03 | Domain 4: Security and Compliance. Task 4.1: Implement and manage security and compliance tools and policies (MFA, federated identity, policy conditions, multi-account strategy) |
| SCS-C03 | Domain 4: Identity and Access Management. Task 4.1: Design, implement, and troubleshoot authentication strategies (IAM Identity Center, MFA, AWS STS temporary credentials) |

## Cost and cleanup

- Nothing in this module has an hourly charge. IAM Identity Center, IAM, AWS
  CloudShell, Resource Explorer and budgets without actions are free. Budget
  actions are free for the first two action-enabled budgets; this module
  doesn't use them.
- The only thing you create that you shouldn't leave behind is the IAM user
  and access key from [Lab 0.1.3](#lab-013-how-temporary-credentials-work-mfa-and-sts).
  [Lab 0.1.4](#lab-014-retire-the-access-key) deletes them, and the
  [final cleanup step](#cleanup) checks that they're gone.
- Keep the budget from [Lab 0.2.1](#lab-021-a-budget-alert). It protects you
  for the rest of the course.

## Conventions

- Do NOT store AWS credentials in code repositories.
  - [Manage access keys for IAM users](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html)
  - [Configuration and credential file settings](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)

- DO use the [AWS documentation and user guides](https://docs.aws.amazon.com/).
  Avoid other sites like stackoverflow.com for answers. Part of the skill
  you're building is finding answers in AWS's own documentation.

- DO use the `--debug` switch on AWS CLI commands to see what happens behind
  the scenes: which credentials were found, which endpoint was called and
  what the raw response was. Many EC2 commands also accept `--dry-run`, which
  checks your permissions without doing anything.

- DO tag everything you create with your identifier (for example
  `Owner=<your-id>`) and include it in resource names. Lesson 0.2 relies on
  this.

## Before you start: which account, which region

**Use a dedicated lab account.** Every lab in this course creates and deletes
resources. Later lessons use tools that delete *everything* in an account. You
want all of that in an account that holds nothing else. The course creates
this account under AWS Organizations in
[module 19](../19-multi-account/README.md), early in Phase 1.
<!-- VERIFY: module 19 directory name (../19-multi-account) once it exists -->
Until then, the bootstrap below gets you working safely on day one.

**Lab region: `us-east-2` (Ohio).** You set it once, in your AWS CLI profile.
CLI examples in this course don't pass `--region`, and templates take
region-specific values as parameters. `us-east-2` is in the lowest price tier
and keeps lab resources away from any real workloads you run in other
regions. A few services are global or live in `us-east-1` whatever your
profile says: IAM, Organizations, billing and AWS Budgets, and CloudFront with
its ACM certificate. Labs that use them point this out.

## Lesson 0.1: Getting AWS credentials

### Principle 0.1

*Humans get short-lived credentials from an identity provider. Long-lived
secret keys on laptops are a liability, not a convenience.*

### Practice 0.1

The following labs prepare you to work through the rest of the course. You
will protect the account's root user, set up IAM Identity Center so that you
sign in once and the AWS CLI receives temporary credentials, and then do the
old way by hand once: an IAM user key plus MFA, exchanged for an STS session
token. Doing it by hand shows what Identity Center automates, and STS
questions come up in every exam. The lesson ends with the long-lived key
deleted.

#### Lab 0.1.1: Secure the account and enable IAM Identity Center

This is the one-time bootstrap. Use the console for it; it happens once, and
some steps can't be done from the CLI.

1. Sign in as the root user, add
   [MFA to the root user](https://docs.aws.amazon.com/IAM/latest/UserGuide/enable-mfa-for-root.html)
   (if AWS didn't already make you do it at sign-in), and make sure the root
   user has no access keys. After this lab you should only need root for the
   [tasks that require root user credentials](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-user.html#root-user-tasks).

1. Enable IAM Identity Center. Follow
   [Getting started](https://docs.aws.amazon.com/singlesignon/latest/userguide/getting-started.html)
   in the IAM Identity Center User Guide. Choose what fits your situation:

   - **Day one, one account:** enable the *organization instance* from your
     account. This creates an AWS Organization and makes this account its
     management account. Don't choose an *account instance*: it can't give
     you access to AWS accounts, only to applications.
     <!-- VERIFY: accounts on the post-July-2025 AWS Free Tier "free plan" may need upgrading to a paid plan before they can use AWS Organizations -->
   - **You already have an organization:** use the Identity Center that is
     already running in its management account (or ask whoever runs it).

   Enable Identity Center in `us-east-2` unless your organization already uses
   another region. That region is its *home region*. It holds your identity
   store and you can't simply move it later.
   <!-- VERIFY: Identity Center now supports replication to additional Regions for organization instances; confirm that the primary Region still can't be changed -->

1. In Identity Center, create a user for yourself (with MFA, which Identity
   Center asks for by default) and a permission set. Assign both to the
   account.
   - For the day-one bootstrap, that account is the management account, and
     the predefined `AdministratorAccess` permission set is what the early
     labs need. Keep in mind that the management account is exactly where
     you *don't* want lab resources in the long run. SCPs don't apply to it,
     and it's the account that can close all the others.
   - In [module 19](../19-multi-account/README.md) you create a
     member account for labs, assign the same permission set there, and move
     your CLI profile to it. After that, the management account is only used
     for organization and billing tasks.

1. Note your **AWS access portal URL** (the "start URL") from the Identity
   Center dashboard. You need it in the next lab.

##### Question 0.1.1

What is the difference between a *user* in IAM Identity Center and an *IAM
user*? What does a *permission set* become in the account it's assigned to?
(Hint: look at IAM roles in that account after you assign it.)

#### Lab 0.1.2: AWS CLI v2 with IAM Identity Center

1. [Install or update AWS CLI v2](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
   on your laptop. Check it with `aws --version`.

1. Run `aws configure sso` and follow
   [Configuring IAM Identity Center authentication with the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/sso-configure-profile-token.html).
   - Give the session a name (for example `stelligent-u`), paste the start URL,
     and enter Identity Center's home region as the SSO region.
   - Pick your account and permission set.
   - Set the **default client region to `us-east-2`**, output `json`, and give
     the profile a short name (for example `lab`).

1. Open `~/.aws/config` and read what the wizard wrote. Note that there is an
   `[sso-session ...]` section and a `[profile ...]` section, and that
   nothing was written to `~/.aws/credentials`. The example below uses
   placeholders; yours has your own values:

   ```ini
   [profile lab]
   sso_session = stelligent-u
   sso_account_id = 123456789012
   sso_role_name = AdministratorAccess
   region = us-east-2
   output = json

   [sso-session stelligent-u]
   sso_start_url = https://d-1234567890.awsapps.com/start
   sso_region = us-east-2
   sso_registration_scopes = sso:account:access
   ```

1. Make the profile your default for this shell with
   `export AWS_PROFILE=lab`, sign in with `aws sso login`, and then run a
   few commands to confirm access:

   - [get-caller-identity](https://docs.aws.amazon.com/cli/latest/reference/sts/get-caller-identity.html)
   - [list-buckets](https://docs.aws.amazon.com/cli/latest/reference/s3api/list-buckets.html)
   - [describe-instances](https://docs.aws.amazon.com/cli/latest/reference/ec2/describe-instances.html)

1. Run `aws sts get-caller-identity --debug` and find the lines where the
   CLI looks for credentials. Then look in `~/.aws/sso/cache/` and
   `~/.aws/cli/cache/`.

##### Question 0.1.2

What does the ARN returned by `get-caller-identity` tell you about the
identity you are actually using? How long do these credentials last, and what
do you do when they expire?

#### Lab 0.1.3: How temporary credentials work: MFA and STS

Before Identity Center, the usual setup was an IAM user with a long-lived
access key and an MFA device. To use the MFA, you traded the key plus a
one-time code for temporary credentials from
[AWS STS](https://docs.aws.amazon.com/STS/latest/APIReference/API_GetSessionToken.html).
You're going to do that once, because it's what Identity Center does for you
behind the scenes, and because the exams expect you to know it.

Set it up with your `lab` profile:

1. Create an IAM user named `<your-id>-mfa-lab` with no console access.
1. [Assign it a virtual MFA device](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa_enable_virtual.html).
1. Give the user a small inline policy. It should allow `iam:ListMFADevices`
   on itself, and allow `s3:ListAllMyBuckets` and `ec2:DescribeInstances`
   *only when* `aws:MultiFactorAuthPresent` is true. The user doesn't need
   permission to call `sts:GetSessionToken`; find out why in the docs.
   See [Configuring MFA-protected API access](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa_configure-api-require.html).
   Save the policy in your repository.
1. Create an access key for the user and store it in a profile named
   `mfa-lab` in `~/.aws/credentials` (`aws configure --profile mfa-lab`). Set
   `region = us-east-2` for that profile. Remember that an access key and
   secret key together are user credentials. Never commit them, never paste
   them into chat or email, and delete them when this lab is done.
1. Try `aws s3api list-buckets --profile mfa-lab`. It should be denied.

##### Option 1: Getting credentials via the STS command

Find the ARN of the MFA device (IAM console > Users > your user > Security
credentials > "Assigned MFA device", or `aws iam list-mfa-devices`). The
token code is the current code from your MFA app.

```shell
aws sts get-session-token \
    --serial-number arn:aws:iam::123456789012:mfa/USERNAME \
    --token-code 123456 \
    --profile mfa-lab
```

This returns JSON containing the temporary credentials:

```json
{
    "Credentials": {
        "AccessKeyId": "ASIAIOSFODNN7EXAMPLE",
        "SecretAccessKey": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        "SessionToken": "AQoDYXdzEJr...<remainder of security token>",
        "Expiration": "2026-10-11T10:09:50Z"
    }
}
```

Note that the access key ID starts with `ASIA` (temporary) rather than
`AKIA` (long-lived). To use these credentials, put them in their own profile.
The keys go in `~/.aws/credentials`:

```ini
[temp]
aws_access_key_id = ASIAIOSFODNN7EXAMPLE
aws_secret_access_key = wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
aws_session_token = AQoDYXdzEJr...<remainder of security token>
```

and settings such as region go in `~/.aws/config`:

```ini
[profile temp]
region = us-east-2
output = json
```

`aws configure set <key> <value> --profile temp` writes each value to the
right file for you. Then either select the profile:

```shell
export AWS_PROFILE=temp
aws s3api list-buckets
```

or export the three values as environment variables (`AWS_ACCESS_KEY_ID`,
`AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`). Leaving out the session token
is a classic mistake. The same `list-buckets` call now succeeds. By default
these credentials last 12 hours; `--duration-seconds` changes that.

##### Exercise 0.1.3: MFA Script

1. Create a script to automate the gathering and assigning of the temporary
   AWS MFA credentials from Option 1.
1. Try to reduce the amount of manual input as much as possible.
1. Make it safe. It must never damage the credentials file, lose other
   profiles, or overwrite working credentials when STS rejects the code. It
   shouldn't leave secrets lying around in readable temporary files.

> TT - `n9n-autologin.sh` in the scripts directory accomplishes these tasks.
> Just call the script with the latest MFA code. It finds the MFA device from
> `AWS_MFA_SERIAL`, else `mfa_serial` in the source profile
> (`AWS_SOURCE_PROFILE`, default `n9n`) in `~/.aws/config`, else by asking
> IAM, so no account ID is kept in the script. It writes only the `[temp]`
> profile (`AWS_TARGET_PROFILE`) with `aws configure set`, so other profiles
> are untouched. Keys go to `~/.aws/credentials`, and region/output go to
> `~/.aws/config`. The region comes from the source profile, else
> `us-east-2`. If `get-session-token` fails, it stops and leaves the existing
> credentials alone. The STS response is held in a `mktemp` file with mode
> 600 that is removed on exit.

##### Question 0.1.3: 1

What method did you use to store the aws credentials? What are some other
options?

> $HOME/.aws/credentials was used here. Other methods include inline
> declaration, environment variables, or AWS Vault.

##### Question 0.1.3: 2

Which AWS environment variable cannot be set in order to run the
`aws sts get-session-token` command?

##### Question 0.1.3: 3

Your policy allowed `list-buckets` only when `aws:MultiFactorAuthPresent` is
true. Why did the long-lived key fail and the session credentials succeed,
even though both belong to the same IAM user?

##### Option 2: Using aws-vault to handle your temporary tokens

If you would rather not manage STS tokens yourself, use
[aws-vault](https://github.com/ByteNess/aws-vault). The original
`99designs/aws-vault` project has been abandoned; ByteNess maintains the fork.
aws-vault keeps the long-lived key in your operating system's secure store
(macOS Keychain, Windows Credential Manager, or on Linux the Secret Service,
`pass` or an encrypted file; see its `--backend` option) instead of in
`~/.aws/credentials`.
<!-- VERIFY: package managers (brew/choco/nix "aws-vault") now install the ByteNess fork rather than the 99designs release -->

Add the key with `aws-vault add mfa-lab`, then add the MFA device's ARN to the
profile in `~/.aws/config`:

```ini
[profile mfa-lab]
region = us-east-2
output = json
mfa_serial = arn:aws:iam::123456789012:mfa/USERNAME
```

Now you can run any command through aws-vault, for example
`aws-vault exec mfa-lab -- aws s3api list-buckets`. It prompts for the MFA
code and caches the session. If you forget the password of aws-vault's store,
see the "backends" section of its USAGE document for how to reset that
backend and start over.

#### Lab 0.1.4: Retire the access key

You have now seen the old way. Remove it:

1. Delete the `<your-id>-mfa-lab` user's access key, deactivate and delete its
   MFA device, and delete the user (CLI: `aws iam delete-access-key`,
   `aws iam deactivate-mfa-device`, `aws iam delete-virtual-mfa-device`,
   `aws iam delete-user-policy`, `aws iam delete-user`).
1. Remove the `[mfa-lab]` and `[temp]` sections from `~/.aws/credentials` and
   `~/.aws/config`. `aws configure` can set values but can't delete a
   section, so use an editor.
1. Delete the MFA entry from your authenticator app, and remove the key from
   aws-vault if you used it (`aws-vault remove mfa-lab`).
1. Confirm with `aws iam list-users` that the user is gone.

### Retrospective 0.1

#### Question: Where did the credentials come from?

*Compare the credentials you got from `aws sso login` with the ones you got
from `get-session-token`. Both are temporary and both need a session token.
What is different about how they were issued and what they are allowed to
do, and what happens to each when the person leaves the team? Why is IAM
Identity Center preferred for people, while IAM roles are preferred for
workloads such as EC2 instances and Lambda functions?*

## Lesson 0.2: Cost safety

### Principle 0.2

*You find out what a lab costs from an alert, not from the invoice. Anything
you can't find, you can't delete.*

### Practice 0.2

Every later module ends with a cleanup step, but people forget, stacks fail
halfway through, and some resources (NAT gateways, load balancers, public IPv4
addresses, EKS clusters) charge by the hour. These labs set up an early
warning, show you how to find everything you've tagged, and introduce the
heavy tool for emptying a lab account, along with the rules for keeping it
away from anything that matters.

#### Lab 0.2.1: A budget alert

Create a monthly cost budget with email alerts using
[AWS Budgets](https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html).

- Budgets is a global service. Its endpoint lives in `us-east-1` whatever
  region your profile uses, and a budget covers every region.
- Create the budget in the account that pays the bill. On day one that's your
  only account. Once you have an organization, a budget in the management
  account can cover the whole organization or filter on the lab account.
- Pick a limit you would actually notice (for example 20 USD). Set one alert
  on *actual* spend at 50% and one on *forecasted* spend at 100%.
- Use the CLI:
  [`aws budgets create-budget`](https://docs.aws.amazon.com/cli/latest/reference/budgets/create-budget.html)
  with a `budget.json` and a `notifications-with-subscribers.json`. Look up
  your account ID with `aws sts get-caller-identity`. Don't hard-code it in
  anything you commit.
- Save the two JSON files in your repository, but use a placeholder for your
  email address rather than committing the real one.
- Also look at the console's budget templates, especially the *zero spend*
  budget, and at
  [Cost Anomaly Detection](https://docs.aws.amazon.com/cost-management/latest/userguide/manage-ad.html).

Check with `aws budgets describe-budgets --account-id <id>`. Then confirm the
subscription email arrived and isn't in your spam folder.

##### Question 0.2.1

How often is budget data refreshed? If a lab left a NAT gateway running
overnight, roughly when would this budget tell you?

#### Lab 0.2.2: Finding what you created

Tags are how you find your own resources later.

1. Create something cheap and tagged, for example an empty S3 bucket named
   with your identifier and tagged `Owner=<your-id>`.
1. Find it by tag with the
   [Resource Groups Tagging API](https://docs.aws.amazon.com/resourcegroupstagging/latest/APIReference/overview.html):
   `aws resourcegroupstaggingapi get-resources --tag-filters Key=Owner,Values=<your-id>`.
   Note that it searches one region at a time.
1. Turn on [AWS Resource Explorer](https://docs.aws.amazon.com/resource-explorer/latest/userguide/welcome.html)
   (Quick setup, with an aggregator index in `us-east-2`). Search for
   `tag:Owner=<your-id>` in the console and with
   `aws resource-explorer-2 search`.
1. Find the same resources with the console's
   [Tag Editor](https://docs.aws.amazon.com/tag-editor/latest/userguide/tag-editor.html).
1. Delete the bucket.

These are the gentle cleanup tools. They show you what's there, and you
decide what to delete. Use them first, especially in any shared account.

##### Question 0.2.2

Which of your resources would these searches miss? (Think about untagged
resources, resources other services create for you, and regions you haven't
indexed.) How could you make tagging automatic for everything you deploy
with CloudFormation?

#### Lab 0.2.3: Account-wide cleanup tooling

> **WARNING: aws-nuke deletes every resource it can find in an account that
> isn't filtered out. Never run it against an account that holds real
> workloads, your organization's management account, or any account you
> share. Use it only in your dedicated lab account, and only after reading
> the dry-run output line by line.**

[aws-nuke](https://github.com/ekristen/aws-nuke) is the maintained fork
(`ekristen/aws-nuke`; the original `rebuy-de/aws-nuke` was archived in October
2024). It has several safety checks:

- It runs as a dry run unless you pass `--no-dry-run`.
- It refuses to run unless the account has an account alias.
- Its config requires a `blocklist` of accounts it must never touch.
- It only touches accounts listed under `accounts`.

Do this now, but **dry run only**:

1. Read the [aws-nuke documentation](https://aws-nuke.ekristen.dev/),
   including the configuration and filtering pages.
1. Write a config that targets only your lab account. Put your management
   account (and any other account you own) in `blocklist`, limit `regions` to
   `us-east-2` and `global`, and add filters that keep what you want to keep:
   your Identity Center roles (`AWSReservedSSO_*`), your budget, and the
   organization's own roles. Save it in your repository with placeholder
   account IDs.
1. Once you have the lab account from
   [module 19](../19-multi-account/README.md), run it as a dry run
   against that account and read the output. Until then, don't run it at all.
   The bootstrap account is your management account.

Cloud Custodian and AWS Config rules with remediation are other ways to
enforce cleanup; later modules cover some of them.

### Retrospective 0.2

#### Question: Alerts are not limits

*A budget alert tells you about spend; it doesn't stop it. What could you add
if you wanted spend to trigger an automatic response, and what would that
response have to be careful not to break? Why is "delete everything that
isn't tagged" dangerous even in a lab account?*

## Lesson 0.3: Your workstation and repository

### Principle 0.3

*A reliable, repeatable process to create your development environment
leads to a solution others can contribute to.*

### Practice 0.3

You'll work from a GitHub repository created from the course template, using
a local terminal as your main environment. Two alternatives run the same
commands elsewhere: a VS Code dev container, which gives you a reproducible
toolchain on any machine, and AWS CloudShell, a browser shell with the CLI
already installed. Comparing where each one gets its credentials is the point
of the retrospective.

#### Lab 0.3.1: GitHub

1. Create a new repository from the
   [Stelligent-U repository template](https://github.com/defenestratexp/stelligent-tt/generate)
   ([Creating a repository from a template](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)).
1. Select the owner of the repository (yourself, not the course's owner).
1. Name the new private repository. Its default branch is `main`.
1. Generate an SSH key, add it to GitHub and test access using
   [Connecting to GitHub with SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).
   Clone the private repository to your laptop.

#### Lab 0.3.2: Local terminal, dev container and CloudShell

Run the same commands (`aws sts get-caller-identity`,
`aws s3api list-buckets`, `aws ec2 describe-instances`) in each environment
you set up, and note which identity each one reports.

1. **Local terminal (required).** You already have this from Lab 0.1.2.
   Also install git and the language runtime you'll use for the course
   (Python, Node.js, Go or Ruby).

1. **Dev container (optional).** Put the toolchain in a
   [dev container](https://containers.dev/) so it's the same on any machine,
   using [VS Code Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers).
   - Add `.devcontainer/devcontainer.json` to your repository. Base it on a
     Dev Containers image for your language, and add the AWS CLI with the
     `ghcr.io/devcontainers/features/aws-cli:1` feature.
   - Credentials: bind-mount your host's `~/.aws` into the container's home
     directory so the SSO profile and token cache are shared. Or run
     `aws sso login --use-device-code` inside the container: the default
     browser sign-in expects a browser on the same machine as the CLI.
   - Never copy keys into the image or commit them to `.devcontainer/`.

1. **AWS CloudShell.** Open
   [CloudShell](https://docs.aws.amazon.com/cloudshell/latest/userguide/welcome.html)
   from the console while signed in through your AWS access portal, in
   `us-east-2`. The CLI is pre-installed and already signed in as your
   console identity. Your home directory keeps about 1 GB per region between
   sessions, and it's deleted after a long period without use (check the docs
   for the current limits). It suits quick checks, but it's a poor place for
   your only copy of anything.

##### Question 0.3.2

In CloudShell you didn't run `aws configure` or `aws sso login`. Where did
its credentials come from, and what happens to them when your console session
ends?

#### Lab 0.3.3: Clone the repository

Work with your GitHub repository in each environment you set up.

1. Install git if the environment doesn't already have it (CloudShell does).
1. Clone the repository. For SSH, you need a key in that environment. Where
   you can't use your laptop's key, use HTTPS with the
   [GitHub CLI](https://cli.github.com/) (`gh auth login`) or a
   [fine-grained personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
   limited to this one repository.
1. Think about what's left behind: a token or key stored in CloudShell's home
   directory stays there until you delete it.

### Retrospective 0.3

#### Question: Environments

*Running the same commands on your laptop, in a dev container and in
CloudShell should have shown the same results. What does that tell you about
the access each environment has? None of them used a long-lived access key.
Name the credential source in each case, and one more way to give access
without keys (hint: think about code running on EC2 or in a CI pipeline).*

#### Task

Set up your local environment (or dev container) with the programming
language you'll use for the course, then:

- Choose Python, Node.js, Go or Ruby
- Create a new branch off `main`
- In the `00-dev-environment` directory, write a small "hello world!"
  application in that language. If you built a dev container, commit its
  `.devcontainer/` too
- Add the files to your new branch, commit them, and push the branch to your
  repository
- Create a pull request from your branch to `main` within your own repository
  and merge after reviewing

#### Cleanup

Before you finish the module, check that:

- `aws iam list-users` no longer shows `<your-id>-mfa-lab`, and no profile in
  `~/.aws/credentials` holds an `AKIA...` key you don't need
- the test bucket from Lab 0.2.2 is gone
- `git grep -nE 'AKIA|ASIA|aws_secret_access_key'` in your repository finds
  nothing but placeholders
- any token or SSH key you created only for CloudShell has been deleted from
  its home directory and revoked in GitHub

Keep your IAM Identity Center setup and the budget; you need both for the
rest of the course.

## Further Reading

- [IAM Identity Center User Guide](https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html)
- [Security best practices in IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [Temporary security credentials in IAM](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp.html)
- [Configuration and credential file settings in the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html),
  including the order in which the CLI looks for credentials
- [Organizing Your AWS Environment Using Multiple Accounts](https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/organizing-your-aws-environment.html)
  (the whitepaper behind module 19)
- [How to migrate from AWS Cloud9 to AWS IDE Toolkits or AWS CloudShell](https://aws.amazon.com/blogs/devops/how-to-migrate-from-aws-cloud9-to-aws-ide-toolkits-or-aws-cloudshell/)
- [AWS Cost Management User Guide](https://docs.aws.amazon.com/cost-management/latest/userguide/what-is-costmanagement.html)
- [Best Practices for Tagging AWS Resources](https://docs.aws.amazon.com/whitepapers/latest/tagging-best-practices/tagging-best-practices.html)
- [aws-nuke (ekristen fork) documentation](https://aws-nuke.ekristen.dev/)
