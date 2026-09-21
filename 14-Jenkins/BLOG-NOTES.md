# Blog notes: Topic 14, Jenkins

## Working title

Jenkins on AWS in 2026: no open ports, no stored keys, no pets

## Hook

Search for "Jenkins on EC2" and most results still open port 8080 and SSH
to the world, install Java 11 or 17, click through the setup wizard, and
paste an IAM user's access keys into the credentials store. None of that
holds up in 2026. Jenkins LTS has required Java 21 (or 25) on the
controller and on every agent since 2.555.1 in April 2026, Configuration
as Code is the normal way to run it, and on AWS the controller never needs
a public port or a long-lived AWS key. This post rebuilds the 2022
Stelligent-U Jenkins module that way: an Amazon Linux 2023 controller
reached only through Session Manager, plugins pinned in `plugins.txt`,
the whole system described in JCasC, and one short-lived EC2 agent per
build, launched with the controller's instance role.

## Key points

1. **Nothing inbound.** The controller's security group has no inbound
   rules, Jenkins binds to `127.0.0.1`, and you reach it with Session
   Manager port forwarding. The only other allowed path is SSH from the
   controller's security group to the agents' security group.
2. **Java 21 everywhere.** 2.555.1 dropped Java 17 for controllers and
   agents. On AL2023 that is `java-21-amazon-corretto-headless`, and the
   agent's init script has to install it too, or agents fail to connect.
3. **Rebuildable from Git.** `plugins.txt` (installed by the plugin
   installation manager tool), JCasC YAML, and a boot script that pulls
   both from S3. Stack facts reach JCasC as environment variables from a
   systemd drop-in. Secrets reach it as files fetched at boot from Parameter
   Store (the key pair CloudFormation created) and Secrets Manager (the
   admin password). A second stack from the same files proves it.
4. **Ephemeral agents, instance roles only.** The EC2 plugin launches an
   agent per build (`maxTotalUses: 1`) with the controller's role. Its IAM
   policy is scoped with the `jenkins_cloud_name` tag the plugin applies at
   launch, so the controller can terminate only its own agents, and
   `iam:PassRole` names the agent role only. Builds get AWS permissions from
   the agent role, not from Jenkins credentials.
5. **Artifacts in S3 without agent permissions.** Artifact Manager on S3
   has the controller presign URLs; agents upload with plain HTTPS.
6. **Back up data, rebuild configuration.** Scheduled EBS snapshots of
   `JENKINS_HOME` plus a root-volume replacement give a measurable RTO/RPO;
   everything else comes back from Git.

## Gotchas readers will hit

- The Jenkins RPM repository is now `https://pkg.jenkins.io/rpm-stable/`
  and verifies repository metadata (`repo_gpgcheck=1`); old posts import
  `jenkins.io-2023.key` from `redhat-stable`.
- The package logs to the journal, not `/var/log/jenkins/jenkins.log`,
  unless you set `JENKINS_LOG` in a systemd drop-in.
- The plugin installation manager tool **deletes** its download directory
  before installing. Stop Jenkins first, and don't point it at a directory
  holding anything else.
- `--latest` defaults to true: pinned top-level plugins can still pull the
  newest dependencies. Pinning everything means generating the full list.
- The EC2 plugin connects to Linux agents over SSH; with no NAT gateway the
  agents need public IPs for outbound traffic, while the controller must
  connect by private IP.
- The policy on the EC2 plugin's page allows `iam:PassRole` on `*` and
  actions this setup never calls (`iam:ListInstanceProfilesForRole`,
  `ec2:GetPasswordData`, and the spot request calls when agents are
  on-demand).
- Deleting the controller while an agent runs leaves an orphaned,
  billed instance, and the stack deletion fails because the agent still
  uses the security group and instance profile.
- A controller with no inbound path can't receive GitHub webhooks; use
  periodic branch scanning or a relay.
- Job definitions aren't covered by JCasC itself, and the Job DSL plugin
  is marked "up for adoption" on the plugin index.

## Exam objectives supported

- DOP-C02 Domain 1: Tasks 1.1–1.3 (CI/CD pipelines, automated testing,
  artifacts)
- DOP-C02 Domain 2: Task 2.1 (infrastructure and reusable components as
  code)
- DOP-C02 Domain 3: Task 3.3 (automated recovery for RTO and RPO)
- DOP-C02 Domain 4: Task 4.1 (log collection with the CloudWatch agent)
- DOP-C02 Domain 6: Tasks 6.1 and 6.2 (least-privilege instance roles,
  no long-lived credentials)

## Material to capture while doing the labs

- The `ec2-plugin-agents` policy next to the plugin's documented policy,
  with the differences annotated.
- A timeline of one build: queue, `RunInstances`, SSH connect, build,
  terminate, with the wait time.
- The decoded `UnauthorizedOperation` message from Lab 14.3.2 (account ID
  redacted).
- A diagram: laptop → Session Manager → controller (127.0.0.1:8080) → SSH
  → agent; S3 for config and artifacts; Parameter Store and Secrets
  Manager for secrets.
- The measured restore time from Lab 14.5.2 and the cost of a day of
  running the stack.
