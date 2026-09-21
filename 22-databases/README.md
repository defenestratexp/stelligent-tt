# Topic 22: Databases

<!-- TOC -->

- [Topic 22: Databases](#topic-22-databases)
  - [What changed in the 2026 edition](#what-changed-in-the-2026-edition)
  - [Exam coverage](#exam-coverage)
  - [Cost and cleanup](#cost-and-cleanup)
  - [Guidance](#guidance)
  - [Conventions](#conventions)
  - [Lesson 22.1: A managed relational database](#lesson-221-a-managed-relational-database)
    - [Principle 22.1](#principle-221)
    - [Practice 22.1](#practice-221)
      - [Lab 22.1.1: A private network for databases](#lab-2211-a-private-network-for-databases)
      - [Lab 22.1.2: A PostgreSQL instance in CloudFormation](#lab-2212-a-postgresql-instance-in-cloudformation)
      - [Lab 22.1.3: Connect with the managed secret](#lab-2213-connect-with-the-managed-secret)
      - [Lab 22.1.4: IAM database authentication](#lab-2214-iam-database-authentication)
    - [Retrospective 22.1](#retrospective-221)
  - [Lesson 22.2: Backups, replicas and Multi-AZ](#lesson-222-backups-replicas-and-multi-az)
    - [Principle 22.2](#principle-222)
    - [Practice 22.2](#practice-222)
      - [Lab 22.2.1: Automated backups and snapshots](#lab-2221-automated-backups-and-snapshots)
      - [Lab 22.2.2: Point-in-time restore](#lab-2222-point-in-time-restore)
      - [Lab 22.2.3: Read replicas](#lab-2223-read-replicas)
      - [Lab 22.2.4: Multi-AZ DB instance: fail over on purpose](#lab-2224-multi-az-db-instance-fail-over-on-purpose)
      - [Lab 22.2.5: Multi-AZ DB cluster, on paper](#lab-2225-multi-az-db-cluster-on-paper)
    - [Retrospective 22.2](#retrospective-222)
  - [Lesson 22.3: Aurora and RDS Proxy](#lesson-223-aurora-and-rds-proxy)
    - [Principle 22.3](#principle-223)
    - [Practice 22.3](#practice-223)
      - [Lab 22.3.1: Aurora Serverless v2 that scales to zero](#lab-2231-aurora-serverless-v2-that-scales-to-zero)
      - [Lab 22.3.2: Query it with the Data API](#lab-2232-query-it-with-the-data-api)
      - [Lab 22.3.3: A reader, endpoints and failover](#lab-2233-a-reader-endpoints-and-failover)
      - [Lab 22.3.4: RDS Proxy in front of the RDS instance](#lab-2234-rds-proxy-in-front-of-the-rds-instance)
    - [Retrospective 22.3](#retrospective-223)
  - [Lesson 22.4: DynamoDB, designed from access patterns](#lesson-224-dynamodb-designed-from-access-patterns)
    - [Principle 22.4](#principle-224)
    - [Practice 22.4](#practice-224)
      - [Lab 22.4.1: Write down the access patterns](#lab-2241-write-down-the-access-patterns)
      - [Lab 22.4.2: The table and its keys](#lab-2242-the-table-and-its-keys)
      - [Lab 22.4.3: Query, Scan and what they cost](#lab-2243-query-scan-and-what-they-cost)
      - [Lab 22.4.4: Conditional writes](#lab-2244-conditional-writes)
      - [Lab 22.4.5: A sparse global secondary index](#lab-2245-a-sparse-global-secondary-index)
      - [Lab 22.4.6: Capacity modes and throttling](#lab-2246-capacity-modes-and-throttling)
    - [Retrospective 22.4](#retrospective-224)
  - [Lesson 22.5: Operating DynamoDB](#lesson-225-operating-dynamodb)
    - [Principle 22.5](#principle-225)
    - [Practice 22.5](#practice-225)
      - [Lab 22.5.1: TTL and Streams](#lab-2251-ttl-and-streams)
      - [Lab 22.5.2: Point-in-time recovery and backups](#lab-2252-point-in-time-recovery-and-backups)
      - [Lab 22.5.3: Global tables (optional)](#lab-2253-global-tables-optional)
    - [Retrospective 22.5](#retrospective-225)
  - [Lesson 22.6: Choosing, and cleaning up](#lesson-226-choosing-and-cleaning-up)
    - [Principle 22.6](#principle-226)
    - [Practice 22.6](#practice-226)
      - [Lab 22.6.1: Pick the database](#lab-2261-pick-the-database)
      - [Lab 22.6.2: Clean up the module](#lab-2262-clean-up-the-module)
    - [Retrospective 22.6](#retrospective-226)
  - [Further Reading](#further-reading)

<!-- /TOC -->

## What changed in the 2026 edition

- **New module.** The 2022 course touched a database once: Lab 9.2.1 put a
  DynamoDB table behind a Lambda function. Databases carry a lot of weight
  on the Solutions Architect, Developer and CloudOps exams, so the 2026
  edition gives them a module of their own.
- Relational databases run in **private subnets with no internet path**,
  and you reach them through an EC2 Instance Connect Endpoint, which has no
  charge. No bastion with a public IP, no publicly accessible database.
- **No database passwords in templates, parameters or shell history.** RDS
  generates and rotates the master password in Secrets Manager
  (`ManageMasterUserPassword`), and Lab 22.1.4 removes the password
  altogether with IAM database authentication.
- It covers features that did not exist in 2022 or changed since: Multi-AZ
  DB *clusters* with two readable standbys, Aurora Serverless v2 scaling to
  zero ACUs with automatic pause (November 2024), the RDS Data API for
  Aurora Serverless v2 and provisioned clusters, RDS Extended Support
  charges for old major versions, DynamoDB on-demand as the default
  capacity mode (with its price cut in November 2024), on-demand maximum
  throughput and warm throughput, a configurable PITR recovery period, and
  multi-Region strongly consistent global tables.

## Exam coverage

| Exam | Domain / task statement |
|---|---|
| SAA-C03 | Domain 1: Design Secure Architectures (Task 1.3: data security controls: encryption at rest and in transit, credential management) |
| SAA-C03 | Domain 2: Design Resilient Architectures (Task 2.2: highly available and fault-tolerant architectures: Multi-AZ, read replicas, Aurora, global tables) |
| SAA-C03 | Domain 3: Design High-Performing Architectures (Task 3.3: high-performing database solutions: RDS Proxy, read replicas, DynamoDB key and index design, capacity) |
| SAA-C03 | Domain 4: Design Cost-Optimized Architectures (Task 4.3: cost-optimized database solutions: instance classes, Serverless v2, on-demand vs provisioned) |
| DVA-C02 → C03 | Domain 1: Development with AWS Services (Task 1.3: use data stores in application development: keys, indexes, Query vs Scan, consistency, TTL, Streams). C03 guide publishes 2026-10-27 and adds GenAI / agent topics |
| DVA-C02 → C03 | Domain 2: Security (Task 2.3: manage sensitive data in application code: Secrets Manager, IAM database authentication) |
| SOA-C03 | Domain 2: Reliability and Business Continuity (Task 2.1: scaling in managed databases; Task 2.2: Multi-AZ; Task 2.3: snapshots, backups, point-in-time restore against RTO and RPO) |
| SOA-C03 | Domain 1: Monitoring, Logging, Analysis, Remediation, and Performance Optimization (replica lag, throttling, RDS Proxy) |

## Cost and cleanup

This module costs more to leave running than most, because **RDS and
Aurora bill by the hour whether you use them or not.** Build, observe,
answer the questions, delete. The figures below are rough on-demand prices
for `us-east-2`; check the pricing pages before you start.
<!-- VERIFY: current us-east-2 prices for db.t4g.micro PostgreSQL
(single-AZ and Multi-AZ), gp3 RDS storage, Aurora Serverless v2 ACU-hour,
RDS Proxy vCPU-hour and t4g.nano. -->

- **Free:** the VPC, subnets, security groups and the EC2 Instance Connect
  Endpoint (Lab 22.1.1). Nothing in this module needs a NAT gateway, an
  internet gateway or a public IPv4 address.
- **RDS for PostgreSQL** on `db.t4g.micro`, the smallest current burstable
  Graviton class, single-AZ with 20 GiB of gp3: roughly $0.02 an hour for
  the instance plus about $2.30 a month for storage, so around $15 a month
  if forgotten. **Only Lab 22.2.4 turns on Multi-AZ, which doubles both**;
  turn it off again at the end of that lab.
- **Create the instance on a current major version** (PostgreSQL 17 on
  `db.t4g.micro` at the time of writing) and set
  `EngineLifecycleSupport: open-source-rds-extended-support-disabled`.
  CloudFormation's default enrols the instance in RDS Extended Support,
  which adds a per-vCPU-hour charge once a major version leaves standard
  support.
- **Restored instances and read replicas** (Labs 22.2.2 and 22.2.3) are
  full extra instances at the same hourly price. Delete each at the end of
  its lab.
- **Aurora Serverless v2** (Lesson 22.3) bills per ACU-hour while active,
  about $0.12 per ACU-hour. With a minimum capacity of **0 ACUs** it pauses
  after five idle minutes and then charges only for storage (cents).
  An RDS Proxy attached to an Aurora cluster keeps it from pausing, which
  is one reason Lab 22.3.4 puts the proxy in front of the RDS instance
  instead.
- **RDS Proxy** bills per vCPU-hour of the target, with a two-vCPU minimum
  for provisioned instances: about $0.03 an hour, $22 a month if forgotten.
  Delete it at the end of Lab 22.3.4.
- **The client instance** (`t4g.nano`) is about $3 a month. Stop it
  between sessions if you like.
- **Secrets Manager:** each RDS-managed secret is $0.40 a month, prorated,
  and is deleted with its database.
- **Snapshots:** manual snapshots, and the final snapshots CloudFormation
  takes by default when you delete an RDS stack, are billed as backup
  storage until you delete them. That is why every template in this
  module sets `DeletionPolicy: Delete` and every cleanup step
  **deliberately skips the final snapshot**. It's lab data. In production
  you would do the opposite.
- **DynamoDB** on-demand at lab scale costs fractions of a cent. PITR is
  billed per GB-month of table size, which here is a few kilobytes.
  On-demand backups stay (and bill) after the table is gone until you
  delete them. The optional global table in Lab 22.5.3 adds replicated
  writes in `us-east-1`, still pennies.
- **Between sessions:** you can stop an RDS instance for up to seven days
  (`aws rds stop-db-instance`); RDS starts it again automatically after
  that. Storage still bills while it's stopped.
- **Worst case:** if you walked away from everything at its most
  expensive point (Multi-AZ on, proxy up, a replica and a restored
  instance running), expect roughly $80 to $100 a month. Your module 00
  and 19 budgets should catch that.
- **Cleanup:** [Lab 22.6.2](#lab-2262-clean-up-the-module) removes
  everything this module created, in dependency order, and checks for
  leftover snapshots and backups.

## Guidance

- Explore the official docs! See the
  [Amazon RDS User Guide](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Welcome.html),
  [Amazon Aurora User Guide](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/CHAP_AuroraOverview.html),
  [Amazon DynamoDB Developer Guide](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html),
  the [RDS](https://docs.aws.amazon.com/cli/latest/reference/rds/index.html),
  [RDS Data API](https://docs.aws.amazon.com/cli/latest/reference/rds-data/index.html)
  and [DynamoDB](https://docs.aws.amazon.com/cli/latest/reference/dynamodb/index.html)
  CLI references, and the CloudFormation reference for
  [AWS::RDS::DBInstance](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-rds-dbinstance.html),
  [AWS::RDS::DBCluster](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-rds-dbcluster.html),
  [AWS::RDS::DBProxy](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-rds-dbproxy.html)
  and
  [AWS::DynamoDB::Table](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-dynamodb-table.html).

- Avoid using other sites like stackoverflow.com for answers \-- part
  of the skill set you're building is finding answers straight from
  the source, AWS.

- Explore your curiosity. Try to understand why things work the way
  they do. Read more of the documentation than just what you need to
  find the answers.

## Conventions

- **Profile and Region.** Everything runs in the lab account with the `lab`
  profile from module 19, in `us-east-2`. CLI examples don't pass
  `--region` except in Lab 22.5.3, which is about Regions.
- **Names.** Every resource name and stack name starts with your
  identifier, shown here as `<you>`: `<you>-db-network`, `<you>-pg`,
  `<you>-aurora`, `<you>-lab-tracker` and so on. Tag everything with
  `owner=<you>`.
- **Engine.** The relational labs use PostgreSQL: RDS for PostgreSQL in
  Lessons 22.1 and 22.2, Aurora PostgreSQL-Compatible in Lesson 22.3. The
  ideas carry over to MySQL; the exams use both.
- **A PostgreSQL client on your own machine.** You run `psql` locally
  and reach the database through an SSH port forward. Install the
  PostgreSQL client package for your OS (version 16 or newer), and
  download the [RDS certificate bundle](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.SSL.html)
  for your Region or the global bundle.
- **Templates live next to your answers.** Keep `db-instance.yaml`,
  `aurora.yaml`, `proxy.yaml` and `dynamodb.yaml` in your copy of this
  directory. Each must pass `cfn-lint`. The only starter file is
  [starter/network.yaml](starter/network.yaml): the network is module 04's
  subject, not this one's.
- **Secrets never touch the repository.** Don't paste passwords, tokens or
  secret values into your answers. Write `<redacted>`.
- **Plan your sittings.** Lessons 22.1 to 22.3 share one RDS instance that
  bills by the hour. Do them in as few sittings as you can, stop the
  instance between sittings, or delete and recreate the stack (it takes
  about ten minutes).

## Lesson 22.1: A managed relational database

### Principle 22.1

*A managed database is still your database: AWS runs the engine, the
host and the backups, but where it sits on the network and who can log in
are decisions you make, in code.*

### Practice 22.1

Amazon RDS takes over the undifferentiated work of running a relational
database: provisioning, patching, backups, failover. What it doesn't do is
decide who can reach the database or how they authenticate. In these labs
you'll put a PostgreSQL instance in subnets that have no route to the
internet, let RDS generate and rotate its master password in Secrets
Manager, connect to it through a free EC2 Instance Connect Endpoint, and
then replace the password with short-lived IAM authentication tokens.

#### Lab 22.1.1: A private network for databases

Read [starter/network.yaml](starter/network.yaml) before you deploy it.
It creates a VPC with three private subnets (one per Availability Zone)
and **no internet gateway or NAT gateway**, three security groups, an
EC2 Instance Connect Endpoint and a `t4g.nano` instance that exists only
as an SSH hop into the VPC.

- Deploy it as `<you>-db-network` with your identifier as `Owner`.
- List the stack outputs. You'll pass them to every other stack in this
  module, either as parameters or with `Fn::ImportValue`.
- Connect to the client instance with
  [`aws ec2-instance-connect ssh`](https://docs.aws.amazon.com/cli/latest/reference/ec2-instance-connect/ssh.html)
  and `--connection-type eice`. Once connected, try to reach anything on
  the internet. Then disconnect.

Read [EC2 Instance Connect Endpoint](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/connect-with-ec2-instance-connect-endpoint.html),
including its considerations and quotas.

##### Question: No way out

_The client instance has no public IP, and the VPC has no internet
gateway. How did your SSH session get in? What does the endpoint's
security group allow, and why is the client's inbound SSH rule written
against that security group rather than a CIDR?_

##### Question: Why three subnets

_A single-AZ database needs only one subnet. Why does an RDS DB subnet
group require subnets in at least two Availability Zones, and what would
break later in this module if the VPC had only two?_

#### Lab 22.1.2: A PostgreSQL instance in CloudFormation

Write `db-instance.yaml` from the CloudFormation reference. It takes the
network stack's outputs as parameters and creates:

- an `AWS::RDS::DBSubnetGroup` over the three private subnets;
- an `AWS::RDS::DBInstance` named `<you>-pg` with:
  - engine `postgres`, a current major version and class `db.t4g.micro`.
    Find the valid combinations with
    `aws rds describe-db-engine-versions` and
    `aws rds describe-orderable-db-instance-options`. Don't guess;
  - 20 GiB of `gp3` storage, `StorageEncrypted: true`;
  - `PubliclyAccessible: false`, the network stack's database security
    group, and `MultiAZ: false`;
  - `MasterUsername` set, and **`ManageMasterUserPassword: true`**. There
    is no `MasterUserPassword` property anywhere in your template and no
    password parameter;
  - `BackupRetentionPeriod: 1`, `DeletionProtection: false`,
    `EngineLifecycleSupport: open-source-rds-extended-support-disabled`;
  - `DeletionPolicy: Delete` and `UpdateReplacePolicy: Delete` on the
    instance (see
    [DeletionPolicy](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-deletionpolicy.html)).
- Outputs for the endpoint address, the port, the instance's resource ID
  (`DbiResourceId`) and the secret ARN (`MasterUserSecret.SecretArn`).

Deploy it as `<you>-db-instance` and time how long the create takes.

##### Question: The defaults you overrode

_For each property you set above, what would the default have been, and
what would it have cost you or exposed? Pay particular attention to
`DeletionPolicy`: what does CloudFormation do by default when you delete a
stack that holds an `AWS::RDS::DBInstance`?_

##### Question: Extended Support

_Read [Amazon RDS Extended
Support](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/extended-support.html).
What happens to an instance on a major version that has reached the end
of standard support if it's enrolled, and if it isn't? Why might a
production team deliberately leave it enrolled?_

#### Lab 22.1.3: Connect with the managed secret

- Describe the instance and find `MasterUserSecret`. Describe the secret
  (not its value): note its name, the KMS key and the rotation schedule.
- Open a port forward from your machine through the client instance to
  the database. `aws ec2-instance-connect ssh` accepts
  `--local-forwarding` in OpenSSH format (`5432:<db-endpoint>:5432`).
- In a second terminal, read the password with
  `aws secretsmanager get-secret-value` into an environment variable
  (`PGPASSWORD`), not onto the command line, and connect with `psql`.
- Connect with full certificate verification: `sslmode=verify-full`, the
  RDS CA bundle, `host=` set to the real endpoint name and
  `hostaddr=127.0.0.1` so libpq connects through the tunnel but checks the
  certificate against the real name. See [Connecting to a PostgreSQL DB
  instance](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ConnectToPostgreSQLInstance.html)
  and [Using SSL with a PostgreSQL DB
  instance](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/PostgreSQL.Concepts.General.SSL.html).
- Create a table `journal (id serial primary key, note text, created_at
  timestamptz default now())` and insert a few rows. You'll use it
  throughout Lessons 22.1 and 22.2.
- Rotate the secret on demand with `aws rds modify-db-instance
  --rotate-master-user-password --apply-immediately`. Try your old
  session, then a new connection with the old password, then the new one.

##### Question: TLS

_Try `sslmode=disable`. What happens, and which parameter in the default
parameter group causes it? Why is `verify-full` better than `require`?_

##### Question: Who can read the password

_Anyone who can call `secretsmanager:GetSecretValue` on that secret, and
use its KMS key, can log in as the master user. With your `LabAdmin`
permission set, that's you. How would you let an application read it but
stop a human operator from doing the same?_

#### Lab 22.1.4: IAM database authentication

Passwords that rotate are better than passwords that don't. No password at
all is better still. With IAM database authentication, a client signs a
15-minute token with its AWS credentials and uses it as the password.

- Read [IAM database
  authentication](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.html),
  including its limitations.
- Add `EnableIAMDatabaseAuthentication: true` to your template and update
  the stack.
- As the master user, create a database user `app_iam` and grant it the
  `rds_iam` role, plus `SELECT, INSERT` on `journal`.
- Your `LabAdmin` role can connect as anyone, because it has
  `AdministratorAccess`. To see the permission model properly, add an IAM
  role to `db-instance.yaml` that your account can assume, whose only
  permission is `rds-db:connect` on
  `arn:${AWS::Partition}:rds-db:${AWS::Region}:${AWS::AccountId}:dbuser:<DbiResourceId>/app_iam`.
  Build the ARN from the instance's `DbiResourceId`; don't paste IDs.
- Add a profile for that role to `~/.aws/config` (`source_profile = lab`),
  generate a token with `aws rds generate-db-auth-token --profile ...`,
  and connect as `app_iam` through the tunnel with the token as
  `PGPASSWORD`.
- Negative test: generate a token for the master user with the same
  profile and try it.

IAM authentication needs a few hundred MiB of extra memory on the
instance, and `db.t4g.micro` has 1 GiB. If connections fail with
out-of-memory errors in the log, note it, and try `db.t4g.small` for this
lab only.
<!-- VERIFY: whether IAM auth works reliably on db.t4g.micro PostgreSQL 17
with the default parameter group. -->

##### Question: Where the token goes

_`generate-db-auth-token` didn't call any AWS API. How can it produce a
token offline, and how does the database check it? What happens to your
session when the token expires 15 minutes later?_

##### Question: The master user and rds_iam

_The docs say that for PostgreSQL, granting `rds_iam` to a user means that
user must log in with IAM. What would happen if you granted `rds_iam` to
the master user?_

### Retrospective 22.1

#### Question: Tokens or secrets

_Compare the managed secret and IAM authentication for (a) a Lambda
function that opens a new connection per invocation at 500 requests a
second, (b) a long-running container with a connection pool, (c) a
human running ad-hoc queries. Which would you pick for each, and why?_

#### Question: Nothing public

_The database has no public endpoint, the VPC has no internet gateway, and
yet you worked with it from your laptop. List every control on that path
(IAM, the endpoint, security groups, TLS, database authentication) and say
which one you'd trust if all the others failed._

## Lesson 22.2: Backups, replicas and Multi-AZ

### Principle 22.2

*Backups, read replicas and standbys solve different problems: backups
recover from mistakes, replicas scale reads, standbys survive the loss of
an Availability Zone. Know which one you're paying for.*

### Practice 22.2

The exams love to ask which of these features meets a stated RPO, RTO or
performance need, because they are easy to confuse. A Multi-AZ standby
won't save you from a `DELETE` without a `WHERE`: it faithfully copies the
mistake. A read replica won't fail over by itself. A snapshot is only as
recent as the last one you took. In these labs you'll use each on your
`<you>-pg` instance and measure what it gives you.

Each lab that creates a second instance asks you to delete it at the end.

#### Lab 22.2.1: Automated backups and snapshots

- Read [Backing up, restoring and exporting
  data](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_CommonTasks.BackupRestore.html)
  and [Introduction to
  backups](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html).
- Show the instance's backup retention period, backup window and
  `LatestRestorableTime`. Run the query again a few minutes later.
- List the automated backups for the instance
  (`describe-db-instance-automated-backups`) and the snapshots
  (`describe-db-snapshots`), both automated and manual.
- Take a manual snapshot, `<you>-pg-before-mistake`, and wait for it.
- Insert a row into `journal` that says when you took the snapshot.

##### Question: Automated or manual

_What happens to automated backups when you delete the instance? What
happens to manual snapshots? Which one would you use to keep a copy for a
year, and what would it cost?_

##### Question: How recent

_How far behind the present is `LatestRestorableTime`, and why isn't it
zero? What does that tell you about the best RPO point-in-time restore can
offer?_

#### Lab 22.2.2: Point-in-time restore

Make a mistake on purpose, then undo it without touching the original.

- Note the time, then `DELETE FROM journal;`.
- Restore the instance to a time just before the delete with
  `aws rds restore-db-instance-to-point-in-time`, as a **new** instance
  `<you>-pg-restored`: same subnet group and security group,
  `db.t4g.micro`, not publicly accessible, single-AZ. See [Restoring a DB
  instance to a specified
  time](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PIT.html).
- Time the restore.
- Work out how to log in to the restored instance. Does it have a
  `MasterUserSecret`? Which password does it expect? (Hint: look at the
  secret's version stages, and at the list of operations that support
  `--manage-master-user-password` in [Password management with Amazon RDS
  and AWS Secrets
  Manager](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-secrets-manager.html).)
  <!-- VERIFY: that a PostgreSQL instance restored to a point in time has
  no MasterUserSecret and expects the master password current at the
  restore time. -->
- Connect, confirm the rows are there, and copy them back into
  `<you>-pg` (a `pg_dump` of one table through two tunnels, or a few
  `INSERT`s, whichever you prefer).
- Delete `<you>-pg-restored` with `--skip-final-snapshot
  --delete-automated-backups`.

##### Question: RTO

_How long did the restore take, end to end, including the time to find
the right timestamp and copy the data back? If your RTO were 15 minutes,
would point-in-time restore meet it? What would?_

##### Question: A new endpoint

_The restore created a new instance with a new endpoint. What would an
application need to change to use it? How could you avoid changing the
application at all?_

#### Lab 22.2.3: Read replicas

A read replica is a separate instance that applies changes from the
source asynchronously. It serves reads, has its own endpoint, and never
takes over by itself.

- Read [Working with DB instance read
  replicas](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_ReadRepl.html).
- Now read the **limitations** section of [Password management with
  Amazon RDS and AWS Secrets
  Manager](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-secrets-manager.html)
  again. What does it say about read replicas?
- Try it anyway: `aws rds create-db-instance-read-replica` from
  `<you>-pg`, as `db.t4g.micro` in the same subnet group. Record exactly
  what happens.
  <!-- VERIFY: the current behaviour when creating an RDS for PostgreSQL
  read replica of a source that uses ManageMasterUserPassword; the docs
  list it as unsupported. -->
- If the replica is created: insert rows on the source and read them on
  the replica, watch the `ReplicaLag` metric, try an `INSERT` on the
  replica, then delete it with `--skip-final-snapshot`.
- If it isn't: don't turn off password management to force it. Lab 22.3.3
  gives you readers on Aurora, where this limitation doesn't apply.

##### Question: Replica or standby

_Complete the comparison: synchronous or asynchronous; readable or not;
same Region only or cross-Region; automatic failover or manual promotion;
how many per source. Do it for a read replica, a Multi-AZ DB instance
standby and a Multi-AZ DB cluster reader._

##### Question: Credentials and replicas

_Why might password management and read replicas not mix? If you needed
both today, what would you do? (Look for the AWS Database Blog post on
rotating credentials for primaries with read replicas.)_

#### Lab 22.2.4: Multi-AZ DB instance: fail over on purpose

This is the one lab in the module that runs a Multi-AZ deployment, and it
doubles the instance and storage cost while it's on. Finish it in one
sitting.

- Read [Multi-AZ DB instance
  deployments](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZSingleStandby.html).
- Set `MultiAZ: true` in your template and update the stack. Watch the
  events (`aws rds describe-events --source-type db-instance`) while it
  converts. Is there downtime?
- On the client instance, resolve the endpoint name
  (`getent hosts <endpoint>`) and note the IP and which subnet it's in.
- Open a `psql` session through your tunnel, and in another terminal run
  a loop that opens a new connection and inserts a timestamp into
  `journal` every second.
- Fail over: `aws rds reboot-db-instance --force-failover`.
- Afterwards, measure the gap in timestamps, resolve the endpoint again,
  and read the events.
- Set `MultiAZ: false` and update the stack. Confirm with
  `describe-db-instances`.

##### Question: What moved

_Which of these changed after the failover: the endpoint name, the IP
address it resolves to, the Availability Zone of the primary, your open
`psql` session, your loop? Why does the loop recover when the open
session doesn't?_

##### Question: DNS caching

_How would a client that caches DNS for a long time behave during a
failover? Where would you look to control that in a Java or Python
application?_

#### Lab 22.2.5: Multi-AZ DB cluster, on paper

A Multi-AZ DB *cluster* is a different deployment: a writer and two
readable standbys in three Availability Zones, with semisynchronous
replication. It isn't Aurora, and it doesn't run on burstable classes, so
you won't build one.

- Read [Multi-AZ DB cluster
  deployments](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/multi-az-db-clusters-concepts.html)
  and its limitations.
- Find the smallest instance class a Multi-AZ DB cluster supports, and
  estimate its monthly cost in `us-east-2` for three instances.

##### Question: Three deployments

_For each of Single-AZ, Multi-AZ DB instance and Multi-AZ DB cluster,
give: the number of copies of the data, whether the standbys serve reads,
typical failover time, which endpoints you get, and the cheapest instance
class. When is the cluster worth its price?_

### Retrospective 22.2

#### Question: RPO and RTO for each feature

_Fill in a table with rows for automated backups with point-in-time
restore, manual snapshots, a read replica you promote, a Multi-AZ DB
instance and a cross-Region read replica. Columns: what failure it
protects against, RPO, RTO, and what it costs on top of the primary._

#### Question: A bad migration

_A schema migration drops a column that production still needs. The
instance is Multi-AZ with one read replica. Which of your recovery
options actually helps, and how fast?_

## Lesson 22.3: Aurora and RDS Proxy

### Principle 22.3

*Aurora separates compute from storage, so replicas, failover and scaling
become operations on compute alone. RDS Proxy separates your
application's connections from the database's.*

### Practice 22.3

Aurora keeps six copies of your data across three Availability Zones in a
shared cluster volume. Instances attach to that volume: one writer and up
to 15 readers. Because readers don't replay a log into their own storage,
they add capacity quickly and fail over quickly. Aurora Serverless v2
instances resize themselves in Aurora Capacity Units (ACUs), and since
November 2024 can scale to zero and pause when nobody's connected, which
makes Aurora affordable for a lab.

RDS Proxy is a different kind of tool. It holds a pool of database
connections and multiplexes many client connections onto them, which
protects small databases from connection storms (think Lambda) and hides
most of a failover from clients.

#### Lab 22.3.1: Aurora Serverless v2 that scales to zero

- Read [Using Aurora Serverless
  v2](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless-v2.html)
  and [Scaling to zero ACUs with automatic pause and
  resume](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-serverless-v2-auto-pause.html).
  Note which engine versions support a minimum of 0 ACUs.
- Write `aurora.yaml`:
  - an `AWS::RDS::DBSubnetGroup` over the three private subnets;
  - an `AWS::RDS::DBCluster` named `<you>-aurora`: engine
    `aurora-postgresql` on a version that supports 0 ACUs,
    `ServerlessV2ScalingConfiguration` with `MinCapacity: 0`,
    `MaxCapacity: 2` and `SecondsUntilAutoPause: 300`,
    `ManageMasterUserPassword: true`, `StorageEncrypted: true`, the
    database security group, `BackupRetentionPeriod: 1`,
    `EngineLifecycleSupport: open-source-rds-extended-support-disabled`,
    and `DeletionPolicy: Delete`;
  - one `AWS::RDS::DBInstance` with `DBInstanceClass: db.serverless` and
    `DBClusterIdentifier` pointing at the cluster.
- Deploy it as `<you>-aurora`.
- Watch the `ServerlessDatabaseCapacity` metric for the instance over the
  next 15 minutes without connecting. Find the events that show it
  pausing (`RDS-EVENT-0370` to `0374`).

##### Question: Status while paused

_What does `describe-db-instances` report as the status of a paused
instance? What would a monitoring check that only looks at status miss?_

##### Question: What keeps it awake

_List four things that stop a Serverless v2 instance from pausing. Which
one would you most likely do by accident during development?_

#### Lab 22.3.2: Query it with the Data API

The RDS Data API runs SQL over HTTPS with your IAM credentials and a
Secrets Manager secret. There's no network path to open and no driver to
install.

- Read [Using the Amazon RDS Data
  API](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/data-api.html)
  and its limitations.
- Enable it with `EnableHttpEndpoint: true` on the cluster and update the
  stack.
- From your laptop (no tunnel), run `aws rds-data execute-statement` with
  the cluster ARN and the cluster's managed secret ARN. Time the first
  call after the instance has paused, then a second call.
- Create the same `journal` table and insert a few rows with a
  transaction (`begin-transaction`, `execute-statement`,
  `commit-transaction`).

##### Question: Resume time

_How long did the first call take after a pause? How would you design a
client for that, and when would a 15-second first query be
unacceptable?_

##### Question: Who can run SQL

_Which IAM permissions did the Data API call need? How is this different,
from a security point of view, from a Lambda function in the VPC with a
database driver?_

#### Lab 22.3.3: A reader, endpoints and failover

- Add a second `db.serverless` instance to the cluster with
  `PromotionTier: 1`. Update the stack.
- Describe the cluster and record its endpoints: the cluster (writer)
  endpoint and the reader endpoint. List each instance's role
  (`IsClusterWriter`).
- Using the Data API or `psql` through your tunnel (the cluster uses the
  same database security group), write through the cluster endpoint and
  read through the reader endpoint.
- Fail over with `aws rds failover-db-cluster`. Describe the cluster
  again: which instance is the writer now, and did the endpoint names
  change? Compare the failover time with Lab 22.2.4.
- Change the reader to `PromotionTier: 2` and let the cluster sit idle.
  Which instances pause?
- Remove the reader from the template and update the stack.

##### Question: Aurora replicas and RDS read replicas

_Why is Aurora replica lag usually measured in milliseconds when an RDS
read replica can fall minutes behind? Why can an Aurora reader become the
writer in seconds?_

##### Question: Promotion tiers

_What do promotion tiers 0 and 1 mean for failover, for Serverless v2
scaling and for automatic pause? When would you deliberately put a
reader in tier 15?_

#### Lab 22.3.4: RDS Proxy in front of the RDS instance

You put the proxy in front of `<you>-pg`, not the Aurora cluster, because
a proxy holds connections open to its targets and would keep the Aurora
instance from ever pausing.

- Read [Amazon RDS
  Proxy](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy.html),
  [Setting up database credentials for RDS
  Proxy](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-proxy-secrets-arns.html)
  and [RDS Proxy
  pricing](https://aws.amazon.com/rds/proxy/pricing/).
- Add a proxy security group to the network stack, as its TODO says:
  inbound 5432 from the client security group, plus an ingress rule on
  the database security group from the proxy's security group.
- Write `proxy.yaml`:
  - an IAM role that `rds.amazonaws.com` can assume, allowed to read only
    `<you>-pg`'s managed secret (and to decrypt it with the Secrets
    Manager KMS key through Secrets Manager);
  - an `AWS::RDS::DBProxy` named `<you>-pg-proxy`: engine family
    `POSTGRESQL`, `RequireTLS: true`, the private subnets, the proxy
    security group, and one `Auth` entry with `AuthScheme: SECRETS` and
    the managed secret ARN;
  - an `AWS::RDS::DBProxyTargetGroup` (`TargetGroupName: default`)
    pointing at `<you>-pg`.
  <!-- VERIFY: that RDS Proxy accepts an RDS-managed master user secret
  (rds!db-...) directly, and that the proxy needs no Secrets Manager VPC
  endpoint in subnets without internet access. -->
- Deploy it as `<you>-pg-proxy`. Check `aws rds describe-db-proxy-targets`
  until the target is `AVAILABLE`. If it isn't, the `Reason` and
  `Description` fields tell you why.
- Connect through the proxy endpoint via your tunnel. Compare
  `ClientConnections` and `DatabaseConnections` in CloudWatch while you
  open ten sessions at once.
- Run the reboot loop from Lab 22.2.4 again, once against the instance
  endpoint and once against the proxy endpoint, with a plain
  `reboot-db-instance`. Compare the gaps.
- Delete the `<you>-pg-proxy` stack at the end of the lab.

##### Question: Rotation behind the proxy

_The managed secret rotates every seven days. What does the proxy do when
it rotates, and what do clients connected to the proxy notice?_

##### Question: Pinning

_What is session pinning, what causes it in PostgreSQL, and why does it
reduce the benefit of the proxy? Which CloudWatch metric shows it?_

##### Question: When not to use a proxy

_The proxy costs roughly twice as much per hour as the `db.t4g.micro`
behind it. When is it worth it, and when would the Data API or a
connection pool in the application be the better answer?_

### Retrospective 22.3

#### Question: Aurora or RDS

_For a small internal app with a few users during office hours, compare
RDS for PostgreSQL on `db.t4g.micro` with Aurora Serverless v2 at 0 to 2
ACUs: monthly cost, cold-start behaviour, failover, backups, storage
growth. Which would you choose, and what would change your mind?_

#### Question: Proxy and serverless

_Why is RDS Proxy in front of Aurora Serverless v2 billed at a minimum
number of ACUs, and what does it do to automatic pause? Is there ever a
reason to combine them?_
<!-- VERIFY: that RDS Proxy for Aurora Serverless v2 has a minimum ACU
charge (commonly cited as 8 ACUs); the pricing page doesn't state it. -->

## Lesson 22.4: DynamoDB, designed from access patterns

### Principle 22.4

*In DynamoDB you design the keys for the questions you will ask, before
you write any data. A relational schema models the data; a DynamoDB
table models the access patterns.*

### Practice 22.4

Module 09 put items in a table and queried them back. That works for one
access pattern. With more than one, the choice of partition key, sort key
and secondary indexes decides whether each question is a cheap `Query` or
an expensive `Scan`, and whether traffic spreads across partitions or
piles onto one.

These labs build a small **lab tracker**: students, their lab
submissions, and a queue of submissions waiting for review. You'll design
it from access patterns, build it in CloudFormation, and measure what each
operation costs. Use on-demand capacity except where a lab says otherwise.

Read these first:

- [Core components of DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.CoreComponents.html)
- [Best practices for designing and using partition keys
  effectively](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-partition-key-design.html)
- [Best practices for using sort keys to organize
  data](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-sort-keys.html)

#### Lab 22.4.1: Write down the access patterns

Before any YAML, write a table in your answers with one row per access
pattern: what the application asks, which key it knows, what it expects
back and in what order, and how often.

The lab tracker must support at least:

1. Get a student's profile by student ID.
2. List a student's submissions, newest first.
3. Get one submission, knowing the student and the lab number.
4. List the submissions for one lab that are waiting for review, oldest
   first.
5. Keep a reviewer's "claimed" marker on a submission for 30 minutes,
   then let it lapse.

Then design the keys. Use generic key attribute names (`pk`, `sk`) and
item types distinguished by prefixes, such as `STUDENT#<id>` and
`SUB#<lab>#<timestamp>`. For each access pattern, write the exact
operation and key condition that serves it. Mark any pattern that your
base table can't serve with a `Query`; Lab 22.4.5 fixes it.

##### Question: One table or several

_Why does this design put students and submissions in one table? What
would you give up, and what would you gain, with a table per entity?_

##### Question: Hot partitions

_Suppose one lab is due tomorrow and every student submits in the last
hour. Which of your keys, if any, would concentrate that write traffic on
a single partition key value? How does DynamoDB's adaptive capacity
help, and where does it stop helping?_

#### Lab 22.4.2: The table and its keys

Write `dynamodb.yaml` with an `AWS::DynamoDB::Table` named
`<you>-lab-tracker`:

- `BillingMode: PAY_PER_REQUEST`, `pk` (string) as partition key, `sk`
  (string) as sort key;
- `DeletionProtectionEnabled: false` (you'll turn it on later to see what
  it does), SSE with the AWS owned key, and `DeletionPolicy: Delete`;
- a **local secondary index** that lets you list a student's submissions
  by score instead of time. You can't add an LSI after the table exists,
  so decide now.

Then write a small script (Python with boto3, or the CLI with
`batch-write-item`) that loads a few students and 20 to 30 submissions
across several labs, some reviewed, some pending.

##### Question: LSI or GSI

_Read [Local secondary
indexes](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/LSI.html)
and [Global secondary
indexes](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.html).
Compare them on: when you can create them, which partition key they use,
consistency of reads, whose capacity they consume, and the 10 GB item
collection limit. Would you really use an LSI here?_

#### Lab 22.4.3: Query, Scan and what they cost

- Serve access patterns 1 to 3 with `get-item` and `query`. Add
  `--return-consumed-capacity TOTAL` to every call and record the read
  units each consumed.
- Serve pattern 4 with a `scan` and a filter expression. Record the
  consumed capacity and compare `Count` with `ScannedCount`.
- Run pattern 2 with `--consistent-read` and without. Compare the
  capacity consumed.
- Use `--projection-expression` to fetch only two attributes. Did the
  consumed capacity change?

See [Query](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Query.html),
[Scan](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Scan.html)
and [Read consistency](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadConsistency.html).

##### Question: Filters don't save money

_Why did the filtered `scan` cost the same as an unfiltered one? What
does a filter expression change, and what doesn't it?_

##### Question: Units

_How are read request units calculated for a 6 KB item read with strong
consistency, with eventual consistency, and in a transaction? And write
request units for a 1.5 KB item?_

#### Lab 22.4.4: Conditional writes

- Register a student only if they don't already exist
  (`attribute_not_exists(pk)`). Run it twice.
- Add a `version` number to submissions and implement optimistic locking:
  a reviewer updates the score only if `version` still has the value they
  read, and increments it. Simulate two reviewers racing.
- Write a submission and increment a per-student `submissionCount` on the
  profile in one `transact-write-items` call.

See [Condition expressions](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.ConditionExpressions.html)
and [Transactions](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transactions.html).

##### Question: Failed conditions

_What error did the losing reviewer get, and did the failed write consume
capacity? How should application code handle it?_

#### Lab 22.4.5: A sparse global secondary index

Access pattern 4 needs a different partition key: the lab, not the
student.

- Give pending submissions two extra attributes, for example
  `reviewQueue = LAB#<lab>` and `queuedAt = <timestamp>`. Remove them
  (`REMOVE` in an update expression) when the submission is reviewed.
- Add a GSI on `reviewQueue` / `queuedAt` with a projection that carries
  only what a reviewer needs. Update the stack and watch the index
  backfill (`IndexStatus`).
- Serve pattern 4 with a `query` on the index. Compare its consumed
  capacity with the `scan` from Lab 22.4.3.
- Mark a submission reviewed and query again.

##### Question: Sparse

_Why does the index contain only pending submissions? What would it cost
to keep every submission in it instead?_

##### Question: Index consistency

_Can you do a strongly consistent read on a GSI? What could a reviewer
see immediately after another reviewer marks a submission done?_

#### Lab 22.4.6: Capacity modes and throttling

- Read [DynamoDB throughput
  capacity](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/capacity-mode.html)
  and [Considerations when switching capacity
  modes](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-switching-capacity-modes.html).
- Switch the table to provisioned mode with 1 RCU and 1 WCU (and the same
  on the GSI) in the template. Write a loop that puts items as fast as
  it can for two minutes. Watch for throttling in your client and in the
  `ThrottledRequests` and `WriteThrottleEvents` metrics.
- Switch back to on-demand and set a
  [maximum throughput](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/on-demand-capacity-mode-max-throughput.html)
  (`OnDemandThroughput`) of a few write units per second. Run the loop
  again.
- Describe the table's warm throughput.

##### Question: Burst capacity

_Your provisioned table may not have throttled straight away. Why not?
How long does burst capacity last?_

##### Question: Which mode

_On-demand is now the default and AWS's recommendation for most
workloads. When would you still choose provisioned capacity, and what
limits how often you can switch between the modes?_

### Retrospective 22.4

#### Question: A new access pattern

_Six months later, product asks for "all submissions reviewed by a given
reviewer this week." What are your options (new GSI, a new item type,
a scan, exporting to S3 and querying with Athena), and what does each
cost to build and to run?_

#### Question: Relational thinking

_What did you do in this lesson that would be a mistake in PostgreSQL,
and what would be a mistake in DynamoDB that is normal in PostgreSQL?_

## Lesson 22.5: Operating DynamoDB

### Principle 22.5

*DynamoDB removes servers, not operations: data still expires, changes
still need to flow somewhere, and tables still need backups.*

### Practice 22.5

These labs add the features that come up when a table is in production:
expiring data automatically with TTL, reacting to every change with
Streams and Lambda, recovering from mistakes with point-in-time recovery,
and replicating to another Region with global tables.

#### Lab 22.5.1: TTL and Streams

- Read [Using time to live
  (TTL)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)
  and [Change data capture for DynamoDB
  Streams](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.html).
- Enable TTL on an attribute named `expiresAt`, and a stream with
  `NEW_AND_OLD_IMAGES`, in the template.
- Implement access pattern 5: a "claim" item with `expiresAt` set 30
  minutes ahead (epoch seconds, a Number). Write a few with `expiresAt`
  already in the past.
- Query for claims and filter out expired ones in your query, because
  expired items can still be returned until DynamoDB deletes them.
- Add a Lambda function (Python 3.13, as in module 09) with an event
  source mapping on the stream. Give it a
  [filter](https://docs.aws.amazon.com/lambda/latest/dg/invocation-eventfiltering.html)
  so it's invoked only for TTL deletions, and have it log the old image
  of each expired claim. See [DynamoDB Streams and Time to
  Live](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/time-to-live-ttl-streams.html).
- Come back later (it can take a while) and find the log entries.

##### Question: When is expired

_How soon after `expiresAt` did the items disappear? Why must your
application never rely on TTL for exact timing, and do TTL deletions
consume write capacity?_

##### Question: Service or user

_How does a stream record for a TTL deletion differ from one for a
`delete-item` you ran yourself? Why does that matter for an archiving
function?_

#### Lab 22.5.2: Point-in-time recovery and backups

- Read [Point-in-time backups for
  DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Point-in-time-recovery.html)
  and [Backing up and restoring DynamoDB
  tables](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/CreateBackup.html).
- Enable PITR in the template with a recovery period of 7 days.
- Take an on-demand backup with `create-backup`.
- Delete several submissions by mistake, then restore the table to a
  point before the deletion as `<you>-lab-tracker-restored`.
- Describe the restored table and list what it **didn't** bring with it
  (TTL, streams, PITR, tags, deletion protection and so on).
- Turn on deletion protection on the original table and try to delete
  it. Turn it off again.
- Delete the restored table and the on-demand backup.

##### Question: Restores make new tables

_Both RDS and DynamoDB restore into a new resource rather than
overwriting the old one. Why? What does your application's configuration
need to look like for that to be a quick change?_

##### Question: A deleted table

_What happens to PITR data when you delete a table that has PITR
enabled? What happens to on-demand backups?_

#### Lab 22.5.3: Global tables (optional)

Global tables replicate a table to other Regions, each replica accepting
reads and writes. This lab is optional: it's cheap at lab scale, but
**a table used to add a replica can't be deleted for 24 hours** after the
replica is created, which delays your cleanup.

Read [Global tables](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GlobalTables.html)
and [How DynamoDB global tables
work](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/V2globaltables_HowItWorks.html)
either way.

- Hands-on (optional): create a separate small table
  `<you>-global-demo` in `us-east-2`, add a replica in `us-east-1` (your
  module 19 region guardrail allows it), write in one Region and read in
  the other, and look at the `ReplicationLatency` metric. Then write the
  same item in both Regions at the same moment and see which one wins.
  Remove the replica, and delete the table when the 24 hours are up.

##### Question: MREC or MRSC

_Compare multi-Region eventual consistency and multi-Region strong
consistency: RPO, write latency, how conflicts are handled, how many
Regions, and which features (TTL, LSIs, transactions) each gives up. Why
couldn't you add an MRSC replica to your lab tracker table?_

##### Question: Global tables or global database

_How does a DynamoDB global table differ from an Aurora global database
in who can write where and how failover works?_

### Retrospective 22.5

#### Question: Backups across services

_AWS Backup (module 23) can back up both RDS and DynamoDB on a schedule
with a retention policy. What would it add over the native features you
used in this module, and what does it cost?_

## Lesson 22.6: Choosing, and cleaning up

### Principle 22.6

*Choose the database for the access pattern and the operating model you
can live with, and delete it the moment you're done learning from it.*

### Practice 22.6

The exams give short scenarios and ask for the right database. The first
lab is questions only. The second removes everything this module built.

#### Lab 22.6.1: Pick the database

Read the [AWS database decision
guide](https://docs.aws.amazon.com/decision-guides/latest/databases-on-aws-how-to-choose/databases-on-aws-how-to-choose.html),
then answer.

##### Question: Scenarios

_For each scenario, name the service and deployment you'd choose, and one
reason: (a) an e-commerce catalogue with unpredictable spikes, key-value
lookups and single-digit millisecond reads; (b) an existing MySQL
application whose reads outgrow one instance; (c) a relational database
that must survive the loss of an Availability Zone with no data loss and
failover under 35 seconds; (d) a reporting database used two hours a day;
(e) thousands of Lambda functions connecting to one PostgreSQL database;
(f) a session store where items should vanish after an hour; (g) an
application that must keep accepting writes in two Regions._

##### Question: Other engines

_Where would ElastiCache, DocumentDB, Neptune, Keyspaces, Timestream and
Redshift fit? One sentence each is enough._

#### Lab 22.6.2: Clean up the module

Delete in dependency order and skip every final snapshot on purpose: this
is lab data, and your templates set `DeletionPolicy: Delete` so that
CloudFormation doesn't snapshot it for you.

- **Proxy:** delete the `<you>-pg-proxy` stack if it still exists.
- **Leftover instances:** `<you>-pg-restored` and any read replica, with
  `aws rds delete-db-instance --skip-final-snapshot
  --delete-automated-backups`.
- **RDS instance:** delete the `<you>-db-instance` stack.
- **Aurora:** delete the `<you>-aurora` stack.
- **DynamoDB:** delete the `<you>-lab-tracker` stack (turn off deletion
  protection first if you left it on), the Lambda function from Lab
  22.5.1 and its log group, any restored tables, and on-demand backups
  (`aws dynamodb list-backups`). If you did Lab 22.5.3, remove the
  replica and delete `<you>-global-demo` in both Regions once 24 hours
  have passed.
- **Manual snapshots:** delete `<you>-pg-before-mistake` and anything else
  `aws rds describe-db-snapshots --snapshot-type manual` and
  `aws rds describe-db-cluster-snapshots --snapshot-type manual` list.
- **Retained backups:** check
  `aws rds describe-db-instance-automated-backups` and
  `aws rds describe-db-cluster-automated-backups` for anything left
  behind, and delete it.
- **Secrets:** confirm with `aws secretsmanager list-secrets` that the
  `rds!` secrets are gone (RDS deletes them with their database).
- **Network:** delete the `<you>-db-network` stack last, including any IAM
  role or profile you added for Lab 22.1.4.
- **Local files:** remove the extra profile from `~/.aws/config`, and any
  exported `PGPASSWORD` from your shell.
- A day later, check Cost Explorer for the lab account, filtered to RDS
  and DynamoDB.

##### Question: Why skip the snapshot

_In production you'd almost always keep a final snapshot. Name two
situations where skipping it is the right call, and one control (from
this module or module 19) that would stop someone from skipping it in
production._

### Retrospective 22.6

#### Question: What cost the most

_Look at the lab account's bill for the days you worked on this module.
Which resource cost the most, and what would you do differently next time
to learn the same things for less?_

## Further Reading

- [Amazon RDS best
  practices](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_BestPractices.html)
  and [Best practices with Amazon
  Aurora](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.BestPractices.html)
- [Using Amazon RDS Blue/Green Deployments for database
  updates](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/blue-green-deployments.html):
  how teams upgrade major versions with a short switchover. Note that it
  doesn't support RDS-managed master passwords.
- [Using Amazon Aurora global
  databases](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/aurora-global-database.html)
- [Best practices for designing and architecting with
  DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html),
  including the sections on single-table design and on handling
  many-to-many relationships
- [Understanding DynamoDB warm
  throughput](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/warm-throughput.html)
  and [Burst and adaptive
  capacity](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/burst-adaptive-capacity.html)
- [DynamoDB export to
  S3](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/S3DataExport.HowItWorks.html),
  for the analytics questions DynamoDB shouldn't answer itself
- [Amazon DynamoDB
  Accelerator (DAX)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.html)
  and [Amazon ElastiCache](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/WhatIs.html),
  for when caching is the answer
