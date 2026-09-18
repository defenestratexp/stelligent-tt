# Topic 10: Key Management Service (KMS)

<!-- TOC -->

- [Topic 10: Key Management Service (KMS)](#topic-10-key-management-service-kms)
  - [What changed in the 2026 edition](#what-changed-in-the-2026-edition)
  - [Exam coverage](#exam-coverage)
  - [Cost and cleanup](#cost-and-cleanup)
  - [Guidance](#guidance)
  - [Lesson 10.1: KMS Keys, Aliases and Key Policies](#lesson-101-kms-keys-aliases-and-key-policies)
    - [Principle 10.1](#principle-101)
    - [Practice 10.1](#practice-101)
      - [Lab 10.1.1: Create a KMS Key](#lab-1011-create-a-kms-key)
        - [Question: The Account Statement](#question-the-account-statement)
        - [Question: Lockout](#question-lockout)
      - [Lab 10.1.2: Create a KMS Alias](#lab-1012-create-a-kms-alias)
      - [Lab 10.1.3: Encrypt and Decrypt a Small Secret](#lab-1013-encrypt-and-decrypt-a-small-secret)
        - [Question: Decrypting the Ciphertext File](#question-decrypting-the-ciphertext-file)
        - [Question: Encryption Context](#question-encryption-context)
        - [Question: Size Limit](#question-size-limit)
    - [Retrospective 10.1](#retrospective-101)
      - [Question: KMS Alias](#question-kms-alias)
      - [Question: Kinds of Keys](#question-kinds-of-keys)
  - [Lesson 10.2: Who Can Use a Key](#lesson-102-who-can-use-a-key)
    - [Principle 10.2](#principle-102)
    - [Practice 10.2](#practice-102)
      - [Lab 10.2.1: A Second Principal of Your Own](#lab-1021-a-second-principal-of-your-own)
        - [Question: Denied](#question-denied)
      - [Lab 10.2.2: Allow Access with an IAM Policy](#lab-1022-allow-access-with-an-iam-policy)
        - [Question: Why the IAM Policy Worked](#question-why-the-iam-policy-worked)
      - [Lab 10.2.3: Allow Access with a Grant](#lab-1023-allow-access-with-a-grant)
        - [Question: Grant Tokens](#question-grant-tokens)
        - [Question: Retire or Revoke](#question-retire-or-revoke)
    - [Retrospective 10.2](#retrospective-102)
      - [Question: Choosing the Mechanism](#question-choosing-the-mechanism)
  - [Lesson 10.3: Envelope Encryption](#lesson-103-envelope-encryption)
    - [Principle 10.3](#principle-103)
    - [Practice 10.3](#practice-103)
      - [Lab 10.3.1: Generate a Data Key](#lab-1031-generate-a-data-key)
        - [Question: Two Copies](#question-two-copies)
      - [Lab 10.3.2: Client-Side Envelope Encryption with boto3](#lab-1032-client-side-envelope-encryption-with-boto3)
        - [Question: Moving the Object](#question-moving-the-object)
        - [Question: Client-Side and Server-Side](#question-client-side-and-server-side)
      - [Lab 10.3.3: Let a Library Do It](#lab-1033-let-a-library-do-it)
        - [Question: What the Library Adds](#question-what-the-library-adds)
    - [Retrospective 10.3](#retrospective-103)
      - [Question: Leaked Data Key](#question-leaked-data-key)
  - [Lesson 10.4: Key Lifecycle](#lesson-104-key-lifecycle)
    - [Principle 10.4](#principle-104)
    - [Practice 10.4](#practice-104)
      - [Lab 10.4.1: Rotation](#lab-1041-rotation)
        - [Question: What Rotation Changes](#question-what-rotation-changes)
        - [Question: Keys That Can't Rotate](#question-keys-that-cant-rotate)
      - [Lab 10.4.2: Multi-Region Keys](#lab-1042-multi-region-keys)
        - [Question: Same Key or Not](#question-same-key-or-not)
      - [Lab 10.4.3: Disable a Key](#lab-1043-disable-a-key)
      - [Lab 10.4.4: Clean Up](#lab-1044-clean-up)
        - [Question: Deleting the Stack](#question-deleting-the-stack)
    - [Retrospective 10.4](#retrospective-104)
      - [Question: Disable or Delete](#question-disable-or-delete)
      - [Question: When Multi-Region](#question-when-multi-region)
      - [Question: Bring Your Own Key](#question-bring-your-own-key)
  - [Further Reading](#further-reading)

<!-- /TOC -->

## What changed in the 2026 edition

- "Customer master key (CMK)" is gone. AWS now says **KMS key**, and splits
  them into customer managed keys, AWS managed keys (such as `aws/s3`) and AWS
  owned keys. Some API field names still say `CustomerMasterKeySpec`; the
  concept is the same.
- The labs work for one person. The old module had you send a ciphertext to
  a colleague with administrator access. Now you create a second IAM role in
  your lab account, assume it, and use it to see key policies, IAM policies
  and grants allow or deny access.
- New lesson on **who can use a key**: key policies, IAM policies and
  **grants**, including grant tokens and retiring or revoking a grant.
- The Ruby `Aws::S3::EncryptionV2::Client` lab is replaced by an
  **envelope encryption** lab in Python (boto3 and `cryptography`), followed by
  the same job done with the AWS Encryption SDK's command-line tool. The S3
  Encryption Client isn't available for Python.
- New lesson on the **key lifecycle**: automatic rotation with a configurable
  rotation period (90 to 2,560 days, added in 2024), on-demand rotation,
  **multi-Region keys**, disabling keys, and scheduling deletion.
- Key policies name your IAM Identity Center role instead of "your IAM user".
- This module builds on module 02, which already covers SSE-KMS, the
  `aws/s3` AWS managed key and S3 Bucket Keys. It doesn't repeat them.
- The pointers to `stelligent/crossing` and `stelligent/keystore` are gone.
  Neither has been updated since 2021.
- New: cost notes and a cleanup lab that schedules key deletion with the
  shortest waiting period.

## Exam coverage

| Exam | Domain / task statement |
|---|---|
| SAA-C03 | Domain 1: Design Secure Architectures (1.3 Determine appropriate data security controls: encryption at rest, key management, key rotation) |
| SCS-C03 | Domain 5: Data Protection (Task 5.2: controls for data at rest, client-side vs server-side encryption; Task 5.3: key materials, imported key material, keys across one or more Regions) |
| SCS-C03 | Domain 4: Identity and Access Management (key policies, grants, resource-based vs identity-based policies) |
| SOA-C03 | Domain 4: Security and Compliance (Skill 4.2.2: implement, configure and troubleshoot encryption at rest, for example AWS KMS) |
| DVA-C02 | Domain 2: Security (Task 2.2: implement encryption by using AWS services, including client-side encryption and key rotation). C03 adds GenAI / agent topics; its guide publishes 2026-10-27. |

## Cost and cleanup

- Each **customer managed KMS key** costs **$1 per month, prorated hourly**.
  That includes each multi-Region replica. This module creates three: one
  single-Region key, one multi-Region primary key and one replica. Kept for a
  week, they cost well under a dollar in total.
- The first and second **rotation** of a key each add another $1 per month
  (prorated). Later rotations are free. The on-demand rotation in Lab 10.4.1
  adds a few cents while the key exists.
- **API requests** cost $0.03 per 10,000 for symmetric keys, after a free tier
  of 20,000 requests per month across all Regions. These labs make a few
  hundred.
- **Deleting a key isn't immediate.** You schedule deletion with a waiting
  period of 7 to 30 days; the default is 30. Always choose **7** in this
  course, both in the template (`PendingWindowInDays`) and on the CLI. Keys
  pending deletion aren't charged. A multi-Region primary key can't even start
  its waiting period until every replica has been deleted.
- The S3 bucket from Lesson 10.3 costs cents.
- Lab 10.4.4 removes everything this module creates. Once the waiting period
  ends, anything you encrypted under these keys can never be decrypted again.
  That's the point: keep nothing encrypted under a lab key that you want back.

<!-- VERIFY: whether a multi-Region primary key in the PendingReplicaDeletion state is billed. The pricing page says keys "scheduled for deletion" are free but doesn't mention this state. -->

## Guidance

- Explore the official docs! See the
  [AWS KMS Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/overview.html),
  [API Reference](https://docs.aws.amazon.com/kms/latest/APIReference/Welcome.html),
  [CLI Reference](https://docs.aws.amazon.com/cli/latest/reference/kms/index.html),
  and
  [CloudFormation](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-kms-key.html)
  docs.

- Avoid using other sites like stackoverflow.com for answers \-- part
  of the skill set you're building is finding answers straight from
  the source, AWS. Many KMS tutorials still say "CMK" and predate
  configurable rotation, on-demand rotation and multi-Region keys.

- Explore your curiosity. Try to understand why things work the way
  they do. Read more of the documentation than just what you need to
  find the answers.

- Your AWS profile sets the lab region (`us-east-2`). KMS keys are regional,
  so the CLI commands in this module don't need `--region`, except in Lab
  10.4.2, which is about Regions.

- Use the CLI and CloudFormation. The KMS console is useful for looking at
  key policies and rotation history, but don't create keys there.

## Lesson 10.1: KMS Keys, Aliases and Key Policies

### Principle 10.1

*AWS KMS holds your keys so that nobody, including you, ever handles the key
material. You control who may use a key, and every use is logged.*

### Practice 10.1

A KMS key never leaves KMS unencrypted. You send data (or, more often, a data
key) to KMS and get back ciphertext or plaintext, if the key's policy allows
it. Every call is recorded in CloudTrail. The following labs introduce the
fundamental resources in KMS: KMS keys, their key policies, and aliases.

Read
[AWS KMS keys](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#kms_keys)
and [Key policies](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html)
before you start.

#### Lab 10.1.1: Create a KMS Key

Create a CloudFormation template that
[creates a symmetric encryption KMS key](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-kms-key.html).
You'll add to this stack throughout the module.

- Give it a description and tags that include your identifier.

- Set `PendingWindowInDays` to 7.

- Write the key policy yourself rather than taking the default:

  - Keep the statement that gives the account (`arn:aws:iam::<account>:root`,
    built with `AWS::AccountId`) full access. Read the
    [default key policy](https://docs.aws.amazon.com/kms/latest/developerguide/key-policy-default.html)
    page to understand what it does before you decide.

  - Make **your IAM Identity Center role** both a key administrator and a key
    user. The role that Identity Center creates for your permission set has a
    generated suffix and a path (`aws-reserved/sso.amazonaws.com/...`), so
    AWS recommends naming the account as the principal and matching the role
    ARN with `ArnLike` on `aws:PrincipalArn` and a wildcard. See
    [Referencing permission sets in resource policies and KMS key policies](https://docs.aws.amazon.com/singlesignon/latest/userguide/referencingpermissionsets.html).
    Pass the role ARN pattern in as a parameter.

- Look at the result with `aws kms describe-key` and
  `aws kms get-key-policy`.

An example ARN in these docs looks like
`arn:aws:iam::123456789012:role/...`. Never put your real account ID in the
template; use `AWS::AccountId`.

##### Question: The Account Statement

_What does the statement that grants `kms:*` to the account's root principal
actually allow? Does it let the root user in? Does it let every IAM
principal in the account use the key?_

##### Question: Lockout

_What is the key policy lockout safety check, and what would happen to your
key if you removed both the account statement and your own role from the
policy? How would you recover it?_

#### Lab 10.1.2: Create a KMS Alias

Update your template to add an
[AWS::KMS::Alias](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-kms-alias.html)
with a snazzy name that includes your identifier (aliases must start with
`alias/`, and `alias/aws/` is reserved for AWS managed keys). Point it at your
key.

- List aliases with `aws kms list-aliases` and find yours. Note the AWS
  managed aliases too; module 02 created `aws/s3` if you did Lab 2.4.2.

#### Lab 10.1.3: Encrypt and Decrypt a Small Secret

Use the
[aws kms encrypt](https://docs.aws.amazon.com/cli/latest/reference/kms/encrypt.html)
command to encrypt a plaintext file with a secret message (maybe the combo to
the safe, or your luggage password), using your alias as the key ID. Save the
ciphertext as a binary file. Then use
[aws kms decrypt](https://docs.aws.amazon.com/cli/latest/reference/kms/decrypt.html)
to get the message back into a new file.

- Use `fileb://` for binary input. The CLI returns ciphertext and plaintext
  base64-encoded; decode them before writing files.

- Encrypt a second copy with an
  [encryption context](https://docs.aws.amazon.com/kms/latest/developerguide/encrypt_context.html)
  such as `purpose=stelligent-u`. Try to decrypt it with no context, the
  wrong context and the right one.

- Keep the ciphertext files. You'll decrypt them again after rotating the key
  in Lesson 10.4.

##### Question: Decrypting the Ciphertext File

_For decrypting the ciphertext file, why didn't you have to specify a key? How
did you have permission to decrypt?_

##### Question: Encryption Context

_The encryption context isn't secret; it appears in CloudTrail in plaintext.
So what does it protect against? Where would you see it if you looked for
your `Decrypt` call in CloudTrail?_

##### Question: Size Limit

_Try to encrypt a file larger than 4 KB. What happens, and what does that
tell you about how KMS is meant to be used?_

### Retrospective 10.1

#### Question: KMS Alias

_Why is it beneficial to use a KMS alias? Can you use an alias in a key
policy or an IAM policy's `Resource` element? What can you do instead?_

(See [Aliases in AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/kms-alias.html).)

#### Question: Kinds of Keys

_Compare customer managed keys, AWS managed keys and AWS owned keys: who can
see the key policy, who can change it, who rotates the key, and which ones
you pay for._

## Lesson 10.2: Who Can Use a Key

### Principle 10.2

*A KMS key is usable only when its key policy says so. IAM policies and
grants add access only when the key policy lets them.*

### Practice 10.2

Every KMS key has exactly one key policy, and it is the root of access
control for that key. The account statement you kept in Lab 10.1.1 is what
lets IAM policies in your account grant access to the key at all.
[Grants](https://docs.aws.amazon.com/kms/latest/developerguide/grants.html)
are a third mechanism: temporary, narrowly scoped permissions that you create
and delete without editing any policy. AWS services use grants all the time,
for example when EBS attaches an encrypted volume.

You don't need a second person for these labs. You'll create a second
principal (an IAM role you can assume) and watch what it can and can't do.
Read
[How to determine access to a KMS key](https://docs.aws.amazon.com/kms/latest/developerguide/determining-access.html)
first.

#### Lab 10.2.1: A Second Principal of Your Own

Add an IAM role to your stack to play your colleague:

- Its trust policy lets **only your Identity Center role** assume it (the
  account as principal, with the same `aws:PrincipalArn` condition you used
  in the key policy).

- It has no permissions policies at all.

Assume the role with `aws sts assume-role` (or a CLI profile with
`role_arn` and `source_profile`), and as that role:

- Try to decrypt the ciphertext file from Lab 10.1.3.

- Try `aws kms describe-key` on your alias.

##### Question: Denied

_What error did you get? The key policy has a statement for the account. Why
wasn't that enough?_

#### Lab 10.2.2: Allow Access with an IAM Policy

Give the colleague role an inline policy that allows `kms:Decrypt` and
`kms:DescribeKey` on your key's ARN only. Update the stack and try again as
the role.

Then remove the policy so the role is back to having no permissions.

##### Question: Why the IAM Policy Worked

_Your key policy never mentions the colleague role. Why did an IAM policy
work? What would have happened if you had removed the account statement from
the key policy in Lab 10.1.1?_

#### Lab 10.2.3: Allow Access with a Grant

Use your own role to create a grant for the colleague role with
[aws kms create-grant](https://docs.aws.amazon.com/cli/latest/reference/kms/create-grant.html):

- Allow only the `Decrypt` operation.

- Add an encryption context constraint so that the grant only works for
  ciphertext encrypted with `purpose=stelligent-u`.

- Name your identity role as the retiring principal.

Save the grant ID and grant token from the output. As the colleague role:

- Decrypt the ciphertext that carries the encryption context. Use the grant
  token on the first attempt.

- Try to decrypt the ciphertext without the encryption context.

- Check `aws kms list-grants` as your own role.

Finally, retire the grant with `aws kms retire-grant` and confirm (allowing
for a short delay) that the colleague role is denied again.

##### Question: Grant Tokens

_Why does a grant token exist? What might happen if you skipped it in a
script that creates a grant and uses it immediately?_

(See [Using a grant token](https://docs.aws.amazon.com/kms/latest/developerguide/using-grant-token.html).)

##### Question: Retire or Revoke

_What is the difference between retiring and revoking a grant? Who can do
each?_

### Retrospective 10.2

Look up your `CreateGrant`, `Decrypt` and `RetireGrant` calls in CloudTrail
event history with `aws cloudtrail lookup-events`. Can you tell which
principal made each call and which grant authorized the decrypt?

#### Question: Choosing the Mechanism

_For each case, which would you use: the key policy, an IAM policy, or a
grant? (a) Your security team must be able to administer every key, even if
IAM policies change. (b) A Lambda function in your account needs to decrypt
one secret. (c) A batch job needs to decrypt data for one hour, then lose
access. (d) Another AWS account needs to encrypt data with your key._

## Lesson 10.3: Envelope Encryption

### Principle 10.3

*KMS keys encrypt keys, not data. Encrypt your data locally with a data key,
and let KMS protect the data key.*

### Practice 10.3

KMS won't encrypt more than 4 KB, and sending every byte to KMS would be slow
and expensive anyway.
[Envelope encryption](https://docs.aws.amazon.com/kms/latest/developerguide/kms-cryptography.html#enveloping)
solves this: ask KMS for a
[data key](https://docs.aws.amazon.com/kms/latest/developerguide/data-keys.html),
encrypt the data locally with the plaintext copy, throw the plaintext copy
away, and store the encrypted copy next to the ciphertext. To decrypt, send
only the small encrypted data key to KMS.

This is what SSE-KMS does inside S3 (module 02), and what S3 Bucket Keys
optimize. In these labs you do it yourself on the client side, so the data is
encrypted before S3 ever sees it. The old version of this module used the Ruby
S3 Encryption Client. The
[Amazon S3 Encryption Client](https://docs.aws.amazon.com/amazon-s3-encryption-client/latest/developerguide/what-is-s3-encryption-client.html)
is still available for Java, Go, .NET, Ruby, C++ and PHP, but not for Python.
Here you'll build the envelope yourself with boto3 to see how it works, then
compare it with the AWS Encryption SDK.

Add an S3 bucket to your stack for these labs. Leave its default encryption
as SSE-S3.

#### Lab 10.3.1: Generate a Data Key

Call
[aws kms generate-data-key](https://docs.aws.amazon.com/cli/latest/reference/kms/generate-data-key.html)
with your alias and `--key-spec AES_256`.

- Look at the two fields that come back, and at their sizes once decoded.

- Decrypt the `CiphertextBlob` with `aws kms decrypt` and compare it with the
  `Plaintext` field.

- Look up `generate-data-key-without-plaintext` and note when you would use
  it.

##### Question: Two Copies

_Why does KMS return the data key twice? Which copy do you store, and which
do you destroy as soon as you've used it?_

#### Lab 10.3.2: Client-Side Envelope Encryption with boto3

Write a Python script using [boto3](https://docs.aws.amazon.com/boto3/latest/)
(and the [`cryptography`](https://cryptography.io/en/latest/) package for
AES-GCM) that:

- Asks KMS for a data key under your alias
  ([`generate_data_key`](https://docs.aws.amazon.com/boto3/latest/reference/services/kms/client/generate_data_key.html)),
  with an encryption context that names the bucket and the object key the
  file will be stored under.

- Encrypts a local file with AES-256-GCM using the plaintext data key and a
  random 96-bit nonce, then drops every reference to the plaintext key.

- Uploads the ciphertext to your bucket with `put_object`, storing the
  encrypted data key and the nonce (base64-encoded) as
  [object metadata](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingMetadata.html).

- Reads the object back with `get_object` and prints the first bytes, so you
  can see it's ciphertext.

- Downloads the object, decrypts the data key with KMS (passing the same
  encryption context), decrypts the file locally, and saves it under a new
  name. Compare it with the original.

Take the bucket name and alias as arguments or environment variables. Don't
hard-code them, and never write the plaintext data key to disk or a log.

##### Question: Moving the Object

_Copy the encrypted object to a different key in the bucket (`aws s3 cp`
keeps the metadata) and run your decrypt step on the copy. What happens, and
why is that a feature?_

##### Question: Client-Side and Server-Side

_Your object was encrypted by your script and then encrypted again by S3 with
SSE-S3. What does each layer protect against? Who can read the object if
they have `s3:GetObject` but not `kms:Decrypt` on your key?_

#### Lab 10.3.3: Let a Library Do It

Hand-built envelopes work, but they are easy to get subtly wrong. The
[AWS Encryption SDK](https://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/introduction.html)
does envelope encryption for you and writes a portable, documented message
format. Its command-line tool, the
[AWS Encryption CLI](https://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/crypto-cli.html),
is built on the Python implementation.

- Install the CLI (`aws-encryption-sdk-cli`, version 4.x) into a Python
  virtual environment. Versions before 4.0.0 are end of support.

- Encrypt the same file you used in Lab 10.3.2 with `--wrapping-keys` set to
  your key's ARN, an encryption context, and `--metadata-output` so you can
  read what it did.

- Decrypt it with `--max-encrypted-data-keys 1` and `--buffer`. Note that
  decrypt needs the key ARN, not the alias.

- Optional: do the same in Python with the
  [AWS Encryption SDK for Python](https://docs.aws.amazon.com/encryption-sdk/latest/developer-guide/python.html)
  and an AWS KMS keyring.

##### Question: What the Library Adds

_Compare the SDK's output with your own format from Lab 10.3.2. What does the
Encryption SDK do that your script doesn't? Look up key commitment,
algorithm suites with signing, and encrypting under several wrapping keys at
once._

### Retrospective 10.3

#### Question: Leaked Data Key

_Suppose one plaintext data key from your script ended up in a log file. What
data is exposed? Does rotating or disabling the KMS key fix it? What would
you do instead?_

## Lesson 10.4: Key Lifecycle

### Principle 10.4

*A key has a lifecycle: it rotates, it may need to exist in more than one
Region, and it is eventually retired. Deleting a key deletes every piece of
data that depends on it.*

### Practice 10.4

These labs walk your key through the rest of its life. Read
[Rotate AWS KMS keys](https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html),
[Multi-Region keys](https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html)
and [Delete an AWS KMS key](https://docs.aws.amazon.com/kms/latest/developerguide/deleting-keys.html)
first.

#### Lab 10.4.1: Rotation

Automatic rotation is off by default on customer managed keys.

- In your template, turn on `EnableKeyRotation` and set
  `RotationPeriodInDays` to the shortest period allowed. Update the stack and
  check the result with `aws kms get-key-rotation-status`. When is the next
  rotation?

- Rotate the key now with
  [aws kms rotate-key-on-demand](https://docs.aws.amazon.com/cli/latest/reference/kms/rotate-key-on-demand.html).
  Watch `get-key-rotation-status` until the on-demand rotation finishes, then
  list the rotations with `aws kms list-key-rotations`.

- Decrypt the ciphertext files from Lab 10.1.3 again. Encrypt something new
  and compare the key ID in the output with the key ID from before.

##### Question: What Rotation Changes

_After rotation, which things changed and which stayed the same: the key ID,
the key ARN, the alias, the key policy, the key material, your old
ciphertext? Why did your old ciphertext still decrypt?_

##### Question: Keys That Can't Rotate

_Which kinds of KMS keys support automatic rotation, which support only
on-demand rotation, and which you have to rotate "manually"? What does manual
rotation involve, and why is an alias essential for it? How many on-demand
rotations can you do per key?_

#### Lab 10.4.2: Multi-Region Keys

A multi-Region key is a set of keys in different Regions with the same key ID
and key material, so data encrypted in one Region can be decrypted in another
without a cross-Region call. This lab is about Regions, so here you pass
`--region` explicitly.

- Add a second KMS key to your stack with `MultiRegion: true`, its own alias,
  the same kind of key policy as your first key, and `PendingWindowInDays: 7`.
  Look at its key ID. What's different?

- Create a replica in `us-east-1`: either a second stack deployed there with
  an
  [AWS::KMS::ReplicaKey](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-kms-replicakey.html)
  (pass the primary key ARN as a parameter), or
  [aws kms replicate-key](https://docs.aws.amazon.com/cli/latest/reference/kms/replicate-key.html).
  If you use the CLI, give the replica a key policy; otherwise it gets the
  default one. Prefer the stack.

- Encrypt a secret with the primary key in `us-east-2`, then decrypt it with
  `--region us-east-1`.

- Compare `describe-key` and `get-key-policy` for the primary and the replica.

##### Question: Same Key or Not

_Which properties do the primary and replica share, and which are
independent? If you disable the primary, can you still decrypt with the
replica? Where can you turn on rotation?_

#### Lab 10.4.3: Disable a Key

Before deleting a key, AWS recommends disabling it first, to find out whether
anything still needs it.

- Disable your single-Region key with `aws kms disable-key` and try to
  decrypt one of your ciphertext files. Save the error.

- Re-enable it with `aws kms enable-key`, and decrypt again.

- Look up the CloudTrail events for the failed and successful calls. A
  [CloudWatch alarm on attempts to use a disabled or pending-deletion key](https://docs.aws.amazon.com/kms/latest/developerguide/deleting-keys-creating-cloudwatch-alarm.html)
  is how you'd catch a forgotten dependency in production.

#### Lab 10.4.4: Clean Up

Remove everything this module created:

- Empty the S3 bucket from Lesson 10.3.

- Delete the replica first: delete the replica stack in `us-east-1`, or run
  `aws kms schedule-key-deletion --pending-window-in-days 7 --region us-east-1`
  on the replica if you created it with the CLI.

- Delete your main stack. It removes the bucket, the colleague role and the
  aliases, and schedules both keys for deletion with the 7-day window you set
  in `PendingWindowInDays`.

- Schedule deletion (7 days) of any key you created outside CloudFormation.

- Confirm with `aws kms describe-key` that each key is in the
  `PendingDeletion` or `PendingReplicaDeletion` state, and note the
  `DeletionDate`. Check both Regions.

- Delete the local ciphertext files, or accept that they become unreadable
  when the keys are deleted.

##### Question: Deleting the Stack

_What happened to your KMS keys when you deleted the stack? Why doesn't
CloudFormation delete them immediately? Why is the multi-Region primary key
in a different state from the single-Region key?_

### Retrospective 10.4

#### Question: Disable or Delete

_While a key is pending deletion, how could you find out whether something
still uses it? What does
[How unusable KMS keys affect data keys](https://docs.aws.amazon.com/kms/latest/developerguide/unusable-kms-keys.html)
say about an EBS volume that is already attached when its key is disabled?_

#### Question: When Multi-Region

_AWS recommends single-Region keys for most workloads. Why? Give one case
where a multi-Region key is the right choice, and say how S3 cross-Region
replication treats a multi-Region key._

#### Question: Bring Your Own Key

_Some compliance rules require that you generate the key material yourself.
Read
[Importing key material](https://docs.aws.amazon.com/kms/latest/developerguide/importing-keys.html).
What do you gain and what do you take on compared with key material that KMS
generates? How does rotation work for a key with imported material?_

## Further Reading

- The [AWS KMS best practices](https://docs.aws.amazon.com/prescriptive-guidance/latest/aws-kms-best-practices/introduction.html)
  guide covers key policies, least privilege, rotation and monitoring in more
  depth than the labs.

- [AWS services integrated with AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/service-integration.html)
  lists every service that can encrypt with your keys. Pick one you use (EBS,
  RDS, Secrets Manager, Lambda environment variables) and read its
  *Encryption at rest* page to see how it uses grants and data keys.

- [ABAC for AWS KMS](https://docs.aws.amazon.com/kms/latest/developerguide/abac.html)
  shows how to control access with aliases and tags instead of key ARNs.

- [AWS KMS cryptographic details](https://docs.aws.amazon.com/kms/latest/cryptographic-details/intro.html)
  explains how keys are protected inside KMS's hardware security modules.

- [AWS CloudHSM](https://docs.aws.amazon.com/cloudhsm/latest/userguide/introduction.html)
  and [KMS custom key stores](https://docs.aws.amazon.com/kms/latest/developerguide/key-store-overview.html)
  are the options when you need single-tenant HSMs or keys held outside AWS.

- Module 11 uses KMS keys to protect Parameter Store `SecureString`
  parameters and Secrets Manager secrets.
