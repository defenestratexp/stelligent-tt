# Stelligent-U, 2026 Edition — Update Plan

**Status:** approved 2026-09-18; all 29 modules written 2026-09-18 on the `edition-2026` branch (one commit per module). Next: work through the labs in a real lab account and resolve the `<!-- VERIFY -->` markers.
**Why:** the course was last updated upstream in October 2022. Retaking the AWS certifications
in 2026 means working from material that still runs in a new AWS account and that covers what
the current exam guides test. Each completed module also becomes a blog post.

## Principles

1. **Keep the course's shape.** Every lesson stays Principle → Practice → Lab → Question →
   Retrospective → Further Reading, CloudFormation in YAML, CLI over console, one branch per
   lesson with a PR to your lab repository's default branch (`main` for new GitHub repositories).
2. **Keep module numbers 00–18 stable.** Updated modules keep their numbers; new modules start
   at 19, so existing links and notes don't break.
3. **It must run in a new account.** No Cloud9, no launch configurations, no retired runtimes
   or operating systems. AMIs are looked up from SSM public parameters rather than hard-coded.
4. **Cost is part of every lab.** A budget alert is set up in module 00; every module states
   what it costs to leave running and ends with a cleanup step.
5. **One home region, parameterized.** No more mix of us-east-1, us-east-2 and us-west-2.

## Target exams and order

| # | Exam | Code | Notes |
|---|---|---|---|
| 1 | Cloud Practitioner | CLF-C02 | Cheapest, fastest; the pass unlocks a 50% voucher |
| 2 | AI Practitioner | AIF-C01 | GenAI now appears across CloudOps, Security and the upcoming C03s |
| 3 | Solutions Architect – Associate | SAA-C03 | Stable, no update announced |
| 4 | CloudOps Engineer – Associate (formerly SysOps) | SOA-C03 | Closest to day-to-day work |
| 5 | Developer – Associate | DVA-C03 | C02 ends ~2026-11-30; C03 guide publishes 2026-10-27 |
| 6 | DevOps Engineer – Professional | DOP-C02 | Later renews DVA and CloudOps |
| 7 | Solutions Architect – Professional | SAP-C03 | C02 ends ~2026-11-16; later renews SAA |
| 8 | Security – Specialty | SCS-C03 | |

Lapsed certifications have to be passed again as a new candidate; the renewal cascades only
help once they are active again.

## Existing modules

| # | Module | Change | Main work | Exams | Est. h |
|---|---|---|---|---|---|
| 00 | Dev environment | **Heavy** | Replace Cloud9 with local/CloudShell; IAM Identity Center + `aws configure sso`; budget alert; cleanup tooling; fix `n9n-autologin.sh` bugs | all | 4 |
| 01 | CloudFormation | Light | Add cfn-lint, change sets, drift detection, IaC generator; fix the "another US region" lab | SOA, DOP | 8 |
| 02 | S3 | **Heavy** | Rewrite Lesson 2.2 around Block Public Access + Object Ownership; default SSE-S3, bucket keys | SAA, SOA, SCS | 9 |
| 03 | IAM | Light | Identity Center principals; Access Analyzer; permission boundaries | all | 7 |
| 04 | VPCs | Light | Session Manager / EC2 Instance Connect Endpoint instead of a bastion; public-IPv4 and NAT costs; IPAM, Reachability Analyzer | SAA, SOA | 13 |
| 05 | EC2 | **Heavy** | IMDSv2; AL2023 via SSM parameters; gp3, Graviton; drop Cloud9 lab and EOL OSes | SAA, SOA | 12 |
| 06 | Auto Scaling | **Heavy** | Launch templates, Instance Refresh, warm pools, mixed instances | SAA, SOA | 9 |
| 07 | Load balancing | Light | Rewrite `asg_example.yaml` (launch template, AL2023, correct cfn-signal); TLS 1.3 policy | SAA, SOA | 7 |
| 08 | CloudWatch Logs → **Observability** | **Heavy** | `aws logs tail`, Logs Insights, metric filters + alarms, CloudWatch agent, EventBridge; fix `8.1.2.yml` | SOA, DOP | 10 |
| 09 | Lambda | Light | EventBridge instead of CloudTrail rules; function URLs; current runtimes; Powertools | DVA | 8 |
| 10 | KMS | Light | "KMS keys" terminology; envelope encryption, grants, rotation; solo-learner lab | SAA, SCS | 5 |
| 11 | Parameter Store | Light | Console links; Secrets Manager; add AppConfig | DVA, SOA | 5 |
| 12 | CodePipeline | Light | CodeConnections source instead of a GitHub PAT; V2 pipelines; `main` | DVA, DOP | 11 |
| 13 | ECS | **Heavy** | ECR auth, capacity providers, AL2023, correct Fargate facts, one NAT gateway | DVA, DOP | 12 |
| 14 | Jenkins | **Replace infra** | New `base.yaml`; Jenkins LTS on Java 21 with JCasC; ephemeral EC2 agents; instance-role credentials | DOP | 16 |
| 15 | Kubernetes / EKS | **Heavy** | Fix kubectl commands; access entries, Pod Identity, Auto Mode; rebuild the sample app | DOP, SAP | 14 |
| 16 | SAM | **Heavy** | Current runtimes, SDK v3, `sam deploy --guided`; keep the safe-deployment lesson | DVA, DOP | 13 |
| 17 | Terraform | **Heavy** | `required_providers`; S3 native state locking (no DynamoDB); OpenTofu note; `import`/`moved` blocks | SOA, DOP | 12 |
| 18 | Step Functions | Light + expand | Workflow Studio; JSONata; Retry/Catch lab; SDK integrations; EventBridge trigger | DVA, SAA | 6 |

