# Blog notes: Module 00, Development Environment

## Working title

From MFA session scripts to IAM Identity Center

Alternatives: "Your first day on AWS in 2026: no Cloud9, no access keys, one
budget alert"; "The four bugs in my MFA login script (and why I don't need it
any more)".

## Hook

The 2022 onboarding module told you to put an IAM user's access key on your
laptop, enable MFA, and then write a script to trade an MFA code for STS
session credentials every morning. Then it sent you to Cloud9. In 2026, Cloud9
is closed to new customers, `aws configure sso` does the token exchange for
you, and the script I wrote back then turned out to delete other profiles and
wipe working credentials whenever I mistyped a code. This post covers what day
one on AWS looks like now, and why doing the old way by hand once is still
worth it.

## Key points

- **IAM Identity Center + `aws configure sso` replaces long-lived keys.**
  Nothing goes into `~/.aws/credentials`. The CLI caches an SSO token and gets
  role credentials when it needs them. Permission sets become
  `AWSReservedSSO_*` roles in each account.
- **Organization instance, not account instance.** An account instance of
  Identity Center can't give you access to AWS accounts. On day one you enable
  the organization instance, which turns your account into an Organizations
  management account. Move lab work to a member account as soon as you can.
- **Why MFA + STS is still worth doing by hand once:** `GetSessionToken`, the
  `aws:MultiFactorAuthPresent` condition, `ASIA` vs `AKIA` key prefixes,
  session credentials that can't call IAM/STS. These show up on CLF, SOA and
  SCS questions.
- **The script's bugs are the lesson.** `sed -i '1,/temp/!d'` deleted every
  profile after the first line that matched "temp". A failed `get-session-token`
  still wiped the old creds. Secrets went to a fixed `/tmp` file with the
  default umask. Region/output were written to the credentials file. The fix:
  `aws configure set ... --profile temp`, check the exit status, `mktemp` +
  `chmod 600` + `trap`.
- **Cost safety on day one:** a budget with actual and forecast alerts (global
  service, `us-east-1` endpoint), tag everything, Resource Explorer or Tag
  Editor to find it, and `ekristen/aws-nuke` (dry run, alias check, blocklist)
  only in a dedicated lab account.
- **Cloud9 replacements:** local CLI v2, a dev container with the AWS CLI
  feature, and CloudShell (already signed in as your console identity, about
  1 GB of persistent home per region).

## Gotchas readers will hit

- `aws configure sso` asks for the **SSO region**, meaning Identity Center's
  home region, and separately for the **default client region**. They're not
  the same setting.
- Since CLI 2.22 the default sign-in is PKCE. It expects a browser on the same
  machine, so in a dev container or over SSH use `--use-device-code`, or
  bind-mount `~/.aws` from the host.
- `aws configure set` can't delete a profile; removing old sections is an
  editor job.
- Budgets are refreshed a few times a day, not in real time. An overnight NAT
  gateway shows up the next day.
- `rebuy-de/aws-nuke` was archived in October 2024; v3 of the `ekristen` fork
  needs `aws-nuke run`, and the config key is `blocklist`.
- The upstream `99designs/aws-vault` was abandoned; ByteNess maintains the
  fork.
- Free-plan accounts (Free Tier since July 2025) may need upgrading before
  Organizations, and therefore an Identity Center organization instance, is
  available. Check this before publishing.

## Exam objectives supported

- CLF-C02 Domain 2 (Task 2.3, access management), Domain 3 (Task 3.1, ways to
  operate in AWS), Domain 4 (Task 4.2, billing and budget resources)
- SOA-C03 Domain 4, Task 4.1 (MFA, federated identity, policy conditions,
  multi-account)
- SCS-C03 Domain 4, Task 4.1 (Identity Center, MFA, STS temporary credentials)
