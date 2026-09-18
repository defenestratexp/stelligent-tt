# Topic 14: Jenkins

<!-- TOC -->

- [Topic 14: Jenkins](#topic-14-jenkins)
  - [What changed in the 2026 edition](#what-changed-in-the-2026-edition)
  - [Exam coverage](#exam-coverage)
  - [Cost and cleanup](#cost-and-cleanup)
  - [Guidance](#guidance)
  - [Conventions](#conventions)
  - [Lesson 14.1: A controller nobody can reach](#lesson-141-a-controller-nobody-can-reach)
    - [Principle 14.1](#principle-141)
    - [Practice 14.1](#practice-141)
      - [Lab 14.1.1: Deploy the controller](#lab-1411-deploy-the-controller)
      - [Lab 14.1.2: Reach Jenkins through Session Manager](#lab-1412-reach-jenkins-through-session-manager)
      - [Lab 14.1.3: Ship the Jenkins log to CloudWatch](#lab-1413-ship-the-jenkins-log-to-cloudwatch)
    - [Retrospective 14.1](#retrospective-141)
  - [Lesson 14.2: Configuration as code](#lesson-142-configuration-as-code)
    - [Principle 14.2](#principle-142)
    - [Practice 14.2](#practice-142)
      - [Lab 14.2.1: Pinned plugins](#lab-1421-pinned-plugins)
      - [Lab 14.2.2: JCasC replaces the setup wizard](#lab-1422-jcasc-replaces-the-setup-wizard)
      - [Lab 14.2.3: Matrix-based security](#lab-1423-matrix-based-security)
      - [Lab 14.2.4: Rebuild from code](#lab-1424-rebuild-from-code)
    - [Retrospective 14.2](#retrospective-142)
  - [Lesson 14.3: Ephemeral agents](#lesson-143-ephemeral-agents)
    - [Principle 14.3](#principle-143)
    - [Practice 14.3](#practice-143)
      - [Lab 14.3.1: An EC2 cloud](#lab-1431-an-ec2-cloud)
      - [Lab 14.3.2: Least privilege for the controller](#lab-1432-least-privilege-for-the-controller)
      - [Lab 14.3.3: Jenkins native tools](#lab-1433-jenkins-native-tools)
    - [Retrospective 14.3](#retrospective-143)
  - [Lesson 14.4: Pipelines](#lesson-144-pipelines)
    - [Principle 14.4](#principle-144)
    - [Practice 14.4](#practice-144)
      - [Lab 14.4.1: A declarative Jenkinsfile](#lab-1441-a-declarative-jenkinsfile)
      - [Lab 14.4.2: Artifacts and parameters](#lab-1442-artifacts-and-parameters)
      - [Lab 14.4.3: AWS permissions for builds](#lab-1443-aws-permissions-for-builds)
      - [Lab 14.4.4: Pipeline reuse with a shared library](#lab-1444-pipeline-reuse-with-a-shared-library)
    - [Retrospective 14.4](#retrospective-144)
  - [Lesson 14.5: Backup and recovery](#lesson-145-backup-and-recovery)
    - [Principle 14.5](#principle-145)
    - [Practice 14.5](#practice-145)
      - [Lab 14.5.1: Scheduled snapshots](#lab-1451-scheduled-snapshots)
      - [Lab 14.5.2: Restore JENKINS_HOME](#lab-1452-restore-jenkins_home)
      - [Lab 14.5.3: Clean up the module](#lab-1453-clean-up-the-module)
    - [Retrospective 14.5](#retrospective-145)
  - [Further Reading](#further-reading)

<!-- /TOC -->

## What changed in the 2026 edition

- **New infrastructure.** The old `base.yaml` opened SSH and ICMP to
  `0.0.0.0/0`, had a malformed network ACL, left out the instance type and
  hard-coded AMI IDs. The new one runs the controller on Amazon Linux 2023
  from the SSM public parameter, requires IMDSv2, has **no inbound rules**,
  and binds Jenkins to `127.0.0.1`. You reach the UI with Session Manager
  port forwarding, not an Elastic IP.
- **Java 21.** Since LTS 2.555.1 (April 2026) Jenkins needs Java 21 or 25 on
  the controller *and* on agents; Java 17 is no longer supported. The LTS
  line in September 2026 is 2.568.x. The old labs used OpenJDK 8, Ubuntu
  18.04 and the original Amazon Linux AMI, all end of life.
- **Configuration as code.** The 2022 text called Jenkins Configuration as
  Code (JCasC) "not recommended". It is now the normal way to run Jenkins:
  plugins pinned in `plugins.txt`, installed by the plugin installation
  manager tool, and system configuration in JCasC YAML kept in Git.
- **Ephemeral agents with no stored AWS keys.** Two hand-registered static
  agents are replaced by the EC2 plugin, which launches an agent per build
  using the controller's **instance role** and terminates it afterwards. The
  controller's IAM policy only lets it launch and terminate instances tagged
  with its own cloud name.
- **Builds get AWS permissions from the agent's role**, and artifacts go to
  S3 through Artifact Manager on S3, which also uses the instance role.
- **Pipelines are declarative Jenkinsfiles.** The Freestyle "team A" job is
  gone; reuse is taught with a shared library.
- **Backup** uses scheduled EBS snapshots and a root-volume replacement
  instead of hand-made snapshots and a rebuilt instance.
- Jenkins now says **controller** and **agent**; the links moved from the
  retired wiki to jenkins.io. The sample Java app targets Java 21 with JUnit
  Jupiter and current Maven plugins.
- Labs run in the lab account in `us-east-2` with the `lab` profile.

## Exam coverage

| Exam | Domain / task statement |
|---|---|
| DOP-C02 | Domain 1: SDLC Automation (Task 1.1: implement CI/CD pipelines; Task 1.2: integrate automated testing into pipelines; Task 1.3: build and manage artifacts) |
| DOP-C02 | Domain 2: Configuration Management and IaC (Task 2.1: define cloud infrastructure and reusable components to provision and manage systems throughout their lifecycle) |
| DOP-C02 | Domain 3: Resilient Cloud Solutions (Task 3.3: implement automated recovery processes to meet RTO and RPO requirements) |
| DOP-C02 | Domain 4: Monitoring and Logging (Task 4.1: configure the collection, aggregation and storage of logs and metrics) |
| DOP-C02 | Domain 6: Security and Compliance (Task 6.1: implement techniques for identity and access management at scale; Task 6.2: apply automation for security controls and data protection) |

## Cost and cleanup

- **The controller** is a `t3.medium` (about $0.042 an hour, roughly $1 a
  day) with a 30 GiB gp3 root volume (about $2.40 a month, billed while the
  volume exists, even with the instance stopped).
- **Agents** are `t3.small` (about $0.021 an hour) and exist only while a
  build runs plus the idle timeout you set. An agent left behind by a
  deleted controller keeps billing, so the cleanup lab checks for strays.
- **Public IPv4 addresses** cost $0.005 an hour each: one for the
  controller, one per running agent. That is still far cheaper than a NAT
  gateway.
- **Small charges:** one Secrets Manager secret ($0.40 a month, prorated),
  S3 storage for configuration and artifacts (artifacts expire after 30
  days), CloudWatch Logs ingestion and storage, and EBS snapshots (about
  $0.05 per GB-month) from Lesson 14.5.
- Stop the controller between sessions (`aws ec2 stop-instances`) or
  delete the stack. Everything except build history can be rebuilt from
  your repository; that is the point of Lesson 14.2.
- **Cleanup:** [Lab 14.5.3](#lab-1453-clean-up-the-module) terminates stray
  agents, empties the bucket, deletes the stacks, snapshots and log group.

## Guidance

- Explore the official docs! See the
  [Jenkins User Handbook](https://www.jenkins.io/doc/book/), the
  [Pipeline syntax reference](https://www.jenkins.io/doc/book/pipeline/syntax/),
  the [plugin index](https://plugins.jenkins.io/) and, on the AWS side, the
  [Session Manager](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager.html)
  and
  [CloudFormation template reference](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/introduction.html)
  docs.
- A plugin's own page and README are its documentation. Read the
  configuration-as-code examples there, then confirm key names on your
  controller under **Manage Jenkins > Configuration as Code >
  Documentation**.
- Avoid copying Jenkins setups from blog posts: most still use Java 11 or
  17, `master`, open port 8080 and access keys stored in Jenkins.
- Only configure what your architecture needs. Jenkins has thousands of
  options; you don't need most of them.

## Conventions

- **Profile and Region.** Everything runs in the lab account with the `lab`
  profile, in `us-east-2`. CLI examples don't pass `--region`.
- **Names.** `<you>` is your identifier and the stack's `StudentId`
  parameter. Name your stack `<you>-jenkins`.
- **Placeholders.** Examples use `123456789012` for the account ID and
  `i-0123456789abcdef0` for an instance. Don't commit your real account ID.
- **Your repository.** Copy `base.yaml`, `jenkins/` and `my-app/` from this
  directory into your lab repository and work there. `jenkins/` is what you
  upload to the bucket; `my-app/` is what your pipeline builds.
- **Session Manager plugin.** You installed it in module 05; check it with
  `session-manager-plugin --version`.

## Lesson 14.1: A controller nobody can reach

### Principle 14.1

*A Jenkins controller can run anything on anything it is connected to, so
treat it as a production system: no port open to the internet, access
granted by IAM, and a log you can read without logging in.*

### Practice 14.1

Jenkins is an open-source automation server; the **controller** schedules
work and keeps configuration and history, and **agents** run the builds.
`base.yaml` builds the controller host for you: an Amazon Linux 2023
instance with Java 21 and the current Jenkins LTS from the Jenkins RPM
repository, plus the roles, security groups, key pair, secret and bucket
the later lessons use. Read it before you deploy it; every lab in this
module changes something in it or in `jenkins/`.

#### Lab 14.1.1: Deploy the controller

- Read `base.yaml` and answer for yourself: what can reach the controller,
  what can the controller reach, and what does its role allow? Find where
  the Jenkins package repository comes from, and what the systemd drop-in
  under `/etc/systemd/system/jenkins.service.d/` sets.
- Deploy it into a public subnet of the default VPC (or your module 04
  VPC) with `aws cloudformation deploy`, parameters from `base-params.json`
  or `--parameter-overrides`, and `--capabilities CAPABILITY_IAM`.
- The stack waits for the instance's `cfn-signal`. If it fails, start a
  Session Manager shell and read `/var/log/cfn-init.log` and
  `/var/log/cfn-init-cmd.log` before you delete anything.

##### Question: Where is the internet?

_The controller has a public IPv4 address but its security group has no
inbound rules. What can a scanner on the internet do with that address?
Why does the template use a public address at all instead of a private
subnet, and what would a private subnet need instead?_

#### Lab 14.1.2: Reach Jenkins through Session Manager

- Start a port-forwarding session to the controller with the
  `AWS-StartPortForwardingSession` document (the stack's
  `PortForwardCommand` output) and open `http://localhost:8080/`. See
  [Start a session](https://docs.aws.amazon.com/systems-manager/latest/userguide/session-manager-working-with-sessions-start.html),
  section on port forwarding.
- Jenkins shows **Unlock Jenkins**. Read the initial admin password from
  `/var/lib/jenkins/secrets/initialAdminPassword` with a Session Manager
  shell, not SSH.
- Finish the setup wizard with **no** plugins selected and look around:
  **Manage Jenkins**, **Nodes**, **Credentials**, **Security**. Don't
  configure anything yet; Lesson 14.2 throws this state away.
- On the instance, run `ss -tlnp | grep 8080`. Which address is Jenkins
  listening on, and where is that set?

##### Question: Port forwarding and the listen address

_Jenkins listens on `127.0.0.1`. Why does port forwarding still work? What
else, besides the missing inbound rule, now stops another instance in the
VPC from reaching the UI?_

#### Lab 14.1.3: Ship the Jenkins log to CloudWatch

The Jenkins package runs under systemd and logs to the journal by default
(see the commented `JENKINS_LOG` line in the unit file,
`systemctl cat jenkins`).

- In `base.yaml`, set `JENKINS_LOG` in the drop-in so Jenkins also writes
  `/var/log/jenkins/jenkins.log`, and make sure the `jenkins` user can
  write that directory.
- Install and configure the
  [CloudWatch agent](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/install-CloudWatch-Agent-on-EC2-Instance.html)
  through cfn-init to ship that file to a log group `/<you>/jenkins` that
  the template creates with a 7-day retention.
- Give the controller role only the permissions the agent needs for that
  log group (the TODO in `ControllerRole`).
- Update the stack and follow the log with `aws logs tail --follow`.
  Restart Jenkins and watch it start.

##### Question: One log for everything

_Build logs from agents appear in the Jenkins UI. Are they in the file you
just shipped? Where does Jenkins keep them, and what would you do if an
auditor wanted build logs kept for a year?_

### Retrospective 14.1

#### Question: Agent access

_Agents accept SSH, but only from the controller's security group. Is that
an exception to "no inbound SSH"? What would you need to change to remove
it?_

#### Question: A load balancer instead

_A team of fifty can't all run port-forwarding sessions. Sketch the
alternative: an Application Load Balancer with an ACM certificate,
authentication at the listener (OIDC or Amazon Cognito) and AWS WAF, with
the controller in a private subnet. Which security group rules, Jenkins
settings (listen address, Jenkins URL) and costs change? How do GitHub
webhooks reach Jenkins in each design?_

## Lesson 14.2: Configuration as code

### Principle 14.2

*If you can't rebuild your Jenkins controller from a Git repository, you
don't have a Jenkins controller, you have a pet.*

### Practice 14.2

Plugins are where Jenkins gets almost all of its features, and where most
of its security advisories come from. Configuration made by clicking is
invisible in review and lost with the instance. In this lesson you pin the
plugins, describe the system in YAML, and prove you can rebuild the
controller from that alone.

The loop is always the same:

1. Edit `jenkins/plugins.txt` or `jenkins/casc/*.yaml` in your repository.
2. `aws s3 sync jenkins/ s3://<bucket>/jenkins/ --delete`
3. Run `/usr/local/sbin/jenkins-apply-config` on the controller with
   [Run Command](https://docs.aws.amazon.com/systems-manager/latest/userguide/running-commands.html)
   (`AWS-RunShellScript`) and read its output with
   `aws ssm get-command-invocation`.

The same script runs at boot, so a new controller comes up configured.

#### Lab 14.2.1: Pinned plugins

- Browse the [plugin index](https://plugins.jenkins.io/). For each plugin
  in the starter `plugins.txt`, find what it does, its current version, its
  health score and whether it has open security warnings.
- Read the README of the
  [plugin installation manager tool](https://github.com/jenkinsci/plugin-installation-manager-tool),
  particularly the `--latest` option and version pinning.
- Upload the starter and apply it. Then list the installed plugins
  (`ls /var/lib/jenkins/plugins`, or **Manage Jenkins > Plugins**).

##### Question: Pinned, but only at the top

_You pinned four plugins; how many were installed? What decided the
versions of the others, and what would you do to make the whole set
reproducible? What is the trade-off between pinned versions and security
fixes?_

#### Lab 14.2.2: JCasC replaces the setup wizard

- Read the
  [Configuration as Code](https://www.jenkins.io/doc/book/managing/casc/)
  handbook page and the plugin's
  [secrets documentation](https://github.com/jenkinsci/configuration-as-code-plugin/blob/master/docs/features/secrets.adoc).
- Read `jenkins/casc/jenkins.yaml`. Work out where each `${...}` value
  comes from: an environment variable from the drop-in, or a file that
  `jenkins-apply-config` fetched from Parameter Store or Secrets Manager.
- In `base.yaml`, add the system property that skips the setup wizard to
  `JAVA_OPTS` in the drop-in. Update the stack, upload the starter JCasC
  file and apply.
- Log in as `admin` with the password from Secrets Manager (the stack's
  `AdminPasswordSecretArn` output). Check **Manage Jenkins > Configuration
  as Code > View Configuration**.
- Change the system message in the UI, then apply again. What happened to
  your change?

##### Question: Secrets in configuration

_The admin password and the agents' SSH key reach Jenkins through files
written at boot. Where else could JCasC get them (look at the secret
sources the plugin supports), and what would each option change about the
controller's IAM policy and what sits on its disk?_

#### Lab 14.2.3: Matrix-based security

- Add the [Matrix Authorization Strategy](https://plugins.jenkins.io/matrix-auth/)
  plugin to `plugins.txt`, pinned.
- In JCasC, replace `loggedInUsersCanDoAnything` with a global matrix: the
  admin has `Overall/Administer`, and a second user `<you>-viewer` can only
  read jobs and builds. Store the viewer's password the same way as the
  admin's.
- Log in as the viewer in a private browser window and confirm what it
  can't do.

##### Question: Who else is an administrator?

_Name two other ways, outside the Jenkins permission matrix, that someone
could become effectively an administrator of this controller. Consider IAM
and the Session Manager permissions you gave yourself, and who can change
a Jenkinsfile._

#### Lab 14.2.4: Rebuild from code

- Deploy a second copy of the stack from the same files, as
  `<you>-jenkins-b` with `StudentId` `<you>-b`, upload the same `jenkins/`
  directory to its bucket and let it boot.
- Compare the two controllers. List what is the same and what is missing
  on the new one.
- Delete the second stack (empty its bucket first).

##### Question: What is still a pet?

_What was missing on the rebuilt controller? Which of it should be in code
(hint: jobs, and who maintains the plugin that would define them), and
which of it is data you have to back up instead (Lesson 14.5)?_

### Retrospective 14.2

#### Question: Plugin management

_Compare four ways to manage plugins: clicking in the UI, `plugins.txt`
with the plugin installation manager tool, a custom container image built
`FROM jenkins/jenkins:lts-jdk21`, and a golden AMI built with EC2 Image
Builder (module 20). Which suits this controller, and which would you pick
for twenty teams?_

## Lesson 14.3: Ephemeral agents

### Principle 14.3

*Build agents should be cattle: created for a build, given only the
permissions that build needs, and destroyed afterwards.*

### Practice 14.3

A static agent collects state between builds (files in the workspace,
credentials, installed tools) and costs money while idle. The
[EC2 plugin](https://plugins.jenkins.io/ec2/) launches an instance when a
build needs a label, connects to it over SSH from the controller, and
terminates it when it has been idle long enough or has run its quota of
builds. The plugin calls EC2 with the controller's instance role, so there
are no AWS keys in Jenkins.

#### Lab 14.3.1: An EC2 cloud

- Finish the `amazonEC2` cloud in `jenkins/casc/jenkins.yaml`. Use the
  plugin's page and **Manage Jenkins > Configuration as Code >
  Documentation** to find the keys for:
  - connecting over the agent's **private IP** and giving it a **public
    IP** (the agent needs outbound HTTPS, and there is no NAT gateway);
  - IMDSv2 required, hop limit 1;
  - host key verification that doesn't blindly accept any key;
  - an init script that installs Java 21 (`java-21-amazon-corretto-headless`)
    and Git, because agents need the same Java as the controller;
  - an idle timeout, an instance cap of 2, and **one build per agent**.
- Apply, then create a Pipeline job in the UI whose script needs the
  `al2023` label and runs `java -version` and `aws sts get-caller-identity`.
- Watch the agent appear and disappear:
  `aws ec2 describe-instances --filters Name=tag:jenkins_cloud_name,Values=<you>-agents`.
  Read the agent's launch log in **Manage Jenkins > Nodes**.

##### Question: Whose identity?

_Which role did `aws sts get-caller-identity` report, the controller's or
the agent's? Why is that the one you want?_

##### Question: How long did you wait?

_How long did the build wait for its agent? Which settings trade that wait
for cost (spare instances, idle time, instance type, a pre-baked AMI), and
what would you choose for a team that builds every few minutes?_

#### Lab 14.3.2: Least privilege for the controller

- Compare the `ec2-plugin-agents` policy in `base.yaml` with the policy on
  the EC2 plugin's page. For every difference, say why it is safe to leave
  out or narrow. Use the
  [EC2 example policies](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ExamplePolicies_EC2.html)
  to understand the tag conditions.
- Break it on purpose: change the cloud's `name` in JCasC to anything other
  than `${AGENT_CLOUD_NAME}`, apply, and start a build. Find the error in the
  Jenkins log, decode the message with `aws sts
  decode-authorization-message`, and restore the name.
- Find the matching `RunInstances` event in CloudTrail event history.
  <!-- VERIFY: an end-to-end run with this trimmed policy (launch, tag,
  connect, terminate) with EC2 plugin 2064.x; it was built from the plugin
  source, not from a live test. -->

##### Question: A compromised controller

_Someone gets the script console on this controller. With this role, what
can they do in the account? What could they have done with the policy from
the plugin page, which allows `iam:PassRole` on `*`?_

#### Lab 14.3.3: Jenkins native tools

- Add a Maven installation under `tool:` in JCasC that installs a current
  Maven 3.9 release automatically; it is installed on each agent at first
  use. See [Managing tools](https://www.jenkins.io/doc/book/managing/tools/).
- Read about the
  [script console](https://www.jenkins.io/doc/book/managing/script-console/),
  the [Jenkins CLI](https://www.jenkins.io/doc/book/managing/cli/) and the
  [remote access API](https://www.jenkins.io/doc/book/using/remote-access-api/).
  Use the CLI or the API (through your port-forwarding session, with an API
  token) to list jobs and trigger a build.

##### Question: The most powerful page

_Why is the script console as powerful as a root shell on the controller?
Who should have it, and how does that relate to the JCasC approach of not
changing things by hand?_

### Retrospective 14.3

#### Question: Other ways to get agents

_Compare the EC2 plugin with the EC2 Fleet plugin (an Auto Scaling group or
Spot Fleet as the pool), the Kubernetes plugin on EKS (module 15), and
running builds in AWS CodeBuild (module 12). What does each need on the
network, in IAM and in the controller?_

## Lesson 14.4: Pipelines

### Principle 14.4

*[A Pipeline is a user-defined model of a CD pipeline](https://www.jenkins.io/doc/book/pipeline/),
and it belongs in the repository next to the code it builds.*

### Practice 14.4

Pipelines are written in a `Jenkinsfile` using the
[declarative syntax](https://www.jenkins.io/doc/book/pipeline/syntax/#declarative-pipeline).
Scripted syntax still exists and appears inside `script {}` blocks and
shared libraries, but new pipelines should be declarative: it is
validated before it runs, it is easier to review, and it is what the
tooling and documentation assume. `my-app/Jenkinsfile` is a starter.

#### Lab 14.4.1: A declarative Jenkinsfile

- Read [Using a Jenkinsfile](https://www.jenkins.io/doc/book/pipeline/jenkinsfile/)
  and [Branches and pull requests](https://www.jenkins.io/doc/book/pipeline/multibranch/).
- Finish the starter: use the Maven tool from Lab 14.3.3 and publish the
  JUnit results.
- Create a **Multibranch Pipeline** job for your lab repository (a public
  repository needs no credentials to clone over HTTPS). Commit and push to
  `main` and to a feature branch and watch each branch get its own job.
- Your controller can't receive webhooks. Configure periodic branch
  scanning instead.
- Use [Replay](https://www.jenkins.io/doc/book/pipeline/development/#replay)
  to try a change without committing it.

##### Question: Webhooks

_Polling works but wastes calls and adds delay. How would you get GitHub
webhooks to this controller without opening it to the internet? Compare
putting a load balancer in front, relaying through Amazon API Gateway and
Lambda, and a relay service._

#### Lab 14.4.2: Artifacts and parameters

##### Task: Artifact storage

Artifacts kept on the controller's disk are lost with it and fill it up.

- Add [Artifact Manager on S3](https://plugins.jenkins.io/artifact-manager-s3/)
  to `plugins.txt` and configure it in JCasC to use the stack's bucket with
  the `artifacts/` prefix and the instance profile (no credentials).
- Finish the controller's `controller-bucket` policy from the plugin's
  README; add nothing it doesn't ask for.
- Archive the jar with `archiveArtifacts` and find it in S3.

##### Task: Build parameters

- Add a string, a choice and a boolean parameter and use them in a stage of
  their own. Note what happens the first time a branch job runs after you
  add them.

##### Question: Who uploads?

_The build ran on the agent, and the agent's role has no S3 permissions.
How did the jar get into the bucket? What does that mean for a malicious
build that wants to overwrite another job's artifacts?_

#### Lab 14.4.3: AWS permissions for builds

- Create a parameter `/<you>/jenkins/greeting` in Parameter Store (in a
  template, not the console).
- Add a stage that reads it with the AWS CLI. It fails; read the error.
- Fix it the right way: a policy on the **agent** role in `base.yaml` that
  allows `ssm:GetParameter` on that one parameter. Don't add credentials to
  Jenkins and don't touch the controller role.

##### Question: One role for every build

_Every build on these agents gets the same role. What goes wrong when two
teams with different permissions share this cloud? How would you give each
team its own role (hint: agent templates and labels, and who may use
them)?_

#### Lab 14.4.4: Pipeline reuse with a shared library

Every team copying the same Jenkinsfile quickly becomes hard to maintain.
A [shared library](https://www.jenkins.io/doc/book/pipeline/shared-libraries/)
keeps common steps in one repository.

- Create a library repository (or a directory of your lab repository) with
  `vars/mvnBuild.groovy`, a step that prints the environment with `env` and
  runs `mvn -B clean verify`.
- Configure it as a global library in JCasC, pinned to a tag rather than a
  branch.
- Replace the `sh 'mvn ...'` step with `mvnBuild()` and confirm in the build
  log that the library ran.

##### Question: Trusted code

_Global libraries run outside the Groovy sandbox. What does that mean for
who may push to the library repository, and why did you pin it to a tag?_

### Retrospective 14.4

#### Question: Build definition management

_Build definitions usually live in each project's repository. With many
projects, how would you centralise them so that a platform team controls
what every pipeline must do (tests, scans, approvals) while teams still
own their builds?_

#### Question: Jenkins or CodePipeline?

_You built the same kind of pipeline with CodePipeline in module 12.
Compare them on what you operate, how builds get AWS permissions, cost when
idle, and plugin risk. When would you still choose Jenkins in 2026?_

## Lesson 14.5: Backup and recovery

### Principle 14.5

*Anything that can go wrong will go wrong. Rebuild configuration from code;
back up only the data code can't recreate.*

### Practice 14.5

After Lesson 14.2, the controller's configuration comes from Git.
`JENKINS_HOME` (`/var/lib/jenkins`) still holds build history, job state,
credentials added by hand and the key that encrypts stored secrets. Read
[Backing-up/Restoring Jenkins](https://www.jenkins.io/doc/book/system-administration/backing-up/)
first: it lists what matters in `JENKINS_HOME` and what doesn't.

#### Lab 14.5.1: Scheduled snapshots

- In a separate template, create an
  [Amazon Data Lifecycle Manager](https://docs.aws.amazon.com/ebs/latest/userguide/snapshot-lifecycle.html)
  policy (or an [AWS Backup](https://docs.aws.amazon.com/aws-backup/latest/devguide/whatisbackup.html)
  plan) that snapshots volumes tagged `Name=<you>-jenkins-home` daily and
  keeps three.
- Take one snapshot now as well, so you don't have to wait a day.

##### Question: A consistent snapshot

_Jenkins keeps writing while the snapshot is taken. Is a snapshot of a
running controller safe to restore? What would you do before a snapshot to
make it consistent, and what does that cost in availability?_

#### Lab 14.5.2: Restore JENKINS_HOME

- Run a few builds, snapshot, then delete a job and its builds.
- Restore with a
  [root volume replacement](https://docs.aws.amazon.com/ebs/latest/userguide/replace-root.html)
  from your snapshot. Confirm the job, its build history and its artifacts
  (in S3) are back.
- Time it. That is your recovery time for this design.

##### Question: RTO and RPO

_With daily snapshots and the restore you just timed, what are this
controller's RPO and RTO? How would you shrink each (for example, JENKINS_HOME
on its own EBS volume or on EFS, an Auto Scaling group of one, more
frequent snapshots), and what does each cost?_

#### Lab 14.5.3: Clean up the module

- Stop any running builds, then check for agents the plugin didn't clean
  up: `aws ec2 describe-instances --filters
  Name=tag:jenkins_cloud_name,Values=<you>-agents
  Name=instance-state-name,Values=pending,running,stopped`. Terminate them:
  running agents keep the agent security group and instance profile in use,
  so the stack deletion fails.
- Empty the bucket (`aws s3 rm s3://<bucket> --recursive`).
- Delete the stacks: `<you>-jenkins`, the snapshot policy stack, any
  `-b` stack from Lab 14.2.4, and the parameter from Lab 14.4.3.
- Delete the snapshots the policy and you made
  (`aws ec2 describe-snapshots --owner-ids self` filtered by tag), and the
  `/<you>/jenkins` log group if its stack didn't own it.
- Confirm nothing tagged with your `Student` tag is left, with the Resource
  Groups Tagging API (`aws resourcegroupstaggingapi get-resources`).

### Retrospective 14.5

#### Question: What to back up

_List what in `JENKINS_HOME` you would still back up now that configuration
is in Git, and what you would deliberately leave out. Where does
`secrets/master.key` fit, and what happens to stored credentials if you
restore everything except it?_

## Further Reading

- [Jenkins LTS changelog](https://www.jenkins.io/changelog-stable/) and the
  [LTS upgrade guides](https://www.jenkins.io/doc/upgrade-guide/): read
  them before every upgrade; 2.555.x is the one that required Java 21.
- [Java support policy](https://www.jenkins.io/doc/book/platform-information/support-policy-java/):
  which Java versions each Jenkins line supports.
- [Jenkins security advisories](https://www.jenkins.io/security/advisories/):
  most are about plugins, which is why you pin and review them.
- [Securing Jenkins](https://www.jenkins.io/doc/book/security/) and
  [Controller isolation](https://www.jenkins.io/doc/book/security/controller-isolation/):
  why builds shouldn't run on the controller.
- [Access Control for Builds](https://www.jenkins.io/doc/book/security/build-authorization/):
  which identity a build runs as inside Jenkins.
- [Parallel stages and matrix](https://www.jenkins.io/doc/book/pipeline/syntax/#parallel):
  run stages concurrently, for example on x86_64 and Graviton agents.
- [Authenticate users using an Application Load Balancer](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/listener-authenticate-users.html):
  the building block for the load-balancer design in Retrospective 14.1.