## New modules

Ordered by how much exam weight they carry for the certifications above.

| # | Module | Covers | Exams | Est. h |
|---|---|---|---|---|
| 19 | Multi-account foundation | Organizations, SCPs/RCPs, Control Tower, RAM | SAA, SOA, DOP, SAP, SCS | 8 |
| 20 | Systems Manager | Session Manager, Patch Manager, Automation, State Manager, EC2 Image Builder | SOA, DOP | 10 |
| 21 | DNS and edge | Route 53 routing policies + health checks; CloudFront with OAC; WAF | SAA, SOA | 8 |
| 22 | Databases | RDS / Aurora (Multi-AZ, read replicas, backups, RDS Proxy); DynamoDB depth | SAA, DVA, SOA | 10 |
| 23 | Storage and backup | EFS, AWS Backup, DR patterns and RTO/RPO | SAA, SOA | 6 |
| 24 | Messaging and events | SQS (DLQ, FIFO), SNS, EventBridge (rules, Pipes, Scheduler) | DVA, SAA | 8 |
| 25 | AWS CDK | CDK in Python; compare with modules 01 and 17 | DVA, SOA, DOP | 10 |
| 26 | Governance and detection | AWS Config + conformance packs, GuardDuty, Security Hub, Inspector | SOA, DOP, SCS | 8 |
| 27 | Resilience engineering | Deployment strategies, FIS, Resilience Hub, Application Recovery Controller | DOP, SAP | 8 |
| 28 | Generative AI on AWS | Bedrock, Guardrails, agents / AgentCore; Kiro / Q Developer; securing GenAI | AIF, SOA, SCS, DVA-C03, SAP-C03 | 10 |

## Phases (aligned to the exam order)

| Phase | Modules | Supports | Rough hours |
|---|---|---|---|
| 1. Foundations | 00, 01, 02, 03, 19 | CLF, then everything | ~36 |
| 2. Core infrastructure | 04, 05, 06, 07, 21, 22, 23 | SAA | ~65 |
| 3. Operations | 08, 10, 11, 20, 26 | CloudOps | ~38 |
| 4. Serverless and apps | 09, 16, 18, 24, 25 | DVA | ~42 |
| 5. Delivery and containers | 12, 13, 14, 15, 17, 27 | DOP | ~73 |
| 6. AI | 28 | AIF (study alongside Phase 1) | ~10 |

About 265 hours in total, excluding blog writing. AIF can be taken early from reading plus
module 28.

## Blog series

Each module produces a post: what changed since the 2022 version, the lab, the gotchas, and
which exam objective it covers. The long version goes on the LLC site; LinkedIn gets a short
summary that links back. Strongest early topics:

1. Why `aws s3 sync --acl public-read` fails now (module 02)
2. From MFA session scripts to IAM Identity Center (module 00)
3. Launch configurations are gone: ASG updates with launch templates (06/07)
4. Terraform state on S3 without DynamoDB (17)
5. Protecting stateful resources in CodePipeline with change sets and approval (12)
6. Safe Lambda deployments with SAM and CodeDeploy hooks (16)
7. Jenkins on AWS in 2026 (14)

## Also fix

- ~~CI lint workflow (`actions/setup-ruby@v1`, Ruby 2.7 are dead).~~ Done: current actions, plus a cfn-lint job.
- ~~Links pointing at `github.com/stelligent/stelligent-u` instead of the fork.~~ Done.
- Lab instructions: say `main`, the default for new GitHub repositories, instead of `master` (done per module).
- `n9n-autologin.sh`: its cleanup `sed` can delete other profiles, a failed login wipes
  existing credentials, and it writes temporary credentials to a world-readable file.

## Decisions (2026-09-18)

1. **Lab region: `us-east-2` (Ohio)**, set once in the AWS profile and passed as a parameter,
   never hard-coded. It is in the lowest price tier and keeps lab resources apart from the
   owner's real infrastructure in `us-west-2`. A few services are global or pinned to
   `us-east-1` (CloudFront certificates, billing and budgets); those labs say so.
2. **Separate lab account.** Labs run in a dedicated account created under AWS Organizations
   (module 19, done early in Phase 1). Cleanup tooling such as aws-nuke must never run in
   the account that holds real infrastructure.
3. **Exam versions: target the new ones** (DVA-C03, SAP-C03). Recertification is presented to
   employers as in progress, targeting Q1 2027.
4. **CDK language: Python.**
5. **Blog:** full posts on the LLC site; LinkedIn posts link to them.
6. **Scope: all ten new modules**, written with the new exam versions in mind.
