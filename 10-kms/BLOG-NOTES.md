# Blog Notes: Module 10, KMS

## Working title

KMS without a second person: key policies, grants and envelope encryption,
solo, in 2026

## Hook

The 2022 version of this lesson called them "CMKs", had you email a
ciphertext to a colleague with admin rights so they could decrypt it, and
did client-side encryption with a Ruby S3 client. Since then AWS renamed the
concept (it's a *KMS key* now), made rotation configurable (anywhere from 90
days to 7 years) and added on-demand rotation, capped rotation pricing, and
made multi-Region keys a normal part of DR designs. This post rebuilds the
lesson so one person in one lab account can see every layer: who can use a
key, how envelope encryption actually works, and what happens when a key
rotates, gets replicated, and is finally deleted.

## Key points

1. **The key policy is the root of access.** The "account" statement in the
   default key policy doesn't let everyone in; it lets IAM policies count.
   Demonstrate with a second role you assume yourself: denied, then allowed
   by an IAM policy, then allowed by a grant.
1. **Grants are for temporary, narrow access.** Encryption-context
   constraints, grant tokens for eventual consistency, retire vs revoke. This
   is how EBS, RDS and friends use your keys behind the scenes.
1. **Envelope encryption by hand, then with a library.** `GenerateDataKey`,
   AES-GCM locally, store the encrypted data key with the object, and bind it
   with an encryption context (show that a copied object fails to decrypt).
   Then do it properly with the AWS Encryption CLI and explain what the
   library adds (key commitment, signing, multiple wrapping keys).
1. **Rotation changes key material, not the key.** Same key ID, ARN, alias
   and policy; old ciphertext still decrypts. Custom period 90–2,560 days,
   up to 25 on-demand rotations per key, and only the first two rotations
   add to the bill.
1. **Multi-Region keys share material, not policy.** Same `mrk-` key ID and
   material in each Region; key policies, grants, aliases and enabled state
   are independent. AWS still recommends single-Region keys by default.
1. **Deletion is a 7–30 day countdown, and then data is gone.** Disable
   first, alarm on attempted use, and remember a multi-Region primary waits
   for its replicas.

## Gotchas readers will hit

- The CLI returns ciphertext and plaintext base64-encoded; forgetting to
  decode (or using `file://` instead of `fileb://`) gives confusing
  `InvalidCiphertextException` errors.
- `Encrypt` accepts at most 4,096 bytes. Bigger files need envelope
  encryption.
- Identity Center roles have a path and a generated suffix. Put the account
  in `Principal` and match the role with `ArnLike` on `aws:PrincipalArn`.
- A brand-new grant may not work for a few seconds without its grant token.
- The Encryption CLI's decrypt needs the key ARN, not an alias.
- The S3 Encryption Client has no Python implementation, which is why the
  lab builds the envelope with boto3 and `cryptography`.
- Deleting a CloudFormation stack doesn't delete a KMS key; it schedules
  deletion using `PendingWindowInDays` (default 30). Set it to 7 in labs.
- A multi-Region primary key sits in `PendingReplicaDeletion` until every
  replica is gone, then starts its own waiting period.

<!-- VERIFY: capture the exact AccessDenied message for the colleague role in Lab 10.2.1 and the error for a mismatched encryption context in Lab 10.3.2 while doing the labs. -->

## Exam objectives

- SAA-C03 Domain 1: Design Secure Architectures (1.3 data security controls)
- SCS-C03 Domain 5: Data Protection (Tasks 5.2 and 5.3) and Domain 4:
  Identity and Access Management
- SOA-C03 Domain 4: Security and Compliance (Skill 4.2.2 encryption at rest)
- DVA-C02 Domain 2: Security (Task 2.2 encryption with AWS services)
