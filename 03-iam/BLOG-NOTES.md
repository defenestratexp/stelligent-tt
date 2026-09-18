# Blog notes: Module 03 (IAM)

## Working title

Testing least privilege: positive and negative tests with the IAM policy
simulator and Access Analyzer

## Hook

The 2022 version of this module had you assume roles as an IAM user and
check permissions by hand: run a command, see whether it fails. In 2026
nobody should have an IAM user to start from. You sign in through IAM
Identity Center, which makes your "who am I" an `AWSReservedSSO_` role
with a random suffix, and that single fact breaks the naive trust
policy. Meanwhile AWS has shipped tools that make permission testing
something you can automate: the policy simulator, Access Analyzer policy
validation, and custom policy checks that prove a policy does *not*
grant something.

## Key points

1. **Know who you are.** `aws sts get-caller-identity` returns an STS
   session ARN; the trust policy needs the IAM role ARN, path and all
   (`role/aws-reserved/sso.amazonaws.com/<region>/AWSReservedSSO_...`).
2. **Don't trust a suffix.** Remove every assignment of a permission set
   and Identity Center recreates the role with a new suffix. Trust the
   account and narrow it with `ArnLike` on `aws:PrincipalArn` instead.
3. **Positive and negative tests.** For every permission you grant, test
   one thing that should work and one adjacent thing that shouldn't.
   The simulator answers both without touching real resources.
4. **Validate before you deploy.** `aws accessanalyzer validate-policy`
   catches grammar errors, unsupported condition keys and
   `iam:PassRole` on `*` before CloudFormation ever sees the template;
   `check-access-not-granted` turns a negative test into a check that
   fails a pipeline.
5. **Boundaries cap, they don't grant.** A permissions boundary on a
   role with `AmazonS3FullAccess` still blocks writes; the delegated-
   admin pattern uses `iam:PermissionsBoundary` to stop privilege
   escalation. SCPs and RCPs do the same job at the organization level.
6. **Shrink afterwards.** Unused-access findings and CloudTrail-based
   policy generation show what a role actually used.

## Gotchas readers will hit

- Pasting the `arn:aws:sts::...:assumed-role/...` session ARN into the
  trust policy instead of the IAM role ARN.
- Identity Center in `us-east-1` puts no region in the role path; every
  other home region does.
- Trusting the account root means the caller also needs `sts:AssumeRole`
  in its own identity policy; naming the role directly doesn't.
- Assuming a role from an SSO session is role chaining: one hour
  maximum, whatever `MaxSessionDuration` says.
- Changing a customer managed policy's `Description` forces replacement,
  which fails if you gave the policy a fixed name.
- The simulator evaluates identity policies and SCPs, but can't simulate
  resource-based policies for roles; confirm against the live API.
- An unused-access analyzer is billed per role per month, including the
  SSO roles. Delete it after the demo.

## Exam objectives supported

- SAA-C03 Domain 1: Design Secure Architectures (1.1)
- SCS-C03 Domain 4: Identity and Access Management
- DOP-C02 Domain 6: Security and Compliance (6.1)
- SOA-C03 Security and Compliance; CLF-C02 Domain 2 (2.3)
