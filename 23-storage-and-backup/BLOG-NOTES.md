# Blog notes: Topic 23, Storage and Backup

## Working title

Backups you've actually restored: EFS, AWS Backup and a DR plan with
numbers on it

## Hook

The 2022 version of this course had no backup module at all. You took one
EBS snapshot in the EC2 module and moved on. That matches how a lot of
real systems are run: something takes backups, nobody has restored one,
and "DR" means a diagram. In 2026 AWS gives you the pieces to do better
without much money: AWS Backup plans that pick resources by tag, restore
testing that restores your backups on a schedule and times it, Vault Lock
to stop anyone deleting them, and cheap cross-Region copies. This post
builds a shared EFS file system, backs it up, restores a single deleted
file, proves the restore works automatically, and then puts real RPO and
RTO numbers on a small workload and picks the DR strategy they call for.

## Key points

1. **EFS has three access layers.** The mount target security group
   (network), the file system policy (IAM: require TLS, require IAM auth,
   no root) and access points (POSIX user and root directory). Show the
   four mount attempts: no TLS, no IAM, no access point, all three.
2. **EFS storage classes and lifecycle.** Standard, IA and Archive
   (November 2023); Archive needs Elastic throughput; IA and Archive bill
   each file as at least 128 KiB; "move back to Standard on first access".
3. **AWS Backup is policy, place and proof.** A plan (schedule,
   retention, copy actions), a vault (key, access policy, lock) and restore
   testing ($1.50 per recovery point per run, so run it deliberately).
4. **Restores are non-destructive.** An EFS restore never overwrites: the
   file comes back in `aws-backup-restore_<datetime>/`. Your runbook has
   to include moving it back.
5. **Vault Lock: governance vs compliance.** Compliance mode becomes
   permanent after a grace time of at least 3 days and is selected by one
   parameter, `ChangeableForDays`. Show a governance-mode lock blocking a
   delete, then being removed. Mention the `backup:ChangeableForDays`
   condition key for an SCP that blocks compliance mode by accident.
6. **RTO and RPO pick the strategy.** Backup and restore, pilot light,
   warm standby, multi-site active/active, with what each keeps running in
   the DR Region. Replication is not a backup: it faithfully copies your
   mistakes.

## Gotchas readers will hit

- EFS created with the CLI, API or CloudFormation is **not encrypted** at
  rest unless you say so, and it can't be encrypted later. The console
  defaults the other way.
- The console turns on EFS automatic backups; CloudFormation and the CLI
  don't (except for One Zone). The automatic backup vault's access policy
  denies deleting its recovery points.
- A file system policy without `ClientRootAccess` squashes root, so
  `sudo touch` fails on a mount that works for reading.
- `amazon-efs-utils` is in the AL2023 repositories; install it with `dnf`.
  TLS mounts go through a local proxy, so `mount` doesn't show the mount
  target's address.
- Selecting backups by tag also depends on service opt-in; explicitly
  listed ARNs don't.
- AWS Backup's EBS backups show up as ordinary EBS snapshots. Delete them
  through AWS Backup, not `ec2 delete-snapshot`.
- Restoring a root volume backup and mounting it next to the original
  fails on XFS because of the duplicate UUID.
- AWS Backup doesn't copy cold-tier recovery points across Regions, and
  cold storage needs a total retention of at least 90 days.
- The first EBS snapshot copy to a new Region is full, not incremental,
  and so is any copy that changes the KMS key.
- S3 replication doesn't replicate delete markers unless told to, and
  doesn't touch objects that existed before the rule (Batch Replication
  does).
- A region guardrail SCP from the multi-account module blocks the DR
  Region unless you picked `us-east-1` or added it.
- Cleanup spans two Regions and lots of things no stack owns: recovery
  points, copies, replica buckets with versions, replicated file systems.

## Exam objectives supported

- SAA-C03 Domain 2: Design Resilient Architectures (Task 2.2: DR
  strategies, RPO and RTO, data durability and backups)
- SAA-C03 Domain 3: Design High-Performing Architectures (Task 3.1:
  storage solutions)
- SAA-C03 Domain 4: Design Cost-Optimized Architectures (Task 4.1:
  cost-optimized storage)
- SOA-C03 Domain 1, Skill 1.3.4: shared storage and EFS lifecycle
  policies
- SOA-C03 Domain 2, Task 2.3: backup and restore strategies (Skills 2.3.1
  and 2.3.4)

## Material to capture while doing the labs

- The four EFS mount attempts from Lab 23.1.3 and their error messages.
- `describe-file-systems` output showing `SizeInBytes` split across
  Standard, IA and Archive after a day with a short lifecycle policy.
- Timestamps for one item-level restore (start to readable file), and
  the restore testing job's reported duration: the first real RTO numbers.
- The failed backup job message when retention exceeds the vault lock's
  maximum.
- The RTO/RPO table from Lab 23.3.1, redrawn as a diagram of the four
  strategies with this workload's pieces placed on it.
- The monthly cost of each DR option for 100 GB, from the pricing pages.
