# Topic 20: Systems Manager

<!-- TOC -->

- [Topic 20: Systems Manager](#topic-20-systems-manager)
  - [What changed in the 2026 edition](#what-changed-in-the-2026-edition)
  - [Exam coverage](#exam-coverage)
  - [Cost and cleanup](#cost-and-cleanup)
  - [Guidance](#guidance)
  - [Conventions](#conventions)
  - [Lesson 20.1: Session Manager in depth](#lesson-201-session-manager-in-depth)
    - [Principle 20.1](#principle-201)
    - [Practice 20.1](#practice-201)
      - [Lab 20.1.1: A fleet to manage](#lab-2011-a-fleet-to-manage)
      - [Lab 20.1.2: Log every session](#lab-2012-log-every-session)
      - [Lab 20.1.3: Session preferences](#lab-2013-session-preferences)
      - [Lab 20.1.4: Port forwarding](#lab-2014-port-forwarding)
      - [Lab 20.1.5: Who may open which session](#lab-2015-who-may-open-which-session)
    - [Retrospective 20.1](#retrospective-201)
  - [Lesson 20.2: Run Command, State Manager and Inventory](#lesson-202-run-command-state-manager-and-inventory)
    - [Principle 20.2](#principle-202)
    - [Practice 20.2](#practice-202)
      - [Lab 20.2.1: Run Command across a fleet](#lab-2021-run-command-across-a-fleet)
      - [Lab 20.2.2: Your own Command document](#lab-2022-your-own-command-document)
      - [Lab 20.2.3: Desired state with State Manager](#lab-2023-desired-state-with-state-manager)
      - [Lab 20.2.4: Inventory and resource data sync](#lab-2024-inventory-and-resource-data-sync)
    - [Retrospective 20.2](#retrospective-202)
  - [Lesson 20.3: Patch Manager and maintenance windows](#lesson-203-patch-manager-and-maintenance-windows)
    - [Principle 20.3](#principle-203)
    - [Practice 20.3](#practice-203)
      - [Lab 20.3.1: Patch baselines](#lab-2031-patch-baselines)
      - [Lab 20.3.2: Scan before you install](#lab-2032-scan-before-you-install)
      - [Lab 20.3.3: A maintenance window](#lab-2033-a-maintenance-window)
      - [Lab 20.3.4: Patch groups and patch policies](#lab-2034-patch-groups-and-patch-policies)
    - [Retrospective 20.3](#retrospective-203)
  - [Lesson 20.4: Automation runbooks](#lesson-204-automation-runbooks)
    - [Principle 20.4](#principle-204)
    - [Practice 20.4](#practice-204)
      - [Lab 20.4.1: Run AWS-owned runbooks](#lab-2041-run-aws-owned-runbooks)
      - [Lab 20.4.2: Diagnose an unmanaged node](#lab-2042-diagnose-an-unmanaged-node)
      - [Lab 20.4.3: Write a runbook](#lab-2043-write-a-runbook)
      - [Lab 20.4.4: Schedule the runbook](#lab-2044-schedule-the-runbook)
    - [Retrospective 20.4](#retrospective-204)
  - [Lesson 20.5: Golden AMIs with EC2 Image Builder](#lesson-205-golden-amis-with-ec2-image-builder)
    - [Principle 20.5](#principle-205)
    - [Practice 20.5](#practice-205)
      - [Lab 20.5.1: A hardening component](#lab-2051-a-hardening-component)
      - [Lab 20.5.2: Recipe, infrastructure and distribution](#lab-2052-recipe-infrastructure-and-distribution)
      - [Lab 20.5.3: Build the image](#lab-2053-build-the-image)
      - [Lab 20.5.4: Roll the fleet onto the new AMI](#lab-2054-roll-the-fleet-onto-the-new-ami)
      - [Lab 20.5.5: Image lifecycle policy (optional)](#lab-2055-image-lifecycle-policy-optional)
      - [Lab 20.5.6: The unified console and Quick Setup (optional)](#lab-2056-the-unified-console-and-quick-setup-optional)
      - [Lab 20.5.7: Clean up the module](#lab-2057-clean-up-the-module)
    - [Retrospective 20.5](#retrospective-205)
  - [Further Reading](#further-reading)

<!-- /TOC -->

## What changed in the 2026 edition

- **New module.** The 2022 course used Systems Manager only for Parameter
  Store (module 11). Module 05 now introduces Session Manager as the way onto
  an instance; this module covers the rest of the operations toolkit that the
  CloudOps exam tests: session logging, Run Command, State Manager,
  Inventory, Patch Manager, maintenance windows, Automation and EC2 Image
  Builder.
- SOA-C03 names these tools directly: custom and predefined **Automation
  runbooks** (Skill 1.2.3), **EC2 Image Builder** (Skill 3.1.1) and **Systems
  Manager** for operational automation (Skill 3.2.1).
- It teaches the current way of doing things: **patch policies** in Quick
  Setup are AWS's recommended way to configure patching, and patch groups are
  no longer offered in the console for account-Region pairs that never used
  them. **Default Host Management Configuration** (DHMC) can make instances
  managed without an instance profile, and the **unified Systems Manager
  console** sets up DHMC, inventory and agent updates in one step.
- Image Builder recipes can take their parent image from an SSM parameter,
  and distribution can write the new AMI ID to a parameter (April 2025). The
  lab pipeline builds a hardened AL2023 AMI and publishes it that way, so the
  fleet template never holds an AMI ID. Image Builder's STIG hardening
  components have supported Amazon Linux 2023 since 2025.
- What's gone or changed: **Change Manager** and **Incident Manager** closed
  to new customers on 7 November 2025 (AWS points to OpsCenter instead). The
  **advanced-instances tier** for on-premises and multicloud servers was
  removed on 30 June 2026 and replaced with per-use pricing for those nodes.
  The Systems Manager CloudWatch dashboard was retired after 30 April 2026.
- Labs run in the lab account in `us-east-2` with the `lab` profile. There
  is no SSH anywhere, and the only inbound security group rule is one the
  port-forwarding lab adds between the fleet's own instances.

## Exam coverage

| Exam | Domain / task statement |
|---|---|
| SOA-C03 | Domain 1: Monitoring, Logging, Analysis, Remediation, and Performance Optimization (Task 1.2: identify and remediate issues; Skill 1.2.3: custom and predefined Automation runbooks) |
| SOA-C03 | Domain 3: Deployment, Provisioning, and Automation (Task 3.1: provision and maintain cloud resources, Skill 3.1.1: AMIs with EC2 Image Builder; Task 3.2: automate the management of existing resources, Skill 3.2.1: Systems Manager) |
| SOA-C03 | Domain 4: Security and Compliance (Task 4.1: security and compliance tools; session logging, patch compliance, least-privilege session access) |
| DOP-C02 | Domain 2: Configuration Management and IaC (Task 2.1: reusable components such as golden AMIs; Task 2.3: automated solutions for large-scale environments, including inventory, configuration, patch management and State Manager) |
| DOP-C02 | Domain 5: Incident and Event Response (Task 5.2: implement configuration changes in response to events) |
| DOP-C02 | Domain 6: Security and Compliance (Task 6.2: automation for security controls) |

## Cost and cleanup

- **Free on EC2:** Session Manager, Run Command, State Manager, Inventory,
  Patch Manager, maintenance windows, Compliance, Fleet Manager, Quick Setup
  and standard Parameter Store parameters. You pay only for what they create
  or write to, such as S3 objects and CloudWatch Logs.
- **The fleet** (Lab 20.1.1) is two `t4g.micro` instances with public IPv4
  addresses: roughly $0.03 an hour, or about $0.70 a day. Delete the stack
  between sessions; everything in the labs can be re-created.
- **Automation** charges $0.002 per step and $0.00003 per second of
  `aws:executeScript` run time. The labs run well under a hundred steps.
  <!-- VERIFY: the size of the Automation free-tier allowance; the pricing
  page says "Included with AWS Free Tier (limits apply)" without numbers. -->
- **OpsCenter** charges $2.97 per 1,000 OpsItems created, plus a small
  charge for API calls. Only optional steps create OpsItems.
- **Not used, but know the prices:** just-in-time node access is billed per
  node-hour after a free trial, so don't enable it in the lab account. For
  hybrid and multicloud nodes (non-EC2 servers), registration has been free
  since 30 June 2026, and from 30 September 2026 each Session Manager session
  costs $0.05 and each Run Command invocation $0.002. The course registers
  none.
- **EC2 Image Builder** has no charge of its own. Each build launches a
  build instance and a test instance for 20 to 60 minutes, and every AMI
  keeps an EBS snapshot (about $0.05 per GB-month) until you delete it.
  Deleting Image Builder resources, including the image resource, does
  **not** deregister the AMI or delete its snapshot. Leave Amazon Inspector
  image scanning off unless Inspector is already enabled.
- **Small charges:** CloudWatch Logs ingestion and storage for session and
  command logs, S3 storage for logs and inventory, Athena queries ($5 per TB
  scanned, so fractions of a cent here), and a KMS key ($1 a month, prorated)
  if you do the optional session-encryption step.
- **Cleanup:** [Lab 20.5.7](#lab-2057-clean-up-the-module) removes everything:
  stacks, AMIs and snapshots, parameters, documents, associations,
  maintenance windows, baselines, buckets, log groups and the Session Manager
  preferences.

## Guidance

- Explore the official docs! See the AWS Systems Manager
  [User Guide](https://docs.aws.amazon.com/systems-manager/latest/userguide/what-is-systems-manager.html),
  [API Reference](https://docs.aws.amazon.com/systems-manager/latest/APIReference/Welcome.html),
  [CLI Reference](https://docs.aws.amazon.com/cli/latest/reference/ssm/)
  and
  [CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/AWS_SSM.html)
  docs, the
  [Automation runbook reference](https://docs.aws.amazon.com/systems-manager-automation-runbooks/latest/userguide/automation-runbook-reference.html),
  and the
  [EC2 Image Builder User Guide](https://docs.aws.amazon.com/imagebuilder/latest/userguide/what-is-image-builder.html)
  with its
  [CLI](https://docs.aws.amazon.com/cli/latest/reference/imagebuilder/) and
  [CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/AWS_ImageBuilder.html)
  references.

- Systems Manager is a family of tools that share a few ideas: **managed
  nodes** (anything running the SSM Agent that has permission to talk to the
  service), **SSM documents** (JSON or YAML that say what to do: Command,
  Session, Automation and more) and **targets** (instance IDs, tags or
  resource groups). Learn those three first and every tool will look
  familiar.

- Avoid using other sites like stackoverflow.com for answers \-- part
  of the skill set you're building is finding answers straight from
  the source, AWS.

- Explore your curiosity. Try to understand why things work the way
  they do. Read more of the documentation than just what you need to
  find the answers.

## Conventions

- **Profile and Region.** Everything runs in the lab account with the `lab`
  profile from module 19, in `us-east-2`. CLI examples don't pass
  `--region`.
- **Names.** `<you>` is your identifier. Put it in every stack, document,
  association, baseline, window, bucket and parameter name, and tag
  resources with `owner=<you>`. Custom SSM document names can't start with
  the prefixes AWS reserves (`aws`, `amazon`, `amzn`, `AWSEC2`,
  `AWSConfigRemediation`, `AWSSupport`), which is another reason to lead
  with `<you>`.
- **Placeholders.** Examples use `123456789012` for the account ID and
  `i-0123456789abcdef0` for an instance. Don't commit your real account ID;
  write `<lab-account-id>` in your answers.
- **CloudFormation where it fits, the CLI where it teaches.** Buckets, log
  groups, roles, documents, baselines, windows and the Image Builder
  resources belong in templates. Commands you run once to see what happens
  (`send-command`, `start-automation-execution`) stay on the CLI; save
  them in a script in your repository.
- **Session Manager plugin.** You installed it in module 05. Check it with
  `session-manager-plugin --version`.
- DO use the AWS CLI rather than the console, except where a step says the
  console is required.

## Lesson 20.1: Session Manager in depth

### Principle 20.1

*Access to a server should be granted by IAM, carried over an outbound
connection, and recorded, so that nobody needs a key and every session can
be audited.*

### Practice 20.1

In module 05 you opened a shell with `aws ssm start-session` and saw that no
inbound port was needed. That's the start. In an audited environment you
also need to know what was typed, cap how long a session can idle or last,
decide which operating system user people land as, reach services on the
instance (or behind it) without opening ports, and control who may do which
of those things.

All of those are **Session Manager preferences** or **Session documents**.
Preferences live in a Session document named `SSM-SessionManagerRunShell`,
one per account per Region. Other Session documents define port forwarding
and interactive commands. IAM decides who can start a session, on which
nodes, with which documents.

#### Lab 20.1.1: A fleet to manage

Start from the starter template
[starter/fleet.yaml](starter/fleet.yaml). It creates two AL2023 instances
tagged `Environment=dev` and `Environment=prod`, each running nginx, with an
instance profile that has `AmazonSSMManagedInstanceCore`, a security group
with no inbound rules and IMDSv2 required.

- Read the template before you deploy it. Find where the AMI comes from and
  why it's a parameter.

- Deploy it as `<you>-ssm-fleet` into the default VPC.

- Confirm both instances are managed nodes with
  `aws ssm describe-instance-information`. Filter the output by the
  `Environment` tag, and note the agent version, platform and ping status.

- Read [Default Host Management
  Configuration](https://docs.aws.amazon.com/systems-manager/latest/userguide/fleet-manager-default-host-management-configuration.html)
  (DHMC). Don't turn it on yet; Lab 20.5.6 does that, optionally.

##### Question: Two ways to become managed

_With DHMC, instances can be managed without an instance profile. What
does DHMC require of the instance (metadata version, agent version)? If an
instance has both DHMC and an instance profile, which credentials does the
SSM Agent use, and what must you remove from the profile for DHMC to take
over? Why does this course keep the instance profile anyway?_

#### Lab 20.1.2: Log every session

Session logs can go to S3 (written when the session ends) and to CloudWatch
Logs (at the end, or streamed as the session runs). The **instance** writes
them, so the instance role needs permission, not you.

- Read [Logging session
  activity](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-logging.html),
  including the limitations box.

- Write a small template, `<you>-ssm-logging`, with:
  - an S3 bucket for session logs (Block Public Access on, SSE-S3, a
    lifecycle rule that expires objects after 30 days);
  - a CloudWatch Logs log group with a 7-day retention;
  - outputs for both names.

- Give the fleet role the permissions it needs to write there. The
  [instance profile
  page](https://docs.aws.amazon.com/systems-manager/latest/userguide/getting-started-create-iam-instance-profile.html)
  lists them. Scope `s3:PutObject` to your bucket and the log actions to
  your log group. Update the fleet stack (the `TODO` in the template marks
  the spot).

- Point the preferences at the bucket and the log group. Write the
  preferences as a JSON file in your repository and apply it with
  `aws ssm update-document --name SSM-SessionManagerRunShell
  --document-version '$LATEST'` (or `create-document` with
  `--document-type Session` if the document doesn't exist yet). See
  [Update Session Manager preferences (command
  line)](https://docs.aws.amazon.com/systems-manager/latest/userguide/getting-started-configure-preferences-cli.html)
  and the [Session document
  schema](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-schema.html).
  Turn on CloudWatch streaming.

- Open a session on the dev instance, run a few commands, exit. Then:
  - `aws logs tail` the log group;
  - list and download the S3 object;
  - `aws ssm describe-sessions --state History` and find your session.

<!-- VERIFY: whether cloudWatchEncryptionEnabled=true requires a KMS key
on the log group (not just the default CloudWatch Logs encryption). Lab
wording assumes it does and asks the student to find out. -->

##### Question: Encryption flags

_The preferences have `s3EncryptionEnabled` and
`cloudWatchEncryptionEnabled`. What does each one actually check? Your
bucket uses SSE-S3 by default; what did you have to set for the log group,
and why? How is that different from `kmsKeyId`?_

##### Question: What the log can't see

_Type a password at a prompt that echoes it, then one that doesn't
(`read -s`). What ends up in the log? Which kind of session isn't logged at
all, and why can't it be?_

#### Lab 20.1.3: Session preferences

Extend your preferences file and update the document again:

- An **idle timeout** of 10 minutes and a **maximum session duration** of 60
  minutes ([idle
  timeout](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-preferences-timeout.html),
  [maximum
  duration](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-preferences-max-timeout.html)).

- **Run As** support, so sessions start as `ec2-user` instead of `ssm-user`
  ([Run
  As](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-preferences-run-as.html)).

- A Linux **shell profile** that starts in `ec2-user`'s home directory and
  runs `bash`
  ([shell profile](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-preferences-shell-config.html)).

- Open a new session and check `whoami`, `pwd` and what `sudo -l` allows.
  Leave it idle and time how long it takes to close.

##### Question: Choosing the user

_Session Manager checks three places, in order, to decide the Run As user.
What are they? How would you let one team land as `ec2-user` and another as
a restricted `appsupport` user on the same instances, without two
preferences documents?_

##### Question: Preferences per Region

_Your preferences document exists in `us-east-2` only. What happens to
logging if someone starts a session on an instance in `us-east-1`? How would
you make sure every Region your organization allows has the same
preferences?_

#### Lab 20.1.4: Port forwarding

Port forwarding carries a TCP connection from your laptop to a port on the
instance, or through the instance to another host, over the same outbound
Session Manager channel. See [Start a
session](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-sessions-start.html),
sections on port forwarding.

- **To the node.** Forward local port 8080 to port 80 on the dev instance
  with the `AWS-StartPortForwardingSession` document, and `curl
  localhost:8080` from your machine.

- **Through the node to a remote host.** Forward local port 8081 to port 80
  on the **prod** instance's private IP, going through the **dev** instance,
  with `AWS-StartPortForwardingSessionToRemoteHost`. It fails. Work out why
  without changing anything, then fix it in the fleet template with the
  smallest rule you can write: one inbound rule, TCP 80, whose source is the
  fleet security group itself, not a CIDR. Update the stack and try again.

- Look for your port-forwarding session in the S3 bucket and log group.

##### Question: A tunnel to a database

_Module 22 puts a database in a private subnet. How would you use this
technique to connect a desktop SQL client to it with no bastion host, no
inbound rule from the internet and no VPN? Which host name would you give as
`host`, and what has to be true of the security groups and of the instance
you tunnel through?_

##### Question: The one inbound rule

_You added an inbound rule to a fleet that had none. Why is a
security-group-referencing rule better than the VPC CIDR here? Does Session
Manager itself need this rule?_

#### Lab 20.1.5: Who may open which session

By default, anyone allowed `ssm:StartSession` can use the default shell
document and every other Session document they can name. Lock that down.

- Read [Control session
  access](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-getting-started-restrict-access.html),
  [Start a session with a specific
  document](https://docs.aws.amazon.com/systems-manager/latest/userguide/getting-started-specify-session-document.html)
  and the [sample IAM policies for Session
  Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/getting-started-restrict-access-quickstart.html).
  <!-- VERIFY: the page "Enforce a session document permission check for
  the AWS CLI" (getting-started-sessiondocumentaccesscheck.html), which
  documents ssm:SessionDocumentAccessCheck, redirected to the guide's root
  on 2026-09-18 though search engines still index it. Confirm the condition
  key is still supported and where it is documented now. -->

- In a template, create a role `<you>-web-tunnel` that your lab principal
  can assume. Its policy should allow:
  - `ssm:StartSession` only on instances tagged `Environment=dev`, and only
    with the `AWS-StartPortForwardingSession` document, using the
    `ssm:SessionDocumentAccessCheck` condition;
  - `ssm:TerminateSession` and `ssm:ResumeSession` only on sessions that
    role started. The sample policies scope these with a
    `session/${aws:userid}-*` resource; start a session as the role and
    compare its session ID with what that pattern expands to;
  - the other actions the sample policies list for a working session
    (for example `ssmmessages:OpenDataChannel`).

- Add a CLI profile that assumes the role, then test:
  - Positive: port-forward to the dev instance.
  - Negative: port-forward to the prod instance.
  - Negative: a plain shell session (no `--document-name`) on dev.
  - Negative: terminate a session your normal `lab` profile started.

##### Question: Least privilege for sessions

_Why does `ssm:SessionDocumentAccessCheck` matter even when the
`Resource` list names only the port-forwarding document? What would the
role have been able to do without it?_

### Retrospective 20.1

#### Question: Just-in-time node access

_Read [Just-in-time node
access](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-just-in-time-node-access.html).
Compare it with what you built in Lab 20.1.5: who approves access, how
long it lasts, and what it costs. When would the extra cost be worth it?_

#### Question: Where the audit trail is

_A security reviewer asks, "Who opened a shell on the prod instance last
Tuesday, and what did they run?" List every place you'd look (CloudTrail,
the session history, S3, CloudWatch Logs), which question each one
answers, and which one an administrator on the instance could tamper
with._

## Lesson 20.2: Run Command, State Manager and Inventory

### Principle 20.2

*Say what should be true of every server once, and let the service keep
making it true, instead of logging in to fix servers one at a time.*

### Practice 20.2

A shell session is one person on one server. **Run Command** runs a
Command document on many nodes at once, chosen by tag, with rate controls
so a bad command doesn't hit the whole fleet. **State Manager** runs a
document on a schedule and reports compliance, so drift gets corrected.
**Inventory** is itself a State Manager association, one that collects what
is installed and configured on every node.

These labs go from one-off commands to a desired state that repairs itself,
and end with a queryable record of the fleet.

#### Lab 20.2.1: Run Command across a fleet

- Read [Run
  Command](https://docs.aws.amazon.com/systems-manager/latest/userguide/run-command.html)
  and [Run commands at
  scale](https://docs.aws.amazon.com/systems-manager/latest/userguide/send-commands-multiple.html).

- With `aws ssm send-command` and the `AWS-RunShellScript` document, run
  `dnf check-update; uptime` on every instance tagged `owner=<you>`. Target
  by tag, not by instance ID. Set `--max-concurrency 1` and
  `--max-errors 0`.

- Send the output to your log group
  ([CloudWatch output](https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-rc-setting-up-cwlogs.html))
  and to a prefix in your logging bucket. Read it with
  `aws ssm list-command-invocations --details` and in both destinations.

- Run a command that fails on purpose (`exit 1`) against both instances with
  `--max-errors 0`. What happened to the second instance?

##### Question: Rate control

_What do `--max-concurrency` and `--max-errors` each control? For a fleet of
200 web servers behind a load balancer, what values would you choose for a
config change, and why can percentages be safer than absolute numbers?_

##### Question: Where the output went

_`list-command-invocations` truncates output. At how many characters? Why
did you have to give the instance role permission for the S3 and CloudWatch
Logs output, rather than yourself?_

#### Lab 20.2.2: Your own Command document

`AWS-RunShellScript` runs anything, which is also its problem. A custom
Command document can take typed, validated parameters and do one thing.

- Read [Command document plugin
  reference](https://docs.aws.amazon.com/systems-manager/latest/userguide/documents-command-ssm-plugin-reference.html)
  and [Creating SSM document
  content](https://docs.aws.amazon.com/systems-manager/latest/userguide/documents-creating-content.html).

- In a template (`AWS::SSM::Document`, `DocumentType: Command`,
  `schemaVersion: '2.2'`), write `<you>-SetMotd`. It takes a `Message`
  parameter restricted by `allowedPattern` to letters, digits, spaces and
  basic punctuation, writes it to `/etc/motd`, and prints the file.

- Run it with `send-command` against the dev instance. Then try a message
  containing `$(id)`. What stopped it?

- Update the document and look at `list-document-versions`. Which version
  does `send-command` use if you don't say?

##### Question: Documents as an interface

_Why is a narrow document with validated parameters a better thing to grant
a support team than `ssm:SendCommand` on `AWS-RunShellScript`? Write the
IAM `Resource` element that would allow only your document._

#### Lab 20.2.3: Desired state with State Manager

- Read [State
  Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-state.html)
  and [How State Manager
  works](https://docs.aws.amazon.com/systems-manager/latest/userguide/state-manager-about.html).

- In a template, create two `AWS::SSM::Association` resources:
  - **nginx stays running:** `AWS-RunShellScript` (or your own document) that
    installs nginx if missing and runs `systemctl enable --now nginx`,
    targeted at `tag:owner=<you>`, every 30 minutes, with a compliance
    severity of `HIGH`.
  - **Agent stays current:** `AWS-UpdateSSMAgent`, weekly. See [Automating
    updates to SSM
    Agent](https://docs.aws.amazon.com/systems-manager/latest/userguide/ssm-agent-automatic-updates.html).

- Break the desired state: open a session on dev and
  `sudo systemctl stop nginx`. Don't wait 30 minutes; run the association
  now with `aws ssm start-associations-once`. Check nginx again.

- Look at compliance:
  `aws ssm list-resource-compliance-summaries` and
  `list-compliance-items` for the dev instance. See
  [Compliance](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-compliance.html).

##### Question: Run Command or State Manager

_Both of these ran the same script. When would you choose each? What does
an association give you that a cron job on the instance doesn't?_

##### Question: New instances

_Replace the dev instance (change its tags or recreate the stack). Did the
associations run on the new instance without you doing anything? Why?_

#### Lab 20.2.4: Inventory and resource data sync

- Read [Inventory](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-inventory.html)
  and [Working with custom
  inventory](https://docs.aws.amazon.com/systems-manager/latest/userguide/inventory-custom.html).

- Add a third association to your template: `AWS-GatherSoftwareInventory`,
  every 30 minutes, targeted at `tag:owner=<you>`. Collect applications,
  network config, services and instance details.

- On the prod instance, write a custom inventory item (for example
  `Custom:ServerRole` with a `Role` of `web` and a `Team` of `<you>`) in the
  directory the docs give.

- Query the fleet with `aws ssm get-inventory` and
  `list-inventory-entries`: which version of `nginx` and of
  `amazon-ssm-agent` does each instance have? Which instance has your custom
  type?

- Create a [resource data
  sync](https://docs.aws.amazon.com/systems-manager/latest/userguide/inventory-create-resource-data-sync.html)
  (`AWS::SSM::ResourceDataSync`) to a new prefix in your bucket. The bucket
  needs a bucket policy that lets Systems Manager write; the page has one.
  Wait for data to arrive, then list what's there.

- (Optional) Query it with
  [Athena](https://docs.aws.amazon.com/athena/latest/ug/what-is.html): create
  a database and table over the sync prefix (the walkthrough in the Inventory
  docs has the DDL) and list every package whose name starts with `nginx`.
  Delete the Athena objects afterwards.

##### Question: One inventory association

_What happens if a node is targeted by two inventory associations that both
target by tag? Why might that bite you if you later enable the unified
console or a Quick Setup host-management configuration?_

### Retrospective 20.2

#### Question: Configuration management tools

_State Manager can also run Ansible playbooks and Chef recipes
(`AWS-ApplyAnsiblePlaybooks`, `AWS-ApplyChefRecipes`). Compare using it that
way with running Ansible from a control node over SSH. What does each
approach need open on the network, and where do the credentials live?_

#### Question: Drift you can't see

_Your nginx association corrects a stopped service. What kinds of drift
would it not detect? How would Inventory, AWS Config (module 26) and
immutable AMIs (Lesson 20.5) each help?_

## Lesson 20.3: Patch Manager and maintenance windows

### Principle 20.3

*Patching is a policy, a schedule and a report: decide what counts as
compliant, install it when it's safe to, and prove it.*

### Practice 20.3

Patch Manager separates three questions. **What should be installed?** A
patch baseline: approval rules by classification, severity and age, plus
explicit approve and reject lists. **When?** A maintenance window, a
State Manager association, a patch policy or "Patch now". **Did it
work?** Patch compliance, per node, reported to Systems Manager.

The labs build a custom AL2023 baseline, scan with it, install through a
maintenance window on dev only, and then compare that setup with patch
groups and with patch policies.

On AL2023, read [How security patches are
selected](https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager-selecting-patches.html)
alongside [deterministic
upgrades](https://docs.aws.amazon.com/linux/al2023/ug/deterministic-upgrades.html):
AL2023 repositories are versioned, and Patch Manager patches from the latest
repository version regardless of what the instance is locked to.

#### Lab 20.3.1: Patch baselines

- Read [Predefined and custom patch
  baselines](https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager-predefined-and-custom-patch-baselines.html).
  Find the predefined `AWS-AmazonLinux2023DefaultPatchBaseline` with
  `aws ssm describe-patch-baselines` and read its rules with
  `get-patch-baseline`.

- In a template, create `<you>-al2023-baseline`
  (`AWS::SSM::PatchBaseline`, operating system `AMAZON_LINUX_2023`) that:
  - approves `Security` patches of severity `Critical` and `Important`
    after 3 days, and `Bugfix` patches after 7;
  - reports a missing approved patch as `HIGH` non-compliance
    (`ApprovedPatchesComplianceLevel`), and decides what a security update
    that is available but not yet approved counts as
    (`AvailableSecurityUpdatesComplianceStatus`);
  - rejects one package you pick (for example a specific `nginx` version),
    with `RejectedPatchesAction` set so that it's blocked even as a
    dependency.

- Don't make it the default yet.

##### Question: Approval delay

_Why would you approve security patches 3 days after release rather than
immediately? What does the delay protect you from, and what does it cost
you? How do you approve one urgent patch without changing the delay?_

#### Lab 20.3.2: Scan before you install

- Read [About the AWS-RunPatchBaseline SSM
  document](https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager-aws-runpatchbaseline.html).

- Register your baseline as the default for AL2023 in the lab account
  (`register-default-patch-baseline`). See [Setting an existing patch
  baseline as the
  default](https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager-default-patch-baseline.html).

- Run `AWS-RunPatchBaseline` with `Operation=Scan` on both instances using
  Run Command.

- Read the results: `describe-instance-patch-states` (counts per state) and
  `describe-instance-patches` (per-patch detail) for each instance. Are the
  instances compliant? Which patches are `Missing`?

##### Question: Compliance is yours to define

_The docs say patch states don't mean compliance. What does? If an instance
has a `Missing` patch that your baseline doesn't approve, is it compliant?_

#### Lab 20.3.3: A maintenance window

Install patches on dev only, at a time you choose, with a reboot if needed.

- Read [Maintenance
  windows](https://docs.aws.amazon.com/systems-manager/latest/userguide/maintenance-windows.html).

- In a template, create:
  - `AWS::SSM::MaintenanceWindow` `<you>-dev-patching`: a `cron` schedule
    with an explicit `ScheduleTimezone`, a 2-hour duration, a 1-hour cutoff
    and `AllowUnassociatedTargets: false`;
  - `AWS::SSM::MaintenanceWindowTarget` for `tag:Environment=dev` and
    `tag:owner=<you>`;
  - `AWS::SSM::MaintenanceWindowTask` of type `RUN_COMMAND` running
    `AWS-RunPatchBaseline` with `Operation=Install` and
    `RebootOption=RebootIfNeeded`, with rate controls, and command output
    to your bucket.

- Set the schedule a few minutes into the future, deploy, and watch it run
  with `describe-maintenance-window-executions` and
  `describe-maintenance-window-execution-tasks`. Then move the schedule
  back to something harmless (for example, weekly at 03:00 on Sunday).

- Scan both instances again. Compare dev and prod.

##### Question: Duration and cutoff

_What do the window's duration and cutoff each control? What happens to a
task that is still running when the cutoff arrives, and to one that hasn't
started?_

##### Question: Patching behind a load balancer

_Dev had a single instance. If it were five instances behind an
Application Load Balancer, which task settings would stop the window from
rebooting them all at once? What else would you want to happen before and
after each instance is patched? (Lesson 20.4 builds part of that.)_

#### Lab 20.3.4: Patch groups and patch policies

Two more ways to decide which baseline applies to which nodes.

- **Patch groups.** Read [Patch
  groups](https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager-patch-groups.html).
  Tag prod with `PatchGroup=prod` and register the predefined AL2023
  baseline for that group with `register-patch-baseline-for-patch-group`.
  Scan prod again. Which baseline did it use, and where does the scan
  output say so?
  <!-- VERIFY: that register-patch-baseline-for-patch-group still works
  from the CLI in an account-Region pair that never used patch groups
  before December 2022 (the docs only say the console doesn't offer it). -->

- **Patch policies.** Read [Patch policy configurations in Quick
  Setup](https://docs.aws.amazon.com/systems-manager/latest/userguide/patch-manager-policies.html)
  and [Configure patching with a Quick Setup patch
  policy](https://docs.aws.amazon.com/systems-manager/latest/userguide/quick-setup-patch-manager.html).
  Don't create one: it creates its own associations, roles and an S3
  bucket, and it would compete with the window you built. Answer the
  questions below instead.

##### Question: Three ways to pick a baseline

_Compare the default baseline, a patch group and a patch policy: how is the
baseline chosen for a node, can it span accounts and Regions, and what
happens to patch groups once a node is covered by a patch policy?_

##### Question: The recommended way

_AWS recommends patch policies for new setups. What did you learn by doing
it by hand that a patch policy would have hidden from you?_

### Retrospective 20.3

#### Question: Patch or replace

_Lesson 20.5 builds a new AMI with patches baked in. For a stateless web
fleet in an Auto Scaling group, would you patch instances in place or
replace them from a new AMI? For a single database server? What would
Patch Manager still be for in the replace-from-AMI world?_

#### Question: Reporting upward

_Your manager wants a weekly report of patch compliance across every
account in the organization. Which Systems Manager features, or other
services from this course, would produce it with the least ongoing work?_

## Lesson 20.4: Automation runbooks

### Principle 20.4

*An operational procedure that is written down as steps a machine can run
is faster, safer and auditable, and it stays correct because it gets used.*

### Practice 20.4

An **Automation runbook** is an SSM document (`schemaVersion: '0.3'`) whose
steps call AWS APIs, run commands on nodes, run Python or PowerShell,
branch, wait, loop and pause for approval. Runbooks run in the Systems
Manager service rather than on a node, as you or as an assumed **service
role**, and every step's input and output is recorded.

AWS publishes hundreds of runbooks: `AWS-*` for common operations and
`AWSSupport-*` for diagnostics. You'll use some of those first, with rate
control across tagged targets, then write your own that snapshots, patches
and health-checks an instance, and schedule it from your maintenance
window. SOA-C03 Skill 1.2.3 asks for exactly this: running predefined
runbooks and writing custom ones.

#### Lab 20.4.1: Run AWS-owned runbooks

- Read [Automation](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-automation.html)
  and [Setting up
  Automation](https://docs.aws.amazon.com/systems-manager/latest/userguide/automation-setup.html).

- Create an Automation service role in a template, `<you>-automation`,
  trusted by `ssm.amazonaws.com` with an `aws:SourceAccount` condition, and
  with only the permissions this lesson needs. You'll grow it in Lab 20.4.3.

- Read [AWS-RestartEC2Instance](https://docs.aws.amazon.com/systems-manager-automation-runbooks/latest/userguide/automation-aws-restartec2instance.html)
  in the runbook reference, then look at its steps with
  `aws ssm get-document --name AWS-RestartEC2Instance`.

- Preview it with `aws ssm start-execution-preview` against the dev
  instance and read the result with `get-execution-preview`. See
  [start-execution-preview](https://docs.aws.amazon.com/cli/latest/reference/ssm/start-execution-preview.html).

- Run it against **every** instance tagged `owner=<you>` in one execution,
  with `--target-parameter-name InstanceId`, `--targets` on the tag,
  `--max-concurrency 1` and `--max-errors 0`, passing your service role as
  `AutomationAssumeRole`. See [Run automated operations at
  scale](https://docs.aws.amazon.com/systems-manager/latest/userguide/running-automations-scale.html).

- Follow it with `describe-automation-executions` and
  `describe-automation-step-executions`. How many child executions were
  there?

##### Question: Whose permissions

_What happens if you start the runbook without `AutomationAssumeRole`?
When is running as yourself fine, and when must a runbook use a service
role (think of State Manager, maintenance windows and EventBridge)? What
does `iam:PassRole` have to do with it?_

#### Lab 20.4.2: Diagnose an unmanaged node

- Break the dev instance's management: find its instance profile
  association with `aws ec2 describe-iam-instance-profile-associations` and
  remove it with `disassociate-iam-instance-profile`. (This makes the stack
  drift on purpose; you'll put it back.) Wait until
  `describe-instance-information` shows it as `ConnectionLost`.

- Run [AWSSupport-TroubleshootManagedInstance](https://docs.aws.amazon.com/systems-manager-automation-runbooks/latest/userguide/automation-awssupport-troubleshoot-managed-instance.html)
  on it and read the findings.

- Fix it the way the findings suggest (`associate-iam-instance-profile`
  with the stack's profile), and check that it comes back online. Run
  drift detection on the fleet stack to confirm it matches the template
  again.

##### Question: Reading someone else's runbook

_Pick two steps from that runbook's definition. What API or check does each
perform? What would you have had to check by hand without it?_

#### Lab 20.4.3: Write a runbook

Write `<you>-SafePatch` as an `AWS::SSM::Document` with
`DocumentType: Automation`. Read the
[actions reference](https://docs.aws.amazon.com/systems-manager/latest/userguide/automation-actions.html),
[Authoring
runbooks](https://docs.aws.amazon.com/systems-manager/latest/userguide/automation-authoring-runbooks.html)
and
[aws:executeScript](https://docs.aws.amazon.com/systems-manager/latest/userguide/automation-action-executeScript.html).

It takes an `InstanceId` (type `AWS::EC2::Instance::Id`) and an
`AutomationAssumeRole`, and it:

1. finds the instance's root volume (`aws:executeAwsApi`, with an output
   selector);
1. snapshots it, tagged with `owner`, the instance ID and the execution ID
   (`aws:executeAwsApi`), and waits for the snapshot to complete
   (`aws:waitForAwsResourceProperty`);
1. patches the instance (`aws:runCommand` with `AWS-RunPatchBaseline`,
   `Install`, `RebootIfNeeded`);
1. health-checks it (`aws:runCommand` with a script that fails unless
   `curl -fsS http://localhost/` succeeds), and on failure goes to a step
   that tags the instance `needs-attention=true` instead of just aborting;
1. summarises the instance's patch state with an `aws:executeScript` step
   (runtime `python3.12`, calling `describe_instance_patch_states` with
   boto3) and returns it as a runbook output, along with the snapshot ID.

Grow the service role with exactly the permissions the steps need. Run it
on dev with `start-automation-execution`, then break it on purpose (stop
nginx first) and confirm the failure path tags the instance.

##### Question: Failure paths

_Which step properties (`onFailure`, `maxAttempts`, `timeoutSeconds`,
`isCritical`, `nextStep`) did you use, and what does the execution report
if the health check fails but your tagging step succeeds? Is that the
status you want to alert on?_

##### Question: Snapshots are not free

_Every run leaves a snapshot. How would you stop them piling up? (Consider
a later step, Amazon Data Lifecycle Manager, and AWS Backup from module
23.)_

#### Lab 20.4.4: Schedule the runbook

- In your maintenance window template, replace the `RUN_COMMAND` patch task
  with an `AUTOMATION` task that runs `<you>-SafePatch` against the window's
  targets, passing `{{ TARGET_ID }}` as `InstanceId` and your service role.
  Check the docs for how a window passes each target to a runbook.

- Trigger the window as before and follow both the window execution and
  the automation executions it started.

- (Optional) Look at [OpsCenter](https://docs.aws.amazon.com/systems-manager/latest/userguide/OpsCenter.html).
  Add a step to the failure path that creates an OpsItem with
  `aws:executeAwsApi` (`ssm:CreateOpsItem`), linking the instance and the
  snapshot. Each OpsItem is a fraction of a cent; resolve it when you're
  done.

##### Question: Other triggers

_List three other ways to start this runbook automatically (for example
State Manager, an EventBridge rule, an AWS Config remediation, a CloudWatch
alarm action). Which would you choose to patch-and-verify every time a new
critical patch is approved, and why?_

### Retrospective 20.4

#### Question: Runbook or Step Functions

_Module 18 built workflows in Step Functions. Where do Automation runbooks
and Step Functions overlap, and where does each win? Think of running
commands on instances, approvals, rate control across targets, cost per
step and who the audience is._

#### Question: Limits

_Look up the Automation service quotas: concurrent executions, the
`aws:executeScript` time limit and nested-runbook depth. Which one would
you hit first if you ran `<you>-SafePatch` across 500 instances, and how
would you design around it?_

## Lesson 20.5: Golden AMIs with EC2 Image Builder

### Principle 20.5

*Build servers from an image that was patched, hardened and tested before
it ever took traffic, and publish it where your templates can find it.*

### Practice 20.5

Lessons 20.2 to 20.4 fixed servers after launch. The other half of
operations is to launch them right. **EC2 Image Builder** turns a parent
image into a new AMI by running **components** (AWSTOE documents with
build, validate and test phases) on a build instance, then tests the result
on a fresh instance and distributes it.

Its pieces are separate resources: a **component**, an **image recipe**
(parent image plus components plus block devices), an **infrastructure
configuration** (instance types, instance profile, subnet, security group,
logging), a **distribution configuration** (AMI name, tags, Regions,
accounts, launch permissions, SSM parameter output) and an **image
pipeline** that ties them together and runs on a schedule or on demand.

You'll build a pipeline whose parent image is the AL2023 public parameter,
which applies AWS's update and STIG hardening components plus one of your
own, and which writes the new AMI ID to an SSM parameter. Then you'll point
the fleet at that parameter.

#### Lab 20.5.1: A hardening component

- Read [How Image Builder
  works](https://docs.aws.amazon.com/imagebuilder/latest/userguide/how-image-builder-works.html),
  [AWSTOE component
  documents](https://docs.aws.amazon.com/imagebuilder/latest/userguide/toe-use-documents.html)
  and [Create a component with
  YAML](https://docs.aws.amazon.com/imagebuilder/latest/userguide/create-component-yaml.html).

- List Amazon-owned components with
  `aws imagebuilder list-components --owner Amazon` and find:
  - `update-linux`;
  - the Linux STIG hardening component. Read
    [STIG hardening
    components](https://docs.aws.amazon.com/imagebuilder/latest/userguide/ib-stig.html):
    which inputs does it take, which level is the default, and which STIG
    version does it apply to AL2023? Check with `get-component` that it
    supports your fleet's architecture (arm64 for the starter's default).
    <!-- VERIFY: the exact name and ARN of the current Linux STIG component
    (the docs list both `STIG-Build-Linux` and the older
    `-Low`/`-Medium`/`-High` variants) and whether it supports arm64 on
    AL2023. -->

- Write your own component, `<you>-baseline-linux`, as an
  `AWS::ImageBuilder::Component` with inline YAML data:
  - **build:** install `amazon-cloudwatch-agent`, set a login banner in
    `/etc/motd`, and make sure `amazon-ssm-agent` is enabled;
  - **validate:** fail the build if any of those isn't true;
  - **test:** on the test instance, check that `amazon-ssm-agent` is running
    and that `sshd` is not enabled. (Your fleet never uses SSH; an image
    that doesn't start it can't be reached that way even by mistake.)
  <!-- VERIFY: that disabling sshd doesn't break Image Builder's own
  build/test orchestration, which uses the SSM Agent. -->

##### Question: Build, validate, test

_Why does AWSTOE separate validate from test? Which phase runs on which
instance, and what does that tell you about where a test for "the service
comes back after a reboot" belongs?_

#### Lab 20.5.2: Recipe, infrastructure and distribution

Put these in one template, `<you>-image-pipeline`:

- **Image recipe** (`AWS::ImageBuilder::ImageRecipe`): parent image
  `ssm:/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-arm64`
  (or the `x86_64` one if the STIG component doesn't support arm64); the
  components `update-linux`, the STIG component at level `Medium` or `Low`,
  and yours; an encrypted `gp3` root volume. See [Use a base image
  parameter in your
  recipe](https://docs.aws.amazon.com/imagebuilder/latest/userguide/tutorial-ssm-parameters-recipe.html).

- **Build instance role and profile:** trusted by EC2, with
  `AmazonSSMManagedInstanceCore` and `EC2InstanceProfileForImageBuilder`,
  plus `s3:PutObject` on a log prefix in your bucket.

- **Infrastructure configuration**
  (`AWS::ImageBuilder::InfrastructureConfiguration`): that profile, a small
  instance type that matches the architecture, a default-VPC subnet, a
  security group with no inbound rules, `TerminateInstanceOnFailure: true`,
  and S3 logging. See [Manage infrastructure
  configurations](https://docs.aws.amazon.com/imagebuilder/latest/userguide/manage-infra-config.html).

- **Execution role:** a custom role with the `EC2ImageBuilderExecutionPolicy`
  managed policy, plus `ssm:PutParameter` on your output parameter and
  `ec2:DescribeImages`. The docs recommend a custom role over the
  service-linked role; find out why.

- **Distribution configuration**
  (`AWS::ImageBuilder::DistributionConfiguration`): one distribution for
  `us-east-2`, an AMI name containing `<you>` and
  `{{ imagebuilder:buildDate }}`, AMI tags (`owner`, `hardened=true`), and
  an SSM parameter configuration that writes `/<you>/ami/al2023-hardened`
  with data type `aws:ec2:image`. See [Create and update AMI distribution
  configurations](https://docs.aws.amazon.com/imagebuilder/latest/userguide/cr-upd-ami-distribution-settings.html).

- **Image pipeline** (`AWS::ImageBuilder::ImagePipeline`): the recipe,
  infrastructure and distribution, the execution role, image tests on, no
  schedule for now, and image scanning off.

##### Question: Where the AMI ID lives

_Compare the AMI IDs in three places: the public parameter your recipe
starts from, the parameter your pipeline writes, and the `ImageId` of a
running instance. Which ones change when, and which one does your fleet
template read?_

##### Question: The service-linked role

_The service-linked role can write parameters only under one prefix. Which
prefix, and why does using your own execution role keep your SCPs and RCPs
from module 19 in force?_

#### Lab 20.5.3: Build the image

- Start a build with `aws imagebuilder start-image-pipeline-execution`.

- Follow it: `list-image-pipeline-images`, then `get-image` on the build
  version until its status is `AVAILABLE` (or `FAILED`). Watch the build
  instance appear in `describe-instance-information` while it runs, and
  read the logs in your bucket and in the `/aws/imagebuilder/` log group.

- When it's done, read the parameter with `aws ssm get-parameter` and
  `get-parameter-history`. Describe the AMI: tags, snapshot, `ImdsSupport`
  and deprecation time (if any). Compare them with the public AL2023 AMI
  you started from.

- If the build fails, find which component and phase failed from the logs,
  fix it, bump the component or recipe version (they're immutable), and
  build again.

##### Question: Versions are immutable

_Why can't you edit a component or recipe version in place? What does that
mean for your CloudFormation template each time you change the component,
and how does semantic versioning help?_

#### Lab 20.5.4: Roll the fleet onto the new AMI

- Update the fleet stack, setting `FleetImageId` to
  `/<you>/ami/al2023-hardened` (and the instance type, if you built
  `x86_64`). Read the change set first: what happens to the instances?

- Check the new instances without opening a shell:
  - Run Command: `cat /etc/motd; systemctl is-enabled sshd`.
  - Inventory: is `amazon-cloudwatch-agent` listed now?
  - Patch Manager: scan both. How many patches are missing compared with
    Lab 20.3.2?

- Run the pipeline a second time. Does the parameter change? Does the
  fleet change without a stack update? What would make it change?

##### Question: New AMI, same stack

_The fleet template resolves the parameter when the stack is created or
updated, not continuously. How would you roll a fleet in an Auto Scaling
group onto each new image automatically? (Module 06's Instance Refresh and
the pipeline's EventBridge events are two pieces.)_

#### Lab 20.5.5: Image lifecycle policy (optional)

Every build leaves an AMI and a snapshot that cost money forever.

- Read [Manage image
  lifecycles](https://docs.aws.amazon.com/imagebuilder/latest/userguide/manage-image-lifecycles.html).

- Add an `AWS::ImageBuilder::LifecyclePolicy` for images from your recipe:
  deprecate all but the newest image, and delete all but the newest two,
  **deregistering the AMIs and deleting their snapshots**. It needs its own
  execution role with `EC2ImageBuilderLifecycleExecutionPolicy`.

- Keep AMIs tagged `keep=true` out of it, and make sure the one your
  parameter points at can't be deleted while it's in use.

##### Question: Deprecate, disable, delete

_What does each lifecycle action do to an AMI? Can running instances keep
running on a deregistered AMI, and can an Auto Scaling group launch new
ones from it?_

#### Lab 20.5.6: The unified console and Quick Setup (optional)

You've now built by hand much of what Systems Manager can set up for you.

- Read [What is the unified
  console?](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-unified-console.html),
  [Setting up for a single account and
  Region](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-setting-up-single-account-region.html)
  and [Quick
  Setup](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-quick-setup.html).
  List the roles, associations, Lambda functions and bucket that enabling it
  creates.

- If you want to see it, enable it in the console for `us-east-2` only
  (this one step needs the console), with DHMC on. Then:
  - list the new associations and compare them with yours. Which one
    collides with your inventory association?
  - use **Explore nodes** and **Review node insights** on your fleet;
  - launch a throwaway AL2023 instance with **no instance profile** and IMDSv2
    required, and see whether it becomes managed through DHMC. Terminate it.

- Disable it again from **Settings** afterwards and list what's left. Delete
  anything it leaves behind in the cleanup lab.
  <!-- VERIFY: which resources "Disable Systems Manager" removes (Quick
  Setup configuration, associations, roles, the diagnosis bucket) and
  which it leaves. -->

##### Question: By hand or by Quick Setup

_For a real organization with 50 accounts, which of this module's pieces
would you let Quick Setup or the unified console manage, and which would
you keep in your own templates? Why?_

#### Lab 20.5.7: Clean up the module

Delete in an order that avoids dependency errors, and check each step.

- **Image Builder:** delete the lifecycle policy (if any) and the
  `<you>-image-pipeline` stack. Then list your AMIs
  (`describe-images --owners self --filters Name=tag:owner,Values=<you>`)
  and deregister each with `--delete-associated-snapshots`. Deleting the
  image resources doesn't do this for you. Delete any Image Builder image
  build versions still listed (`list-images --owner Self`). Delete the
  `/<you>/ami/al2023-hardened` parameter; the stack didn't create it, so
  deleting the stack won't remove it.

- **Snapshots:** delete the snapshots `<you>-SafePatch` created
  (`describe-snapshots --owner-ids self` filtered by your tag).

- **Systems Manager resources:** delete the stacks holding your maintenance
  window, associations, baseline, documents, resource data sync and
  automation role. Deregister your baseline as the AL2023 default first
  (register the AWS predefined one again) and deregister any patch group.
  Resolve any OpsItems you created.

- **Session Manager preferences:** remove the S3 and CloudWatch settings,
  timeouts and Run As from `SSM-SessionManagerRunShell` (update it with an
  empty `inputs` block, or see [Disabling session
  logging](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-enable-and-disable-logging.html)).
  Delete the tunnel role and its CLI profile.

- **Fleet and logging:** delete the fleet stack, then empty the logging
  bucket (including the inventory sync and Image Builder log prefixes) and
  delete the logging stack. Delete the Image Builder and Run Command log
  groups the services created. Drop any Athena database and table.

- **Unified console:** if you enabled it, confirm it's disabled and remove
  what it left.

- **Check:** `describe-instances` (nothing running with your tag),
  `describe-images --owners self`, `describe-snapshots --owner-ids self`,
  `list-associations`, `describe-maintenance-windows`,
  `list-documents --filters Key=Owner,Values=Self`,
  `describe-patch-baselines --filters Key=OWNER,Values=Self`,
  `get-parameters-by-path --path /<you>/ --recursive` and
  `list-resource-data-sync`. All should be empty of your resources.

### Retrospective 20.5

#### Question: One pipeline, many accounts

_Your organization wants every account to launch only from approved
hardened AMIs. Using what you know from module 19 and this lesson, sketch
how you would build once, share the AMI to the organization or specific
OUs, publish the ID where every account can read it, and stop accounts from
launching anything else. Which pieces are Image Builder settings, and
which are organization policies?_

#### Question: Hardening trade-offs

_The STIG component applied settings you didn't write. How would you find
out which ones broke something, and how would you decide between a lower
STIG level, a custom component that reverts one setting, or a CIS
benchmark image from AWS Marketplace?_

## Further Reading

- [AWS Systems Manager Change Manager availability
  change](https://docs.aws.amazon.com/systems-manager/latest/userguide/change-manager-availability-change.html)
  and [Incident Manager availability
  change](https://docs.aws.amazon.com/incident-manager/latest/userguide/incident-manager-availability-change.html):
  what replaced them.
- [Managing nodes in hybrid and multicloud
  environments](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-hybrid-multicloud.html)
  and the [June 2026 pricing
  change](https://aws.amazon.com/about-aws/whats-new/2026/06/aws-systems-manager-multicloud-vm/)
  for non-EC2 nodes.
- [Monitoring Systems Manager events with
  EventBridge](https://docs.aws.amazon.com/systems-manager/latest/userguide/monitoring-eventbridge-events.html):
  react to association compliance, Automation status and maintenance window
  results.
- [Using native parameter support for AMI
  IDs](https://docs.aws.amazon.com/systems-manager/latest/userguide/parameter-store-ec2-aliases.html):
  launch instances directly from an `aws:ec2:image` parameter.
- [AWS Systems Manager
  pricing](https://aws.amazon.com/systems-manager/pricing/): check it before
  enabling anything billed per node or per step.
- The [Operational Excellence
  pillar](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/welcome.html)
  of the AWS Well-Architected Framework, which is where runbooks, playbooks
  and "operations as code" come from.
