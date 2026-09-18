# Topic 15: Kubernetes on Amazon EKS

<!-- TOC -->

- [Topic 15: Kubernetes on Amazon EKS](#topic-15-kubernetes-on-amazon-eks)
  - [What changed in the 2026 edition](#what-changed-in-the-2026-edition)
  - [Exam coverage](#exam-coverage)
  - [Cost and cleanup](#cost-and-cleanup)
  - [Guidance](#guidance)
  - [Conventions](#conventions)
  - [Lesson 15.1: An EKS cluster with Auto Mode](#lesson-151-an-eks-cluster-with-auto-mode)
    - [Principle 15.1](#principle-151)
    - [Practice 15.1](#practice-151)
      - [Lab 15.1.1: Tools and account settings](#lab-1511-tools-and-account-settings)
        - [Question: Which Version](#question-which-version)
      - [Lab 15.1.2: Create the cluster](#lab-1512-create-the-cluster)
        - [Question: NAT Gateway](#question-nat-gateway)
        - [Question: Two IAM Roles](#question-two-iam-roles)
      - [Lab 15.1.3: Connect kubectl](#lab-1513-connect-kubectl)
        - [Question: Where the Credentials Come From](#question-where-the-credentials-come-from)
      - [Lab 15.1.4: Look around an empty cluster](#lab-1514-look-around-an-empty-cluster)
        - [Question: Where Is CoreDNS](#question-where-is-coredns)
        - [Question: No Nodes](#question-no-nodes)
    - [Retrospective 15.1](#retrospective-151)
      - [Question: Pausing a Cluster](#question-pausing-a-cluster)
      - [Question: eksctl or Infrastructure as Code](#question-eksctl-or-infrastructure-as-code)
  - [Lesson 15.2: Standing up Pods](#lesson-152-standing-up-pods)
    - [Principle 15.2](#principle-152)
    - [Practice 15.2](#practice-152)
      - [Lab 15.2.1: Standing Up Pods Imperatively](#lab-1521-standing-up-pods-imperatively)
        - [Question: Pending Pod](#question-pending-pod)
      - [Lab 15.2.2: Pulling Definition File of Existing Pod](#lab-1522-pulling-definition-file-of-existing-pod)
      - [Lab 15.2.3: Generating New Pod Definition File](#lab-1523-generating-new-pod-definition-file)
        - [Question: Client or Server Dry Run](#question-client-or-server-dry-run)
        - [Question: Requests and Auto Mode](#question-requests-and-auto-mode)
      - [Lab 15.2.4: Standing Up Pods Declaratively](#lab-1524-standing-up-pods-declaratively)
        - [Question: Create or Apply](#question-create-or-apply)
    - [Retrospective 15.2](#retrospective-152)
      - [Question: Where Did the Node Go](#question-where-did-the-node-go)
  - [Lesson 15.3: Standing Up Deployment](#lesson-153-standing-up-deployment)
    - [Principle 15.3](#principle-153)
    - [Practice 15.3](#practice-153)
      - [Lab 15.3.1: Standing Up Deployment Imperatively](#lab-1531-standing-up-deployment-imperatively)
        - [Question: Pods after Deletion](#question-pods-after-deletion)
        - [Question: Standalone Pods](#question-standalone-pods)
      - [Lab 15.3.2: Pulling Definition File of Existing Deployment](#lab-1532-pulling-definition-file-of-existing-deployment)
      - [Lab 15.3.3: Generating New Deployment Definition File](#lab-1533-generating-new-deployment-definition-file)
        - [Question: Dry-Run Flag](#question-dry-run-flag)
      - [Lab 15.3.4: Standing Up Deployment Declaratively](#lab-1534-standing-up-deployment-declaratively)
        - [Question: Scale Drift](#question-scale-drift)
      - [Lab 15.3.5: Introduction to ReplicaSets](#lab-1535-introduction-to-replicasets)
        - [Question: ReplicaSet Deletion](#question-replicaset-deletion)
    - [Retrospective 15.3](#retrospective-153)
  - [Lesson 15.4: Perform Rolling Update on Deployment](#lesson-154-perform-rolling-update-on-deployment)
    - [Principle 15.4](#principle-154)
    - [Practice 15.4](#practice-154)
      - [Lab 15.4.1: Rolling Update of Deployment with Definition File](#lab-1541-rolling-update-of-deployment-with-definition-file)
        - [Question: Different Definition File](#question-different-definition-file)
        - [Question: Update Behaviors](#question-update-behaviors)
      - [Lab 15.4.2: Changing Image of Deployment Using kubectl](#lab-1542-changing-image-of-deployment-using-kubectl)
        - [Question: Edit Name](#question-edit-name)
        - [Question: Edit Replica Count](#question-edit-replica-count)
      - [Lab 15.4.3: Roll Back a Bad Release](#lab-1543-roll-back-a-bad-release)
        - [Question: Stuck Rollout](#question-stuck-rollout)
    - [Retrospective 15.4](#retrospective-154)
      - [Question: Rollback Strategy](#question-rollback-strategy)
  - [Lesson 15.5: Setting Up ECR for Use with EKS](#lesson-155-setting-up-ecr-for-use-with-eks)
    - [Principle 15.5](#principle-155)
    - [Practice 15.5](#practice-155)
      - [Lab 15.5.1: Create ECR Repository](#lab-1551-create-ecr-repository)
        - [Question: Immutable Tags](#question-immutable-tags)
      - [Lab 15.5.2: Push Image to ECR](#lab-1552-push-image-to-ecr)
        - [Question: Image Architecture](#question-image-architecture)
    - [Retrospective 15.5](#retrospective-155)
      - [Question: ECR Access](#question-ecr-access)
      - [Question: Pulls Through the NAT Gateway](#question-pulls-through-the-nat-gateway)
  - [Lesson 15.6: Creating Custom Deployment](#lesson-156-creating-custom-deployment)
    - [Principle 15.6](#principle-156)
    - [Practice 15.6](#practice-156)
      - [Lab 15.6.1: Creating Custom Deployment Definition File](#lab-1561-creating-custom-deployment-definition-file)
        - [Question: Docker Registry Access](#question-docker-registry-access)
        - [Question: Probes](#question-probes)
      - [Lab 15.6.2: Introduction to Services in Kubernetes](#lab-1562-introduction-to-services-in-kubernetes)
      - [Lab 15.6.3: Deploying Kubernetes Service](#lab-1563-deploying-kubernetes-service)
        - [Question: Internal by Default](#question-internal-by-default)
        - [Question: Multiple External Ports](#question-multiple-external-ports)
        - [Question: Source Ranges](#question-source-ranges)
    - [Retrospective 15.6](#retrospective-156)
      - [Question: Delete Deployment](#question-delete-deployment)
      - [Question: Service or Ingress](#question-service-or-ingress)
  - [Lesson 15.7: Perform Rolling Update on Custom Deployment](#lesson-157-perform-rolling-update-on-custom-deployment)
    - [Principle 15.7](#principle-157)
    - [Practice 15.7](#practice-157)
      - [Lab 15.7.1: Change Background Color](#lab-1571-change-background-color)
        - [Question: Deployment vs Standalone Pods](#question-deployment-vs-standalone-pods)
        - [Question: Errors During the Rollout](#question-errors-during-the-rollout)
    - [Retrospective 15.7](#retrospective-157)
  - [Lesson 15.8: Auto Mode Compute](#lesson-158-auto-mode-compute)
    - [Principle 15.8](#principle-158)
    - [Practice 15.8](#practice-158)
      - [Lab 15.8.1: Watch It Scale](#lab-1581-watch-it-scale)
        - [Question: Who Picked the Instance](#question-who-picked-the-instance)
        - [Question: Consolidation](#question-consolidation)
      - [Lab 15.8.2: Managed Instances](#lab-1582-managed-instances)
        - [Question: What You Can't Do](#question-what-you-cant-do)
      - [Lab 15.8.3: A Capped NodePool](#lab-1583-a-capped-nodepool)
        - [Question: Is It a Cap](#question-is-it-a-cap)
        - [Question: Burstable Instances](#question-burstable-instances)
    - [Retrospective 15.8](#retrospective-158)
      - [Question: Auto Mode or Not](#question-auto-mode-or-not)
  - [Lesson 15.9: Who Can Do What](#lesson-159-who-can-do-what)
    - [Principle 15.9](#principle-159)
    - [Practice 15.9](#practice-159)
      - [Lab 15.9.1: Who Can Already Get In](#lab-1591-who-can-already-get-in)
        - [Question: The aws-auth ConfigMap](#question-the-aws-auth-configmap)
      - [Lab 15.9.2: A Namespace-Scoped Viewer](#lab-1592-a-namespace-scoped-viewer)
        - [Question: Access Policy or RBAC Group](#question-access-policy-or-rbac-group)
      - [Lab 15.9.3: Pod Identity](#lab-1593-pod-identity)
        - [Question: Where the Pod's Credentials Come From](#question-where-the-pods-credentials-come-from)
        - [Question: Pods Created Too Early](#question-pods-created-too-early)
      - [Lab 15.9.4: Tighten the Trust Policy](#lab-1594-tighten-the-trust-policy)
        - [Question: Two Places to Say No](#question-two-places-to-say-no)
    - [Retrospective 15.9](#retrospective-159)
      - [Question: Pod Identity or IRSA](#question-pod-identity-or-irsa)
      - [Question: Another Account](#question-another-account)
  - [Lesson 15.10: Tearing It Down](#lesson-1510-tearing-it-down)
    - [Principle 15.10](#principle-1510)
    - [Practice 15.10](#practice-1510)
      - [Lab 15.10.1: Remove What Kubernetes Created](#lab-15101-remove-what-kubernetes-created)
      - [Lab 15.10.2: Delete the Cluster and Your Stacks](#lab-15102-delete-the-cluster-and-your-stacks)
      - [Lab 15.10.3: Verify Nothing Is Left](#lab-15103-verify-nothing-is-left)
        - [Question: Orphans](#question-orphans)
    - [Retrospective 15.10](#retrospective-1510)
      - [Question: Guardrails](#question-guardrails)
  - [Further Reading](#further-reading)

<!-- /TOC -->

## What changed in the 2026 edition

- **EKS Auto Mode instead of managed node groups.** The cluster in
  `eksctl/cluster.yaml` now uses
  [EKS Auto Mode](https://docs.aws.amazon.com/eks/latest/userguide/automode.html):
  EKS launches, patches and removes the EC2 instances, and runs the
  networking, load balancing, storage, DNS and Pod Identity components
  for you. The old file created two node groups (four `t3.small`
  instances) that ran whether or not anything was scheduled. A new
  Lesson 15.8 shows how Auto Mode picks instances and how a NodePool
  limits what it can launch.
- **A current, pinned Kubernetes version with standard support only.**
  The config pins Kubernetes 1.36 and sets the upgrade policy to
  `STANDARD`. New clusters default to *extended* support, which costs
  $0.60 an hour instead of $0.10 once standard support ends, and eksctl
  picks its own default version (1.34 in eksctl 0.230.0, whose standard
  support ends 2026-12-02) if you don't pin one.
- **kubectl commands fixed.** `kubectl run --generator=run-pod/v1` fails
  with `unknown flag` on current kubectl; `kubectl run` now always creates
  a Pod. Bare `--dry-run` is `--dry-run=client` (or `=server`), and
  `--record` is replaced by the `kubernetes.io/change-cause` annotation
  and `kubectl rollout history`. Image tags are pinned instead of
  `latest`.
- **Access entries instead of the `aws-auth` ConfigMap.** Auto Mode
  requires access entries, and the cluster uses the `API` authentication
  mode, so it has no `aws-auth` ConfigMap at all. New Lesson
  15.9 grants a second IAM role read-only access to one namespace with an
  EKS access policy. The AWS IAM Authenticator install step is gone:
  kubectl gets tokens from `aws eks get-token`.
- **EKS Pod Identity.** New Lab 15.9.3 gives a Pod read access to one S3
  bucket through a Pod Identity association, and the retrospective
  compares it with IAM roles for service accounts (IRSA).
- **The sample app is rebuilt.** The 2022 app was a Create React App on
  Node.js 12 (end of life April 2022) with hundreds of npm dependencies. It's now a
  dependency-free Node.js 22 server that shows its version and the Pod
  that served the request, so rolling updates are visible. The old app
  also only changed color at runtime because the container ran React's
  development server.
- **ECR.** The repository template drops a repository policy that added
  nothing for same-account pulls (and named `ecr:GetAuthorizationToken`,
  which isn't a repository-level action), and adds immutable tags, scan on
  push, a lifecycle rule and `EmptyOnDelete`. Push uses
  `aws ecr get-login-password`, and images are built for `linux/amd64`.
- **Load balancers.** A `LoadBalancer` Service now gets a Network Load
  Balancer from Auto Mode. It is **internal unless you ask for
  `internet-facing`**, and the labs restrict it to your own IP address.
- **Cost and cleanup.** The module states what the cluster costs by the
  hour, and a final lesson deletes resources in the order that avoids
  orphaned load balancers, network interfaces and volumes, then checks
  for them. aws-vault, Cloud9-era instructions and `us-east-1` are gone.

## Exam coverage

| Exam | Domain / task statement |
|---|---|
| DOP-C02 | Domain 1: SDLC Automation (Task 1.3: build and manage artifacts in ECR; Task 1.4: deployment strategies for container environments such as Amazon EKS, rolling updates and rollback, troubleshooting deployment issues) |
| DOP-C02 | Domain 3: Resilient Cloud Solutions (Task 3.2: deploying container-based applications on Amazon EKS; auto scaling and load balancing) |
| DOP-C02 | Domain 4: Monitoring and Logging (Task 4.3: EKS autoscalers; analyzing incidents in Amazon EKS) |
| DOP-C02 | Domain 6: Security and Compliance (Task 6.1: roles for human and machine access, least privilege, attribute-based access control with session tags) |
| SAP-C02 → C03 | Domain 2: Design for New Solutions (Task 2.1: deployment strategy; Task 2.3: security controls; Task 2.6: cost optimization) |
| SAP-C02 → C03 | Domain 4: Accelerate Workload Migration and Modernization (Task 4.4: opportunities for modernization, containers). C03 guide publishes 2026-10-27 and adds GenAI / agent topics |

**Not in scope:** the skills the CNCF's CKA and CKAD exams test beyond
what AWS exams ask, such as building a cluster with kubeadm, etcd backup
and restore, node troubleshooting, and writing RBAC, NetworkPolicies and
StatefulSets from memory. This module teaches enough Kubernetes to run
workloads on EKS and to answer the EKS questions on the AWS exams. Further
Reading points at where to go next.

## Cost and cleanup

EKS is the most expensive thing in the course to leave running by
accident. Everything below is billed by the hour, in `us-east-2`, whether
or not you're using it.

| Resource | Rough cost | Created by |
|---|---|---|
| EKS control plane, standard support | $0.10/hour (about $73 a month) | `eksctl create cluster` |
| Same, **extended** support | $0.60/hour | a version past its 14 months of standard support. The config sets `upgradePolicy: STANDARD` so this can't happen |
| EKS Auto Mode management fee | per instance, on top of the EC2 price (about 12% of the On-Demand price for the examples on the pricing page) | every node Auto Mode launches |
| Nodes (EC2) | a 2-vCPU instance is roughly $0.04 to $0.10/hour; Auto Mode launches none until a Pod needs one | Pods you schedule |
| NAT gateway | $0.045/hour plus $0.045 per GB processed, plus its public IPv4 address | the eksctl VPC (one gateway) |
| Network Load Balancer | about $0.0225/hour plus capacity units, plus a public IPv4 address per Availability Zone at $0.005/hour | each `LoadBalancer` Service |
| EBS volumes | node root and data volumes, cents per day | Auto Mode, deleted with the node |
| ECR storage, S3 | cents | Lessons 15.5 and 15.9 |

With the cluster, one or two small nodes and one NLB, expect **$0.30 to
$0.40 an hour, or $7 to $10 a day.** Left running for a month, that's
well over $200.

- **There is no "stop" for EKS.** You can't pause the control plane. If
  you're stopping for more than a few hours, delete the cluster (Lab
  15.10.2) and recreate it from your `cluster.yaml` later; creation takes
  15 to 20 minutes. Your manifests and your ECR stack can stay.
- **Delete load balancers before the cluster.** Kubernetes Services of
  type `LoadBalancer` and Ingresses create load balancers, security
  groups and network interfaces in your VPC that CloudFormation doesn't
  know about. If they outlive the cluster, they keep billing and block
  deletion of the eksctl VPC stack. Auto Mode and eksctl both try to
  clean them up, but only while the cluster is reachable. Delete them
  yourself first.
- **Auto Mode resources are hidden by default.** In accounts that had no
  managed instances before April 2026, EC2 hides the instances, volumes
  and network interfaces that Auto Mode creates from the console and from
  `describe` calls. They are still billed. Lab 15.1.1 shows the setting,
  and the cleanup checks pass `--include-managed-resources`.
- **Cleanup:** [Lesson 15.10](#lesson-1510-tearing-it-down) removes
  everything in order and then checks for orphaned load balancers,
  network interfaces, EBS volumes, NAT gateways, stacks and roles.

<!-- VERIFY: hourly figures were read from the EKS, VPC and ELB pricing
pages in September 2026 (us-east-1 figures); confirm us-east-2 matches.
The 12% management fee is derived from the EKS pricing page examples
(m5a.xlarge, c6a.2xlarge), not stated as a percentage. -->

## Guidance

- Prerequisites: module 13 (containers, ECR) and a basic understanding
  of Docker and Dockerfiles. Module 03 (IAM roles and trust policies)
  matters for Lesson 15.9.

- Explore the official docs! See the
  [Amazon EKS User Guide](https://docs.aws.amazon.com/eks/latest/userguide/what-is-eks.html),
  the [EKS Best Practices Guide](https://docs.aws.amazon.com/eks/latest/best-practices/introduction.html),
  the [Kubernetes documentation](https://kubernetes.io/docs/home/), the
  [kubectl reference](https://kubernetes.io/docs/reference/kubectl/) and
  the [eksctl documentation](https://docs.aws.amazon.com/eks/latest/eksctl/what-is-eksctl.html).

- Two sets of docs apply at once. Kubernetes concepts (Pods,
  Deployments, Services) are documented on kubernetes.io; how EKS
  implements them on AWS (nodes, load balancers, IAM) is in the EKS
  User Guide. When they seem to disagree, the EKS guide describes what
  your cluster actually does.

- Avoid using other sites like stackoverflow.com for answers \-- part
  of the skill set you're building is finding answers straight from
  the source. Kubernetes blog posts age quickly: anything that uses
  `--generator`, `aws-auth`, `extensions/v1beta1` or `aws-iam-authenticator`
  predates what you're running.

- Explore your curiosity. Try to understand why things work the way
  they do. Read more of the documentation than just what you need to
  find the answers.

## Conventions

- **Profile and Region.** Everything runs in the lab account in
  `us-east-2` with the `lab` profile: `export AWS_PROFILE=lab` in each
  shell. eksctl reads the Region from `metadata.region` in the config
  file, which is set to `us-east-2`.
- **Names.** Your cluster is `<your-id>-lab15`. Other resources start
  with `<your-id>` and are tagged `owner=<your-id>` and `topic=15`.
- **Namespace.** Your workloads go in a namespace called `lab15`
  (created in Lab 15.2.1), not `default`.
- **Placeholders.** Examples use `123456789012` for the lab account.
  Never commit your real account ID, your kubeconfig, or the IP address
  you use in Lab 15.6.2.
- **Your repository.** Keep your manifests and your copy of
  `cluster.yaml` in `15-Kubernetes/` of your lab repository, one branch
  per lesson.
- **Image registry.** Public images come from the
  [Amazon ECR Public Gallery](https://gallery.ecr.aws/) copies of the
  Docker Official Images (`public.ecr.aws/docker/library/...`). Your
  nodes share one NAT gateway address, and Docker Hub limits anonymous
  pulls to 100 per six hours per address.

## Lesson 15.1: An EKS cluster with Auto Mode

### Principle 15.1

*EKS runs the Kubernetes control plane for you, and with Auto Mode it
runs the nodes too. You still own the workloads, who can reach them, and
the bill.*

### Practice 15.1

A Kubernetes cluster has a **control plane** (the API server, etcd, the
scheduler and controllers) and a **data plane** of nodes that run your
Pods. EKS runs the control plane across three Availability Zones in an
AWS-owned account and charges per cluster-hour. For the data plane you
choose one of:

| Option | Who runs the instances | You manage |
|---|---|---|
| Self-managed nodes | You | AMI, Auto Scaling group, upgrades, add-ons |
| Managed node groups | EKS, in an Auto Scaling group you size | Instance types, scaling, upgrade timing, add-ons |
| Fargate | AWS, one micro-VM per Pod | Fargate profiles; no DaemonSets, no Pod Identity |
| **EKS Auto Mode** | EKS, as EC2 *managed instances* chosen per workload | NodePools (optional) and your workloads |

Read [Automate cluster infrastructure with EKS Auto
Mode](https://docs.aws.amazon.com/eks/latest/userguide/automode.html)
and [Learn about Amazon EKS Auto Mode managed
instances](https://docs.aws.amazon.com/eks/latest/userguide/automode-learn-instances.html)
before you start.

You'll create the cluster with [eksctl](https://docs.aws.amazon.com/eks/latest/eksctl/what-is-eksctl.html),
the official CLI for EKS. It reads a `ClusterConfig` file and deploys
CloudFormation stacks for the VPC, IAM roles and cluster. That makes it
the shortest readable path to a working cluster; Retrospective 15.1 asks
you to compare it with writing the same thing in CloudFormation, CDK or
Terraform.

#### Lab 15.1.1: Tools and account settings

- Install or update:
  - [AWS CLI v2](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html),
    a recent release (the cleanup checks need `--include-managed-resources`).
  - [kubectl](https://kubernetes.io/docs/tasks/tools/), within one minor
    version of the cluster: 1.35, 1.36 or 1.37 for a 1.36 cluster.
  - [eksctl](https://eksctl.io/installation/) 0.215.0 or later (the
    course was written with 0.230.0). eksctl validates the version you ask
    for against the EKS API, so a newer Kubernetes version works even if
    the eksctl release predates it.
    <!-- VERIFY: eksctl 0.230.0 hard-codes versions up to 1.35 but
    validates against DescribeClusterVersions; creating a 1.36 Auto Mode
    cluster with it was not tested for this edition. -->
  - Docker, with `buildx` (included in current Docker Desktop and Docker
    Engine).
- `export AWS_PROFILE=lab`, run `aws sso login` if needed, and confirm
  `aws sts get-caller-identity` shows the lab account.
- Run `aws eks describe-cluster-versions --query
  "clusterVersions[].[clusterVersion,status,endOfStandardSupportDate]"
  --output table`. Note which versions are in `STANDARD_SUPPORT` and
  when each one's standard support ends.
- Run `aws ec2 get-managed-resource-visibility`. If it says `hidden`,
  the EC2 instances, volumes and network interfaces Auto Mode creates
  won't appear in the EC2 console or in plain `describe-*` output. In
  your dedicated lab account you may set it to `visible` with
  `aws ec2 modify-managed-resource-visibility --default-visibility
  visible` for this module; write down the original value so Lab 15.10.3
  can restore it. See [Managed resource visibility
  settings](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/amazon-ec2-managed-instances.html#managed-resource-visibility-settings).

##### Question: Which Version

_Which Kubernetes version will you use, and when does its standard
support end? What does eksctl pick if `metadata.version` is left out,
and why is that a cost risk? What happens to a cluster with upgrade
policy `STANDARD` on the day its version leaves standard support?
(See [Understand the Kubernetes version lifecycle on
EKS](https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html).)_

#### Lab 15.1.2: Create the cluster

- Copy `eksctl/cluster.yaml` from this module into your lab repository.
  Read every line and its comment, then replace `<your-id>` and, if your
  answer to the last question differs, the version.
- Compare it with the [Auto Mode eksctl
  example](https://docs.aws.amazon.com/eks/latest/userguide/automode-get-started-eksctl.html)
  and the [eksctl config file
  schema](https://schema.eksctl.io/). Find where the file sets the
  authentication mode, the upgrade policy and the NAT gateway.
- Run `eksctl create cluster -f cluster.yaml`. It takes 15 to 20
  minutes.
- While you wait, open the CloudFormation console (or run
  `aws cloudformation describe-stack-resources --stack-name
  eksctl-<your-id>-lab15-cluster`) and list what the stack creates:
  subnets, route tables, NAT gateway, security groups, IAM roles and the
  `AWS::EKS::Cluster` resource.

If creation fails with `UnsupportedAvailabilityZoneException`, add
`availabilityZones:` with three `us-east-2` zones named in the error
message to the config and try again. Delete the failed stacks first
(`eksctl delete cluster -f cluster.yaml`).

##### Question: NAT Gateway

_Auto Mode puts nodes in the private subnets. Why do they need a NAT
gateway at all? What would it take to run without one? (Think about
which endpoints the nodes call: the EKS API, ECR, S3, STS.) What does
`gateway: HighlyAvailable` change, in resilience and in cost?_

##### Question: Two IAM Roles

_eksctl created a cluster IAM role and a node IAM role. Find both
(`aws eks describe-cluster --name <your-id>-lab15 --query
"cluster.[roleArn,computeConfig]"`) and list their attached policies.
Which one lets nodes pull from your private ECR repository in Lesson
15.5?_

#### Lab 15.1.3: Connect kubectl

- eksctl added a context to `~/.kube/config`. Run `kubectl config
  get-contexts` and `kubectl cluster-info`.
- If you use another machine, or the context is missing, create it with
  `aws eks update-kubeconfig --name <your-id>-lab15 --alias lab15`. See
  [Connect kubectl to an EKS cluster by creating a kubeconfig
  file](https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html).
- Run `kubectl version` and check the client and server versions are
  within one minor version.
- Open `~/.kube/config` and find the `users:` entry for the cluster.
  There's no password or certificate for you in it.

##### Question: Where the Credentials Come From

_What command does kubectl run to authenticate, and what does it send to
the API server? What happens to your kubectl session when your IAM
Identity Center session expires, and how do you fix it? If the
kubeconfig names no AWS profile, which credentials does that command
use?_

#### Lab 15.1.4: Look around an empty cluster

- Run `kubectl get nodes`. There are none. Run `kubectl get pods -A`.
  Compare with what a cluster with managed node groups shows: `aws-node`,
  `kube-proxy` and `coredns` Pods.
- Run `kubectl get nodepools` and `kubectl get nodeclasses`, then
  `kubectl describe nodepool general-purpose`.
- Run `kubectl api-resources | grep -E "eks.amazonaws.com|karpenter"`
  to see the custom resources Auto Mode adds.
- Run `aws eks describe-cluster --name <your-id>-lab15 --query
  "cluster.{version:version,upgradePolicy:upgradePolicy,access:accessConfig,compute:computeConfig,storage:storageConfig}"`
  and `aws eks list-addons --cluster-name <your-id>-lab15`.

##### Question: Where Is CoreDNS

_A Kubernetes cluster needs DNS, networking and a proxy on every node.
In an Auto Mode cluster, where do CoreDNS, the VPC CNI and kube-proxy
run, and who upgrades them? (See [Learn about VPC Networking and Load
Balancing in EKS Auto
Mode](https://docs.aws.amazon.com/eks/latest/userguide/auto-networking.html).)_

##### Question: No Nodes

_What is this cluster costing you right now, with no nodes? What will
make the first node appear?_

### Retrospective 15.1

#### Question: Pausing a Cluster

_You can stop an EC2 instance overnight, but not an EKS cluster. Work
out what the cluster in this lab costs per day with no workloads, and
decide whether you'll keep it between study sessions or delete and
recreate it. What would you have to redo after recreating it?_

#### Question: eksctl or Infrastructure as Code

_eksctl generated CloudFormation for you. The same cluster could be an
`AWS::EKS::Cluster` with `ComputeConfig` in your own template, a CDK
construct (module 25) or a Terraform module (module 17). What do you
gain and lose with each? Which would you choose for a team that runs
twenty clusters?_

## Lesson 15.2: Standing up Pods

### Principle 15.2

*A Pod is the smallest unit Kubernetes schedules: one or more containers
that share a network address and storage, placed together on one node.*

### Practice 15.2

Now that you have a cluster, you're going to launch
[Pods](https://kubernetes.io/docs/concepts/workloads/pods/) imperatively
with `kubectl` and declaratively with definition files. In an Auto Mode
cluster the first Pod also makes EKS launch the first node, which you'll
watch happen.

#### Lab 15.2.1: Standing Up Pods Imperatively

- Create a namespace for the module and make it your default:

  ```bash
  kubectl create namespace lab15
  kubectl config set-context --current --namespace=lab15
  ```

- Run `kubectl get pods`. There are no Pods in the namespace.
- In a second terminal, run `kubectl get nodes --watch`, and in a third,
  `kubectl get nodeclaims --watch`.
- Run:

  ```bash
  kubectl run busybox --image=public.ecr.aws/docker/library/busybox:1.37 -- sleep 3000
  ```

> The result of the command should be `pod/busybox created`

- In the command above:
  - `kubectl run` creates a single Pod. (Before Kubernetes 1.18 it could
    also create Deployments and Jobs, which is what the old
    `--generator=run-pod/v1` flag chose between. The flag is gone.)
  - the Pod is named `busybox`
  - the image is `busybox:1.37` from the ECR Public Gallery. Without a
    registry host, such as `busybox:1.37`, the image comes from Docker
    Hub.
  - everything after `--` replaces the container's command: `sleep 3000`
- Run `kubectl get pods` a few times. The Pod is `Pending` for about a
  minute, while a NodeClaim and then a node appear in your other
  terminals, and then it is `Running`.
- Run `kubectl describe pod busybox` and read the results. They show:
  - the [namespace](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)
    and [node](https://kubernetes.io/docs/concepts/architecture/nodes/)
    the Pod runs on, and its IP address. Compare that IP with the VPC
    subnet ranges.
  - the containers, their image and command
  - [volume](https://kubernetes.io/docs/concepts/storage/volumes/) mounts,
    including the service account token
  - [tolerations](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/)
  - the Events: `FailedScheduling`, then `Nominated`, `Scheduled`,
    `Pulling`, `Started`
- Run `kubectl get nodes -L node.kubernetes.io/instance-type,karpenter.sh/nodepool,topology.kubernetes.io/zone`.

##### Question: Pending Pod

_Why was the Pod `Pending` at first? Which component decided to launch a
node, which NodePool did it use, and which instance type did it pick?
What is the relationship between a NodeClaim, a node and an EC2
instance?_

#### Lab 15.2.2: Pulling Definition File of Existing Pod

- Run `kubectl get pod busybox -o yaml > busybox-pod-lab152.yaml`
  - Open `busybox-pod-lab152.yaml` in a text editor.
  - This is what a [Pod manifest](https://kubernetes.io/docs/concepts/workloads/pods/#using-pods)
    looks like after the cluster has filled it in.
  - Most of these fields (the `status:` section, `uid`,
    `resourceVersion`, the node name, default tolerations) were added at
    creation time.
- Run `kubectl delete pod busybox` to delete the Pod.

The next section will go over creating Pod definition files.

#### Lab 15.2.3: Generating New Pod Definition File

Definition files are useful because they can be put into version control
and reviewed, and they lock in a Pod's configuration.

- Run:

  ```bash
  kubectl run busybox --image=public.ecr.aws/docker/library/busybox:1.37 \
    --dry-run=client -o yaml -- sleep 3000 > busybox-pod-lab153.yaml
  ```

- Open `busybox-pod-lab153.yaml`.
  - Compare it with `busybox-pod-lab152.yaml` from
    [Lab 15.2.2](#lab-1522-pulling-definition-file-of-existing-pod).
    The new file has far fewer fields; the cluster fills in defaults for
    anything you leave out.
  - `apiVersion:` names the API group and version for the resource type,
    and `kind:` names the type. They go together: a Pod is `v1`, a
    Deployment is `apps/v1`. `kubectl api-resources` lists them all.
  - `metadata:` holds the `name:` and can hold `namespace:`, `labels:`
    and `annotations:`. Labels are how Deployments and Services find
    their Pods, as you'll see in the next lessons.
  - `spec.containers:` is a list: each entry names an image and, here,
    the arguments that replace its command.
- Add a `resources:` block to the container that requests `50m` of CPU
  and `32Mi` of memory. See [Resource Management for Pods and
  Containers](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/).

##### Question: Client or Server Dry Run

_Run the same command with `--dry-run=server`. What's different about
the output, and what did the server check that the client couldn't?_

##### Question: Requests and Auto Mode

_Auto Mode sizes and launches nodes from the resource requests of Pods
that can't be scheduled. What happens when Pods request nothing? What
happens when they request far more than they use?_

#### Lab 15.2.4: Standing Up Pods Declaratively

- Run `kubectl apply -f busybox-pod-lab153.yaml`

> The result of the command should be `pod/busybox created`

- Run `kubectl get pods` and `kubectl describe pod busybox`.
- Change the `sleep` duration in the file and run `kubectl apply` again.
  Read the error.

After you're done inspecting the Pod, delete it with `kubectl delete -f
busybox-pod-lab153.yaml`.

##### Question: Create or Apply

_What's the difference between `kubectl create -f` and `kubectl apply
-f`? Why couldn't `apply` change the command of a running Pod?_

### Retrospective 15.2

Read more about the [Pod
Lifecycle](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/).

#### Question: Where Did the Node Go

_Leave `kubectl get nodes --watch` running for a few minutes after the
last Pod is deleted. What happens to the node, and why? What does that
mean for a Pod you start ten minutes from now?_

## Lesson 15.3: Standing Up Deployment

### Principle 15.3

*A Deployment declares how many copies of a Pod you want and which
version they run; its controllers keep reality matching that
declaration.*

### Practice 15.3

Now that you've stood up Pods imperatively and declaratively, you'll do
the same with
[Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/).

#### Lab 15.3.1: Standing Up Deployment Imperatively

- Run:

  ```bash
  kubectl create deployment nginx-deployment \
    --image=public.ecr.aws/docker/library/nginx:1.30
  ```

> The result of the command should be `deployment.apps/nginx-deployment created`

- Use [kubectl get](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_get/)
  to list the Deployments in your namespace. Yours should be there.
- Run `kubectl describe deployment nginx-deployment`. The results show:
  - the number of replicas (desired, updated, available)
  - the update strategy
  - the Pod template: containers, images, ports
  - the label selector that decides which Pods belong to the Deployment
  - events
- Run `kubectl get pods`. There is a Pod named `nginx-deployment-*`.
- Note the Pod's name, delete it with `kubectl delete pod <name>`, and
  run `kubectl get pods` again.

##### Question: Pods after Deletion

_Why was there still a Pod after you deleted it? Is it the same Pod?_

##### Question: Standalone Pods

_Can you think of [use
cases](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#use-case)
for Deployments over standalone Pods? Is there any case where a
standalone Pod is the right choice?_

#### Lab 15.3.2: Pulling Definition File of Existing Deployment

- Generate the YAML definition of your existing Deployment and save it
  as `nginx-deployment-lab332.yaml`. Use the
  [kubectl get](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_get/)
  docs if you need them.
  - Notice the `apiVersion:` and `kind:` differ from the Pod file.
  - Find the fields a Pod manifest doesn't have.
- Run `kubectl delete deployment nginx-deployment`.

#### Lab 15.3.3: Generating New Deployment Definition File

- Run:

  ```bash
  kubectl create deployment nginx-deployment \
    --image=public.ecr.aws/docker/library/nginx:1.30 \
    --dry-run=client -o yaml > nginx-deployment-lab333.yaml
  ```

- Compare it with the file from the previous lab.
- Look at `strategy:` in the previous lab's file. That's the update
  policy the Deployment gets if you don't set one.
- Look at `spec.template:`. It's a Pod definition in the same format as
  a Pod file, minus `apiVersion` and `kind`.
- Look at `spec.replicas:`. It defaults to 1. If a Pod in a Deployment
  is deleted or crashes, another one replaces it.
- Look at `spec.selector.matchLabels:`. The same labels must be on the
  Pods in `spec.template.metadata.labels`, or the API server rejects the
  Deployment.
- Add a `resources.requests` block to the container, as in Lab 15.2.3.

##### Question: Dry-Run Flag

_What happens if you leave out `--dry-run=client`? Why does the old
spelling, a bare `--dry-run`, no longer work?_

#### Lab 15.3.4: Standing Up Deployment Declaratively

- Change `replicas:` in `nginx-deployment-lab333.yaml` to 3.
  - Run `kubectl apply -f nginx-deployment-lab333.yaml`
  - Check the Deployment and count its Pods.
  - Run `kubectl get pods -o wide` and see which nodes they landed on.
- Scale with kubectl:
  - `kubectl scale deployment/nginx-deployment --replicas=6`
  - Inspect the Deployment and Pods again.
  - Read [Scaling a
    Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#scaling-a-deployment),
    including the HorizontalPodAutoscaler.
- Run `kubectl diff -f nginx-deployment-lab333.yaml`.

##### Question: Scale Drift

_The file says 3 replicas and the cluster has 6. What does `kubectl
diff` show, and what happens at the next `kubectl apply`? What does that
tell you about mixing imperative and declarative changes?_

#### Lab 15.3.5: Introduction to ReplicaSets

A Deployment doesn't manage Pods directly. It creates a
[ReplicaSet](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/)
for each version of its Pod template, and the ReplicaSet keeps the right
number of Pods running.

- Run `kubectl get replicasets`.
  - The `DESIRED` count matches the replicas you set on the Deployment.
- Run `kubectl describe replicaset <your-replicaset-name>`. Compare it
  with the Deployment and Pod output.
- Generate the YAML of the ReplicaSet with kubectl and find its
  `ownerReferences`.

##### Question: ReplicaSet Deletion

_What do you think will happen if you delete the ReplicaSet? In a second
terminal run `kubectl get replicasets,pods --watch` (or `watch kubectl
get all` if you have `watch`), then delete the ReplicaSet in the first.
Why did Pods terminate, and why did new ones start?_

### Retrospective 15.3

Think of situations where `kubectl` commands are the right tool and
where definition files are. Consider an application with several
Deployments owned by different teams, and a production incident at 3 AM.

Keep the Deployment from this lesson running for the next one.

## Lesson 15.4: Perform Rolling Update on Deployment

### Principle 15.4

*A rolling update replaces Pods a few at a time, so a Deployment changes
version without downtime, and every change is a revision you can roll
back to.*

### Practice 15.4

Next you'll perform a [rolling
update](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#updating-a-deployment)
on the Deployment from [Lab
15.3.4](#lab-1534-standing-up-deployment-declaratively), then roll it
back.

#### Lab 15.4.1: Rolling Update of Deployment with Definition File

Copy `nginx-deployment-lab333.yaml` to `nginx-deployment-lab341.yaml`.

- In `nginx-deployment-lab341.yaml`:
  - change the image to `public.ecr.aws/docker/library/nginx:1.31`
  - change `replicas` to `10`
  - add the annotation `kubernetes.io/change-cause: "nginx 1.31, 10 replicas"`
    under `metadata.annotations` of the Deployment
- In a second terminal run `kubectl get pods --watch`; in a third,
  `kubectl get deployment nginx-deployment --watch`.
- Apply the new file and run `kubectl rollout status
  deployment/nginx-deployment`.
  - Watch Pod names change and the `UP-TO-DATE` and `AVAILABLE` columns.
  - Confirm the image changed by inspecting the Pods and the Deployment.
- Keep the watches running for the next lab.

##### Question: Different Definition File

_Why didn't the Deployment's name change when you applied a different
file?_

##### Question: Update Behaviors

_How is the update behavior set? Pull the Deployment's configuration
with kubectl and read `spec.strategy`. What do `maxSurge` and
`maxUnavailable` mean for 10 replicas, and how many new ReplicaSets
exist now?_

#### Lab 15.4.2: Changing Image of Deployment Using kubectl

There are other ways to change a Deployment with kubectl.

- Run:

  ```bash
  kubectl set image deployment/nginx-deployment \
    nginx=public.ecr.aws/docker/library/nginx:1.30-alpine
  kubectl annotate deployment/nginx-deployment \
    kubernetes.io/change-cause="nginx 1.30-alpine via set image"
  ```

  - Confirm the image changed.
  - `nginx` in `nginx=...` is the *container* name, not the Deployment
    name.
- Run `kubectl rollout history deployment/nginx-deployment`. The
  annotation is what fills `CHANGE-CAUSE`; it replaces the deprecated
  `--record` flag.

Next use [`kubectl edit`](https://kubernetes.io/docs/reference/kubectl/generated/kubectl_edit/)
to update the Deployment.

- Run `kubectl edit deployment nginx-deployment`
  - It opens the live configuration in your `$EDITOR` (vi if unset).
  - Change the image to `public.ecr.aws/docker/library/nginx:1.31-alpine`
    and save. The Deployment starts updating.
  - If the edit is rejected, kubectl saves your attempt to a file in
    `/tmp` and tells you where.

##### Question: Edit Name

_What happens if you change the Deployment's name in `kubectl edit`? Try
it._

##### Question: Edit Replica Count

_What happens if you change the replica count in `kubectl edit`? Which
file in your repository is now wrong?_

#### Lab 15.4.3: Roll Back a Bad Release

- Set the image to a tag that doesn't exist, such as
  `public.ecr.aws/docker/library/nginx:9.99`, with `kubectl set image`.
- Run `kubectl rollout status deployment/nginx-deployment` and `kubectl
  get pods`. Read the events of one of the new Pods.
- Count how many old Pods are still running.
- Roll back with `kubectl rollout undo deployment/nginx-deployment`,
  then roll back to a specific earlier revision with `--to-revision`.
  See [Rolling Back a
  Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#rolling-back-a-deployment).

##### Question: Stuck Rollout

_Why did the broken rollout stop instead of replacing every Pod? How
long until the Deployment reports that it failed to progress, and where
is that set? What would have caught this in a pipeline before it
reached the cluster?_

Remove the Deployment (`kubectl delete deployment nginx-deployment`)
before starting the next lesson.

### Retrospective 15.4

#### Question: Rollback Strategy

_`kubectl rollout undo` rolls back the cluster but not your repository.
Consider how keeping one definition file per release in version
control, and deploying only from it, changes how you roll forward and
back. How does this compare with the ECS deployment circuit breaker from
module 13?_

## Lesson 15.5: Setting Up ECR for Use with EKS

### Principle 15.5

*ECR is a private, managed container registry. Nodes in the same account
pull from it with their IAM role; no registry passwords live in the
cluster.*

### Practice 15.5

In this lesson you'll create an [ECR
repository](https://docs.aws.amazon.com/AmazonECR/latest/userguide/Repositories.html),
build the sample app and push it. Make sure Docker is running.

#### Lab 15.5.1: Create ECR Repository

- Read `ecr/ecr.yaml` in this module. Look up
  [`ImageTagMutability`](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-ecr-repository.html),
  `EmptyOnDelete` and the lifecycle policy.
- Deploy it:

  ```bash
  aws cloudformation deploy --template-file ecr/ecr.yaml \
    --stack-name <your-id>-lab15-ecr \
    --parameter-overrides Prefix=<your-id> \
    --tags owner=<your-id> topic=15
  ```

- Get the repository URI from the stack's `RepositoryUri` output
  (`aws cloudformation describe-stacks --stack-name <your-id>-lab15-ecr
  --query "Stacks[0].Outputs"`).

##### Question: Immutable Tags

_What happens if you push `v1` twice? Why is that useful for a
Deployment that names `:v1`, and why is `latest` a poor tag to deploy
from?_

#### Lab 15.5.2: Push Image to ECR

- Read `sample_app/server.js`, `sample_app/Dockerfile` and
  `sample_app/README.md`. Run the app locally as the README shows.
- Log Docker in to your registry (see [Private registry
  authentication](https://docs.aws.amazon.com/AmazonECR/latest/userguide/registry_auth.html)):

  ```bash
  aws ecr get-login-password | docker login --username AWS \
    --password-stdin 123456789012.dkr.ecr.us-east-2.amazonaws.com
  ```

- Build for `linux/amd64`, tag with the repository URI and `:v1`, and
  push. See [Pushing a Docker
  image](https://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html).
- Confirm with
  `aws ecr describe-images --repository-name <your-id>-kubernetes`, and read the scan result with `aws ecr
  describe-image-scan-findings`.

##### Question: Image Architecture

_Why does the build say `--platform linux/amd64`? What happens on an
Apple silicon Mac if you leave it out, and how would you build one image
that runs on both amd64 and arm64 (Graviton) nodes?_

### Retrospective 15.5

#### Question: ECR Access

_How do your nodes get permission to pull from this repository? Look at
the node role from Lab 15.1.2 and at the [ECR on EKS
docs](https://docs.aws.amazon.com/AmazonECR/latest/userguide/ECR_on_EKS.html).
The 2022 template had a repository policy granting the account root;
why wasn't it needed? When would you need a repository policy?_

#### Question: Pulls Through the NAT Gateway

_Every image layer your nodes pull goes through the NAT gateway at
$0.045 per GB. What would you add to the VPC to avoid that for ECR, and
what would it cost?_

## Lesson 15.6: Creating Custom Deployment

### Principle 15.6

*A Service gives a changing set of Pods one stable address. A Service of
type `LoadBalancer` asks the cloud for a load balancer in front of it.*

### Practice 15.6

In this lesson you'll deploy the image you pushed and put a Network Load
Balancer in front of it. In Auto Mode, EKS itself creates the load
balancer; no controller to install.

#### Lab 15.6.1: Creating Custom Deployment Definition File

Using what you've learned, write a Deployment definition file,
`custom-deployment.yaml`:

- Name the Deployment `custom-deployment`, with label `app: custom`.
- Use your ECR image URI with the `:v1` tag.
- Declare [container
  port](https://kubernetes.io/docs/concepts/services-networking/connect-applications-service/)
  `8080`.
- Set the [environment
  variables](https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/)
  `BG_COLOR` to a color of your choice and `APP_VERSION` to `v1`.
- Request `100m` CPU and `64Mi` memory, and limit memory to `128Mi`.
- Add a [readiness and a liveness
  probe](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
  on `GET /healthz`, port 8080.
- Add a `securityContext` that sets `runAsNonRoot: true` and
  `allowPrivilegeEscalation: false`.
- Set replicas to `2`.

Generate a starting point with `kubectl create deployment --dry-run=client
-o yaml`, then edit. Check your file with `kubectl apply --dry-run=server
-f custom-deployment.yaml`, then apply it and check the Deployment and
Pods before moving on. `kubectl logs deployment/custom-deployment` shows
the app's startup line.

##### Question: Docker Registry Access

_How would your cluster pull images from a private registry that isn't
ECR, such as a private Docker Hub or GitHub Container Registry
repository? (See [Images](https://kubernetes.io/docs/concepts/containers/images/).)
Where would that credential live, and who could read it?_

##### Question: Probes

_What would happen during a rolling update without the readiness probe?
What would happen if the liveness probe pointed at a path that takes
five seconds to answer?_

#### Lab 15.6.2: Introduction to Services in Kubernetes

Next you'll put a
[Service](https://kubernetes.io/docs/concepts/services-networking/service/)
in front of the Deployment so you can reach it from your browser.

- Run:

  ```bash
  kubectl expose deployment custom-deployment --type=LoadBalancer \
    --name=custom-service --port=80 --target-port=8080 \
    --dry-run=client -o yaml > custom-service.yaml
  ```

- Open the file and read it.
  - `spec.type` is the [Service
    type](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types).
    You're using `LoadBalancer`.
  - `port` is what the load balancer listens on; `targetPort` is the
    container port.
  - `selector` is how the Service finds its Pods: every Ready Pod with
    those labels.
- Read [Use Service Annotations to configure Network Load
  Balancers](https://docs.aws.amazon.com/eks/latest/userguide/auto-configure-nlb.html).
  Then edit the file:
  - Add the annotation
    `service.beta.kubernetes.io/aws-load-balancer-scheme: internet-facing`.
  - Set `spec.loadBalancerClass: eks.amazonaws.com/nlb` (the Auto Mode
    default, written down so it's explicit).
  - Set `spec.loadBalancerSourceRanges` to your own public address as a
    `/32` (`curl -s https://checkip.amazonaws.com`), so the load balancer
    isn't open to the whole internet.

#### Lab 15.6.3: Deploying Kubernetes Service

- Apply `custom-service.yaml` and run `kubectl get service custom-service
  --watch` until `EXTERNAL-IP` shows a DNS name.
- Find the load balancer in AWS: `aws elbv2 describe-load-balancers
  --query "LoadBalancers[].[LoadBalancerName,Type,Scheme,DNSName]"`.
  Look at its target group with `aws elbv2 describe-target-groups` and
  `describe-target-health`. The targets are Pod IP addresses, not
  instances.
- After a few minutes, open `http://<EXTERNAL-IP>/` in your browser. The
  background is your `BG_COLOR`. Refresh a few times and watch the Pod
  name.

##### Question: Internal by Default

_What kind of load balancer would you have got without the `scheme`
annotation, and could you have reached it? Why is that a sensible
default?_

##### Question: Multiple External Ports

_Can a Service map more than one external port to the same container
port? Try it by editing the Service. Why might you want to?_

##### Question: Source Ranges

_What did Auto Mode do with `loadBalancerSourceRanges`? Find the
security group rules on the load balancer. What happens when your home
IP address changes?_

### Retrospective 15.6

#### Question: Delete Deployment

_What happens to the Service, and to the load balancer, if you delete the
Deployment but not the Service? What does it cost?_

#### Question: Service or Ingress

_A Service of type `LoadBalancer` gives you one NLB per Service. Read
[Create an IngressClass to configure an Application Load
Balancer](https://docs.aws.amazon.com/eks/latest/userguide/auto-configure-alb.html).
When would you use an Ingress and an ALB instead, and how many load
balancers would ten web apps need each way?_

## Lesson 15.7: Perform Rolling Update on Custom Deployment

### Principle 15.7

*During a rolling update, a Service sends traffic only to Pods that are
Ready, so users see old and new versions side by side but no errors.*

### Practice 15.7

You'll change the background color with a rolling update while the app
is behind the load balancer.

#### Lab 15.7.1: Change Background Color

- Scale your Deployment to `5` replicas with kubectl.
- Copy the Deployment file to `custom-deployment-lab371.yaml`.
  - Set replicas to `5`.
  - Set `BG_COLOR` to a different color and `APP_VERSION` to `v2`.
  - Add a `kubernetes.io/change-cause` annotation.
- In another terminal, request the page in a loop and print the version
  and Pod name:

  ```bash
  while true; do curl -s http://<EXTERNAL-IP>/ | grep -o -E 'v[0-9]+|custom-deployment-[a-z0-9-]+' | paste -sd' ' -; sleep 0.5; done
  ```

- Apply the new file and watch the loop output until every response is
  `v2`.

##### Question: Deployment vs Standalone Pods

_What are the benefits of using a Service with Pods that are part of a
Deployment over a Service with standalone Pods?_

##### Question: Errors During the Rollout

_Did any request fail during the update? If some did, why: think about
how long the load balancer takes to register a new Pod IP and to stop
sending to an old one, and what the app does on `SIGTERM`. Which Pod or
Deployment settings would you change to make it cleaner?_

### Retrospective 15.7

Read about [performing a rolling
update](https://kubernetes.io/docs/tutorials/kubernetes-basics/update/update-intro/),
and compare the Kubernetes rolling update with the ECS rolling and
blue/green deployments in module 13. Which exam scenarios call for
blue/green or canary instead?

Keep the custom Deployment and Service for the next lesson.

## Lesson 15.8: Auto Mode Compute

### Principle 15.8

*In Auto Mode you describe what your Pods need and EKS chooses, launches,
patches and removes the instances. Your levers are resource requests and
NodePools.*

### Practice 15.8

Auto Mode runs [Karpenter](https://karpenter.sh/) for you. Karpenter
watches for Pods that can't be scheduled, picks the cheapest instance
that fits them from what a NodePool allows, launches it, and later
removes or replaces nodes that are empty, underused, drifted or expired.
Read [Create a Node Pool for EKS Auto
Mode](https://docs.aws.amazon.com/eks/latest/userguide/create-node-pool.html)
and [Enable or Disable Built-in
NodePools](https://docs.aws.amazon.com/eks/latest/userguide/set-builtin-node-pools.html).

#### Lab 15.8.1: Watch It Scale

- Keep `kubectl get nodeclaims --watch` running in another terminal.
- Scale `custom-deployment` to 20 replicas.
- When all Pods are Running, run `kubectl get nodes -L
  node.kubernetes.io/instance-type,karpenter.sh/capacity-type,topology.kubernetes.io/zone`
  and `kubectl get pods -o wide`.
- Scale back to 2 and keep watching for five minutes.

##### Question: Who Picked the Instance

_Which instance types did Auto Mode launch, in which zones, and why
those? What would change if each Pod requested `1` CPU instead of
`100m`?_

##### Question: Consolidation

_What happened to the extra nodes after you scaled down, and how long
did it take? What protects a workload from being moved at a bad moment?
(Look up PodDisruptionBudgets and NodePool disruption budgets.)_

#### Lab 15.8.2: Managed Instances

- Find one node's EC2 instance ID (`kubectl get node <name> -o
  jsonpath='{.spec.providerID}'`) and describe it:
  `aws ec2 describe-instances --instance-ids <id> --query
  "Reservations[].Instances[].[InstanceType,Operator,MetadataOptions]"`.
- Try `aws ec2 stop-instances --instance-ids <id>`. Read the error.
- Start a Pod that tries to use the node's credentials:

  ```bash
  kubectl run imds-test --rm -it --restart=Never \
    --image=public.ecr.aws/aws-cli/aws-cli:2.36.49 -- sts get-caller-identity
  ```

##### Question: What You Can't Do

_Why can't you stop, SSH into, or change the AMI of an Auto Mode node?
What does EKS do about OS patches, and how often are nodes replaced? What
is `MetadataOptions` set to, and why did the Pod find no credentials?_

#### Lab 15.8.3: A Capped NodePool

- Read `k8s/nodepool-lab.yaml` in this module and apply it.
- Run `kubectl rollout restart deployment/custom-deployment` and watch
  which NodePool the new nodes come from.
- Scale `custom-deployment` to 20 replicas again. Watch the `lab15-small`
  NodePool reach its limits (`kubectl describe nodepool lab15-small`),
  and see where the remaining Pods go.
- Scale back to 2.

##### Question: Is It a Cap

_Did the limit stop Auto Mode from launching more capacity? What would
you have to change for a NodePool limit to be a hard cost ceiling for the
cluster?_

##### Question: Burstable Instances

_The NodePool allows `t` instances. What's the catch with burstable
instances for steady workloads, and what does "unlimited" mode do to the
bill? When would Spot capacity be a better way to save money?_

### Retrospective 15.8

#### Question: Auto Mode or Not

_Auto Mode adds a per-instance fee and takes away SSH, custom AMIs and
some networking options. For which teams is that a good trade? Compare
it with managed node groups plus self-managed Karpenter, and with
Fargate, on cost, effort and control._

## Lesson 15.9: Who Can Do What

### Principle 15.9

*Two separate questions: which IAM principals may call the Kubernetes
API (access entries), and which AWS APIs a Pod may call (Pod Identity).
Both are answered with IAM roles, managed through the EKS API from
outside the cluster.*

### Practice 15.9

Before access entries, EKS mapped IAM principals to Kubernetes users in
a ConfigMap called `aws-auth` inside the cluster. A typo in it could lock
everyone out, and changes weren't in CloudTrail. Before Pod Identity,
Pods got AWS credentials through IAM roles for service accounts (IRSA),
which needs an OIDC provider and a trust policy per cluster. Read [Grant
IAM users and roles access to Kubernetes
APIs](https://docs.aws.amazon.com/eks/latest/userguide/grant-k8s-access.html)
and [Learn how EKS Pod Identity grants pods access to AWS
services](https://docs.aws.amazon.com/eks/latest/userguide/pod-identities.html).

#### Lab 15.9.1: Who Can Already Get In

- Run `aws eks list-access-entries --cluster-name <your-id>-lab15`.
  Identify each entry: your Identity Center role, and roles EKS created.
- Find your role's ARN. `aws sts get-caller-identity` shows an
  assumed-role ARN; the IAM role ARN has the path
  `/aws-reserved/sso.amazonaws.com/` (`aws iam list-roles --path-prefix
  /aws-reserved/sso.amazonaws.com/`).
- Run the following, with your role's ARN:

  ```bash
  aws eks list-associated-access-policies --cluster-name <your-id>-lab15 \
    --principal-arn <your-role-arn>
  ```

- Run `kubectl auth whoami` and `kubectl get configmap aws-auth -n
  kube-system`.

##### Question: The aws-auth ConfigMap

_Why is there no `aws-auth` ConfigMap? What could go wrong with it that
can't go wrong with access entries? If you deleted your own access entry
by mistake, how would you get back in?_

#### Lab 15.9.2: A Namespace-Scoped Viewer

- Create an IAM role named `<your-id>-lab15-viewer` that principals in
  your account can assume, with one permission: `eks:DescribeCluster` on
  your cluster (so `update-kubeconfig` works). Write it as a small
  CloudFormation template in your repository.
- Give it read-only access to the `lab15` namespace only:

  ```bash
  aws eks create-access-entry --cluster-name <your-id>-lab15 \
    --principal-arn arn:aws:iam::123456789012:role/<your-id>-lab15-viewer
  aws eks associate-access-policy --cluster-name <your-id>-lab15 \
    --principal-arn arn:aws:iam::123456789012:role/<your-id>-lab15-viewer \
    --policy-arn arn:aws:eks::aws:cluster-access-policy/AmazonEKSViewPolicy \
    --access-scope type=namespace,namespaces=lab15
  ```

- Add a profile to `~/.aws/config` that assumes the role:

  ```ini
  [profile lab-eks-viewer]
  role_arn = arn:aws:iam::123456789012:role/<your-id>-lab15-viewer
  source_profile = lab
  region = us-east-2
  ```

- Add a kubeconfig context for it:

  ```bash
  aws eks update-kubeconfig --name <your-id>-lab15 \
    --profile lab-eks-viewer --alias lab15-viewer
  ```

- As the viewer (`kubectl --context lab15-viewer ...`), try:
  `get pods -n lab15`, `get pods -n kube-system`, `delete pod <a pod> -n
  lab15`, `get secrets -n lab15` and `auth can-i --list -n lab15`.
- Switch back with `kubectl config use-context` to your admin context.

The access entry and policy could also be written as
`AWS::EKS::AccessEntry` in your template, or under `accessConfig` in
`cluster.yaml`. See [Review access policy
permissions](https://docs.aws.amazon.com/eks/latest/userguide/access-policy-permissions.html).

##### Question: Access Policy or RBAC Group

_Access policies are fixed sets of permissions. When would you instead
give the access entry a Kubernetes group and write your own `Role` and
`RoleBinding`? Which access policy would let the viewer read Secrets,
and why is that not "read-only" in practice?_

#### Lab 15.9.3: Pod Identity

- Complete `pod-identity/pod-identity.yaml` from this module: the TODOs
  ask for parameters, an IAM role that `pods.eks.amazonaws.com` can
  assume with `sts:AssumeRole` and `sts:TagSession`, read-only
  permissions on the bucket, and an
  [`AWS::EKS::PodIdentityAssociation`](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-eks-podidentityassociation.html).
  Run `cfn-lint` on it.
- Deploy it with `aws cloudformation deploy ... --capabilities
  CAPABILITY_IAM` (`CAPABILITY_NAMED_IAM` if you give the role a name). Upload a small text file to the bucket.
- In the cluster, create the service account: `kubectl create
  serviceaccount s3-reader`.
- Write a Pod manifest, `s3-reader-pod.yaml`, for a Pod that:
  - runs as service account `s3-reader`
  - uses the image `public.ecr.aws/aws-cli/aws-cli:2.36.49` with the
    command `sleep 3600`
  - sets `AWS_REGION` to `us-east-2`
  - requests `50m` CPU and `64Mi` memory
- Apply it, then:
  - `kubectl exec s3-reader -- env | grep AWS_`
  - `kubectl exec s3-reader -- aws sts get-caller-identity`
  - `kubectl exec s3-reader -- aws s3 cp s3://<bucket>/<file> -`
  - `kubectl exec s3-reader -- aws s3 ls` (lists all buckets)
- Run the same Pod with the `default` service account under another
  name, and try the `s3 cp` again.

##### Question: Where the Pod's Credentials Come From

_Which environment variables did EKS add, and what does each point at?
Who called STS, and what did the session tags say (look for the
`AssumeRoleForPodIdentity` and `AssumeRole` events in CloudTrail)? Why
did `aws s3 ls` fail?_

##### Question: Pods Created Too Early

_What happens to a Pod that was already running before its service
account got an association? Why?_

#### Lab 15.9.4: Tighten the Trust Policy

Any service account associated with the role can use it. Restrict the
role itself to your namespace and service account.

- Add a `Condition` to the trust policy on
  `aws:RequestTag/kubernetes-namespace` and
  `aws:RequestTag/kubernetes-service-account`. See [Create IAM role with
  trust policy required by EKS Pod
  Identity](https://docs.aws.amazon.com/eks/latest/userguide/pod-id-role.html)
  and [Grant Pods access to AWS resources based on
  tags](https://docs.aws.amazon.com/eks/latest/userguide/pod-id-abac.html).
  Update the stack.
- Create a second service account, `other`, and a second association
  that maps it to the same role (`aws eks
  create-pod-identity-association`). Run a Pod as `other` and try the
  `s3 cp`.
- Delete the second association when you're done.

##### Question: Two Places to Say No

_The association says which service account gets the role; the trust
policy says who may assume it. Why have both? Who in an organization
would own each?_

### Retrospective 15.9

#### Question: Pod Identity or IRSA

_Read [Grant Kubernetes workloads access to AWS using Kubernetes Service
Accounts](https://docs.aws.amazon.com/eks/latest/userguide/service-accounts.html).
Compare Pod Identity with IAM roles for service accounts: what each
needs per cluster, what the trust policy looks like, what happens when
you move a workload to a new cluster, and where each doesn't work (hint:
Fargate). Which would you pick for a new Auto Mode cluster?_

#### Question: Another Account

_A Pod needs to read a bucket in a different AWS account. How would you
do it with Pod Identity, and what does the association's
`targetRoleArn` do?_

## Lesson 15.10: Tearing It Down

### Principle 15.10

*Delete from the inside out: first what Kubernetes created in AWS, then
the cluster, then what you created around it. Then check, because
leftovers keep billing.*

### Practice 15.10

The cluster created resources through three different owners:
Kubernetes controllers (load balancers, target groups, security group
rules, network interfaces, volumes), eksctl's CloudFormation stacks (VPC,
roles, cluster) and your own stacks (ECR, Pod Identity, viewer role).
Each owner has to delete its own, in that order. Read [Delete a
cluster](https://docs.aws.amazon.com/eks/latest/userguide/delete-cluster.html).

#### Lab 15.10.1: Remove What Kubernetes Created

- Note the cluster's VPC ID:

  ```bash
  aws eks describe-cluster --name <your-id>-lab15 \
    --query "cluster.resourcesVpcConfig.vpcId"
  ```

- List Services with an external address: `kubectl get svc -A`. Delete
  every Service of type `LoadBalancer`.
- List Ingresses (`kubectl get ingress -A`) and persistent volume claims
  (`kubectl get pvc -A`) and delete any you created.
- Delete your NodePool: `kubectl delete -f k8s/nodepool-lab.yaml`.
- Delete the namespace: `kubectl delete namespace lab15`.
- Wait until no load balancer remains in the cluster's VPC:

  ```bash
  aws elbv2 describe-load-balancers \
    --query "LoadBalancers[?VpcId=='vpc-0123456789abcdef0'].[LoadBalancerName,State.Code]"
  ```

#### Lab 15.10.2: Delete the Cluster and Your Stacks

- Delete the cluster: `eksctl delete cluster -f cluster.yaml --wait`.
  It deletes the cluster, which takes its Auto Mode nodes, access entries
  and Pod Identity associations with it, and then eksctl's stacks.
- Delete your own stacks:
  - the Pod Identity stack: empty the bucket first (`aws s3 rm
    s3://<bucket> --recursive`), then `aws cloudformation delete-stack`.
    Its association went with the cluster, so CloudFormation may report
    it already deleted.
  - the viewer role stack
  - the ECR stack (`EmptyOnDelete` removes the images)
- Remove the local configuration: the `lab-eks-viewer` profile in
  `~/.aws/config`, and the contexts, clusters and users for the lab
  cluster in `~/.kube/config` (`kubectl config get-contexts`, then
  `kubectl config delete-context`, `delete-cluster` and `delete-user`).

#### Lab 15.10.3: Verify Nothing Is Left

Run each check and expect empty output. `--include-managed-resources`
makes EC2 list resources that Auto Mode created even when managed
resources are hidden.

```bash
aws eks list-clusters
aws cloudformation list-stacks \
  --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE DELETE_FAILED ROLLBACK_COMPLETE \
  --query "StackSummaries[?contains(StackName,'lab15')].[StackName,StackStatus]"
aws elbv2 describe-load-balancers --query "LoadBalancers[].[LoadBalancerName,VpcId]"
aws elbv2 describe-target-groups --query "TargetGroups[].[TargetGroupName,VpcId]"
aws ec2 describe-instances --include-managed-resources \
  --filters Name=instance-state-name,Values=pending,running,stopping,stopped \
  --query "Reservations[].Instances[].[InstanceId,Operator.Principal]"
aws ec2 describe-network-interfaces --include-managed-resources \
  --filters Name=status,Values=available \
  --query "NetworkInterfaces[].[NetworkInterfaceId,Description]"
aws ec2 describe-volumes --include-managed-resources \
  --filters Name=status,Values=available \
  --query "Volumes[].[VolumeId,Size,CreateTime]"
aws ec2 describe-nat-gateways --filter Name=state,Values=pending,available \
  --query "NatGateways[].[NatGatewayId,VpcId]"
aws ec2 describe-addresses --query "Addresses[].[PublicIp,AllocationId,AssociationId]"
aws ec2 describe-vpcs --filters Name=tag:alpha.eksctl.io/cluster-name,Values=<your-id>-lab15
aws iam list-roles --query "Roles[?contains(RoleName,'lab15')].RoleName"
aws logs describe-log-groups --log-group-name-prefix /aws/eks/<your-id>-lab15
aws ecr describe-repositories --query "repositories[].repositoryName"
aws resourcegroupstaggingapi get-resources --tag-filters Key=topic,Values=15 \
  --query "ResourceTagMappingList[].ResourceARN"
```

Anything left over:

- A load balancer or target group from the cluster: delete it with
  `aws elbv2 delete-load-balancer` / `delete-target-group`, then any
  security group it used.
- A stack in `DELETE_FAILED`: read its events
  (`aws cloudformation describe-stack-events`) to find the resource that
  blocked it, usually a security group or subnet still used by an
  orphaned network interface, delete that, and delete the stack again.
- An `available` volume or network interface you can tie to the cluster
  (check its tags and description): delete it.
- The tagging API can show resources that were deleted recently; confirm
  each one before you worry.

Finally, if you changed the managed resource visibility setting in Lab
15.1.1, set it back.

##### Question: Orphans

_Suppose you'd run `aws eks delete-cluster` straight away, with the
Service still in place, on a cluster that used the self-managed AWS Load
Balancer Controller instead of Auto Mode. What would have been left
behind, what would it cost, and why would the VPC stack fail to delete?_

### Retrospective 15.10

#### Question: Guardrails

_This lesson relied on you remembering to clean up. What would catch a
forgotten cluster automatically? Consider the budget alert from module
00, a scheduled check for EKS clusters older than a day, a tag-based
cleanup tool such as the one in module 19, and an SCP that limits
instance types in the lab account._

## Further Reading

- [Amazon EKS Best Practices
  Guide](https://docs.aws.amazon.com/eks/latest/best-practices/introduction.html):
  security, reliability, networking, cost optimization and Auto Mode
  sections.
- [Amazon EKS workshop](https://www.eksworkshop.com/) for guided labs on
  autoscaling, observability, networking and GitOps.
- [Karpenter documentation](https://karpenter.sh/docs/) explains the
  NodePool and disruption behavior Auto Mode is built on.
- [Helm](https://helm.sh/docs/intro/quickstart/) is the most common way to
  package and install applications on Kubernetes.
- [Kubernetes The Hard
  Way](https://github.com/kelseyhightower/kubernetes-the-hard-way) builds
  a cluster by hand, which teaches what EKS is doing for you.
- The [CNCF curriculum](https://github.com/cncf/curriculum) for the CKA and
  CKAD exams, if you want the Kubernetes skills this module leaves out.
