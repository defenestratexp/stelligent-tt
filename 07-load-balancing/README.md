# Topic 7: Load Balancers

<!-- TOC -->

- [Topic 7: Load Balancers](#topic-7-load-balancers)
  - [What changed in the 2026 edition](#what-changed-in-the-2026-edition)
  - [Exam coverage](#exam-coverage)
  - [Cost and cleanup](#cost-and-cleanup)
  - [Guidance](#guidance)
  - [Lesson 7.1: Introduction to Load Balancers](#lesson-71-introduction-to-load-balancers)
    - [Principle 7.1](#principle-71)
    - [Practice 7.1](#practice-71)
      - [Lab 7.1.1: An ALB in Front of an ASG](#lab-711-an-alb-in-front-of-an-asg)
        - [Question: Listeners and Target Groups](#question-listeners-and-target-groups)
        - [Question: Security Group Chaining](#question-security-group-chaining)
        - [Question: Grace Period](#question-grace-period)
      - [Lab 7.1.2: Health Checks](#lab-712-health-checks)
        - [Question: Health Checks](#question-health-checks)
        - [Question: ASG Behavior](#question-asg-behavior)
        - [Question: Fail Open](#question-fail-open)
      - [Lab 7.1.3: HTTPS with a TLS 1.3 Security Policy](#lab-713-https-with-a-tls-13-security-policy)
        - [Question: Default Policy](#question-default-policy)
        - [Question: SSL Policy](#question-ssl-policy)
        - [Question: Certificate Management](#question-certificate-management)
      - [Lab 7.1.4: Clean Up](#lab-714-clean-up)
    - [Retrospective 7.1](#retrospective-71)
      - [Question: ALB Architectures](#question-alb-architectures)
      - [Question: Ready or Healthy?](#question-ready-or-healthy)
  - [Further Reading](#further-reading)

<!-- /TOC -->

## What changed in the 2026 edition

- The starter template, [asg_example.yaml](asg_example.yaml), is rewritten.
  It uses a launch template instead of a launch configuration (accounts
  created after 2024-10-01 can't create launch configurations), Amazon Linux
  2023 from the SSM public parameter instead of a hard-coded Amazon Linux 1
  AMI, `t3.micro` instead of `t2.micro`, and IMDSv2 required. It installs
  `aws-cfn-bootstrap` with `dnf` and manages nginx with systemd.
- The old template's `cfn-signal` never worked: it signalled the launch
  configuration, which can't receive signals, and the Auto Scaling group had
  no `CreationPolicy`. The new template signals the Auto Scaling group, which
  waits for three signals on create and on rolling updates.
- The `REPLACE_WITH_...` placeholders are gone. VPC, subnets and your
  identifier are stack parameters.
- The web servers accept HTTP only from the load balancer's security group,
  and nothing accepts SSH. Use Session Manager if you need a shell.
- Lab 7.1.3 now teaches TLS 1.3 security policies, including the hybrid
  post-quantum (`PQ`) policies, and the fact that CloudFormation and the CLI
  still default to `ELBSecurityPolicy-2016-08`. The old "pick a policy with FS
  in its name" step is replaced.
- Lab 7.1.3 offers two certificate paths: a public ACM certificate if you have
  a domain, or an imported self-signed certificate if you don't. It also adds
  an HTTP-to-HTTPS redirect.
- Lab 7.1.2 adds a question about how an ALB *fails open* when every target is
  unhealthy.
- New: cost notes, a full clean-up lab, and replacements for dead links (the
  self-signed certificate guide and the ECS blog post).

## Exam coverage

| Exam | Domain / task statement |
|---|---|
| SAA-C03 | Domain 2: Design Resilient Architectures (2.1 scalable and loosely coupled architectures, 2.2 highly available and fault-tolerant architectures) |
| SAA-C03 | Domain 1: Design Secure Architectures (1.2 secure workloads and applications, 1.3 data security controls: encryption in transit, ACM) |
| SOA-C03 | Domain 2: Reliability and Business Continuity (ELB health checks with Auto Scaling) |
| SOA-C03 | Domain 5: Networking and Content Delivery (load balancer listeners, target groups, troubleshooting) |
| SOA-C03 | Domain 4: Security and Compliance (TLS security policies, certificates) |
| SCS-C03 | Domain 5: Data Protection (encryption in transit) |

## Cost and cleanup

- **Load balancers have an hourly charge.** An Application Load Balancer costs
  about $0.0225 per hour plus a charge per load balancer capacity unit (LCU),
  roughly $16 a month before traffic. See
  [Elastic Load Balancing pricing](https://aws.amazon.com/elasticloadbalancing/pricing/).
  <!-- VERIFY: the pricing page shows $0.0225/hour for us-east-1; confirm the us-east-2 rate. -->
- **Public IPv4 addresses cost $0.005 per hour each**, in use or idle
  ([VPC pricing](https://aws.amazon.com/vpc/pricing/)). An internet-facing
  ALB uses at least one per Availability Zone, and the starter template gives
  each of the three web servers one. That's at least five addresses, about
  $18 a month.
- Three `t3.micro` instances add roughly $23 a month. Left running, this
  module costs about $60 a month. The AWS Free Tier may cover part of it in a
  new account; don't count on it.
- Public ACM certificates used with a load balancer are free, and so are
  imported certificates. If you register a domain or create a Route 53 hosted
  zone for Lab 7.1.3, those are billed separately (a hosted zone is $0.50 a
  month).
  <!-- VERIFY: ACM's pricing page confirms ACM-issued public certificates are free for integrated services; it doesn't mention imported certificates. -->
- Deploy, do the lab, and delete the stack the same day. Lab 7.1.4 removes
  everything this module creates.

## Guidance

- Explore the official docs! See the
  [Application Load Balancer User Guide](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/introduction.html),
  the [elbv2 CLI reference](https://docs.aws.amazon.com/cli/latest/reference/elbv2/),
  and the CloudFormation reference for
  [load balancers](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-elasticloadbalancingv2-loadbalancer.html),
  [target groups](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-elasticloadbalancingv2-targetgroup.html)
  and
  [listeners](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-elasticloadbalancingv2-listener.html).

- Avoid using other sites like stackoverflow.com for answers \-- part
  of the skill set you're building is finding answers straight from
  the source, AWS. Older tutorials use launch configurations, Amazon Linux 2
  and the FS security policies; all three are out of date.

- Explore your curiosity. Try to understand why things work the way
  they do. Read more of the documentation than just what you need to
  find the answers.

- Work in your lab account with the `lab` profile from module 19
  (`export AWS_PROFILE=lab`). The profile sets the lab region, `us-east-2`,
  so the commands in this module don't need `--region`.

- Build everything with CloudFormation in YAML and inspect it with the CLI.
  The console is useful for *looking* at target health, but make your changes
  in the template.

## Lesson 7.1: Introduction to Load Balancers

### Principle 7.1

*Application Load Balancers are the best general-purpose service for
distributing web traffic to many servers in multiple Availability
Zones.*

This section demonstrates the setup, management, and configuration you
may run into on an engagement involving load balancers. It isn't an
exhaustive look at Elastic Load Balancing, but it gives you the
fundamentals and tells you where to look next. Elastic Load Balancing has
other types for other jobs:
[Network Load Balancers](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/introduction.html)
for TCP, UDP and TLS at layer 4, and
[Gateway Load Balancers](https://docs.aws.amazon.com/elasticloadbalancing/latest/gateway/introduction.html)
for inserting network appliances. Classic Load Balancers are the legacy type;
don't build new ones.

### Practice 7.1

This section gets you familiar with the basic setup of an Application Load
Balancer (ALB): listeners, target groups and health checks, how the ALB
works with an Auto Scaling group, and how to terminate TLS with a
certificate and a modern security policy.

#### Lab 7.1.1: An ALB in Front of an ASG

In Topic 6, you created Auto Scaling groups (ASGs) from launch templates. In
this lab you take an ASG of instances that serve a web page on port 80 and
put an internet-facing ALB in front of them.

- Copy [asg_example.yaml](asg_example.yaml) into your repository and read it
  first. Note how the instances get their AMI (an SSM public parameter),
  how `cfn-init` reads its configuration from the launch template's
  metadata, and which resource `cfn-signal` signals and why.

- Deploy it as is, to check that it works before you change anything. You
  need your VPC ID and two public subnets in different Availability Zones:
  the default VPC's subnets are fine
  (`aws ec2 describe-subnets --filters Name=default-for-az,Values=true`).
  The template creates an IAM role, so `aws cloudformation deploy` needs
  `--capabilities CAPABILITY_IAM`. The stack reaches `CREATE_COMPLETE` only
  after all three instances signal success.

- Extend the template:

  - A security group for the load balancer that allows HTTP (and, for Lab
    7.1.3, HTTPS) from the internet.
  - An ingress rule on the web servers' security group that allows port 80
    *from the load balancer's security group only*.
  - A [target group](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-elasticloadbalancingv2-targetgroup.html)
    for the instances, with a health check on `/index.html`.
  - An internet-facing
    [ALB](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-elasticloadbalancingv2-loadbalancer.html)
    in the same public subnets.
  - An HTTP
    [listener](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-elasticloadbalancingv2-listener.html)
    on port 80 that forwards to the target group.
  - On the Auto Scaling group,
    [attach the target group](https://docs.aws.amazon.com/autoscaling/ec2/userguide/attach-load-balancer-asg.html),
    set `HealthCheckType` to `ELB`, and choose a `HealthCheckGracePeriod`.
  - An output with the ALB's DNS name.

- Update the stack, then browse to (or `curl`) the DNS name. Check the
  targets with `aws elbv2 describe-target-health`.

##### Question: Listeners and Target Groups

_What is the benefit of breaking up the load balancer into specific listeners
and target groups?_

##### Question: Security Group Chaining

_Why reference the load balancer's security group instead of opening port 80
to the VPC CIDR or to `0.0.0.0/0`? Can you still reach an instance directly on
its public IP address?_

##### Question: Grace Period

_How long does your instance take from launch until nginx serves the page?
(Look in `/var/log/cfn-init.log` through Session Manager, or at the stack
events.) What happens if the grace period is shorter than that, and what
happens if it's much longer?_

#### Lab 7.1.2: Health Checks

Now, let's break the health check to see what happens when things go
haywire!

- Modify the target group:

  - Update the health check path to `/BADindex.html`
  - Change the interval to 20 seconds
  - Change the healthy threshold to 2
  - Change the unhealthy threshold to 3
  - Add a target group attribute with key
    `deregistration_delay.timeout_seconds`, value 20

- Wait about two minutes after the stack update completes.

- Go to your load balancer endpoint, and watch the targets with
  `aws elbv2 describe-target-health` and the group's activity with
  `aws autoscaling describe-scaling-activities`.

##### Question: Health Checks

_What can be controlled with the interval, healthy threshold and unhealthy
threshold settings? With your values, how long does it take a failing target
to be marked unhealthy?_

##### Question: ASG Behavior

_What's happening to the instances in the ASG? How do you know?_

##### Question: Fail Open

_Did the page still load at any point while every target was failing its
health check? Read
[health checks for target groups](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/target-group-health-checks.html)
and explain what you saw. Why would AWS design it that way?_

#### Lab 7.1.3: HTTPS with a TLS 1.3 Security Policy

Fix the bad health check, confirm every target is healthy again, and then
add an HTTPS listener.

You need a certificate. Pick the path that fits what you have:

- **You have a domain** whose DNS you control (in Route 53 or elsewhere):
  [request a public certificate](https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-request-public.html)
  from AWS Certificate Manager (ACM) in `us-east-2` for a name such as
  `lb-<your-identifier>.<your-domain>`, and complete
  [DNS validation](https://docs.aws.amazon.com/acm/latest/userguide/dns-validation.html).
  Then point that name at the ALB (a Route 53 alias record, or a CNAME at
  your DNS provider). Browsers will trust this certificate.

- **You don't have a domain**: create a self-signed certificate with
  `openssl` and
  [import it into ACM](https://docs.aws.amazon.com/acm/latest/userguide/import-certificate.html)
  with `aws acm import-certificate`. Check the
  [import prerequisites](https://docs.aws.amazon.com/acm/latest/userguide/import-certificate-prerequisites.html)
  first. Put the ALB's DNS name in the certificate's `subjectAltName`
  (`openssl req -addext`), because the common name (CN) is limited to 64
  characters and ALB DNS names can be longer. The CLI reads the certificate
  and key files with `fileb://`.
  CloudFormation can't import certificates, so do this with the CLI
  and pass the certificate ARN to your stack as a parameter. Keep the private
  key out of your Git repository. Your browser will warn you, because it
  doesn't trust a certificate you signed yourself.

Then:

- Add a listener on port 443 using HTTPS that references your certificate
  and forwards to the target group.

- Set its `SslPolicy` to a
  [security policy](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/describe-ssl-policies.html)
  that supports TLS 1.3. Start with the policy AWS recommends,
  `ELBSecurityPolicy-TLS13-1-2-Res-PQ-2025-09`, and compare it with the others
  using `aws elbv2 describe-ssl-policies`.

- Change the port 80 listener's default action to a
  [redirect](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/rule-action-types.html)
  to HTTPS instead of forwarding.

- Test it. `curl -v` shows the TLS version it negotiated (add `-k` for a
  self-signed certificate). `openssl s_client -connect <alb-dns-name>:443`
  with `-tls1_1`, `-tls1_2` and `-tls1_3` shows which versions the listener
  accepts.

- Switch the listener to `ELBSecurityPolicy-TLS13-1-3-PQ-2025-09` (TLS 1.3
  only) and repeat the `openssl` tests.

##### Question: Default Policy

_Which security policy does a listener get if you leave out `SslPolicy` in
CloudFormation? Which does it get when you create it in the console? Which
TLS versions does the CloudFormation default allow?_

##### Question: SSL Policy

_What is the trade-off of going with a more secure security policy? How
would you find out whether any real clients still connect with TLS 1.2
before you switch to a TLS 1.3-only policy?_

##### Question: Certificate Management

_What are your options for getting a certificate onto a load balancer (a
public ACM certificate, an imported certificate, AWS Private CA)? Which ones
renew automatically, and who is responsible for renewing the others?_

#### Lab 7.1.4: Clean Up

[Load balancers bill by the hour](https://aws.amazon.com/elasticloadbalancing/pricing/),
so don't leave this running.

- Delete your stack and wait for the deletion to finish
  (`aws cloudformation wait stack-delete-complete`).
- Delete the certificate from ACM: the imported self-signed certificate, or
  the public certificate you requested. ACM refuses to delete a certificate
  that a load balancer still uses, which is why the stack goes first.
- If you took the domain path, delete the DNS validation record and the
  record that pointed at the ALB, and any hosted zone you created just for
  this lab.
- Confirm nothing is left:
  `aws elbv2 describe-load-balancers` should list nothing of yours, and
  `aws ec2 describe-instances --filters Name=tag:Student,Values=<your-identifier> Name=instance-state-name,Values=running`
  should return no instances.

### Retrospective 7.1

#### Question: ALB Architectures

_What are some of the common cloud architectures where you would want an
ALB? When would you choose a Network Load Balancer instead?_

#### Question: Ready or Healthy?

_Your instances call `cfn-signal` as soon as `cfn-init` finishes, before the
ALB has marked them healthy. Why can that let a broken rolling update
"succeed"? How would you make an instance signal only after it passes the
load balancer's health check? (The
[`CreationPolicy` documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-attribute-creationpolicy.html)
points to an example.)_

Discuss with your mentor: the starter template gives every web server a
public IP address so it can reach `dnf` and CloudFormation. What would a
production version look like, and what would it cost?

## Further Reading

- [Target groups](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-target-groups.html)
  and [target group attributes](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/edit-target-group-attributes.html):
  sticky sessions, slow start, routing algorithms and target group health
  thresholds.
- [Path-based routing](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/tutorial-load-balancer-routing.html)
  with listener rules, which is how one ALB fronts many services. Module 13
  puts a load balancer in front of ECS services.
- [Mutual TLS authentication](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/mutual-authentication.html)
  on an ALB listener.
- [Troubleshooting Application Load Balancers](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-troubleshooting.html),
  including why targets fail health checks.
- [Post-quantum cryptography at AWS](https://aws.amazon.com/security/post-quantum-cryptography/),
  the background to the `PQ` security policies.
