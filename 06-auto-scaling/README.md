# Topic 6: Auto Scaling

<!-- TOC -->

- [Topic 6: Auto Scaling](#topic-6-auto-scaling)
  - [What changed in the 2026 edition](#what-changed-in-the-2026-edition)
  - [Exam coverage](#exam-coverage)
  - [Cost and cleanup](#cost-and-cleanup)
  - [Guidance](#guidance)
  - [Lesson 6.1: Launch Templates and Auto Scaling Groups](#lesson-61-launch-templates-and-auto-scaling-groups)
    - [Principle 6.1](#principle-61)
    - [Practice 6.1](#practice-61)
      - [Lab 6.1.1: ASG from an Instance, the Old Way](#lab-611-asg-from-an-instance-the-old-way)
        - [Question: What Failed](#question-what-failed)
      - [Lab 6.1.2: Launch Template from an Instance](#lab-612-launch-template-from-an-instance)
        - [Question: Resources](#question-resources)
        - [Question: Parameters](#question-parameters)
      - [Lab 6.1.3: Launch Template and ASG in CloudFormation](#lab-613-launch-template-and-asg-in-cloudformation)
        - [Question: ASG From Existing Instance](#question-asg-from-existing-instance)
        - [Question: IMDSv2](#question-imdsv2)
      - [Lab 6.1.4: Launch Template Changes](#lab-614-launch-template-changes)
        - [Question: Stack Updates](#question-stack-updates)
        - [Question: Template Versions](#question-template-versions)
        - [Question: Replacement Instance](#question-replacement-instance)
      - [Lab 6.1.5: Know When It Worked](#lab-615-know-when-it-worked)
        - [Question: Signal Target](#question-signal-target)
        - [Question: Failed Signal](#question-failed-signal)
      - [Lab 6.1.6: ASG Update Policy](#lab-616-asg-update-policy)
        - [Question: Instance Updating](#question-instance-updating)
        - [Question: Changing Architecture](#question-changing-architecture)
      - [Lab 6.1.7: Clean Up](#lab-617-clean-up)
        - [Question: Stack Tear Down](#question-stack-tear-down)
    - [Retrospective 6.1](#retrospective-61)
      - [Question: Private Subnets](#question-private-subnets)
  - [Lesson 6.2: Health Checks](#lesson-62-health-checks)
    - [Principle 6.2](#principle-62)
    - [Practice 6.2](#practice-62)
      - [Lab 6.2.1: Use awscli to Describe an ASG](#lab-621-use-awscli-to-describe-an-asg)
        - [Question: Filtering Output](#question-filtering-output)
        - [Question: Instance Timing](#question-instance-timing)
      - [Lab 6.2.2: Scale Out](#lab-622-scale-out)
        - [Question: Desired Count](#question-desired-count)
        - [Question: Update Delay](#question-update-delay)
      - [Lab 6.2.3: Manual Interference](#lab-623-manual-interference)
        - [Question: Launch Before Terminate](#question-launch-before-terminate)
      - [Lab 6.2.4: Troubleshooting Features](#lab-624-troubleshooting-features)
    - [Retrospective 6.2](#retrospective-62)
      - [Question: CloudWatch](#question-cloudwatch)
  - [Lesson 6.3: Scaling Policies](#lesson-63-scaling-policies)
    - [Principle 6.3](#principle-63)
    - [Practice 6.3](#practice-63)
      - [Lab 6.3.1: Simple Scale-Out](#lab-631-simple-scale-out)
        - [Question: Alarm Period](#question-alarm-period)
        - [Question: Scaling Interval](#question-scaling-interval)
        - [Question: Scale-In](#question-scale-in)
      - [Lab 6.3.2: Simple Scale-In](#lab-632-simple-scale-in)
        - [Question: Instance Count](#question-instance-count)
        - [Question: Termination Order](#question-termination-order)
        - [Question: Termination Policy](#question-termination-policy)
      - [Lab 6.3.3: Target Tracking Policy](#lab-633-target-tracking-policy)
        - [Question: Configuration Complexity](#question-configuration-complexity)
        - [Question: Scale-Out Delay](#question-scale-out-delay)
        - [Question: Scale-In Delay](#question-scale-in-delay)
      - [Lab 6.3.4: Target Tracking Scale-In](#lab-634-target-tracking-scale-in)
        - [Question: Changing Delay](#question-changing-delay)
    - [Retrospective 6.3](#retrospective-63)
      - [Question: Burstable Instances](#question-burstable-instances)
  - [Lesson 6.4: Updating and Optimizing Groups](#lesson-64-updating-and-optimizing-groups)
    - [Principle 6.4](#principle-64)
    - [Practice 6.4](#practice-64)
      - [Lab 6.4.1: Instance Refresh from the CLI](#lab-641-instance-refresh-from-the-cli)
        - [Question: Skip Matching](#question-skip-matching)
        - [Question: Drift](#question-drift)
      - [Lab 6.4.2: Instance Refresh from CloudFormation](#lab-642-instance-refresh-from-cloudformation)
        - [Question: Rolling Update vs Instance Refresh](#question-rolling-update-vs-instance-refresh)
        - [Question: Readiness](#question-readiness)
      - [Lab 6.4.3: Mixed Instances and Spot](#lab-643-mixed-instances-and-spot)
        - [Question: What Launched](#question-what-launched)
        - [Question: One Template, Two Architectures](#question-one-template-two-architectures)
        - [Question: Interruptions](#question-interruptions)
      - [Lab 6.4.4: Warm Pools](#lab-644-warm-pools)
        - [Question: Cold and Warm Starts](#question-cold-and-warm-starts)
        - [Question: What You Pay For](#question-what-you-pay-for)
      - [Lab 6.4.5: Clean Up](#lab-645-clean-up)
    - [Retrospective 6.4](#retrospective-64)
      - [Question: Choosing an Update Mechanism](#question-choosing-an-update-mechanism)
  - [Further Reading](#further-reading)

<!-- /TOC -->

## What changed in the 2026 edition

- Launch configurations are gone from the labs. Accounts created on or after
  October 1, 2024 can't create them by any method, so the old "create an ASG
  from an instance" lab now fails on purpose (Lab 6.1.1). Every group in this
  module uses a launch template.
- Instances run Amazon Linux 2023, looked up from the SSM public parameter,
  on t3 and t4g instance types, with IMDSv2 required and no SSH: you connect
  with Session Manager, and the security group has no inbound rules.
- New Lab 6.1.5: `cfn-signal` and `CreationPolicy` done correctly on AL2023,
  including installing `aws-cfn-bootstrap` with `dnf` and signalling the Auto
  Scaling group's logical ID.
- New Lesson 6.4: Instance Refresh (from the CLI and through the
  CloudFormation `AutoScalingInstanceRefresh` update policy), instance
  maintenance policies, mixed instances groups with Spot, and warm pools.
- Lesson 6.3 covers detailed monitoring, default instance warmup and burstable
  CPU credits, and generates load with `stress-ng` through Systems Manager
  instead of SSH.
- Labs use the lab region (`us-east-2`) and the `lab` profile. CloudFormation
  links point at the new Template Reference guide.

## Exam coverage

| Exam | Domain / task statement |
|---|---|
| SAA-C03 | Domain 2: Design Resilient Architectures (2.1 scalable architectures, 2.2 highly available architectures, immutable infrastructure) |
| SAA-C03 | Domain 3: Design High-Performing Architectures (3.2 elastic compute) |
| SAA-C03 | Domain 4: Design Cost-Optimized Architectures (4.2 cost-optimized compute: Spot, scaling strategies, hibernation) |
| SOA-C03 | Domain 2: Reliability and Business Continuity (2.1 scalability and elasticity, 2.2 highly available environments) |
| SOA-C03 | Domain 3: Deployment, Provisioning, and Automation (3.1 CloudFormation, deployment strategies, deployment issues) |
| SOA-C03 | Domain 1: Monitoring, Logging, Analysis, Remediation, and Performance Optimization (CloudWatch alarms and metrics) |

## Cost and cleanup

- A t3.micro in `us-east-2` costs about a cent an hour, and a t4g.micro a
  little less. Each instance also has a **public IPv4 address**, billed at
  $0.005 per hour. A group of two left running for a month costs roughly $20.
- **Detailed monitoring** (Lesson 6.3) is billed per metric, a few cents per
  instance per day. It stops when the instances do.
- t3 and t4g instances start in *unlimited* credit mode. Running `stress-ng`
  for a few minutes is fine; leaving it running for hours can add surplus
  CPU credit charges.
- Instances in a **warm pool** (Lab 6.4.4) are stopped, so you pay only for
  their EBS volumes, but the pool refills itself as you use it. Delete the
  warm pool with the stack.
- Nothing in this module has a large hourly charge: no NAT gateways, load
  balancers or KMS keys. The risk is forgetting a group, because an Auto
  Scaling group replaces any instance you terminate by hand. Delete the
  **group** (or its stack), not the instances.
- Lab 6.1.7 removes everything Lesson 6.1 created; Lab 6.4.5 removes
  everything else.

## Guidance

- Explore the official docs! See the EC2 Auto Scaling
  [User Guide](https://docs.aws.amazon.com/autoscaling/ec2/userguide/what-is-amazon-ec2-auto-scaling.html),
  [API Reference](https://docs.aws.amazon.com/autoscaling/ec2/APIReference/Welcome.html),
  [CLI Reference](https://docs.aws.amazon.com/cli/latest/reference/autoscaling/index.html),
  and
  [CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-autoscaling-autoscalinggroup.html)
  docs.

- Avoid using other sites like stackoverflow.com for answers \-- part
  of the skill set you're building is finding answers straight from
  the source, AWS. Most Auto Scaling tutorials on the web use launch
  configurations and Amazon Linux 2; neither works as written in a new
  account.

- Explore your curiosity. Try to understand why things work the way
  they do. Read more of the documentation than just what you need to
  find the answers.

- Use the `lab` profile. It sets the lab region (`us-east-2`), so the CLI
  commands in this module don't need `--region`. Include your identifier in
  stack names, resource names and tags.

- Look up AMIs with the SSM public parameter
  `/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64`
  (or `-arm64` for Graviton), through a CloudFormation
  [SSM parameter type](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cloudformation-supplied-parameter-types.html#cloudformation-supplied-parameter-types-ssm-parameter-types).
  Never hard-code an AMI ID.

- Don't open SSH. Give instances an instance profile with the
  `AmazonSSMManagedInstanceCore` managed policy and connect with
  [Session Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html),
  or run commands with
  [Run Command](https://docs.aws.amazon.com/systems-manager/latest/userguide/run-command.html).
  AL2023 ships with the SSM Agent. The instances need a route to the
  Systems Manager endpoints: a public subnet with a public IPv4 address (the
  default VPC works) or the VPC endpoints from module 04.

## Lesson 6.1: Launch Templates and Auto Scaling Groups

### Principle 6.1

*EC2 Auto Scaling lets you simplify infrastructure code by applying the
same configuration to many instances. That configuration lives in a
versioned launch template.*

### Practice 6.1

This section gets you familiar with EC2 Auto Scaling, Amazon's original
scaling service and still one of its most useful. The User Guide's
[introduction](https://docs.aws.amazon.com/autoscaling/ec2/userguide/what-is-amazon-ec2-auto-scaling.html)
is a great place to get familiar with the basic components.

An Auto Scaling group (ASG) needs to know how to launch an instance. For
years that was a *launch configuration*: immutable, unversioned, and limited
to the EC2 features of its day. Its replacement, the
[launch template](https://docs.aws.amazon.com/autoscaling/ec2/userguide/launch-templates.html),
is versioned, supports every current EC2 feature, and is the only option in
a new account. You'll see launch configurations in older code and in the
docs; read the
[launch configurations](https://docs.aws.amazon.com/autoscaling/ec2/userguide/launch-configurations.html)
page once for the dates and don't write new ones.

#### Lab 6.1.1: ASG from an Instance, the Old Way

In Topic 5, you created CloudFormation templates that launched EC2
instances. The simplest thing older tutorials do to create an ASG is to
[ask Amazon to create one from a running instance](https://docs.aws.amazon.com/autoscaling/ec2/userguide/create-asg-from-instance.html).

- Launch your Linux template from Topic 5: one Amazon Linux 2023 instance
  with Session Manager access. It ended Topic 5 on Graviton (`t4g.micro` with
  the `arm64` AMI parameter), which is fine here. Get the instance ID.

- Use `aws autoscaling create-auto-scaling-group` with `--instance-id` to
  create an ASG from that instance, limited to a single instance.

- In an account created after October 2024 this should fail. Save the exact
  error message in your answer below.

<!-- VERIFY: capture the exact error returned by create-auto-scaling-group --instance-id in an account created after 2024-10-01. -->

##### Question: What Failed

_What error did you get? Read the create-from-instance page again: what
resource does this command create behind the scenes, and why can't your
account create it? If the command succeeded, what does that tell you about
the age of the account you're using?_

#### Lab 6.1.2: Launch Template from an Instance

Do the same thing the current way: turn the instance into a launch template,
then create the group from the template.

- Use
  [aws ec2 get-launch-template-data](https://docs.aws.amazon.com/cli/latest/reference/ec2/get-launch-template-data.html)
  to read the configuration of your instance as launch template data.

- Create a launch template from that data with
  [aws ec2 create-launch-template](https://docs.aws.amazon.com/cli/latest/reference/ec2/create-launch-template.html).
  Remove anything from the data that you don't want copied to every future
  instance.

- Create an ASG from the launch template with
  [aws autoscaling create-auto-scaling-group](https://docs.aws.amazon.com/cli/latest/reference/autoscaling/create-auto-scaling-group.html),
  in the same subnet as the instance, limited to a single instance at all
  times.

##### Question: Resources

_What was created in addition to the new Auto Scaling group? Look for an IAM
role you didn't create (see
[service-linked roles](https://docs.aws.amazon.com/autoscaling/ec2/userguide/autoscaling-service-linked-role.html))._

##### Question: Parameters

_What did `get-launch-template-data` record from the instance? Which values
did you remove before creating the template, and why would they be wrong for
a group of instances?_

#### Lab 6.1.3: Launch Template and ASG in CloudFormation

Write a new template that explicitly creates an
[AWS::EC2::LaunchTemplate](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-ec2-launchtemplate.html)
and an
[AWS::AutoScaling::AutoScalingGroup](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-autoscaling-autoscalinggroup.html),
and create a stack from it.

- Take the AMI from the AL2023 SSM public parameter through a `LatestAmiId`
  parameter, and the VPC and subnets as parameters (`AWS::EC2::VPC::Id` and
  `List<AWS::EC2::Subnet::Id>`). Use at least two subnets in different
  Availability Zones.

- Start on x86: default `LatestAmiId` to the `x86_64` parameter and pass a
  t3.micro instance type in as a parameter. The AMI and the instance type must
  match in architecture; you'll move the group to Graviton in Lab 6.1.6.

- Require IMDSv2 in the launch template's `MetadataOptions`.

- Add a security group with **no inbound rules**, and an instance profile
  with the `AmazonSSMManagedInstanceCore` managed policy. Confirm that the
  instance shows up in `aws ssm describe-instance-information` and that you
  can start a Session Manager session to it. You'll need
  `--capabilities CAPABILITY_IAM` to create the stack.

- Keep the group at one instance. Take your identifier as a `StudentId`
  parameter and use it in `Name` and `Student` tags on the instances (through
  the launch template's `TagSpecifications` or tags the group propagates).

- Specify only the information or extra resources that you must; keep your
  template as simple as possible for these exercises. Run `cfn-lint` on it
  before every create or update, as you did in module 01.

##### Question: ASG From Existing Instance

_What configuration or resources did you have to create explicitly that
Amazon took from the instance in Lab 6.1.2?_

##### Question: IMDSv2

_Remove `MetadataOptions` from a copy of your template, launch an instance
from it, and check its metadata options with `aws ec2 describe-instances`.
Is IMDSv1 still off? Why? (See
[IMDSv2 on AL2023](https://docs.aws.amazon.com/linux/al2023/ug/imdsv2.html).)
Why set it in the template anyway?_

#### Lab 6.1.4: Launch Template Changes

Change the instance type in your launch template from t3.micro to t3.small.
Update your stack.

In the ASG's `LaunchTemplate` property, reference the launch template version
with the template's `LatestVersionNumber` attribute rather than the strings
`$Latest` or `$Default`.

##### Question: Stack Updates

_After updating your stack, did your running instance get replaced or resized?_

##### Question: Template Versions

_Did the launch template get replaced, or did it get a new version? List its
versions with `aws ec2 describe-launch-template-versions`. What would have
happened to the ASG during the stack update if you had referenced `$Latest`
instead of `LatestVersionNumber`?_

Terminate the instance in your ASG with `aws ec2 terminate-instances`.

##### Question: Replacement Instance

_Is the replacement instance the new size or the old?_

#### Lab 6.1.5: Know When It Worked

CloudFormation marks your ASG `CREATE_COMPLETE` as soon as the group exists,
whether or not the software on its instances ever started. A
[CreationPolicy](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-attribute-creationpolicy.html)
makes CloudFormation wait for instances to report success with
[cfn-signal](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/cfn-signal.html).

- Add user data to the launch template that installs a web server (or any
  package) and then signals CloudFormation.

- AL2023 doesn't guarantee the helper scripts are present. Install the
  `aws-cfn-bootstrap` package with `dnf` at the start of your user data; the
  scripts land in `/opt/aws/bin`.

- Call `cfn-signal` with the exit status of your setup, the stack name, the
  **logical ID of the Auto Scaling group** (not the launch template) as the
  resource, and the region. Use the `AWS::StackName` and `AWS::Region`
  pseudo-parameters in a `!Sub`.

- Make sure a failing setup still sends a failure signal instead of silently
  exiting. Don't start the script with `set -e` (or `#!/bin/bash -e`): the
  script would stop before it reaches `cfn-signal`, and CloudFormation would
  wait for the full timeout. Start it with `#!/bin/bash -x` so every command is
  logged, and pass the setup step's exit status to `cfn-signal -e`.

- Add a `CreationPolicy` to the ASG with a signal count equal to the desired
  capacity and a timeout of about 10 minutes.

A `CreationPolicy` only applies when the resource is created, so delete and
recreate the stack (or create a second stack) to see it work. Then create one
more stack with a deliberately broken setup step (a package name that doesn't
exist) and watch what CloudFormation does.

##### Question: Signal Target

_Why does `cfn-signal` name the Auto Scaling group rather than the instance
it runs on? How does the instance get permission to call
`SignalResource`?_

##### Question: Failed Signal

_What did the stack events show when the broken setup ran? How long did it
take to fail, and what did CloudFormation do with the group and its
instances?_

#### Lab 6.1.6: ASG Update Policy

Add an
[UpdatePolicy](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-attribute-updatepolicy.html)
with `AutoScalingRollingUpdate` to your ASG so that instances are replaced
when the launch template changes. Set `WaitOnResourceSignals` so the rolling
update uses the same signals as your `CreationPolicy`, and set
`MinInstancesInService` so the group never drops to zero instances. Update
the stack with only the policy change first; the docs explain why.

Then move the group to Graviton, as you moved a single instance in Topic 5:
first change only the instance type to t4g.small and update the stack, then
change the AMI parameter to the `arm64` parameter as well and update again.

##### Question: Instance Updating

_After updating, what did you see change? Did your running instance get
replaced this time? In what order were instances launched and terminated?_

##### Question: Changing Architecture

_What happened when you changed only the instance type? Where did the failure
show up (stack events, scaling activities, or both), and what did the rolling
update do with the instances it had already replaced?_

#### Lab 6.1.7: Clean Up

Trace out all the resources created by your stacks and the resources
associated with them, then tear everything down:

- Delete the CloudFormation stacks from Labs 6.1.3 to 6.1.6.

- Delete the ASG and launch template you created with the CLI in Lab 6.1.2
  (`aws autoscaling delete-auto-scaling-group --force-delete` and
  `aws ec2 delete-launch-template`), and the Topic 5 stack from Lab 6.1.1.

- Confirm with `aws autoscaling describe-auto-scaling-groups` and
  `aws ec2 describe-instances` that nothing is left running.

##### Question: Stack Tear Down

_After you tear down the stacks, do all the associated resources go away?
What's left, and would you delete it?_

### Retrospective 6.1

Compare your template with the
[Topic 7 starter template](../07-load-balancing/asg_example.yaml), which uses
the same pattern with `cfn-init`. Read more about the
[benefits of Auto Scaling](https://docs.aws.amazon.com/autoscaling/ec2/userguide/auto-scaling-benefits.html),
and about
[migrating existing groups to launch templates](https://docs.aws.amazon.com/autoscaling/ec2/userguide/migrate-to-launch-templates.html),
which you'll meet in older accounts.

#### Question: Private Subnets

_Suppose your instances were in private subnets with no NAT gateway. Which
steps in your user data would fail (installing packages, `cfn-signal`,
Session Manager), and which VPC endpoints would you need for each?_

## Lesson 6.2: Health Checks

### Principle 6.2

*Auto Scaling is a high-availability solution that ensures only healthy
instances are running.*

### Practice 6.2

By default, Auto Scaling
[watches EC2 instance health](https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-health-checks.html)
to know when to replace an instance. It can also use the health checks that
load balancers monitor to know whether or not applications are healthy;
you'll do that in Topic 7.

Recreate the stack from Lab 6.1.6 (launch template, ASG with a
`CreationPolicy` and rolling update policy, Session Manager access) for this
lesson and the next.

#### Lab 6.2.1: Use awscli to Describe an ASG

Use the AWS CLI for this process. As you work, compare what you see in
the CLI with what you see in the console, but make all your changes
using the CLI.

[Describe the resources](https://docs.aws.amazon.com/cli/latest/reference/cloudformation/describe-stack-resources.html)
in your stack. From that output, find the name of your ASG.

##### Question: Filtering Output

_Can you filter your output with `--query` to print only your ASG's
physical resource ID? Given that name,
[describe your ASG](https://docs.aws.amazon.com/cli/latest/reference/autoscaling/describe-auto-scaling-groups.html).
Find the instance ID. Can you filter the output to print only the instance ID
value?_

(You can use the `--query` option, but you can also use
[jq](https://jqlang.org/). Both are useful in different scenarios.)

[Terminate that instance](https://docs.aws.amazon.com/cli/latest/reference/ec2/terminate-instances.html).
Describe your ASG again. Run the command repeatedly until you see the new
instance launch, and list the group's
[scaling activities](https://docs.aws.amazon.com/cli/latest/reference/autoscaling/describe-scaling-activities.html).

##### Question: Instance Timing

_How long did it take for the new instance to spin up? How long before it was
marked as healthy? Where did your `cfn-signal` call go this time?_

#### Lab 6.2.2: Scale Out

Watch your stack and your ASG in the web console as you do this lab.

Modify your stack template to increase the desired number of instances,
then update the stack.

##### Question: Desired Count

_Did it work? If it didn't, what else do you have to increase?_

##### Question: Update Delay

_How quickly after your stack update did you see the ASG change?_

#### Lab 6.2.3: Manual Interference

Take one of your instances
[out of your ASG manually](https://docs.aws.amazon.com/cli/latest/reference/autoscaling/set-instance-health.html)
by marking it unhealthy with the CLI. Observe Auto Scaling as it launches a
replacement instance. Take note of what it does with the instance you marked
unhealthy, and in which order.

##### Question: Launch Before Terminate

_Did Auto Scaling terminate the unhealthy instance before or after launching
its replacement? Read about
[instance maintenance policies](https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-instance-maintenance-policy.html).
How would you change that order, and when would you want to?_

#### Lab 6.2.4: Troubleshooting Features

Simply killing a failing server feels like an easy remedy when all your
infrastructure is code and your systems are immutable. It's usually helpful
to know why something failed, though, and when you have to do some
debugging, the ASG offers a few options, including
[placing an instance on standby](https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-enter-exit-standby.html)
or
[suspending processes](https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-suspend-resume-processes.html).

Standby allows you to take an instance out of action without changing
anything else: no new instance is created, the standby one isn't
terminated, and its health status stays as it was before standby.
Put an instance on standby using the CLI. Observe your ASG in the console
and see for yourself that the health status doesn't change and the group
hasn't changed. Put the instance back in action. Note the commands you used
and the change to the lifecycle state of the instance after each change.
Start a Session Manager session to the instance while it's on standby; this
is where you'd debug it.

Read through the
[types of processes](https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-suspend-resume-processes.html#process-types)
in the suspending processes doc. It gives you a lot of flexibility. For
example, if you have a problematic deployment, you may want to suspend
`AddToLoadBalancer`, launch a new instance by
[increasing the desired capacity](https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-scaling-manually.html)
of the ASG, and run tests against it while it's deployed to the sidelines.
We're not using a load balancer right now, so we can't exercise
`AddToLoadBalancer`, but let's look at another. Suspend `Launch`, then put
an instance on standby and back in action again. Note the process you have
to go through, including any commands you run, and resume `Launch` when
you're done.

### Retrospective 6.2

#### Question: CloudWatch

_How would you use Amazon CloudWatch to help monitor your ASG? Which group
metrics would you enable, and what would you alarm on?_

You can read more about
[monitoring Auto Scaling groups](https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-cloudwatch-monitoring.html)
with CloudWatch.

## Lesson 6.3: Scaling Policies

### Principle 6.3

*Auto Scaling ensures you always maintain resources that match your
performance and cost needs.*

### Practice 6.3

In this lesson, you'll work with
[CloudWatch alarms](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-cloudwatch-alarm.html)
to scale your ASG in or out according to load. This is the original scaling
method Amazon offered for EC2, now called
[simple scaling](https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html).
Then you'll replace it with
[target tracking](https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-target-tracking.html),
which is what AWS recommends for most workloads.

Before you start:

- Turn on
  [detailed monitoring](https://docs.aws.amazon.com/autoscaling/ec2/userguide/enable-as-instance-metrics.html)
  in the launch template, so instances report metrics every minute instead
  of every five.

- Set the group's `DefaultInstanceWarmup`. Read
  [default instance warmup](https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-default-instance-warmup.html)
  to choose a value.

- Install `stress-ng` in your user data. It's in the AL2023 repository.

To load an instance, run `stress-ng` for a few minutes with
[aws ssm send-command](https://docs.aws.amazon.com/cli/latest/reference/ssm/send-command.html)
and the `AWS-RunShellScript` document, or from a Session Manager session.

#### Lab 6.3.1: Simple Scale-Out

Add a CloudWatch alarm to your template and associate it with a
[scaling policy](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-autoscaling-scalingpolicy.html)
on your ASG.

- Watch for average CPU utilization above 60% over two 1-minute periods and
  scale the group out (or "up") by one instance.

- Ensure that your desired number of instances is lower than your max
  number.

Update your stack, then load one of the instances for about five minutes.

##### Question: Alarm Period

_What would your alarm have done with a 1-minute period if you hadn't turned
on detailed monitoring?_

##### Question: Scaling Interval

_After the evaluation periods, do you see a new instance created? Which
scaling activity recorded it?_

Stop the load (or let `stress-ng` time out).

##### Question: Scale-In

_After the load has been low for a few minutes, do you see any instances terminated?_

#### Lab 6.3.2: Simple Scale-In

Add another alarm, this time to allow the group to scale back in (or
"down"):

- Watch for average CPU utilization below 40% over two 1-minute periods and
  scale in by one instance.

Update your stack.

##### Question: Instance Count

_Do you see more instances than the configured "desired capacity"?_

##### Question: Termination Order

_If an instance is automatically terminated, which is it, the last one created
or the first?_

##### Question: Termination Policy

_Can you change your configuration to alter which instance gets terminated
first? (See
[termination policies](https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-termination-policies.html).)_

#### Lab 6.3.3: Target Tracking Policy

Replace your simple scale-out policy with a target tracking scaling policy:

- Use a
  [predefined metric](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-properties-autoscaling-scalingpolicy-targettrackingconfiguration.html)
  for average CPU utilization, with a target of 50%.

- Disable scale-in so that your original simple scale-in policy is
  the only one used to reduce the size of the group.

*NOTE: If you get an error from CloudFormation saying you can't modify
the policy, do it in 2 separate steps: first delete your scale-out
policy and update your stack, then add your target tracking policy and
update your stack again.*

##### Question: Configuration Complexity

_Is your resulting configuration more or less complicated than the one that
uses a simple policy? Which alarms exist now, and who created them?_

Load an instance the way you did in Lab 6.3.1, then stop.

##### Question: Scale-Out Delay

_How long do you have to let it run before you see the group scale out?_

##### Question: Scale-In Delay

_How much time passes after you stop before it scales back in?_

#### Lab 6.3.4: Target Tracking Scale-In

Now eliminate your simple scale-in policy and enable scale-in on your
target tracking policy. Update your stack, then load an instance again until
an instance is added.

##### Question: Changing Delay

_After you stop the load, how long does it take now before scale-in? Why is
target tracking slower to scale in than to scale out?_

### Retrospective 6.3

You can also scale on a schedule, or let
[predictive scaling](https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-predictive-scaling.html)
forecast load from history. In Topic 7 you'll integrate
[Elastic Load Balancing](https://docs.aws.amazon.com/autoscaling/ec2/userguide/autoscaling-load-balancer.html)
with your ASG and can scale on request count per target instead of CPU.

#### Question: Burstable Instances

_Your t3 and t4g instances earn and spend
[CPU credits](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/burstable-performance-instances.html).
Why is CPU utilization on a burstable instance a tricky scaling metric? What
would you use in production?_

## Lesson 6.4: Updating and Optimizing Groups

### Principle 6.4

*A group is only as good as the way you change it. Replace instances
deliberately, with capacity to spare, and pay only for the capacity you
need.*

### Practice 6.4

In Lab 6.1.6 CloudFormation replaced your instances with a rolling update.
[Instance Refresh](https://docs.aws.amazon.com/autoscaling/ec2/userguide/asg-instance-refresh.html)
is the Auto Scaling feature that does the same job with more control:
launch-before-terminate, checkpoints, skip matching, bake time and
automatic rollback. You can start it yourself, and CloudFormation can now run
it for you through the `AutoScalingInstanceRefresh` update policy.

Then you'll look at two ways to shape the capacity itself:
[mixed instances groups](https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-mixed-instances-groups.html),
which spread a group across several instance types and Spot, and
[warm pools](https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-warm-pools.html),
which keep pre-initialized instances stopped until you need them.

Keep the stack from Lesson 6.3. Remove the scaling policies and alarms, and
set the desired capacity to 2 so there is something to refresh.

#### Lab 6.4.1: Instance Refresh from the CLI

- Create a new version of your launch template from the CLI with
  [create-launch-template-version](https://docs.aws.amazon.com/cli/latest/reference/ec2/create-launch-template-version.html),
  based on the current version, with a small change to the user data (for
  example, a different message in the web page).

- Start an instance refresh with
  [start-instance-refresh](https://docs.aws.amazon.com/cli/latest/reference/autoscaling/start-instance-refresh.html).
  Put the new version in the desired configuration. Set the minimum healthy
  percentage to 100 and the maximum to 200, turn on skip matching, and add a
  checkpoint at 50%.

- Watch it with `describe-instance-refreshes` and the group's scaling
  activities. At the checkpoint, decide whether to continue, and try
  [rolling back](https://docs.aws.amazon.com/autoscaling/ec2/userguide/instance-refresh-rollback.html)
  instead.

##### Question: Skip Matching

_Start a second refresh with the same desired configuration. What happened?
What kind of change would skip matching fail to notice?_

##### Question: Drift

_You changed the group outside CloudFormation. Run drift detection on the
stack. What does it report, and what will the next stack update do to your
group?_

#### Lab 6.4.2: Instance Refresh from CloudFormation

Let CloudFormation start the refresh instead of you:

- Replace the `AutoScalingRollingUpdate` policy with an
  [AutoScalingInstanceRefresh](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-attribute-updatepolicy.html#cfn-attributes-updatepolicy-instancerefresh)
  policy using the `Rolling` strategy. A group can't have both.

- Give the group an `InstanceMaintenancePolicy` with a minimum healthy
  percentage of 100 and a maximum of 200.

- Update the stack with a change to the launch template's user data, and
  watch the refresh in the Auto Scaling console while the stack updates.

##### Question: Rolling Update vs Instance Refresh

_Compare this update with the rolling update in Lab 6.1.6. Which one kept
full capacity the whole time? What did each do if a new instance failed?_

##### Question: Readiness

_Instance Refresh doesn't use `cfn-signal`. What does it use to decide a new
instance is ready, and what would you add if your instances need several
minutes of bootstrapping before they can take traffic? What happens to your
`cfn-signal` call now when a refresh launches an instance?_

<!-- VERIFY: behaviour of a CreationPolicy on an ASG that also has an AutoScalingInstanceRefresh update policy (signals ignored during refresh, still honoured at create). -->

#### Lab 6.4.3: Mixed Instances and Spot

Replace the ASG's `LaunchTemplate` property with a `MixedInstancesPolicy`:

- Keep your launch template as the base, and list at least three instance
  types that can run your AMI as overrides.

- Keep one On-Demand instance as the base capacity and run everything above
  it on Spot, with the `price-capacity-optimized` allocation strategy (see
  [allocation strategies](https://docs.aws.amazon.com/autoscaling/ec2/userguide/allocation-strategies.html)).

- Turn on
  [capacity rebalancing](https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-capacity-rebalancing.html).

- Scale the group to 3 and describe the instances.

Optional: replace the instance type list with
[attribute-based instance type selection](https://docs.aws.amazon.com/autoscaling/ec2/userguide/create-mixed-instances-group-attribute-based-instance-type-selection.html)
(vCPU and memory ranges) and see which types it picks.

##### Question: What Launched

_Which instance types and purchase options did you get? How can you tell
which instances are Spot from the CLI?_

##### Question: One Template, Two Architectures

_Can you list t3.micro and t4g.micro as overrides of the same launch
template? What would you have to add to the policy to mix x86 and Graviton in
one group?_

##### Question: Interruptions

_What happens to a Spot instance when EC2 needs the capacity back, and what
does capacity rebalancing change about that? What kinds of workload should
never run on Spot?_

#### Lab 6.4.4: Warm Pools

Warm pools help when instances take a long time to boot. Simulate that, then
measure the difference.

- Warm pools don't support Spot in a mixed instances group. Set the On-Demand
  percentage above base capacity to 100 (or go back to a plain
  `LaunchTemplate`).

- Add a slow step (for example `sleep 180`) to your user data before it
  signals. Scale the group out by one with `set-desired-capacity` and time how
  long the new instance takes to become `InService`.

- Add an
  [AWS::AutoScaling::WarmPool](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-autoscaling-warmpool.html)
  with the `Stopped` pool state and an instance reuse policy that returns
  instances to the pool on scale-in.

- Auto Scaling stops an instance as soon as it has launched into the pool,
  without waiting for user data. Add a
  [lifecycle hook](https://docs.aws.amazon.com/autoscaling/ec2/userguide/warm-pool-instance-lifecycle.html)
  for `autoscaling:EC2_INSTANCE_LAUNCHING` and have your user data call
  `complete-lifecycle-action` when it finishes. The instance role needs
  permission for that call, and the user data needs the instance ID from
  IMDSv2.

- Once the pool has filled and its instances are stopped, scale out by one
  again and time it.

##### Question: Cold and Warm Starts

_How long did the cold start and the warm start take? When the instance left
the warm pool and booted again, did your user data run? What completed the
lifecycle hook the second time, and how would you fix that? (See
[target lifecycle state](https://docs.aws.amazon.com/autoscaling/ec2/userguide/retrieving-target-lifecycle-state-through-imds.html).)_

##### Question: What You Pay For

_What do you pay for an instance in the `Stopped` pool state? Why does AWS
discourage the `Running` pool state, and what does `Hibernated` add?_

#### Lab 6.4.5: Clean Up

- Delete the stack. Check that the warm pool, the lifecycle hook, the group
  and all its instances (including stopped warm pool instances) are gone.

- Delete any launch template versions or other resources you created
  outside the stack.

- Confirm with `aws autoscaling describe-auto-scaling-groups`,
  `aws ec2 describe-launch-templates` and `aws ec2 describe-instances` that
  nothing from this module is left.

### Retrospective 6.4

#### Question: Choosing an Update Mechanism

_You now know four ways to get a new launch template version onto a group:
do nothing and let instances age out, `AutoScalingReplacingUpdate`,
`AutoScalingRollingUpdate`, and Instance Refresh (by hand or through
`AutoScalingInstanceRefresh`). For each, when would you choose it? Which
gives you a new group, which can roll back automatically, and which honours
the group's instance maintenance policy?_

## Further Reading

- Make sure you're familiar with the issues brought up in the
  [EC2 Auto Scaling FAQ](https://aws.amazon.com/ec2/autoscaling/faqs/).

- [Lifecycle hooks](https://docs.aws.amazon.com/autoscaling/ec2/userguide/lifecycle-hooks.html)
  are how you run custom actions as instances launch and terminate, from
  draining connections to shipping logs before an instance disappears.

- [Maximum instance lifetime](https://docs.aws.amazon.com/autoscaling/ec2/userguide/asg-max-instance-lifetime.html)
  replaces instances on a schedule, which keeps long-lived groups patched.

- [Scaling your applications faster with EC2 Auto Scaling Warm Pools](https://aws.amazon.com/blogs/compute/scaling-your-applications-faster-with-ec2-auto-scaling-warm-pools/)
  and
  [Introducing the price-capacity-optimized allocation strategy for EC2 Spot Instances](https://aws.amazon.com/blogs/compute/introducing-price-capacity-optimized-allocation-strategy-for-ec2-spot-instances/)
  go deeper into Lesson 6.4.

- Application Auto Scaling scales resources other than EC2 (ECS services,
  DynamoDB tables, Aurora replicas, Lambda provisioned concurrency) with the
  same target tracking and step scaling ideas. See
  [what is Application Auto Scaling](https://docs.aws.amazon.com/autoscaling/application/userguide/what-is-application-auto-scaling.html).
