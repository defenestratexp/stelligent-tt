# Topic 17: Terraform

<!-- TOC -->

- [Topic 17: Terraform](#topic-17-terraform)
  - [What changed in the 2026 edition](#what-changed-in-the-2026-edition)
  - [Exam coverage](#exam-coverage)
  - [Cost and cleanup](#cost-and-cleanup)
  - [Guidance](#guidance)
  - [Conventions](#conventions)
  - [Lesson 17.1: Introduction to Terraform](#lesson-171-introduction-to-terraform)
    - [Principle 17.1](#principle-171)
    - [Practice 17.1](#practice-171)
      - [Lab 17.1.1: Toolchain and language features](#lab-1711-toolchain-and-language-features)
      - [Lab 17.1.2: Resources, data sources and variables](#lab-1712-resources-data-sources-and-variables)
    - [Retrospective 17.1](#retrospective-171)
  - [Lesson 17.2: Getting started and Terraform state](#lesson-172-getting-started-and-terraform-state)
    - [Principle 17.2](#principle-172)
    - [Practice 17.2](#practice-172)
      - [Lab 17.2.1: Terraform quickstart](#lab-1721-terraform-quickstart)
      - [Lab 17.2.2: Remote state in S3](#lab-1722-remote-state-in-s3)
      - [Lab 17.2.3: State locking without DynamoDB](#lab-1723-state-locking-without-dynamodb)
    - [Retrospective 17.2](#retrospective-172)
  - [Lesson 17.3: Environments, variables and plan review](#lesson-173-environments-variables-and-plan-review)
    - [Principle 17.3](#principle-173)
    - [Practice 17.3](#practice-173)
      - [Lab 17.3.1: Workspaces and separate state](#lab-1731-workspaces-and-separate-state)
      - [Lab 17.3.2: Variables, validation and tfvars files](#lab-1732-variables-validation-and-tfvars-files)
      - [Lab 17.3.3: Saved plans and plan review](#lab-1733-saved-plans-and-plan-review)
      - [Lab 17.3.4: Further network changes](#lab-1734-further-network-changes)
    - [Retrospective 17.3](#retrospective-173)
  - [Lesson 17.4: Using Terraform modules](#lesson-174-using-terraform-modules)
    - [Principle 17.4](#principle-174)
    - [Practice 17.4](#practice-174)
      - [Lab 17.4.1: Creating and using a local module](#lab-1741-creating-and-using-a-local-module)
      - [Lab 17.4.2: A module from the registry](#lab-1742-a-module-from-the-registry)
      - [Lab 17.4.3: Module versioning](#lab-1743-module-versioning)
    - [Retrospective 17.4](#retrospective-174)
  - [Lesson 17.5: Guardrails and tests](#lesson-175-guardrails-and-tests)
    - [Principle 17.5](#principle-175)
    - [Practice 17.5](#practice-175)
      - [Lab 17.5.1: Preconditions and postconditions](#lab-1751-preconditions-and-postconditions)
      - [Lab 17.5.2: Check blocks](#lab-1752-check-blocks)
      - [Lab 17.5.3: terraform test](#lab-1753-terraform-test)
    - [Retrospective 17.5](#retrospective-175)
  - [Lesson 17.6: Changing what already exists](#lesson-176-changing-what-already-exists)
    - [Principle 17.6](#principle-176)
    - [Practice 17.6](#practice-176)
      - [Lab 17.6.1: Import blocks](#lab-1761-import-blocks)
      - [Lab 17.6.2: Moved blocks](#lab-1762-moved-blocks)
      - [Lab 17.6.3: Removed blocks and drift](#lab-1763-removed-blocks-and-drift)
      - [Lab 17.6.4: Clean up the module](#lab-1764-clean-up-the-module)
    - [Retrospective 17.6](#retrospective-176)
  - [Further Reading](#further-reading)

<!-- /TOC -->

## What changed in the 2026 edition

- **Terraform 1.11 or later.** The 2022 module asked for 0.12. Every
  snippet here has been checked with `terraform fmt` and `terraform
  validate` on Terraform 1.11 and on the current release, with version
  6 of the AWS provider.
- **Provider versions go in `required_providers`.** The old quickstart
  put `version = "~> 2.0"` inside the `provider "aws"` block. That
  argument is deprecated; versions now live in a `terraform {}` block,
  and the dependency lock file (`.terraform.lock.hcl`) records exactly
  what `init` installed.
- **Fixed invalid syntax.** The old `data "aws_vpc"` example used a
  `tags { ... }` block. `tags` is an argument that takes a map, so it's
  `tags = { ... }`.
- **No hard-coded AMIs.** The `aws_instance` example reads Amazon Linux
  2023 from the SSM public parameter instead of using `ami-1234567890`,
  uses `t3.micro` and requires IMDSv2.
- **State locking without DynamoDB.** Since Terraform 1.11 the S3 backend
  locks state with a lock file in the same bucket (`use_lockfile =
  true`), using S3 conditional writes. The DynamoDB arguments are
  deprecated. Lab 17.2.3 no longer creates a lock table.
- **One resource per S3 bucket setting.** Since version 4 of the AWS
  provider, versioning, encryption and public access are separate
  resources (`aws_s3_bucket_versioning` and friends), not arguments of
  `aws_s3_bucket`.
- **Workspaces are introduced as one option, not the default.** The old
  quickstart told you never to use the `default` workspace. HashiCorp's
  own docs now say workspaces don't suit environments that need separate
  credentials or access controls; Lesson 17.3 compares workspaces with
  separate state.
- **New Lesson 17.5, guardrails and tests:** variable validation,
  preconditions and postconditions, `check` blocks, and `terraform test`
  with a mocked AWS provider.
- **New Lesson 17.6, changing what already exists:** `import` blocks,
  `moved` blocks, `removed` blocks and drift with `-refresh-only`, then a
  cleanup lab that removes the versioned state bucket.
- **Licence and OpenTofu.** Terraform 1.6 and later is under the
  Business Source License 1.1, not MPL 2.0. OpenTofu is the open-source
  fork (MPL 2.0, a CNCF sandbox project). Practice 17.1 explains what
  that means for you.
- **CDK for Terraform (CDKTF) was archived in December 2025.** If you
  want to write infrastructure in a general-purpose language, see the AWS
  CDK (module 25); this module sticks to HCL.
- **AWS provider 6 adds a `region` argument to most resources**, so a
  single provider configuration can manage several Regions. The labs use
  one Region, `us-east-2`.
- Links point to `developer.hashicorp.com` and the Terraform Registry;
  the old `terraform.io/docs` paths redirect or no longer exist.

## Exam coverage

| Exam | Domain / task statement |
|---|---|
| SOA-C03 | Domain 3: Deployment, Provisioning, and Automation (Skill 3.1.6: use and manage third-party tools to automate resource deployment, for example Terraform and Git; Skill 3.1.3: identify and remediate deployment issues) |
| DOP-C02 | Domain 2: Configuration Management and IaC (Task 2.1: define cloud infrastructure and reusable components to provision and manage systems throughout their lifecycle) |
| DOP-C02 | Domain 1: SDLC Automation (Task 1.1: implement CI/CD pipelines; Task 1.2: integrate automated testing into CI/CD pipelines) |

Terraform itself is named only in the CloudOps guide. The DevOps
Professional exam asks about CloudFormation and the CDK, but the ideas
this module drills (state, drift, previewing a change, reusable
components, testing infrastructure code in a pipeline) are the same.

## Cost and cleanup

This module is cheap if you follow the labs as written.

- **The state bucket** costs cents a month. It's versioned, so every
  `apply` and every lock leaves an old version behind; Lab 17.2.3 adds a
  lifecycle rule so they don't pile up.
- **VPCs, subnets, route tables and internet gateways are free.** The
  labs don't create NAT gateways, load balancers or instances. If you
  add a NAT gateway or an instance with a public IPv4 address while
  experimenting, both are billed by the hour; destroy them the same day.
- **Lab 17.1.2 and Lab 17.4.2 are plan-only.** The `aws_instance` in
  Lab 17.1.2 and the registry VPC module in Lab 17.4.2 are there to read
  a plan, not to apply.
- **`terraform test` with a mocked provider creates nothing in AWS.**
  A test file without mocks does create and then destroy real resources.
- **Terraform does not roll back.** A failed `apply` leaves whatever it
  had created in place, recorded in state. Destroy from the same
  directory and workspace, or you'll have resources no state file knows
  about.
- **Cleanup:** [Lab 17.6.4](#lab-1764-clean-up-the-module) destroys
  every configuration and workspace, deletes the buckets you created
  outside Terraform, then removes the state bucket, including every
  object version and delete marker.

## Guidance

- Explore the official docs! See the
  [Terraform documentation](https://developer.hashicorp.com/terraform/docs),
  the [Terraform language
  reference](https://developer.hashicorp.com/terraform/language),
  and the [AWS provider
  docs](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
  in the Terraform Registry.

- AWS publishes its own [best practices for using the Terraform AWS
  provider](https://docs.aws.amazon.com/prescriptive-guidance/latest/terraform-aws-provider-best-practices/introduction.html)
  (AWS Prescriptive Guidance). Skim it now; several questions come from it.

- Avoid using other sites like stackoverflow.com for answers \-- part
  of the skill set you're building is finding answers straight from
  the Terraform docs.

- Watch the dates on what you read. A tutorial that puts `version` in a
  `provider` block, sets `acl = "private"` on `aws_s3_bucket` or creates
  a DynamoDB lock table was written for an older Terraform or provider.

- Explore your curiosity. Try to understand why things work the way
  they do. Read more of the documentation than just what you need to
  find the answers.

## Conventions

- **Profile and Region.** Everything runs in the lab account in
  `us-east-2` with the `lab` profile. The provider and backend blocks in
  this module set `profile = "lab"`; if you'd rather keep profiles out of
  code, delete that line and `export AWS_PROFILE=lab` in each shell
  instead. Don't do both with different values.
- **Placeholders.** Examples use `123456789012` for the lab account and
  `<you>` for your identifier. Keep real account IDs out of your
  repository.
- **Names and tags** include your identifier. Every configuration sets
  `default_tags` on the provider with `owner = "<you>"` and `topic =
  "17"`, so Lab 17.6.4 can find what's left.
- **Your repository.** Keep your code in `17-terraform/` of your lab
  repository. Commit your `.tf` files and each root configuration's
  `.terraform.lock.hcl`. Never commit `.terraform/`, `*.tfstate`,
  `*.tfstate.backup`, saved plan files or `.tfvars` files that hold
  secrets. Add a `.gitignore` before your first `terraform init`.

## Lesson 17.1: Introduction to Terraform

### Principle 17.1

*Terraform compares the configuration you write with the state it
recorded last time and with what's really there, and makes the API calls
to close the gap. There is no service on the other end holding your
stack: the state is yours to keep.*

### Practice 17.1

[Terraform](https://developer.hashicorp.com/terraform/docs) is an
infrastructure-as-code tool from HashiCorp (an IBM company since 2025).
You write configuration in HCL; **providers** turn it into API calls. The
AWS provider is one of thousands, which is why teams that manage AWS
alongside a DNS provider, GitHub, a monitoring SaaS or another cloud
tend to pick Terraform. It doesn't make moving between clouds easy (an
`aws_vpc` isn't a `google_compute_network`), but it gives you one tool
and one workflow for all of them.

**Licence and OpenTofu.** Terraform was MPL 2.0 open source until
August 2023. Terraform 1.6 and later is released under the [Business
Source License
1.1](https://github.com/hashicorp/terraform/blob/main/LICENSE), which
allows production use by anyone except in a product that competes with
HashiCorp's paid offerings. In response, a group of vendors forked
Terraform 1.5 as [OpenTofu](https://opentofu.org/docs/), now under the
Linux Foundation and accepted into the [CNCF as a sandbox
project](https://www.cncf.io/projects/opentofu/) in April 2025. The
`tofu` CLI reads the same `.tf` files and uses the same providers, and
everything in this module works with either, with one difference worth
knowing: OpenTofu can encrypt state and plan files itself, with a key
from AWS KMS among others ([state
encryption](https://opentofu.org/docs/language/state/encryption/)). The
two have diverged since the fork, so check before assuming a feature
from one exists in the other. The labs say `terraform`; if you use
OpenTofu, substitute `tofu`.

You have now met, or will meet, three ways to write infrastructure as
code in this course. Module 25 has the same table from the CDK's side;
this one adds the rows that matter most when Terraform is the tool.

| | CloudFormation (module 01) | AWS CDK (module 25) | Terraform (this module) |
|---|---|---|---|
| You write | YAML templates | Python (or TypeScript, Java, C#, Go) that synthesizes templates | HCL (or JSON) |
| Deployment engine | CloudFormation | CloudFormation | Terraform CLI calling AWS APIs through a provider |
| Where state lives | The stack, inside CloudFormation | The stack, inside CloudFormation | A state file you store, lock and protect (S3 with `use_lockfile`) |
| Locking | CloudFormation serializes updates to a stack | Same as CloudFormation | The backend's lock (a `.tflock` object in S3) |
| Preview a change | Change set | `cdk diff` (creates a change set) | `terraform plan`, saved with `-out` and applied as is |
| When an apply fails | Rolls back to the last good state | Same as CloudFormation | Stops; what was created stays and is in state. Fix and re-apply |
| Reuse | Nested stacks, modules, macros | Constructs published as libraries | Modules from a registry, Git or a local path |
| Bring existing resources in | Resource import, IaC generator | `cdk import`, `cdk migrate` | `import` blocks, with `-generate-config-out` |
| Find drift | Drift detection | `cdk drift` | `terraform plan -refresh-only` |
| Rename without replacing | Stack refactoring | `cdk refactor` | `moved` blocks |
| Stop managing without deleting | `DeletionPolicy: Retain`, then remove | `RemovalPolicy.RETAIN`, `cdk orphan` | `removed` blocks with `destroy = false` |
| Unit tests | cfn-lint and Guard check the template | `aws_cdk.assertions` against the synthesized template | `terraform test`, with mocked providers |
| Runtime assertions | Hooks, Config rules | Same, plus aspects at synth time | `check` blocks, preconditions and postconditions |
| Secrets | Dynamic references, never stored in the template | Same as CloudFormation | Stored in state in plain text unless the argument is write-only or ephemeral |
| Other providers | Registry extensions (third-party resource types) | Same as CloudFormation | Thousands of providers; the main reason teams choose it |
| Per-account setup | None | `cdk bootstrap` once per account and Region | A state bucket |
| Licence | AWS service | Apache 2.0 | BSL 1.1 (OpenTofu fork: MPL 2.0) |

#### Lab 17.1.1: Toolchain and language features

- Install Terraform 1.11 or later from the [install
  page](https://developer.hashicorp.com/terraform/install) and run
  `terraform version`. If you use a version manager such as `tfenv`, or
  OpenTofu, note which. Pin the version you use in a `.terraform-version`
  file or in your notes; later labs assume at least 1.11.

- Run `terraform -help` and skim the command list. You'll use `init`,
  `fmt`, `validate`, `plan`, `apply`, `destroy`, `show`, `state`,
  `workspace`, `console` and `test` in this module.

- Read [Types and
  values](https://developer.hashicorp.com/terraform/language/expressions/types).
  In brief:
  - primitive types: `string`, `number` (no separate int and float) and
    `bool`;
  - collection types, whose elements all share one type: `list` (ordered,
    `my_list[0]`), `map` (`my_map["key"]`) and `set` (unordered, no index;
    `toset()` turns a list into one);
  - structural types, whose attributes can differ: `object` and `tuple`;
  - `null`, which means "leave this argument unset".

- Skim the [built-in
  functions](https://developer.hashicorp.com/terraform/language/functions).
  There are too many to learn, and you'll come back when you need one.
  Providers can now ship their own functions too, but you still can't
  define functions in HCL.

- Terraform has three ways to make many of something:
  - `count` makes a *list* of resources. If an item in the middle
    goes away, every later index shifts, and Terraform plans to replace
    them.
  - `for_each` makes a *map* of resources keyed by strings you choose,
    from a map or a set of strings. Removing one key touches only that
    resource.
  - `for` expressions build lists and maps from other collections, much
    like a Python comprehension.

- String interpolation uses `${}`:

  ```hcl
  greeting = "Hello ${var.world}"
  ```

- Start `terraform console` in an empty directory and try some of this:
  `cidrsubnet("10.0.0.0/20", 4, 1)`, `[for s in ["a", "b"] : upper(s)]`,
  `{ for i, az in ["us-east-2a", "us-east-2b"] : az => i }`,
  `toset(["a", "a", "b"])`, `type(1)`.

##### Question: count or for_each

_You create three subnets with `count` from a list of AZs, then remove
the first AZ from the list. What does the plan say? What does the same
change do with `for_each`? When is `count` still the right choice?_

#### Lab 17.1.2: Resources, data sources and variables

Work in a directory named `language` in `17-terraform/`. You'll write a
few blocks, run `terraform init` and `terraform plan`, read the plan,
and apply nothing.

- Start with a `terraform` block and a provider configuration. The
  `terraform` block says which Terraform and which providers this
  configuration needs; the `provider` block configures the provider.

  ```hcl
  terraform {
    required_version = ">= 1.11"

    required_providers {
      aws = {
        source  = "hashicorp/aws"
        version = "~> 6.0"
      }
    }
  }

  provider "aws" {
    region  = "us-east-2"
    profile = "lab"

    default_tags {
      tags = {
        owner = "<you>"
        topic = "17"
      }
    }
  }
  ```

  Read [Provider
  requirements](https://developer.hashicorp.com/terraform/language/providers/requirements).
  What does `~> 6.0` allow, and what would `~> 6.10.0` allow?

- **Resources** create infrastructure. The resource type and name
  together must be unique, and are how you refer to the resource
  elsewhere: `aws_instance.web.id` is the instance ID once it exists.
  The provider docs list each resource's arguments and the attributes it
  exports.

- **Data sources** read something that already exists. Their arguments
  act as filters, and most must match exactly one object. The AMI comes
  from the SSM public parameter, never a hard-coded ID:

  ```hcl
  data "aws_ssm_parameter" "al2023" {
    name = "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64"
  }

  resource "aws_instance" "web" {
    ami           = data.aws_ssm_parameter.al2023.value
    instance_type = "t3.micro"

    metadata_options {
      http_tokens = "required"
    }
  }
  ```

  A data source that filters by tags takes a map:

  ```hcl
  data "aws_vpc" "shared" {
    tags = {
      Name        = "my-public-vpc"
      Environment = "production"
    }
  }
  ```

  You'd use its ID as `data.aws_vpc.shared.id`. There's no such VPC in
  your account, so leave this one commented out unless you create one.

- **Input variables** are the configuration's parameters, like
  CloudFormation parameters. Reference them as `var.<name>`:

  ```hcl
  variable "team_name" {
    type        = string
    description = "Team that owns these resources."
    default     = "Stelligent"
  }
  ```

  Don't make the Region a variable with a default of its own; the
  profile or provider block already says where you are.

- **Local values** name an expression so you write it once:

  ```hcl
  locals {
    name_prefix = "stelligent-u-17-${var.team_name}"
  }
  ```

- **Outputs** expose values to the person running Terraform, to other
  configurations and to modules that call this one. Add an output for the
  AMI ID you looked up. Terraform marks SSM parameter values sensitive,
  so you'll need `sensitive = true` on the output, or `nonsensitive()`
  around the value; decide which is right for an AMI ID.

- Run `terraform init`, `terraform fmt`, `terraform validate` and
  `terraform plan`. Read the plan: which values are known now and which
  say `(known after apply)`? Don't apply. Delete the `aws_instance` when
  you're done reading.

##### Question: Plan without apply

_`terraform plan` needed your AWS credentials even though it created
nothing. What did it call AWS for? Which of the commands you ran worked
without credentials?_

### Retrospective 17.1

#### Question: Default Minimum Module Files

_What are the recommended files for a minimum Terraform module? Read
[Standard module
structure](https://developer.hashicorp.com/terraform/language/modules/develop/structure)
and the [style
guide](https://developer.hashicorp.com/terraform/language/style). Which
of those files did you just write, and where do `terraform` and
`provider` blocks belong?_

## Lesson 17.2: Getting started and Terraform state

### Principle 17.2

*State is Terraform's memory of what it manages. Keep it remote,
versioned, encrypted, locked, and readable only by the people and
pipelines that run Terraform.*

### Practice 17.2

Terraform records every object it manages, and the attributes it read
back, in a JSON state file. With no backend configured, that file is
`terraform.tfstate` next to your code. In these labs you'll create an S3
bucket with local state, move the state into that bucket, and watch the
S3 backend lock it. Read the [S3 backend
docs](https://developer.hashicorp.com/terraform/language/backend/s3)
before you start.

#### Lab 17.2.1: Terraform quickstart

- In `17-terraform/`, create a directory named `state-management` and a
  `main.tf` with the `terraform` and `provider` blocks from Lab 17.1.2.

- Using the AWS provider docs, write the code for an S3 bucket named
  `stelligent-u-17-<you>-tfstate` with:
  - versioning enabled (`aws_s3_bucket_versioning`);
  - Block Public Access on, all four settings
    (`aws_s3_bucket_public_access_block`). New buckets already have it,
    but saying so in code means Terraform will notice if someone turns
    it off;
  - default encryption. New buckets use SSE-S3 already; use SSE-KMS with
    the `aws/s3` key or your own key only if you've done module 10 and
    want to (`aws_s3_bucket_server_side_encryption_configuration`).

  Don't set `acl` on the bucket: ACLs are disabled on new buckets.

- Run `terraform init` and read what it did. Open
  `.terraform.lock.hcl`: what's recorded in it, and why should it be
  committed?

- Run `terraform plan`, then `terraform apply`. Terraform shows the plan
  again and waits for `yes`.

- Confirm the bucket with the CLI: `aws s3api get-bucket-versioning
  --bucket stelligent-u-17-<you>-tfstate`.

#### Lab 17.2.2: Remote state in S3

- Look at `terraform.tfstate`. It's JSON. Find the bucket, its
  attributes, the `serial` and the `lineage`. Run `terraform state list`
  and `terraform state show aws_s3_bucket_versioning.<name>`.

- Keeping state on a laptop is fine for a spike, but nobody else can
  see it, and committing it to Git means secrets in Git and state that's
  always one commit behind. Add a backend to the `terraform` block in
  `main.tf`:

  ```hcl
  terraform {
    backend "s3" {
      bucket       = "stelligent-u-17-<you>-tfstate"
      key          = "state-management/terraform.tfstate"
      region       = "us-east-2"
      profile      = "lab"
      encrypt      = true
      use_lockfile = true
    }
  }
  ```

  Backend blocks can't use variables or locals; every value is literal
  or passed with `terraform init -backend-config=...`.

- Run `terraform init -migrate-state` and answer `yes` when it asks to
  copy the state into S3.

- Look at the local `terraform.tfstate` now, and at
  `terraform.tfstate.backup`. Download the state object from S3 with
  `aws s3 cp` and compare it with the backup. Then delete both local
  files: from now on, S3 has the only copy, and bucket versioning is
  your backup.

##### Question: State Management

_Your state now lives in the bucket that the state describes. What could
go wrong with that? What protects you if someone runs `terraform
destroy` in this directory?_

##### Question: Secrets

_Read [Manage sensitive data in your
configuration](https://developer.hashicorp.com/terraform/language/manage-sensitive-data).
If a configuration creates a database with a password, where does the
password end up? What do `sensitive = true`, a customer managed KMS key
on the backend (`kms_key_id`), [ephemeral
resources](https://developer.hashicorp.com/terraform/language/resources/ephemeral)
and [write-only
arguments](https://developer.hashicorp.com/terraform/language/resources/ephemeral/write-only)
each change? Which of them keeps the password out of state?_

#### Lab 17.2.3: State locking without DynamoDB

Remote state stops people working from different copies, but two runs
at the same moment can still both read the state, both change things,
and the last one to write wins. A **lock** makes the second run wait or
fail.

Until Terraform 1.10, the S3 backend needed a DynamoDB table for
locking. Terraform 1.11 made **S3 native locking** generally available:
with `use_lockfile = true`, Terraform writes `<key>.tflock` next to the
state with an S3 [conditional
write](https://docs.aws.amazon.com/AmazonS3/latest/userguide/conditional-writes.html)
that succeeds only if the object doesn't already exist, and deletes it
when it's done. The DynamoDB arguments (`dynamodb_table`) are deprecated;
if you're migrating an existing backend, you can set both while
everyone upgrades, then remove the table.

You enabled the lock file in Lab 17.2.2. Now watch it work.

- In one terminal, change something small (add a tag to the bucket) and
  run `terraform apply`. Leave it waiting at the `yes` prompt.

- In a second terminal, in the same directory, run `terraform plan`.
  Read the error: who holds the lock, since when, and the lock ID.

- While the first terminal is still waiting, list the objects next to
  the state: `aws s3api list-objects-v2 --bucket
  stelligent-u-17-<you>-tfstate --prefix state-management/`. Download
  the `.tflock` object and read it.

- In the second terminal, run `terraform plan -lock-timeout=2m`, then
  answer `yes` in the first. What happens to the second run?

- Read [`terraform
  force-unlock`](https://developer.hashicorp.com/terraform/cli/commands/force-unlock).
  Don't run it now; write down when it's safe to.

- The bucket is versioned, so every lock and every state write leaves a
  noncurrent version, and every lock release leaves a delete marker. List
  them with `aws s3api list-object-versions`. Add an
  `aws_s3_bucket_lifecycle_configuration` that expires noncurrent
  versions after 90 days and removes expired delete markers. Keep enough
  history to recover from a bad apply; decide how much that is.

- Check the IAM side: the backend docs list the permissions a role needs
  on the state object and on the lock file. Which extra action does the
  lock file need that the state file doesn't?

##### Question: State Issues

_Do you think using Terraform to bootstrap and manage its own state
bucket is a problem? Why or why not? How else could the bucket be
created (think module 01, or module 19's account baseline)?_

##### Question: Why not DynamoDB

_The DynamoDB table was one more resource to create, pay for, protect
and clean up. What else did moving the lock into S3 change? Think about
IAM permissions, encryption of the lock, and what a stale lock looks
like._

### Retrospective 17.2

#### Question: Terraform State Security

_Is any sensitive data stored in the Terraform state file? If so, what
steps should you take to ensure the file is secure? Write the bucket
policy and IAM policy you'd want in a real account: who can read state,
who can write it, and who can delete old versions?_

## Lesson 17.3: Environments, variables and plan review

### Principle 17.3

*Split state by blast radius, and apply the plan you reviewed, not a
fresh one.*

### Practice 17.3

Everything in one state file means one mistake can reach everything, and
every plan has to refresh everything. You'll build a small network in a
`dev` directory, run it twice with workspaces, compare that with keeping
environments in separate directories and state keys, then tighten the
workflow with variable validation and saved plans.

#### Lab 17.3.1: Workspaces and separate state

- In `17-terraform/`, next to `state-management`, create `dev/network`
  and `prod/network`.

- Using the AWS provider docs, write a VPC with two private subnets in
  `dev/network/main.tf`. Take the VPC CIDR and the list of availability
  zones as variables (defaults are fine for now). Use `for_each` to make
  one subnet per AZ, and the
  [`cidrsubnet`](https://developer.hashicorp.com/terraform/language/functions/cidrsubnet)
  function to calculate each subnet's CIDR. If `for_each` gets you stuck
  for too long, use `count` and come back to it.

- Copy the `terraform` and `provider` blocks from `state-management`,
  and change the backend `key` to `dev/network/terraform.tfstate`.

- Run `terraform init`, then `terraform workspace list`. Create a
  workspace (`terraform workspace new blue`) and apply.

- Create a second workspace (`green`), change the CIDR default so the
  VPCs don't overlap, and apply again.

- List the bucket. Where did the two workspaces' state go? Read the
  `workspace_key_prefix` argument in the backend docs. Use
  `terraform.workspace` in a `Name` tag so you can tell the VPCs apart.

- Now read [Workspaces](https://developer.hashicorp.com/terraform/cli/workspaces),
  especially the note on when workspaces aren't appropriate. The
  alternative is what you already did with `state-management` and
  `dev/network`: a directory, and so a state key, per environment and
  per component, each with its own backend configuration and possibly its
  own account and role.

##### Question: Workspaces

_Are workspaces alone sufficient to separate dev environments from prod
environments? Why or why not? Where would each approach put the IAM
boundary between dev and prod, and what happens to each if prod lives in
a different AWS account?_

#### Lab 17.3.2: Variables, validation and tfvars files

- Move your variable declarations into `variables.tf`. Run `terraform
  plan` to confirm nothing changes.

- Give every variable a `type` and a `description`, and remove the
  defaults from the ones that differ between environments.

- Add [validation](https://developer.hashicorp.com/terraform/language/validate)
  so a bad value fails at plan time with a message you wrote. For
  example:

  ```hcl
  variable "vpc_cidr" {
    type        = string
    description = "CIDR block for the lab VPC."

    validation {
      condition     = can(cidrhost(var.vpc_cidr, 0)) && tonumber(split("/", var.vpc_cidr)[1]) <= 24
      error_message = "vpc_cidr must be a valid IPv4 CIDR block of /24 or larger."
    }
  }
  ```

  Add one more rule of your own (for example, that there are at least two
  AZs, or that an `env` variable is one of `dev` or `prod`). Since
  Terraform 1.9 a validation can refer to other variables too.

- Create `blue.tfvars` and `green.tfvars` with a unique CIDR in each.
  A `.tfvars` file only sets values, it doesn't declare them:

  ```hcl
  vpc_cidr = "10.10.0.0/20"
  ```

  Run `terraform plan -var-file=blue.tfvars` in the `blue` workspace.
  Then try an invalid CIDR and read the error.

##### Question: Validation or precondition

_Your validation can check that a CIDR is well formed. Could it check
that the CIDR doesn't overlap another VPC in the account? What would
you use instead (look ahead to Lesson 17.5)?_

#### Lab 17.3.3: Saved plans and plan review

`terraform plan` shows what Terraform would do now. By the time you run
`terraform apply`, someone may have changed the code or the
infrastructure, and a plain `apply` plans again. A **saved plan**
(`terraform plan -out=tfplan`) records exactly what was reviewed, and
`terraform apply tfplan` applies that and nothing else, refusing if the
state has changed since. Read the
[`plan`](https://developer.hashicorp.com/terraform/cli/commands/plan) and
[`show`](https://developer.hashicorp.com/terraform/cli/commands/show)
command references.

In the language of your choice, write a script that:

- takes a workspace name and `plan` or `apply`;
- selects the workspace and warns if `<workspace>.tfvars` doesn't exist;
- for `plan`, saves a plan file, prints a human-readable summary with
  `terraform show`, and writes the machine-readable version with
  `terraform show -json`;
- fails the plan step if the JSON plan contains any `delete` action
  (look at `resource_changes[].change.actions`), unless a flag such as
  `--allow-destroy` is passed;
- for `apply`, applies the waiting plan file and exits with an error if
  there isn't one;
- archives each applied plan with the time it was applied.

Then:

- Plan `blue`, change a tag in the code, and apply the saved plan.
  Confirm the tag change wasn't applied.
- Make a change that replaces a subnet (change its CIDR) and confirm your
  script stops it.
- Plan and apply `green`, and confirm `blue` wasn't affected.
- Try `terraform plan -detailed-exitcode`. What exit code means "no
  changes", and how would a pipeline use it?

Note what a failed apply looks like: **Terraform does not roll back.** If
you know CloudFormation, read that twice. Whatever succeeded before the
error stays, and is in state; you fix the code and apply again.

##### Question: CI/CD Pipelines

_Consider how you would use a CI/CD pipeline to roll out infrastructure
changes. Outside of the pipeline itself, what additional resources would
you need to write or create? Where does the plan file live between the
plan and apply stages, who approves it, and what credentials does each
stage need?_

#### Lab 17.3.4: Further network changes

Make one or both subnets public: add an internet gateway, a route table
with a default route to it, and route table associations. Use the
provider docs for
[`aws_vpc`](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/vpc)
and the related resources.

- Add any new variables to `variables.tf` and both `.tfvars` files.
- Plan and apply through your script, in both workspaces.
- Once you're happy with it, `terraform destroy` in both workspaces (with
  the right `-var-file`), then `terraform workspace select default` and
  `terraform workspace delete` each one.

### Retrospective 17.3

#### Question: View Terraform Plan File

_How do you view the contents of a saved plan file without applying it?
The plan file is binary; what's inside it that makes it as sensitive as
the state?_

## Lesson 17.4: Using Terraform modules

### Principle 17.4

*A module is a function for infrastructure: inputs, outputs and a
contract. Write one when it adds a layer of abstraction; pin the version
of any module you didn't write.*

### Practice 17.4

Every directory of `.tf` files is a module; the one you run `terraform`
in is the **root module**. Other modules are called with a `module`
block and can come from a local path, the [Terraform
Registry](https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/latest),
a Git repository or an S3 bucket. Read
[Modules](https://developer.hashicorp.com/terraform/language/modules) and
[Module sources](https://developer.hashicorp.com/terraform/language/modules/sources).

#### Lab 17.4.1: Creating and using a local module

A VPC with public subnets is a sensible abstraction: callers want "a
network with these CIDRs", not the eight resource types behind it. A
single EC2 instance usually isn't.

- Create `17-terraform/modules/network`. Copy your `dev/network` code
  into it, then remove the `backend` and `provider` blocks. A shared
  module keeps a `terraform` block with `required_providers` (a minimum
  version, such as `>= 6.0`) but never configures a provider: the caller
  does.

- Add `outputs.tf` with the VPC ID and the subnet IDs. With `for_each`,
  the subnet output looks like this:

  ```hcl
  output "public_subnet_ids" {
    value = [for az, s in aws_subnet.public : s.id]
  }
  ```

- In `prod/network`, write a `main.tf` with the `terraform` and
  `provider` blocks (state key `prod/network/terraform.tfstate`) and a
  `module` block that calls `../../modules/network` with a CIDR that
  doesn't overlap dev.

- Run `terraform init`, `plan` and `apply` in `prod/network`. Find the
  module's resources in `terraform state list`; note the
  `module.<name>.` prefix. Outputs are read as
  `module.<name>.<output>`.

#### Lab 17.4.2: A module from the registry

- In a scratch directory, call the community
  [VPC module](https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/latest)
  with a version constraint:

  ```hcl
  module "vpc" {
    source  = "terraform-aws-modules/vpc/aws"
    version = "~> 6.0"

    name = "stelligent-u-17-<you>-registry"
    cidr = "10.20.0.0/16"
    azs  = ["us-east-2a", "us-east-2b"]
  }
  ```

  Add public and private subnets using the module's inputs.

- Run `terraform init` and look in `.terraform/modules/`. Run `terraform
  plan` and compare what it would create with your module. Read the
  module's inputs for NAT gateways: what's the default, and what would
  turning it on cost?

- Don't apply. Delete the scratch directory.

##### Question: Trusting someone else's module

_What did the registry module do that yours doesn't? What would you
check before using a community module in production, and what does the
version constraint protect you from? Does `.terraform.lock.hcl` lock
module versions?_

#### Lab 17.4.3: Module versioning

A local path always uses whatever is checked out next to it, so every
caller changes when the module does. To make callers choose when to
upgrade, publish the module somewhere versioned: a registry (the public
one or a private one) or Git with a ref.

```hcl
module "network" {
  # A subdirectory of a Git repository, pinned to a tag.
  source = "git::https://github.com/<you>/<your-lab-repo>.git//17-terraform/modules/network?ref=network-v1.0.0"

  vpc_cidr = "10.40.0.0/20"
}
```

The `//` separates the repository from the path inside it. `ref` can be
a tag, a branch or a commit SHA.

- Commit your module and tag it `network-v1.0.0`. Push the tag.
- Point `prod/network` at the tagged Git source and run `terraform init`
  and `terraform plan`. It should show no changes.
- Change the module (another tag), commit, and plan again. The change
  shouldn't appear until you move the `ref`.

### Retrospective 17.4

#### Question: When to Use Modules

_What are some use cases and when is it appropriate to create a module?
When does a module make code harder to read? How would you release a
breaking change to a module that other teams call?_

## Lesson 17.5: Guardrails and tests

### Principle 17.5

*Catch the mistake at the cheapest point: a variable validation before
the plan, a condition during it, a check after it, and a test before any
of it reaches a real account.*

### Practice 17.5

Terraform has four layers of assertions. Read [Validate your
configuration](https://developer.hashicorp.com/terraform/language/validate)
for an overview.

- **Variable validation** (Lab 17.3.2) checks inputs.
- **Preconditions and postconditions** in a resource, data source or
  output check assumptions and guarantees, and stop the run when they
  fail.
- **`check` blocks** check the infrastructure as a whole and only
  **warn**; they run on every plan and apply.
- **`terraform test`** runs your configuration in a test harness,
  against real infrastructure or a mocked provider.

You'll add each to `modules/network`.

#### Lab 17.5.1: Preconditions and postconditions

Read [Custom
conditions](https://developer.hashicorp.com/terraform/language/expressions/custom-conditions).

- Add a **precondition** to the subnet resource that fails if there are
  more AZs than the VPC CIDR has room for.
- Add a **postcondition** to the VPC that fails if DNS hostnames aren't
  enabled after apply. Remove `enable_dns_hostnames = true` to watch it
  fail, then put it back.
- Add a precondition on an output. When would that be the right place?

##### Question: Which failure, when

_Your precondition refers to a variable, just like a validation could.
Why is a precondition sometimes the only choice? Which of your
conditions ran during `plan` and which only during `apply`, and why?_

#### Lab 17.5.2: Check blocks

A `check` block can contain its own **scoped data source**, which
Terraform reads at the end of every plan and apply. Failures are
warnings: the run continues, and a scheduled plan surfaces them. That
makes checks a lightweight way to watch for drift or broken assumptions.

```hcl
check "vpc_dns" {
  data "aws_vpc" "live" {
    id = aws_vpc.this.id
  }

  assert {
    condition     = data.aws_vpc.live.enable_dns_support
    error_message = "DNS resolution is off in ${aws_vpc.this.id}."
  }
}
```

- Add a check like this to your module, apply it in `prod/network`, then
  turn DNS support off:

  ```bash
  aws ec2 modify-vpc-attribute --vpc-id <id> --no-enable-dns-support
  ```

  Run `terraform plan`. What does the check say, and what does the plan
  propose?
- Turn it back on.

Read [Checks](https://developer.hashicorp.com/terraform/language/checks).

##### Question: Check or postcondition

_You could have written the DNS assertion as a postcondition on the VPC.
What's different when it fails? When would you want a warning rather
than an error?_

#### Lab 17.5.3: terraform test

`terraform test` runs `*.tftest.hcl` files, found in the module's root
and in a `tests/` directory. Each `run` block plans or applies the
module with the variables you give it, then evaluates `assert` blocks.
A run with `command = apply` against the real provider creates real
resources and destroys them at the end. A **mock provider** replaces
the provider with one that returns made-up values, so tests need no
credentials and create nothing. Read
[Tests](https://developer.hashicorp.com/terraform/language/tests) and
[Mocks](https://developer.hashicorp.com/terraform/language/tests/mocking).

- Create `modules/network/tests/network.tftest.hcl`. Start from this
  shape:

  ```hcl
  mock_provider "aws" {
    mock_data "aws_vpc" {
      defaults = {
        enable_dns_support = true
      }
    }
  }

  variables {
    vpc_cidr = "10.10.0.0/20"
  }

  run "subnets_fit_in_the_vpc" {
    # With a mock provider, "apply" creates nothing real: computed
    # attributes get fake values, so the check block can be evaluated.
    command = apply

    assert {
      condition     = length(aws_subnet.public) == 2
      error_message = "Expected one subnet per AZ."
    }
  }

  run "rejects_a_tiny_vpc" {
    command = plan

    variables {
      vpc_cidr = "10.10.0.0/28"
    }

    expect_failures = [var.vpc_cidr]
  }
  ```

  Adjust the resource and variable names to match your module.

- Run `terraform init` and `terraform test` in `modules/network` with
  no AWS credentials in your shell (`AWS_PROFILE=` and no SSO session).

- Add runs that assert the first subnet's CIDR, that your precondition
  fires when there are too many AZs (`expect_failures` takes the
  resource), and that the outputs have the shape a caller expects.

- Try changing the first run to `command = plan`. It fails: the check
  block's data source depends on the VPC ID, which isn't known until
  apply. That's why the example uses `apply` under the mock.

- Stretch: write a second test file with no mock provider, using the
  `lab` profile and `command = apply`. Run it with `terraform test
  -filter=tests/<file>` and watch it create and destroy a real VPC.

##### Question: Unit or integration

_What did the mocked tests prove, and what couldn't they? Which tests
would you run on every pull request and which only nightly, and why?
Where does `terraform test` fit with Terratest or with the CDK's
`assertions` module from module 25?_

### Retrospective 17.5

#### Question: Where to put the rule

_A teammate wants to enforce "every VPC CIDR is a /20 from 10.0.0.0/8".
Name the places you could enforce it (a variable validation, a
precondition, a check, a test, a policy in a pipeline, an SCP) and pick
one. What does each one miss?_

## Lesson 17.6: Changing what already exists

### Principle 17.6

*Change existing infrastructure the same way you create it: in code, as
a plan someone can review. Import, rename and forget with blocks, not
with `terraform state` commands typed at a prompt.*

### Practice 17.6

The CLI commands `terraform import`, `terraform state mv` and
`terraform state rm` edit state directly, one resource at a time, with
no plan to review. Since Terraform 1.5 and 1.7, the same operations can
be written as `import`, `moved` and `removed` blocks, which show up in
the plan, go through code review and run in a pipeline like any other
change. Work in a new directory, `17-terraform/adopt`, with the usual
`terraform`, backend (key `adopt/terraform.tfstate`) and `provider`
blocks.

#### Lab 17.6.1: Import blocks

- Create a bucket outside Terraform:

  ```bash
  aws s3api create-bucket --bucket stelligent-u-17-<you>-adopted \
    --create-bucket-configuration LocationConstraint=us-east-2
  ```

- Read [Import existing
  resources](https://developer.hashicorp.com/terraform/language/import)
  and the [`import` block
  reference](https://developer.hashicorp.com/terraform/language/block/import).
  Add an `import` block for the bucket, without writing the resource:

  ```hcl
  import {
    to = aws_s3_bucket.adopted
    id = "stelligent-u-17-<you>-adopted"
  }
  ```

- Run `terraform plan -generate-config-out=generated.tf`. Read
  [Generate configuration for imported
  resources](https://developer.hashicorp.com/terraform/language/import/generating-configuration):
  the flag is still marked experimental. Tidy `generated.tf` (remove
  arguments that are just defaults), move the resource into `main.tf`,
  and plan again until the plan says `1 to import, 0 to add, 0 to change,
  0 to destroy`, or explain every change it still wants.

- Apply. Import the bucket's versioning and public access block the same
  way. Then delete the `import` blocks; they have done their job.

##### Question: Import at scale

_`import` blocks accept `for_each`. How would you adopt twenty buckets
that follow a naming pattern? How does this compare with CloudFormation
resource import and the IaC generator in module 01?_

#### Lab 17.6.2: Moved blocks

Terraform identifies a resource by its address. Rename
`aws_s3_bucket.adopted` to `aws_s3_bucket.logs` and plan: Terraform
wants to destroy one bucket and create another. A `moved` block tells it
the object just has a new address.

```hcl
moved {
  from = aws_s3_bucket.adopted
  to   = aws_s3_bucket.logs
}
```

- Add the block (and one for each related resource) and plan again. It
  should show the moves and nothing to create or destroy. Apply.
- Do the same for a bigger refactor: in `prod/network`, if you created
  anything outside the module in Lesson 17.4, move it into the module
  (`to = module.network.aws_...`), or change a resource from `count` to
  `for_each` (`from = aws_subnet.public[0]`, `to =
  aws_subnet.public["us-east-2a"]`).
- Read [Refactoring
  modules](https://developer.hashicorp.com/terraform/language/modules/develop/refactoring):
  when can you delete a `moved` block, and why does a shared module keep
  them for a long time?

#### Lab 17.6.3: Removed blocks and drift

- Stop managing the bucket without deleting it. Delete the resource
  blocks and add:

  ```hcl
  removed {
    from = aws_s3_bucket.logs

    lifecycle {
      destroy = false
    }
  }
  ```

  Add one for each related resource, plan and apply. Confirm the bucket
  still exists and `terraform state list` no longer shows it. See the
  [`removed` block
  reference](https://developer.hashicorp.com/terraform/language/block/removed).

- **Drift.** In `prod/network`, change a tag on the VPC with the CLI
  (`aws ec2 create-tags`). Run `terraform plan -refresh-only`: it shows
  what changed outside Terraform and offers to update the state to
  match. Then run a normal `terraform plan`: it offers to put the tag
  back. Decide which is right, and apply it.

##### Question: Refresh-only

_When would you accept drift into state with `terraform apply
-refresh-only` instead of reverting it? What does this module give you
for detecting drift on a schedule, compared with CloudFormation drift
detection or AWS Config (module 26)?_

#### Lab 17.6.4: Clean up the module

Destroy in the reverse order you built, and remove the state bucket
last, because every other configuration keeps its state in it.

- **Every configuration.** In `prod/network` (and `dev/network` if
  anything's left in any workspace), run `terraform destroy`. For
  `dev/network`, `terraform workspace list` first and destroy in each
  workspace, then delete the workspaces. Run `terraform state list` in
  each directory afterwards; it should print nothing.

- **Buckets outside Terraform.** Delete the `adopted` bucket you told
  Terraform to forget: `aws s3 rb s3://stelligent-u-17-<you>-adopted`.

- **Leftovers.** List anything still tagged `topic=17`:
  `aws resourcegroupstaggingapi get-resources --tag-filters
  Key=topic,Values=17`. Only the state bucket should remain.

- **The state bucket.** Its own state is inside it, so move that state
  out first:
  1. In `state-management`, delete the `backend "s3"` block and run
     `terraform init -migrate-state`. Answer `yes`; the state is now in
     a local `terraform.tfstate`.
  2. The bucket is versioned, so it still holds every old version of
     every state file, lock file and delete marker. Either set
     `force_destroy = true` on `aws_s3_bucket` and run `terraform apply`
     first (the setting only takes effect once it's in state), or empty
     the bucket yourself: list with `aws s3api list-object-versions` and
     delete every version **and** delete marker with `aws s3api
     delete-objects`. `aws s3 rm --recursive` isn't enough: it only adds
     more delete markers. See [Deleting object
     versions](https://docs.aws.amazon.com/AmazonS3/latest/userguide/DeletingObjectVersions.html).
  3. Run `terraform destroy`.
  4. Confirm with `aws s3api head-bucket --bucket
     stelligent-u-17-<you>-tfstate`, which should now fail with a 404.

- **Your repository.** Make sure no `terraform.tfstate`,
  `terraform.tfstate.backup`, plan file or `.terraform/` directory is
  committed, and delete the local state file from `state-management`.

##### Question: Destroy protection

_Nothing stopped you destroying the state bucket once its state was
local. What would you add in a real account so that a `terraform
destroy` in the wrong directory can't remove it? Look at the
`prevent_destroy` lifecycle argument, bucket policies and module 19's
SCPs._

### Retrospective 17.6

#### Question: CloudFormation, CDK or Terraform

_Use the table from Practice 17.1. You've now seen all three tools
import, rename, and fail halfway through a change. For each, what
happens to the resources and the recorded state when an update fails
partway? Which behaviour would you want for a database, and which for a
fleet of DNS records at a third-party provider?_

#### Question: Terraform or OpenTofu

_Your team is starting a new project. What would make you choose
OpenTofu over Terraform, or the other way round? Consider the licence,
state encryption, features that exist in only one of them, support, and
what your CI tooling expects._

## Further Reading

- [Terraform: Up & Running](https://www.terraformupandrunning.com/), a
  comprehensive book, and the [Gruntwork blog](https://blog.gruntwork.io/)
  from the same authors.
- [Terratest](https://terratest.gruntwork.io/): integration tests for
  Terraform written in Go, for when `terraform test` isn't enough.
- [The `terraform_remote_state` data
  source](https://developer.hashicorp.com/terraform/language/state/remote-state-data):
  read another configuration's outputs. Read the warning about what it
  exposes, and consider SSM parameters instead.
- [Dependency lock
  file](https://developer.hashicorp.com/terraform/language/files/dependency-lock):
  what `init -upgrade` changes, and why a lock file created on macOS may
  need `terraform providers lock` for Linux CI runners.
- [Enhanced Region
  support](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/guides/enhanced-region-support)
  and the [version 6 upgrade
  guide](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/guides/version-6-upgrade)
  for the AWS provider.
- [Migrating to OpenTofu](https://opentofu.org/docs/intro/migration/).
- The [Terraform 1.11
  changelog](https://github.com/hashicorp/terraform/blob/v1.11/CHANGELOG.md),
  which made S3 native locking generally available.
- The [archived CDK for
  Terraform](https://github.com/hashicorp/terraform-cdk) repository and
  its deprecation notice.
