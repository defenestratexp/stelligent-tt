# Blog notes: Topic 22, Databases

## Working title

Databases on AWS for learners who pay their own bill: RDS, Aurora and
DynamoDB without a password in sight

Alternatives: "No public endpoint, no password, no final snapshot: a lab
database done right in 2026"; "The read replica my Secrets Manager
password wouldn't let me create".

## Hook

The 2022 course had one database moment: a DynamoDB table behind a Lambda
function. The exams I'm retaking ask much more: Multi-AZ instance versus
Multi-AZ cluster, read replica versus standby, RDS Proxy, point-in-time
restore against an RPO, GSI versus LSI, on-demand versus provisioned. So
this module builds all of it, on a budget. The database lives in subnets
that can't reach the internet, and the laptop still gets a `psql` prompt
through a free EC2 Instance Connect Endpoint. RDS generates and rotates
the password, and IAM tokens replace it. Aurora Serverless v2 now scales
to zero, so a lab cluster costs pennies while idle. And every template
sets `DeletionPolicy: Delete`, because CloudFormation's default for RDS
quietly leaves you a snapshot to pay for.

## Key points

1. **Private by default, still reachable.** Three private subnets, no
   internet gateway, no NAT gateway, and `aws ec2-instance-connect ssh
   --local-forwarding` gives `psql` on the laptop a path to the database
   at no charge. `sslmode=verify-full` with `hostaddr=127.0.0.1` keeps
   certificate checking intact through the tunnel.
2. **Let RDS own the password, then get rid of it.** `ManageMasterUserPassword`
   keeps the master password out of templates and rotates it every seven
   days. IAM database authentication swaps it for a 15-minute token signed
   locally. Show the `rds-db:connect` ARN built from `DbiResourceId`.
3. **Backups, replicas and standbys answer different questions.** Delete
   rows, restore to a point in time, time it, and see that Multi-AZ
   copied the mistake faithfully. Fail over on purpose and measure the gap
   with a one-second insert loop.
4. **Aurora separates compute from storage.** Serverless v2 with a
   minimum of 0 ACUs pauses after five idle minutes. Readers in promotion
   tiers 0 and 1 follow the writer; tier 2 and up can pause on their own.
   The Data API gets you SQL with no network path at all.
5. **RDS Proxy is worth it for connection storms, not for every
   database.** Put it in front of a `db.t4g.micro`, not a Serverless v2
   cluster, because the proxy keeps connections open and the cluster never
   pauses (and the proxy is billed per ACU there, reportedly with an
   8-ACU minimum).
   <!-- VERIFY: RDS Proxy minimum ACU charge for Aurora Serverless v2; the
   pricing page doesn't state it explicitly. -->
6. **DynamoDB is designed from access patterns.** Write the patterns
   first, then keys; watch a filtered `scan` cost the same as an
   unfiltered one; fix it with a sparse GSI. TTL plus Streams plus a Lambda
   filter on `userIdentity` archives expired items for almost nothing.

## Gotchas readers will hit

- **CloudFormation snapshots RDS by default.** `AWS::RDS::DBInstance`
  (without `DBClusterIdentifier`) and `AWS::RDS::DBCluster` have a default
  `DeletionPolicy` of `Snapshot`. Deleting the stack leaves a snapshot
  that bills until someone notices.
- **RDS Extended Support is opt-out.** CloudFormation's
  `EngineLifecycleSupport` defaults to `open-source-rds-extended-support`,
  which charges extra once the major version leaves standard support.
- **Managed passwords and read replicas don't mix.** The RDS docs list
  creating a read replica of a source with an RDS-managed secret as
  unsupported (all engines except SQL Server), and Blue/Green
  Deployments too. Capture exactly what the CLI says.
- **A point-in-time restore is a new instance with a new endpoint,** and
  for PostgreSQL the docs don't list restores among the operations that
  accept `--manage-master-user-password`. Confirm what the restored
  instance's credentials are in the lab.
- **Multi-AZ DB clusters don't run on burstable classes.** The smallest
  options are `db.c6gd.medium` or `.large` sizes of `m`/`r` classes with
  local NVMe, so they're a paper exercise in a lab.
- **IAM database auth needs memory**: 300 to 1,000 MiB extra according to
  the docs, which is a lot on a 1 GiB `db.t4g.micro`.
- **A paused Aurora instance still says `available`.** Only
  `ServerlessDatabaseCapacity` / `ACUUtilization` at zero show it's
  paused. An idle `psql` session left open keeps it awake.
- **The RDS Proxy default endpoint is placed in only two AZs** from the
  subnets you give it, and `use1-az3` doesn't support RDS Proxy (not an
  issue in `us-east-2`, but it catches people in `us-east-1`).
- **TTL is lazy.** Expired items can linger for days and still come back
  from reads unless you filter them out.
- **Global tables delay cleanup.** You can't delete a table used to add a
  replica for 24 hours after the replica is created.
- **On-demand backups outlive their table,** and so does the 35-day
  system backup DynamoDB takes when you delete a PITR-enabled table (that
  one is free).

## Exam objectives supported

- SAA-C03 Domain 1 (Task 1.3 data security controls), Domain 2 (Task 2.2
  highly available and fault-tolerant architectures), Domain 3 (Task 3.3
  high-performing database solutions), Domain 4 (Task 4.3 cost-optimized
  database solutions)
- DVA-C02 → C03 Domain 1 (Task 1.3 use data stores in application
  development) and Domain 2 (Task 2.3 manage sensitive data)
- SOA-C03 Domain 2: Reliability and Business Continuity (Tasks 2.1 to
  2.3: database scaling, Multi-AZ, backups and point-in-time restore)

## Material to capture while doing the labs

- The create-time for `db.t4g.micro`, the PITR restore time and the
  failover gap from the insert loop, for Multi-AZ instance, Aurora and via
  RDS Proxy. A small table of the three numbers is the post's centrepiece.
- The exact CLI output when creating a read replica of a managed-secret
  source.
- A `ServerlessDatabaseCapacity` graph showing pause, resume on a Data API
  call, and pause again.
- `--return-consumed-capacity` numbers for `get-item`, `query`, filtered
  `scan` and the sparse GSI `query`.
- A diagram: laptop → EC2 Instance Connect Endpoint → client instance →
  (proxy) → database, with the security group on each hop.
- The cost of the module from Cost Explorer, filtered to RDS and
  DynamoDB, with account IDs redacted.
