# Topic 23: Storage and Backup

<!-- TOC -->

- [Topic 23: Storage and Backup](#topic-23-storage-and-backup)
  - [What changed in the 2026 edition](#what-changed-in-the-2026-edition)
  - [Exam coverage](#exam-coverage)
  - [Cost and cleanup](#cost-and-cleanup)
  - [Guidance](#guidance)
  - [Conventions](#conventions)
  - [Lesson 23.1: Shared file storage with Amazon EFS](#lesson-231-shared-file-storage-with-amazon-efs)
    - [Principle 23.1](#principle-231)
    - [Practice 23.1](#practice-231)
      - [Lab 23.1.1: A file system with two mount targets](#lab-2311-a-file-system-with-two-mount-targets)
      - [Lab 23.1.2: Mount it from two Availability Zones](#lab-2312-mount-it-from-two-availability-zones)
      - [Lab 23.1.3: Access points and a file system policy](#lab-2313-access-points-and-a-file-system-policy)
      - [Lab 23.1.4: Lifecycle management and storage classes](#lab-2314-lifecycle-management-and-storage-classes)
    - [Retrospective 23.1](#retrospective-231)
  - [Lesson 23.2: AWS Backup](#lesson-232-aws-backup)
    - [Principle 23.2](#principle-232)
    - [Practice 23.2](#practice-232)
      - [Lab 23.2.1: Opt-in, a vault and a role](#lab-2321-opt-in-a-vault-and-a-role)
      - [Lab 23.2.2: A backup plan that selects by tag](#lab-2322-a-backup-plan-that-selects-by-tag)
      - [Lab 23.2.3: Back up now, then restore](#lab-2323-back-up-now-then-restore)
      - [Lab 23.2.4: Vault Lock in governance mode](#lab-2324-vault-lock-in-governance-mode)
      - [Lab 23.2.5: Restore testing](#lab-2325-restore-testing)
    - [Retrospective 23.2](#retrospective-232)
  - [Lesson 23.3: Disaster recovery, RTO and RPO](#lesson-233-disaster-recovery-rto-and-rpo)
    - [Principle 23.3](#principle-233)
    - [Practice 23.3](#practice-233)
      - [Lab 23.3.1: Put numbers on it](#lab-2331-put-numbers-on-it)
      - [Lab 23.3.2: Copy backups to your DR Region](#lab-2332-copy-backups-to-your-dr-region)
      - [Lab 23.3.3: Copy an EBS snapshot by hand](#lab-2333-copy-an-ebs-snapshot-by-hand)
      - [Lab 23.3.4: S3 Cross-Region Replication](#lab-2334-s3-cross-region-replication)
      - [Lab 23.3.5: EFS replication and failover (optional)](#lab-2335-efs-replication-and-failover-optional)
      - [Lab 23.3.6: Clean up the module](#lab-2336-clean-up-the-module)
    - [Retrospective 23.3](#retrospective-233)
  - [Further Reading](#further-reading)

<!-- /TOC -->

## What changed in the 2026 edition

- **New module.** The 2022 course touched storage only through S3 and EBS
  and never taught backup or disaster recovery. Both are tested on SAA-C03
  (Domain 2) and CloudOps SOA-C03 (Task 2.3, "Implement backup and restore
  strategies", and Skill 1.3.4 on shared storage and EFS lifecycle
  policies).
- **Amazon EFS** is covered as it works in 2026: Elastic throughput as the
  default, three storage classes (Standard, Infrequent Access and
  **Archive**, added in November 2023), lifecycle policies that can move
  files back to Standard on first access, access points, IAM authorization
  for NFS clients, and the `amazon-efs-utils` mount helper on Amazon Linux
  2023. The clients are reached with Session Manager, not SSH.
- **AWS Backup** is the one place backup policy lives: plans, tag-based
  selections, vaults, **Vault Lock**, cross-Region copies and **restore
  testing** (launched November 2023), which proves on a schedule that your
  backups can actually be restored.
- **Disaster recovery** is taught through the four strategies in AWS's
  [Disaster Recovery of Workloads on
  AWS](https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-workloads-on-aws.html)
  whitepaper, with RTO and RPO as the numbers that choose between them.
  The labs build the data layer of a DR plan: cross-Region backup copies,
  EBS snapshot copies (including time-based copies), S3 Cross-Region
  Replication and, optionally, EFS replication.
- It builds on modules 02 (S3 versioning; replication was only a question
  there) and 05 (EBS volumes and snapshots) rather than repeating them.

## Exam coverage

| Exam | Domain / task statement |
|---|---|
| SAA-C03 | Domain 2: Design Resilient Architectures (Task 2.2: highly available and/or fault-tolerant architectures, including DR strategies, RPO and RTO) |
| SAA-C03 | Domain 3: Design High-Performing Architectures (Task 3.1: high-performing and/or scalable storage solutions) |
| SAA-C03 | Domain 4: Design Cost-Optimized Architectures (Task 4.1: cost-optimized storage solutions) |
| SOA-C03 | Domain 1: Monitoring, Logging, Analysis, Remediation, and Performance Optimization (Skill 1.3.4: shared storage, EFS lifecycle policies) |
| SOA-C03 | Domain 2: Reliability and Business Continuity (Task 2.3: backup and restore strategies; Skill 2.3.4: backup and restore, pilot light, warm standby, active/active) |

## Cost and cleanup

Prices are for `us-east-2` in September 2026. Check
[EFS pricing](https://aws.amazon.com/efs/pricing/),
[AWS Backup pricing](https://aws.amazon.com/backup/pricing/) and
[EBS pricing](https://aws.amazon.com/ebs/pricing/) before you start.

- **Nothing in this module has an hourly charge except the two EC2
  clients.** Two `t4g.micro` instances cost about $0.0084 an hour each,
  plus $0.005 an hour for each public IPv4 address if you use the default
  VPC. Stop them (or delete the stack) between sessions.
- **EFS storage** is charged per GB-month: about $0.30 in Standard, $0.016
  in Infrequent Access and $0.008 in Archive. Elastic throughput adds about
  $0.03 per GB read and $0.06 per GB written. The labs write well under a
  gigabyte, so EFS costs cents. IA and Archive bill every file as at least
  128 KiB, and Archive has a 90-day minimum storage duration.
- **AWS Backup storage:** EFS backups cost about $0.05 per GB-month (warm)
  and $0.01 (cold, with a 90-day minimum). EBS backups are billed as EBS
  snapshots (about $0.05 per GB-month). Restoring EFS data costs about
  $0.02 per GB.
- **Restore testing** charges a fixed fee of **$1.50 for each recovery
  point it restores**, on every run, plus the cost of the restored
  resource while it exists. A daily plan left running costs about $45 a
  month per protected resource. Lab 23.2.5 runs it once and deletes it.
- **Cross-Region copies pay twice:** once to move the data (an AWS Backup
  EFS copy from `us-east-2` to `us-east-1` is $0.04 per GB; EBS snapshot
  copies and S3 replication pay EC2/S3 inter-Region transfer), and again to
  store a full copy in the second Region. The first copy of an EBS snapshot
  to a new Region is a full copy, not an incremental one. S3 Replication
  Time Control adds $0.015 per GB. Time-based EBS snapshot copies add
  $0.005 to $0.020 per GiB, depending on the completion time you ask for.
  <!-- VERIFY: inter-Region data transfer rate between us-east-2 and the
  student's DR Region (historically $0.01/GB to us-east-1, $0.02/GB to
  most others). -->
- **Vault Lock in compliance mode is irreversible.** After its grace time
  (at least 3 days) ends, nobody, not you, not the root user, not AWS
  Support, can remove the lock or delete a recovery point before its
  retention ends, and you pay for that storage the whole time. A recovery
  point with no expiry in a compliance-locked vault is billed forever.
  **This course uses governance mode only.** Never pass
  `--changeable-for-days` to `put-backup-vault-lock-configuration`, and
  never put `ChangeableForDays` in a CloudFormation template. That one
  parameter is what turns a lock into compliance mode.
- **Cleanup:** [Lab 23.3.6](#lab-2336-clean-up-the-module) removes
  everything, in both Regions. Recovery points, snapshot copies, replica
  buckets and replicated file systems are not part of any stack, so
  deleting stacks is not enough.

## Guidance

- Explore the official docs! See the
  [Amazon EFS User Guide](https://docs.aws.amazon.com/efs/latest/ug/whatisefs.html),
  [AWS Backup Developer Guide](https://docs.aws.amazon.com/aws-backup/latest/devguide/whatisbackup.html),
  and the CLI references for
  [efs](https://docs.aws.amazon.com/cli/latest/reference/efs/index.html)
  and
  [backup](https://docs.aws.amazon.com/cli/latest/reference/backup/index.html).
  The CloudFormation resource types are under
  [Amazon EFS](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/AWS_EFS.html)
  and
  [AWS Backup](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/AWS_Backup.html).

- Read the whitepaper
  [Disaster Recovery of Workloads on AWS](https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-workloads-on-aws.html)
  before Lesson 23.3. Most exam questions about DR strategies are answered
  by its "Disaster recovery options in the cloud" section.

- Avoid using other sites like stackoverflow.com for answers \-- part
  of the skill set you're building is finding answers straight from
  the source, AWS. Posts written before late 2023 describe EFS without
  Elastic throughput or the Archive class, and AWS Backup without restore
  testing.

- Explore your curiosity. Try to understand why things work the way
  they do. Read more of the documentation than just what you need to
  find the answers.

## Conventions

- **Profile and Region.** Every lab uses the `lab` profile from module 19,
  whose Region is `us-east-2`. CLI examples don't pass `--region` except
  where a lab is about a second Region.
- **The DR Region.** Lesson 23.3 needs a second Region, called
  `<dr-region>` in this README. Choose it the way you did in module 01:
  an enabled Region, close enough that transfer is cheap. **`us-east-1` is
  the easy choice**, because the module 19 region guardrail already allows
  it. If you want a different Region, add it to the guardrail SCP from the
  management account before Lesson 23.3 and take it out again after
  Lab 23.3.6. In DR-Region commands, pass `--region <dr-region>`
  explicitly.
- **Session Manager, not SSH.** The starter template gives the clients
  the `AmazonSSMManagedInstanceCore` policy and a security group with no
  inbound rules. Connect with `aws ssm start-session --target <instance-id>`,
  which needs the
  [Session Manager plugin](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-install-plugin.html)
  on your machine. Module 04 introduced it; module 20 covers it in depth.
- **Placeholders.** `<you>` is your identifier, `123456789012` stands for
  the lab account ID, and IDs such as `fs-0123456789abcdef0` are examples.
  Don't commit real account IDs or ARNs from your account to your answers.
- **Templates.** Write your CloudFormation in YAML, run `cfn-lint` on it
  before you deploy (module 01), and tag everything with `owner=<you>`.
- DO use the AWS CLI rather than the console, except where a step says the
  console is required.

## Lesson 23.1: Shared file storage with Amazon EFS

### Principle 23.1

*Amazon EFS is one elastic NFS file system for a whole Region. Mount
targets put it in your subnets; security groups, the file system policy
and access points decide who gets in and as whom.*

### Practice 23.1

EBS, from module 05, is a block device for one instance in one
Availability Zone. S3, from module 02, is object storage that you reach
with API calls. EFS sits between them: a POSIX file system that many
instances, containers and Lambda functions mount at once, over NFSv4,
from every Availability Zone in the Region. You don't provision capacity.
It grows and shrinks with the files you store, and you pay for what is
stored plus, with Elastic throughput, what is read and written.

Three layers control access, and the labs add them one at a time:

1. **Network:** a mount target in each Availability Zone, with a security
   group that allows NFS (TCP 2049) only from your clients.
2. **IAM:** a *file system policy* (a resource policy on the file system)
   that can require TLS, require IAM authentication and limit which
   principals may mount, write or act as root.
3. **POSIX:** an *access point* that forces a user and group ID and a
   root directory on every request that comes through it.

Start from the starter template
[starter/efs-clients.yaml](starter/efs-clients.yaml). It creates two
Amazon Linux 2023 clients in different Availability Zones, installs
`amazon-efs-utils`, and leaves the EFS resources to you. Copy it into your
repository as `efs.yaml`; you'll add to it throughout this lesson.

#### Lab 23.1.1: A file system with two mount targets

Read [How Amazon EFS works](https://docs.aws.amazon.com/efs/latest/ug/how-it-works.html),
[Managing mount targets](https://docs.aws.amazon.com/efs/latest/ug/accessing-fs.html)
and the
[`AWS::EFS::FileSystem`](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-efs-filesystem.html)
reference. Then add to your template:

- A security group for the mount targets that allows inbound TCP 2049
  from the clients' security group only. Reference the group, not a CIDR.

- A **Regional** file system (not One Zone) that is:
  - **encrypted at rest** with the AWS managed key. The console encrypts
    by default; the API, CLI and CloudFormation don't, and you can't turn
    encryption on later;
  - using the **Elastic** throughput mode and the General Purpose
    performance mode;
  - **not** enrolled in EFS automatic backups (set `BackupPolicy` to
    `DISABLED`). Lesson 23.2 builds backups you control instead;
  - tagged with `owner=<you>` and a `Name`.

- One mount target in each of the two subnets the clients use.

- Outputs for the file system ID and ARN.

Deploy the stack. The starter asks for a VPC and two subnets in different
Availability Zones. The default VPC works: its subnets give instances a
public IP address, which Session Manager and `dnf` need unless you add a
NAT gateway or VPC endpoints.

Then look at what you built:

- `aws efs describe-file-systems` for your file system. Find the
  encryption setting, throughput mode, `SizeInBytes` and the number of
  mount targets.
- `aws efs describe-mount-targets` and note each target's Availability
  Zone, IP address and network interface.

##### Question: Encryption at rest

_Your template has `Encrypted: true`. What happens to an existing,
unencrypted file system if you add that line and update the stack? How
would you get the data of an unencrypted file system onto an encrypted
one? (See
[Encrypting data at rest](https://docs.aws.amazon.com/efs/latest/ug/encryption-at-rest.html).)_

##### Question: One mount target per AZ

_Why does EFS allow only one mount target per Availability Zone per file
system? A client in a third Availability Zone with no mount target can
still mount the file system: what does that cost, and what does it risk?_

#### Lab 23.1.2: Mount it from two Availability Zones

Read [Mounting on EC2 Linux instances using the EFS mount
helper](https://docs.aws.amazon.com/efs/latest/ug/mounting-fs-mount-helper-ec2-linux.html)
and [Encrypting data in
transit](https://docs.aws.amazon.com/efs/latest/ug/encryption-in-transit.html).

- Start a Session Manager session on client A. Confirm the mount helper
  is installed (`rpm -q amazon-efs-utils`). The user data in the starter
  installed it with `dnf`.

- Mount the file system on `/mnt/efs` with the mount helper **and TLS**
  (`-o tls`). Create a directory and a file in it, and write a few lines
  of text.

- Start a session on client B, mount the file system the same way, and
  read the file. Append to it from B and read it again from A.

- Compare the output of `mount` and `df -h /mnt/efs` with what you
  expected. What server address does the NFS mount point at when TLS is
  on, and why?
  <!-- VERIFY: that efs-utils v2+ TLS mounts (efs-proxy) show a
  127.0.0.1 server address in mount/df output on AL2023. -->

- Unmount on both clients and mount again with an `/etc/fstab` entry
  using the `_netdev` and `tls` options. Test it with `sudo mount -a`
  rather than a reboot.

##### Question: Close-to-open

_Read [Data consistency in Amazon
EFS](https://docs.aws.amazon.com/efs/latest/ug/features.html#consistency).
When does a write on client A become visible on client B? What does that
mean for two instances writing the same log file?_

##### Question: EFS, EBS or S3

_For each of these, pick EFS, EBS or S3 and give one reason: (a) a
database's data directory; (b) a CMS's uploaded images, served by six
web servers behind a load balancer; (c) nightly exports kept for seven
years; (d) home directories for a fleet of build agents in three
Availability Zones. Since April 2026,
[S3 Files](https://aws.amazon.com/blogs/aws/launching-s3-files-making-s3-buckets-accessible-as-file-systems/)
can present an S3 bucket as an NFS file system too. When would you reach
for it instead of EFS?_

#### Lab 23.1.3: Access points and a file system policy

So far any client that can reach TCP 2049 can mount the file system, as
root, without TLS. Close that down.

Read [Working with access
points](https://docs.aws.amazon.com/efs/latest/ug/efs-access-points.html),
[Using IAM to control access to file
systems](https://docs.aws.amazon.com/efs/latest/ug/iam-access-control-nfs-efs.html)
and [Creating file system
policies](https://docs.aws.amazon.com/efs/latest/ug/create-file-system-policy.html).

- Add an
  [`AWS::EFS::AccessPoint`](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-efs-accesspoint.html)
  for an application called `app`:
  - POSIX user and group `1001`;
  - root directory `/app`, which EFS should create on first use, owned by
    `1001:1001` with permissions `0755`.

- Add a `FileSystemPolicy` to the file system that:
  - denies every request that isn't sent over TLS
    (`aws:SecureTransport`);
  - allows `elasticfilesystem:ClientMount` and
    `elasticfilesystem:ClientWrite` to the clients' IAM role (the starter
    outputs its ARN), but only through your access point
    (`elasticfilesystem:AccessPointArn`);
  - does **not** grant `elasticfilesystem:ClientRootAccess` to anyone.

- Update the stack, then test from client A. Record the exact command and
  result for each:
  - Negative: mount without `tls`.
  - Negative: mount with `tls` but without `iam`.
  - Negative: mount with `tls,iam` but without the access point.
  - Positive: mount with `tls,iam,accesspoint=<fsap-id>`. Write a file,
    then run `ls -ln` and `id`. Which UID owns the file, and which UID are
    you in the session?

- From client B, mount the same way and confirm it sees only the contents
  of `/app`, not the files you wrote in Lab 23.1.2.

##### Question: Where did the files from Lab 23.1.2 go?

_They are still in the file system. How would an administrator reach
them now, and what would you add to the policy to allow it for one
specific role only?_

##### Question: Root squashing

_Without `ClientRootAccess`, what happens when `root` on a client creates
a file? Why is that a sensible default for a shared file system, and
which setting in the console's "file system policy" editor does the same
thing?_

##### Question: Security groups and policies

_The mount target security group and the file system policy both limit
access. Give one attack each one stops that the other doesn't._

#### Lab 23.1.4: Lifecycle management and storage classes

Read [EFS storage
classes](https://docs.aws.amazon.com/efs/latest/ug/features.html#storage-classes)
and [Managing storage
lifecycle](https://docs.aws.amazon.com/efs/latest/ug/lifecycle-management-efs.html).

- Add `LifecyclePolicies` to your file system in the template:
  - files not read or written for 30 days move to Infrequent Access;
  - files not accessed for 90 days move to Archive;
  - a file in IA or Archive moves back to Standard on its first access.

- Update the stack and confirm with `aws efs describe-lifecycle-configuration`.

- As the access point user, write a 50 MB file and a hundred 4 KB files
  (`dd` and a shell loop will do). Look at `SizeInBytes` in
  `describe-file-systems`: it breaks the metered size down by storage
  class. It can take a while to update.

- *Optional, if you're keeping the stack overnight:* change the IA
  transition to `AFTER_1_DAY`, check the breakdown tomorrow, then set it
  back.

##### Question: What counts as access

_Does `ls -l` on a directory of IA files reset their lifecycle timers?
Does reading one? What does "move back on first access" cost you, and
when would you leave it off?_

##### Question: Small files

_Your hundred 4 KB files are billed as 128 KiB each if they tier to IA or
Archive. When is tiering small files to IA a bad deal? (Compare the
Standard and IA prices in the cost section.)_

##### Question: Archive and throughput

_Why can't a file system whose lifecycle policy uses Archive be switched
to Bursting or Provisioned throughput? Read [Amazon EFS performance
specifications](https://docs.aws.amazon.com/efs/latest/ug/performance.html)
and explain in one or two sentences how the three throughput modes are
billed._

### Retrospective 23.1

#### Question: Regional or One Zone

_One Zone file systems cost about half as much. Which of the four
workloads from Lab 23.1.2 could live with One Zone, and what does AWS do
automatically for One Zone file systems (read
[Backing up EFS file
systems](https://docs.aws.amazon.com/efs/latest/ug/awsbackup.html)) that
makes it less risky?_

#### Task: Containers and functions

_Read how
[Amazon ECS](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/efs-volumes.html)
and [AWS Lambda](https://docs.aws.amazon.com/lambda/latest/dg/configuration-filesystem.html)
mount EFS. Lambda can only mount through an access point. Sketch
(don't deploy) what you would add to `efs.yaml` so a Lambda function
could write to `/app`, and note what the function needs from the VPC._

## Lesson 23.2: AWS Backup

### Principle 23.2

*A backup is a policy, a place and a proof: a plan says when and how
long, a vault says where and who may delete, and a restore test proves
it works. A backup you have never restored is a hope.*

### Practice 23.2

In module 05 you took an EBS snapshot by hand. That works for one volume
on one day. AWS Backup turns it into policy for many resource types at
once (EBS, EC2, EFS, RDS and Aurora, DynamoDB, S3, FSx and more):

- A **backup plan** holds rules: a schedule, a start and completion
  window, a lifecycle (when to move to cold storage, when to delete) and
  optional copy actions to other vaults.
- A **resource assignment** (backup selection) says which resources a
  plan protects, usually by tag.
- A **backup vault** stores the recovery points, encrypted with a KMS
  key, behind a vault access policy and, optionally, a Vault Lock.
- **Restore testing** restores recovery points on a schedule, times the
  restore and deletes the result.

Keep the stack from Lesson 23.1 running. Write this lesson's resources in
a second template, `backup.yaml`, so that you can delete the backup
configuration without deleting the data it protects.

#### Lab 23.2.1: Opt-in, a vault and a role

Read [Getting started with AWS
Backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/getting-started.html)
and [Backup vaults](https://docs.aws.amazon.com/aws-backup/latest/devguide/vaults.html).

- Run `aws backup describe-region-settings`. Which resource types are
  opted in? Is EFS? Is EBS? Opt-in matters when a plan selects resources
  by tag; see "service opt-in" in [Assigning resources to a backup
  plan](https://docs.aws.amazon.com/aws-backup/latest/devguide/assigning-resources.html).

- In `backup.yaml`, create:
  - a backup vault named `<you>-vault`, tagged, using the default
    encryption. After deploying, find out which KMS key it uses;
  - an IAM role that AWS Backup can assume (`backup.amazonaws.com`), with
    the AWS managed policies
    [`AWSBackupServiceRolePolicyForBackup`](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AWSBackupServiceRolePolicyForBackup.html)
    and
    [`AWSBackupServiceRolePolicyForRestores`](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/AWSBackupServiceRolePolicyForRestores.html).
    The console creates `AWSBackupDefaultServiceRole` for you the first
    time; with the CLI and CloudFormation you create your own.

- Deploy it, and list the vaults in the Region. You may see vaults you
  didn't create (`Default`, or `aws/efs/automatic-backup-vault` if an EFS
  file system was ever created in the console with automatic backups on).

##### Question: Vault encryption

_Your EFS file system is encrypted with one key and your vault with
another. Which key protects the recovery point? Why do AWS's cross-account
backup guides recommend a customer managed key for the vault instead of
the AWS managed key? (See [Encryption for backups in AWS
Backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/encryption.html).)_

#### Lab 23.2.2: A backup plan that selects by tag

Read [Create a backup
plan](https://docs.aws.amazon.com/aws-backup/latest/devguide/creating-a-backup-plan.html)
and [Assigning resources to a backup
plan](https://docs.aws.amazon.com/aws-backup/latest/devguide/assigning-resources.html).

- Add to `backup.yaml`:
  - an
    [`AWS::Backup::BackupPlan`](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-backup-backupplan.html)
    named `<you>-daily` with one rule: a daily backup (cron expression, in
    a time zone you choose), a one-hour start window, and deletion after
    7 days. No cold storage: explain why in the question below;
  - an
    [`AWS::Backup::BackupSelection`](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-backup-backupselection.html)
    that uses your role and selects every resource tagged
    `backup-plan=<you>-daily`.

- Tag the EFS file system (in `efs.yaml`) and client A's root EBS volume
  (with `aws ec2 create-tags`) with `backup-plan=<you>-daily`.

- Deploy, then check the result the next day with
  `aws backup list-backup-jobs` and `list-recovery-points-by-backup-vault`.
  Lab 23.2.3 doesn't wait for the schedule, so carry on.

##### Question: Cold storage

_Why would a cold-storage transition make no sense with a 7-day
retention? What is the shortest total retention that allows cold storage,
and which of your two resource types can use it at all? (For EBS, see
what "cold" means in the backup plan docs.)_

##### Question: Tags as the contract

_Selecting by tag means anyone who can tag a resource can put it in, or
take it out of, a backup plan. What could go wrong? How would you use an
SCP (module 19) or AWS Backup Audit Manager to guard against it?_

#### Lab 23.2.3: Back up now, then restore

Read [Creating an on-demand
backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/recov-point-create-on-demand-backup.html),
[Restore an Amazon EFS file
system](https://docs.aws.amazon.com/aws-backup/latest/devguide/restoring-efs.html)
and [Restore an Amazon EBS
volume](https://docs.aws.amazon.com/aws-backup/latest/devguide/restoring-ebs.html).

**Back up.**

- Through the access point, write a file called `precious.txt` with a
  line of text and the current time.
- Start an on-demand backup of the file system into `<you>-vault` with
  `aws backup start-backup-job`, using your role and a lifecycle that
  deletes it after 7 days. Poll `describe-backup-job` until it completes.
  Note how long it took.
- Start an on-demand backup of client A's root volume the same way. How
  does the recovery point ARN differ from the EFS one? Look for the
  backup in `aws ec2 describe-snapshots --owner-ids self` too.

**Lose something.** Delete `precious.txt`, and change another file.

**Restore a file.**

- Get the restore metadata for the EFS recovery point with
  `get-recovery-point-restore-metadata`.
- Start an **item-level** restore of `/app/precious.txt` into the
  **existing** file system with `start-restore-job`
  (`newFileSystem=false`, `ItemsToRestore`). Poll `describe-restore-job`.
- Find the restored file. It is **not** back where it was: look for an
  `aws-backup-restore_<datetime>` directory at the root of the file
  system. You'll need a mount without the access point, so work out how
  to do that under the policy from Lab 23.1.3 (or mount as an
  administrator role you allow for this purpose).

**Restore a volume.**

- Restore the EBS recovery point to a **new volume** in client **B**'s
  Availability Zone. Attach it to client B, mount it read-only, and
  compare a file (for example `/etc/hostname`) with client A's. Both root
  file systems were made from the same AMI, so XFS will refuse to mount a
  second file system with the same UUID: find the mount option that
  allows it. Then unmount, detach and delete the restored volume.

##### Question: Your first RTO and RPO

_If `precious.txt` had been lost at the worst possible moment under the
daily plan from Lab 23.2.2, how much data would you have lost (RPO)? How
long did the item-level restore take from `start-restore-job` to the file
being readable (a measured RTO for one file)? What would change for a
full restore of a 5 TB file system? (See "Backup performance" in
[Backing up EFS file
systems](https://docs.aws.amazon.com/efs/latest/ug/awsbackup.html).)_

##### Question: Non-destructive restores

_Why does AWS Backup never overwrite an EFS file system in place? What
does that mean for your recovery runbook?_

##### Question: Snapshots you didn't take

_The EBS backup appeared in `describe-snapshots`. Should you delete it
there with `aws ec2 delete-snapshot`? Why or why not?_

#### Lab 23.2.4: Vault Lock in governance mode

**Warning: read this whole lab before you type anything.** Vault Lock
has two modes. In **compliance** mode, once the grace time ends, the lock
can never be removed and no recovery point can be deleted before its
retention ends, by anyone, including the root user and AWS. The only
thing that selects compliance mode is the `ChangeableForDays` parameter
(`--changeable-for-days` on the CLI). **Do not use it in this course.**
This lab uses **governance** mode, which an administrator can remove.

Read [AWS Backup Vault
Lock](https://docs.aws.amazon.com/aws-backup/latest/devguide/vault-lock.html)
from top to bottom first.

- Create a **second** vault, `<you>-locked`, with the CLI. Don't lock the
  vault your plan uses.

- Lock it in governance mode with `put-backup-vault-lock-configuration`,
  passing only the vault name, `--min-retention-days 1` and
  `--max-retention-days 7`. Before you press Enter, read the command back
  and confirm `--changeable-for-days` is not in it.

- `describe-backup-vault` on it. Note `Locked`, `MinRetentionDays`,
  `MaxRetentionDays`, and whether there is a `LockDate`.

- Test it:
  - Negative: start an on-demand EFS backup into `<you>-locked` whose
    lifecycle deletes it after **30** days. Why does the job fail, and
    where do you read the reason?
  - Positive: the same backup with a 2-day retention. Wait for it to
    complete.
  - Negative: `delete-recovery-point` on that recovery point.
  - Remove the lock with `delete-backup-vault-lock-configuration`.
  - Positive: `delete-recovery-point` again.

- Leave the vault unlocked. Lab 23.3.6 deletes it.

##### Question: Governance or compliance

_Who can remove a governance-mode lock? What would you need in place,
beyond Vault Lock, to stop a compromised administrator doing exactly what
you just did? (Think about SCPs, a separate backup account and
[logically air-gapped
vaults](https://docs.aws.amazon.com/aws-backup/latest/devguide/logicallyairgappedvault.html).)_

##### Question: The grace time

_In compliance mode, what can you still do during the grace time, what is
its minimum length, and what happens when it ends? What happens to a
compliance-locked vault if the account is closed?_

##### Task: A guardrail against compliance mode

_Find the IAM actions and condition keys AWS Backup supports for
`PutBackupVaultLockConfiguration` in the
[Service Authorization Reference](https://docs.aws.amazon.com/service-authorization/latest/reference/list_backup.html).
Write (don't attach) an SCP statement for the `Sandbox` OU that stops
anyone in the lab account from creating a compliance-mode lock by mistake,
while still allowing governance mode. Validate it with IAM Access
Analyzer, as in module 19._

#### Lab 23.2.5: Restore testing

Read [Restore
testing](https://docs.aws.amazon.com/aws-backup/latest/devguide/restore-testing.html)
and [Restore testing
validation](https://docs.aws.amazon.com/aws-backup/latest/devguide/restore-testing-validation.html).
Remember the cost: $1.50 for every recovery point restored, every run.

- Create a restore testing plan with `create-restore-testing-plan`:
  - a daily schedule a little after now (in UTC or with a time zone);
  - a one-hour start window;
  - recovery point selection: the **latest** snapshot recovery point in
    the last 7 days, from `<you>-vault` only.

- Add one selection with `create-restore-testing-selection`:
  - protected resource type `EFS`, and your file system's ARN (not a
    wildcard: that would test every EFS file system in the account);
  - your backup role;
  - a validation window of 1 hour, so the restored file system lives long
    enough to look at.

- When the plan has run, find its job with `list-restore-jobs
  --by-restore-testing-plan-arn <plan-arn>`. Note its `DeletionStatus`
  and `ValidationStatus`. Describe the restored file system: its name,
  its tags, and whether it has mount targets.

- *Optional:* report a validation result for the job with
  `put-restore-validation-result`, as a script would after checking the
  data.

- Then delete the selection and the plan (in that order), so it runs only
  once. Confirm within a day that the restored file system is gone.

##### Question: What a restore test proves

_The restore test succeeded. List three things it proved, and three
things about your recovery it did not prove (think about mount targets,
access points, the file system policy, DNS names and the application)._

##### Question: Which recovery point

_When would you choose `RANDOM_WITHIN_WINDOW` over
`LATEST_WITHIN_WINDOW`? What kind of failure does testing only the latest
backup miss?_

### Retrospective 23.2

#### Question: Backups and replication

_EFS and S3 both offer continuous replication (Lesson 23.3). Why is
replication not a substitute for backups? Describe one incident that
replication would make worse._

#### Question: Proving it to an auditor

_Read about [AWS Backup Audit
Manager](https://docs.aws.amazon.com/aws-backup/latest/devguide/aws-backup-audit-manager.html).
Which of its controls would have caught (a) a resource with no backup
plan, (b) backups kept for less than your policy requires, and (c)
restores that take longer than your RTO?_

## Lesson 23.3: Disaster recovery, RTO and RPO

### Principle 23.3

*RTO and RPO choose the strategy, and the strategy sets the bill. Decide
the numbers first, then build the cheapest thing that meets them, and
test it.*

### Practice 23.3

**Recovery point objective (RPO)** is how much data you can afford to
lose, measured in time. **Recovery time objective (RTO)** is how long you
can afford to be down. AWS's DR whitepaper arranges four strategies along
those two axes:

| Strategy | What runs in the DR Region before a disaster | Typical RPO / RTO |
|---|---|---|
| Backup and restore | Nothing but copies of backups; infrastructure is redeployed from code | Hours / hours to a day |
| Pilot light | Data stores kept in sync; application tier deployed but switched off | Minutes / tens of minutes |
| Warm standby | A scaled-down, fully working copy that can take traffic at once | Seconds to minutes / minutes |
| Multi-site active/active | Full production in each Region, all serving traffic | Near zero / near zero |

The RPO and RTO figures are orders of magnitude, not guarantees. Read the
[Disaster recovery options in the
cloud](https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html)
section for the detail, especially the difference between pilot light
(must be switched on) and warm standby (only needs scaling up), and why
failover should depend on data plane operations rather than control plane
ones.

Every strategy needs the data in the other Region first. That is what
these labs build, for the data you created in this module: EFS backups,
an EBS snapshot, an S3 bucket and, optionally, a live EFS replica.
Routing traffic between Regions is module 21 (Route 53 failover),
databases are module 22 (read replicas and Aurora global databases), and
failover orchestration is module 27 (Application Recovery Controller,
Resilience Hub).

#### Lab 23.3.1: Put numbers on it

No AWS resources in this lab. Imagine the file share from Lesson 23.1 is
the upload store of a small web application, and that the application
also keeps originals in an S3 bucket. The business says: "We can re-do
up to an hour of uploads by hand, and we can be down for half a day, but
not longer."

- Write a table in your README answer: for each component (EFS data, EBS
  root volumes, S3 originals, the infrastructure itself), state the RPO
  and RTO you'll design for, the AWS feature that meets it, and a rough
  monthly cost for 100 GB of data.
- Say which of the four strategies the result is, and what would have to
  change in the business requirement to move you one strategy up or down.

##### Question: The infrastructure is data too

_Your CloudFormation templates, AMIs and parameters are part of recovery.
Where does each of them live today, and would they be available if
`us-east-2` were down?_

#### Lab 23.3.2: Copy backups to your DR Region

Read [Creating backup copies across AWS
Regions](https://docs.aws.amazon.com/aws-backup/latest/devguide/cross-region-backup.html).

- Deploy a stack in `<dr-region>` (pass `--region`) that creates a vault
  `<you>-dr-vault`. Reuse a template: a vault is a vault.

- Add a copy action to the rule in your `<you>-daily` plan that copies
  each recovery point to the DR vault and deletes the copy after 7 days.
  The destination is a vault ARN; build it from a parameter, not a
  hard-coded account ID.

- Don't wait for the schedule. Copy your on-demand EFS recovery point
  from Lab 23.2.3 with `start-copy-job`. Poll `describe-copy-job`, then
  list the recovery points in the DR vault with `--region <dr-region>`.

- Restore the copy to a **new** file system in `<dr-region>`. Describe
  it. What does it lack that your `us-east-2` file system had? Delete it
  once you've answered.

##### Question: Cold copies

_AWS Backup doesn't copy recovery points that are already in cold
storage to another Region. How would you design the lifecycle of a
backup that must be kept for a year and also copied to a second
Region?_

##### Question: Which Region

_What makes a Region a good DR Region for `us-east-2`? Think about
distance, service availability, price, data residency and your SCP._

#### Lab 23.3.3: Copy an EBS snapshot by hand

AWS Backup did the copying in the previous lab. Do it once by hand so you
know what it does. This builds on the snapshot work in module 05.

Read [Copy an Amazon EBS
snapshot](https://docs.aws.amazon.com/ebs/latest/userguide/ebs-copy-snapshot.html).

- Create a snapshot of client B's root volume with
  `aws ec2 create-snapshot`, tagged with your identifier. Wait for it to
  complete.

- Copy it to `<dr-region>` with `aws ec2 copy-snapshot`. The command runs
  **in the destination Region**: pass `--region <dr-region>` and
  `--source-region us-east-2`. Tag the copy.

- Check the copy's encryption: `describe-snapshots --region <dr-region>`.
  Which key encrypted it, and why? (Your account may have [EBS encryption
  by default](https://docs.aws.amazon.com/ebs/latest/userguide/encryption-by-default.html)
  on in one Region and not the other: check with
  `get-ebs-encryption-by-default` in both.)

- *Optional, costs about $0.02 per GiB:* copy the same snapshot again as
  a [time-based
  copy](https://docs.aws.amazon.com/ebs/latest/userguide/time-based-copies.html)
  with a 15-minute completion duration. Compare `StartTime` and
  `CompletionTime` for both copies.

##### Question: Full or incremental

_Your first copy to `<dr-region>` was a full copy. Under what conditions
will the next copy of a newer snapshot of the same volume be
incremental? What breaks that chain?_

##### Question: Automating it

_You now know three ways to get EBS snapshots into another Region: by
hand, with an AWS Backup copy action, and with [Amazon Data Lifecycle
Manager](https://docs.aws.amazon.com/ebs/latest/userguide/snapshot-lifecycle.html)
cross-Region copy rules. When would you choose Data Lifecycle Manager over
AWS Backup?_

##### Question: Protecting snapshots from deletion

_Read about [Recycle
Bin](https://docs.aws.amazon.com/ebs/latest/userguide/recycle-bin.html)
and [EBS snapshot
lock](https://docs.aws.amazon.com/ebs/latest/userguide/ebs-snapshot-lock.html).
Which protects against an accidental `delete-snapshot`, which against a
malicious one, and how do they compare with Vault Lock?_

#### Lab 23.3.4: S3 Cross-Region Replication

Module 02 asked what replication needs you to turn on first. Now build
it. Read [Replicating objects within and across
Regions](https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication.html)
and [Configuring replication for buckets in the same
account](https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication-walkthrough1.html).

- Write a template for a **versioned** bucket and deploy it twice: once
  in `us-east-2` as the source, once in `<dr-region>` as the destination.
  Name the buckets with your identifier and the Region.

- In the source stack, add an IAM role that S3 can assume, with only the
  permissions replication needs, and a `ReplicationConfiguration` with one
  rule that replicates everything to the destination bucket. Leave delete
  marker replication **off**.

- Upload an object to the source. Check its `ReplicationStatus` with
  `aws s3api head-object` on the source and on the replica
  (`--region <dr-region>`) until it shows `COMPLETED` and `REPLICA`.

- Delete the object in the source (a plain `aws s3 rm`). Is it still
  readable in the destination? List the versions in both buckets and
  explain the difference.

- *Optional:* turn on [S3 Replication Time
  Control](https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication-time-control.html)
  for the rule and look at the replication metrics it publishes. It adds
  $0.015 per GB replicated plus CloudWatch metric charges; turn it off
  again when you've looked.

##### Question: Existing objects

_You created the replication rule after the bucket already held objects.
Were they replicated? What would you use to replicate them? (Look up S3
Batch Replication.)_

##### Question: Replication as DR

_S3 RTC is designed to replicate 99.9% of objects within 15 minutes. What
RPO does that let you promise for the S3 part of Lab 23.3.1? What does
replication not protect against that versioning, Object Lock or AWS
Backup for S3 would?_

#### Lab 23.3.5: EFS replication and failover (optional)

This lab creates a second file system in `<dr-region>` that stays in
sync with yours. It costs storage in both Regions and data transfer for
every change. Skip it if you're watching the bill, and read the pages
instead.

Read [Replicating EFS file
systems](https://docs.aws.amazon.com/efs/latest/ug/efs-replication.html)
and [Using the
replica](https://docs.aws.amazon.com/efs/latest/ug/replication-fail-over.html).

- Create a replication configuration from your file system to a **new**
  file system in `<dr-region>` with
  `aws efs create-replication-configuration`.
- Watch `describe-replication-configurations` until the initial sync
  finishes. Find the `TimeSinceLastSync` metric in CloudWatch for the
  source file system.
- Write a file through the access point in `us-east-2`. How long until
  the "last synced" time passes the moment you wrote it?
- Fail over: delete the replication configuration. What happens to the
  destination file system's write protection? (It has no mount targets
  yet; you'd create them in a real failover.)
- Delete the destination file system in `<dr-region>`.

##### Question: Replica RPO

_EFS replication aims for an RPO of 15 minutes for most file systems.
When can it take longer? Would EFS replication or a cross-Region backup
copy meet the one-hour RPO in Lab 23.3.1, and which is cheaper?_

#### Lab 23.3.6: Clean up the module

Resources in this module live in two Regions and several of them are not
in any stack. Work through this list in order, and check each Region at
the end.

1. **Restore testing:** confirm no restore testing plans remain
   (`list-restore-testing-plans`) and that the test-restored file system
   is gone.
2. **Replication:** delete any EFS replication configuration and the
   replica file system in `<dr-region>`. Delete the replication rule from
   the source bucket.
3. **Vault lock:** confirm `<you>-locked` has no lock
   (`describe-backup-vault` shows `"Locked": false`). If it's still
   locked in governance mode, remove the lock.
4. **Recovery points:** delete every recovery point in `<you>-vault`,
   `<you>-locked` and, with `--region <dr-region>`, `<you>-dr-vault`,
   using `delete-recovery-point`. Delete EBS backups here, not with
   `ec2 delete-snapshot`.
5. **Backup plan and vaults:** delete the `backup.yaml` stack (plan,
   selection, vault, role). Delete the `<you>-locked` vault and the DR
   vault stack. A vault that still holds recovery points can't be
   deleted.
6. **Snapshots and volumes:** delete the manual snapshot in `us-east-2`,
   both snapshot copies in `<dr-region>`, and any restored volume or file
   system you kept.
7. **Buckets:** empty both replication buckets, **including every object
   version and delete marker** (module 02, Lab 2.3.2), then delete their
   stacks.
8. **EFS and clients:** unmount on the clients, then delete the
   `efs.yaml` stack. It deletes the access point, mount targets, file
   system, security groups, instances and role.
9. **SCP:** if you added a Region to the module 19 region guardrail for
   this module, remove it from the management account.

Finally, with the `lab` profile, in **both** Regions:

- `aws backup list-backup-vaults` and `list-recovery-points-by-backup-vault`
  for anything left;
- `aws efs describe-file-systems`;
- `aws ec2 describe-snapshots --owner-ids self` and `describe-volumes`;
- `aws s3api list-buckets` for your replication buckets.

`AWS Backup` service-linked roles and the vaults called `Default` or
`aws/efs/automatic-backup-vault`, if they exist, cost nothing while they
are empty. Leave them.

### Retrospective 23.3

#### Question: Where the RTO really goes

_In a backup-and-restore DR plan, list everything that has to happen
between "`us-east-2` is down" and "users are back", and estimate each
step. Which steps are control plane operations in the DR Region, and why
does the whitepaper worry about that?_

#### Question: Pilot light or warm standby

_For the workload in Lab 23.3.1, what would pilot light add to what you
built, and what would warm standby add on top of that? Which service
quotas would you check in the DR Region before a disaster?_

#### Task: A DR runbook

_Write a one-page runbook for restoring the file share into `<dr-region>`
from the copied backups: who decides to fail over, the commands, how you
check the data, and how you fail back. Keep it in your repository; you'll
add Route 53 failover to it in module 21._

## Further Reading

- [Disaster Recovery of Workloads on
  AWS](https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-workloads-on-aws.html)
  (whitepaper), including its sections on testing DR.
- The [Reliability
  pillar](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/welcome.html)
  of the AWS Well-Architected Framework, "Plan for disaster recovery".
- [AWS Elastic Disaster
  Recovery](https://docs.aws.amazon.com/drs/latest/userguide/what-is-drs.html):
  block-level replication of servers into a pilot-light staging area.
- [Cross-account backup copies](https://docs.aws.amazon.com/aws-backup/latest/devguide/create-cross-account-backup.html)
  and [logically air-gapped
  vaults](https://docs.aws.amazon.com/aws-backup/latest/devguide/logicallyairgappedvault.html):
  keeping backups out of reach of a compromised workload account.
- [Amazon FSx](https://docs.aws.amazon.com/fsx/): managed Windows File
  Server, Lustre, NetApp ONTAP and OpenZFS file systems, the other
  shared-storage answers on the exams.
- [AWS DataSync](https://docs.aws.amazon.com/datasync/latest/userguide/what-is-datasync.html):
  moving data into and between EFS, FSx and S3.
