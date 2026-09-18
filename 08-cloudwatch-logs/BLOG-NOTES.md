# Blog Notes: Module 08, Observability

## Working title

Where did `/var/log/messages` go? CloudWatch Logs, metric filters and
EventBridge on Amazon Linux 2023

## Hook

The classic "ship your logs to CloudWatch" tutorial installs an agent,
points it at `/var/log/messages`, and follows the stream with a third-party
Python tool. On Amazon Linux 2023 that file doesn't exist: the system logs
to the systemd journal, and `rsyslog` isn't installed. Meanwhile the AWS CLI
tails logs by itself, the CloudWatch agent reads the journal directly, and
"CloudWatch Events" has been EventBridge for years. This post rebuilds the
2022 lab on AL2023, then goes the rest of the way from log lines to an
alarm in your inbox, and shows which change notifications need a CloudTrail
trail and which don't.

## Key points

1. **AL2023 logs to the journal.** No `/var/log/messages`. The agent's
   `journald` section (units, priority, field matches) replaces tailing a
   syslog file; application logs still come from files. Create the log
   groups yourself, with a retention, instead of letting the agent create
   groups that never expire.
1. **The agent config lives in Parameter Store**, and the managed policy
   only allows parameters named `AmazonCloudWatch-*`. Updating the
   parameter changes nothing until something runs `fetch-config` again
   (`AmazonCloudWatch-ManageAgent` with Run Command at fleet scale).
1. **Reading logs without extra tools:** `aws logs tail --since 5m --follow
   --filter-pattern '{ $.level = "ERROR" }'` versus Live Tail (per-minute
   billing after the free allowance, 3-hour sessions) versus Logs Insights
   (billed per GB scanned). Which one for which job.
1. **From logs to alarms:** a metric filter (default value 0, no backfill,
   dimensions multiply metrics and cost), an alarm with M-of-N datapoints
   and a deliberate missing-data choice, a composite alarm so you page on
   symptoms, SNS for the email. Log classes decide what's possible:
   Infrequent Access has no metric filters, Live Tail or subscription
   filters, and a group's class can't be changed.
1. **Two ways to hear about a change.** EC2 state changes reach EventBridge
   without any setup; "AWS API Call via CloudTrail" events need a trail,
   and read-only calls need a special rule state. Compare an EventBridge
   rule with a metric filter on the trail's log group: delay, cost, and
   what each can trigger.

## Gotchas readers will hit

- Copy-pasted agent configs that read `/var/log/messages` start cleanly and
  send nothing on AL2023.
- The agent can't read its configuration from a parameter with any other
  name prefix: `CloudWatchAgentServerPolicy` scopes `ssm:GetParameter` to
  `AmazonCloudWatch-*`.
- Setting `retention_in_days` in the agent config on an existing group
  deletes older events, and two different values for the same group stop
  the agent with an error.
- `aws logs tail` and `get-log-events` don't work on Infrequent Access
  groups; only Logs Insights does.
- Metric filters only count events that arrive after they exist; a fresh
  alarm sits in `INSUFFICIENT_DATA` until data flows.
- A metric filter with dimensions can't have a default value, so the graph
  has gaps during quiet periods.
- The EventBridge rule is created but no email arrives: the SNS topic
  policy doesn't allow `events.amazonaws.com`.
- An SCP that protects CloudTrail (module 19) lets you create a lab trail
  but not delete it. Plan the exempt role before you create the trail.
- A second trail in an account already covered by an organization trail is
  a paid copy of management events.

<!-- VERIFY: while doing Lab 8.1.2, confirm the AL2023 amazon-cloudwatch-agent package version supports the journald section, and capture what the agent log says when the parameter name lacks the AmazonCloudWatch- prefix. -->

## Exam objectives

- SOA-C03 Domain 1: Monitoring, Logging, Analysis, Remediation, and
  Performance Optimization (Task 1.1, Skills 1.1.1 to 1.1.5; Task 1.2,
  Skill 1.2.2 EventBridge)
- DOP-C02 Domain 4: Monitoring and Logging (4.1, 4.2, 4.3) and Domain 5:
  Incident and Event Response (5.1)
- SCS-C03 Domain 1: Detection (Task 1.1 monitoring and alerting; Task 1.2
  logging solutions)
