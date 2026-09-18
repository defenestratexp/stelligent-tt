# Topic 5: Elastic Compute Cloud (EC2)

<!-- TOC -->

- [Topic 5: Elastic Compute Cloud (EC2)](#topic-5-elastic-compute-cloud-ec2)
  - [What changed in the 2026 edition](#what-changed-in-the-2026-edition)
  - [Exam coverage](#exam-coverage)
  - [Cost and cleanup](#cost-and-cleanup)
  - [Guidance](#guidance)
  - [Lesson 5.1: Introduction to Elastic Compute Cloud](#lesson-51-introduction-to-elastic-compute-cloud)
    - [Principle 5.1](#principle-51)
    - [Practice 5.1](#practice-51)
      - [Lab 5.1.1: Find an AMI Without Hard-Coding It](#lab-511-find-an-ami-without-hard-coding-it)
        - [Question: Why Not an AMI ID](#question-why-not-an-ami-id)
      - [Lab 5.1.2: Launch Two EC2 Instances](#lab-512-launch-two-ec2-instances)
      - [Lab 5.1.3: Move the Linux Instance to Graviton](#lab-513-move-the-linux-instance-to-graviton)
        - [Question: What Happened to the Instance](#question-what-happened-to-the-instance)
      - [Lab 5.1.4: Teardown](#lab-514-teardown)
    - [Retrospective 5.1](#retrospective-51)
      - [Question: Resource Replacement](#question-resource-replacement)
      - [Question: Pinning an AMI](#question-pinning-an-ami)
  - [Lesson 5.2: Instance Access](#lesson-52-instance-access)
    - [Principle 5.2](#principle-52)
    - [Practice 5.2](#practice-52)
      - [Lab 5.2.1: Session Manager](#lab-521-session-manager)
        - [Question: No Open Ports](#question-no-open-ports)
      - [Lab 5.2.2: Instance Metadata with IMDSv2](#lab-522-instance-metadata-with-imdsv2)
        - [Question: Why a Token](#question-why-a-token)
        - [Question: Hop Limit](#question-hop-limit)
      - [Lab 5.2.3: Elastic IP](#lab-523-elastic-ip)
        - [Question: Paying for Addresses](#question-paying-for-addresses)
      - [Lab 5.2.4: SSH, If You Must](#lab-524-ssh-if-you-must)
        - [Question: Comparing Access Methods](#question-comparing-access-methods)
    - [Retrospective 5.2](#retrospective-52)
  - [Lesson 5.3: Monitoring EC2 Instances](#lesson-53-monitoring-ec2-instances)
    - [Principle 5.3](#principle-53)
    - [Practice 5.3](#practice-53)
      - [Lab 5.3.1: Understanding Instance Metrics](#lab-531-understanding-instance-metrics)
        - [Question: Burstable Credits](#question-burstable-credits)
      - [Lab 5.3.2: Installing the CloudWatch Agent](#lab-532-installing-the-cloudwatch-agent)
        - [Question: Missing Metrics](#question-missing-metrics)
        - [Task: Private Subnet](#task-private-subnet)
      - [Lab 5.3.3: cfn-init](#lab-533-cfn-init)
    - [Retrospective 5.3](#retrospective-53)
      - [Task: Cleaner Userdata](#task-cleaner-userdata)
      - [Task: Know When It Worked](#task-know-when-it-worked)
  - [Lesson 5.4: Exploring EC2 Instance Components](#lesson-54-exploring-ec2-instance-components)
    - [Principle 5.4](#principle-54)
    - [Practice 5.4](#practice-54)
      - [Lab 5.4.1: EBS Volumes](#lab-541-ebs-volumes)
        - [Question: Device Names](#question-device-names)
      - [Lab 5.4.2: EBS Snapshot](#lab-542-ebs-snapshot)
      - [Lab 5.4.3: Attaching Snapshots](#lab-543-attaching-snapshots)
        - [Question: First Read](#question-first-read)
      - [Lab 5.4.4: Instance Snapshots](#lab-544-instance-snapshots)
        - [Question: Inherited Settings](#question-inherited-settings)
      - [Lab 5.4.5: Clean Up](#lab-545-clean-up)
    - [Retrospective 5.4](#retrospective-54)
      - [Question: Encryption by Default](#question-encryption-by-default)
      - [Question: Graviton Economics](#question-graviton-economics)
  - [Further Reading](#further-reading)

<!-- /TOC -->

## What changed in the 2026 edition

- The Cloud9 metadata lab is gone: Cloud9 is closed to new customers. Instance
  metadata is now queried from your own lab instance, and with IMDSv2 (session
  tokens) only. New Lab 5.2.2 shows why IMDSv1 is turned off.
- AMIs are never hard-coded or looked up by hand. Lab 5.1.1 finds them in the
  Systems Manager public parameters, and templates use the
  `AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>` parameter type.
- End-of-life operating systems are gone: Amazon Linux 2023 (AL2023)
  replaces Ubuntu 16.04/20.04 and Amazon Linux 1/2, and the Windows lab uses
  Windows Server 2025 and never Windows Server 2012 R2. AL2023 uses `dnf` and
  systemd.
- Lab 5.1.3 no longer "updates" to an older Windows AMI to trigger a
  replacement. It moves the Linux instance to Graviton (arm64, `t4g`), which
  shows replacement and introduces Graviton at the same time.
- Instance access starts with Session Manager (no inbound ports, no keys).
  SSH is optional, limited to your own IP address, and compared with EC2
  Instance Connect. The `echo -e "rsa blob"` key workaround is gone.
- Instances use `t3`/`t4g` types and `gp3` volumes, and launch templates set
  IMDSv2 explicitly.
- The retired EC2 monitoring scripts are no longer mentioned; the CloudWatch
  agent is installed from the AL2023 package repository. The Ubuntu
  `cfn-hup` workaround is replaced by the `aws-cfn-bootstrap` package and a
  systemd service.
- New: public IPv4 address charges, burstable CPU credits, NVMe device
  names, AMI cleanup (deregistering an AMI leaves its snapshots unless you ask
  otherwise), and a cleanup lab that checks for leftovers.
- Labs run in your lab account in `us-east-2` through the `lab` profile.
- The unlabelled code fence in Retrospective 5.3 is fixed.

## Exam coverage

| Exam | Domain / task statement |
|---|---|
| CLF-C02 | Domain 3: Cloud Technology and Services (compute, storage) |
| SAA-C03 | Domain 1: Design Secure Architectures (1.1 secure access to AWS resources; 1.3 data security controls) |
| SAA-C03 | Domain 3: Design High-Performing Architectures (3.1 storage; 3.2 compute) |
| SAA-C03 | Domain 4: Design Cost-Optimized Architectures (4.1 storage; 4.2 compute) |
| SOA-C03 | Domain 1: Monitoring, Logging, Analysis, Remediation, and Performance Optimization |
| SOA-C03 | Domain 2: Reliability and Business Continuity (snapshots, AMIs) |
| SOA-C03 | Domain 3: Deployment, Provisioning, and Automation |
| SOA-C03 | Domain 4: Security and Compliance (IMDSv2, instance roles, Session Manager) |

## Cost and cleanup

- A `t3.micro` or `t4g.micro` running Linux costs about a cent per hour.
  Stop or delete your stack between sessions.
- **Windows** instances (Lab 5.1.2 only) add a per-hour license charge and
  need a larger instance type. Delete the Windows instance as soon as the lab
  asks you to.
- **Public IPv4 addresses** cost $0.005 per hour each, whether attached to a
  running instance or an idle Elastic IP. Instances in the default VPC get one
  automatically. An Elastic IP that isn't attached is charged too; release it.
- `t3` and `t4g` instances launch in *unlimited* credit mode. An instance that
  runs at high CPU for a long time is billed for surplus credits.
- **EBS** volumes, snapshots and the snapshots behind your AMIs are billed per
  GB-month until you delete them, even after the instance is gone.
- **Interface VPC endpoints** (the optional private-subnet task) cost about
  $0.01 per hour per endpoint per Availability Zone, plus data processing.
  <!-- VERIFY: interface endpoint hourly price in us-east-2; the PrivateLink pricing page no longer shows it in static text. -->
- Detailed monitoring and custom metrics from the CloudWatch agent are billed
  per metric. The labs publish only a handful.
- Lab 5.1.4 deletes the Lesson 5.1 stack. Lab 5.4.5 removes everything else
  this module creates, including AMIs, snapshots, key pairs and Elastic IPs
  that don't belong to a stack.

## Guidance

- Use the
  [Amazon EC2 User Guide](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html),
  the [Amazon EBS User Guide](https://docs.aws.amazon.com/ebs/latest/userguide/what-is-ebs.html)
  and the
  [CloudFormation template reference](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/introduction.html).
  Don't copy CloudFormation templates from the internet at large. Many
  still launch EOL AMIs, allow SSH from anywhere and leave IMDSv1 on.

- Use the
  [AWS CLI](https://docs.aws.amazon.com/cli/latest/reference/ec2/)
  rather than the console unless a lab says otherwise. Your `lab` profile sets
  the region (`us-east-2`), so commands don't need `--region`.

- Use every link in this document and notice how the AWS documentation is
  laid out.

- Only specify the configuration your resources need. Don't get lost in all
  the options you can add.

- Name stacks and tag resources with your identifier, as in earlier modules.
  Create a branch for each lesson and push your templates and scripts to it.

## Lesson 5.1: Introduction to Elastic Compute Cloud

### Principle 5.1

*EC2 is one of the fundamental building blocks of AWS.*

### Practice 5.1

Like IAM, EC2 consists of a set of services and resources. Most are organized
around instances: virtual servers launched from an Amazon Machine Image (AMI)
onto an instance type. Around them sit launch templates, security groups,
network interfaces, Elastic IP addresses, EBS volumes and snapshots. Together
they provide flexible compute and storage capacity.

Of note:

- EC2 is the gateway for many workloads into AWS.

- EC2 also runs underneath other services. Amazon ECS and Amazon EKS
  run containers on EC2 instances unless you choose Fargate, and many managed
  services run on EC2 capacity you never see.

- AWS builds its own Arm processors, Graviton. Arm instance types have a `g`
  in the family name (`t4g`, `m8g`) and often cost less for the same work.

#### Lab 5.1.1: Find an AMI Without Hard-Coding It

AMI IDs are different in every region and change every time the image is
rebuilt. AWS publishes the current IDs as
[Systems Manager public parameters](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/finding-an-ami-parameter-store.html).
Using the CLI:

- List the Amazon Linux parameter names under
  `/aws/service/ami-amazon-linux-latest` (see
  [Calling AMI public parameters](https://docs.aws.amazon.com/systems-manager/latest/userguide/parameter-store-public-parameters-ami.html)).
  Find the AL2023 parameters for `x86_64` and `arm64`. Which parameters in
  that list point at operating systems you should no longer launch?

- Find the parameter for **Windows Server 2025 English Full Base** under
  `/aws/service/ami-windows-latest`.

- Get the AMI ID behind each parameter, then use `aws ec2 describe-images` to
  show each AMI's name, architecture, owner, creation date, deprecation date
  and `ImdsSupport` value.

Save your commands (not their output) in your repository.

##### Question: Why Not an AMI ID

_AL2023 AMIs are
[deprecated 90 days after release](https://docs.aws.amazon.com/linux/al2023/ug/ec2.html#ami-deprecation).
What happens to a template with a hard-coded AMI ID after a few months, and in
another region? What does using the parameter give up?_

#### Lab 5.1.2: Launch Two EC2 Instances

Create a CloudFormation template that launches two instances when the stack
is created:

- Use a launch template,
  [AWS::EC2::LaunchTemplate](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-ec2-launchtemplate.html),
  for the attributes the instances share instead of repeating them on each
  [AWS::EC2::Instance](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-ec2-instance.html).
  In the launch template, require IMDSv2 in
  [MetadataOptions](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-properties-ec2-launchtemplate-metadataoptions.html)
  and give the root volume the `gp3` type.

- Create two instance resources from that launch template, each with its own
  AMI and instance type:

  - an AL2023 (`x86_64`) instance on `t3.micro`;
  - a Windows Server 2025 instance. Windows needs more memory; check the
    [Windows AMI reference](https://docs.aws.amazon.com/ec2/latest/windows-ami-reference/winserver-ami-changes.html)
    and pick a `t3` size that will boot it comfortably.

- Take each AMI as a template parameter of type
  `AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>` whose default is the
  public parameter name from Lab 5.1.1. See
  [SSM parameter types](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cloudformation-supplied-parameter-types.html#cloudformation-supplied-parameter-types-ssm-parameter-types).

- Launch the instances into the default VPC. Add no security group rules and
  no key pair yet.

Create the stack:

- Write a script that uses the AWS CLI to create the stack and then uses a
  [waiter](https://docs.aws.amazon.com/cli/latest/reference/cloudformation/wait/)
  so that the script exits only when CloudFormation has finished.

- Use the CLI to describe the stack's resources, then describe each instance.
  Which AMI ID did CloudFormation resolve for each one? Where can you see it
  on the stack?

#### Lab 5.1.3: Move the Linux Instance to Graviton

Change the Linux instance to run on Graviton:

- Point its AMI parameter at the AL2023 `arm64` parameter and change its
  instance type to `t4g.micro`. Can you change only one of the two? Try it
  with a
  [change set](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-changesets.html)
  first and read what CloudFormation plans to do.

- Update your stack.

- Query the stack's events using the CLI.

##### Question: What Happened to the Instance

_What happened to your original Linux instance? Compare its instance ID
before and after, and read the `Replacement` column of your change set._

#### Lab 5.1.4: Teardown

There is usually some delay between initiating an instance's termination and
the instance disappearing altogether.

- Delete your stack. Immediately afterwards, query your instances' states.
  How long do terminated instances stay visible?

- Confirm that no Windows instance is left running.

### Retrospective 5.1

#### Question: Resource Replacement

_When updating a stack containing an EC2 instance,
[what other changes](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-update-behaviors.html)
cause the same thing to happen as in Lab 5.1.3? Look at the `LaunchTemplate`
property in particular: what happens to an instance when you change anything
in its launch template and the instance follows the latest version?_

#### Question: Pinning an AMI

_A parameter default of `.../al2023-ami-kernel-default-x86_64` resolves to a
new AMI when AWS publishes one. Does your running instance change? When does
the new value take effect, and how would you keep a production stack on a
known AMI while still avoiding hard-coded IDs?_

## Lesson 5.2: Instance Access

### Principle 5.2

*Reach instances through AWS APIs you can control with IAM and log, not
through open ports and long-lived keys.*

### Practice 5.2

You need to get onto instances to develop and debug provisioning. The old
answer was SSH with a key pair and port 22 open.
[Session Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html)
gives you a shell through the Systems Manager agent instead: no inbound
rules, no keys, IAM decides who may connect, and sessions can be logged.
You'll set it up first, use it to explore instance metadata, then look at
Elastic IPs and at SSH for comparison. Module 04 covers reaching instances
in private subnets with EC2 Instance Connect Endpoint, and module 20 covers
Systems Manager in depth.

Start again from your Lesson 5.1 template (you deleted the stack in Lab
5.1.4) and keep the Linux instance on Graviton.

#### Lab 5.2.1: Session Manager

- Remove the Windows instance and its parameter from your template, and
  create the stack again.

- Create an IAM role that EC2 can assume, attach the AWS managed policy
  `AmazonSSMManagedInstanceCore`, and create an instance profile for it.
  Attach the instance profile in your launch template. See
  [Instance profile permissions for Systems Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/setup-instance-permissions.html)
  and
  [IAM roles for Amazon EC2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html).

- Give the launch template a security group with **no inbound rules**.

- Update the stack. Then confirm the instance is registered with
  `aws ssm describe-instance-information`.

- Install the
  [Session Manager plugin](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html)
  for the CLI and connect with `aws ssm start-session`. Which user are you,
  and how do you get to `ec2-user`?

The SSM Agent comes preinstalled on AL2023 and on the Windows Server AMIs.
If `describe-instance-information` shows nothing after a few minutes, see
[Troubleshooting managed node availability](https://docs.aws.amazon.com/systems-manager/latest/userguide/fleet-manager-troubleshooting-managed-nodes.html).

##### Question: No Open Ports

_Your security group allows nothing in. How does the session reach the
instance? What does the instance need instead, and what would change in a
private subnet with no NAT gateway?_

#### Lab 5.2.2: Instance Metadata with IMDSv2

Every instance can read facts about itself from the
[Instance Metadata Service](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-metadata.html)
(IMDS) at a link-local address. From your Session Manager shell:

- Request `meta-data/` the old way, with a plain `curl` and no token. What
  HTTP status do you get?

- Retrieve the data the
  [IMDSv2 way](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instancedata-data-retrieval.html):
  get a session token with a `PUT`, then send it with each request. Use it to
  find:

  - the AMI the instance was launched from;
  - the instance type;
  - the public IPv4 address;
  - the security groups the instance is associated with;
  - the subnet ID (look under the network interface's MAC address);
  - the name of the IAM role, and what the credentials path returns.

- Find the same information with the `ec2-metadata` tool that ships with
  AL2023.

- Look at the instance's metadata options with `aws ec2 describe-instances`,
  and at your account's defaults with `aws ec2 get-instance-metadata-defaults`.
  Which setting required IMDSv2: your launch template, the AMI, or both?

Save your queries (not the outputs) in your repository.

##### Question: Why a Token

_What kind of attack does IMDSv2's `PUT`-then-token design stop? Why is the
credentials path the thing an attacker wants? Read
[IMDSv2 and the transition](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-metadata-transition-to-version-2.html)._

##### Question: Hop Limit

_What is the `HttpPutResponseHopLimit`, what value did your instance get, and
why would a container on the instance need a value of 2? How would you
[enforce IMDSv2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/configuring-IMDS-new-instances.html)
for every new instance in an account, or across an organization?_

#### Lab 5.2.3: Elastic IP

An Elastic IP (EIP) address is a static public IPv4 address reserved by your
account. If an instance fails, you can move the EIP to a replacement and
clients keep using the same address.

- Update the template to create an EIP and associate it with your instance.

- Create a stack output with the EIP's address, update the stack, and fetch
  the output with the CLI.

Try pinging that address. Does it work?

- Add an inbound rule for
  [ICMP](https://en.wikipedia.org/wiki/Internet_Control_Message_Protocol)
  echo requests from **your own public IP address only** (a `/32`). Pass the
  address in as a stack parameter.

- Update the stack.

Can you ping your instance now? If not, troubleshoot and fix the issue in
your template.

##### Question: Paying for Addresses

_Before you added the EIP, did the instance already have a public IPv4
address? What happened to that address when you associated the EIP? Read the
[public IPv4 pricing](https://aws.amazon.com/vpc/pricing/): what does each
address cost per month, and what does an EIP cost when it isn't attached?_

#### Lab 5.2.4: SSH, If You Must

Plenty of tools and colleagues still expect SSH. Do it once, safely, so you
can compare:

- Create an
  [EC2 key pair](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html)
  of type `ed25519`, either with `aws ec2 create-key-pair` (write the private
  key straight to a file with `--query` and `--output text`, then `chmod 600`
  it) or as an
  [AWS::EC2::KeyPair](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-ec2-keypair.html)
  resource. If you use the resource, where does the private key end up?

- Add the key pair to your launch template and allow TCP port 22 from your
  `/32` only. Update the stack. What happened to the instance, and why?

- SSH in as `ec2-user`.

- Now try
  [EC2 Instance Connect](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-instance-connect-methods.html)
  with `aws ec2-instance-connect ssh`. It pushes a one-time public key through
  the EC2 API. Which IAM permission does it need, and does it still need port
  22 open?

- Remove the port 22 rule and the key pair from your template and update
  the stack. Leave the ICMP rule for now.

##### Question: Comparing Access Methods

_Compare SSH with a key pair, EC2 Instance Connect and Session Manager: what
has to be open on the network, what secret has to be managed, how access is
granted and revoked, and what gets logged. When would you still choose SSH?_

### Retrospective 5.2

For more on connection problems, see
[Troubleshoot connecting to your instance](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/TroubleshootingInstancesConnecting.html).
Session Manager can also forward ports (for example, RDP to a Windows
instance) and carry SSH, so tools that expect SSH can still avoid an open
port 22. Look up how in the Session Manager documentation.

## Lesson 5.3: Monitoring EC2 Instances

### Principle 5.3

*Monitoring your instances is critical for maintaining healthy workloads.*

### Practice 5.3

Monitoring is an important part of maintaining the reliability, availability
and performance of your EC2 instances. In AWS the goal is usually to replace
a malfunctioning server rather than nurse it, but you still need to know that
it is malfunctioning.

#### Lab 5.3.1: Understanding Instance Metrics

Continue with your template: one AL2023 instance, Session Manager, no SSH.
Read and re-read
[Monitor Amazon EC2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/monitoring_ec2.html).

A small set of metrics is collected for every instance. The
[CloudWatch agent](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Install-CloudWatch-Agent.html)
collects an
[extended set](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/metrics-collected-by-CloudWatch-agent.html).

- Make sure the instance is in the default VPC and update the stack if you
  changed anything.

- Use `aws cloudwatch list-metrics` to see which metrics exist for your
  instance, and fetch a few of them with `aws cloudwatch get-metric-data`.
  Look at the same data in the console.

- What is the period of the default metrics? What does
  [detailed monitoring](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/manage-detailed-monitoring.html)
  change, and what does it cost?

Record the default metrics.

##### Question: Burstable Credits

_Your `t4g.micro` reports `CPUCreditBalance` and related metrics. What are
CPU credits, what does
[unlimited mode](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-performance-instances-unlimited-mode-concepts.html)
do when they run out, and which metric shows credits you'll be billed for?_

#### Lab 5.3.2: Installing the CloudWatch Agent

Install the CloudWatch agent on that same instance, using two more important
features of instance provisioning: the instance profile you created in Lab
5.2.1, and
[user data](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html).
If you get stuck, open a Session Manager shell and read the cloud-init logs
mentioned in the user data docs.

- Add the AWS managed policy `CloudWatchAgentServerPolicy` to your instance
  role.

- Modify your launch template so that user data installs the agent from the
  AL2023 package repository (`amazon-cloudwatch-agent`, with `dnf`), then
  configures and starts it. See
  [Manual installation on Amazon EC2](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/manual-installation.html).
  Collect at least memory and disk utilization.

- Keep the agent configuration out of the user data script: store it in a
  Parameter Store parameter created by your stack, and have the agent
  fetch it from there.

- Recreate the stack so the
  [user data runs](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/user-data.html).
  Why doesn't an update to the user data alone do it?

Compare the metrics now available with those from Lab 5.3.1. Record your
results.

##### Question: Missing Metrics

_Why can't EC2 report memory or disk-space utilization without an agent,
when it can report CPU and network?_

##### Task: Private Subnet

The default VPC has only public subnets. Copy your template, add a private
subnet (no route to an internet gateway, no NAT gateway) and launch the
instance there. Add what's needed so that Session Manager still works and the
agent can still publish metrics. See
[VPC endpoints for Systems Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/setup-create-vpc.html)
and
[CloudWatch and interface VPC endpoints](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch-and-interface-VPC.html).
How does the instance install the agent package with no internet access?
(Where are the AL2023 package repositories hosted?) Note
the per-hour cost of each endpoint you add, and delete this stack when you're
done.

#### Lab 5.3.3: cfn-init

User data is immensely useful for provisioning instances as they launch, but
long scripts detailing a series of complex actions get messy. One way to
organize them is the `Metadata` attribute with
[AWS::CloudFormation::Init](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-init.html)
and the
[cfn-init helper script](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/cfn-init.html).

- Go back to your public-subnet template. Add
  [Metadata](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/metadata-section-structure.html)
  to your instance, and move the logic that installs, configures and starts
  the CloudWatch agent into `AWS::CloudFormation::Init` (`packages`, `files`,
  `commands` and `services`).

- Reduce your user data to installing the `aws-cfn-bootstrap` package with
  `dnf` and calling `cfn-init`. Don't rely on the helper scripts being
  preinstalled: they aren't on the AL2023 minimal AMI.

- Add [cfn-hup](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/cfn-hup.html)
  so that a change to the metadata is applied without replacing the instance.
  AL2023 uses systemd: make sure `cfn-hup` runs as a systemd service (the
  `services` key supports `systemd`) and check with `systemctl status
  cfn-hup`.
  <!-- VERIFY: whether the AL2023 aws-cfn-bootstrap package ships a cfn-hup systemd unit or the student must write one via the files key. -->

- Recreate your stack.

Verify that the metrics you saw in Lab 5.3.2 are still being collected. Then
change something in the agent configuration, update the stack, and watch
`cfn-hup` apply it.

### Retrospective 5.3

#### Task: Cleaner Userdata

With YAML's multi-line string syntax you can embed user data scripts without
`\n` escapes and other syntactic mess that makes them hard to read, debug and
reuse. If you haven't done this already, try it and repeat Lab 5.3.2.

> Hint: when you want to put several commands into UserData in a YAML
> template, use this format to keep it readable:

```yaml
UserData:
  Fn::Base64: !Sub |
    #!/bin/bash
    # bash code goes here just like a normal script.
    echo "Running in region ${AWS::Region}"
    env | sort
```

In a launch template, `UserData` sits under `LaunchTemplateData`.

#### Task: Know When It Worked

Besides seeing evidence that cfn-init worked, you can combine it with
[cfn-signal](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/cfn-signal.html)
and a
[CreationPolicy](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-attribute-creationpolicy.html)
so that the stack only reports success when provisioning succeeded. Add that
to your template, then break the agent configuration on purpose and watch the
stack roll back.

## Lesson 5.4: Exploring EC2 Instance Components

### Principle 5.4

*Instances are constructed from other independently manageable AWS
components.*

### Practice 5.4

An EC2 instance is its own small ecosystem. It is created from an AMI, sized
by an instance type, and can take on an IAM role, a static IP address, extra
network interfaces and volumes, and security groups. Many of these outlive
the instance, and so do their bills.

Continue with your existing stack.

#### Lab 5.4.1: EBS Volumes

Add a second
[Elastic Block Store](https://docs.aws.amazon.com/ebs/latest/userguide/what-is-ebs.html)
(EBS) volume to your instance.

- In CloudFormation, create an encrypted `gp3`
  [AWS::EC2::Volume](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-ec2-volume.html)
  and attach it with an
  [AWS::EC2::VolumeAttachment](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-ec2-volumeattachment.html).
  The volume must be in the instance's Availability Zone; get it from the
  instance rather than hard-coding it.

- Modify cfn-init (or user data) to format the new volume, mount it and add
  it to `/etc/fstab` so it survives a reboot. The attachment may happen after
  your script starts; make the script wait for the device.

- Recreate your stack.

Use Session Manager to verify that the volume is mounted.

##### Question: Device Names

_You attached the volume as `/dev/sdf` (or similar). What is it called inside
the instance, and why? Read
[device names on Linux instances](https://docs.aws.amazon.com/ebs/latest/userguide/nvme-ebs-volumes.html).
Why should `/etc/fstab` refer to the file system by UUID, and what does the
`nofail` option protect you from?_

#### Lab 5.4.2: EBS Snapshot

Create a file on the second volume and take an EBS snapshot.

- Update cfn-init (or user data) to write a simple text file to the new
  volume.

- Recreate the stack.

- Use the CLI to create a
  [snapshot](https://docs.aws.amazon.com/ebs/latest/userguide/ebs-snapshots.html)
  of the volume, and a waiter to know when it's complete.

Use the CLI to describe the snapshot and save the output. Is a snapshot of a
mounted, in-use volume safe to restore? What would make it safer?

#### Lab 5.4.3: Attaching Snapshots

Repeat Lab 5.4.1, but create the volume from your snapshot. A replacement
instance can then be rebuilt from a recent snapshot, reducing or avoiding
data loss.

- Add a stack parameter for the snapshot ID.

- Modify the template so that the second volume is created from that
  snapshot.

- Update the stack.

Open a session on the instance. *Can you find the file that you wrote to the
second volume?*

##### Question: First Read

_A volume created from a snapshot is available immediately, but the first
read of each block is slower. Why? What are your options when that matters,
and what do they cost? See
[Initialize Amazon EBS volumes](https://docs.aws.amazon.com/ebs/latest/userguide/initalize-volume.html)._

#### Lab 5.4.4: Instance Snapshots

Besides snapshots of single volumes, you can capture a whole instance as an
AMI.

- Open a session and add a file to `ec2-user`'s home directory.

- Use the CLI to
  [create an AMI](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/creating-an-ami-ebs.html)
  from the instance. By default the instance reboots; what does
  `--no-reboot` trade away? Wait for the image to be available.

- Pass the new AMI ID to your stack's AMI parameter. It is an SSM parameter
  type, so what do you need to change to pass an AMI ID directly? Update the
  stack.

Open a session on the new instance and check for the file in the home
directory.

##### Question: Inherited Settings

_Run `aws ec2 describe-images` on your AMI. What snapshots does it
reference? Did it keep the `ImdsSupport` value of the AL2023 image you
started from, and does it matter given your launch template?_

#### Lab 5.4.5: Clean Up

Tear down everything this module created:

- Delete your stacks, including the private-subnet stack if you built it.

- Deregister your AMI and delete its snapshots. `aws ec2 deregister-image`
  keeps them unless you pass `--delete-associated-snapshots`. See
  [Deregister an AMI](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/deregister-ami.html).

- Delete the snapshot from Lab 5.4.2 and any key pair you created outside a
  stack.

- Check that nothing is left:
  `aws ec2 describe-instances` (no non-terminated instances),
  `describe-volumes`, `describe-snapshots --owner-ids self`,
  `describe-images --owners self`, `describe-addresses` (no Elastic IPs)
  and `describe-key-pairs`. Delete any CloudWatch log groups and Parameter
  Store parameters you created by hand.

### Retrospective 5.4

Read the
[EBS volume types](https://docs.aws.amazon.com/ebs/latest/userguide/ebs-volume-types.html)
and
[instance store](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/InstanceStorage.html)
documentation to learn more about these components. Note what `gp3` gives you
without extra charge (a baseline of 3,000 IOPS and 125 MiB/s at any size) and
what `gp2` doesn't.

#### Question: Encryption by Default

_You encrypted your volume in the template. How would you make sure every new
volume and snapshot copy in the account is encrypted, even when someone
forgets? What happens to snapshots and AMIs made from encrypted volumes? See
[EBS encryption by default](https://docs.aws.amazon.com/ebs/latest/userguide/encryption-by-default.html)._

#### Question: Graviton Economics

_Compare the on-demand price of `t3.micro` and `t4g.micro` in `us-east-2`,
and of an `m7i.large` and `m7g.large`. What has to be true of your software
before you can move to Graviton, and what in this module would have broken if
you had installed an `x86_64`-only package?_

## Further Reading

- Instance types vary radically to support different workloads. Become
  familiar with the
  [instance types](https://docs.aws.amazon.com/ec2/latest/instancetypes/instance-types.html),
  their naming, and the fact that they change over time.

- Instance types shouldn't be confused with
  [purchasing options](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/instance-purchasing-options.html):
  On-Demand, Savings Plans, Reserved Instances, Spot Instances, Dedicated
  Hosts and Dedicated Instances, and capacity reservations.

- The
  [AWS Graviton Technical Guide](https://github.com/aws/aws-graviton-getting-started)
  covers porting software to Arm, language by language.

- [AWS Compute Optimizer](https://docs.aws.amazon.com/compute-optimizer/latest/ug/what-is-compute-optimizer.html)
  recommends instance types and EBS volume settings from your actual usage.

- [Amazon Linux 2023](https://docs.aws.amazon.com/linux/al2023/ug/what-is-amazon-linux.html)
  differs from Amazon Linux 2 in package management, release cadence and
  defaults. Read the comparison before migrating older instructions.
