# Blog Notes: Module 02, S3

## Working title

Why `aws s3 sync --acl public-read` fails in 2026 (and what to do instead)

## Hook

Almost every S3 tutorial written before 2023 makes a bucket public with one
flag. Run that command against a bucket created today and it fails with
`AccessControlListNotSupported`, and switching to a public bucket policy fails
too. Nothing is broken: since April 2023 every new bucket starts with Block
Public Access on and ACLs disabled, and since January 2023 every object is
encrypted whether you ask or not. This post walks through the failure, what
the error is telling you, and the ways to share S3 data that replaced ACLs.

## Key points

1. **The two defaults behind the error.** Block Public Access (four settings,
   at bucket, account and organization level, most restrictive wins) and
   Object Ownership = Bucket owner enforced (ACLs disabled). Show how to read
   both with `get-public-access-block`, `s3control get-public-access-block`
   and `get-bucket-ownership-controls`.
1. **"Public" has a precise meaning.** A bucket policy that grants
   `Principal: "*"` is not public if it's limited by a fixed condition such as
   `aws:SourceIp` (narrower than /8), `aws:SourceVpce` or `aws:PrincipalOrgID`.
   `get-bucket-policy-status` tells you what S3 thinks.
1. **Pick the sharing tool by audience:** IAM policy for your own workloads,
   bucket policy with a condition for partners and networks, presigned URLs
   for one-off downloads, CloudFront with Origin Access Control for the
   public internet.
1. **If you must turn BPA off, do it narrowly:** one bucket, only
   `BlockPublicPolicy` and `RestrictPublicBuckets`, a `public/` prefix, and
   Access Analyzer watching. Never the account-level switch.
1. **Encryption is the same story.** SSE-S3 is automatic; the real decision
   is whose key (SSE-S3, `aws/s3`, customer managed key, DSSE-KMS) and turning
   on S3 Bucket Keys so SSE-KMS doesn't multiply your KMS bill. SSE-C has been
   blocked by default on new buckets since April 2026.

## Gotchas readers will hit

- `--acl bucket-owner-full-control` still works on ACL-disabled buckets; any
  other ACL fails. Old cross-account upload scripts often send it, which
  confuses people about what "ACLs disabled" means.
- The error from `put-bucket-policy` with a public policy is `AccessDenied`,
  which reads like a missing IAM permission, not a BPA block.
- A `Deny` in a bucket policy can lock out administrators; only the root user
  (or the management account's privileged root task) can remove it.
- Presigned URLs die when the signing credentials do. An Identity Center
  session that expires in an hour caps a "7 day" URL at an hour.
- `aws s3 rb --force` does not empty a versioned bucket, and CloudFormation
  won't delete a stack whose bucket still holds versions or delete markers.
- Changing default encryption doesn't re-encrypt existing objects.
- Lifecycle rules don't transition objects under 128 KB by default, so tiny
  test files never move.

<!-- VERIFY: capture the exact put-bucket-policy error text when BlockPublicPolicy is on while doing Lab 2.2.6. -->

## Exam objectives

- SAA-C03 Domain 1 (1.1 secure access, 1.3 data security controls) and
  Domain 4 (4.1 cost-optimized storage)
- SOA-C03 Domain 4: Security and Compliance; Domain 2: Reliability and
  Business Continuity
- SCS-C03 Domain 5: Data Protection
- CLF-C02 Domain 2: Security and Compliance
