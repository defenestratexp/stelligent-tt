# Blog Notes: Module 05, EC2

## Working title

Launching an EC2 instance in 2026: no AMI IDs, no open ports, no IMDSv1

## Hook

The EC2 tutorial most of us learned from launched Ubuntu from an AMI ID
copied out of the console, opened port 22 to the world, and read instance
metadata with a bare `curl`. Every one of those steps is now wrong or
fragile: AMI IDs go stale in weeks, Amazon Linux 2023 and current AMIs require
IMDSv2 so the bare `curl` gets a 401, public IPv4 addresses cost money, and
Session Manager gives you a shell with nothing open at all. This post rebuilds
the basic "launch an instance with CloudFormation" exercise the current way,
and ends with a Graviton instance that costs less than the x86 one it
replaced.

## Key points

1. **Look up AMIs, don't paste them.** SSM public parameters
   (`/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-arm64`,
   `/aws/service/ami-windows-latest/...`) plus the
   `AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>` parameter type. AL2023
   AMIs are deprecated 90 days after release, so a pasted ID ages fast.
   Mention the trade-off: the parameter resolves on each stack update.
1. **IMDSv2 by default.** AL2023 AMIs carry `ImdsSupport: v2.0` (IMDSv2 only,
   hop limit 2); set `MetadataOptions` in the launch template anyway so the
   intent is in code, and know the account-level default and enforcement
   switches. Explain the SSRF attack the token defends against.
1. **Session Manager first.** An instance profile with
   `AmazonSSMManagedInstanceCore`, a security group with no inbound rules, and
   `aws ssm start-session`. Compare with SSH and EC2 Instance Connect on open
   ports, secrets to manage, revocation and logging.
1. **Replacement is the lesson in "update".** Changing the AMI, the key pair,
   or anything in a launch template the instance follows replaces the
   instance. Moving to Graviton (arm64 AMI + `t4g`) shows it and saves money
   in the same step; a change set previews it.
1. **Cost traps that didn't exist in the old tutorial:** $0.005/hour per
   public IPv4 address (idle EIPs too), `t3`/`t4g` unlimited credit mode, AMI
   snapshots that survive `deregister-image` unless you pass
   `--delete-associated-snapshots`, and `gp3` instead of `gp2` for a 3,000
   IOPS baseline at any size.

## Gotchas readers will hit

- Plain `curl http://169.254.169.254/latest/meta-data/` returns
  `401 Unauthorized` on AL2023. Old scripts and some agents break silently.
- The Session Manager plugin is a separate install from the AWS CLI;
  `start-session` fails without it.
- AL2023 minimal AMIs don't include the CloudFormation helper scripts;
  install `aws-cfn-bootstrap` with `dnf` before calling `cfn-init`. `cfn-hup`
  needs a systemd unit, not an init.d script.
- A volume attached as `/dev/sdf` shows up as `/dev/nvme1n1` on Nitro
  instances, and user data can run before the attachment finishes.
- Adding a key pair to a running stack replaces the instance (`KeyName`
  requires replacement), so anything on its disk is gone.
- Windows Server 2025 AMIs only run on Nitro instance types and need more
  memory than a `t3.micro` offers.
- The instance in a private subnet without NAT needs several interface
  endpoints for Session Manager and CloudWatch, each billed per hour per AZ.

<!-- VERIFY: capture the exact IMDSv1 error and the AL2023 cfn-hup unit situation while doing Labs 5.2.2 and 5.3.3. -->

## Exam objectives

- SAA-C03 Domain 1 (1.1 secure access), Domain 3 (3.2 high-performing
  compute) and Domain 4 (4.2 cost-optimized compute)
- SOA-C03 Domain 4: Security and Compliance; Domain 3: Deployment,
  Provisioning, and Automation; Domain 1: Monitoring, Logging, Analysis,
  Remediation, and Performance Optimization
- CLF-C02 Domain 3: Cloud Technology and Services
