# Authoring Guide — 2026 Edition

How every module in the 2026 edition is written. Read with [UPDATE-PLAN-2026.md](UPDATE-PLAN-2026.md).

## 1. Keep the course's voice and shape

- Follow [templates/NN-topic-name/README.md](templates/NN-topic-name/README.md): a TOC, then
  **Guidance**, then lessons of **Principle → Practice → Lab NN.x.y (with Questions) →
  Retrospective**, then **Further Reading**.
- Labs tell the student *what* to build and *why*, and point at the official docs. They do not
  hand over finished templates. Starter files are fine where the old module had them.
- Questions are answered inline by the student with `> ` quotes (see [WORKFLOW.md](WORKFLOW.md)).
- CloudFormation is YAML. The CLI is preferred over the console; say so when a step genuinely
  needs the console (e.g. a one-time CodeConnections handshake).
- Keep what already works. Rewrite what is broken or misleading. Don't pad.

## 2. Standard sections added to every module

Directly under the module title and TOC, add these three short sections:

```markdown
## What changed in the 2026 edition

- One bullet per substantive change (e.g. "Launch configurations replaced with launch
  templates: new accounts can't create them since October 2024.")

## Exam coverage

| Exam | Domain / task statement |
|---|---|
| SAA-C03 | Domain 1: Design Secure Architectures |

## Cost and cleanup

- What the labs cost if left running (order of magnitude; note anything with an hourly
  charge: NAT gateways, load balancers, public IPv4 addresses, EKS, KMS keys, Windows).
- The cleanup lab or command that removes everything the module created.
```

The retrospective or final lab of every module ends with an explicit cleanup step.

## 3. Account, region and naming

- Labs run in a **dedicated lab account** (created in module 19; module 00 explains why and
  links forward). Never suggest running cleanup tooling in an account with real workloads.
- **Lab region is `us-east-2`.** It is set once in the student's AWS profile. Templates take
  region-specific values as parameters or use `AWS::Region`; CLI examples rely on the profile
  and do not pass `--region` unless the lab is about regions.
- Services that are global or pinned to `us-east-1` (IAM, Organizations, CloudFront +
  its ACM certificate, Budgets, billing) are called out where they appear.
- Resource names and tags include the student's identifier, as the original course asks.
- Lab repositories use `main` as the default branch.

## 4. Current platform facts (as of September 2026)

Use these; do not reintroduce the old behaviour.

- **Identity:** IAM Identity Center with `aws configure sso` is the default way to get CLI
  credentials. Long-lived IAM user keys are shown only as the thing to avoid.
- **Cloud9** is closed to new customers. Use a local terminal, a dev container, or CloudShell.
- **Auto Scaling launch configurations** can't be created in accounts made after 2024-10-01.
  Use launch templates.
- **AMIs:** Amazon Linux 2023 via the SSM public parameter
  `/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64` (or `-arm64`).
  Amazon Linux 1 and 2, Ubuntu ≤ 20.04 and Windows 2012 R2 are end of life. AL2023 uses `dnf`
  and systemd; install `aws-cfn-bootstrap` explicitly when cfn-init is needed.
- **EC2:** IMDSv2 required; gp3 volumes; t3/t4g (not t2).
- **Lambda runtimes:** Python 3.12/3.13, Node.js 22. AWS SDK for JavaScript v3 only.
- **S3:** new buckets have Block Public Access on and ACLs disabled (Object Ownership =
  BucketOwnerEnforced); all objects are encrypted with SSE-S3 by default.
- **Events:** "CloudWatch Events" is EventBridge. S3 can send events to EventBridge directly;
  don't add a CloudTrail trail just to react to S3 uploads.
- **CLI v2:** `aws ecr get-login-password | docker login --password-stdin`; `aws logs tail`.
- **kubectl:** no `--generator`; `--dry-run=client`; EKS access entries instead of `aws-auth`.
- **Terraform:** `required_providers` in a `terraform {}` block; S3 backend with
  `use_lockfile = true` (no DynamoDB lock table); mention OpenTofu as the open-source fork.
- **CodePipeline:** V2 pipeline type; GitHub source via an AWS CodeConnections connection,
  never a personal access token.
- **Renamed services:** Amazon Data Firehose, Infrastructure Composer, Amazon Q Developer in
  chat applications, SageMaker AI, Fault Injection Service.
- **Retired — do not use:** Cloud9, CodeStar, OpsWorks, CodeCatalyst (maintenance), CodeGuru
  Security, App Mesh, Proton, App Runner (closed to new customers), CloudWatch Evidently,
  Elastic Inference, EC2-Classic, QLDB.

When unsure whether something is still current, check the AWS docs and prefer the documented
behaviour. Flag anything you could not verify with `<!-- VERIFY: ... -->`.

## 5. Exam alignment

Target exams: CLF-C02, AIF-C01, SAA-C03, SOA-C03 (CloudOps Engineer – Associate), DVA-C03,
DOP-C02, SAP-C03, SCS-C03. The C03 guides for DVA and SAP publish on 2026-10-27; until then
map to the C02 domains and note "C03 adds GenAI / agent topics". Use the domain names from
the official exam guides.

## 6. Templates, code and validation

- Every CloudFormation template in the repo must pass `cfn-lint` (see `.cfnlintrc`).
  Intentionally incomplete starter templates must still parse; mark the gap with a comment
  such as `# TODO(student): add the files section` rather than leaving invalid YAML.
- No hard-coded AMI IDs, account IDs or ARNs. Use parameters, pseudo-parameters and SSM
  public parameters.
- Security groups open only what the lab needs; SSH/RDP from `0.0.0.0/0` is not acceptable.
  Prefer Session Manager to SSH.
- Terraform snippets must be valid for Terraform ≥ 1.11.
- Sample application code uses currently supported runtimes and dependencies.

## 7. Public repository rules

This repository is public. Never include:

- AWS account IDs, access keys, ARNs from a real account, or email addresses;
- hostnames, IP addresses or details of anyone's private infrastructure;
- anything copied from paid or copyrighted training material.

## 8. Blog notes

Each module gets `BLOG-NOTES.md` in its directory: a working title, the one-paragraph hook
(usually "what changed since the old tutorial"), 4–6 key points, the gotchas a reader will hit,
and which exam objective it supports. These are notes for a post that will be finished after
the student has done the labs; don't write the post itself.
