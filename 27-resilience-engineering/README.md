# Topic 27: Resilience Engineering

<!-- TOC -->

- [Topic 27: Resilience Engineering](#topic-27-resilience-engineering)
  - [What changed in the 2026 edition](#what-changed-in-the-2026-edition)
  - [Exam coverage](#exam-coverage)
  - [Cost and cleanup](#cost-and-cleanup)
  - [Guidance](#guidance)
  - [Conventions](#conventions)
  - [Lesson 27.1: Deployment strategies compared](#lesson-271-deployment-strategies-compared)
    - [Principle 27.1](#principle-271)
    - [Practice 27.1](#practice-271)
      - [Lab 27.1.1: The target workload and its steady state](#lab-2711-the-target-workload-and-its-steady-state)
      - [Lab 27.1.2: A rolling update, measured](#lab-2712-a-rolling-update-measured)
      - [Lab 27.1.3: Blue/green and canary with weighted target groups](#lab-2713-bluegreen-and-canary-with-weighted-target-groups)
      - [Lab 27.1.4: The same strategies on ECS and Lambda (on paper)](#lab-2714-the-same-strategies-on-ecs-and-lambda-on-paper)
    - [Retrospective 27.1](#retrospective-271)
  - [Lesson 27.2: AWS Fault Injection Service](#lesson-272-aws-fault-injection-service)
    - [Principle 27.2](#principle-272)
    - [Practice 27.2](#practice-272)
      - [Lab 27.2.1: Steady-state alarms and a target tag](#lab-2721-steady-state-alarms-and-a-target-tag)
      - [Lab 27.2.2: A first experiment: CPU stress on one instance](#lab-2722-a-first-experiment-cpu-stress-on-one-instance)
      - [Lab 27.2.3: Lose an Availability Zone's instances](#lab-2723-lose-an-availability-zones-instances)
      - [Lab 27.2.4: The safety lever](#lab-2724-the-safety-lever)
      - [Lab 27.2.5: AZ Availability: Power Interruption, on paper](#lab-2725-az-availability-power-interruption-on-paper)
    - [Retrospective 27.2](#retrospective-272)
  - [Lesson 27.3: AWS Resilience Hub](#lesson-273-aws-resilience-hub)
    - [Principle 27.3](#principle-273)
    - [Practice 27.3](#practice-273)
      - [Lab 27.3.1: A resiliency policy from your RTO and RPO](#lab-2731-a-resiliency-policy-from-your-rto-and-rpo)
      - [Lab 27.3.2: An application from your stack](#lab-2732-an-application-from-your-stack)
      - [Lab 27.3.3: Assess and read the recommendations](#lab-2733-assess-and-read-the-recommendations)
      - [Lab 27.3.4: Fix one thing, reassess, and delete the application](#lab-2734-fix-one-thing-reassess-and-delete-the-application)
    - [Retrospective 27.3](#retrospective-273)
  - [Lesson 27.4: Application Recovery Controller](#lesson-274-application-recovery-controller)
    - [Principle 27.4](#principle-274)
    - [Practice 27.4](#practice-274)
      - [Lab 27.4.1: Register the workload for zonal shift](#lab-2741-register-the-workload-for-zonal-shift)
      - [Lab 27.4.2: Shift away from an Availability Zone](#lab-2742-shift-away-from-an-availability-zone)
      - [Lab 27.4.3: Zonal autoshift and a practice run](#lab-2743-zonal-autoshift-and-a-practice-run)
      - [Lab 27.4.4: Routing control and Region switch, on paper](#lab-2744-routing-control-and-region-switch-on-paper)
    - [Retrospective 27.4](#retrospective-274)
  - [Lesson 27.5: Game days and runbooks](#lesson-275-game-days-and-runbooks)
    - [Principle 27.5](#principle-275)
    - [Practice 27.5](#practice-275)
      - [Lab 27.5.1: A runbook for "one AZ is sick"](#lab-2751-a-runbook-for-one-az-is-sick)
      - [Lab 27.5.2: Run a game day](#lab-2752-run-a-game-day)
      - [Lab 27.5.3: The post-incident review](#lab-2753-the-post-incident-review)
      - [Lab 27.5.4: Clean up the module](#lab-2754-clean-up-the-module)
    - [Retrospective 27.5](#retrospective-275)
  - [Further Reading](#further-reading)

<!-- /TOC -->

## What changed in the 2026 edition

- **New module.** The 2022 course deployed with rolling updates (module
  06) and Lambda canaries (module 16), but never compared deployment
  strategies across platforms and never broke anything on purpose. The
  DevOps Pro exam (DOP-C02) tests both: Task 1.4 on deployment strategies
  and Domain 3 on resilient solutions and automated recovery. The
  Solutions Architect Pro exam tests DR testing and rollback design.
- **Deployment strategies, side by side.** One lesson puts in-place,
  rolling, blue/green, canary and linear next to each other for EC2 Auto
  Scaling, Amazon ECS and Lambda, and builds blue/green and canary on an
  Application Load Balancer with weighted target groups. It refers back to
  modules 06, 07, 13 and 16 instead of repeating them. Amazon ECS gained
  **built-in blue/green** deployments in July 2025 and **built-in linear
  and canary** deployments in October 2025, so CodeDeploy is no longer the
  only way to shift traffic gradually on ECS.
- **AWS Fault Injection Service** (FIS, formerly Fault Injection
  Simulator, which is still the name in the DOP-C02 guide). Every
  experiment in this module has a **stop condition** tied to a CloudWatch
  alarm. The labs use the AWS-owned `AWSFIS-Run-CPU-Stress` document,
  stop instances in one Availability Zone, preview targets with
  `actionsMode=skip-all`, pull the account's **safety lever**, and read
  the **AZ Availability: Power Interruption** scenario from the scenario
  library on paper.
- **AWS Resilience Hub** turns the RTO and RPO from module 23 into a
  resiliency policy and assesses a CloudFormation stack against it. In May
  2026 AWS launched a *next generation* of Resilience Hub (systems,
  services, GenAI-powered failure mode assessments and, since August 2026,
  recommended resilience tests run through FIS). The labs use the original
  application model, which is what the current exam guides describe and
  which existing and new customers can still use; the next generation is
  covered on paper.
- **Amazon Application Recovery Controller (ARC).** Zonal shift and
  zonal autoshift (free) for an Application Load Balancer and an Auto
  Scaling group, including autoshift practice runs. Routing control
  (billed per cluster-hour) and **Region switch** (added in August 2025,
  billed per plan) are covered on paper only. ARC **readiness checks**
  closed to new customers on April 30, 2026.
- **Game days and runbooks.** The module ends with a runbook for losing an
  Availability Zone, a game day that uses your own FIS experiments, and a
  blameless post-incident review.

## Exam coverage

| Exam | Domain / task statement |
|---|---|
| DOP-C02 | Domain 1: SDLC Automation (Task 1.4: deployment strategies for instance, container and serverless environments; mutable and immutable deployment patterns; blue/green and canary) |
| DOP-C02 | Domain 3: Resilient Cloud Solutions (Task 3.1: identifying and remediating single points of failure, load balancing across Availability Zones; Task 3.3: automated recovery to meet RTO and RPO, testing failover of Multi-AZ workloads) |
| DOP-C02 | Domain 5: Incident and Event Response (Task 5.3: troubleshooting system and application failures, analyzing failed deployments) |
| SAP-C02 → C03 | Domain 1: Design Solutions for Organizational Complexity (Task 1.3: reliable and resilient architectures, automatic recovery from failure) |
| SAP-C02 → C03 | Domain 2: Design for New Solutions (Task 2.1: deployment strategies with rollback mechanisms; Task 2.2: business continuity, performing disaster recovery testing). The C03 guide publishes 2026-10-27 and adds GenAI / agent topics |
| SOA-C03 | Domain 2: Reliability and Business Continuity (Skill 2.2.1: ELB health checks; Skill 2.2.2: fault-tolerant, Multi-AZ systems). Application Recovery Controller is on the in-scope list; FIS and Resilience Hub are on the out-of-scope list |
| SOA-C03 | Domain 3: Deployment, Provisioning, and Automation (Skill 3.1.5: implement deployment strategies and services) |

## Cost and cleanup

Prices are for `us-east-2` in September 2026. Check
[FIS pricing](https://aws.amazon.com/fis/pricing/),
[Resilience Hub pricing](https://aws.amazon.com/resilience-hub/pricing/),
[ARC pricing](https://aws.amazon.com/application-recovery-controller/pricing/)
and
[Elastic Load Balancing pricing](https://aws.amazon.com/elasticloadbalancing/pricing/)
before you start.

- **The target workload has an hourly charge.** The Application Load
  Balancer costs about $0.0225 an hour plus load balancer capacity units
  (about $16 a month before traffic). Two `t3.micro` instances add about
  $0.021 an hour, and every public IPv4 address costs $0.005 an hour: the
  load balancer uses one per Availability Zone and each instance has one.
  Left running, the stack costs about $1.70 a day, or $50 a month. Lab
  27.1.3 doubles the instances for as long as blue and green both run.
  Delete the stack between sessions if you'll be away for more than a day
  or two; it redeploys in minutes.
  <!-- VERIFY: ALB hourly rate in us-east-2 (module 07 has the same open
  question). -->
- **AWS FIS costs $0.10 per action-minute.** An action that runs for five
  minutes costs $0.50; two actions that run in parallel for five minutes
  cost $1.00. The experiments in this module are five minutes long, so
  the whole module, including a game day, should cost $5 to $10 in FIS
  charges. Experiments you stop early are billed only for the minutes
  that ran, and experiments the safety lever prevents from starting cost
  nothing. **Don't run the AZ Power Interruption scenario with its
  default durations**: it runs several actions for 30 minutes each, which
  is well over $15 per run. Experiment reports, which this module doesn't
  use, cost $5 each.
  <!-- VERIFY: that a start-experiment with actionsMode=skip-all (target
  preview only) is not billed, since no action runs. -->
- **AWS Resilience Hub bills per application.** With the original
  application model, an application costs **$15 a month**, from the
  moment its first assessment runs until you delete it. New customers get
  their first three applications free for six months. The next
  generation (May 2026) bills $15 per *service* per month, plus $10 per
  service per month for dependency assessment. **Delete the application
  in Lab 27.3.4, the same day you create it**, even if you are inside
  the free trial: it's easy to forget, and the trial ends by itself.
  <!-- VERIFY: whether a Resilience Hub application deleted after one day
  is billed pro rata or for the whole month. -->
- **ARC zonal shift and zonal autoshift are free.** You pay for the
  resources whose traffic you shift, not the shift. **Routing control is
  not free: each cluster costs $2.50 an hour (about $1,800 a month)** and
  an account can have two. **Don't create a cluster in this course.**
  Region switch plans cost $70 a month each and readiness checks $0.045
  an hour each; this module covers them on paper only.
- **Small charges:** CloudWatch alarms ($0.10 per standard-resolution
  alarm per month, prorated), the FIS experiment log group (a few KB),
  and Systems Manager Run Command, which FIS uses and which is free on EC2
  instances.
- **Cleanup:** [Lab 27.5.4](#lab-2754-clean-up-the-module) stops any
  running experiment, deletes the experiment templates, the Resilience
  Hub application and policy, the zonal autoshift and practice run
  configuration, and the stacks, then checks that nothing is left. ARC
  configuration and Resilience Hub applications are not all in stacks, so
  deleting stacks alone is not enough.

## Guidance

- Explore the official docs! See the
  [AWS FIS User Guide](https://docs.aws.amazon.com/fis/latest/userguide/what-is.html),
  [AWS Resilience Hub User Guide](https://docs.aws.amazon.com/resilience-hub/latest/userguide/what-is.html),
  [ARC Developer Guide](https://docs.aws.amazon.com/r53recovery/latest/dg/what-is-route53-recovery.html)
  and the CLI references for
  [fis](https://docs.aws.amazon.com/cli/latest/reference/fis/),
  [resiliencehub](https://docs.aws.amazon.com/cli/latest/reference/resiliencehub/)
  and
  [arc-zonal-shift](https://docs.aws.amazon.com/cli/latest/reference/arc-zonal-shift/).
  The CloudFormation resource types are under
  [AWS FIS](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/AWS_FIS.html),
  [AWS Resilience Hub](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/AWS_ResilienceHub.html)
  and
  [ARC zonal shift](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/AWS_ARCZonalShift.html).

- Read the Builders' Library articles
  [Automating safe, hands-off
  deployments](https://aws.amazon.com/builders-library/automating-safe-hands-off-deployments/)
  before Lesson 27.1 and [Static stability using Availability
  Zones](https://aws.amazon.com/builders-library/static-stability-using-availability-zones/)
  before Lesson 27.4. Many exam questions about deployments and
  Availability Zones are answered by the reasoning in those two articles.

- Avoid using other sites like stackoverflow.com for answers \-- part
  of the skill set you're building is finding answers straight from
  the source, AWS. Posts written before mid-2025 say ECS needs CodeDeploy
  for blue/green and canary, and describe Resilience Hub and ARC before
  their 2025 and 2026 changes.

- Explore your curiosity. Try to understand why things work the way
  they do. Read more of the documentation than just what you need to
  find the answers.

## Conventions

- **Profile and Region.** Every lab uses the `lab` profile from module 19,
  whose Region is `us-east-2`. CLI examples don't pass `--region`.
- **This module breaks things on purpose. Only ever in the lab account.**
  Every experiment targets resources by a tag that only your lab stacks
  carry, and every experiment has a stop condition. If an experiment
  selects anything you didn't expect in its target preview, stop there.
- **The probe.** Several labs ask you to watch the workload from the
  outside while something happens to it. Run this in a second terminal
  and leave it running (replace the DNS name with the stack output):

  ```bash
  ALB=<LoadBalancerDnsName>
  while true; do
    printf '%s %s\n' "$(date +%T)" \
      "$(curl -s -m 2 -w ' %{http_code}' "http://$ALB/" | tr -d '\n')"
    sleep 0.5
  done | tee probe.log
  ```

  Each line shows the time, then the version, instance, Availability Zone
  name and Availability Zone ID that answered, then the HTTP status
  (`000` means no answer within two seconds). `cut -d' ' -f2- probe.log |
  sort | uniq -c` gives you counts.
- **Placeholders.** `<you>` is your identifier, `123456789012` stands for
  the lab account ID, and names such as `use2-az1` are examples. Don't
  commit real account IDs or ARNs from your account to your answers.
- **Templates.** Write your CloudFormation in YAML, run `cfn-lint` on it
  before you deploy (module 01), and tag everything with your identifier.
- DO use the AWS CLI rather than the console, except where a step says the
  console is required.

## Lesson 27.1: Deployment strategies compared

### Principle 27.1

*Every deployment is a change you are injecting into production. A
deployment strategy decides how much of production sees the change at
once, how you find out it's bad, and how fast you can take it back.*

### Practice 27.1

You have already deployed four ways. Module 06 replaced instances with
`AutoScalingRollingUpdate` and Instance Refresh. Module 07 put those
instances behind a load balancer. Module 13 ran ECS services, which roll
tasks by default. Module 16 shifted Lambda traffic with CodeDeploy
canaries, hooks and alarms. This lesson puts them side by side:

| Strategy | What happens | Capacity during the change | Rollback |
|---|---|---|---|
| In-place, all at once | Every running copy is updated at the same moment | Can drop to zero | Deploy the old version again |
| Rolling | A batch at a time is updated or replaced | Reduced by one batch, unless you add an extra batch first | Roll forward again with the old version |
| Immutable / blue/green | A complete new copy (green) is built beside the old (blue); traffic moves when green is ready | Double while both exist | Move traffic back to blue, which is still running |
| Canary | A small share of traffic goes to the new version for a bake time, then the rest | New version at small scale first | Move the small share back |
| Linear | Traffic moves in equal steps with a wait between each | Grows step by step | Move traffic back |

Canary and linear are ways of moving traffic *during* a blue/green
deployment; they need two versions running side by side and something
that can split traffic between them (a load balancer's weighted target
groups, a Lambda alias, an ECS service, weighted DNS records).

The labs deploy a small target workload that the whole module uses,
measure what a rolling update looks like from the outside, and then build
blue/green and canary on the load balancer. The last lab maps the same
ideas onto ECS and Lambda without deploying them again.

#### Lab 27.1.1: The target workload and its steady state

The starter template
[starter/target-workload.yaml](starter/target-workload.yaml) follows the
conventions of module 07's
[asg_example.yaml](../07-load-balancing/asg_example.yaml): a launch
template on Amazon Linux 2023 with IMDSv2 required, `cfn-init` and
`cfn-signal`, no SSH, and an Auto Scaling group behind an internet-facing
Application Load Balancer. Each web server writes one line to its home
page: the release version, its instance ID, its Availability Zone name
and its Availability Zone ID. The load balancer only accepts HTTP from
the address range you pass as `ClientCidr`.

- Copy the starter into your repository as `workload.yaml`. Read it all,
  including the `TODO(student)` markers; you fill them in over the
  module.
- Deploy it as `<you>-resilience` with the `lab` profile. Use the default
  VPC and two public subnets in different Availability Zones, your public
  address as a `/32` for `ClientCidr`, and the default of two instances.
- Start the probe from [Conventions](#conventions). Both instances, in
  both Availability Zones, should answer.
- Write down the **steady state** of the workload: the numbers that say
  "it's working" from a user's point of view. Read
  [CloudWatch metrics for your Application Load
  Balancer](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-cloudwatch-metrics.html)
  and pick three metrics, with their normal values under your probe's
  traffic. At least one should count errors (`HTTPCode_Target_5XX_Count`,
  `HTTPCode_ELB_5XX_Count`) and one should measure capacity
  (`HealthyHostCount` for the target group). Get the values with
  `aws cloudwatch get-metric-statistics` or `get-metric-data`, using the
  dimension values from the stack outputs.

##### Question: Metrics that are missing

_With no errors, `HTTPCode_Target_5XX_Count` has no data points at all,
not zeros. What does that mean for an alarm on it, and which
`TreatMissingData` setting would you choose for an alarm that must say
"all is well" when nothing is failing?_

##### Question: One per Availability Zone

_The group has two instances in two Availability Zones. What fraction of
capacity do you lose if one Availability Zone fails? What would you change
to lose a third, and what would that cost?_

#### Lab 27.1.2: A rolling update, measured

The starter's Auto Scaling group has an `AutoScalingRollingUpdate` policy,
as in module 07: one instance at a time, keeping at least one in service,
waiting for `cfn-signal`. In module 06 you watched a rolling update from
CloudFormation's side. Now watch it from the user's side.

- Leave the probe running. Update the stack with `AppVersion` set to `v2`.
- When the update completes, stop the probe and count what it saw:
  how many answers came from `v1`, how many from `v2`, how many were not
  `200`, and for how long both versions answered.
- Update again to `v3`, this time with the update policy changed to
  `MaxBatchSize: 2` and `MinInstancesInService: 0` (an in-place, all at
  once deployment, in effect). Count again.
- Put the policy back as it was.

##### Question: Two versions at once

_For how long did users see both versions? What kinds of change make that
dangerous (think about database schemas, API contracts between tiers,
and sessions)?_

##### Question: Where the errors came from

_Did the rolling update produce any non-`200` answers? If it did, when:
as an old instance was deregistered, or as a new one was registered?
Which target group attribute controls the first, and which health check
settings control the second? What did the all-at-once update cost you?_

#### Lab 27.1.3: Blue/green and canary with weighted target groups

An Application Load Balancer listener can
[forward to several target groups with
weights](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/rule-action-types.html#forward-actions).
That is all you need for blue/green, canary and linear deployments on
EC2, without CodeDeploy.

- In `workload.yaml`, rename nothing: the existing target group and Auto
  Scaling group are **blue**. Add a **green** target group and a second
  Auto Scaling group registered with it, using the same launch template
  but its own version parameter (`GreenAppVersion`), and a
  `GreenCapacity` parameter (default `0`) for its min, max and desired
  capacity. Think about what its `CreationPolicy` should wait for when
  the capacity is zero.
- Replace the listener's default action with a `forward` action that has
  a `ForwardConfig` with both target groups and two parameters,
  `BlueWeight` (default `100`) and `GreenWeight` (default `0`).
- Deploy a canary:
  1. Update with `GreenAppVersion=v4`, `GreenCapacity=2`, weights
     unchanged. Green is running and healthy but gets no traffic. Test it
     *before* it gets traffic; how can you reach only the green
     instances? (Look at listener rules with conditions, or Session
     Manager port forwarding from module 20.)
  2. Shift 10% to green (`BlueWeight=90`, `GreenWeight=10`) and run the
     probe for two minutes. Count the answers.
  3. Roll back: weights `100`/`0`. How long did it take, and did any
     request fail?
  4. Shift again, `50`/`50`, then `0`/`100`. Green is now production.
  5. Scale blue to zero only after the bake time you'd want in real life.
- Turn on [target group
  stickiness](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/rule-action-types.html#forward-action-stickiness-cli)
  in the forward action (`TargetGroupStickinessConfig`) for a few minutes and
  repeat the 10% step with `curl -c`/`-b` and a cookie jar. What changes
  for one user?

##### Question: What made it blue/green

_Compare this with Lab 27.1.2. What did the old version do during the
shift, and what did rolling back consist of? What did you pay for that
safety, and for how long?_

##### Question: Weights or DNS

_You could have done the same with two load balancers and weighted Route
53 records (module 21). What would be worse about rolling back, and
why?_

##### Question: Nobody watching

_Nothing in this lab would have rolled back by itself. List what
CodeDeploy's EC2 blue/green deployments add on top of weighted target
groups. Read [Overview of a blue/green
deployment](https://docs.aws.amazon.com/codedeploy/latest/userguide/welcome.html#welcome-deployment-overview-blue-green)
and look for alarms, automatic rollback, and what happens to the
original instances._

#### Lab 27.1.4: The same strategies on ECS and Lambda (on paper)

No AWS resources in this lab. Read:

- [Amazon ECS deployment
  types](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-types.html),
  including the rolling update's
  [deployment circuit
  breaker](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-circuit-breaker.html)
  and the built-in [blue/green
  deployments](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-type-blue-green.html)
  with their lifecycle hooks;
- [Working with deployment configurations in
  CodeDeploy](https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-configurations.html),
  for EC2, ECS and Lambda;
- your own notes from Lesson 16.4 (Lambda aliases, `DeploymentPreference`,
  hooks and alarms);
- [Deployment policies and
  settings](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features.rolling-version-deploy.html)
  in Elastic Beanstalk, which the exams still ask about.

Then fill in this table in your answers. For each cell, name the
feature or setting that provides it, or write "none".

| | EC2 Auto Scaling | Amazon ECS | AWS Lambda | Elastic Beanstalk |
|---|---|---|---|---|
| In-place / all at once | | | | |
| Rolling | | | | |
| Rolling with an extra batch | | | | |
| Blue/green | | | | |
| Canary | | | | |
| Linear | | | | |
| Automatic rollback on alarm | | | | |
| Pre-traffic test hook | | | | |

##### Question: ECS without CodeDeploy

_Since 2025, ECS can run blue/green, canary and linear deployments
itself. What does an ECS service need in front of it to use them, and
what does it give you that the rolling update with a circuit breaker
doesn't? When would you still choose CodeDeploy?_

##### Question: Immutable is a spectrum

_Rank these from most mutable to most immutable, and say what each
replaces: a CodeDeploy in-place deployment, `AutoScalingRollingUpdate`,
Instance Refresh, Elastic Beanstalk's "Immutable" policy, and your
weighted blue/green. Which exam answer are you looking for when a
question says "the deployment must not affect the running fleet"?_

### Retrospective 27.1

#### Question: Choosing a strategy

_For each of these, choose a strategy and the AWS feature you'd use, and
say what signal would stop the deployment: (a) a nightly batch job on
Lambda; (b) a public API on ECS Fargate serving 2,000 requests a second;
(c) a legacy app on three EC2 instances that must never run two versions
at once; (d) a database schema change._

#### Question: The deployment is the experiment

_A canary with an alarm and automatic rollback is a controlled experiment
on production. What are its hypothesis, its blast radius and its stop
condition? Keep your answer: the next lesson uses the same three words._

## Lesson 27.2: AWS Fault Injection Service

### Principle 27.2

*Chaos engineering is the scientific method applied to failure: state the
steady state, predict what a fault will do to it, inject the smallest
fault that tests the prediction, and stop the moment the prediction is
wrong. An experiment without a stop condition is just an outage you
caused.*

### Practice 27.2

AWS FIS runs **experiments** from **experiment templates**. A template
names:

- **targets**: the resources to act on, chosen by ARN, by tag or by
  filter, and a **selection mode** (`ALL`, `COUNT(n)` or `PERCENT(n)`)
  that sets the blast radius;
- **actions**: what to do to them, such as stopping instances, running
  an SSM document, disrupting a subnet's network or returning API errors,
  in parallel or in sequence (`startAfter`);
- **stop conditions**: CloudWatch alarms. If one goes into `ALARM` while
  the experiment runs, FIS stops the experiment and rolls back the
  actions that can be rolled back;
- an **IAM role** that FIS assumes to act on your behalf;
- optionally, **logging** to CloudWatch Logs or S3.

FIS also lets you template an experiment *without* a stop condition.
**This course never does.** The starter template makes the stop
condition a required parameter.

Keep the workload from Lesson 27.1 running with blue at full capacity
and green scaled to zero (or remove green from your template). Read
[How AWS FIS works](https://docs.aws.amazon.com/fis/latest/userguide/what-is.html)
and [Experiment templates](https://docs.aws.amazon.com/fis/latest/userguide/experiment-templates.html)
first.

#### Lab 27.2.1: Steady-state alarms and a target tag

Read [Stop conditions for AWS
FIS](https://docs.aws.amazon.com/fis/latest/userguide/stop-conditions.html)
and, from module 08, your notes on alarms.

- Add to `workload.yaml`:
  - an alarm `<you>-steady-state-errors` on the load balancer's 5XX
    responses (target and ELB) that goes into `ALARM` when there are
    more than a handful in a minute. Use metric math to add the two
    metrics, and choose `TreatMissingData` from your answer to Lab
    27.1.1;
  - an alarm `<you>-steady-state-capacity` on the blue target group's
    `HealthyHostCount`, in `ALARM` when it drops below 1 for a minute;
  - a tag `fis-target` with your identifier as its value on the
    instances (in the launch template's `TagSpecifications`). This tag is
    how every experiment in the module chooses targets, so the
    experiments can never select an instance that isn't yours.
- Update the stack, wait for the instances to be replaced, and check that
  both alarms are `OK` with `aws cloudwatch describe-alarms`.
- Decide which of the two is the stop condition for "CPU stress on one
  instance". Its ARN goes into the next lab.

##### Question: Choosing the stop condition

_Why stop on user-visible errors rather than on high CPU, the very thing
the experiment causes? For an experiment that stops one instance on
purpose, would the capacity alarm make a good stop condition? What does
that tell you about writing one stop condition per experiment?_

##### Question: Alarms that are too slow

_Your alarm evaluates one-minute periods. How much harm can an experiment
do before the stop condition fires? What would you change to make it
faster, and what does that cost?_

#### Lab 27.2.2: A first experiment: CPU stress on one instance

The starter
[starter/fis-cpu-stress.yaml](starter/fis-cpu-stress.yaml) is a worked
example: an experiment role and one experiment template. Read it before
you deploy it, and compare it with [Run CPU stress on an
instance](https://docs.aws.amazon.com/fis/latest/userguide/fis-tutorial-run-cpu-stress.html)
and [Use Systems Manager SSM documents with AWS
FIS](https://docs.aws.amazon.com/fis/latest/userguide/actions-ssm-agent.html).

- Before you deploy, answer in your own words: what does the role allow,
  on which resources? Why does the trust policy have conditions? Which
  instances can the experiment select, and how many? What is the stop
  condition?
- Deploy it as `<you>-fis`, passing your identifier as `TargetTagValue`
  and the error alarm's ARN as `StopConditionAlarmArn`.
  <!-- VERIFY: that FIS accepts the log group ARN returned by
  `!GetAtt LogGroup.Arn` (it ends in `:*`) in the starter's
  LogConfiguration; run once before publishing. -->
- Write your **hypothesis** in your answers before you run anything: "If
  one of the two web servers runs at 100% CPU for four minutes, then …".
- **Preview first.** Start the experiment with
  `--experiment-options actionsMode=skip-all`. Read
  [Generate a target
  preview](https://docs.aws.amazon.com/fis/latest/userguide/generate-target-preview.html).
  List the targets it resolved with `list-experiment-resolved-targets`.
  Is it exactly one of your instances?
- **Run it** without the option, with the probe running. Follow it with
  `aws fis get-experiment`, the instances' `CPUUtilization`, the Run
  Command history (`aws ssm list-commands`) and the experiment's log
  stream in `/fis/<you>-experiments`.
- Was your hypothesis right? Record the probe's counts and the steady
  state metrics during the experiment.
- **Trip the stop condition.** Start the experiment again. While it runs,
  force the stop condition's alarm into `ALARM` with
  `aws cloudwatch set-alarm-state`. Watch the experiment's state change,
  then check on the target instance whether `stress-ng` is still running
  (Session Manager, `pgrep stress-ng`).

##### Question: Two durations

_The action's `duration` and the document's `DurationSeconds` are
different settings. What happens if the action is shorter than the
document? Longer? Which one should be longer, and why?_

##### Question: What rolled back

_When the stop condition fired, what did FIS do to the running SSM
command? Look for the rollback script the AWS FIS documents create on
the instance. Which kinds of action can FIS undo when it stops, and which
can't be undone (think about `aws:ec2:terminate-instances`)?_

##### Question: Least privilege for FIS

_The role could have used the AWS managed policy
`AWSFaultInjectionSimulatorSSMAccess` or
`AWSFaultInjectionSimulatorEC2Access` instead of an inline policy. What
would it have been allowed to do that the starter's policy doesn't?_

#### Lab 27.2.3: Lose an Availability Zone's instances

Now write an experiment yourself. When an Availability Zone fails, its
instances stop answering *and* Auto Scaling can't launch replacements
there. Read the
[`aws:ec2:stop-instances`](https://docs.aws.amazon.com/fis/latest/userguide/fis-actions-reference.html#stop-instances)
and
[`aws:ec2:asg-insufficient-instance-capacity-error`](https://docs.aws.amazon.com/fis/latest/userguide/fis-actions-reference.html#asg-ice)
actions and the [targets](https://docs.aws.amazon.com/fis/latest/userguide/targets.html)
page.

- Add a second experiment template, `<you>-lose-one-az`, to your FIS
  template:
  - **Target 1:** instances with your `fis-target` tag that are
    `running` and in one Availability Zone of your choice (filter on
    `Placement.AvailabilityZone`, from a template parameter).
  - **Target 2:** your Auto Scaling group, selected by ARN or by tag.
  - **Action 1,** in parallel with action 2: stop the target instances
    and start them again after five minutes. Set
    `completeIfInstancesTerminated` and work out why you need it here.
  - **Action 2:** make the Auto Scaling group's launches in that same
    Availability Zone fail with insufficient capacity for five minutes.
  - **Stop condition:** the error alarm. (Read your answer to "Choosing
    the stop condition" again before you choose.)
- Give the role only the extra permissions these two actions need. The
  second one uses `ec2:InjectApiError` with the `ec2:FisActionId` and
  `ec2:FisTargetArns` condition keys; see the example policies in the FIS
  User Guide.
- Write your hypothesis. Include what the load balancer does, what Auto
  Scaling does, and in which Availability Zone the replacement launches.
- Preview with `skip-all`, then run it with the probe running. Watch
  `aws autoscaling describe-scaling-activities` as well as the probe.

##### Question: Where the replacement went

_Did Auto Scaling replace the stopped instance? In which Availability
Zone did it try first, what did the injected error do, and what did Auto
Scaling do next? What happened to the stopped instance when FIS tried to
start it again?_

##### Question: What users saw

_How many errors did the probe record, and when? Would a user have
noticed? What would you change in the target group's health check, or in
the application, to shorten the window?_

#### Lab 27.2.4: The safety lever

Every account has one FIS **safety lever** per Region. Engaging it stops
every running experiment and cancels any that try to start. Read [Safety
levers for AWS
FIS](https://docs.aws.amazon.com/fis/latest/userguide/safety-lever.html).

- Check its state: `aws fis get-safety-lever --id default`.
- Start the CPU stress experiment. While it runs, engage the lever with
  `update-safety-lever-state` and a reason. What state does the
  experiment end in?
- With the lever still engaged, start the experiment again. What
  happens, and does it cost anything?
- **Disengage the lever** and confirm with `get-safety-lever`. Don't
  leave it engaged: the next lessons need FIS.

##### Question: Stop condition or safety lever

_Both stop experiments. Who (or what) pulls each one, and what does each
protect against? Who in a real organization should be allowed to call
`update-safety-lever-state`, and how would you enforce that with an SCP
(module 19)?_

#### Lab 27.2.5: AZ Availability: Power Interruption, on paper

FIS ships a **scenario library** of prebuilt experiment templates. Read
[AZ Availability: Power
Interruption](https://docs.aws.amazon.com/fis/latest/userguide/az-availability-scenario.html)
from top to bottom, including its scenario JSON. You won't run it.

- For each action in the scenario, write one line: what it does, what it
  simulates, which resources in `workload.yaml` (if any) it would target
  with its default tags, and how long it lasts.
- The scenario has no stop condition of its own; its JSON has an empty
  one. Which of your alarms would you add, and would you add more than
  one?
- Trim the scenario to your workload: remove the actions whose targets
  you don't have (and explain why `Pause-Instance-Launches` must go if
  you don't list IAM role ARNs), change the Availability Zone to one of
  yours, retag the targets to use `fis-target`, and shorten every
  duration to 10 minutes. Save the result as `az-power-interruption.json`
  in your repository.
- Estimate what your trimmed version would cost to run, and what the
  default version costs, in action-minutes and dollars.
- *Optional:* create a template from your JSON with
  `create-experiment-template` and start it with `actionsMode=skip-all`
  to see which targets it resolves. Then delete the template.

##### Question: What the scenario can't simulate

_Read the scenario's limitations. Which symptoms of a real Availability
Zone power loss does it not produce, and which parts of your workload
(the load balancer's own nodes in that zone, for example) does it leave
untouched?_

##### Question: The recovery action

_Five minutes into the scenario, `aws:arc:start-zonal-autoshift` shifts
traffic away from the Availability Zone. Which resources does it act on,
and what must be true of them first? You'll set that up in Lesson 27.4._

### Retrospective 27.2

#### Question: Production or not

_FIS is designed to run in production. Why would you ever do that? List
what must be true before a team runs its first experiment in production
(think about stop conditions, the safety lever, observability, the
blast radius, who is on call and who has been told)._

#### Question: Experiments in the pipeline

_How would you run the CPU stress experiment as a stage of the module 12
pipeline after every deployment to a test environment? What would count
as a failure, and what would the pipeline do about it?_

## Lesson 27.3: AWS Resilience Hub

### Principle 27.3

*Resilience Hub turns RTO and RPO into a policy and checks your
architecture against it. Its answer is an estimate from configuration,
not a measurement; the experiments in Lesson 27.2 and the game day in
Lesson 27.5 are how you find out if the estimate holds.*

### Practice 27.3

In module 23 you put numbers on recovery and chose a DR strategy by hand.
Resilience Hub does a first pass of that automatically:

- A **resiliency policy** holds RTO and RPO targets for four disruption
  types: *Application* (bad code or configuration), *Cloud
  Infrastructure* (a failed component), *Cloud Infrastructure AZ
  disruption* and, optionally, *Cloud Infrastructure Region incident*. The
  CLI calls them `Software`, `Hardware`, `AZ` and `Region`.
- An **application** is a set of resources imported from CloudFormation
  stacks, Terraform state files, resource groups, AppRegistry or
  myApplications, grouped into **Application Components** that fail
  together.
- An **assessment** estimates the workload's RTO and RPO for each
  disruption type, marks the policy met or breached, and produces
  recommendations: architecture changes, CloudWatch alarms, standard
  operating procedures (SOPs, as SSM documents) and FIS experiments.

This lesson uses the original application model. At the end you compare
it with the next generation of Resilience Hub, launched in May 2026.

**The application costs $15 a month from its first assessment until you
delete it. Do Labs 27.3.1 to 27.3.4 in one sitting and delete it at the
end of Lab 27.3.4.**

Read [AWS Resilience Hub
concepts](https://docs.aws.amazon.com/resilience-hub/latest/userguide/concepts-terms.html)
first.

#### Lab 27.3.1: A resiliency policy from your RTO and RPO

Read [Creating resiliency
policies](https://docs.aws.amazon.com/resilience-hub/latest/userguide/create-policy.html)
and
[`create-resiliency-policy`](https://docs.aws.amazon.com/cli/latest/reference/resiliencehub/create-resiliency-policy.html).

- Decide targets for your web tier. It's stateless, so think about what
  RPO even means for it. Suggested: application RTO 1 hour, cloud
  infrastructure RTO 15 minutes, AZ RTO 15 minutes; no Region targets.
  Write down why you chose each.
- Create the policy `<you>-web` with the CLI, tier `Important`, and data
  location constraint `AnyLocation`. Values are in seconds.
- `aws resiliencehub list-resiliency-policies`. Look at the suggested
  policies AWS provides as well: `list-suggested-resiliency-policies`.
  Which one is closest to yours?

##### Question: RPO for a stateless tier

_What does an RPO mean for a tier that stores nothing? Which part of the
full application from module 23's Lab 23.3.1 would actually drive the
RPO, and should it be in the same Resilience Hub application?_

#### Lab 27.3.2: An application from your stack

Read [Invoker
role](https://docs.aws.amazon.com/resilience-hub/latest/userguide/security-iam-resilience-hub-invoker-role.html)
and [Get started by adding an
application](https://docs.aws.amazon.com/resilience-hub/latest/userguide/describe-app-intro.html).

- Create an **invoker role** that Resilience Hub assumes to read your
  resources: trusted by `resiliencehub.amazonaws.com`, with the AWS
  managed policy `AWSResilienceHubAsssessmentExecutionPolicy` (yes, three
  s's in "Asssessment"; that's its real name). Put it in its own small
  template. You'll need `iam:PassRole` on it to create the application.
- Create the application with `aws resiliencehub create-app`:
  `--name <you>-web`, your policy's ARN, a role-based permission model
  with your invoker role's name, and `--assessment-schedule Disabled`.
- Import the `<you>-resilience` stack as the application's input source
  with `import-resources-to-draft-app-version --source-arns <stack-arn>`.
  Poll `describe-draft-app-version-resources-import-status` until it
  succeeds.
- List what it imported with `list-app-version-resources` for the
  `draft` version. Which resources from your template are there, which
  are missing, and how were they grouped into Application Components?
- Publish the draft with `publish-app-version`.

##### Question: What it ignored

_Your stack has security groups, a launch template, IAM roles, alarms
and a listener. Which did Resilience Hub import? Read [supported
resources](https://docs.aws.amazon.com/resilience-hub/latest/userguide/supported-resources.html)
and explain the rule it uses to decide._

#### Lab 27.3.3: Assess and read the recommendations

Read [Running resiliency
assessments](https://docs.aws.amazon.com/resilience-hub/latest/userguide/run-assessment.html)
and [Reviewing assessment
reports](https://docs.aws.amazon.com/resilience-hub/latest/userguide/review-assessment.html).
Billing for the application starts now.

- Start an assessment of the `release` version with
  `start-app-assessment`. Poll `describe-app-assessment` until it
  finishes.
- Record, for each disruption type: the compliance status, the estimated
  workload RTO and RPO, and your policy's target. Record the resiliency
  score.
- Read the recommendations with:
  - `list-app-component-compliances` and
    `list-app-component-recommendations`;
  - `list-alarm-recommendations`;
  - `list-sop-recommendations`;
  - `list-test-recommendations`.
- Compare the test recommendations with the experiments you wrote in
  Lesson 27.2. Which did it suggest that you haven't written, and which
  of yours did it not think of? Compare the alarm recommendations with
  your steady-state alarms.

##### Question: Estimated, not measured

_The assessment estimated an RTO for an AZ disruption. Where does that
number come from? What did your Lab 27.2.3 experiment measure that the
estimate can't know?_

##### Question: Breached or met

_Was any disruption type breached? For each one, what is the smallest
change to `workload.yaml` that would meet the policy, and what would it
cost per month?_

#### Lab 27.3.4: Fix one thing, reassess, and delete the application

- Make one change to `workload.yaml` that a recommendation asked for (or
  that you believe improves the AZ disruption result), and update the
  stack.
- Reimport the stack into the draft version, publish it, and run a
  second assessment. What changed? Look for **drift** in the assessment.
- *Optional:* generate the recommended alarms or FIS experiments as a
  CloudFormation template with `create-recommendation-template` and read
  it. Don't deploy it.
- **Delete the application** with `aws resiliencehub delete-app`, then the
  resiliency policy with `delete-resiliency-policy`. Confirm with
  `list-apps` that it's gone. Keep the invoker role until Lab 27.5.4.

##### Question: The next generation

_Read [What is Next generation Resilience
Hub?](https://docs.aws.amazon.com/resilience-hub/latest/userguide/next-gen-what-is.html)
and [Failure mode
assessments](https://docs.aws.amazon.com/resilience-hub/latest/userguide/next-gen-failure-mode-assessments.html).
How do its *systems*, *services* and modular *resilience policies* map
onto the application, AppComponents and resiliency policy you used? What
does a GenAI-powered failure mode assessment add to a rules-based one,
and what would you still verify by hand? How is it billed?_

### Retrospective 27.3

#### Question: Continuous assessment

_You turned the daily schedule off to control the lab. In a real team,
what would a daily assessment plus drift notifications to SNS catch that
a deployment pipeline wouldn't? Who should get the notification?_

#### Question: One application or many

_Your organization has 40 services. Would you create one Resilience Hub
application per service, per team, or per business capability? Think
about RTO targets, ownership and the per-application price._

## Lesson 27.4: Application Recovery Controller

### Principle 27.4

*Recover with the simplest action that doesn't depend on the thing that
is broken. Moving traffic away from a sick Availability Zone is one API
call on a highly available data plane; waiting for the zone to heal, or
redeploying into the other zones, is not.*

### Practice 27.4

Amazon Application Recovery Controller (ARC) has two families of
features:

- **Within a Region:** *zonal shift* moves traffic for a supported
  resource (Application and Network Load Balancers, EC2 Auto Scaling
  groups, EKS clusters) away from one Availability Zone for a time you
  choose, up to three days. *Zonal autoshift* lets AWS start that shift
  for you when its own telemetry sees an Availability Zone impairment,
  and requires weekly *practice runs* that prove your application
  survives it. Both are free.
- **Across Regions:** *routing control* (on/off switches, backed by Route
  53 health checks, on a highly available cluster) and *Region switch*
  (orchestrated, multi-step Region failover plans). Both are billed
  whether or not you use them, so this course covers them on paper.

Read [Zonal shift in
ARC](https://docs.aws.amazon.com/r53recovery/latest/dg/arc-zonal-shift.html)
and [Zonal autoshift in
ARC](https://docs.aws.amazon.com/r53recovery/latest/dg/arc-zonal-autoshift.html).
Keep the workload running with two instances in two Availability Zones.

#### Lab 27.4.1: Register the workload for zonal shift

Read the resource requirements for [Application Load
Balancers](https://docs.aws.amazon.com/r53recovery/latest/dg/arc-zonal-shift.resource-types.app-load-balancers.html)
and [EC2 Auto Scaling
groups](https://docs.aws.amazon.com/r53recovery/latest/dg/arc-zonal-shift.resource-types.ec2-auto-scaling-groups.html).

- In `workload.yaml`, fill in the two `TODO(student)` markers for this
  lab:
  - turn on ARC zonal shift integration in the load balancer's
    attributes;
  - give the Auto Scaling group an `AvailabilityZoneImpairmentPolicy`
    that enables zonal shift. Choose the impaired-zone health check
    behavior and write down why.
- Update the stack. List the resources ARC now manages with
  `aws arc-zonal-shift list-managed-resources`, and look at your load
  balancer with `get-managed-resource`. What does it report for
  `appliedWeights` and `zonalShifts`?
- Find the **Availability Zone IDs** of your two subnets
  (`aws ec2 describe-subnets`, field `AvailabilityZoneId`). Zonal shift
  takes IDs, not names.

##### Question: Names and IDs

_Why does ARC use Availability Zone IDs (`use2-az1`) instead of names
(`us-east-2a`)? What goes wrong in a multi-account organization if a
runbook says "shift away from us-east-2a"?_

#### Lab 27.4.2: Shift away from an Availability Zone

Read [Starting, updating, or canceling a zonal
shift](https://docs.aws.amazon.com/r53recovery/latest/dg/arc-zonal-shift.start-cancel.html)
and [Best practices for zonal
shifts](https://docs.aws.amazon.com/r53recovery/latest/dg/route53-arc-best-practices.zonal-shifts.html).

- With the probe running, resolve the load balancer's DNS name with
  `dig +short` and note the addresses.
- Start a zonal shift on the **load balancer** away from one of your
  Availability Zone IDs with `start-zonal-shift`, expiring in 30 minutes,
  with a comment.
- Watch:
  - the probe: which Availability Zone answers now, and how quickly did
    the other one stop answering?
  - `dig +short` again: what changed?
  - `aws elbv2 describe-target-health`: look for `AdministrativeOverride`
    on the targets in the shifted-away zone. Are they healthy?
- Cancel the shift with `cancel-zonal-shift` and watch traffic return.
- Now start a zonal shift on the **Auto Scaling group** away from the
  same zone, and while it's active, scale the group out by one with
  `set-desired-capacity`. Where does the new instance launch? Scale back
  in and cancel the shift.

##### Question: Shift or stop

_Compare this with Lab 27.2.3, where the instances in one zone were
stopped. Which was faster for users, and why? What did the shift not
depend on that the stopped-instance recovery did (health checks, Auto
Scaling, EC2 launches)?_

##### Question: Clients that don't let go

_The load balancer's DNS no longer returned the shifted zone's address,
but some requests may still have reached it for a while. Why? Which
settings, on the client and on the load balancer, decide how long?_

##### Question: Cross-zone load balancing

_Your load balancer has cross-zone load balancing on (the ALB default).
With a zonal shift active, can a load balancer node in a healthy zone
still send requests to a target in the shifted zone? Read the
[ALB zonal shift](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/zonal-shift.html)
page and explain what "administrative override" does._

#### Lab 27.4.3: Zonal autoshift and a practice run

Read [Enabling and working with zonal
autoshift](https://docs.aws.amazon.com/r53recovery/latest/dg/arc-zonal-autoshift.start-cancel.html)
and [`create-practice-run-configuration`](https://docs.aws.amazon.com/cli/latest/reference/arc-zonal-shift/create-practice-run-configuration.html).
Autoshift is free; its practice runs shift your traffic for about 30
minutes every week while it's enabled.

- Create a practice run configuration for the **load balancer**: your
  error alarm as the **outcome alarm**, the capacity alarm as a
  **blocking alarm**, and blocked windows that keep practice runs away
  from times you'd be working through other labs.
- Enable zonal autoshift for the load balancer with
  `update-zonal-autoshift-configuration`.
- Start an on-demand practice run with `start-practice-run`, with the
  probe running. Follow it with `list-zonal-shifts` and watch for its
  outcome.
- *Optional:* set up an EventBridge rule for zonal autoshift events (see
  [Using zonal autoshift with Amazon
  EventBridge](https://docs.aws.amazon.com/r53recovery/latest/dg/eventbridge-zonal-autoshift.html))
  that sends them to the SNS topic from module 08 or 24.
- Leave autoshift enabled until Lab 27.5.4, which disables it and deletes
  the practice run configuration.

##### Question: Pre-scaling

_AWS strongly recommends pre-scaling before you enable autoshift, and
warns that autoshift doesn't wait for Auto Scaling. With two instances
in two zones, what fraction of capacity does a practice run leave you?
What `MinSize` and instance count would let you lose a zone with no loss
of capacity, and what would it cost?_

##### Question: Outcome and blocking alarms

_What is the difference between the outcome alarm and the blocking
alarm? What does ARC do if the outcome alarm fires during a practice run,
and why would you not want a practice run to start while the capacity
alarm is already in `ALARM`?_

#### Lab 27.4.4: Routing control and Region switch, on paper

No AWS resources in this lab. **Don't create a routing control cluster:
it costs $2.50 an hour from the moment it exists.** Read:

- [Routing control in
  ARC](https://docs.aws.amazon.com/r53recovery/latest/dg/routing-control.html),
  including how a cluster's five Regional endpoints work and what safety
  rules are;
- [Region switch in
  ARC](https://docs.aws.amazon.com/r53recovery/latest/dg/region-switch.html);
- the [readiness check availability
  change](https://docs.aws.amazon.com/r53recovery/latest/dg/arc-readiness-availability-change.html);
- your answer to module 21's question "DNS or something else".

Then sketch, in your answers, an active/passive version of this workload
in `us-east-2` and your DR Region from module 23, failed over by routing
control. Show the Route 53 records, the health checks that routing
controls drive, one assertion rule and one gating rule, and the command
an operator runs to fail over. Then list what a Region switch plan would
do in addition.

##### Question: Control plane and data plane

_Why must you fail over with the routing control cluster's data plane API
(`route53-recovery-cluster update-routing-control-state`) and not by
editing Route 53 records? Which part of Route 53 is the control plane,
and why does the DR whitepaper from module 23 worry about it?_

##### Question: Worth $1,800 a month

_Routing control costs about $1,800 a month per cluster, whatever you
use it for. For which workloads is that cheap? For the workload in this
module, what would you use instead?_

### Retrospective 27.4

#### Question: Static stability

_Read [Static stability using Availability
Zones](https://aws.amazon.com/builders-library/static-stability-using-availability-zones/).
Is your workload statically stable against the loss of one Availability
Zone? List what it would need, and which of this module's labs would
prove it._

#### Question: Zonal shift after a bad deployment

_Zonal shift is also meant for a bad deployment that has reached only one
Availability Zone. What would your deployment strategy from Lesson 27.1
have to look like for that to be possible?_

## Lesson 27.5: Game days and runbooks

### Principle 27.5

*A runbook nobody has run is a guess, and a recovery nobody has
practised takes longer than anyone thinks. A game day is where a team
finds out, on a day it chose, instead of at 3 a.m. on a day it didn't.*

### Practice 27.5

A **runbook** is the written, tested procedure for one kind of event:
how to recognize it, who decides, what to run, how to check it worked,
and how to go back. A **game day** is a planned exercise in which one
person injects a failure (here, with your FIS experiments) and the
people on call detect, diagnose and recover from it using the runbook,
while someone keeps time and notes. A **post-incident review** turns what
went wrong into actions, without blaming people.

Read the Well-Architected guidance on [conducting game
days](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_testing_resiliency_game_days_resiliency.html),
[testing resiliency with chaos
engineering](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_testing_resiliency_failure_injection_resiliency.html)
and [using
runbooks](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_ready_to_support_use_runbooks.html).

#### Lab 27.5.1: A runbook for "one AZ is sick"

Write `runbooks/az-impairment.md` in your repository for this workload.
It must fit on one page and have these sections:

1. **Detection.** Which alarms fire, which metrics you look at (per
   Availability Zone, from the load balancer), and which AWS Health
   events would tell you it's AWS and not you.
2. **Decision.** Who decides to shift, and the rule they use. (For
   example: "if one zone's 5XX rate is more than X times the others' for
   Y minutes, shift; don't wait for a root cause.")
3. **Action.** The exact commands, with Availability Zone **IDs**, for
   the load balancer and the Auto Scaling group, and in which order.
4. **Verification.** How you know the shift worked.
5. **Recovery.** When and how you cancel the shift, in which order for the
   load balancer and the Auto Scaling group, and why the order matters
   (see the ASG best practices in Lab 27.4.1's reading).
6. **Communication.** Who you tell and what you say.

*Optional:* turn the Action section into a Systems Manager Automation
runbook (module 20, Lab 20.4.3) that takes the Availability Zone ID as a
parameter and starts both shifts.

##### Question: The runbook's own dependencies

_What does your runbook depend on to work: which consoles, APIs, IAM
roles and credentials? Which of those could be affected by the same
event? Does zonal shift depend on anything in the impaired zone?_

#### Lab 27.5.2: Run a game day

Do this with your mentor. One of you is the **injector**; the other is
**on call**. If you're working alone, write a small script that picks
one of your experiment templates at random and starts it at a random
time in the next half hour, and don't look at which one it chose.

- **Before:** agree the scope (only your lab stacks), the time box (one
  hour), the stop conditions (every experiment has one), who pulls the
  safety lever if things go wrong, and what counts as recovered. Write
  them down.
- **During:** the injector starts one experiment from Lesson 27.2 without
  saying which. The person on call watches only the alarms and dashboards
  a real on-call engineer would have (not the FIS console), follows
  `runbooks/az-impairment.md` or improvises if it doesn't fit, and says
  out loud what they think is happening. The injector records the time
  of each event: fault injected, first alarm, first human notice,
  diagnosis, mitigation started, steady state restored.
- Run at least two rounds, swapping roles if you can. One round should
  be the "lose one AZ" experiment.

##### Question: Time to detect, time to mitigate

_Fill in the timeline for each round. Where did the time go: detection,
diagnosis or mitigation? Which of those would zonal autoshift have
removed?_

#### Lab 27.5.3: The post-incident review

Write `reviews/<date>-game-day.md` for the most interesting round, in the
shape of AWS's [correction of errors
(COE)](https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_evolve_ops_perform_rca_process.html)
process:

- a summary a manager can read in 30 seconds;
- the timeline from Lab 27.5.2;
- impact, in the steady-state terms from Lab 27.1.1;
- "five whys" for the slowest part of the response;
- what went well;
- action items, each with an owner, a due date and whether it prevents,
  detects or mitigates.

Carry out at least one action item before you finish the module (a
better alarm, a runbook fix, a new experiment).

##### Question: Blameless

_Rewrite this finding so that it would survive a blameless review: "The
on-call engineer ran the command for the wrong Availability Zone." What
system change makes the mistake impossible or harmless?_

#### Lab 27.5.4: Clean up the module

Resources in this module are spread across stacks, FIS, Resilience Hub
and ARC. Work through the list in order.

1. **FIS:** list experiments (`aws fis list-experiments`) and stop any
   that are running. Check that the safety lever is **disengaged**
   (`get-safety-lever --id default`). Delete the `<you>-fis` stack (the
   role, experiment templates and log group) and any template you
   created by hand (`list-experiment-templates`).
2. **ARC:** cancel any active zonal shift (`list-zonal-shifts`). Disable
   zonal autoshift for the load balancer, then delete its practice run
   configuration (`delete-practice-run-configuration`). Confirm with
   `get-managed-resource`.
3. **Resilience Hub:** confirm `aws resiliencehub list-apps` and
   `list-resiliency-policies` show nothing of yours (Lab 27.3.4 should
   have deleted them). Delete the invoker role's stack.
4. **The workload:** delete the `<you>-resilience` stack. It deletes the
   load balancer, target groups, both Auto Scaling groups, the launch
   template, alarms, security groups and roles.
5. **Anything else:** EventBridge rules or SNS subscriptions from the
   optional steps, and the `probe.log` files (don't commit load balancer
   DNS names you'd rather keep private).

Finally, with the `lab` profile:

- `aws elbv2 describe-load-balancers` and
  `aws autoscaling describe-auto-scaling-groups` show nothing of yours;
- `aws fis list-experiment-templates` is empty of your templates;
- `aws arc-zonal-shift list-managed-resources` no longer lists your
  resources;
- `aws resiliencehub list-apps` is empty;
- `aws cloudwatch describe-alarms --alarm-name-prefix <you>` is empty.

### Retrospective 27.5

#### Question: How often

_How often should a team run a game day, and how would you decide which
failure to practise next? What should trigger an unscheduled one?_

#### Question: From game day to automation

_Look back over the module. Which parts of your response could be
automated safely (autoshift, alarms that roll back a deployment,
experiments in the pipeline), and which should stay a human decision?
Why?_

## Further Reading

- [Resilience analysis
  framework](https://docs.aws.amazon.com/prescriptive-guidance/latest/resilience-analysis-framework/introduction.html)
  (AWS Prescriptive Guidance): the failure categories behind Resilience
  Hub's assessments.
- [Advanced Multi-AZ Resilience
  Patterns](https://docs.aws.amazon.com/whitepapers/latest/advanced-multi-az-resilience-patterns/advanced-multi-az-resilience-patterns.html)
  (whitepaper): detecting gray failures in one Availability Zone and
  isolating them with zonal shift.
- [Disaster Recovery of Workloads on
  AWS](https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-workloads-on-aws.html),
  from module 23, for the multi-Region side that routing control and
  Region switch serve.
- The [FIS scenario
  library](https://docs.aws.amazon.com/fis/latest/userguide/scenario-library.html),
  including cross-Region connectivity scenarios, and
  [multi-account
  experiments](https://docs.aws.amazon.com/fis/latest/userguide/multi-account.html)
  for organizations like the one from module 19.
- [Amazon ECS blue/green service deployments
  workflow](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/blue-green-deployment-how-it-works.html)
  and [CodeDeploy blue/green deployments for Amazon
  ECS](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-type-bluegreen.html),
  to compare the two ways ECS shifts traffic.
- [Principles of Chaos Engineering](https://principlesofchaos.org/): the
  short manifesto that the experiment vocabulary in Lesson 27.2 comes
  from.
