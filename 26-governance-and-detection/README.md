# Topic 26: Governance and Detection

<!-- TOC -->

- [Topic 26: Governance and Detection](#topic-26-governance-and-detection)
  - [What changed in the 2026 edition](#what-changed-in-the-2026-edition)
  - [Exam coverage](#exam-coverage)
  - [Cost and cleanup](#cost-and-cleanup)
  - [Guidance](#guidance)
  - [Conventions](#conventions)
  - [Lesson 26.1: CloudTrail, the audit backbone](#lesson-261-cloudtrail-the-audit-backbone)
    - [Principle 26.1](#principle-261)
    - [Practice 26.1](#practice-261)
      - [Lab 26.1.1: Event history](#lab-2611-event-history)
      - [Lab 26.1.2: An organization trail](#lab-2612-an-organization-trail)
      - [Lab 26.1.3: Read and verify the logs](#lab-2613-read-and-verify-the-logs)
      - [Lab 26.1.4: Insights and Lake, on paper](#lab-2614-insights-and-lake-on-paper)
    - [Retrospective 26.1](#retrospective-261)
  - [Lesson 26.2: AWS Config](#lesson-262-aws-config)
    - [Principle 26.2](#principle-262)
    - [Practice 26.2](#practice-262)
      - [Lab 26.2.1: A recorder that records only what you need](#lab-2621-a-recorder-that-records-only-what-you-need)
      - [Lab 26.2.2: Managed rules](#lab-2622-managed-rules)
      - [Lab 26.2.3: A custom rule in Guard](#lab-2623-a-custom-rule-in-guard)
      - [Lab 26.2.4: Remediation with Systems Manager Automation](#lab-2624-remediation-with-systems-manager-automation)
      - [Lab 26.2.5: A conformance pack](#lab-2625-a-conformance-pack)
      - [Lab 26.2.6: An aggregator and advanced queries](#lab-2626-an-aggregator-and-advanced-queries)
    - [Retrospective 26.2](#retrospective-262)
  - [Lesson 26.3: Amazon GuardDuty](#lesson-263-amazon-guardduty)
    - [Principle 26.3](#principle-263)
    - [Practice 26.3](#practice-263)
      - [Lab 26.3.1: Turn on a detector](#lab-2631-turn-on-a-detector)
      - [Lab 26.3.2: Sample findings](#lab-2632-sample-findings)
      - [Lab 26.3.3: Route findings to a person](#lab-2633-route-findings-to-a-person)
      - [Lab 26.3.4: Suppression rules](#lab-2634-suppression-rules)
    - [Retrospective 26.3](#retrospective-263)
  - [Lesson 26.4: Amazon Inspector](#lesson-264-amazon-inspector)
    - [Principle 26.4](#principle-264)
    - [Practice 26.4](#practice-264)
      - [Lab 26.4.1: Activate Inspector for what you run](#lab-2641-activate-inspector-for-what-you-run)
      - [Lab 26.4.2: Scan a container image](#lab-2642-scan-a-container-image)
      - [Lab 26.4.3: Scan a Lambda function](#lab-2643-scan-a-lambda-function)
      - [Lab 26.4.4: EC2 scanning (optional)](#lab-2644-ec2-scanning-optional)
    - [Retrospective 26.4](#retrospective-264)
  - [Lesson 26.5: Security Hub and running it all from one place](#lesson-265-security-hub-and-running-it-all-from-one-place)
    - [Principle 26.5](#principle-265)
    - [Practice 26.5](#practice-265)
      - [Lab 26.5.1: Security Hub and Security Hub CSPM](#lab-2651-security-hub-and-security-hub-cspm)
      - [Lab 26.5.2: One queue of findings](#lab-2652-one-queue-of-findings)
      - [Lab 26.5.3: Delegated administrators for security services](#lab-2653-delegated-administrators-for-security-services)
      - [Lab 26.5.4: Clean up the module](#lab-2654-clean-up-the-module)
    - [Retrospective 26.5](#retrospective-265)
  - [Further Reading](#further-reading)

<!-- /TOC -->

## What changed in the 2026 edition

- **New module.** The 2022 course met CloudTrail once, in module 08, as a
  source of CloudWatch Logs events, and never taught AWS Config,
  GuardDuty, Security Hub or Inspector. All five are named in the CloudOps
  (SOA-C03), DevOps Pro (DOP-C02) and Security Specialty (SCS-C03) exam
  guides, and SCS-C03 tests them in almost every domain.
- **Security Hub is two products now.** At re:Inforce 2025 AWS previewed a
  new, unified *AWS Security Hub*, which became generally available in
  December 2025. The original product, which runs control checks against
  standards such as AWS Foundational Security Best Practices, was renamed
  **AWS Security Hub CSPM** (cloud security posture management). The new
  Security Hub correlates CSPM, GuardDuty, Inspector and Macie findings
  into *exposure findings*, uses the OCSF schema, and bills its Essentials
  plan per resource. Lesson 26.5 teaches both and how they fit together.
- **AWS Config can record daily instead of continuously** (since
  November 2023), and you can pick exactly which resource types to record. The
  labs use both, and show when daily recording saves money and when it
  costs more.
- **Custom Config rules in Guard.** Custom policy rules are written in
  CloudFormation Guard and need no Lambda function. The Lambda-based
  custom rule is still covered, as the option for checks Guard can't
  express.
- **GuardDuty has grown.** Extended Threat Detection (attack-sequence
  findings, no extra charge), Malware Protection for S3 and for AWS
  Backup, Runtime Monitoring, and AI Protection for Bedrock and SageMaker
  AI workloads. The labs use sample findings, so no attack simulation is
  needed.
- **Amazon Inspector** here is the current service (`inspector2`), which
  scans EC2, ECR images and Lambda functions continuously. Inspector
  Classic, with its agents and assessment templates, reached end of
  support on May 20, 2026. Older study material (and the DOP-C02 guide's
  "common assessment templates") still describes it.
- **CloudTrail Lake closed to new customers on May 31, 2026.** It is
  covered on paper only; AWS points new users at CloudWatch instead.
  Trails, Insights and aggregated events are unaffected.
- It builds on module 19: an **organization trail** from the management
  account, the baseline SCP that protects CloudTrail, and **delegated
  administrators** for the security services.

## Exam coverage

| Exam | Domain / task statement |
|---|---|
| SOA-C03 | Domain 4: Security and Compliance (Skill 4.1.2: audit access with CloudTrail; Skill 4.1.5: continuous monitoring with AWS Config conformance packs; Skill 4.2.5: configure reports and remediate findings from Security Hub, GuardDuty, AWS Config and Inspector) |
| SOA-C03 | Domain 3: Deployment, Provisioning, and Automation (Skill 3.2.1: automate operational processes with Systems Manager) |
| DOP-C02 | Domain 4: Monitoring and Logging (Task 4.2: Inspector, AWS Config rules, CloudTrail events; configuring AWS Config rules to remediate issues) |
| DOP-C02 | Domain 5: Incident and Event Response (Task 5.2: remediate a non-desired system state with AWS Config) |
| DOP-C02 | Domain 6: Security and Compliance (Task 6.2: security controls across accounts with Security Hub; Task 6.3: security monitoring and auditing) |
| SCS-C03 | Domain 1: Detection (Task 1.1: monitoring and alerting for an account or organization, including conformance packs and Security Hub; Task 1.2: logging, including an organization trail) |
| SCS-C03 | Domain 2: Incident Response (Skill 2.1.4: automatic remediation; Skill 2.2.3: validate findings from AWS security services) |
| SCS-C03 | Domain 6: Security Foundations and Governance (Skill 6.1.4: delegated administrator accounts; Skill 6.2.1: CloudFormation Guard; Task 6.3: evaluate compliance with AWS Config and Security Hub) |

## Cost and cleanup

This module turns on services that bill by volume, several of them with a
free trial that ends by itself. **Do Lessons 26.3 to 26.5 within two
weeks, then run [Lab 26.5.4](#lab-2654-clean-up-the-module) the same
day.** Nothing in this module should still be enabled a month from now.

- **AWS Config has no free trial.** You pay per configuration item (CI)
  recorded and per rule evaluation. At the time of writing, in US
  Regions: $0.003 per CI with continuous recording, $0.012 per CI with
  daily recording, and $0.001 per rule or conformance-pack evaluation for
  the first 100,000. Recording only two resource types in one Region, as
  Lab 26.2.1 does, keeps the module to cents. Recording *everything*,
  continuously, in every Region is how people get surprised. S3 storage
  for Config history is extra and tiny.
- **GuardDuty:** 30-day free trial per account and Region, covering the
  foundational detection and the protection plans it turns on by default.
  After that it bills by volume of events analyzed. Check the days left
  with `aws guardduty get-remaining-free-trial-days`.
- **Amazon Inspector:** **15-day** free trial (not 30) for EC2, ECR and
  Lambda scanning. Afterwards, for example, $0.09 per container image
  scanned and $0.30 per Lambda function per month. Check with
  `aws inspector2 batch-get-free-trial-info`.
- **Security Hub:** 30-day free trial of the Essentials plan per account
  and Region, even if you used Security Hub CSPM or Inspector trials
  before. After the trial the Essentials plan is billed per resource, and
  it absorbs the billing for Security Hub CSPM checks and the Inspector
  scanning it covers. **Security Hub CSPM** on its own also has a 30-day
  trial, then bills per security check.
- **CloudTrail:** Event history is free. The first copy of management
  events delivered by a trail is free in each Region; a second trail
  logging the same events costs $2.00 per 100,000 events. Data events,
  network activity events and Insights are extra and are not turned on
  in this module. You pay for the S3 storage of the log files.
- **Small charges:** an ECR repository with a couple of images, one
  Lambda function, SNS email, Systems Manager Automation runs for
  remediation (well inside the free tier for a handful of runs), and an
  optional EC2 instance in Lab 26.4.4 (hourly).
- **Cleanup:** [Lab 26.5.4](#lab-2654-clean-up-the-module) disables every
  service this module enabled, in both accounts, and checks that nothing
  is left: Security Hub, Security Hub CSPM, Inspector, GuardDuty, the
  Config rules, remediations, conformance pack, aggregator and recorder,
  the organization trail and their buckets. It also covers what services
  create for you, such as service-linked recorders.

<!-- VERIFY: prices above were read from the AWS pricing pages in
September 2026 (us-east-1 figures); check the us-east-2 figures when you
run the labs. -->

## Guidance

- Explore the official docs! See the
  [AWS CloudTrail User Guide](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html),
  [AWS Config Developer Guide](https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html),
  [Amazon GuardDuty User Guide](https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html),
  [Amazon Inspector User Guide](https://docs.aws.amazon.com/inspector/latest/user/what-is-inspector.html)
  and
  [AWS Security Hub User Guide](https://docs.aws.amazon.com/securityhub/latest/userguide/what-is-securityhub-v2.html),
  and the CLI references for
  [cloudtrail](https://docs.aws.amazon.com/cli/latest/reference/cloudtrail/),
  [configservice](https://docs.aws.amazon.com/cli/latest/reference/configservice/),
  [guardduty](https://docs.aws.amazon.com/cli/latest/reference/guardduty/),
  [inspector2](https://docs.aws.amazon.com/cli/latest/reference/inspector2/)
  and
  [securityhub](https://docs.aws.amazon.com/cli/latest/reference/securityhub/).

- Read the
  [AWS Security Reference Architecture](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/welcome.html)
  (AWS SRA) overview. It shows where each of these services lives in a
  real organization: which account owns the trail bucket, which is the
  delegated administrator, and why. The exams lean on it.

- Avoid using other sites like stackoverflow.com for answers \-- part
  of the skill set you're building is finding answers straight from
  the source, AWS.

- Explore your curiosity. Try to understand why things work the way
  they do. Read more of the documentation than just what you need to
  find the answers.

## Conventions

- **Profiles and Region.** Everything runs in the lab account with the
  `lab` profile and Region `us-east-2`, as set up in module 19, except
  where a lab says to use `mgmt` (the organization trail in Lesson 26.1,
  and the read-only organization commands in Lab 26.5.3). Don't pass
  `--region` unless the lab is about Regions.
- **Placeholders.** Examples follow module 19: `444455556666` for the management
  account, `111122223333` for the lab account and `o-exampleorgid` for the
  organization. Keep real account IDs,
  organization IDs and email addresses out of your repository; write
  `<lab-account-id>` in your answers.
- **One Region.** Enable each service in `us-east-2` only. In a real
  organization you'd enable detective services in every enabled Region;
  Retrospective 26.5 asks you how.
- **Names and tags** include your identifier. Tag everything you create
  with `owner` and `topic=26`, so Lab 26.5.4 can find it.
- DO use the AWS CLI and CloudFormation rather than the console, except
  where a step says the console is needed.

## Lesson 26.1: CloudTrail, the audit backbone

### Principle 26.1

*Every other service in this module answers "what is wrong?". CloudTrail
answers "who did it, when, from where", so it has to be on, complete and
out of reach of the people it records.*

### Practice 26.1

CloudTrail records API calls. Without doing anything, every account keeps
90 days of management events in **Event history**. A **trail** delivers
events to S3 (and optionally CloudWatch Logs) for as long as you keep
them. An **organization trail**, created in the management account or by a
CloudTrail delegated administrator, logs every account in the
organization to one bucket, and member accounts can see it but can't stop
or change it.

Module 08 had you build a single-account trail with CloudFormation. Here
you replace that idea with the multi-account pattern the exams expect.

#### Lab 26.1.1: Event history

With the `lab` profile:

- Use
  [`aws cloudtrail lookup-events`](https://docs.aws.amazon.com/cli/latest/reference/cloudtrail/lookup-events.html)
  to find the `ConsoleLogin` or `GetRoleCredentials` events from your
  most recent sign-in, then the events for something you created in
  another module, such as `CreateBucket`.

- Find the `userIdentity` block in one event and identify the
  Identity Center role and the session name.

- Try the same lookup with `--region us-east-1`. Why are some events
  only there?

##### Question: What Event history leaves out

_Read
[Working with CloudTrail event history](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/view-cloudtrail-events.html).
What kinds of events never appear in Event history? How long does it keep
what it does record? What does that mean for an incident you discover
four months later?_

#### Lab 26.1.2: An organization trail

This lab runs in the **management account** with the `mgmt` profile.
Module 19 asked you to keep that account empty, and in a real
organization the bucket would live in a dedicated *log archive* account.
For a solo learner with one lab account, the management account is the
only place that isn't wiped by aws-nuke, so it holds the trail and its
bucket for this module.

- Read [Creating a trail for an
  organization](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/creating-trail-organization.html)
  and its "Prepare for creating a trail for your organization" page.
  Enable trusted access for CloudTrail if it isn't already.

- In `us-east-2`, create an S3 bucket named with your identifier for the
  trail. Write its bucket policy from [Amazon S3 bucket policy for
  CloudTrail](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/create-s3-bucket-policy-for-cloudtrail.html),
  including the statement for organization trails, and scope it with
  `aws:SourceArn`. A CloudFormation template in the management account is
  fine; so is the CLI.

- Create a **multi-Region organization trail** with log file validation
  turned on, management events only (read and write), and no data
  events. Start logging.

- With the `lab` profile, run `aws cloudtrail describe-trails` and
  `get-trail-status` on the organization trail. Then try
  `aws cloudtrail stop-logging` on it.

*If you still have a trail in the lab account from module 08, the
organization trail is a second copy of the same management events and
the lab account pays for it. Delete the old one from its stack. Module
19's baseline SCP denies `DeleteTrail` in the lab account, so you'll need
the exemption you designed in Lab 19.2.3, or delete it from the
management account side.*
<!-- VERIFY: whether a member account's own (non-organization) trail can
be deleted by the management account, or only through a role in the
member account. -->

##### Question: Two reasons it can't be stopped

_Your `stop-logging` call from the lab account failed. Name both things
that stop it: one is a property of organization trails, the other is
something you built in module 19. Which of the two would still protect the
trail if someone removed the SCP?_

##### Question: Why multi-Region

_The labs only use `us-east-2`. Why is the trail still multi-Region? What
kinds of events does a Region you never use record, and why would an
attacker like that Region?_

#### Lab 26.1.3: Read and verify the logs

- Wait 15 minutes, then list the bucket. Describe the key structure: where
  do the organization ID, the account ID, the Region and the date appear?

- Download one log file from the lab account's prefix, decompress it and
  find an event you caused with the `lab` profile.

- Run
  [`aws cloudtrail validate-logs`](https://docs.aws.amazon.com/cli/latest/reference/cloudtrail/validate-logs.html)
  for the last hour. Then read [Validating CloudTrail log file
  integrity](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-log-file-validation-intro.html)
  and explain what a digest file proves.

##### Question: Protecting the bucket

_Log file validation tells you a file was changed; it doesn't stop the
change. What would you add to the trail bucket so that nobody, including
an administrator in the management account, can delete or overwrite log
files for a year? (Think S3 Object Lock, versioning, MFA delete, and
where the bucket lives.)_

#### Lab 26.1.4: Insights and Lake, on paper

Don't turn either of these on. Read and answer.

- [Working with CloudTrail
  Insights](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/logging-insights-events-with-cloudtrail.html):
  Insights learns a baseline of API call volume and error rates and
  records an Insights event when activity departs from it. It is billed
  per 100,000 events analyzed.
- [CloudTrail Lake](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-lake.html)
  and its [availability
  change](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-lake-service-availability-change.html):
  a managed event data store you query with SQL. Since May 31, 2026 it
  isn't open to new customers.

##### Question: Which tool for which question

_For each question, say whether you'd use Event history, a trail plus
Athena, CloudTrail Insights, or an EventBridge rule, and why: (a) who
deleted this security group yesterday? (b) alert me within minutes when
anyone calls `StopLogging`; (c) a role that normally makes 20
`AssumeRole` calls an hour made 4,000; (d) every `PutObject` on one
bucket over the last year._

### Retrospective 26.1

#### Question: What CloudTrail can't tell you

_CloudTrail records the API call to change a security group. It doesn't
record the SSH session that then used the open port, nor the data an
application read from a database. Which logs would you need for each,
and which of them does GuardDuty (Lesson 26.3) read without you turning
them on?_

## Lesson 26.2: AWS Config

### Principle 26.2

*AWS Config keeps a history of how each resource is configured and
judges it against rules, so compliance becomes something you can query
and fix automatically, not something you audit once a year.*

### Practice 26.2

AWS Config has three layers. The **configuration recorder** writes a
configuration item (CI) whenever a recorded resource changes, or once a
day. **Rules** evaluate those CIs, or run on a schedule, and mark each
resource `COMPLIANT` or `NON_COMPLIANT`. **Remediation** runs a Systems
Manager Automation runbook against non-compliant resources. On top of
that, **conformance packs** bundle rules and remediations into one
deployable unit, and **aggregators** give one account a read-only view
of many accounts and Regions.

Everything in this lesson is aimed at S3 buckets, because they're free
to create and easy to break on purpose. Read [How AWS Config
works](https://docs.aws.amazon.com/config/latest/developerguide/how-does-config-work.html)
before you start.

#### Lab 26.2.1: A recorder that records only what you need

Read [Recording AWS resources with AWS
Config](https://docs.aws.amazon.com/config/latest/developerguide/select-resources.html),
especially *Recording frequency*, and the [AWS Config
pricing](https://aws.amazon.com/config/pricing/) page. Then:

- Check whether the lab account already has a recorder:
  `aws configservice describe-configuration-recorders`. There can be only
  one *customer managed* recorder per Region. If you find one from an
  earlier experiment, decide whether to reuse it or delete it.

- Create the AWS Config service-linked role if it doesn't exist.

- Complete [starter/config-recorder.yaml](starter/config-recorder.yaml):
  - record only `AWS::S3::Bucket` and `AWS::EC2::SecurityGroup`, and no
    global resource types;
  - set the default recording frequency to **daily**, with an override
    that records `AWS::S3::Bucket` **continuously** (the labs that
    follow need bucket changes to show up in minutes, not tomorrow);
  - add the delivery channel.

  See
  [AWS::Config::ConfigurationRecorder](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-config-configurationrecorder.html)
  and
  [AWS::Config::DeliveryChannel](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-config-deliverychannel.html).
  Run `cfn-lint`, then deploy.

- Confirm with `describe-configuration-recorder-status` that it is
  recording, and with `describe-configuration-recorders` that the
  frequency and overrides are what you meant.

- Create a test bucket (with a stack, tagged, named with your
  identifier) and find its CI with `get-resource-config-history`.

##### Question: Is daily cheaper?

_Daily recording costs four times as much per CI as continuous recording.
When does it save money, and when does it cost more? For each of these,
pick a frequency: an Auto Scaling group's security groups that change
twenty times a day; the three S3 buckets you create in this module; IAM
roles in an organization with a nightly deployment._

##### Question: Recording scope

_Why record only two types instead of "all resource types"? Read the
section on global resource types: why should an organization record IAM
resources in one Region only, and what goes wrong for periodic IAM rules
if you record them nowhere?_

#### Lab 26.2.2: Managed rules

AWS provides hundreds of [managed
rules](https://docs.aws.amazon.com/config/latest/developerguide/managed-rules-by-aws-config.html).
Add two with the CLI (`put-config-rule`), scoped to `AWS::S3::Bucket`:

- [`s3-bucket-versioning-enabled`](https://docs.aws.amazon.com/config/latest/developerguide/s3-bucket-versioning-enabled.html)
- [`s3-bucket-level-public-access-prohibited`](https://docs.aws.amazon.com/config/latest/developerguide/s3-bucket-level-public-access-prohibited.html)

Your test bucket from Lab 26.2.1 doesn't have versioning, so it should
fail the first rule.

- Use `start-config-rules-evaluation`, then
  `describe-compliance-by-config-rule` and
  `get-compliance-details-by-config-rule` to see the result per
  resource.

- Turn versioning on for the test bucket through its stack, wait a few
  minutes, and check again.

##### Question: Trigger types

_Each managed rule has a trigger type: configuration changes, periodic,
or both. Which does each of your two rules use? What happens to a
change-triggered rule for a resource type the recorder doesn't record?_

##### Question: Detective and proactive

_Some rules support **proactive** evaluation, which checks a resource
configuration before it's deployed. Read [Evaluation
modes](https://docs.aws.amazon.com/config/latest/developerguide/evaluate-config-rules.html).
How does that overlap with CloudFormation Hooks and with the Guard checks
you could run in a pipeline? Where would you put each?_

#### Lab 26.2.3: A custom rule in Guard

When no managed rule fits, a **custom policy rule** lets you write the
check in [CloudFormation
Guard](https://docs.aws.amazon.com/cfn-guard/latest/ug/what-is-guard.html).
Guard rules run on AWS Config's side, and you don't deploy a function.

Write a rule that marks an S3 bucket `NON_COMPLIANT` unless it has an
`owner` tag with a non-empty value.

- Read [Creating AWS Config Custom Policy
  rules](https://docs.aws.amazon.com/config/latest/developerguide/evaluate-config_develop-rules_cfn-guard.html).
- Look at your test bucket's CI (`get-resource-config-history`) to find
  where tags live in a configuration item. The Guard rule evaluates the
  CI, not the CloudFormation template.
- Keep the rule in your repository as `config/require-owner-tag.guard`.
  If you have the `cfn-guard` CLI, test it locally against the CI JSON
  you saved.
- Create it with `put-config-rule`, owner `CUSTOM_POLICY`, runtime
  `guard-2.x.x`, triggered by configuration changes to
  `AWS::S3::Bucket`.
- Positive test: your tagged test bucket is `COMPLIANT`. Negative test:
  create a second bucket without the tag.

*Optional stretch: write the same check as a **Lambda-backed custom
rule** in Python 3.13 (see [Creating custom Lambda
rules](https://docs.aws.amazon.com/config/latest/developerguide/evaluate-config_develop-rules_lambda-functions.html)).
Compare the amount of code, the permissions involved and what you pay
for.*

##### Question: Guard or Lambda

_Give one check that Guard can't express and a Lambda rule can. (Hint:
Guard sees only the one configuration item.) What does a Lambda rule cost
you in operations that a Guard rule doesn't?_

#### Lab 26.2.4: Remediation with Systems Manager Automation

Config can run an [SSM Automation
runbook](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-automation.html)
against a non-compliant resource, by hand or automatically. Read
[Remediating noncompliant
resources](https://docs.aws.amazon.com/config/latest/developerguide/remediation.html)
and [Setting up auto
remediation](https://docs.aws.amazon.com/config/latest/developerguide/setup-autoremediation.html).

- Read the AWS-owned runbook
  [AWS-ConfigureS3BucketVersioning](https://docs.aws.amazon.com/systems-manager-automation-runbooks/latest/userguide/automation-aws-configures3bucketversioning.html).
  Note its parameters, including `AutomationAssumeRole`.

- Create an IAM role for the runbook to assume: trusted by
  `ssm.amazonaws.com`, allowed only `s3:PutBucketVersioning` and
  `s3:GetBucketVersioning` on buckets whose names start with your
  identifier. Validate the policy with Access Analyzer (Lab 3.3.4).

- Attach a **manual** remediation to `s3-bucket-versioning-enabled` with
  `put-remediation-configurations`. Pass the bucket name as the resource
  ID parameter and the role ARN as a static value.

- Create a third bucket without versioning, wait for it to show as
  non-compliant, and run `start-remediation-execution`. Follow it with
  `describe-remediation-execution-status` and in the Automation
  execution history.

- Change the configuration to **automatic**, with a small retry limit,
  and repeat with a fourth bucket.

##### Question: Remediation and drift

_Your third and fourth buckets came from CloudFormation stacks that said
nothing about versioning. Config changed them. Run drift detection on
one of those stacks. What does it report, and what happens to versioning
the next time someone updates the stack? How would you fix this for good?_

##### Question: Automatic remediation risks

_The docs warn that automatic remediation can run against a resource
that is already compliant. Why? Name a remediation you'd never make
automatic, and one you'd happily make automatic._

#### Lab 26.2.5: A conformance pack

A [conformance
pack](https://docs.aws.amazon.com/config/latest/developerguide/conformance-packs.html)
is a YAML template of Config rules and remediations deployed as one
unit, and it reports a compliance score.

- Read a few of the [sample conformance pack
  templates](https://docs.aws.amazon.com/config/latest/developerguide/conformance-pack-sample-templates.html),
  such as *Operational Best Practices for Amazon S3*. Count the rules in
  it. What would it cost to evaluate your buckets against all of them?

- Write your own small pack, `config/s3-baseline-pack.yaml`, with
  `s3-bucket-versioning-enabled` (with its remediation) and your Guard
  rule. Keep the rule names different from the ones you created by hand
  in Labs 26.2.2 and 26.2.3.

- Deploy it with `put-conformance-pack`, then look at
  `describe-conformance-pack-compliance` and
  `get-conformance-pack-compliance-score`.

- Delete the stand-alone rules from Labs 26.2.2 and 26.2.3 (remove the
  remediation configuration first). The pack now owns those checks.

##### Question: Conformance pack or stack

_A conformance pack template looks like CloudFormation. What's different
about deploying it as a pack instead of as a stack of
`AWS::Config::ConfigRule` resources? What does an organization
conformance pack add, and which account can deploy one?_

#### Lab 26.2.6: An aggregator and advanced queries

An
[aggregator](https://docs.aws.amazon.com/config/latest/developerguide/aggregate-data.html)
collects Config data from several accounts and Regions into one
read-only view, at no extra charge.

- In the lab account, create an aggregator (`put-configuration-aggregator`)
  whose source is the lab account in `us-east-2` and `us-east-1`. Config
  isn't enabled in `us-east-1`: look at
  `describe-configuration-aggregator-sources-status` and explain what it
  reports.

- Run an [advanced
  query](https://docs.aws.amazon.com/config/latest/developerguide/querying-AWS-resources.html)
  against your own account with `select-resource-config`, then against
  the aggregator with `select-aggregate-resource-config`: list every
  S3 bucket with its versioning status and `owner` tag.

##### Question: Organization aggregator

_An organization aggregator needs no per-account authorization. Which
account can create one, and what do you have to register in AWS
Organizations to create it from a Security Tooling account instead of
the management account? (Read [Registering a delegated administrator
for AWS
Config](https://docs.aws.amazon.com/config/latest/developerguide/aggregated-register-delegated-administrator.html):
there are two service principals, and they do different jobs.)_

### Retrospective 26.2

#### Question: Preventive and detective

_Module 19 gave you SCPs, which stop an action before it happens. AWS
Config tells you afterwards. For "no S3 bucket may be public", which
controls would you use at each layer: organization policy, account
setting, proactive check in the pipeline, detective rule, remediation?
Which of them could you skip?_

#### Task: Rules as code

_You created rules by CLI, by conformance pack and (optionally) as a
Lambda function. Move the rules you'd keep into one version-controlled
place and write down how a change to a rule gets reviewed and deployed._

## Lesson 26.3: Amazon GuardDuty

### Principle 26.3

*GuardDuty watches the logs you already have for signs of attack, and it
takes one API call to turn on. The work is in routing its findings to
someone and in quieting the ones you've decided don't matter.*

### Practice 26.3

GuardDuty analyzes CloudTrail management events, VPC Flow Logs and DNS
logs, which AWS reads for it without you turning them on. Protection
plans add more sources: S3 data events, EKS audit logs, runtime agents,
RDS login activity, Lambda network activity, malware scans and AI
workloads. Findings have a type such as
`UnauthorizedAccess:IAMUser/InstanceCredentialExfiltration.OutsideAWS`, a
severity, and the resource involved. Extended Threat Detection correlates
findings over time into *attack sequence* findings.

Your lab account has no attacker, so these labs use **sample findings**.
Read [What is Amazon
GuardDuty?](https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html)
first.

#### Lab 26.3.1: Turn on a detector

- With the CLI, create a detector in `us-east-2`
  ([`create-detector`](https://docs.aws.amazon.com/cli/latest/reference/guardduty/create-detector.html)),
  tagged with your identifier.

- Use `get-detector` to list which features (protection plans) are on.
  Compare with the [free trial
  notes](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty-pricing.html):
  which plans did GuardDuty turn on for you, and which one is left off?

- Run `get-remaining-free-trial-days`. Put the date the trial ends in
  your calendar, a few days early.

##### Question: Plans you don't need

_Your lab account has no EKS clusters, RDS databases or Bedrock usage.
Does leaving those plans on cost anything after the trial? Would you
leave them on in a real account that has none of those resources today?_

#### Lab 26.3.2: Sample findings

- Read [Generating sample
  findings](https://docs.aws.amazon.com/guardduty/latest/ug/sample_findings.html)
  and the list of [finding
  types](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_finding-types-active.html).

- Generate three specific sample findings with `create-sample-findings`:
  one EC2 finding, one IAM finding and one S3 finding, each of a
  different severity.

- `list-findings` and `get-findings`. For each, record the type, severity,
  resource and the field that marks it as a sample.

##### Question: Reading a finding type

_Break down one finding type into its parts (threat purpose, resource
type, threat family, detection mechanism). What would you do first if the
IAM finding you generated were real?_

#### Lab 26.3.3: Route findings to a person

GuardDuty sends every finding to EventBridge. Nothing reaches a person
unless you build that.

- Read [Processing GuardDuty findings with
  EventBridge](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_findings_eventbridge.html),
  including the notification frequency section.

- Write a CloudFormation template, `guardduty-alerts.yaml`, with an SNS
  topic, an email subscription (the address as a parameter, never in the
  file), a topic policy that lets EventBridge publish, and an EventBridge
  rule that matches GuardDuty findings with severity 7 or higher. Use an
  EventBridge [numeric
  matching](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-create-pattern-operators.html)
  pattern, not a list of every value, and an input transformer that turns
  the finding into a readable message.

- Generate a high-severity and a low-severity sample finding. Only one
  should reach your inbox.

##### Question: New and repeated findings

_A finding that keeps happening doesn't send a new event each time. How
often are repeat occurrences sent, and who can change that?_

#### Lab 26.3.4: Suppression rules

- Read [Suppression rules in
  GuardDuty](https://docs.aws.amazon.com/guardduty/latest/ug/findings_suppression-rule.html).

- Create a suppression rule
  ([`create-filter`](https://docs.aws.amazon.com/cli/latest/reference/guardduty/create-filter.html)
  with the `ARCHIVE` action) for one high-severity finding type from your
  samples, narrowed with a second criterion such as a resource tag.

- Generate that sample finding again. Confirm it's archived, and that no
  email arrived.

##### Question: The cost of silence

_Suppressed findings aren't sent to EventBridge or Security Hub, and
Extended Threat Detection ignores them when it builds attack sequences.
Why does AWS recommend narrow, reactive suppression rules? Write the
suppression rule you'd use for a vulnerability scanner that port-scans
your own instances every night._

### Retrospective 26.3

#### Question: Credentials leaked from an instance

_GuardDuty reports that credentials from an EC2 instance role are being
used from an IP address outside AWS. Walk through containment, starting
from the finding: what do you revoke, where, and what evidence do you
keep before you change anything? Which AWS runbooks or SSM Automation
documents exist for this?_

## Lesson 26.4: Amazon Inspector

### Principle 26.4

*Inspector finds the known vulnerabilities in what you run, continuously,
so patching becomes a queue ordered by risk instead of a guess.*

### Practice 26.4

Amazon Inspector scans EC2 instances (with the SSM Agent, or agentless
from EBS snapshots), container images in ECR, and Lambda functions
(package dependencies, and optionally your code). It re-scans when a
new CVE is published, not only when your software changes, and it scores
each finding with network reachability and exploitability in mind.

The free trial is **15 days**, shorter than the others. Do this lesson
in one sitting if you can. Read [What is Amazon
Inspector?](https://docs.aws.amazon.com/inspector/latest/user/what-is-inspector.html)
first.

#### Lab 26.4.1: Activate Inspector for what you run

- Activate Inspector for ECR and Lambda standard scanning only:
  [`aws inspector2 enable`](https://docs.aws.amazon.com/cli/latest/reference/inspector2/enable.html)
  with `--resource-types`. Leave EC2, Lambda code scanning and code
  repositories off for now.

- Check `batch-get-account-status` and `batch-get-free-trial-info`.

- Look at the ECR registry scanning configuration
  (`aws ecr get-registry-scanning-configuration`). What changed when
  Inspector took over?

##### Question: Basic and enhanced

_ECR has its own free *basic* scanning. What does Inspector's *enhanced*
scanning add? When would basic scanning be enough?_

#### Lab 26.4.2: Scan a container image

- Create an ECR repository named with your identifier, tagged, with image
  tag immutability on.

- Build a small image from an old base image, for example an
  end-of-life Python or Debian release pulled from the
  [ECR Public Gallery](https://gallery.ecr.aws/), and push it. Push a
  second image built on a current base.

- Use `list-coverage` to confirm both images are covered, then
  `list-findings` filtered to the repository. Compare the counts, look at
  one critical finding in detail, and note the Inspector score, the
  fixed-in version and whether an exploit is known.

- Read [Scanning Amazon ECR container
  images](https://docs.aws.amazon.com/inspector/latest/user/scanning-ecr.html)
  and find the re-scan duration setting. What is it set to?

##### Question: Rebuild, don't patch

_The fix for most of the old image's findings is a newer base image, not
a change to your code. Where in a pipeline (module 12 or 13) would you
stop an image with critical findings from being deployed, and what would
you do about images that are already running?_

#### Lab 26.4.3: Scan a Lambda function

- Package a small Python 3.13 Lambda function with one deliberately
  outdated dependency pinned in `requirements.txt` (pick a version of a
  popular library with a published CVE). Deploy it with a stack, named
  and tagged with your identifier.

- Wait for coverage, then list the function's findings. Upgrade the
  dependency, redeploy, and watch the finding close.

- Read [Scanning Lambda
  functions](https://docs.aws.amazon.com/inspector/latest/user/scanning-lambda.html).
  What would Lambda **code** scanning add, and what does it cost per
  function per month?

##### Question: Suppress or fix

_Inspector supports suppression rules too (`create-filter` with the
`SUPPRESS` action). Describe a vulnerability you'd suppress rather than
fix, and the evidence you'd want recorded when you do._

#### Lab 26.4.4: EC2 scanning (optional)

*This costs an EC2 instance for as long as it runs.* Enable EC2 scanning,
launch one Amazon Linux 2023 `t4g.nano` or `t3.micro` instance from the
SSM public parameter with an instance profile that allows Session
Manager, and no inbound rules. Read [Scanning Amazon EC2
instances](https://docs.aws.amazon.com/inspector/latest/user/scanning-ec2.html)
and find out whether your instance is scanned agent-based or agentless,
and why. Terminate it when you have its findings.

### Retrospective 26.4

#### Question: Vulnerability or misconfiguration

_Inspector reports a vulnerable package. Security Hub CSPM reports a
security group open to the world. GuardDuty reports a port scan. Which of
these is a vulnerability, which a misconfiguration and which a threat?
Why is the combination of the first two worse than either alone? (Lesson
26.5 comes back to this.)_

## Lesson 26.5: Security Hub and running it all from one place

### Principle 26.5

*Security Hub is where the findings meet: it checks posture, collects
what the detectors report, and correlates them, so one queue shows what
to fix first. It only works if someone owns that queue.*

### Practice 26.5

Since December 2025 there are two related products:

- **AWS Security Hub CSPM** is the original Security Hub. It runs
  **controls** grouped into **standards** (AWS Foundational Security Best
  Practices, CIS AWS Foundations Benchmark, NIST SP 800-53, PCI DSS),
  mostly through AWS Config rules it manages for you, and collects
  findings in the AWS Security Finding Format (ASFF).
- **AWS Security Hub** is the new, unified service. It takes signals
  from Security Hub CSPM, GuardDuty, Inspector, Macie and IAM Access
  Analyzer in the OCSF format, correlates them into **exposure findings**
  (for example, an internet-reachable instance with an exploitable
  vulnerability), draws attack paths, and adds unused-access findings.
  Its Essentials plan is billed per resource and includes the CSPM checks
  and the Inspector scanning it covers.

The two are enabled separately, and each has its own CLI commands in the
`securityhub` namespace: the CSPM commands are the original ones, and the
new service's commands end in `-v2`. Read [Introduction to AWS Security
Hub](https://docs.aws.amazon.com/securityhub/latest/userguide/what-is-securityhub-v2.html)
and [Introduction to AWS Security Hub
CSPM](https://docs.aws.amazon.com/securityhub/latest/userguide/what-is-securityhub.html)
before you start.

#### Lab 26.5.1: Security Hub and Security Hub CSPM

- Enable **Security Hub** in the lab account in `us-east-2` only. The
  CLI command is `aws securityhub enable-security-hub-v2`; the console
  ([Enabling Security
  Hub](https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-v2-enable.html))
  shows which capabilities are included, and lets you pick Regions and
  capabilities in one place. Either is fine; say which you used and why.
  <!-- VERIFY: that a member account of an organization with no Security
  Hub delegated administrator can enable Security Hub for itself, and
  which capabilities enable-security-hub-v2 turns on compared with the
  console's "Customize capabilities" path. -->

- Enable **Security Hub CSPM** with only the AWS Foundational Security
  Best Practices standard (`enable-security-hub` without default
  standards, then `batch-enable-standards`).

- Now look at what those two calls created in your account:
  - `aws configservice describe-configuration-recorders`: you should see
    service-linked recorders next to your own. Which Regions are they in?
  - `aws accessanalyzer list-analyzers`, in `us-east-1` too.
  - `aws configservice describe-config-rules`: the `securityhub-` rules.
  - `aws securityhub list-free-trial-statuses-v2`.

- Read [Enabling and configuring AWS Config for Security Hub
  CSPM](https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-setup-prereqs.html).
  Which recorder do the CSPM controls use now, yours or the
  service-linked one?

##### Question: Two recorders

_Your recorder from Lab 26.2.1 records two types, daily by default. The
service-linked recorders record what Security Hub needs. Who pays for
the CIs each of them records? What would have gone wrong if you had
enabled only Security Hub CSPM, with your limited recorder, and no
Security Hub?_

##### Question: Region you didn't pick

_You enabled Security Hub in `us-east-2` only, but something appeared in
`us-east-1`. Why there? What would module 19's region guardrail have
done if it had denied `us-east-1`?_

#### Lab 26.5.2: One queue of findings

- After an hour or so, list findings with `get-findings-v2`. Find the
  GuardDuty sample findings from Lesson 26.3, the Inspector findings from
  Lesson 26.4, and at least one failed CSPM control. For each, note the
  field that tells you which service produced it.

- List CSPM control results for the S3 controls with
  `get-findings` (the ASFF API). Does any of them duplicate one of your
  own Config rules from Lesson 26.2?

- Look for exposure findings with `get-findings-v2`. You may have none.
  Using the definition of an exposure finding and its *traits*, describe
  what you'd have to deploy for one to appear.

- Create one [automation
  rule](https://docs.aws.amazon.com/securityhub/latest/userguide/automation-rules-v2.html)
  with `create-automation-rule-v2` that sets GuardDuty sample findings to
  a low severity or suppresses them, so they don't clutter the queue.
  <!-- VERIFY: the automation rule criteria field names for OCSF
  findings, and whether GuardDuty sample findings are flagged in a field
  a rule can match. -->

##### Question: Where to suppress

_You can quiet a finding in GuardDuty (suppression rule), in Inspector
(suppression rule), in Security Hub CSPM (disable a control) or in
Security Hub (automation rule). For each, what else stops seeing the
finding? Which would you choose for a control that doesn't apply to your
organization, and which for one noisy resource?_

#### Lab 26.5.3: Delegated administrators for security services

In a real organization none of this is enabled account by account. The
management account registers a **delegated administrator** (usually a
*Security Tooling* or *Audit* account), and that account turns the
services on for every member account and Region and sees every finding.
Module 19 told you not to make your sandbox lab account an
administrator, because aws-nuke wipes it. Keep that rule: this lab is
read-only.

- With the `mgmt` profile, list the services with trusted access
  (`aws organizations list-aws-service-access-for-organization`) and the
  delegated administrators (`list-delegated-administrators`). Which of
  the services in this module appear, and why?

- For each service, find the command or console step that registers a
  delegated administrator and the service principal involved. Fill in a
  table in your answers:

  | Service | Registration command | Service principal | Can the management account be the administrator? |
  |---|---|---|---|
  | CloudTrail | | | |
  | AWS Config (rules and packs) | | | |
  | AWS Config (aggregation) | | | |
  | GuardDuty | | | |
  | Inspector | | | |
  | Security Hub / CSPM | | | |

  Start from
  [`register-organization-delegated-admin`](https://docs.aws.amazon.com/cli/latest/reference/cloudtrail/register-organization-delegated-admin.html),
  [Registering a delegated administrator for AWS
  Config](https://docs.aws.amazon.com/config/latest/developerguide/aggregated-register-delegated-administrator.html),
  [`enable-organization-admin-account`](https://docs.aws.amazon.com/cli/latest/reference/guardduty/enable-organization-admin-account.html),
  [`enable-delegated-admin-account`](https://docs.aws.amazon.com/cli/latest/reference/inspector2/enable-delegated-admin-account.html)
  and [Designating a delegated administrator account in Security
  Hub](https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-v2-set-da.html).

- Read the AWS SRA pages on the [Security Tooling
  account](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/security-tooling.html)
  and the [Log Archive
  account](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/log-archive.html).

##### Question: Same administrator everywhere

_The Security Hub and Inspector docs both recommend using the same
delegated administrator for every security service. Why? What breaks,
or gets confusing, if GuardDuty is administered from one account and
Security Hub from another?_

##### Question: Central configuration

_With a delegated administrator, how would you make sure a new account
in the `Workloads` OU gets GuardDuty, Inspector and Security Hub in every
enabled Region on the day it's created, without anyone running a
command? Compare the services' own organization configuration with
Control Tower (Lab 19.3.3)._

#### Lab 26.5.4: Clean up the module

Undo everything in the reverse order you turned it on. Don't rely on
aws-nuke for this: several of these are account settings, not resources.

- **Security Hub** (`lab`): delete your automation rule, then disable
  Security Hub (`disable-security-hub-v2`) and Security Hub CSPM
  (`disable-security-hub`). Confirm with `describe-security-hub-v2`
  and `describe-hub` that both are off.

- **Inspector** (`lab`): `aws inspector2 disable` with every resource
  type you enabled, including EC2 if you did Lab 26.4.4. Confirm with
  `batch-get-account-status`. Delete the Lambda function stack, the ECR
  repository and its images, and terminate the EC2 instance.

- **GuardDuty** (`lab`): delete the suppression rule and the
  `guardduty-alerts` stack, then delete the detector. Confirm
  `list-detectors` is empty.

- **AWS Config** (`lab`): delete the conformance pack, any remaining
  remediation configurations and rules, and the aggregator. Delete the
  test bucket stacks. Empty the Config bucket, then delete the recorder
  stack, which stops and removes the recorder and delivery channel.
  Delete the remediation role.

- **Check for leftovers** in `us-east-2` **and** `us-east-1`:
  - `aws configservice describe-configuration-recorders` returns no
    recorders, including the service-linked ones. If a service-linked
    recorder remains, find out which service owns it and why.
  - `aws configservice describe-config-rules` returns nothing.
  - `aws accessanalyzer list-analyzers` shows no Security Hub analyzer.

- **Organization trail** (`mgmt`): stop logging, delete the trail, empty
  and delete its bucket. If you'd rather keep a trail as the permanent
  audit record for your lab account, you may, as long as you can say why
  and what it costs; if you do, add S3 Object Lock and a lifecycle rule,
  and write it down in your answers.

- Check the free-trial commands one last time: nothing should report an
  active trial or usage.

### Retrospective 26.5

#### Question: The whole picture

_Draw (or describe) the detection stack for an organization with a
management account, a Log Archive account, a Security Tooling account and
ten workload accounts across two Regions. For each service in this
module, say where it's enabled, where its data lands, which account
administers it, and what stops a workload account administrator from
turning it off._

#### Question: Cost of watching

_Estimate the monthly cost of that stack after the free trials, using the
pricing pages. Which service dominates, what drives its cost, and what
would you change (recording scope, frequency, protection plans, scanned
resource types) to halve it without going blind?_

## Further Reading

- [AWS Security Reference
  Architecture](https://docs.aws.amazon.com/prescriptive-guidance/latest/security-reference-architecture/welcome.html):
  the account layout and service placement these services assume.
- [GuardDuty Extended Threat
  Detection](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty-extended-threat-detection.html):
  how attack-sequence findings are built.
- [Test GuardDuty findings in dedicated
  accounts](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_findings-scripts.html):
  generates real findings by simulating activity. It deploys billable
  infrastructure; read it, don't run it in this course.
- [AWS Config Rule Development Kit
  (RDK)](https://github.com/awslabs/aws-config-rdk) for Lambda-backed
  rules, and the [conformance pack
  samples](https://github.com/awslabs/aws-config-rules/tree/master/aws-config-conformance-packs)
  on GitHub.
- [Amazon Security Lake](https://docs.aws.amazon.com/security-lake/latest/userguide/what-is-security-lake.html):
  an OCSF data lake for security logs, named in SCS-C03 Task 1.2.
- [Amazon Detective](https://docs.aws.amazon.com/detective/latest/userguide/what-is-detective.html):
  root-cause investigation over GuardDuty findings (SCS-C03 Skill 2.2.5).
- [Security Hub CSPM controls
  reference](https://docs.aws.amazon.com/securityhub/latest/userguide/securityhub-controls-reference.html):
  read a few controls and find the Config rule behind each.
