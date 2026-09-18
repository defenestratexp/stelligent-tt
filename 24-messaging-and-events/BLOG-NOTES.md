# Blog notes: Topic 24, Messaging and Events

## Working title

Queues, topics and buses: SQS, SNS and EventBridge for people who have
to pick one

Alternatives: "Every message arrives at least once: messaging on AWS in
2026"; "The poison message that billed me for a month (and the five
settings that stop it)".

## Hook

The 2022 course never taught a queue. SNS was where alarm emails came
from and EventBridge was "CloudWatch Events", a way to trigger a Lambda
function. Yet decoupling is a task statement of its own on the
Solutions Architect exam, and the Developer exam asks about event source
mappings, dead-letter queues, idempotency and filter policies by name.
A lot has also moved since 2022: SQS messages up to 1 MiB, fair queues
that turn a message group ID on a *standard* queue into a tenant ID, DLQ
redrive from the CLI, Lambda provisioned mode for SQS, EventBridge
delivering straight to queues in other accounts, event bus logging, and
the EventBridge docs calling scheduled rules "legacy" in favour of
Scheduler. This module builds one order pipeline through all of it.

## Key points

1. **At least once is the contract.** Receive doesn't delete; the
   visibility timeout decides when a message comes back. Every consumer,
   including a Lambda function behind a FIFO queue, must be idempotent.
   Show a message's `ApproximateReceiveCount` climbing.
2. **Poison messages need three settings, not one.** A redrive policy
   with a sensible `maxReceiveCount`, a DLQ retention longer than the
   source's (on standard queues the original enqueue time sticks), and an
   alarm on the DLQ's `ApproximateNumberOfMessagesVisible`, not on
   `NumberOfMessagesSent`.
3. **Partial batch responses are the Lambda setting that matters.**
   Without `ReportBatchItemFailures`, one bad message makes a whole batch
   of good ones retry. With it, return `batchItemFailures`, and for FIFO
   stop at the first failure. Maximum concurrency on the mapping, not
   reserved concurrency on the function, is how you throttle a queue
   consumer without dumping healthy messages into the DLQ.
4. **Fan out with a queue per subscriber.** SNS → SQS gives each consumer
   its own buffer and failure domain; filter policies (on attributes or,
   now, the body) keep unwanted messages away. FIFO topics can feed
   standard queues and archive for replay.
5. **EventBridge is routing by content, with a history.** Custom bus,
   patterns with numeric, prefix, `anything-but`, `exists` and `$or`;
   input transformers; per-target retry policy and DLQ; archive and
   replay to a single rule; schema discovery; bus logs to find out why a
   rule didn't fire.
6. **Pipes and Scheduler replace glue code.** An SQS → filter → Lambda
   enrichment → bus pipe with no consumer of your own; a time-zone-aware
   schedule with a universal target and `ActionAfterCompletion: DELETE`.

## Gotchas readers will hit

- **A Lambda function's own DLQ does nothing for SQS messages.** The DLQ
  goes on the source queue's redrive policy. Classic exam trap.
- **Lambda refuses the event source mapping** if the function timeout is
  longer than the queue's visibility timeout. AWS recommends at least six
  times the function timeout, plus the batching window.
- **Reserved concurrency plus SQS sends healthy messages to the DLQ.**
  Throttled invocations still count as receives. Use the mapping's
  maximum concurrency instead.
- **Filtered-out SQS messages are gone.** An event source mapping's
  filter consumes the messages it doesn't pass on, so two filtered
  mappings on one queue don't split it; confirm the exact behaviour in the
  lab and quote it.
- **`PutEvents` returns 200 when it failed.** Partial failures are in
  `FailedEntryCount`, and a typo in the bus name drops the event without
  any error at all.
- **EventBridge target DLQs must be standard queues**, and `start-message-move-task`
  only redrives DLQs whose source is an SQS queue, so SNS and EventBridge
  DLQs need your own replay tooling.
- **SNS is still 256 KiB** while SQS went to 1 MiB, so a fan-out is
  capped by the topic.
- **SNS can't deliver to a queue encrypted with the AWS managed key**
  `alias/aws/sqs`; it needs SSE-SQS or a customer managed key whose
  policy trusts SNS.
- **A FIFO topic with an archive policy can't be deleted** until you set
  the policy to `{}`, which also deletes the archive.
- **Archives keep events forever by default**, and replayed events are
  billed again. Replays go to every rule on the bus unless you pass
  `FilterArns`.
- **Completed one-time schedules stay in the account** unless you set
  `ActionAfterCompletion: DELETE`, and on recurring schedules that needs
  an end date.
- **Lambda's recursive loop detection doesn't cover EventBridge.** A rule
  that triggers a function that publishes a matching event loops until
  you notice the bill.
- **An idle event source mapping keeps polling.** Disable it between
  sessions or it eats into the free million SQS requests.
  <!-- VERIFY: the actual idle request rate before quoting a number. -->

## Exam objectives supported

- DVA-C02 → C03 Domain 1 (Task 1.1: event-driven and fanout patterns,
  idempotency, DLQs, messaging code; Task 1.2: event source mapping and
  error handling) and Domain 4 (Task 4.3: concurrency, messaging,
  subscription filter policies)
- SAA-C03 Domain 2 (Task 2.1: scalable and loosely coupled architectures)
  and Domain 3 (Task 3.2: decoupling workloads)
- SOA-C03 Domain 1 (Skills 1.1.5 and 1.2.2: SNS notifications, EventBridge
  routing and troubleshooting) and Domain 3 (Skill 3.2.2: event-driven
  automation)

## Material to capture while doing the labs

- The receive-count trace of a poison message through
  `maxReceiveCount` into the DLQ, and the redrive back.
- Number of times good messages were reprocessed before and after
  partial batch responses (same input, same seed for `send_orders.py`).
- `ConcurrentExecutions` and `ApproximateAgeOfOldestMessage` graphs for
  maximum concurrency versus reserved concurrency, and the DLQ count for
  each.
- FIFO: maximum concurrency with 3 groups versus 12.
- The six-pattern table from Lab 24.4.2 against the four sample events.
- A failed EventBridge delivery seen three ways: `FailedInvocations`, the
  DLQ message's `ERROR_CODE`, and the bus log line.
- A diagram of the final pipeline: partner queue → pipe (filter,
  enrichment) → bus → rules → queues and Lambda, with the SNS fan-out
  beside it and the scheduler on top.
- Cost Explorer for the module, grouped by service, with account IDs
  redacted.
