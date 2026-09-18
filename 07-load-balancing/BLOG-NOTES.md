# Blog Notes: Module 07, Load Balancing

## Working title

Your cfn-signal probably never worked: an ALB, an ASG and TLS 1.3 in 2026

## Hook

The classic "ALB in front of an Auto Scaling group" tutorial template has
three problems today. It uses a launch configuration, which accounts created
after October 2024 can't create. It hard-codes an Amazon Linux AMI that is
end of life. And its `cfn-signal` call targets the launch configuration, a
resource that can't receive signals, so the stack only looks like it waits
for the instances. Add HTTPS the way most tutorials show and you also inherit
`ELBSecurityPolicy-2016-08`, which still allows TLS 1.0, because that's what
CloudFormation and the CLI pick when you don't choose. This post rebuilds the
example the current way and shows what each fix buys you.

## Key points

1. **Who gets the signal.** `CreationPolicy` lives on the Auto Scaling group,
   so `cfn-signal --resource` must name the group. `cfn-init --resource`
   names whatever resource holds the `AWS::CloudFormation::Init` metadata
   (here, the launch template). Add `AutoScalingRollingUpdate` with
   `WaitOnResourceSignals` so updates wait too.
1. **Launch template, AL2023, IMDSv2.** Resolve the AMI from
   `/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64`,
   require IMDSv2 in `MetadataOptions`, install `aws-cfn-bootstrap` with
   `dnf`, and use the `systemd` key (not `sysvinit`) under `services`.
1. **Security group chaining.** Instances accept port 80 only from the ALB's
   security group; no SSH anywhere, Session Manager instead.
1. **Health checks have two owners.** The target group decides whether the
   ALB sends a target traffic; `HealthCheckType: ELB` lets the ASG replace
   the instance. The grace period has to cover bootstrap time. When every
   target is unhealthy, the ALB fails open and sends traffic to all of them.
1. **Pick the TLS policy explicitly.** Console default:
   `ELBSecurityPolicy-TLS13-1-2-Res-PQ-2025-09` (AWS's recommendation, with
   hybrid post-quantum ML-KEM key exchange). CloudFormation/CLI/CDK default:
   `ELBSecurityPolicy-2016-08`. Use `-TLS13-1-3-` policies only once
   connection logs show no TLS 1.2 clients.
1. **Certificates without a domain.** A self-signed certificate imported
   into ACM works for a lab; ACM public certificates need a domain and DNS
   validation but are free and renew themselves.

## Gotchas readers will hit

- With `#!/bin/bash -xe`, a failing `cfn-init` exits the script before
  `cfn-signal` runs, so the stack waits for the timeout instead of failing
  fast. Drop `-e` (or trap errors) around the helper calls.
- `cfn-signal` fires when `cfn-init` finishes, not when the ALB marks the
  target healthy, so a rolling update can "succeed" with broken targets.
  AWS's sample templates add a health-verification step before signalling.
- Leaving `HealthCheckGracePeriod` at the CLI/API default of 0 with ELB
  health checks gets new instances killed while they're still bootstrapping.
- Fail-open confuses people in the broken-health-check lab: the page can
  still load while every target is "unhealthy".
- Self-signed certificate CN is limited to 64 characters and ALB DNS names
  can be longer; put the DNS name in `subjectAltName` instead.
- CloudFormation can't import a certificate into ACM, and ACM won't delete a
  certificate still attached to a listener: import with the CLI first, delete
  the stack before the certificate.
- CLI v2 wants `fileb://` for the certificate and key in
  `aws acm import-certificate`.
- An internet-facing ALB plus public-IP instances is five or more billed
  public IPv4 addresses on top of the ALB's hourly charge.

<!-- VERIFY: while doing the labs, confirm `dnf install -y aws-cfn-bootstrap` on the current AL2023 AMI puts cfn-init and cfn-signal in /opt/aws/bin, and capture the stack event shown when a cfn-init failure is signalled. -->
<!-- VERIFY: confirm the 64-character CN limit bites with a real ALB DNS name and that `aws acm import-certificate` accepts a SAN-only self-signed certificate. -->

## Exam objectives

- SAA-C03 Domain 2: Design Resilient Architectures (2.1, 2.2)
- SAA-C03 Domain 1: Design Secure Architectures (1.3 encryption in transit)
- SOA-C03 Domain 2: Reliability and Business Continuity; Domain 5:
  Networking and Content Delivery
- SCS-C03 Domain 5: Data Protection (encryption in transit)
