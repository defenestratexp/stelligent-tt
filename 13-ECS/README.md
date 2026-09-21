# Topic 13: Elastic Container Service (ECS)

<!-- TOC -->

- [Topic 13: Elastic Container Service (ECS)](#topic-13-elastic-container-service-ecs)
  - [What changed in the 2026 edition](#what-changed-in-the-2026-edition)
  - [Exam coverage](#exam-coverage)
  - [Cost and cleanup](#cost-and-cleanup)
  - [Guidance](#guidance)
  - [Lesson 13.1: Elastic Container Registry (ECR)](#lesson-131-elastic-container-registry-ecr)
    - [Principle 13.1](#principle-131)
    - [Practice 13.1](#practice-131)
      - [Lab 13.1.1: Create a Repository](#lab-1311-create-a-repository)
        - [Question: Tag Immutability](#question-tag-immutability)
      - [Lab 13.1.2: Lifecycle Policies](#lab-1312-lifecycle-policies)
        - [Question: Rule Priority](#question-rule-priority)
        - [Question: Expire or Archive](#question-expire-or-archive)
      - [Lab 13.1.3: Authenticate Docker to ECR](#lab-1313-authenticate-docker-to-ecr)
        - [Question: What Docker Stored](#question-what-docker-stored)
        - [Question: Two Ways to Log In](#question-two-ways-to-log-in)
      - [Lab 13.1.4: Build and Push Your Image](#lab-1314-build-and-push-your-image)
        - [Question: Base Image Source](#question-base-image-source)
        - [Question: CPU Architecture](#question-cpu-architecture)
      - [Lab 13.1.5: Image Scanning](#lab-1315-image-scanning)
        - [Question: Old Base Image](#question-old-base-image)
        - [Question: Basic or Enhanced](#question-basic-or-enhanced)
    - [Retrospective 13.1](#retrospective-131)
      - [Question: Image Encryption](#question-image-encryption)
      - [Question: Image Mirroring](#question-image-mirroring)
      - [Question: Repository Policies](#question-repository-policies)
  - [Lesson 13.2: ECS on EC2 with a Capacity Provider](#lesson-132-ecs-on-ec2-with-a-capacity-provider)
    - [Principle 13.2](#principle-132)
    - [Practice 13.2](#practice-132)
      - [Lab 13.2.1: Deploy the Starter](#lab-1321-deploy-the-starter)
        - [Question: What Bills by the Hour](#question-what-bills-by-the-hour)
        - [Question: The Missing NAT Gateways](#question-the-missing-nat-gateways)
      - [Lab 13.2.2: Create a Cluster](#lab-1322-create-a-cluster)
      - [Lab 13.2.3: EC2 Capacity](#lab-1323-ec2-capacity)
        - [Question: Clusters with Non-Default Names](#question-clusters-with-non-default-names)
        - [Question: Three Roles](#question-three-roles)
      - [Lab 13.2.4: Capacity Provider](#lab-1324-capacity-provider)
        - [Question: Target Capacity](#question-target-capacity)
        - [Question: Scale-In Protection](#question-scale-in-protection)
      - [Lab 13.2.5: Task Definition](#lab-1325-task-definition)
        - [Question: CPU Units](#question-cpu-units)
      - [Lab 13.2.6: Service](#lab-1326-service)
        - [Question: Provisioning](#question-provisioning)
        - [Question: Task Density](#question-task-density)
      - [Lab 13.2.7: Break a Deployment](#lab-1327-break-a-deployment)
        - [Question: Who Rolled Back](#question-who-rolled-back)
      - [Lab 13.2.8: Clean Up the EC2 Capacity](#lab-1328-clean-up-the-ec2-capacity)
        - [Question: Deletion Order](#question-deletion-order)
    - [Retrospective 13.2](#retrospective-132)
      - [Question: ECS with Custom AMIs](#question-ecs-with-custom-amis)
      - [Question: Instance Metadata from Tasks](#question-instance-metadata-from-tasks)
  - [Lesson 13.3: ECS on Fargate](#lesson-133-ecs-on-fargate)
    - [Principle 13.3](#principle-133)
    - [Practice 13.3](#practice-133)
      - [Lab 13.3.1: Fargate Capacity Providers](#lab-1331-fargate-capacity-providers)
      - [Lab 13.3.2: A Two-Container Task Definition](#lab-1332-a-two-container-task-definition)
        - [Question: Localhost](#question-localhost)
        - [Question: Fargate Sizes](#question-fargate-sizes)
      - [Lab 13.3.3: Fargate and Fargate Spot Service](#lab-1333-fargate-and-fargate-spot-service)
        - [Question: Base and Weight](#question-base-and-weight)
        - [Question: Spot Interruptions](#question-spot-interruptions)
      - [Lab 13.3.4: Private Subnets and Egress](#lab-1334-private-subnets-and-egress)
        - [Question: Three Ways Out](#question-three-ways-out)
      - [Lab 13.3.5: ECS Exec](#lab-1335-ecs-exec)
        - [Question: No SSH](#question-no-ssh)
        - [Question: Auditing Exec](#question-auditing-exec)
      - [Lab 13.3.6: Service Auto Scaling](#lab-1336-service-auto-scaling)
        - [Question: Which Metric](#question-which-metric)
    - [Retrospective 13.3](#retrospective-133)
      - [Question: EC2 Capacity](#question-ec2-capacity)
      - [Question: Fargate Storage](#question-fargate-storage)
      - [Question: Fargate, EC2 or Managed Instances](#question-fargate-ec2-or-managed-instances)
      - [Question: Scaling Vertically and Horizontally](#question-scaling-vertically-and-horizontally)
  - [Lesson 13.4: Service to Service with Service Connect](#lesson-134-service-to-service-with-service-connect)
    - [Principle 13.4](#principle-134)
    - [Practice 13.4](#practice-134)
      - [Lab 13.4.1: Namespace](#lab-1341-namespace)
      - [Lab 13.4.2: Backend Service](#lab-1342-backend-service)
        - [Question: Port Names](#question-port-names)
      - [Lab 13.4.3: Frontend Client](#lab-1343-frontend-client)
        - [Question: What Service Connect Added](#question-what-service-connect-added)
        - [Question: Other Ways to Connect](#question-other-ways-to-connect)
      - [Lab 13.4.4: Clean Up the Module](#lab-1344-clean-up-the-module)
    - [Retrospective 13.4](#retrospective-134)
      - [Question: Rolling or Blue/Green](#question-rolling-or-bluegreen)
      - [Question: Writing It Yourself](#question-writing-it-yourself)
  - [Further Reading](#further-reading)

<!-- /TOC -->

## What changed in the 2026 edition

- **ECR login uses `get-login-password`.** `aws ecr get-login` was removed
  in AWS CLI v2. Lab 13.1.3 pipes `aws ecr get-login-password` into
  `docker login --password-stdin`, then decodes `get-authorization-token` by
  hand to show what it does.
- **You push your own image, built from ECR Public.** Lab 13.1.4 builds a
  small nginx image from `public.ecr.aws/docker/library/nginx` instead of
  re-pushing Docker Hub's `nginx:latest`, and deals with CPU architecture
  (Apple silicon laptops build arm64 by default).
- **New Lab 13.1.5: image scanning.** Basic scan on push, configured at the
  registry level (the repository-level `ImageScanningConfiguration` is
  deprecated), with enhanced scanning through Amazon Inspector as an option.
  Lifecycle policies are combined into one lab that uses the policy preview
  and mentions the archive storage class.
- **EC2 capacity uses a launch template and a capacity provider.** The old
  lab used `AWS::AutoScaling::LaunchConfiguration`, t2.micro and Amazon
  Linux 2. Accounts created after October 1, 2024 can't create launch
  configurations, and the ECS-optimized Amazon Linux 2 AMI reached end of
  life on June 30, 2026. Lesson 13.2 uses the ECS-optimized Amazon Linux 2023
  AMI from its SSM public parameter, t3 instances, IMDSv2, and an Auto
  Scaling group capacity provider with managed scaling that starts at zero
  instances.
- **The starter has no NAT gateway by default.** The old `starter.yml` had
  two (about $66 a month plus their public IPv4 addresses, whether you used
  them or not). The new one runs tasks in public subnets, adds a free S3
  gateway endpoint, and creates **one** NAT gateway only when you set
  `EnableNatGateway=true` for Lab 13.3.4, which compares that with the
  public-IP and VPC-endpoint designs on cost.
- **Fargate facts corrected.** `Cpu: 256` is a quarter of a vCPU, not "256
  vCPU". Fargate *does* support bind mounts, Amazon EFS and Amazon EBS
  volumes (it doesn't support Docker volumes). The old "scaling vertically
  and horizontally" question defined both terms incorrectly; it's rewritten.
  The deprecated container links question is now a lab (13.3.2) on how
  containers in one `awsvpc` task share `localhost`.
- **New operations labs:** the deployment circuit breaker with rollback
  (13.2.7), Fargate Spot in a capacity provider strategy (13.3.3), ECS Exec
  instead of SSH (13.3.5), and service auto scaling (13.3.6).
- **New Lesson 13.4: ECS Service Connect** for service-to-service calls.
  AWS App Mesh, which older material pairs with ECS, is retired.
- CloudWatch logging is part of the first task definition rather than an
  afterthought, and every lesson ends with a cleanup step.
- The archived `fargatecli` link is gone. AWS Copilot CLI reached end of
  support on June 12, 2026; the retrospective points at its replacements.
- Labs use the lab region (`us-east-2`) and the `lab` profile; the
  placeholder account ID is `123456789012`.

## Exam coverage

| Exam | Domain / task statement |
|---|---|
| DVA-C02 → C03 | Domain 1: Development with AWS Services (Task 1.1: develop code for applications hosted on AWS: microservices, service-to-service communication). C03 guide publishes 2026-10-27 and adds GenAI / agent topics |
| DVA-C02 → C03 | Domain 2: Security (Task 2.1: task roles versus execution roles; Task 2.3: sensitive data in container configuration) |
| DVA-C02 → C03 | Domain 3: Deployment (Task 3.1: prepare application artifacts: container images in ECR; Task 3.4: deploy code: ECS rolling deployments and rollbacks) |
| DVA-C02 → C03 | Domain 4: Troubleshooting and Optimization (Task 4.1: root cause analysis with container logs and ECS events; Task 4.3: right-sizing tasks) |
| DOP-C02 | Domain 1: SDLC Automation (Task 1.3: build and manage artifacts: ECR, lifecycle policies, image scanning; Task 1.4: deployment strategies for container workloads, circuit breaker rollback) |
| DOP-C02 | Domain 2: Configuration Management and IaC (Task 2.1: ECS clusters, services and capacity in CloudFormation) |
| DOP-C02 | Domain 3: Resilient Cloud Solutions (Task 3.2: scalability: capacity providers, service auto scaling, Fargate Spot) |
| DOP-C02 | Domain 5: Incident and Event Response (Task 5.3: troubleshoot failed deployments and tasks; ECS Exec) |
| DOP-C02 | Domain 6: Security and Compliance (Task 6.2: vulnerability scanning of images; least-privilege task roles) |
| SAA-C03 | Domain 2: Design Resilient Architectures (Task 2.1: scalable and loosely coupled architectures: containers, service discovery) |
| SAA-C03 | Domain 3: Design High-Performing Architectures (Task 3.2: high-performing and elastic compute: ECS, Fargate) |
| SAA-C03 | Domain 4: Design Cost-Optimized Architectures (Task 4.2: cost-optimized compute: Fargate Spot, Graviton; Task 4.4: cost-optimized network: NAT gateways, VPC endpoints, public IPv4) |

## Cost and cleanup

Prices are for `us-east-2` in September 2026; see
[AWS Fargate pricing](https://aws.amazon.com/fargate/pricing/),
[Elastic Load Balancing pricing](https://aws.amazon.com/elasticloadbalancing/pricing/),
[Amazon VPC pricing](https://aws.amazon.com/vpc/pricing/) and
[Amazon ECR pricing](https://aws.amazon.com/ecr/pricing/).

- **Fargate** bills per second (one-minute minimum) for the vCPU and memory
  the *task* asks for: $0.04048 per vCPU-hour and $0.004445 per GB-hour on
  x86, $0.03238 and $0.00356 on ARM (Graviton). A 0.25 vCPU / 0.5 GB task is
  about 1.2 cents an hour, roughly $9 a month. Fargate Spot is up to 70%
  cheaper. 20 GiB of ephemeral storage per task is included.
- **The Application Load Balancer** in the starter costs $0.0225 an hour
  (about $16 a month) plus $0.008 per LCU-hour, **from the moment the
  starter stack exists**, whether or not anything is behind it.
- **Public IPv4 addresses** cost $0.005 an hour each: one per Fargate task
  in a public subnet, one per EC2 container instance, one per load balancer
  node, and one on the NAT gateway.
- **NAT gateway:** off by default. Lab 13.3.4 turns on one, at $0.045 an
  hour plus $0.045 per GB processed plus its public IPv4 address. Turn it
  off again at the end of the lab.
- **EC2 capacity** (Lesson 13.2): a t3.small is about 2 cents an hour. The
  Auto Scaling group starts at zero and scales to what the service needs.
- **Interface VPC endpoints** (only if you try the optional part of Lab
  13.3.4) are $0.01 per hour per Availability Zone each, plus $0.01 per GB.
- **ECR:** $0.10 per GB-month of storage; the lab images are tens of MB.
  Basic scanning is free. Enhanced scanning is billed by Amazon Inspector
  after its 15-day free trial.
- **CloudWatch Logs** ingestion is $0.50 per GB; lab logs are tiny. The
  starter's log group keeps logs for 7 days.
- Left running with two Fargate tasks, the module costs about $1.60 a day:
  roughly half for the load balancer and its addresses, half for the tasks
  and theirs. Delete the starter stack between study
  sessions; it recreates in a few minutes.
- Cleanup: [Lab 13.2.8](#lab-1328-clean-up-the-ec2-capacity) removes the
  EC2 capacity, and [Lab 13.4.4](#lab-1344-clean-up-the-module) removes
  everything else, including the ECR repository and the starter stack.

## Guidance

- Explore the official docs! See the Amazon ECS
  [Developer Guide](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html),
  [Best Practices Guide](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-best-practices.html),
  the Amazon ECR
  [User Guide](https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html),
  the [ECS](https://docs.aws.amazon.com/cli/latest/reference/ecs/index.html)
  and [ECR](https://docs.aws.amazon.com/cli/latest/reference/ecr/index.html)
  CLI references, and the
  [ECS](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/AWS_ECS.html)
  and [ECR](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/AWS_ECR.html)
  CloudFormation resource references.

- Avoid using other sites like stackoverflow.com for answers \-- part
  of the skill set you're building is finding answers straight from
  the source, AWS. ECS moves quickly; many tutorials still use launch
  configurations, `ecr get-login`, App Mesh or Copilot.

- Explore your curiosity. Try to understand why things work the way
  they do. Read more of the documentation than just what you need to
  find the answers.

- Use the `lab` profile. It sets the lab region (`us-east-2`), so the CLI
  commands in this module don't need `--region`. Include your identifier in
  stack names, resource names and tags. Examples use the placeholder account
  ID `123456789012`; substitute yours.

- You need Docker (Docker Desktop, Docker Engine or a compatible tool such
  as Podman or Finch) on your workstation, and the
  [Session Manager plugin](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html)
  for the AWS CLI for Lab 13.3.5.

- If at any point you are confused by ECS terminology, keep this picture
  in mind. A *task definition* is the recipe; a *task* is one running copy
  of it; a *service* keeps a number of tasks running; *capacity* (EC2
  instances you own, or Fargate) is where the tasks run; the *cluster*
  groups all of it.

  ```text
  +------------------------------------------------------------+
  | Cluster                                                    |
  |  +------------------------------------------------------+  |
  |  | Service (desired count, deployment settings, LB)     |  |
  |  |   +--------+   +--------+   +--------+               |  |
  |  |   |  Task  |   |  Task  |   |  Task  |  <- copies of |  |
  |  |   +--------+   +--------+   +--------+     a task    |  |
  |  +------|------------|------------|---------  definition |  |
  |         v            v            v                        |
  |  Capacity provider strategy                                |
  |    EC2 container instances (Auto Scaling group)            |
  |    or FARGATE / FARGATE_SPOT                               |
  +------------------------------------------------------------+
  ```

- For Lessons 13.2 to 13.4 a [starter](starter.yml) CloudFormation template
  provides the VPC, the load balancer, security groups, the task execution
  role, an empty task role and a log group, and exports them. It contains no
  `AWS::ECS::*` resources and no EC2 capacity. Put your ECS resources in
  your own stacks that import the starter's outputs with `Fn::ImportValue`,
  so you can delete and recreate them without touching the network. You're
  welcome to write everything from scratch, or in CDK (module 25), instead.

- Run `cfn-lint` on every template before you create or update a stack, as
  you did in module 01.

## Lesson 13.1: Elastic Container Registry (ECR)

### Principle 13.1

*ECR is a private, IAM-controlled registry in your account. It is the
default place to keep the images your AWS workloads run, and it can
expire, scan and replicate them for you.*

### Practice 13.1

This section sets up an ECR repository, cleans it up automatically,
authenticates Docker to it, and pushes an image you built. The repository
and its images are used in the rest of this module.

#### Lab 13.1.1: Create a Repository

Create a private ECR repository with CloudFormation, in its own stack.

- Use the
  [AWS::ECR::Repository](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-ecr-repository.html)
  resource type. Name it `<your-id>-web` and tag it with your identifier.

- Set `ImageTagMutability` to `IMMUTABLE`.

- Leave `EmptyOnDelete` unset (false) for now; you'll think about it in
  Lab 13.4.4.

- Output the repository URI (the `RepositoryUri` attribute) and
  [export](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/outputs-section-structure.html)
  it. You'll use it throughout this module.

##### Question: Tag Immutability

_What does `IMMUTABLE` stop you from doing? Why does that matter when an
ECS service deploys `my-image:v1` today and scales out tomorrow? How do the
`*_WITH_EXCLUSION` settings let you keep a mutable `latest` tag anyway,
and would you?_

#### Lab 13.1.2: Lifecycle Policies

Add a
[lifecycle policy](https://docs.aws.amazon.com/AmazonECR/latest/userguide/LifecyclePolicies.html)
to the repository in your template with two rules:

- keep only **one** untagged image, and
- expire any image pushed more than **30 days** ago.

Before you apply it, test it: write the policy JSON to a file and run
[`aws ecr start-lifecycle-policy-preview`](https://docs.aws.amazon.com/cli/latest/reference/ecr/start-lifecycle-policy-preview.html)
and `get-lifecycle-policy-preview` against the repository. (It's empty now;
run the preview again after Lab 13.1.4.) Then put the policy into the
template's `LifecyclePolicy` property and update the stack.

##### Question: Rule Priority

_Which of your two rules has to have the higher `rulePriority` number, and
why? What would happen to an untagged image that is also 31 days old?_

##### Question: Expire or Archive

_Lifecycle rules can now **archive** images to a cheaper storage class
instead of expiring them. When would you archive rather than delete? What
has to happen before an ECS task can run an archived image?_

#### Lab 13.1.3: Authenticate Docker to ECR

Docker needs credentials for your registry before it can push or pull.
Read [private registry authentication](https://docs.aws.amazon.com/AmazonECR/latest/userguide/registry_auth.html).

- Run `docker logout 123456789012.dkr.ecr.us-east-2.amazonaws.com` (with
  your account ID), then try to `docker pull` any tag from your repository
  URI. Save the error.

- Log in the current way:

  ```bash
  aws ecr get-login-password --profile lab \
    | docker login --username AWS --password-stdin \
      123456789012.dkr.ecr.us-east-2.amazonaws.com
  ```

- Log out and do it again by hand: call
  [`aws ecr get-authorization-token`](https://docs.aws.amazon.com/cli/latest/reference/ecr/get-authorization-token.html),
  base64-decode `authorizationToken`, and look at what's inside before you
  pass the password part to `docker login --password-stdin`. Don't paste
  the token anywhere, including your answers.

##### Question: What Docker Stored

_Where did `docker login` store the credential, and in what form? How long
is it valid? What would you use on a build server so nobody has to run
`docker login` at all? (Look up the Amazon ECR Docker Credential Helper.)_

##### Question: Two Ways to Log In

_Older tutorials use `$(aws ecr get-login --no-include-email)`. What
happens when you run that with AWS CLI v2, and why was it a security
problem (think about where the password ended up)? What did
`get-authorization-token` give you that `get-login-password` hides?_

#### Lab 13.1.4: Build and Push Your Image

Build a small web image of your own rather than re-pushing someone else's.

- Write a `Dockerfile` whose base image is
  `public.ecr.aws/docker/library/nginx:stable-alpine` (the Docker official
  nginx image, mirrored on
  [Amazon ECR Public](https://gallery.ecr.aws/)). Copy in an `index.html`
  that shows your identifier and a version string such as `v1`.

- Build it for **linux/amd64** (`docker buildx build --platform
  linux/amd64 ...`), run it locally with `docker run --rm -p 8080:80`, and
  check it with `curl localhost:8080`.

- Tag it with your repository URI and `v1`, and push it. Confirm with
  `aws ecr describe-images`.

- Try to push a different build to the same `v1` tag and save the error.
  Then make a `v2` (change the page) and push that too; you'll deploy both.

- Run the lifecycle policy preview from Lab 13.1.2 again.

##### Question: Base Image Source

_Why pull the base image from ECR Public instead of Docker Hub? Think about
Docker Hub's pull limits for anonymous users, and where your build and your
tasks run._

##### Question: CPU Architecture

_What happens if you build on an Apple silicon (arm64) laptop without
`--platform` and run the image on x86 capacity? What error would the task
show? How would you publish one tag that works on both architectures?_

#### Lab 13.1.5: Image Scanning

Read about
[image scanning](https://docs.aws.amazon.com/AmazonECR/latest/userguide/image-scanning.html).
Scan-on-push used to be a repository setting; it's now configured once for
the registry, with filters that choose repositories.

- Turn on **basic** scan on push for repositories that match
  `<your-id>-*` with
  [`aws ecr put-registry-scanning-configuration`](https://docs.aws.amazon.com/cli/latest/reference/ecr/put-registry-scanning-configuration.html).
  Save the previous configuration first
  (`get-registry-scanning-configuration`) so you can restore it.

- Push a `v3` of your image and read the results with
  `aws ecr describe-image-scan-findings`.

- Build one more image from an old base, such as
  `public.ecr.aws/docker/library/nginx:1.20-alpine`, push it as
  `old-base`, and compare its findings with `v3`.

<!-- VERIFY: confirm nginx:1.20-alpine is still available on the ECR Public docker/library mirror when running the lab. -->

##### Question: Old Base Image

_How many findings, and of what severity, did each image have? What does
that tell you about when to rebuild images that haven't changed? How would
you get notified when a new scan finishes (see
[ECR events and EventBridge](https://docs.aws.amazon.com/AmazonECR/latest/userguide/ecr-eventbridge.html))?_

##### Question: Basic or Enhanced

_What does enhanced scanning (Amazon Inspector) find that basic scanning
doesn't? What does "continuous" scanning mean for an image you pushed a
month ago? Why is basic scanning limited to one scan per image per day?_

### Retrospective 13.1

#### Question: Image Encryption

_How are ECR images encrypted at rest by default, and in transit? When
would you choose `KMS` (or `KMS_DSSE`) encryption instead, and why can't you
change it on an existing repository?_

#### Question: Image Mirroring

_Pushed copies of public images go stale. How would you keep an up-to-date
private copy of a Docker Hub image with an ECR
[pull through cache](https://docs.aws.amazon.com/AmazonECR/latest/userguide/pull-through-cache.html)
rule? What does Docker Hub require that ECR Public doesn't, and where do
those credentials live? How would a
[repository creation template](https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-creation-templates.html)
give the cached repositories your lifecycle policy?_

#### Question: Repository Policies

_Following least privilege, how would you let a second account (say, a
production account) pull from this repository without letting it push?
What conditions could you add to a repository policy, and when would you
use a registry policy instead?_

## Lesson 13.2: ECS on EC2 with a Capacity Provider

### Principle 13.2

*ECS schedules tasks onto capacity. When that capacity is EC2 instances you
own, a capacity provider lets ECS grow and shrink the Auto Scaling group to
fit the tasks, so you manage a launch template, not a fleet.*

### Practice 13.2

This section runs your image on EC2 container instances behind the
starter's load balancer. It's a long sequence: a cluster, a launch template
and Auto Scaling group, a capacity provider, a task definition and a
service. By the end you'll know every piece Fargate hides from you in
Lesson 13.3, and what it costs to own them.

Keep the stacks separate: the starter (network), one for the cluster and
its capacity, and one for the task definition and service. Delete and
recreate the last one freely.

#### Lab 13.2.1: Deploy the Starter

Read [starter.yml](starter.yml) before you deploy it. Then lint it and
create a stack called `<your-id>-ecs-network` with `StudentId` set and
`EnableNatGateway` left at `false`. You'll need `--capabilities
CAPABILITY_IAM`.

##### Question: What Bills by the Hour

_List every resource in the starter that has an hourly charge, with its
price. Which one costs money even though nothing is running yet?_

##### Question: The Missing NAT Gateways

_The 2022 starter created two NAT gateways and routed each private subnet
through its own. What did that cost per month before any traffic? The new
starter has none by default and one when asked. What do you give up with
one NAT gateway instead of one per Availability Zone? Why is that an
acceptable trade-off in a lab and not always in production? What does the
S3 gateway endpoint in the starter save you?_

#### Lab 13.2.2: Create a Cluster

Write a template for the cluster and its capacity. Start with the cluster:

- Use the
  [AWS::ECS::Cluster](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-ecs-cluster.html)
  resource type. Name the cluster `<your-id>` (not `default`) and tag it
  with your identifier.

- Take the starter's stack name as a parameter and import what you need
  from it with `Fn::ImportValue` and `Fn::Sub`.

- Leave Container Insights off for now (it's billed per metric); see
  Further Reading.

#### Lab 13.2.3: EC2 Capacity

Add EC2 capacity to the same template: a launch template and an Auto
Scaling group, as in modules 06 and 07.

- Use an
  [AWS::EC2::LaunchTemplate](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-ec2-launchtemplate.html).
  Launch configurations can't be created in new accounts.

- Take the AMI from the
  [ECS-optimized Amazon Linux 2023 AMI](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-optimized_AMI.html)
  SSM public parameter,
  `/aws/service/ecs/optimized-ami/amazon-linux-2023/recommended/image_id`,
  through an `AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>` parameter.
  The plain AL2023 AMI from earlier modules doesn't include the ECS agent.

- Use a `t3.small` instance type (as a parameter), require IMDSv2
  (`HttpTokens: required`), and add no key pair.

- Create an instance profile whose role has the
  `AmazonEC2ContainerServiceforEC2Role` and `AmazonSSMManagedInstanceCore`
  managed policies.

- Give the instances their own security group with **no inbound rules** and
  outbound HTTPS only. Put them in the starter's **public** subnets with a
  public IPv4 address, so they can reach ECS and ECR without a NAT gateway.

- In user data, tell the ECS agent which cluster to join by writing to
  `/etc/ecs/ecs.config` (see the
  [agent configuration](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-agent-config.html)).
  Add `ECS_AWSVPC_BLOCK_IMDS=true` as well; the retrospective asks why.

- Create an
  [AWS::AutoScaling::AutoScalingGroup](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-autoscaling-autoscalinggroup.html)
  from the launch template (`LatestVersionNumber`) with `MinSize` 0,
  `MaxSize` 2 and **no** `DesiredCapacity`, across both public subnets. Set
  `NewInstancesProtectedFromScaleIn: true`; Lab 13.2.4 explains why.

Deploy the stack. No instances should launch yet.

##### Question: Clusters with Non-Default Names

_If you leave `ECS_CLUSTER` out, which cluster does the agent try to join?
What do you see in `aws ecs list-container-instances` if the name is wrong?
How would you check the agent's log on an instance without SSH?_

##### Question: Three Roles

_This module uses an **instance role**, a **task execution role** and a
**task role**. For each: who assumes it, what does it need, and what would
break if it were missing? Which one does your application code use?_

#### Lab 13.2.4: Capacity Provider

Connect the Auto Scaling group to the cluster with a
[capacity provider](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/asg-capacity-providers.html).

- Add an
  [AWS::ECS::CapacityProvider](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-ecs-capacityprovider.html)
  for the group with managed scaling `ENABLED` and a target capacity of
  100, managed termination protection `ENABLED`, and managed draining
  `ENABLED`.

- Associate it with the cluster and make it the default strategy with
  [AWS::ECS::ClusterCapacityProviderAssociations](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-ecs-clustercapacityproviderassociations.html).

- Update the stack. Look at the Auto Scaling group: what did ECS add to it?
  It should still have zero instances.

##### Question: Target Capacity

_What does a target capacity of 100 mean, and what would 80 change? Which
CloudWatch metric does managed scaling track, and in which namespace?_

##### Question: Scale-In Protection

_Why does managed termination protection need
`NewInstancesProtectedFromScaleIn`? Without it, what could the Auto Scaling
group do to an instance that is running your only task? What does managed
draining add when an instance is terminated for another reason, such as an
instance refresh?_

#### Lab 13.2.5: Task Definition

Start a third template for the application: a task definition and a
service. Create the task definition first.

- Use the
  [AWS::ECS::TaskDefinition](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-ecs-taskdefinition.html)
  resource type with `NetworkMode: awsvpc` and `RequiresCompatibilities`
  of `EC2`.

- Set task-level `Cpu` to 256 and `Memory` to 512.

- One container, `web`, running your image by repository URI and tag. Take
  the tag as a parameter (default `v1`).

- Map container port 80, and give the port mapping a `Name` (`web`) and
  `AppProtocol` (`http`); Lesson 13.4 uses them.

- Send its output to the starter's log group with the `awslogs` log driver
  and a stream prefix. Set the execution role and task role from the
  starter.

Read
[task definition parameters](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task_definition_parameters.html)
for anything you're unsure about.

##### Question: CPU Units

_How much of a vCPU is `Cpu: 256`? What's the difference between task-level
and container-level `Memory` and `MemoryReservation`, and which of them are
required on Fargate?_

#### Lab 13.2.6: Service

Add the service to the application template and deploy it.

- Use the
  [AWS::ECS::Service](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-ecs-service.html)
  resource type with `DesiredCount` 1.

- Use a `CapacityProviderStrategy` with your capacity provider, not a
  `LaunchType`.

- Put the task network interfaces in the starter's **private** subnets
  with the starter's service security group. (On EC2 capacity the instance
  pulls the image and ships the logs, so the task itself doesn't need a
  route to the internet.)

- Register the `web` container on port 80 in the starter's target group,
  and set a `HealthCheckGracePeriodSeconds`.

- In `DeploymentConfiguration`, turn on the
  [deployment circuit breaker](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-circuit-breaker.html)
  with rollback, and keep `MinimumHealthyPercent` 100 and
  `MaximumPercent` 200.

While the stack creates, watch the service events
(`aws ecs describe-services --query 'services[0].events[:5]'`), the task's
`lastStatus`, and the Auto Scaling group. When the task is `RUNNING` and
the target is healthy, open the starter's `LoadBalancerUrl`. Follow the
container log with `aws logs tail /ecs/<your-id> --follow`.

##### Question: Provisioning

_What state was the task in before any instance existed, and what moved it
on? How long did it take from stack creation to a healthy target, and
where did the time go?_

##### Question: Task Density

_Scale the service to 4 tasks. How many instances did you end up with, and
why? A t3.small has room for more 0.25 vCPU tasks than that; what limit
did you hit? Read about
[ENI trunking](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/container-instance-eni.html).
Scale back to 1 and watch the group scale in; how long did it take?_

#### Lab 13.2.7: Break a Deployment

Deploy a version that can't start and let ECS undo it.

- Update the application stack with an image tag that doesn't exist, such
  as `v99`.

- Watch the service events and `aws ecs describe-services --query
  'services[0].deployments'`. Find the task's `stoppedReason`.

- When it's over, confirm what's running and what CloudFormation reports.
  Then deploy `v2` properly and check the page changed.

##### Question: Who Rolled Back

_Both ECS (circuit breaker) and CloudFormation (stack update) can roll
back. Which one acted first, and what state did each end in? How many
failed tasks did it take, and how is that number calculated? How would you
also roll back on a CloudWatch alarm, for a version that starts but
misbehaves?_

#### Lab 13.2.8: Clean Up the EC2 Capacity

Lesson 13.3 uses Fargate. Remove the EC2 pieces but keep the starter stack,
the log group and the ECR repository.

- Delete the application stack (task definition and service), then the
  cluster and capacity stack.

- Confirm that the Auto Scaling group and its instances are gone and that
  `aws ecs list-clusters` doesn't show your cluster.

##### Question: Deletion Order

_What would happen if you tried to delete the cluster stack while the
service still existed? If an instance is protected from scale-in, what has
to happen before the Auto Scaling group can be deleted?_

### Retrospective 13.2

#### Question: ECS with Custom AMIs

_You can run container instances from your own AMI. What has to be on it
for ECS to use it? (See
[installing the container agent](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-agent-install.html).)
The ECS-optimized AMI doesn't install security updates at launch; how would
you keep container instances patched?_

#### Question: Instance Metadata from Tasks

_What could a container on your instances do with the instance role's
credentials if it could reach the instance metadata service? How do
`ECS_AWSVPC_BLOCK_IMDS` and the IMDSv2 hop limit each help, and which
network modes does each one protect? (See
[task IAM roles](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-iam-roles.html).)_

## Lesson 13.3: ECS on Fargate

### Principle 13.3

*Fargate runs each task on capacity AWS manages. You don't choose or patch
instances; you choose the task's size and network, and you pay for exactly
that while it runs.*

### Practice 13.3

This section deploys the same image on Fargate and Fargate Spot, then uses
it to look at the things every container platform has to answer: how
containers in a task talk to each other, how tasks get out to the
internet, how you get a shell without SSH, and how a service scales.

#### Lab 13.3.1: Fargate Capacity Providers

Create a new cluster stack for Fargate.

- Use `AWS::ECS::Cluster` again, named `<your-id>` and tagged.

- Associate the `FARGATE` and `FARGATE_SPOT`
  [capacity providers](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-capacity-providers.html)
  with it (on the cluster itself, or with
  `AWS::ECS::ClusterCapacityProviderAssociations`). There's nothing else to
  build: no launch template, no group, no instance role.

#### Lab 13.3.2: A Two-Container Task Definition

Write a new task definition for Fargate with two containers.

- `RequiresCompatibilities: [FARGATE]`, `NetworkMode: awsvpc`, task-level
  `Cpu` 256 and `Memory` 512, and a `RuntimePlatform` of `LINUX` and
  `X86_64`.

- `web`: your image, as before, with a
  [container health check](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/healthcheck.html)
  that fetches `http://localhost/` (the Alpine nginx image has BusyBox
  `wget`, not `curl`).

- `probe`: `public.ecr.aws/amazonlinux/amazonlinux:2023`, not essential,
  that runs a shell loop which requests `http://localhost/` every 30
  seconds and prints the result. Make it start only after `web` is
  `HEALTHY` (`DependsOn`).

- Both log to the starter's log group with different stream prefixes.

##### Question: Localhost

_How did `probe` reach nginx at `localhost` without a link or an IP
address? The old version of this lab asked about Docker
[container links](https://docs.docker.com/engine/network/links/), which
Fargate doesn't support; why aren't they needed here? Could you run two
nginx containers listening on port 80 in the same task?_

##### Question: Fargate Sizes

_What's the smallest and largest task Fargate will run, and why does it
accept only certain CPU and memory pairs (see
[task CPU and memory](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-tasks-services.html#fargate-tasks-size))?
What would this task cost per month on x86, and on ARM?_

#### Lab 13.3.3: Fargate and Fargate Spot Service

Create a service for the new task definition.

- `DesiredCount` 2 and a `CapacityProviderStrategy` of `FARGATE` with
  `Base` 1 and `Weight` 1, and `FARGATE_SPOT` with `Weight` 1.

- Tasks in the starter's **public** subnets with `AssignPublicIp: ENABLED`
  and the service security group; the same target group; the circuit
  breaker with rollback.

- Deploy. Find which capacity provider each task landed on
  (`aws ecs describe-tasks`), and check the page.

##### Question: Base and Weight

_With this strategy, where do tasks 1 to 6 land as you scale up? Why is a
`Base` on on-demand Fargate a good idea for a web service?_

##### Question: Spot Interruptions

_What warning does a Fargate Spot task get before it's stopped, and how
does your container receive it? What does `stopTimeout` control? Does
nginx shut down cleanly on that signal? What does ECS do if no Spot
capacity is available?_

#### Lab 13.3.4: Private Subnets and Egress

A Fargate task pulls its own image and ships its own logs, so its network
interface needs a way to reach ECR, S3 and CloudWatch Logs.

- Update the service to use the **private** subnets and
  `AssignPublicIp: DISABLED`. Watch what happens to the new tasks, find the
  `stoppedReason`, and watch the circuit breaker.

- Update the starter stack with `EnableNatGateway=true`, and deploy the
  service again. Check that it works.

- Work out the hourly cost of the three ways to give private tasks a route
  out: a NAT gateway (one, or one per zone), interface VPC endpoints for
  ECR (`ecr.api`, `ecr.dkr`) and CloudWatch Logs plus the S3 gateway
  endpoint (see
  [ECR interface endpoints](https://docs.aws.amazon.com/AmazonECR/latest/userguide/vpc-endpoints.html)),
  and public subnets with a public IPv4 address per task.

- Optional: add the interface endpoints to a copy of the starter instead,
  with the NAT gateway off, and prove the tasks start without any route to
  the internet. Delete the endpoints afterwards.

- Put the service back in the public subnets, then update the starter with
  `EnableNatGateway=false`. Confirm with `aws ec2 describe-nat-gateways`
  that the gateway is deleting and that its Elastic IP is released.

##### Question: Three Ways Out

_For this lab (two tasks, a few MB a day) which egress design is cheapest?
At what number of tasks or GB per month does the answer change? Which
design would you choose for production, and what else do you need if you
also use ECS Exec (Lab 13.3.5) with the endpoints?_

#### Lab 13.3.5: ECS Exec

Get a shell in a running container without SSH, a bastion or an open port.
Read [ECS Exec](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-exec.html).

- Give the starter's task role the four `ssmmessages` permissions ECS Exec
  needs (see
  [ECS Exec permissions](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/task-iam-roles.html#ecs-exec-required-iam-permissions)),
  as a policy in your template attached to the imported role name, or by
  editing your copy of the starter.

- Set `EnableExecuteCommand: true` on the service and update it. Existing
  tasks don't get ECS Exec; confirm new ones did with
  `aws ecs describe-tasks` (the `ExecuteCommandAgent` must be `RUNNING`).

- Open a shell in the `web` container:

  ```bash
  aws ecs execute-command --cluster <your-id> --task <task-id> \
    --container web --interactive --command "/bin/sh"
  ```

- Inside, look at `ps`, `ip addr` (or `/proc/net`) and
  `wget -qO- localhost`. Then exit and find the `ExecuteCommand` event in
  CloudTrail (`aws cloudtrail lookup-events`).

##### Question: No SSH

_ECS Exec isn't SSH. What carries the session, which way do the
connections go, and why doesn't the service security group need an inbound
rule? What user do the commands run as?_

##### Question: Auditing Exec

_How would you log every command run through ECS Exec, and prevent people
from turning it on for production tasks? (Look at the cluster's
`executeCommandConfiguration` and the `ecs:enable-execute-command` IAM
condition key.)_

#### Lab 13.3.6: Service Auto Scaling

Scale the number of tasks with
[service auto scaling](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-auto-scaling.html),
which uses Application Auto Scaling.

- Add an
  [AWS::ApplicationAutoScaling::ScalableTarget](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-applicationautoscaling-scalabletarget.html)
  for the service (minimum 2, maximum 4) and a target tracking
  [AWS::ApplicationAutoScaling::ScalingPolicy](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-applicationautoscaling-scalingpolicy.html)
  on `ALBRequestCountPerTarget`.

- Send it requests from your workstation or CloudShell (a loop with `curl`
  is enough, or a load tool you already know) and watch the desired count
  and the alarms Application Auto Scaling created.

- Stop the load and note how long scale-in takes. Set the maximum back to 2
  when you're done.

##### Question: Which Metric

_Why is requests per target a better signal for this service than CPU?
What's the difference between the service's desired count in your
template and the one Application Auto Scaling sets, and how do you stop a
stack update from fighting the scaling policy?_

### Retrospective 13.3

#### Question: EC2 Capacity

_You didn't create any EC2 capacity in this lesson. Where did your tasks
run, what did Fargate size and patch for you, and what did you give up
compared with Lesson 13.2?_

#### Question: Fargate Storage

_The 2022 version of this module claimed Fargate doesn't support volumes
or bind mounts. What storage can a Fargate task actually use (see
[Fargate task storage](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-task-storage.html)),
what can't it use, and which option survives the task stopping?_

#### Question: Fargate, EC2 or Managed Instances

_Name workloads you couldn't run, or wouldn't want to run, on Fargate
(think GPUs, privileged containers, daemon tasks, very large or very
long-running tasks, sustained high utilization). ECS now also offers
[Managed Instances](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ManagedInstances.html),
where AWS runs EC2 instances in your account for you. Where does that sit
between Fargate and the Auto Scaling group you built, and how is it
billed?_

<!-- VERIFY: Managed Instances pricing — the docs say you pay for the whole EC2 instance; confirm whether there is also a per-instance management charge on the ECS pricing page. -->

#### Question: Scaling Vertically and Horizontally

_Scaling horizontally means running more copies of a task; scaling
vertically means giving each task more CPU and memory. How do you do each
one on Fargate and on EC2 capacity, and what has to be replaced in each
case? What does the capacity provider do when you scale either way on
EC2?_

## Lesson 13.4: Service to Service with Service Connect

### Principle 13.4

*Services should find each other by name, not by IP address or load
balancer. ECS Service Connect puts service discovery and a small proxy
into the service definition, so calls between services are named,
load-balanced, retried and measured without extra infrastructure.*

### Practice 13.4

This section splits the site into a frontend (the service you have) and a
backend `api` service with no load balancer, and connects them with
[Service Connect](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-connect.html).
Read the Service Connect
[concepts](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-connect-concepts.html)
page first.

#### Lab 13.4.1: Namespace

- Add an
  [AWS::ServiceDiscovery::HttpNamespace](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-servicediscovery-httpnamespace.html)
  named `<your-id>.internal` to your cluster stack.

- Set it as the cluster's `ServiceConnectDefaults` namespace.

#### Lab 13.4.2: Backend Service

- Build an `api` image: the same nginx base, returning a small JSON or
  text response that includes the word `api`. Push it to your repository
  with a new tag.

- Write a task definition for it on Fargate whose port mapping has
  `Name: api` and `AppProtocol: http`.

- Create a service for it with no load balancer, `DesiredCount` 1, in the
  public subnets with a public IP, and a `ServiceConnectConfiguration`
  that publishes port name `api` with a client alias of `api` on port 80.

- Make the service security group allow port 80 between tasks that use it
  (the `TODO(student)` in the starter).

##### Question: Port Names

_What's the difference between the port name, the discovery name and the
client alias? Which one does a client use in its URL?_

#### Lab 13.4.3: Frontend Client

- Build a new `web` image whose nginx configuration proxies `/api/` to
  `http://api/`, and push it.

- Update the frontend service: the new image, and a
  `ServiceConnectConfiguration` that is enabled with the namespace but
  publishes nothing (a client-only service).

- Request `<LoadBalancerUrl>/api/` and check that the response came from
  the backend. Open the **Service Connect** metrics for the backend in
  CloudWatch.

##### Question: What Service Connect Added

_Describe one of the frontend tasks. What container appeared that isn't in
your task definition, and whose CPU and memory does it use? What happens
to requests if the backend service has two tasks and one is unhealthy?_

##### Question: Other Ways to Connect

_Compare Service Connect with Cloud Map DNS-based service discovery, an
internal load balancer, and Amazon VPC Lattice for this frontend and
backend. Which would you use if a Lambda function also needed to call the
backend? What happened to AWS App Mesh?_

#### Lab 13.4.4: Clean Up the Module

Remove everything this module created.

- Delete the application stacks (both services and task definitions), then
  the cluster stack (the namespace goes with it).

- Deregister any task definition revisions you created outside
  CloudFormation (`aws ecs list-task-definitions`).

- Empty and delete the ECR repository. Either delete the images yourself
  (`aws ecr batch-delete-image`) or set `EmptyOnDelete: true` and update
  the stack before deleting it. Remove any pull through cache rules and
  their Secrets Manager secrets if you made them.

- Restore the registry scanning configuration you saved in Lab 13.1.5.

- Delete the starter stack. The log group is deleted with it.

- Confirm that nothing is left: `aws ecs list-clusters`,
  `aws ecr describe-repositories`, `aws elbv2 describe-load-balancers`,
  `aws ec2 describe-nat-gateways --filter Name=state,Values=available`,
  `aws ec2 describe-addresses`, and `aws logs describe-log-groups
  --log-group-name-prefix /ecs/`.

### Retrospective 13.4

#### Question: Rolling or Blue/Green

_Every deployment in this module was a rolling update. ECS now has a
[built-in blue/green deployment strategy](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-type-blue-green.html)
that also works with Service Connect. How does it differ from a rolling
update with the circuit breaker, and from the older CodeDeploy blue/green
deployments? When is the extra capacity during a deployment worth paying
for?_

#### Question: Writing It Yourself

_You wrote the cluster, capacity, task definitions and services by hand.
Compare that with
[Amazon ECS Express Mode](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/express-service-overview.html)
and with the CDK `ApplicationLoadBalancedFargateService` pattern from
module 25. What does each decide for you, and what would you check before
trusting those decisions (NAT gateways, public IPs, security groups, log
retention)?_

## Further Reading

- The
  [Amazon ECS Best Practices Guide](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-best-practices.html)
  covers networking, capacity, security and deployments in more depth than
  this module.

- [Fargate task networking](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-task-networking.html):
  how each task gets its own network interface, and what it needs to pull
  images and send logs.

- [Container Insights with enhanced observability](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/cloudwatch-container-insights.html)
  adds per-task and per-container metrics; check the per-metric pricing
  before turning it on in a lab account.

- You can share images across accounts with a repository policy. See the
  [repository policy examples](https://docs.aws.amazon.com/AmazonECR/latest/userguide/repository-policy-examples.html),
  and
  [private image replication](https://docs.aws.amazon.com/AmazonECR/latest/userguide/replication.html)
  for copying them to other regions or accounts.

- [Seekable OCI (SOCI)](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/fargate-tasks-services.html#fargate-tasks-soci-images)
  lazy loading starts Fargate tasks with large images faster.

- The AWS Copilot CLI reached end of support on June 12, 2026. The
  [announcement](https://aws.amazon.com/blogs/containers/announcing-the-end-of-support-for-the-aws-copilot-cli/)
  explains the migration paths (Express Mode and CDK L3 constructs).
