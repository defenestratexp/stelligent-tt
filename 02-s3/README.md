# Topic 2: Simple Storage Service (S3)

<!-- TOC -->

- [Topic 2: Simple Storage Service (S3)](#topic-2-simple-storage-service-s3)
  - [What changed in the 2026 edition](#what-changed-in-the-2026-edition)
  - [Exam coverage](#exam-coverage)
  - [Cost and cleanup](#cost-and-cleanup)
  - [Guidance](#guidance)
  - [Lesson 2.1: Introduction to S3 with awscli](#lesson-21-introduction-to-s3-with-awscli)
    - [Principle 2.1](#principle-21)
    - [Practice 2.1](#practice-21)
      - [Lab 2.1.1: Create a Bucket](#lab-211-create-a-bucket)
      - [Lab 2.1.2: Upload Objects to a Bucket](#lab-212-upload-objects-to-a-bucket)
        - [Question: Copying to Top Level](#question-copying-to-top-level)
        - [Question: Directory Copying](#question-directory-copying)
        - [Question: Object Access](#question-object-access)
        - [Question: Sync vs Copy](#question-sync-vs-copy)
      - [Lab 2.1.3: Exclude Private Objects When Uploading to a Bucket](#lab-213-exclude-private-objects-when-uploading-to-a-bucket)
      - [Lab 2.1.4: Clean Up](#lab-214-clean-up)
    - [Retrospective 2.1](#retrospective-21)
  - [Lesson 2.2: S3 Permissions and Sharing](#lesson-22-s3-permissions-and-sharing)
    - [Principle 2.2](#principle-22)
    - [Practice 2.2](#practice-22)
      - [Lab 2.2.1: Try to Publish the Bucket the Old Way](#lab-221-try-to-publish-the-bucket-the-old-way)
        - [Question: What Failed](#question-what-failed)
      - [Lab 2.2.2: Diagnose Block Public Access and Object Ownership](#lab-222-diagnose-block-public-access-and-object-ownership)
        - [Question: Four Settings](#question-four-settings)
        - [Question: Account vs Bucket](#question-account-vs-bucket)
        - [Question: Why Disable ACLs](#question-why-disable-acls)
      - [Lab 2.2.3: IAM Policy vs Bucket Policy](#lab-223-iam-policy-vs-bucket-policy)
        - [Question: Reading Policy](#question-reading-policy)
        - [Question: Public or Not](#question-public-or-not)
        - [Question: Which Policy Wins](#question-which-policy-wins)
      - [Lab 2.2.4: Share an Object with a Presigned URL](#lab-224-share-an-object-with-a-presigned-url)
        - [Question: Presigned URL Lifetime](#question-presigned-url-lifetime)
      - [Lab 2.2.5: Using CloudFormation](#lab-225-using-cloudformation)
      - [Lab 2.2.6: Optional: Controlled Public Access](#lab-226-optional-controlled-public-access)
        - [Question: Detecting Public Buckets](#question-detecting-public-buckets)
    - [Retrospective 2.2](#retrospective-22)
      - [Question: Choosing a Sharing Method](#question-choosing-a-sharing-method)
  - [Lesson 2.3: S3 Versioning and Lifecycle Policies](#lesson-23-s3-versioning-and-lifecycle-policies)
    - [Principle 2.3](#principle-23)
    - [Practice 2.3](#practice-23)
      - [Lab 2.3.1: Set up for Versioning](#lab-231-set-up-for-versioning)
      - [Lab 2.3.2: Object Versions](#lab-232-object-versions)
        - [Question: Deleted Object Versions](#question-deleted-object-versions)
        - [Question: Deleting All Versions](#question-deleting-all-versions)
      - [Lab 2.3.3: Tagging S3 Resources](#lab-233-tagging-s3-resources)
        - [Question: Deleting Tags](#question-deleting-tags)
      - [Lab 2.3.4: Object Lifecycles](#lab-234-object-lifecycles)
        - [Question: Improving Speed](#question-improving-speed)
        - [Question: Small Objects](#question-small-objects)
    - [Stretch Challenge](#stretch-challenge)
    - [Retrospective 2.3](#retrospective-23)
      - [Question: Protecting Versions](#question-protecting-versions)
  - [Lesson 2.4: S3 Object Encryption](#lesson-24-s3-object-encryption)
    - [Principle 2.4](#principle-24)
    - [Practice 2.4](#practice-24)
      - [Lab 2.4.1: Default Encryption with SSE-S3](#lab-241-default-encryption-with-sse-s3)
        - [Question: Encrypting Existing Objects](#question-encrypting-existing-objects)
      - [Lab 2.4.2: SSE-KMS with the AWS Managed Key](#lab-242-sse-kms-with-the-aws-managed-key)
        - [Question: KMS vs S3 Managed Keys](#question-kms-vs-s3-managed-keys)
        - [Question: Customer Managed Key](#question-customer-managed-key)
      - [Lab 2.4.3: Using Your Own KMS Key and S3 Bucket Keys](#lab-243-using-your-own-kms-key-and-s3-bucket-keys)
        - [Question: Key Alias](#question-key-alias)
        - [Question: Bucket Keys](#question-bucket-keys)
      - [Lab 2.4.4: Clean Up](#lab-244-clean-up)
    - [Retrospective 2.4](#retrospective-24)
      - [Question: Requiring Encryption](#question-requiring-encryption)
      - [Question: Multiple Keys](#question-multiple-keys)
      - [Question: Two Layers](#question-two-layers)
  - [Further Reading](#further-reading)

<!-- /TOC -->

## What changed in the 2026 edition

- Lesson 2.2 is rewritten. Since April 2023, new buckets have
  [Block Public Access](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html)
  turned on and
  [Object Ownership](https://docs.aws.amazon.com/AmazonS3/latest/userguide/about-object-ownership.html)
  set to *Bucket owner enforced* (ACLs disabled), so the old
  `aws s3 sync --acl public-read` labs fail. The failure is now the first lab:
  you diagnose it, then share data the current way (a bucket policy with a
  condition, presigned URLs, and a pointer to CloudFront with Origin Access
  Control in module 21). Loosening Block Public Access is optional, limited to
  one bucket, and reversed at the end.
- Object ACLs are no longer taught as an access-control tool; the lesson
  explains why AWS turned them off.
- Lesson 2.4 starts from the fact that every new object has been encrypted
  with SSE-S3 by default since January 2023. It adds S3 Bucket Keys, mentions
  DSSE-KMS, and uses current KMS terminology (the AWS managed key `aws/s3` and
  customer managed keys, not "CMKs").
- "Glacier" is now the S3 Glacier Flexible Retrieval storage class. The old
  vault-based Glacier API is no longer mentioned.
- Labs use the lab region (`us-east-2`) from your AWS profile instead of a
  hard-coded `us-west-2`.
- The dead link to the first lesson and the old `/AmazonS3/latest/dev/`
  documentation links have been replaced.
- New: cleanup steps, including the versioned-bucket cleanup gotcha, and short
  coverage of Object Lock and replication.

## Exam coverage

| Exam | Domain / task statement |
|---|---|
| CLF-C02 | Domain 2: Security and Compliance; Domain 3: Cloud Technology and Services (storage) |
| SAA-C03 | Domain 1: Design Secure Architectures (1.1 secure access, 1.3 data security controls) |
| SAA-C03 | Domain 4: Design Cost-Optimized Architectures (4.1 cost-optimized storage) |
| SOA-C03 | Domain 2: Reliability and Business Continuity (versioning, lifecycle, replication) |
| SOA-C03 | Domain 4: Security and Compliance (access policies, encryption) |
| SCS-C03 | Domain 4: Identity and Access Management (bucket and IAM policies) |
| SCS-C03 | Domain 5: Data Protection (encryption at rest, KMS keys, data access controls) |

## Cost and cleanup

- S3 storage and requests for these labs cost cents. Nothing in this module
  has an hourly charge.
- Each **customer managed KMS key** (Lab 2.4.3) costs about $1 per month,
  prorated, plus a small charge per API request. Schedule its deletion in the
  final lab. The minimum waiting period is 7 days.
- Storage classes have **minimum storage durations** (30 days for
  Standard-IA, 90 days for Glacier Flexible Retrieval). Lab objects rarely get
  that far, but anything that does transition is billed for the minimum
  even if you delete it early.
- **Versioned buckets don't empty the way you expect.** `aws s3 rm --recursive`
  and `aws s3 rb --force` only add delete markers; noncurrent versions stay
  (and are billed), and the bucket still isn't empty. CloudFormation also
  refuses to delete a stack whose bucket still holds objects or versions.
  Delete every version and delete marker first (see Lab 2.3.2 and Lab 2.4.4).
- Don't turn on Object Lock in *compliance* mode in a lab bucket. Nobody,
  including the root user, can delete locked versions until the retention
  period ends.
- Lab 2.4.4 removes everything this module creates.

## Guidance

- Use the [Amazon S3 User Guide](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)
  as much as possible. This module covers *general purpose* buckets. Directory,
  table and vector buckets are separate bucket types with their own rules.

- Avoid using other sites like stackoverflow.com for answers \-- part
  of the skill set you are building is finding answers straight from
  the source, AWS. Blog posts and tutorials written before 2023 describe
  S3 permissions and encryption defaults that no longer apply.

- Explore your curiosity. Try to understand why things work the way
  they do. Read more of the documentation than just what you need to
  find the answers.

- Your AWS profile sets the lab region (`us-east-2`). The CLI commands in this
  module don't need `--region`.

For each section, you'll want to create a branch on your GitHub repo and
push your changes to it. Consider this pattern "assumed" for
all labs going forward so we don't have to increase the length of the
document by copying / pasting "push these changes to your branch" fifty
times.

## Lesson 2.1: Introduction to S3 with awscli

### Principle 2.1

*S3 is an easy-to-use service for storing data in the cloud.*

### Practice 2.1

This section gets you familiar with the basic characteristics of S3
buckets and objects, and how you can interact with them from the command
line.

You created S3 buckets with CloudFormation in
[module 01](../01-cloudformation/README.md). In this practice session, we'll
get familiar with the
[awscli's s3 command](https://docs.aws.amazon.com/cli/latest/reference/s3/).

#### Lab 2.1.1: Create a Bucket

S3 buckets are located in regions, but their names are globally unique.
Using "aws s3", create a bucket:

- Create it in the lab region set in your profile. Check which region the
  bucket ended up in with `aws s3api get-bucket-location`.

- Call the bucket "stelligent-u-_your-identifier_".

- List the contents of the bucket.

#### Lab 2.1.2: Upload Objects to a Bucket

Add an object to your bucket:

- Create a local subdirectory, "data", for s3 files and put a few
  files in it.

- Copy the file to your bucket using the "aws s3" command. Find more
  than one way to upload it.

- List the contents of the bucket after each upload.

##### Question: Copying to Top Level

_How would you copy the contents of the directory to the top level of your bucket?_

##### Question: Directory Copying

_How would you copy the contents and include the directory name in the s3 object
paths?_

##### Question: Object Access

_[Can anyone else see your file yet](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-management.html)?_

For further reading, see the S3
[Policies and permissions](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-policy-language-overview.html)
page.

##### Question: Sync vs Copy

_What makes "sync" a better choice than "cp" for some S3 uploads?_

#### Lab 2.1.3: Exclude Private Objects When Uploading to a Bucket

Add a private file, "private.txt", to your data directory. Then, upload the
directory to your bucket again **without including the private file**.

- Verify after uploading that the file doesn't exist in the bucket.

- Did you find two different ways to accomplish this task? If not, make sure to
  read the [documentation on sync flags](https://docs.aws.amazon.com/cli/latest/reference/s3/sync.html).

#### Lab 2.1.4: Clean Up

Clean up: remove your bucket. What do you have to do before you can
remove it?

### Retrospective 2.1

For additional s3 commands and reference see the
[AWS CLI Command Reference](https://docs.aws.amazon.com/cli/latest/reference/s3/)

## Lesson 2.2: S3 Permissions and Sharing

### Principle 2.2

*S3 is private by default and guarded twice: by the policies you write, and
by Block Public Access, which overrides them. Share data by granting exactly
the access you mean, not by making things public.*

### Practice 2.2

Tutorials written before 2023 made a bucket public with one flag. That no
longer works, and the reason is the first thing this lesson teaches. Since
April 2023 every new bucket starts with all four
[Block Public Access](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html)
settings on and with
[Object Ownership](https://docs.aws.amazon.com/AmazonS3/latest/userguide/about-object-ownership.html)
set to *Bucket owner enforced*, which disables ACLs. See the
[general purpose bucket overview](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html)
for the defaults.

You'll try the old approach and watch it fail, work out which settings
stopped it, and then use the tools that replaced ACLs: identity-based (IAM)
policies, bucket policies with conditions, and presigned URLs. For serving a
website or public downloads, the current answer is CloudFront in front of a
private bucket with
[Origin Access Control](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html)
(OAC). You'll build that in module 21; this lesson explains why you want it.

#### Lab 2.2.1: Try to Publish the Bucket the Old Way

Create your bucket again and upload the contents of your "data" directory with
"aws s3 sync":

- Include the "private.txt" file this time.

- Use the sync parameter that older tutorials use to make every file publicly
  readable (a canned ACL). Find it in the
  [sync reference](https://docs.aws.amazon.com/cli/latest/reference/s3/sync.html).

- It should fail. Save the exact error message in your answer below.

- Upload the files again without that parameter so the rest of the lesson
  has something to work with.

##### Question: What Failed

_What error did you get, and what does it say about the bucket? Did any file
upload?_

#### Lab 2.2.2: Diagnose Block Public Access and Object Ownership

Block Public Access can be set on a bucket, on an account, and (through an
AWS Organizations policy) on every account in an organization. S3 enforces the
most restrictive combination. Use the CLI to inspect the bucket and account
levels, plus the bucket's Object Ownership setting:

- The bucket's Block Public Access configuration
  ([s3api get-public-access-block](https://docs.aws.amazon.com/cli/latest/reference/s3api/get-public-access-block.html)).

- The account's Block Public Access configuration
  ([s3control get-public-access-block](https://docs.aws.amazon.com/cli/latest/reference/s3control/get-public-access-block.html)).
  This command needs your account ID; get it with `aws sts get-caller-identity`
  rather than typing it into your code. An error that says no configuration
  exists is itself an answer.

- The bucket's Object Ownership setting
  ([s3api get-bucket-ownership-controls](https://docs.aws.amazon.com/cli/latest/reference/s3api/get-bucket-ownership-controls.html)).

Write down what you found. You'll restore exactly these values at the end of
the lesson. If your lab account belongs to an organization (module 19), the
account-level values may be inherited from an organization policy that you
can't change from inside the account.

<!-- VERIFY: whether new accounts (standalone or created via Organizations) get account-level Block Public Access on by default; the docs only state the bucket-level default. -->

##### Question: Four Settings

_What does each of the four Block Public Access settings block? Which of them
stopped your upload in Lab 2.2.1, or was it something else?_

##### Question: Account vs Bucket

_If the account-level setting is on and the bucket-level setting is off, can
the bucket be made public? Who should own the account-level setting in an
organization with many accounts?_

##### Question: Why Disable ACLs

_Read [Controlling ownership of objects and disabling ACLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/about-object-ownership.html).
Why did AWS turn ACLs off by default? Name one situation where you might
still need them._

#### Lab 2.2.3: IAM Policy vs Bucket Policy

The [aws s3api command](https://docs.aws.amazon.com/cli/latest/reference/s3api/index.html)
gives you a lot more options than "aws s3". Remove the bucket again, then
recreate it to start fresh, and upload your data directory including
"private.txt".

Build this access model with policies only (no ACLs):

- Anyone making a request **from your current public IP address** can read
  every object, without AWS credentials. Grant this in a bucket policy that
  uses the `aws:SourceIp`
  [condition key](https://docs.aws.amazon.com/AmazonS3/latest/userguide/amazon-s3-policy-keys.html).
  (If you work from CloudShell, its public IP is not your laptop's.)

- Nobody except you can read "private.txt". Add a `Deny` statement for that
  object with a condition on the caller's principal ARN.

- Create a customer managed IAM policy that grants maintenance access to your
  bucket (list the bucket; get, put and delete objects) and nothing else.
  Attach it to an IAM role you can assume, and use that role for the rest of
  this lab. Your Identity Center session from module 00 probably has broad
  permissions already; the point here is to see an identity-based policy and
  a resource-based policy work together.

- Use `aws s3api get-bucket-policy-status` to check whether S3 considers your
  bucket public.

When you're done, verify with `curl` (no credentials) that you can read most
files but not "private.txt", and with the CLI (as your role) that you can
modify files and read "private.txt".

Be careful with `Deny` statements in a bucket policy: a wrong condition can
lock out every principal in the account, including administrators. If that
happens, only the account's root user can delete the bucket policy; in an
organization with centralized root access, the management account does it as a
[privileged root task](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-user-privileged-task.html).
Know which applies to your lab account before you write a `Deny`.

##### Question: Reading Policy

_What do you see when you try to read the bucket policy before you've set
one?_

##### Question: Public or Not

_Your policy grants `s3:GetObject` to `"Principal": "*"`, yet Block Public
Access let you save it and the policy status says it isn't public. Why? Read
[The meaning of "public"](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html#access-control-block-public-access-policy-status)
and name two other condition keys that keep a policy non-public._

##### Question: Which Policy Wins

_Your IAM policy allows you to read "private.txt" and the bucket policy
denies everyone but you. What would happen if the bucket policy denied you
too? How does S3 combine an identity-based policy and a bucket policy for
principals in the same account?_

#### Lab 2.2.4: Share an Object with a Presigned URL

A bucket policy with an IP condition doesn't help if you need to hand one file
to someone outside your network for a short time.
[Presigned URLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ShareObjectPreSignedURL.html)
do that without changing any policy:

- Generate a presigned URL for "private.txt" with
  [aws s3 presign](https://docs.aws.amazon.com/cli/latest/reference/s3/presign.html),
  valid for a few minutes.

- Download it with `curl` from outside your IP allowance (for example, from
  CloudShell or your phone), then again after it has expired.

##### Question: Presigned URL Lifetime

_The URL is signed with your credentials. What happens to it when your
Identity Center session expires before the URL does? What is the longest a
presigned URL can be valid, and how does the kind of credential you sign with
change that?_

#### Lab 2.2.5: Using CloudFormation

It's valuable to know about the s3api command, but you're much more
likely to be managing S3 resources with CloudFormation. Repeat Lab 2.2.3,
but this time do it all with CloudFormation instead of the awscli.

- In the `AWS::S3::Bucket`, set `PublicAccessBlockConfiguration` and
  `OwnershipControls` explicitly to the secure defaults you recorded in Lab
  2.2.2. Declaring them documents your intent and protects you from someone
  changing them in the console.

- Pass your IP address and role ARN in as parameters. Don't hard-code them.

- To keep things simple, implement all of the permissions using a single
  `AWS::S3::BucketPolicy`. The bucket's `AccessControl` property sets a
  canned ACL; leave it out.

When you're done, verify your access again.

#### Lab 2.2.6: Optional: Controlled Public Access

Sometimes content really must be public, and a mentor may ask you to see what
that looks like. Do this only in your lab account, only on this one bucket,
and put everything back when you're done:

- If Lab 2.2.2 showed Block Public Access on at the account level, stop here
  and answer the question below instead. Don't change account-level settings.

- Update your stack so that only `BlockPublicPolicy` and
  `RestrictPublicBuckets` are off for this bucket. Leave the two ACL settings
  on and ACLs disabled.

- Add a policy statement that grants anonymous read to objects under a
  `public/` prefix only, with no IP condition. Confirm the policy status now
  says public, and fetch an object from outside your network.

- Look at the bucket in the S3 console and in
  [IAM Access Analyzer](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-analyzer.html).
  Note how it is flagged.

- Restore all four settings to on and remove the public statement. Confirm the
  policy status is back to not public.

##### Question: Detecting Public Buckets

_If someone in your organization makes a bucket public, how would you find
out? Which tools would tell you, and which setting would have prevented it?_

### Retrospective 2.2

See [this AWS security blog post](https://aws.amazon.com/blogs/security/iam-policies-and-bucket-policies-and-acls-oh-my-controlling-access-to-s3-resources/)
for how IAM policies, bucket policies and ACLs work together. It predates
disabled-by-default ACLs; read it for the evaluation logic. The
[S3 security best practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html)
and the
[bucket policy examples](https://docs.aws.amazon.com/AmazonS3/latest/userguide/example-bucket-policies.html)
are current.

#### Question: Choosing a Sharing Method

_For each case, which would you use: an IAM policy, a bucket policy with a
condition, a presigned URL, or CloudFront with OAC? (a) An application in
your account needs to read and write objects. (b) A partner's AWS account
needs read access to one prefix. (c) A customer needs to download one report
today. (d) A public marketing website._

## Lesson 2.3: S3 Versioning and Lifecycle Policies

### Principle 2.3

*S3 is the go-to solution when working with data that should be
versioned or have a lifecycle.*

### Practice 2.3

See [Versioning](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html),
[Lifecycle management](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html),
[Storage classes](https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html)
and [Storage Class Analysis](https://docs.aws.amazon.com/AmazonS3/latest/userguide/analytics-storage-class.html)
in the S3 docs for information on the labs below. You'll use both the
CLI & CloudFormation. In a professional capacity, you're much more likely to
write policies and bucket options with CloudFormation, and they're
easier to write in its templating language, but some of these tasks \--
like those managing data \-- require the CLI.

#### Lab 2.3.1: Set up for Versioning

Experiment with bucket versioning. Using the CLI, delete the bucket
stack you created for Lesson 2.2, so that we can start out fresh. Make
a copy of the stack template you just wrote above, and modify it for
this lab:

- Create the stack with versioning enabled on the bucket

- Upload your local data files to the bucket with the CLI.

- Modify your local data files, and sync those files to the bucket
  again.

- Inspect your bucket's objects after syncing and see how many
  versions there are.

- Fetch the original version of an object.

#### Lab 2.3.2: Object Versions

Delete one of the objects that you changed.

##### Question: Deleted Object Versions

_Can you still retrieve old versions of the object you removed? What did the
delete actually create?_

##### Question: Deleting All Versions

_How would you delete all versions? Why doesn't `aws s3 rb --force` empty a
versioned bucket, and what are two ways to empty one?_

(See [Deleting object versions](https://docs.aws.amazon.com/AmazonS3/latest/userguide/DeletingObjectVersions.html)
and [Emptying a bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/empty-bucket.html).)

#### Lab 2.3.3: Tagging S3 Resources

Tag one or more of your objects or buckets using "aws s3api", or add
tags to your bucket through CloudFormation. View the tags on them
through the CLI or the console.

##### Question: Deleting Tags

_Can you change a single tag on a bucket or object, or do you have to change
all its tags at once?_

(See `aws:cloudformation:stack-id` and other AWS-managed tags.)

#### Lab 2.3.4: Object Lifecycles

Create a lifecycle policy for the bucket:

- Move objects to the Standard-IA storage class after 30 days.

- Move them to Glacier Flexible Retrieval after 90 days.

- Expire all noncurrent object versions after 7 days.

- Remove all incomplete multipart uploads after 1 day.

After updating your stack, use the [S3 console's](https://console.aws.amazon.com/s3/)
_Management_ tab to double-check your lifecycle settings.

##### Question: Improving Speed

_Can you make any of these transitions more quickly? What stops you, and what
does it cost to move an object out of a class early?_

*See [Transitioning objects](https://docs.aws.amazon.com/AmazonS3/latest/userguide/lifecycle-transition-general-considerations.html).*

##### Question: Small Objects

_Your lab files are only a few bytes. Will your lifecycle rule transition
them at all? Why might that be a sensible default?_

### Stretch Challenge

For objects with the tag you assigned earlier and under the `trash/` prefix,
expire them after 1 day.

### Retrospective 2.3

*How could the lifecycle and versioning features of S3 be used to manage
the lifecycle of a web application? Would you use those features to manage
the webapp code itself, or just the app's data?*

#### Question: Protecting Versions

_Versioning keeps old copies, but anyone with the right permissions can still
delete a version. Read about
[S3 Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html)
and [replication](https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication.html).
What is the difference between governance and compliance mode? Which feature
protects you against accidental deletion, which against a region outage, and
what does replication need you to turn on first?_

## Lesson 2.4: S3 Object Encryption

### Principle 2.4

*S3 encrypts everything at rest by default. Your job is to choose who holds
the key and who can use it.*

### Practice 2.4

See [Protecting data with encryption](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingEncryption.html)
for information on the labs below.

Since January 2023, S3 encrypts every new object with S3-managed keys
(SSE-S3) whether you ask for it or not. See the
[default encryption FAQ](https://docs.aws.amazon.com/AmazonS3/latest/userguide/default-encryption-faq.html).
The old question "is my data encrypted?" is now "whose key, and who is
allowed to use it?". The choices for server-side encryption are:

- **SSE-S3**: S3 owns and manages the keys. No extra cost, no key policy to
  control.
- **SSE-KMS**: keys in AWS KMS, either the AWS managed key `aws/s3` or a
  customer managed key you create. Every use of the key is logged in
  CloudTrail and governed by a key policy. S3 Bucket Keys cut the number of
  KMS requests.
- **DSSE-KMS**: two independent layers of encryption with KMS keys, for
  workloads whose compliance rules require it. It costs more and doesn't use
  Bucket Keys.
- **SSE-C**: you supply the key with every request. Since April 2026 it is
  blocked by default on new general purpose buckets (the
  `BlockedEncryptionTypes` setting in the bucket's default encryption); see
  [SSE-C](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ServerSideEncryptionCustomerKeys.html).
  You won't use it in these labs.

Module 10 covers KMS in depth. Here you only need enough KMS to see how S3
uses it.

#### Lab 2.4.1: Default Encryption with SSE-S3

Look at what S3 did without being asked:

- Use `aws s3api head-object` on one of the objects you uploaded in Lesson
  2.3. Which encryption header is set?

- Read the bucket's default encryption configuration with
  `aws s3api get-bucket-encryption`. You never configured it; where did it
  come from?

- In your stack, set the bucket's default encryption to SSE-S3 explicitly
  with `BucketEncryption`, so the template states what the bucket does.

##### Question: Encrypting Existing Objects

_If you change a bucket's default encryption, are the objects already in it
re-encrypted? How would you change the encryption of existing objects without
downloading and re-uploading them yourself?_

#### Lab 2.4.2: SSE-KMS with the AWS Managed Key

Change the bucket's default encryption to SSE-KMS without naming a key.

- Update your stack.

- Use the S3 API to identify the encryption, and the key if there is one, of
  one of the files in your bucket.

- Modify the local copy of that file and re-sync your bucket.

- Use the S3 API again to check the encryption and key ID.

The first object should show SSE-S3 (`AES256`). The second should show
`aws:kms` and the ARN of a key. Look that key up with `aws kms describe-key`
and `aws kms list-aliases`: S3 used the AWS managed key `aws/s3`, which KMS
created in your account the first time a service asked for it.

##### Question: KMS vs S3 Managed Keys

_Look through the
[SSE-KMS docs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html).
What benefits might you gain by using a KMS key instead of an S3-managed key?
What does it cost you?_

##### Question: Customer Managed Key

_Going further, what can you do with a customer managed key that you can't do
with `aws/s3`? Think about the key policy, cross-account access, rotation and
disabling the key.
(See [AWS KMS keys](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#key-mgmt).)_

#### Lab 2.4.3: Using Your Own KMS Key and S3 Bucket Keys

Use your own KMS key to encrypt files in S3.

- Create a customer managed key by adding an
  [AWS::KMS::Key](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-kms-key.html)
  to your stack or with
  "[aws kms create-key](https://docs.aws.amazon.com/cli/latest/reference/kms/create-key.html)".

- Assign an alias to the key as well.

- Make it the bucket's default encryption key and enable
  [S3 Bucket Keys](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-key.html)
  in the same encryption rule.

- Re-upload some of your test files. Upload one more with the CLI, naming the
  key explicitly.

- Again use the S3 API to verify the key ID used on objects before and after
  the change, and check whether each object reports a Bucket Key.

##### Question: Key Alias

_Can you use the alias when uploading files? Can you use it in a bucket policy
condition that requires a particular key?_

##### Question: Bucket Keys

_What problem do S3 Bucket Keys solve, and what changes in your CloudTrail
logs when they're on?_

#### Lab 2.4.4: Clean Up

Remove everything this module created:

- Empty the versioned bucket completely: every object version and every
  delete marker. Then delete the stack. If the stack deletion fails, find out
  why in the stack events before retrying.

- Schedule deletion of your customer managed key with the shortest waiting
  period and delete its alias. The `aws/s3` key is AWS managed; you can't and
  needn't delete it.

- Delete any IAM role and policy you created in Lab 2.2.3.

- Confirm with `aws s3 ls` that no module buckets remain.

### Retrospective 2.4

#### Question: Requiring Encryption

_Every object is encrypted anyway. What does a bucket policy that requires
encryption still add? Write the condition that rejects uploads using any key
other than your customer managed key._

(See the
[bucket policy examples](https://docs.aws.amazon.com/AmazonS3/latest/userguide/example-bucket-policies.html)
and
[Specifying server-side encryption with AWS KMS](https://docs.aws.amazon.com/AmazonS3/latest/userguide/specifying-kms-encryption.html).)

#### Question: Multiple Keys

_Can you use different keys for different objects? Why might you want to?_

#### Question: Two Layers

_When would you choose
[DSSE-KMS](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingDSSEncryption.html)
over SSE-KMS? What does it cost you?_

## Further Reading

- S3 [objects](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingObjects.html)
  are not files. The
  [index document support](https://docs.aws.amazon.com/AmazonS3/latest/userguide/IndexDocumentSupport.html)
  for web hosting is one use case that makes the difference clear.

- S3 can do
  [static website hosting](https://docs.aws.amazon.com/AmazonS3/latest/userguide/WebsiteHosting.html),
  but website endpoints are HTTP only and need the bucket to be public. In
  practice, put CloudFront with OAC in front of a private bucket (module 21).
  [Redirection rules](https://docs.aws.amazon.com/AmazonS3/latest/userguide/how-to-page-redirect.html)
  are still worth knowing.

- [Event notifications](https://docs.aws.amazon.com/AmazonS3/latest/userguide/EventNotifications.html)
  open up a wide range of other use cases for S3. S3 can
  [send events to EventBridge](https://docs.aws.amazon.com/AmazonS3/latest/userguide/EventBridge.html)
  directly; you don't need a CloudTrail trail to react to uploads.

- The S3 API (and CLI) and CloudFormation sometimes offer very different
  interfaces to the service. Compare the way bucket lifecycle rules are
  managed through
  [put-bucket-lifecycle-configuration](https://docs.aws.amazon.com/cli/latest/reference/s3api/put-bucket-lifecycle-configuration.html)
  with the `LifecycleConfiguration` property of
  [AWS::S3::Bucket](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-s3-bucket.html),
  and bucket policies through
  [put-bucket-policy](https://docs.aws.amazon.com/cli/latest/reference/s3api/put-bucket-policy.html)
  with
  [AWS::S3::BucketPolicy](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-s3-bucketpolicy.html).

- [CloudFront](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Introduction.html)
  lets you serve S3 objects to the public while the bucket stays private, and
  makes access faster and often cheaper.

- [Replication](https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication.html)
  (same-region or cross-region) copies objects to another bucket for lower
  latency, separate ownership across accounts, compliance, or disaster
  recovery. Module 23 covers backup and DR.

- [Amazon S3 Security changes are coming in April of 2023](https://aws.amazon.com/blogs/aws/heads-up-amazon-s3-security-changes-are-coming-in-april-of-2023/)
  and
  [Amazon S3 encrypts new objects by default](https://aws.amazon.com/blogs/aws/amazon-s3-encrypts-new-objects-by-default/)
  are the announcements behind this edition's changes.
