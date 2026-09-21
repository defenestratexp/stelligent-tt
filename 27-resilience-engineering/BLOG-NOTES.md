# Blog notes: Topic 27, Resilience Engineering

## Working title

Break it on purpose, with a stop condition: deployment strategies, AWS
FIS, Resilience Hub and zonal shift on one small workload

## Hook

The 2022 version of this course taught rolling updates in one module and
Lambda canaries in another, and never once broke anything on purpose.
In 2026 AWS makes the whole loop cheap enough to practise in a lab
account: weighted target groups for blue/green and canary without
CodeDeploy, ECS doing its own blue/green, canary and linear deployments
since 2025, Fault Injection Service experiments that cost ten cents an
action-minute and stop themselves when a CloudWatch alarm fires, a
Resilience Hub that grades a CloudFormation stack against your RTO and
RPO, and ARC zonal shift, which moves traffic out of an Availability Zone
with one free API call. The post takes one load balancer and two
instances through all of it, then runs a game day against it and writes
the post-incident review.

## Key points

1. **One table for every deployment strategy.** In-place, rolling,
   blue/green, canary and linear, mapped onto EC2 Auto Scaling, ECS,
   Lambda and Elastic Beanstalk, with what triggers rollback on each.
   Measure a rolling update from the user's side with a curl loop, then
   do blue/green and a 10% canary with ALB weighted target groups.
2. **Steady state first, experiment second.** Define "working" as ALB
   5XX counts and healthy host count, turn them into alarms, and make the
   error alarm the stop condition. The starter FIS template won't deploy
   without one.
3. **Three experiments, growing blast radius.** CPU stress on one
   instance through the `AWSFIS-Run-CPU-Stress` SSM document; stopping
   every instance in one AZ while injecting insufficient-capacity errors
   into the Auto Scaling group for that AZ; and the AZ Power Interruption
   scenario, read and trimmed on paper. Preview targets with
   `actionsMode=skip-all` before every real run.
4. **Resilience Hub is an estimate, not a test.** Build a resiliency
   policy from module 23's RTO/RPO, import the stack, assess, compare its
   recommended alarms and FIS tests with the ones you wrote, then delete
   the app the same day. Mention the May 2026 next generation (systems,
   services, GenAI failure mode assessments) and its pricing.
5. **Zonal shift beats waiting.** Compare the stopped-instance experiment
   with a zonal shift on the ALB: DNS drops the zone's address, targets
   show `AdministrativeOverride`, and nothing depends on health checks or
   new EC2 launches. Then autoshift with a practice run and an outcome
   alarm.
6. **Runbook, game day, COE.** A one-page AZ-impairment runbook, a game
   day where the mentor picks the fault, a timeline split into detect /
   diagnose / mitigate, and a blameless review with owned action items.

## Gotchas readers will hit

- ALB 5XX metrics have no data points when nothing fails; an alarm
  without `TreatMissingData: notBreaching` sits in `INSUFFICIENT_DATA`.
- FIS action `duration` and the SSM document's `DurationSeconds` are
  separate; get them the wrong way round and FIS reports "completed"
  while `stress-ng` is still running.
- `aws:ec2:stop-instances` with `startInstancesAfterDuration` fails when
  Auto Scaling has already replaced (terminated) the stopped instance,
  unless `completeIfInstancesTerminated` is set.
- `ssm:SendCommand` is authorized against both the document and each
  instance; a least-privilege FIS role needs a statement for each.
- The AZ Power Interruption scenario ships with an empty stop condition
  and 30-minute actions. Actions that target by ARN (the IAM role for
  paused launches) can't be skipped when their targets are empty.
- The Resilience Hub managed policy really is spelled
  `AWSResilienceHubAsssessmentExecutionPolicy` (three s's). Billing starts
  at the first assessment, not at `create-app`.
- Zonal shift takes Availability Zone IDs (`use2-az1`), not names, and
  existing keep-alive connections keep reaching the shifted zone for a
  while.
- Autoshift can't be enabled without a practice run configuration, and
  practice runs then shift real traffic weekly until you disable it.
- Routing control costs $2.50 per cluster-hour whether or not you use it;
  ARC readiness checks closed to new customers on 2026-04-30.

## Exam objectives supported

- DOP-C02 Domain 1: SDLC Automation (Task 1.4: deployment strategies)
- DOP-C02 Domain 3: Resilient Cloud Solutions (Tasks 3.1 and 3.3)
- DOP-C02 Domain 5: Incident and Event Response (Task 5.3)
- SAP-C02 → C03 Domain 1 (Task 1.3) and Domain 2 (Tasks 2.1 and 2.2)
- SOA-C03 Domain 2 (Skills 2.2.1, 2.2.2) and Domain 3 (Skill 3.1.5);
  ARC is in scope for SOA-C03, FIS and Resilience Hub are not

## Material to capture while doing the labs

- `probe.log` counts for the rolling update, the all-at-once update and
  the 10% canary (versions, AZs, non-200s), as a small table.
- The CloudWatch graph of `CPUUtilization` and 5XX during the CPU
  stress experiment, and the experiment going to `stopped` after
  `set-alarm-state`.
- Scaling activities from the lose-one-AZ experiment showing the
  injected `InsufficientInstanceCapacity` and where the replacement
  launched.
- The Resilience Hub assessment summary (estimated RTO/RPO per
  disruption type against the policy), with account IDs redacted.
- `dig +short` before and during a zonal shift, and a
  `describe-target-health` excerpt with `AdministrativeOverride`.
- The game-day timeline and a one-paragraph excerpt from the COE.
- The final FIS bill in action-minutes.
