# Topic 4: Virtual Private Clouds (VPCs)

<!-- TOC -->

- [Topic 4: Virtual Private Clouds (VPCs)](#topic-4-virtual-private-clouds-vpcs)
  - [What changed in the 2026 edition](#what-changed-in-the-2026-edition)
  - [Exam coverage](#exam-coverage)
  - [Cost and cleanup](#cost-and-cleanup)
  - [Guidance](#guidance)
  - [Lesson 4.1: Creating Your Own VPC](#lesson-41-creating-your-own-vpc)
    - [Principle 4.1](#principle-41)
    - [Practice 4.1](#practice-41)
      - [Lab 4.1.1: New VPC with "Private" Subnet](#lab-411-new-vpc-with-private-subnet)
      - [Lab 4.1.2: Internet Gateway](#lab-412-internet-gateway)
      - [Lab 4.1.3: Instance Role for Session Manager](#lab-413-instance-role-for-session-manager)
      - [Lab 4.1.4: Test Instance](#lab-414-test-instance)
        - [Question: Post Launch](#question-post-launch)
        - [Question: Verify Connectivity](#question-verify-connectivity)
      - [Lab 4.1.5: Security Group](#lab-415-security-group)
        - [Question: Connectivity](#question-connectivity)
      - [Lab 4.1.6: Public IPv4 Address](#lab-416-public-ipv4-address)
        - [Question: Ping](#question-ping)
        - [Question: Session Manager](#question-session-manager)
        - [Question: Traffic](#question-traffic)
        - [Question: What the Address Costs](#question-what-the-address-costs)
      - [Lab 4.1.7: NAT Gateway](#lab-417-nat-gateway)
        - [Question: Access](#question-access)
        - [Question: Egress](#question-egress)
        - [Question: Deleting the Gateway](#question-deleting-the-gateway)
        - [Question: Recreating the Gateway](#question-recreating-the-gateway)
        - [Question: One per Availability Zone](#question-one-per-availability-zone)
      - [Lab 4.1.8: EC2 Instance Connect Endpoint](#lab-418-ec2-instance-connect-endpoint)
        - [Question: Without the NAT Gateway](#question-without-the-nat-gateway)
        - [Question: Two Ways In](#question-two-ways-in)
      - [Lab 4.1.9: Network ACL](#lab-419-network-acl)
        - [Question: EC2 Connection](#question-ec2-connection)
        - [Question: Return Traffic](#question-return-traffic)
      - [Lab 4.1.10: Reachability Analyzer](#lab-4110-reachability-analyzer)
        - [Question: Blocking Component](#question-blocking-component)
    - [Retrospective 4.1](#retrospective-41)
      - [Question: Bastions](#question-bastions)
      - [Question: Pausing the Lab](#question-pausing-the-lab)
  - [Lesson 4.2: Integration with VPCs](#lesson-42-integration-with-vpcs)
    - [Principle 4.2](#principle-42)
    - [Practice 4.2](#practice-42)
      - [Lab 4.2.1: VPC Peering](#lab-421-vpc-peering)
      - [Lab 4.2.2: EC2 across VPCs](#lab-422-ec2-across-vpcs)
        - [Question: Public to Private](#question-public-to-private)
        - [Question: Private to Public](#question-private-to-public)
        - [Question: No Way Out](#question-no-way-out)
      - [Lab 4.2.3: VPC Gateway Endpoint to S3](#lab-423-vpc-gateway-endpoint-to-s3)
        - [Question: Endpoint Policy vs Bucket Policy](#question-endpoint-policy-vs-bucket-policy)
        - [Question: Prefix Lists](#question-prefix-lists)
      - [Lab 4.2.4: IP Address Management with IPAM](#lab-424-ip-address-management-with-ipam)
        - [Question: Overlapping CIDRs](#question-overlapping-cidrs)
      - [Lab 4.2.5: Clean Up](#lab-425-clean-up)
    - [Retrospective 4.2](#retrospective-42)
      - [Question: Corporate Networks](#question-corporate-networks)
      - [Question: Many VPCs](#question-many-vpcs)
      - [Question: Guardrails](#question-guardrails)
  - [Further Reading](#further-reading)

<!-- /TOC -->

## What changed in the 2026 edition

- **No SSH bastion and no key pair.** The old Lab 4.1.3 (create a key pair)
  is replaced by an instance role for
  [Session Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html).
  You reach the public instance with Session Manager and the private one with
  an
  [EC2 Instance Connect Endpoint](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/connect-with-ec2-instance-connect-endpoint.html)
  (new Lab 4.1.8). No security group opens port 22 to the internet.
- **Public IPv4 costs money.** Since February 2024 every public IPv4 address,
  including Elastic IPs and the one on a NAT gateway, is billed hourly. Lab
  4.1.6 has you work out what your addresses cost.
- **NAT gateway cost and design.** Lab 4.1.7 adds questions on the hourly and
  per-GB charges, one NAT gateway per Availability Zone versus one shared, and
  the new *regional* availability mode.
- **New Lab 4.1.10:**
  [Reachability Analyzer](https://docs.aws.amazon.com/vpc/latest/reachability/what-is-reachability-analyzer.html)
  explains why a path is or isn't open without sending a packet.
- **New Lab 4.2.4:** [Amazon VPC IPAM](https://docs.aws.amazon.com/vpc/latest/ipam/what-it-is-ipam.html)
  for finding the public IPv4 addresses you pay for, and (optionally) for
  allocating non-overlapping VPC CIDRs from a pool.
- The test instances use Amazon Linux 2023 from its SSM public parameter, a
  t3 instance type and IMDSv2. The old "AMI ID and T2 instance type in a
  parameter file" instructions are gone.
- VPC peering (Lab 4.2.1) now stays in the lab region; peering across regions
  is an optional stretch. The S3 gateway endpoint lab creates its own bucket
  instead of relying on the one deleted at the end of module 02.
- New retrospective questions on Transit Gateway and on
  [VPC Block Public Access](https://docs.aws.amazon.com/vpc/latest/userguide/security-vpc-bpa.html).
- New: a cost section, a final cleanup lab, and current documentation links
  in place of the old `/AmazonVPC/latest/UserGuide/` and Quick Start links.

## Exam coverage

| Exam | Domain / task statement |
|---|---|
| SAA-C03 | Domain 1: Design Secure Architectures (1.2 secure workloads and applications) |
| SAA-C03 | Domain 3: Design High-Performing Architectures (3.4 high-performing network architectures) |
| SAA-C03 | Domain 4: Design Cost-Optimized Architectures (4.4 cost-optimized network architectures) |
| SOA-C03 | Domain 5: Networking and Content Delivery (5.1 networking features and connectivity; 5.3 troubleshoot network connectivity) |
| SOA-C03 | Domain 4: Security and Compliance (Session Manager instead of open SSH) |
| SCS-C03 | Domain 3: Infrastructure Security (network segmentation, security groups and network ACLs) |
| CLF-C02 | Domain 3: Cloud Technology and Services (network services) |

## Cost and cleanup

Prices are for `us-east-2` in September 2026; see
[Amazon VPC pricing](https://aws.amazon.com/vpc/pricing/).

- **NAT gateway: the expensive part.** $0.045 per hour (about $33 a month)
  plus $0.045 per GB processed, plus its public IPv4 address. Delete it
  between study sessions (see [Pausing the Lab](#question-pausing-the-lab)).
- **Public IPv4 addresses:** $0.005 per hour each (about $3.60 a month),
  whether attached to a running instance, attached to a stopped one, or not
  attached at all. Your Elastic IP and the NAT gateway's address both count.
- **EC2 instances:** a t3.micro is about a cent an hour, and there are up to
  three of them. Stopped instances still pay for their EBS volumes.
- **Free:** VPCs, subnets, route tables, internet gateways, security groups,
  network ACLs, VPC peering within an Availability Zone, S3 gateway endpoints,
  EC2 Instance Connect Endpoints, and the IPAM Free Tier. Data crossing
  Availability Zones or a peering connection between zones is billed per GB;
  lab traffic makes that negligible.
- **Per use:** each Reachability Analyzer analysis costs $0.10. The IPAM
  Advanced Tier (optional in Lab 4.2.4) costs $0.00027 per active IP address
  per hour, which is fractions of a cent for this lab, but delete the IPAM
  when you're done.
- **Avoid:** interface VPC endpoints for Session Manager in the private-only
  VPC. You'd need three of them at about $0.01 per hour per Availability Zone
  each; Lab 4.2.2 uses a free EC2 Instance Connect Endpoint instead.
- Cleanup: [Lab 4.2.5](#lab-425-clean-up) deletes every stack, the S3 bucket
  and the IPAM, then checks that no Elastic IPs or NAT gateways are left.

## Guidance

- All CloudFormation templates are YAML and should pass
  [`cfn-lint`](https://github.com/aws-cloudformation/cfn-lint) before you
  create a stack from them.

- Use the [Amazon VPC User Guide](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)
  and the
  [CloudFormation template reference](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/introduction.html).
  Do NOT copy templates from the Internet at large. Most VPC tutorials older
  than 2024 end with a bastion host and an SSH rule open to the world; that
  is exactly what this module teaches you not to build.

- Use the AWS CLI rather than the console unless a step says otherwise.

- Run the labs in your lab account with the `lab` profile from
  [module 19](../19-multi-account/README.md) (`export AWS_PROFILE=lab`). The
  profile sets the lab region, `us-east-2`, so the commands here don't pass
  `--region` except in the optional inter-region stretch.

- Install the
  [Session Manager plugin for the AWS CLI](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html)
  before Lab 4.1.6.

- Tag every resource you create with:

  - the key "user" and your identifier;
  - "stelligent-u-lesson" and this lesson number;
  - "stelligent-u-lab" and this lab number.

- This is the longest module in the course. If you're stuck on one lab for
  hours, write down where you are and what isn't working, talk to your
  mentor, and move on.

## Lesson 4.1: Creating Your Own VPC

### Principle 4.1

*VPCs provide isolated environments for running all of your AWS
services. Non-default VPCs are a critical component of any safe
architecture, and nothing in them should be reachable from the Internet
unless you put it there on purpose.*

### Practice 4.1

This section walks you through the steps to create a new VPC. On every
engagement, you'll be working in VPCs created by us or the client. Never
use the default VPC for real work. (EC2-Classic, which predated VPCs, is
retired.)

You'll build a VPC with a public and a private subnet, put an instance in
each, and reach both of them without a key pair, without an SSH bastion and
without opening port 22 to the Internet. Along the way you'll see what each
piece costs, because in a VPC the expensive parts are the ones that connect
you to the Internet.

This is a complicated set of labs. If you get stuck, the
[AWS::EC2::VPCPeeringConnection](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-ec2-vpcpeeringconnection.html)
page has an example template that shows how VPC resources are tied together,
and the
[example routing configurations](https://docs.aws.amazon.com/vpc/latest/userguide/route-table-options.html)
show where each route goes.

#### Lab 4.1.1: New VPC with "Private" Subnet

Launch a new VPC in your lab account:

- Use a [CloudFormation YAML template](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/introduction.html).

- Assign it a /16 CIDR block in
  [private (RFC 1918) address space](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-cidr-blocks.html),
  and provide that block as a stack parameter in a separate parameters file
  (`aws cloudformation create-stack --parameters file://params.json`). Avoid
  `172.31.0.0/16`, which the default VPC uses.

- Create an EC2 subnet resource within your CIDR block that has a /24
  netmask. Pick its Availability Zone with `!Select` and `!GetAZs` rather
  than typing a zone name.

- Provide the VPC ID and subnet ID as stack outputs.

- Tag all your new resources as described in the [Guidance](#guidance).

- Don't use dedicated tenancy (it's needlessly expensive).

#### Lab 4.1.2: Internet Gateway

Update your template to allow traffic
[to and from instances](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html)
on your "private" subnet.

- Add an
  [Internet gateway resource](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-ec2-internetgateway.html).

- Attach the gateway to your VPC.

- Create a route table for the VPC, add a default route to the gateway, and
  associate the route table with your subnet.

We can't call your subnet "private" any more. Now that its default route
points at an Internet gateway, it's a *public* subnet: anything in it with a
public IP address can talk to the Internet, and the Internet can talk back.

#### Lab 4.1.3: Instance Role for Session Manager

The 2022 version of this lab had you create an SSH key pair. You don't need
one. Instead, you'll connect with
[Session Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html),
part of AWS Systems Manager: the SSM Agent on the instance makes an
*outbound* HTTPS connection to Systems Manager, and your shell session rides
on that connection. No inbound port is opened, IAM decides who may connect,
and every session can be logged.

Create a new CloudFormation template for your instances. Start it with:

- An IAM role that EC2 can assume, with the AWS managed policy
  `AmazonSSMManagedInstanceCore` attached.

- An instance profile that contains the role.

Read
[Session Manager prerequisites](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-prerequisites.html)
and note which endpoints the agent must reach on port 443. You'll need that
list in several of the labs that follow.

#### Lab 4.1.4: Test Instance

Launch an EC2 instance into your VPC from the template you started in Lab
4.1.3.

- For the subnet and VPC, reference the outputs of your VPC stack (use
  stack exports and `!ImportValue`, or pass them as parameters).

- Look up the latest Amazon Linux 2023 AMI with a parameter of type
  `AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>` whose default is
  `/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64`.
  Use the standard AMI, not the minimal one: the standard AMI already has the
  SSM Agent and EC2 Instance Connect installed.

- Use a t3.micro instance type (or t4g.micro with the `-arm64` parameter),
  set as a parameter in a new parameters file.

- Require IMDSv2 (`MetadataOptions` with `HttpTokens: required`).

- Attach the instance profile. Don't specify a key pair.

- Provide the instance ID and private IP address as stack outputs.

- Use the same tags you put on your VPC.

##### Question: Post Launch

_After you launch your new stack, can you start a Session Manager session to
the instance (`aws ssm start-session --target <instance-id>`)? Does the
instance appear in `aws ssm describe-instance-information`? Why or why not?_

##### Question: Verify Connectivity

_Is there a way that you can verify Internet connectivity from the instance
without logging in to it? (Think about what the SSM Agent does when it
starts, and what the EC2 console output shows. You'll meet a third way in
Lab 4.1.10.)_

#### Lab 4.1.5: Security Group

Add a
[security group](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html)
to your EC2 stack:

- Allow ICMP echo request (ping) in from **your own public IP address only**
  (a /32, passed as a parameter). Don't allow SSH from anywhere.

- Replace the default "allow all" egress rule with HTTPS (TCP 443) out to
  anywhere, which is what the SSM Agent needs, plus HTTP (TCP 80) so you can
  test with `curl` and install packages.

##### Question: Connectivity

_Can you start a Session Manager session to your instance yet? What is still
missing?_

#### Lab 4.1.6: Public IPv4 Address

Add an Elastic IP to your EC2 stack:

- Associate it with your EC2 instance.

- Provide the public IP as a stack output.

Your instance was already in a subnet with a route to an Internet gateway,
and now it has a public IP address that's reachable from anywhere outside
your VPC. The 2022 course made this instance an SSH bastion at this point.
You won't: your security group still has no inbound SSH rule, and it never
will.

##### Question: Ping

_Can you ping your instance now? From your laptop? From CloudShell?_

##### Question: Session Manager

_Can you start a Session Manager session now? What changed, given that you
didn't open any inbound port? Which user are you logged in as?_

##### Question: Traffic

_From the session, can you send any traffic (e.g. `curl`) out to the
Internet? Can you reach an HTTPS site and a plain HTTP site?_

##### Question: What the Address Costs

_Since February 2024, AWS charges for every public IPv4 address. Using the
[VPC pricing page](https://aws.amazon.com/vpc/pricing/), what does your
Elastic IP cost per month? Does the charge stop if you stop the instance?
If you disassociate the address? Find all the public IPv4 addresses in your
account with `aws ec2 describe-addresses` and
`aws ec2 describe-network-interfaces`, and name one way to avoid the charge
for an instance that only needs outbound access._

#### Lab 4.1.7: NAT Gateway

Update your VPC template/stack by adding a
[NAT gateway](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-nat-gateway.html).

- Put the NAT gateway in the public subnet you created earlier (a zonal NAT
  gateway, the kind the exams still assume).

- Provision a new Elastic IP for the NAT gateway.

We need a private instance to explore some of the concepts below. Add a new
subnet to the VPC stack and a new EC2 instance to the instance stack:

- The new subnet must have a unique netblock inside your VPC CIDR.

- It gets its own route table, whose default route is the NAT gateway.

- Aside from the subnet, configure this instance just like the first one,
  with the same instance profile.

- This instance will not have an Elastic IP or any other public address.

##### Question: Access

_Can you start a Session Manager session to this instance? Trace the path the
SSM Agent's connection takes to reach Systems Manager._

##### Question: Egress

_Can the private instance send traffic out? What source IP address does a
site on the Internet see? (Try `curl https://checkip.amazonaws.com` from both
instances.)_

##### Question: Deleting the Gateway

_If you delete the NAT gateway, what happens to an open Session Manager
session on your private instance? What does
`aws ssm describe-instance-information` report a few minutes later?_

##### Question: Recreating the Gateway

_Recreate the NAT gateway, then disassociate the Elastic IP from the public
EC2 instance. Can you still reach that instance with Session Manager? What
does that tell you about which subnet it should have been in?_

Check the answer in the AWS console as well as the CLI, then reassociate the
Elastic IP.

##### Question: One per Availability Zone

_Your NAT gateway lives in one Availability Zone. What happens to private
instances in other zones if that zone fails, and what does the usual fix
(one NAT gateway per zone) cost for three zones? Read about
[regional NAT gateways](https://docs.aws.amazon.com/vpc/latest/userguide/nat-gateways-regional.html):
what do they change about subnets, routes and high availability, and how are
they billed? When is a NAT gateway the wrong tool entirely (think S3 traffic
and IPv6)?_

#### Lab 4.1.8: EC2 Instance Connect Endpoint

Session Manager needs a path from the instance to Systems Manager. An
[EC2 Instance Connect Endpoint](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/connect-with-ec2-instance-connect-endpoint.html)
works the other way round: it's a network interface in your subnet that
opens a tunnel *in* to an instance's private IP, authorized by IAM. It needs
no Internet access, no public IP and no bastion, and the endpoint itself has
no charge.

Add to your VPC stack:

- A security group for the endpoint that allows outbound TCP 22 to your VPC
  CIDR (or to the private instance's security group).

- An
  [`AWS::EC2::InstanceConnectEndpoint`](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-ec2-instanceconnectendpoint.html)
  in the private subnet, using that security group. Output its ID.

Then add a rule to the private instance's security group that allows TCP 22
**from the endpoint's security group only**. Read
[Security groups for EC2 Instance Connect Endpoint](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/eice-security-groups.html)
to check your rules.

Connect with the AWS CLI. The CLI pushes a one-time public key to the
instance through EC2 Instance Connect, so you still don't need a key pair:

```shell
aws ec2-instance-connect ssh --instance-id <private-instance-id> \
  --os-user ec2-user --connection-type eice
```

Note the
[quotas](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/eice-quotas.html):
one endpoint per VPC, five per region.

##### Question: Without the NAT Gateway

_Delete the NAT gateway again. Which of your two ways into the private
instance still works, and why? Recreate the NAT gateway when you're done._

##### Question: Two Ways In

_Compare Session Manager and EC2 Instance Connect Endpoint: what each one
needs on the instance, in the network and in IAM; which one works for a
Windows instance over RDP; and where you'd look to find out who connected
and what they did. When would you still need port 22 open, and to what
source?_

#### Lab 4.1.9: Network ACL

Add
[network ACLs](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-network-acls.html)
to your VPC stack. Remember that network ACLs are stateless: a rule that lets
a request in does nothing for its reply.

First, add one on the public subnet:

- Inbound: ICMP from your IP address only.

- Outbound: all traffic to anything.

##### Question: EC2 Connection

_Can you still ping your public instance? Can you still start a Session
Manager session to it? Can the private instance still reach the Internet
through the NAT gateway? Explain each answer in terms of which direction the
connection was opened._

Fix the public subnet's ACL so that Session Manager and the NAT gateway work
again, keeping the inbound rules as narrow as you can.

Add another ACL to your private subnet:

- Inbound from your VPC CIDR only: SSH (from the Instance Connect Endpoint),
  ping and HTTP.

- Outbound: all ports, to anything (the NAT gateway forwards the traffic).

- Whatever inbound rule the replies to the private instance's own outbound
  connections need.

_Verify again that you can reach both instances, both ways in._

##### Question: Return Traffic

_Which source address and port range do the replies to your private
instance's `curl` requests arrive from, after the NAT gateway has translated
them? Why doesn't a security group need a rule for them?_

#### Lab 4.1.10: Reachability Analyzer

[Reachability Analyzer](https://docs.aws.amazon.com/vpc/latest/reachability/what-is-reachability-analyzer.html)
reads your configuration (routes, security groups, network ACLs, gateways)
and tells you whether a path is open and, if not, which component blocks it.
It doesn't send any packets. Each analysis costs $0.10, so plan them.

Using the
[CLI](https://docs.aws.amazon.com/vpc/latest/reachability/getting-started-cli.html)
(`aws ec2 create-network-insights-path` and
`aws ec2 start-network-insights-analysis`), analyze these three paths:

1. From the Internet gateway to the public instance, TCP port 22.
1. From the public instance to the private instance, TCP port 22.
1. From the private instance to the Internet gateway, TCP port 443.

Could you have analyzed the ping path the same way? Check which protocols a
path accepts.

Read the results with `aws ec2 describe-network-insights-analyses`.

##### Question: Blocking Component

_For each path, is it reachable? If not, which component blocks it, and does
that match what you expected? For the reachable path, list the hops it
reports. Which of this lab's earlier questions could you have answered with
Reachability Analyzer instead of trial and error?_

### Retrospective 4.1

For more information, read the
[Amazon VPC User Guide](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html),
in particular
[security best practices for your VPC](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-best-practices.html).

#### Question: Bastions

_A client asks you to add an SSH bastion host "like we always do". What would
you propose instead, and what are the arguments you'd make about security,
auditing and cost? Is there a case where a bastion is still the right
answer?_

#### Question: Pausing the Lab

_You're stopping for the day and will pick up Lesson 4.2 tomorrow. Which
resources in your two stacks cost money while you're away, and what's the
smallest change that stops most of that cost? (A stack parameter that
creates the NAT gateway only when set is one answer.)_

## Lesson 4.2: Integration with VPCs

### Principle 4.2

*VPCs are most useful when connected to external resources: other VPCs,
other AWS services, and corporate networks. Connect them privately, and
plan their address space so they can be connected.*

### Practice 4.2

VPCs provide important isolation for your resources. Often, though, they
need to be connected to other services to poke holes through those walls
of isolation. In this lesson you'll connect two VPCs directly, reach S3
without going through the Internet, and use IPAM to see and plan the
addresses you're using.

#### Lab 4.2.1: VPC Peering

Copy the VPC template you created earlier and modify it to launch a
private-only VPC in the lab region.

- Give this VPC a
  [CIDR block](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-cidr-blocks.html)
  that doesn't overlap with the original one.

- Don't attach an Internet gateway or NAT gateway to the new VPC.

- Update both VPC stacks to accept the netblock of the peer VPC as
  a parameter, so that you can...

- add network ACLs in each VPC that allow all traffic in from the
  other VPC, and allow all traffic out to it.

Create a separate stack that creates a
[peering](https://docs.aws.amazon.com/vpc/latest/peering/what-is-vpc-peering.html)
connection between the two VPCs.

- Create a
  [VPC peering connection](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-ec2-vpcpeeringconnection.html)
  from one to the other.

- Add a route in each VPC that sends traffic for the other VPC's CIDR
  to the peering connection.

- The VPC IDs and route table IDs should be passed as stack parameters.

Stretch: peering also works between regions. Deploy the private VPC in a
second region instead (this is the one place in this module where you pass
`--region`), and note what changes: who accepts the connection, where the
routes live, and which security group features stop working.

#### Lab 4.2.2: EC2 across VPCs

Create a new EC2 stack similar to your private instance, but in your new
private-only VPC.

- Allow ping in from the other VPC's CIDR in its security group.

- Add an EC2 Instance Connect Endpoint to the private-only VPC so you can log
  in to this instance.

Pings need to be allowed by the security groups at both ends, in both
directions, and by the network ACLs. Your first VPC's security groups only
allow HTTPS and HTTP out, so expect to adjust them.

##### Question: Public to Private

_Can you ping this instance from the public instance you created earlier?_

##### Question: Private to Public

_Can you ping your public instance from this private instance? Which IPs are
reachable, the public instance's private IP or its public IP, or both?_

Use `traceroute` (`sudo dnf install -y traceroute` on the instance in the
first VPC, which has a way out) to see where traffic flows to both the
public and private IPs.

##### Question: No Way Out

_The private-only VPC has no Internet gateway and no NAT gateway. Could you
use Session Manager on this instance? What would you have to add (see
[Session Manager with AWS PrivateLink](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-getting-started-privatelink.html)),
and what would it cost per month in one Availability Zone? Could the
instance use the first VPC's NAT gateway through the peering connection?_

#### Lab 4.2.3: VPC Gateway Endpoint to S3

VPC endpoints are something you'll see in practically every client
engagement. Instances in private subnets use them to reach AWS services
without a NAT gateway, which is both more private and cheaper: an S3
[gateway endpoint](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-s3.html)
has no hourly or data processing charge.

Create a small S3 bucket for this lab (a stack of its own is simplest) and
put a test file in it. Then create a
[VPC endpoint](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-ec2-vpcendpoint.html)
from your private-only VPC to S3:

- Add the gateway endpoint to your private-only VPC's template and associate
  it with the subnet's route table. Pass the bucket name as a parameter so it
  can be used in the endpoint policy.

- In the
  [endpoint policy](https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-access.html),
  grant access to your bucket only.

- In the bucket policy, deny access that doesn't come through your endpoint
  (the `aws:SourceVpce` condition key; see the
  [bucket policy examples](https://docs.aws.amazon.com/AmazonS3/latest/userguide/example-bucket-policies-vpc-endpoint.html)).
  Be careful: a blanket `Deny` also blocks you from your laptop and from
  CloudFormation. Exempt your own role.

- Give the private-only instance's role permission to read the bucket.

- Turn on DNS support and DNS hostnames for the VPC
  (`EnableDnsSupport` and `EnableDnsHostnames`) if you haven't already. The
  instance still resolves S3's public name; the endpoint's route sends the
  traffic privately.

- Adjust the network ACLs on the endpoint's subnet so that HTTPS to S3 and
  its replies are allowed.

After you update the stacks, make sure you can list and read the bucket from
the instance in your private-only VPC. The instance has no AWS CLI profile;
if the CLI there asks for a region, set `AWS_REGION` for that shell.

##### Question: Endpoint Policy vs Bucket Policy

_What does each of the two policies protect against? Which one stops your
instance from copying data to a bucket in someone else's account?_

##### Question: Prefix Lists

_Look at the route the endpoint added to your route table. What is its
destination? Can you use the same thing in a security group rule? In a
network ACL rule?_

#### Lab 4.2.4: IP Address Management with IPAM

[Amazon VPC IP Address Manager](https://docs.aws.amazon.com/vpc/latest/ipam/what-it-is-ipam.html)
(IPAM) tracks and plans IP addresses across VPCs, regions and accounts. Its
[Free Tier](https://aws.amazon.com/vpc/pricing/) covers one region and one
account and includes *Public IP insights*, which answers "which public IPv4
addresses am I paying for?"

- Create an IPAM in the Free Tier, with the lab region as its operating
  region (an
  [`AWS::EC2::IPAM`](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-ec2-ipam.html)
  resource or `aws ec2 create-ipam`).

- Use
  [Public IP insights](https://docs.aws.amazon.com/vpc/latest/ipam/view-public-ip-insights.html)
  (in the IPAM console, or `aws ec2 get-ipam-discovered-public-addresses`,
  which needs your IPAM's default resource discovery ID) to list the public
  IPv4 addresses in your account. Account for each one: which resource holds
  it, and is it an Elastic IP, an EC2 public IP or a service-managed address?

Stretch (Advanced Tier; managing private IPv4 space isn't in the Free Tier):

- Change the IPAM to the Advanced Tier, create a private IPv4 pool with a
  large block (for example a /12), and set the pool's default netmask to /16.

- Create a third VPC whose CIDR is allocated from the pool
  (`Ipv4IpamPoolId` and `Ipv4NetmaskLength` on `AWS::EC2::VPC` instead of
  `CidrBlock`).

- Look at the pool's allocations and at the compliance and overlap status
  IPAM reports for your three VPCs.

##### Question: Overlapping CIDRs

_Why did Lab 4.2.1 insist on non-overlapping CIDRs? What happens if you try
to peer two VPCs whose CIDRs overlap? In a company with 200 VPCs, how does an
IPAM pool prevent that problem before it starts?_

#### Lab 4.2.5: Clean Up

Remove everything this module created, in dependency order:

- Delete the instance stacks first, then the peering stack, then the VPC
  stacks. If a VPC stack fails to delete, the stack events name the resource
  that's still in use.

- Empty and delete the S3 bucket from Lab 4.2.3. Remove any bucket policy
  `Deny` that would stop you from doing so.

- Delete the IPAM from Lab 4.2.4 (and the third VPC, if you did the stretch).

- Delete any saved Reachability Analyzer paths and analyses.

- Confirm nothing billable is left in the lab region:

  ```shell
  aws ec2 describe-addresses --query 'Addresses[].PublicIp'
  aws ec2 describe-nat-gateways --filter Name=state,Values=available \
    --query 'NatGateways[].NatGatewayId'
  aws ec2 describe-instances --filters Name=instance-state-name,Values=running,stopped \
    --query 'Reservations[].Instances[].InstanceId'
  ```

  Each command should return an empty list.

### Retrospective 4.2

#### Question: Corporate Networks

_How would you integrate your VPC with a corporate network? Compare
[AWS Site-to-Site VPN](https://docs.aws.amazon.com/vpn/latest/s2svpn/VPC_VPN.html)
and [AWS Direct Connect](https://docs.aws.amazon.com/directconnect/latest/UserGuide/Welcome.html)
on cost, setup time, bandwidth and encryption._

#### Question: Many VPCs

_Peering isn't transitive. If ten VPCs all need to talk to each other and to
the corporate network, how many peering connections is that, and what does
[AWS Transit Gateway](https://docs.aws.amazon.com/vpc/latest/tgw/what-is-transit-gateway.html)
change?_

#### Question: Guardrails

_Your organization wants to be sure that no VPC in a workload account can
ever be reached from the Internet, whatever its route tables say. Read about
[VPC Block Public Access](https://docs.aws.amazon.com/vpc/latest/userguide/security-vpc-bpa.html).
Which mode would you use, how do exclusions work, and would your NAT gateway
from Lesson 4.1 still work? How does this compare with the SCPs you'll meet
in module 19?_

## Further Reading

- [VPC endpoints and AWS PrivateLink](https://docs.aws.amazon.com/vpc/latest/privatelink/what-is-privatelink.html)
  connect a VPC privately to many more AWS services, and to services in other
  accounts, keeping that traffic off the open Internet.

- [Amazon VPC-to-Amazon VPC connectivity options](https://docs.aws.amazon.com/whitepapers/latest/aws-vpc-connectivity-options/amazon-vpc-to-amazon-vpc-connectivity-options.html)
  describes many more options and design patterns for connecting VPCs.

- [Amazon VPC Lattice](https://docs.aws.amazon.com/vpc-lattice/latest/ug/what-is-vpc-lattice.html)
  connects services across VPCs and accounts at the application layer,
  without managing peering or routes.

- [Network Access Analyzer](https://docs.aws.amazon.com/vpc/latest/network-access-analyzer/what-is-network-access-analyzer.html)
  is the fleet-wide counterpart to Reachability Analyzer: it finds every
  unintended path that matches a rule, such as "anything reachable from an
  Internet gateway".

- [VPC Flow Logs](https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html)
  record the traffic that actually crossed your network interfaces. Module 08
  uses them.

- [IPv6 in a VPC](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-migrate-ipv6.html)
  with an egress-only Internet gateway avoids both the public IPv4 charge and
  the NAT gateway for outbound traffic.

- [New – AWS Public IPv4 Address Charge + Public IP Insights](https://aws.amazon.com/blogs/aws/new-aws-public-ipv4-address-charge-public-ip-insights/)
  is the announcement behind this edition's cost questions.
