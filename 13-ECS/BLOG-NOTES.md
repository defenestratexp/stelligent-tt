# Blog Notes: Module 13, ECS

## Working title

ECS in 2026: what your 2022 container tutorial gets wrong (and what it
costs you)

## Hook

The typical ECS tutorial from a few years ago logs in with
`$(aws ecr get-login)`, builds EC2 capacity from a launch configuration on
Amazon Linux 2, and ships a VPC template with a NAT gateway in every
Availability Zone. In a new AWS account in 2026 the login command doesn't
exist, the launch configuration can't be created, the AMI is past end of
life, and the NAT gateways quietly bill around $66 a month before a single
request. This post rebuilds the same nginx service the current way: ECR
with scanning and lifecycle rules, an Auto Scaling group capacity provider
that starts at zero, then Fargate and Fargate Spot, with ECS Exec instead
of SSH and the circuit breaker catching a bad deploy.

## Key points

1. **ECR login and images.** `get-login-password | docker login
   --password-stdin`, what the authorization token actually is and how long
   it lasts, immutable tags, lifecycle rules tested with the preview, and
   registry-level scan on push (the repository-level setting is
   deprecated). Build from ECR Public to stay clear of Docker Hub pull
   limits.
1. **EC2 capacity the current way.** Launch template + ECS-optimized
   AL2023 AMI from SSM + Auto Scaling group at zero + capacity provider
   with managed scaling, termination protection and draining. The service
   uses a capacity provider strategy, not a launch type. Show a task sitting
   in `PROVISIONING` while ECS scales the group out.
1. **The NAT gateway question.** Three ways for private tasks to pull
   images: NAT gateway (one vs one per AZ), interface endpoints (ecr.api,
   ecr.dkr, logs, plus ssmmessages for Exec) with the free S3 gateway
   endpoint, or public subnets with a public IPv4 per task. Put numbers on
   each for a small service.
1. **Fargate facts people get wrong.** CPU units (256 = 0.25 vCPU), valid
   CPU/memory pairs, per-second billing, ARM is about 20% cheaper, and
   Fargate supports bind mounts, EFS and EBS volumes (not Docker volumes).
   Fargate Spot with a `base` on on-demand.
1. **Operating without SSH.** ECS Exec (task role `ssmmessages`
   permissions, `enableExecuteCommand`, new tasks only, CloudTrail audit),
   the deployment circuit breaker with rollback, and Service Connect for
   service-to-service calls now that App Mesh is retired.
1. **Where it's heading.** ECS Managed Instances, built-in blue/green
   deployments, and Express Mode, and the Copilot CLI's end of support.

## Gotchas readers will hit

- `aws ecr get-login` returns an "invalid choice" error on CLI v2; old
  scripts fail at the first line.
- An image built on an Apple silicon laptop runs locally but fails on x86
  Fargate or t3 capacity with an exec format error. Use
  `--platform linux/amd64`, a multi-arch build, or an ARM64 runtime
  platform.
- `IMMUTABLE` tags reject a second push to `v1`, which surprises anyone
  used to overwriting `latest`.
- A Fargate task in a public subnet without `assignPublicIp: ENABLED`, or in
  a private subnet with no NAT or endpoints, can't pull its image; the
  stopped reason mentions pulling the image or retrieving the registry
  auth, not networking.
- On EC2 capacity, `awsvpc` tasks don't get public IPs, and each task uses
  an ENI, so a t3.small fits only two tasks without ENI trunking.
- A service can't switch between an Auto Scaling group capacity provider and
  a Fargate one; you create a new service.
- ECS Exec only works for tasks started after it's enabled, and needs the
  Session Manager plugin on the workstation.
- Deleting a cluster stack while a service or protected instance still
  exists hangs or fails; delete services first.
- nginx resolves `proxy_pass` host names at startup. The Service Connect
  alias resolves inside the task, but if the frontend starts before the
  backend's alias exists, nginx can fail to start.
  <!-- VERIFY: reproduce the nginx startup ordering behaviour with Service Connect during Lab 13.4.3 and note the exact error. -->
- CloudFormation waits for the service to stabilise; a failing deployment
  with the circuit breaker off leaves the stack in `UPDATE_IN_PROGRESS` for
  a long time.
  <!-- VERIFY: time how long CloudFormation waits on a stuck ECS service update without the circuit breaker (Lab 13.2.7 variant). -->

## Exam objectives

- DVA-C02 → C03 Domain 3: Deployment (3.1 application artifacts, 3.4
  deploy code) and Domain 4 (troubleshooting); C03 adds GenAI / agent topics
- DOP-C02 Domain 1 (1.3 artifacts, 1.4 deployment strategies), Domain 3
  (3.2 scalability), Domain 5 (5.3 troubleshooting), Domain 6 (image
  scanning)
- SAA-C03 Domain 3 (3.2 elastic compute) and Domain 4 (4.2 cost-optimized
  compute, 4.4 cost-optimized network: NAT gateways vs endpoints)
