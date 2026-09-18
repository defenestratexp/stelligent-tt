<img src="images/logo.png" width=25% height=25%>

# Welcome to Stelligent U

Welcome to the technical side of Stelligent University,
[Stelligent's](https://stelligent.com) onboarding program for engineers. This
repo includes a series of learning modules designed to give cloud engineers
practical experience working with AWS and related technologies.

The goal of this material is to prepare all of our engineers for their first
engagements as Stelligent consultants. Any topic or principal presented here
is part of our technical knowledge baseline: this is what we consider a
"Minimum Viable Engineer". There are a _lot_ of other ideas and technologies
that you'll come across and need to know in your work.  We can't fit it all in,
though, and these are the essentials.

For further information, please see:

* [MVE.md](MVE.md): what we mean by "Minimum Viable Engineer"
* [WORKFLOW.md](WORKFLOW.md): how we suggest you use Stelligent U

## Audience

This is a series of lessons originally written for new Engineers at
Stelligent. The goal of this material is to prepare all of our engineers for
their first engagements as Stelligent engineers. Any topic or principal
presented here is part of our technical knowledge baseline: this is what we
consider a _Minimum Viable Engineer_. There are a _lot_ of other ideas and
technologies that you'll come across and need to know in your career.
We can't fit it all in, though, and these are the essentials.

## Materials

The core of Stelligent U is modules 1-12, the series that makes up our baseline
definition of a Minimum Viable Engineer. Other modules are also available that
provide hands-on experience with tech beyond the baseline. We want to add more
and more to those "continuous learning" modules as time goes by.

You'll find a handful of ways we present each topic. Most of the technical
exercises are labs, where we want you to gain a surface level of exposure to
a variety of AWS services and their most common or compelling features.

Labs within a lesson build on each other. Many lessons require the experience
of previous lessons. Unless you're completely blocked, work through them in
order.

When we provide materials for a lab -- e.g. CloudFormation templates or
policy files -- start with those and add to them as requested.

Some topics also include retrospectives. These aren't always focused so much
on a technical exercise. Our goal here is usually to get you to think more
broadly about the technology at hand.

We also provide further reading for each topic. Find time to explore some of
these materials more deeply. Pursue your curiosity. There are many excellent
resources out there, and we particularly want you to learn more where the topics
match up with your interests.

## 2026 edition

This fork updates the course for AWS as it is in 2026 and for the current AWS
certification exams. Every module states what changed, which exam objectives it
covers, and what its labs cost, and ends with a cleanup step. Labs run in a
dedicated lab account in `us-east-2`. See [UPDATE-PLAN-2026.md](UPDATE-PLAN-2026.md)
for the plan and [AUTHORING-2026.md](AUTHORING-2026.md) for the conventions.

| # | Module | # | Module |
|---|---|---|---|
| 00 | [Dev environment](00-dev-environment/README.md) | 15 | [Kubernetes / EKS](15-Kubernetes/README.md) |
| 01 | [CloudFormation](01-cloudformation/README.md) | 16 | [SAM](16-SAM/README.md) |
| 02 | [S3](02-s3/README.md) | 17 | [Terraform](17-Terraform/README.md) |
| 03 | [IAM](03-iam/README.md) | 18 | [Step Functions](18-step-functions/README.md) |
| 04 | [VPCs](04-vpcs/README.md) | 19 | [Multi-account foundation](19-multi-account/README.md) |
| 05 | [EC2](05-ec2/README.md) | 20 | [Systems Manager](20-systems-manager/README.md) |
| 06 | [Auto Scaling](06-auto-scaling/README.md) | 21 | [DNS and edge](21-dns-and-edge/README.md) |
| 07 | [Load balancing](07-load-balancing/README.md) | 22 | [Databases](22-databases/README.md) |
| 08 | [Observability](08-cloudwatch-logs/README.md) | 23 | [Storage and backup](23-storage-and-backup/README.md) |
| 09 | [Lambda](09-lambda/README.md) | 24 | [Messaging and events](24-messaging-and-events/README.md) |
| 10 | [KMS](10-kms/README.md) | 25 | [AWS CDK](25-aws-cdk/README.md) |
| 11 | [Parameter Store, Secrets Manager, AppConfig](11-parameter-store/README.md) | 26 | [Governance and detection](26-governance-and-detection/README.md) |
| 12 | [CodePipeline](12-codepipeline/README.md) | 27 | [Resilience engineering](27-resilience-engineering/README.md) |
| 13 | [ECS](13-ECS/README.md) | 28 | [Generative AI](28-generative-ai/README.md) |
| 14 | [Jenkins](14-Jenkins/README.md) | | |

Work through them in the phase order in the update plan, which follows the
exam order. Module 19 comes early: it creates the lab account the other labs use.
