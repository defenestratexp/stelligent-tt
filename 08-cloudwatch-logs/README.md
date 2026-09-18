# Topic 8: Observability

<!-- TOC -->

- [Topic 8: Observability](#topic-8-observability)
  - [What changed in the 2026 edition](#what-changed-in-the-2026-edition)
  - [Exam coverage](#exam-coverage)
  - [Cost and cleanup](#cost-and-cleanup)
  - [Guidance](#guidance)
  - [Lesson 8.1: CloudWatch Logs Storage and Retrieval](#lesson-81-cloudwatch-logs-storage-and-retrieval)
    - [Principle 8.1](#principle-81)
    - [Practice 8.1](#practice-81)
      - [Lab 8.1.1: Log Groups and Streams](#lab-811-log-groups-and-streams)
        - [Question: Sequence Tokens](#question-sequence-tokens)
      - [Lab 8.1.2: The CloudWatch Agent](#lab-812-the-cloudwatch-agent)
        - [Question: Parameter Name](#question-parameter-name)
        - [Question: Applying a New Configuration](#question-applying-a-new-configuration)
      - [Lab 8.1.3: Tailing Logs](#lab-813-tailing-logs)
        - [Question: Tail or Live Tail](#question-tail-or-live-tail)
      - [Lab 8.1.4: Log Lifecycle](#lab-814-log-lifecycle)
        - [Question: Never Expire](#question-never-expire)
        - [Question: Choosing a Log Class](#question-choosing-a-log-class)
    - [Retrospective 8.1](#retrospective-81)
      - [Question: A Useful Lifecycle](#question-a-useful-lifecycle)
  - [Lesson 8.2: From Logs to Alarms](#lesson-82-from-logs-to-alarms)
    - [Principle 8.2](#principle-82)
    - [Practice 8.2](#practice-82)
      - [Lab 8.2.1: Logs Insights](#lab-821-logs-insights)
        - [Question: Paying for Queries](#question-paying-for-queries)
      - [Lab 8.2.2: Metric Filters](#lab-822-metric-filters)
        - [Question: No Backfill](#question-no-backfill)
        - [Question: Default Values and Dimensions](#question-default-values-and-dimensions)
      - [Lab 8.2.3: Alarms and Notifications](#lab-823-alarms-and-notifications)
        - [Question: Missing Data](#question-missing-data)
        - [Question: Composite Alarms](#question-composite-alarms)
      - [Lab 8.2.4: A Dashboard](#lab-824-a-dashboard)
      - [Lab 8.2.5: VPC Flow Logs](#lab-825-vpc-flow-logs)
        - [Question: Who Is Knocking](#question-who-is-knocking)
    - [Retrospective 8.2](#retrospective-82)
      - [Question: Metric Filters or Embedded Metrics](#question-metric-filters-or-embedded-metrics)
  - [Lesson 8.3: Auditing and Reacting to Change](#lesson-83-auditing-and-reacting-to-change)
    - [Principle 8.3](#principle-83)
    - [Practice 8.3](#practice-83)
      - [Lab 8.3.1: CloudTrail Event History](#lab-831-cloudtrail-event-history)
        - [Question: What Event History Misses](#question-what-event-history-misses)
      - [Lab 8.3.2: A Trail to CloudWatch Logs](#lab-832-a-trail-to-cloudwatch-logs)
        - [Question: A Second Copy](#question-a-second-copy)
      - [Lab 8.3.3: Alarming on API Activity](#lab-833-alarming-on-api-activity)
      - [Lab 8.3.4: EventBridge Rules](#lab-834-eventbridge-rules)
        - [Question: Which Events Needed the Trail](#question-which-events-needed-the-trail)
        - [Question: Two Paths to One Notification](#question-two-paths-to-one-notification)
      - [Lab 8.3.5: Clean Up](#lab-835-clean-up)
    - [Retrospective 8.3](#retrospective-83)
      - [Question: Events Worth Watching](#question-events-worth-watching)
      - [Task: Beyond Logs and Metrics](#task-beyond-logs-and-metrics)
  - [Further Reading](#further-reading)

<!-- /TOC -->

## What changed in the 2026 edition

- The module is now **Observability**, not just CloudWatch Logs. It covers
  logs, Logs Insights, metric filters, alarms, a dashboard, VPC Flow Logs,
  CloudTrail and EventBridge, which is what the CloudOps (SOA-C03) and
  DevOps (DOP-C02) exams test under monitoring and logging.
- The Cloud9 material is gone: no `.c9logs` log group and no `c9.training`
  stream. Cloud9 is closed to new customers. The log sources are now your
  own AL2023 instance and the AWS services you use.
- The shipped `8.1.2.yml` template was broken (a `files` entry with no
  content, so the YAML didn't describe a valid resource) and launched Ubuntu
  20.04, which is end of life. It is rewritten: Amazon Linux 2023 from the
  SSM public parameter, IMDSv2 required, Session Manager instead of SSH, the
  CloudWatch agent installed with `dnf` and configured from Parameter Store,
  and a small sample service that writes JSON logs to give the later labs
  something to measure. The template passes `cfn-lint`.
- AL2023 has no `/var/log/messages`: it logs to the systemd journal. Lab
  8.1.2 collects the journal with the agent's `journald` section instead of
  tailing a syslog file.
- The third-party `awslogs` tool is replaced by `aws logs tail` (AWS CLI v2)
  and Live Tail.
- New: log classes (Standard and Infrequent Access), Logs Insights, metric
  filters, alarms (including composite alarms), SNS notifications, a
  dashboard, and VPC Flow Logs (which module 04 points here for).
- "CloudWatch Events" is EventBridge. Lesson 8.3 separates events AWS
  services send by themselves (such as EC2 state changes) from API-call
  events, which need a CloudTrail trail. The old retrospective task that
  emailed you on EC2 changes is now Lab 8.3.4.
- Labs run in your lab account in `us-east-2` through the `lab` profile.
  Every log group gets a retention period, and the module ends with a
  cleanup lab.

## Exam coverage

| Exam | Domain / task statement |
|---|---|
| SOA-C03 | Domain 1: Monitoring, Logging, Analysis, Remediation, and Performance Optimization. Task 1.1: Implement metrics, alarms, and filters (Skills 1.1.1 CloudWatch and CloudTrail, 1.1.2 CloudWatch agent, 1.1.3 alarms and composite alarms, 1.1.4 dashboards, 1.1.5 SNS notifications) |
| SOA-C03 | Domain 1. Task 1.2: Identify and remediate issues (Skill 1.2.2: use EventBridge to route events and troubleshoot rules) |
| DOP-C02 | Domain 4: Monitoring and Logging (4.1 collect, aggregate and store logs and metrics; 4.2 audit, monitor and analyze logs and metrics; 4.3 automate monitoring and event management) |
| DOP-C02 | Domain 5: Incident and Event Response (5.1 manage event sources to process, notify and take action) |
| SCS-C03 | Domain 1: Detection (Task 1.1 monitoring and alerting; Task 1.2 logging solutions: CloudTrail, the CloudWatch agent, Logs Insights, VPC Flow Logs) |
| DVA-C02 | Domain 4: Troubleshooting and Optimization (logging and monitoring, custom metrics). C03 adds GenAI / agent topics |

## Cost and cleanup

Prices are for `us-east-2` in September 2026. The labs stay well inside the
CloudWatch free tier if you delete everything at the end.

- **Log ingestion** is $0.50 per GB in the Standard log class and $0.25 per
  GB in Infrequent Access. **Log storage** is $0.03 per GB-month. The free
  tier includes 5 GB a month of ingestion, storage and Logs Insights
  scanning combined. The sample service writes a few MB a day.
- **Logs Insights** queries cost $0.005 per GB scanned. **Live Tail** is
  free for 1,800 minutes a month, then $0.01 per minute: close sessions you
  aren't watching.
- **Custom metrics** (metric filters and the CloudWatch agent's memory and
  disk metrics) are $0.30 per metric per month, prorated by the hour. The
  free tier covers 10.
- **Alarms** are $0.10 per standard-resolution alarm metric per month (10
  free); a **composite alarm** is $0.50 a month. **Dashboards** are $3 a
  month each after the first 3.
- **VPC Flow Logs** delivered to CloudWatch Logs are vended logs: $0.50 per
  GB ingested for the first 10 TB, plus storage. Keep the flow log to one
  network interface and delete it when you finish Lab 8.2.5.
- **CloudTrail:** event history is free. The first trail's copy of
  management events to S3 is free; an additional copy (for example, a
  second trail when an organization trail already covers the account) is
  $2.00 per 100,000 management events. Events sent from a trail to
  CloudWatch Logs are billed as log ingestion.
  <!-- VERIFY: whether the CloudTrail "CloudWatch Logs delivery" charge on the CloudTrail pricing page applies to trail-based delivery or only to the direct (service-linked channel) integration launched in December 2025. -->
- **EventBridge** rules that match AWS service events are free. SNS email
  notifications are free at lab volume.
- **EC2:** the instance in Lab 8.1.2 is a `t4g.micro` (about a cent an hour)
  with a public IPv4 address ($0.005 an hour).
- **Set a retention on every log group.** A log group created by the CLI, the
  agent or a service never expires by default, and CloudFormation creates
  none for you unless you declare it. Forgotten log groups are the usual
  source of a small bill that never goes away.
- Lab 8.3.5 removes everything this module creates and checks for leftovers.

## Guidance

- Explore the official docs! See the
  [CloudWatch Logs User Guide](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html),
  the
  [CloudWatch User Guide](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html),
  the
  [EventBridge User Guide](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html),
  the
  [CloudTrail User Guide](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html),
  the [CLI reference](https://docs.aws.amazon.com/cli/latest/reference/logs/)
  and the
  [CloudFormation template reference](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/AWS_Logs.html).

- Avoid using other sites like stackoverflow.com for answers \-- part
  of the skill set you're building is finding answers straight from
  the source, AWS. Many CloudWatch tutorials still install the retired
  CloudWatch Logs agent (`awslogs`) or read `/var/log/messages`, which
  AL2023 doesn't have.

- Explore your curiosity. Try to understand why things work the way
  they do. Read more of the documentation than just what you need to
  find the answers.

- Use the `lab` profile. It sets the lab region (`us-east-2`), so the CLI
  commands in this module don't need `--region`. Include your identifier in
  stack names, log group names and tags. This module uses log group names
  of the form `/stelligent-u/<you>/lab08/<purpose>`.

- Don't open SSH. The instance in this module has no inbound rules; connect
  with Session Manager (module 05) and run commands with Run Command.

- DO review the CloudFormation documentation to see if a property is
  required when creating a resource.

## Lesson 8.1: CloudWatch Logs Storage and Retrieval

### Principle 8.1

*CloudWatch Logs stores text logs from your applications and from AWS
services in one place, with access control, encryption and a retention
period you choose, so you don't need to log in to a server to read them.*

### Practice 8.1

A **log group** is a set of log streams that share retention, encryption and
access settings. A **log stream** is a sequence of events from one source,
such as one instance. You'll create both by hand, then have the CloudWatch
agent ship an instance's application logs and journal, read them back from
the CLI as they arrive, and decide how long to keep them.

#### Lab 8.1.1: Log Groups and Streams

Use the CLI (see
[Working with log groups and log streams](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html)):

- Create a log group named `/stelligent-u/<you>/lab08/cli`, tagged with
  your identifier.

- Create a log stream named `manual` in it.

- Send three events with
  [put-log-events](https://docs.aws.amazon.com/cli/latest/reference/logs/put-log-events.html).
  Make one of them a JSON object such as
  `{"level":"ERROR","msg":"disk full"}`. Timestamps are in milliseconds
  since the epoch.

- Read them back with `aws logs get-log-events`, then find only the JSON
  event with `aws logs filter-log-events` and a
  [filter pattern](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/FilterAndPatternSyntax.html)
  such as `{ $.level = "ERROR" }`.

- List your log groups with `describe-log-groups
  --log-group-name-prefix /stelligent-u/<you>` and the streams in your group.
  What is the group's retention?

Save your commands (not their output) in your repository.

##### Question: Sequence Tokens

_Older examples pass `--sequence-token` to `put-log-events` and handle
`InvalidSequenceTokenException`. What does the
[PutLogEvents API reference](https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_PutLogEvents.html)
say about sequence tokens now? What limits does it still impose on a batch
(size, number of events, time span)?_

#### Lab 8.1.2: The CloudWatch Agent

The
[CloudWatch agent](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Install-CloudWatch-Agent.html)
is the standard way to send an instance's logs and extra metrics to
CloudWatch. You installed it for metrics in module 05. Now it ships logs.

The starter template [8.1.2.yml](8.1.2.yml) in this directory launches an
AL2023 instance with:

- a sample service, `lab08-app`, that appends a JSON line to
  `/var/log/lab08/app.log` every two seconds (level, path, status code and
  latency), with about 5% errors;
- two log groups, `.../app` and `.../system`, with a retention period;
- the agent, installed with `dnf` and started with its configuration from a
  Parameter Store parameter. That configuration collects memory and disk
  metrics but **no logs** yet.

Copy the template into your repository, then:

- Create the stack in the default VPC. You need
  `--capabilities CAPABILITY_IAM`. Wait for it with a waiter: the instance
  signals CloudFormation when its user data finishes.

- Open a Session Manager session and look at the sample log with
  `tail -f /var/log/lab08/app.log`, and at the journal with `journalctl -n
  20`. Why is there no `/var/log/messages`? (See
  [journald on AL2023](https://docs.aws.amazon.com/linux/al2023/ug/journald.html).)

- Complete the `TODO(student)` in the template: add a `logs` section to the
  agent configuration (see the
  [configuration file reference](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Agent-Configuration-File-Details.html))
  that:

  - sends `/var/log/lab08/app.log` to the app log group, with the instance
    ID as the stream name;
  - sends journal entries at priority `warning` and above, plus everything
    from the `amazon-ssm-agent` unit, to the system log group, using the
    `journald` section.

  <!-- VERIFY: that the amazon-cloudwatch-agent package in the AL2023 repository is recent enough to support the journald section; if not, install the agent from the S3 download location instead. -->

- Update the stack. Then make the running agent load the new configuration
  without replacing the instance: either run `amazon-cloudwatch-agent-ctl -a
  fetch-config` in a session, or send the `AmazonCloudWatch-ManageAgent`
  document with Run Command.

- Confirm with `aws logs describe-log-streams` that each group has a stream
  named after your instance ID.

> *Note:* the agent writes its own log to
> `/opt/aws/amazon-cloudwatch-agent/logs/amazon-cloudwatch-agent.log`. Read
> it first when nothing arrives.

##### Question: Parameter Name

_The parameter's name starts with `AmazonCloudWatch-`. Rename it to
something else and the agent can't read it. Why? Read the
[CloudWatchAgentServerPolicy](https://docs.aws.amazon.com/aws-managed-policy/latest/reference/CloudWatchAgentServerPolicy.html)
managed policy. Which other permission in it lets the agent change a log
group's retention, and why does the template create the log groups itself
instead of letting the agent create them?_

##### Question: Applying a New Configuration

_Updating the parameter didn't change what the running agent collected.
Why not? What would have happened if you had changed the user data
instead? How would you roll a new agent configuration out to a hundred
instances?_

#### Lab 8.1.3: Tailing Logs

The original course installed a third-party tool to follow log streams. AWS
CLI v2 does it natively.

- Use
  [aws logs tail](https://docs.aws.amazon.com/cli/latest/reference/logs/tail.html)
  to show the app log group's events from the last 5 minutes, the last 20
  minutes and the last hour, in the `short` format.

- Follow the group with `--follow` while you change the error rate on the
  instance: `echo 30 | sudo tee /etc/lab08/error-rate`. Then set it back to
  5.

- Follow only errors with `--filter-pattern`. Then follow only requests
  slower than 500 ms.

- Start a
  [Live Tail](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatchLogs_LiveTail.html)
  session on both of your groups with `aws logs start-live-tail` (it takes
  log group ARNs, not names). Stop it when you're done.

##### Question: Tail or Live Tail

_`aws logs tail --follow` and Live Tail both show new events as they
arrive. How does each one get its data, and which is billed per minute?
Which one works on a log group in the Infrequent Access class?_

#### Lab 8.1.4: Log Lifecycle

Any time you're logging information, consider how long you need it and what
it costs to keep.

- Use the CLI to
  [set the retention policy](https://docs.aws.amazon.com/cli/latest/reference/logs/put-retention-policy.html)
  of your `cli` log group to 60 days, and check it with
  `describe-log-groups`.

- Find the maximum retention the API accepts, set it, and check again. Then
  remove the retention policy. What is the group's retention now?

- Set the `cli` group back to 1 day.

- Create a second group, `/stelligent-u/<you>/lab08/ia`, in the
  **Infrequent Access**
  [log class](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatch_Logs_Log_Classes.html),
  with a 1-day retention. Put an event in it, then try `get-log-events` and
  `aws logs tail` against it. How do you read it instead?

##### Question: Never Expire

_What is the default retention of a new log group, and what does that
default cost over a year for a service that writes 1 GB a day? What does
the documentation say about how quickly events are deleted once they pass
the retention period?_

##### Question: Choosing a Log Class

_Can you change a log group's class after creating it? List three features
the Infrequent Access class gives up. For which of your logs would you
choose it?_

### Retrospective 8.1

*Log retention affects cost, compliance and incident response. Know what
CloudWatch Logs can and can't do before you choose where logs live.*

- What are the minimum and maximum retention periods?

- Leave the Lesson 8.1 stack running: Lesson 8.2 builds on it. Delete the
  `ia` log group now.

#### Question: A Useful Lifecycle

_Instead of keeping data in CloudWatch Logs forever, what else can you do
with it? Look at
[export to Amazon S3](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/S3Export.html)
and
[subscription filters](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Subscriptions.html).
Sketch a lifecycle for application logs that must be searchable for 30 days
and kept for a year for audits. Which of the two would you use, and why?_

## Lesson 8.2: From Logs to Alarms

### Principle 8.2

*Logs tell you what happened; metrics and alarms tell you when to look. Turn
the log lines that matter into metrics, and alarm on the symptoms your users
would notice.*

### Practice 8.2

You'll query the sample service's logs with Logs Insights, turn errors and
latency into CloudWatch metrics with metric filters, alarm on them with an
SNS email, put the result on a dashboard, and then point the same tools at a
log source AWS writes for you: VPC Flow Logs. Add the new resources to your
Lesson 8.1 template unless a lab says otherwise.

#### Lab 8.2.1: Logs Insights

[CloudWatch Logs Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AnalyzingLogData.html)
queries one or more log groups with a pipe-based
[query language](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html).
It discovers the fields in JSON logs for you.

In the console, write queries against the app log group that:

- count events by `level` in 5-minute bins;
- show the 90th percentile of `latency_ms` for each `path`;
- list the 10 slowest requests with their timestamp, path and status.

Then:

- Run one of them from the CLI with `aws logs start-query` and
  `aws logs get-query-results`. Why are there two commands?

- Save the queries in your template as
  [AWS::Logs::QueryDefinition](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-logs-querydefinition.html)
  resources, update the stack and find them under **Saved queries** in the
  console.

##### Question: Paying for Queries

_Logs Insights charges by data scanned. What scanned data does each query
report, and what three things can you change to scan less? When would you
reach for Logs Insights instead of `filter-log-events`?_

#### Lab 8.2.2: Metric Filters

A
[metric filter](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/MonitoringLogData.html)
turns matching log events into a CloudWatch metric as they arrive. Add two
[AWS::Logs::MetricFilter](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-logs-metricfilter.html)
resources on the app log group, publishing to a namespace that contains
your identifier (for example `StudentU/<you>`):

- `ErrorCount`: 1 for each event whose `level` is `ERROR`, with a default
  value of 0.

- `Latency`: the value of `latency_ms` from every event, with the unit
  `Milliseconds`.

Before you deploy, try your patterns against sample lines with
`aws logs test-metric-filter`. Update the stack, wait a few minutes, and
fetch both metrics with `aws cloudwatch get-metric-statistics` or
`get-metric-data` (use the `Sum` of `ErrorCount` and the `p90` of
`Latency`).

##### Question: No Backfill

_Your app log group already held an hour of errors when you created the
filter. Do they appear in the metric? What would you use to answer a
question about errors from before the filter existed?_

##### Question: Default Values and Dimensions

_What does the default value of 0 change about the `ErrorCount` graph
during quiet periods? Suppose you add `path` as a dimension. Why can't you
keep the default value, and what happens to your metric count (and bill)
if a field used as a dimension has thousands of distinct values?_

#### Lab 8.2.3: Alarms and Notifications

Now alarm on the error metric and get an email.

- Add an
  [SNS topic](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-sns-topic.html)
  and an email subscription to your address, passed in as a parameter.
  Confirm the subscription from the email SNS sends.

- Add an
  [alarm](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html)
  on `ErrorCount` that goes to `ALARM` when the sum is 10 or more in at
  least 3 of the last 5 one-minute periods, and notifies the topic on both
  `ALARM` and `OK`. Choose how it treats missing data.

- Trigger it: raise the error rate to 50% with Run Command (the
  `AWS-RunShellScript` document), not a Session Manager shell. Watch the
  alarm with `aws cloudwatch describe-alarms` and wait for the email. Then
  set the rate back to 5 and wait for `OK`.

- Test the notification path without breaking anything, using
  `aws cloudwatch set-alarm-state`.

- Add a second alarm on the `p90` of `Latency` above 500 ms, then a
  [composite alarm](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Create_Composite_Alarm.html)
  that is in `ALARM` only when both are. Move the SNS action from the
  individual alarms to the composite alarm.

##### Question: Missing Data

_What are the four ways an alarm can
[treat missing data](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html#alarms-and-missing-data)?
Which did you choose for `ErrorCount`, and what would happen with each
choice if the sample service stopped logging entirely? How would you alarm
on that case?_

##### Question: Composite Alarms

_Why might a team page on a composite alarm but not on the alarms inside
it? What
[actions](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/alarm-actions.html)
can an alarm take besides notifying SNS, and how would an alarm state change
reach EventBridge?_

#### Lab 8.2.4: A Dashboard

Add an
[AWS::CloudWatch::Dashboard](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-cloudwatch-dashboard.html)
to your template with:

- `ErrorCount` and the `p90` of `Latency` on one graph;
- the agent's `mem_used_percent` for your instance;
- an alarm status widget for your three alarms;
- a Logs Insights widget that runs your "10 slowest requests" query.

Build the widgets in the console first if you like, then copy the source
from **Actions**, **View/edit source** into the template and replace the
names and IDs with `!Sub` and `!Ref`. The dashboard body format is in the
[dashboard body structure](https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/CloudWatch-Dashboard-Body-Structure.html)
reference.

#### Lab 8.2.5: VPC Flow Logs

[VPC Flow Logs](https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html)
record the IP traffic accepted or rejected at a network interface. Module 04
pointed here; this is where you use them.

- In a separate small template, create a log group
  (`/stelligent-u/<you>/lab08/flow`, 1-day retention), the
  [IAM role](https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-iam-role.html)
  the flow logs service needs to write to it, and an
  [AWS::EC2::FlowLog](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-ec2-flowlog.html)
  for **your instance's network interface only**, capturing all traffic,
  with a one-minute aggregation interval. Take the network interface ID as
  a parameter.

- Wait 15 minutes, then use Logs Insights to find the rejected traffic:
  count rejected records by source address and destination port, and show
  the top 10.

Delete this stack when you've answered the question below.

##### Question: Who Is Knocking

_Your security group has no inbound rules. Where does the rejected traffic
come from, and on which ports? What would you change to capture only
rejected traffic, and what would it save? Why does the flow log need an IAM
role when the CloudWatch agent used the instance's role?_

### Retrospective 8.2

Logs, metrics and traces answer different questions. You've used logs to
find what happened and metrics to know when to look. Traces follow a single
request across services; the
[CloudWatch agent](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Install-CloudWatch-Agent.html)
can also receive OpenTelemetry and X-Ray traces, and
[CloudWatch Application Signals](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Application-Monitoring-Sections.html)
builds service dashboards and service level objectives from them. They're
worth reading about now and using once you have a multi-service application
(modules 09 and 13).

#### Question: Metric Filters or Embedded Metrics

_The sample service could have published its own metrics instead. Compare a
metric filter with the
[embedded metric format](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Embedded_Metric_Format.html)
and with calling `PutMetricData` from the application. Which one needs no
code change, which one sends no extra API calls, and which one works on a
log group in the Infrequent Access class?_

## Lesson 8.3: Auditing and Reacting to Change

### Principle 8.3

*Every change to your AWS resources is an API call or a service event. Record
the calls with CloudTrail, and react to the events with EventBridge instead
of waiting for someone to notice.*

### Practice 8.3

CloudTrail records API activity in your account. EventBridge receives events
from AWS services, including CloudTrail's record of each API call, and
routes them to targets such as SNS, Lambda or Systems Manager. You'll look
at what CloudTrail keeps for free, build a trail that writes to CloudWatch
Logs, alarm on a class of API call, and write EventBridge rules that tell
you about changes as they happen.

#### Lab 8.3.1: CloudTrail Event History

CloudTrail keeps 90 days of management events in
[event history](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/view-cloudtrail-events.html)
without any setup.

- Use `aws cloudtrail lookup-events` to find the `PutMetricAlarm` calls
  that created your alarms in Lab 8.2.3. Who made them: you, or
  CloudFormation? Look at `userIdentity` and `invokedBy` in the event.

- Find the `RunInstances` call for your Lesson 8.1 instance.

##### Question: What Event History Misses

_What doesn't event history record? Look for data events (such as S3 object
reads), how long events are kept, and whether you can query across
accounts. What does a trail add?_

#### Lab 8.3.2: A Trail to CloudWatch Logs

Before you start:

- Check for existing trails with `aws cloudtrail describe-trails
  --include-shadow-trails`. If you turned on Control Tower or created an
  organization trail in module 19, one may already cover your lab account.

- If your lab account is under the baseline SCP from Lab 19.2.3, you can
  create a trail but not change or delete it. Use the exception you
  designed in that module's "Your own cleanup" question (for example, a
  CloudFormation service role exempted with `aws:PrincipalARN`, passed with
  `--role-arn`) for this stack.

Create a new stack that provides:

- An S3 bucket for the trail, with a
  [bucket policy](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/create-s3-bucket-policy-for-cloudtrail.html)
  that lets CloudTrail write to it, limited with `aws:SourceArn` to your
  trail, and a lifecycle rule that expires objects after a few days.

- A log group (`/stelligent-u/<you>/lab08/trail`, 7-day retention) and the
  [IAM role](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-required-policy-for-cloudwatch-logs.html)
  CloudTrail uses to write to it.

- A multi-Region
  [trail](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-cloudtrail-trail.html)
  that records management events, validates its log files, and sends them
  to the log group.

Make a change in the account (tag your instance, for example) and find the
event in the log group with `aws logs tail` and with a Logs Insights query.
How long did it take to arrive?

##### Question: A Second Copy

_If an organization trail already covers your account, what does your new
trail cost? Since December 2025, CloudTrail events can also reach
CloudWatch Logs without a trail, through a
[service-linked channel](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-service-linked-channels.html)
enabled from CloudWatch. What would you use in an organization with dozens
of accounts?_

#### Lab 8.3.3: Alarming on API Activity

Security teams watch for a short list of risky API calls. Add to your trail
stack:

- A metric filter on the trail log group that counts security group
  changes (`AuthorizeSecurityGroupIngress`, `AuthorizeSecurityGroupEgress`,
  `RevokeSecurityGroupIngress`, `RevokeSecurityGroupEgress`,
  `CreateSecurityGroup` and `DeleteSecurityGroup`), using a JSON filter
  pattern on `$.eventName`.

- An alarm on that metric that notifies your SNS topic.

Test it: add an ICMP rule from your own `/32` to your instance's security
group with the CLI, then remove it. How long did the email take?

#### Lab 8.3.4: EventBridge Rules

[EventBridge rules](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-rules.html)
match events on the default event bus and send them to targets. Add to your
trail stack (or a new one):

- A rule that matches `EC2 Instance State-change Notification` events for
  your instance, sending them to your SNS topic. Use an
  [input transformer](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-transform-target-input.html)
  so the email reads "Instance i-... is now stopped" instead of raw JSON.

- A rule that matches
  [AWS API Call via CloudTrail](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-service-event-cloudtrail.html)
  events for the same security group changes as Lab 8.3.3, sending them to
  the same topic.

- An
  [SNS topic policy](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-use-resource-based.html#eb-sns-permissions)
  that lets EventBridge publish to your topic, limited to your rules.

Write each event pattern from a real sample event (the EventBridge console
has samples for both), and check it with `aws events test-event-pattern`
before you deploy. Then stop and start your instance, and change the
security group again.

##### Question: Which Events Needed the Trail

_Which of your two rules would still work if you deleted the trail? Why?
Would a rule in the default `ENABLED` state match a `DescribeInstances`
call?_

##### Question: Two Paths to One Notification

_You now get two emails for each security group change: one from the
metric filter alarm and one from EventBridge. Compare the two paths for
delay, cost, what the email tells you, and what else each can trigger
(Lambda, a Systems Manager Automation runbook). Which would you keep?_

#### Lab 8.3.5: Clean Up

Tear down everything this module created:

- Delete the flow log stack if it's still there.

- Empty the trail's S3 bucket (including any object versions), then delete
  the trail stack. If the SCP from module 19 blocks `DeleteTrail`, use your
  exempt role.

- Delete the Lesson 8.1/8.2 stack. Unsubscribe any SNS subscription you
  created outside a stack.

- Delete the `cli` and `ia` log groups and any group the agent or a service
  created for you.

- Check that nothing is left:
  `aws logs describe-log-groups --log-group-name-prefix /stelligent-u/<you>`,
  `aws cloudwatch describe-alarms`, `aws cloudwatch list-dashboards`,
  `aws cloudwatch list-metrics --namespace StudentU/<you>` (metrics can't
  be deleted; they drop out of `list-metrics` two weeks after their last data
  point and are billed only while data arrives),
  `aws logs describe-query-definitions`, `aws events list-rules`,
  `aws cloudtrail describe-trails`, `aws ec2 describe-flow-logs` and
  `aws ec2 describe-instances`.

### Retrospective 8.3

#### Question: Events Worth Watching

_What types of events might be important to track in an AWS account? For
three of them, what automated action would you take, and which AWS
resources would carry it out? (Module 20 covers Systems Manager Automation
and module 26 covers AWS Config, GuardDuty and Security Hub, which cover
many of the classic cases for you.)_

#### Task: Beyond Logs and Metrics

Optional, and billed per run: add a
[CloudWatch Synthetics canary](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Synthetics_Canaries.html)
that checks a public URL of your choice every 15 minutes, and an alarm on
its success rate. What does a canary tell you that your logs can't? Delete
the canary, its Lambda function, its S3 artifacts and its alarm when you
are done.

## Further Reading

- [CloudWatch cross-account observability](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Unified-Cross-Account.html)
  lets one monitoring account see the logs, metrics and traces of many
  accounts, which matters once you have the multi-account setup from
  module 19.

- [CloudWatch anomaly detection](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Anomaly_Detection.html)
  alarms on a band learned from a metric's history instead of a fixed
  threshold, and
  [log anomaly detection](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/LogsAnomalyDetection.html)
  does something similar for log patterns.

- [Encrypt log data with AWS KMS](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/encrypt-log-data-kms.html)
  and
  [mask sensitive log data](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/mask-sensitive-log-data.html)
  before logs become a place secrets leak to. Module 10 covers KMS keys.

- [Protecting log groups from deletion](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/protecting-log-groups-from-deletion.html)
  and CloudTrail
  [log file integrity validation](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-log-file-validation-intro.html)
  are what make logs trustworthy as audit evidence.

- The
  [AWS Observability Best Practices](https://aws-observability.github.io/observability-best-practices/)
  guide, maintained by AWS, covers what to measure and how to alarm on it.
