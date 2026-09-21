# Blog Notes: Module 11, Parameter Store, Secrets Manager and AppConfig

## Working title

Three places to keep configuration on AWS, and the one that's really a
deployment tool

## Hook

The 2022 version of this lesson was Parameter Store only, with Secrets
Manager in a "recently introduced" footnote. In 2026 the question isn't
whether to get configuration out of your code but which of three services
it belongs in. Parameter Store is a free, versioned key-value store.
Secrets Manager costs $0.40 a secret because it manages a credential's
whole life: generation, rotation, cross-account sharing. AppConfig treats a
flag flip as a deployment, with gradual rollout, validators and automatic
rollback on a CloudWatch alarm, and it has quietly taken over from
CloudWatch Evidently. This post works through one small app that uses all
three and shows where each one earns its place.

## Key points

1. **Parameter Store is free until you need more.** Standard parameters
   cost nothing at the default 40 TPS; advanced parameters ($0.05 a month)
   buy 8 KB values, expiry policies and cross-account sharing, and can
   never be downgraded. Public parameters (AMI IDs, AppConfig layer ARNs)
   are the part everyone already uses.
1. **CloudFormation reads parameters two ways.** SSM parameter types are
   resolved at create/update time and shown on the stack; dynamic
   references resolve in properties. Neither can read a SecureString into
   UserData: `ssm-secure` works only in a short list of password
   properties, so instances read secrets at boot with their instance role.
1. **Dynamic references don't make a secret secret.**
   `{{resolve:secretsmanager:...}}` works in every property, and the
   receiving service may store the value in plaintext (a String parameter,
   user data, Lambda environment variables). Pass ARNs, not values, or let
   the service own the secret (RDS `ManageMasterUserPassword`).
1. **Rotation is four Lambda steps and three staging labels.**
   createSecret, setSecret, testSecret, finishSecret; `AWSPENDING`,
   `AWSCURRENT`, `AWSPREVIOUS`. Managed rotation (RDS, Aurora, Redshift,
   DocumentDB) and managed external secrets (SaaS partners) remove the
   function altogether.
1. **Cross-account secrets need three yeses:** resource policy, KMS key
   policy (customer managed key only, since `aws/secretsmanager` can't be
   shared) and an identity policy in the other account, plus the full ARN.
1. **AppConfig is a deployment service.** Deployment strategies, bake time
   and alarm-based rollback; validators (JSON Schema for free-form data, a
   built-in schema for flags, Lambda for anything else); the agent caches
   locally and cuts the per-request bill.

## Gotchas readers will hit

- CloudFormation can't create a SecureString parameter; `AWS::SSM::Parameter`
  accepts only `String` and `StringList`.
- Stacks don't notice parameter changes. The value is fixed at the last
  create or update, and drift detection ignores dynamic references.
- `put-resource-policy` on the CLI allows public policies unless you pass
  `--block-public-policy`, while the CloudFormation resource blocks them by
  default.
- A `RotationSchedule` rotates immediately on creation by default, so a
  broken rotation function fails the first time you deploy it.
- `get-latest-configuration` returns an empty body when nothing changed,
  and you must use the new token each time; the old `GetConfiguration` API
  can't read feature flags.
- AppConfig deletion protection can block deleting an environment or
  profile read in the last hour.
- Deleted secrets linger for a recovery window (unless forced) and names
  can't be reused until they're gone.

<!-- VERIFY: while doing Lab 11.3.4, record whether an invalid hosted
version fails at creation or only at start-deployment, for the gotchas. -->

## Exam objectives

- DVA-C02 (→ C03) Domain 2: Security, Task 2.3 (Skill 2.3.3, secret
  management services); Domain 3: Deployment, Skill 3.1.5 (AppConfig) and
  Skill 3.4.11 (deployment strategies)
- SOA-C03 Domain 4: Security and Compliance, Skill 4.2.4 (securely store
  secrets); Domain 3: Deployment, Provisioning, and Automation
- SCS-C03 Domain 5: Data Protection, Skill 5.3.1 (management and rotation of
  credentials and secrets); Domain 4, Skill 4.2.1 (resource policies for
  cross-account access)
