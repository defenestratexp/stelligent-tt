# Topic 24: Messaging and Events

<!-- TOC -->

- [Topic 24: Messaging and Events](#topic-24-messaging-and-events)
  - [What changed in the 2026 edition](#what-changed-in-the-2026-edition)
  - [Exam coverage](#exam-coverage)
  - [Cost and cleanup](#cost-and-cleanup)
  - [Guidance](#guidance)
  - [Conventions](#conventions)
  - [Lesson 24.1: Queues with Amazon SQS](#lesson-241-queues-with-amazon-sqs)
    - [Principle 24.1](#principle-241)
    - [Practice 24.1](#practice-241)
      - [Lab 24.1.1: A standard queue, by hand](#lab-2411-a-standard-queue-by-hand)
      - [Lab 24.1.2: Long polling](#lab-2412-long-polling)
      - [Lab 24.1.3: A dead-letter queue and redrive](#lab-2413-a-dead-letter-queue-and-redrive)
      - [Lab 24.1.4: FIFO queues and message groups](#lab-2414-fifo-queues-and-message-groups)
      - [Lab 24.1.5: A consumer in Python](#lab-2415-a-consumer-in-python)
    - [Retrospective 24.1](#retrospective-241)
  - [Lesson 24.2: Lambda as a queue consumer](#lesson-242-lambda-as-a-queue-consumer)
    - [Principle 24.2](#principle-242)
    - [Practice 24.2](#practice-242)
      - [Lab 24.2.1: An event source mapping](#lab-2421-an-event-source-mapping)
      - [Lab 24.2.2: Partial batch responses](#lab-2422-partial-batch-responses)
      - [Lab 24.2.3: Concurrency and filtering](#lab-2423-concurrency-and-filtering)
      - [Lab 24.2.4: Lambda and a FIFO queue](#lab-2424-lambda-and-a-fifo-queue)
    - [Retrospective 24.2](#retrospective-242)
  - [Lesson 24.3: Publish and subscribe with Amazon SNS](#lesson-243-publish-and-subscribe-with-amazon-sns)
    - [Principle 24.3](#principle-243)
    - [Practice 24.3](#practice-243)
      - [Lab 24.3.1: Fan out to queues](#lab-2431-fan-out-to-queues)
      - [Lab 24.3.2: Subscription filter policies](#lab-2432-subscription-filter-policies)
      - [Lab 24.3.3: When delivery fails](#lab-2433-when-delivery-fails)
      - [Lab 24.3.4: A FIFO topic](#lab-2434-a-fifo-topic)
    - [Retrospective 24.3](#retrospective-243)
  - [Lesson 24.4: EventBridge event buses in depth](#lesson-244-eventbridge-event-buses-in-depth)
    - [Principle 24.4](#principle-244)
    - [Practice 24.4](#practice-244)
      - [Lab 24.4.1: A custom bus and your own events](#lab-2441-a-custom-bus-and-your-own-events)
      - [Lab 24.4.2: Event patterns](#lab-2442-event-patterns)
      - [Lab 24.4.3: Targets, transformers, retries and logs](#lab-2443-targets-transformers-retries-and-logs)
      - [Lab 24.4.4: Archive and replay](#lab-2444-archive-and-replay)
      - [Lab 24.4.5: Schemas](#lab-2445-schemas)
    - [Retrospective 24.4](#retrospective-244)
  - [Lesson 24.5: Pipes, Scheduler and choosing](#lesson-245-pipes-scheduler-and-choosing)
    - [Principle 24.5](#principle-245)
    - [Practice 24.5](#practice-245)
      - [Lab 24.5.1: A pipe from a queue to a bus](#lab-2451-a-pipe-from-a-queue-to-a-bus)
      - [Lab 24.5.2: EventBridge Scheduler](#lab-2452-eventbridge-scheduler)
      - [Lab 24.5.3: Pick the service](#lab-2453-pick-the-service)
      - [Lab 24.5.4: Clean up the module](#lab-2454-clean-up-the-module)
    - [Retrospective 24.5](#retrospective-245)
  - [Further Reading](#further-reading)

<!-- /TOC -->

## What changed in the 2026 edition

- **New module.** The 2022 course used SNS only as a place to send alarm
  emails and met EventBridge (then "CloudWatch Events") as a Lambda
  trigger. It never taught queues. Decoupling with SQS, SNS and
  EventBridge is its own task statement on the Solutions Architect exam,
  and the Developer exam asks about event source mappings, dead-letter
  queues, idempotency and subscription filter policies by name.
- It goes deeper than [module 08](../08-cloudwatch-logs/README.md), which
  wrote EventBridge rules on the default bus for AWS service events. Here
  you publish your own events to a **custom bus**, and use the parts of
  EventBridge module 08 left out: advanced patterns, retry policies and
  target dead-letter queues, archive and replay, the schema registry,
  **Pipes**, **Scheduler** and event bus logging.
- It covers features that did not exist in 2022 or have changed since:
  - SQS messages up to **1 MiB** (was 256 KiB). SNS is still 256 KiB, so
    a fan-out is limited by the topic, not the queue.
  - **SQS fair queues** (July 2025): a message group ID on a *standard*
    queue now means "tenant", and SQS keeps one noisy tenant from
    delaying everyone else.
  - DLQ **redrive from the API and CLI** (`start-message-move-task`), for
    FIFO queues too.
  - Lambda **provisioned mode** for SQS event source mappings, and the
    maximum concurrency setting.
  - SNS **FIFO topics** with message archiving and replay (2023), which
    can also deliver to standard queues.
    <!-- VERIFY: when SNS FIFO topics gained standard SQS queues as
    subscribers (before or after October 2022). -->
  - EventBridge **direct cross-account targets** (January 2025), **1 MB**
    `PutEvents` requests, event bus **logging** to CloudWatch Logs, S3 or
    Firehose, and a note in the docs that **scheduled rules are legacy**:
    new schedules belong in EventBridge Scheduler.
- New queues are encrypted at rest with SQS-managed keys (SSE-SQS) by
  default. The labs keep that default and show where a KMS key would
  change things.

## Exam coverage

| Exam | Domain / task statement |
|---|---|
| DVA-C02 → C03 | Domain 1: Development with AWS Services (Task 1.1: event-driven and fanout patterns, idempotency, loose coupling, retries with backoff and dead-letter queues, writing code that uses messaging services). C03 guide publishes 2026-10-27 and adds GenAI / agent topics |
| DVA-C02 → C03 | Domain 1: Development with AWS Services (Task 1.2: event source mapping, event-driven architecture, handling the event lifecycle and errors with dead-letter queues) |
| DVA-C02 → C03 | Domain 4: Troubleshooting and Optimization (Task 4.3: concurrency, messaging services, subscription filter policies) |
| SAA-C03 | Domain 2: Design Resilient Architectures (Task 2.1: scalable and loosely coupled architectures: event-driven architectures, queuing and publish/subscribe, the services that achieve loose coupling) |
| SAA-C03 | Domain 3: Design High-Performing Architectures (Task 3.2: decoupling workloads so components scale independently) |
| SOA-C03 | Domain 1: Monitoring, Logging, Analysis, Remediation, and Performance Optimization (Skill 1.1.5: notifications through SNS; Skill 1.2.2: use EventBridge to route, enrich and deliver events, and troubleshoot event bus rules) |
| SOA-C03 | Domain 3: Deployment, Provisioning, and Automation (Skill 3.2.2: event-driven automation with Lambda and EventBridge) |

## Cost and cleanup

Nothing in this module bills by the hour. Every service here charges per
request or per event, and the labs send a few thousand at most, so the
whole module should cost cents. The risk is not a forgotten instance but
a forgotten **loop or schedule**: a recurring schedule, a retry storm or
a function that feeds its own trigger can run all month. Prices below are
for `us-east-2`, read from the pricing pages in September 2026.

- **SQS:** the first **1 million requests a month are free** (all Regions
  combined). After that, $0.40 per million for standard queues and $0.50
  per million for FIFO. Each 64 KB chunk of a payload counts as one
  request, so one 1 MiB message is 16 requests. Empty receives count too,
  which is one reason for Lab 24.1.2. Fair queues add $0.10 per million
  requests on top of the standard rate when you set a message group ID on
  a standard queue.
- **Lambda event source mappings poll even when the queue is empty.** An
  enabled mapping on an idle queue keeps making long-poll requests, which
  come out of your free million. Disable mappings between sittings.
  <!-- VERIFY: how many ReceiveMessage calls an idle SQS event source
  mapping makes per hour in the default (on-demand) mode. -->
  Provisioned mode bills for event pollers on top; the module covers it
  on paper only.
- **SNS:** the first 1 million requests a month are free, then $0.50 per
  million. Deliveries to SQS and Lambda have no per-message charge. Email
  is free for the first 1,000 notifications a month. FIFO topics are
  priced per message and per GB of payload, and a FIFO archive is billed
  by storage with a one-day minimum.
- **Lambda:** the always-free allowance (1 million requests and 400,000
  GB-seconds a month) covers every function in this module.
- **EventBridge:** AWS service events on the default bus are free. Custom
  events you publish are $1.00 per million. **Archives** cost $0.10 per GB
  written plus $0.023 per GB-month stored, and replayed events are billed
  again as custom events; an archive keeps events **indefinitely** unless
  you set a retention period. **Schema discovery** is free for the first
  5 million events a month, then $1.00 per million; the registry itself is
  free. **Pipes** cost $0.40 per million requests, counted after
  filtering. **Scheduler** includes 14 million invocations a month free,
  then $1.00 per million. Event bus **logging** has no EventBridge charge;
  you pay for CloudWatch Logs ingestion and storage.
- **CloudWatch Logs:** function logs and the bus log group are set to
  7-day retention. At lab volume they cost nothing worth measuring.
- **KMS:** none. The queues use SSE-SQS, which has no key charge. Lab
  24.3.3 discusses customer managed keys on paper.
- **Cleanup:** [Lab 24.5.4](#lab-2454-clean-up-the-module) deletes every
  stack, archive, discoverer, schedule and schedule group the module
  created, and checks for the things CloudFormation doesn't own: event
  source mappings created by hand, SNS subscriptions made with the CLI,
  and messages waiting in queues.

<!-- VERIFY: EventBridge, Pipes and Scheduler prices above come from the
public pricing page summary; confirm the us-east-2 figures when you run
the labs. -->

## Guidance

- Explore the official docs! See the
  [Amazon SQS Developer Guide](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html),
  [Amazon SNS Developer Guide](https://docs.aws.amazon.com/sns/latest/dg/welcome.html),
  [Amazon EventBridge User Guide](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html),
  [EventBridge Scheduler User Guide](https://docs.aws.amazon.com/scheduler/latest/UserGuide/what-is-scheduler.html)
  and [Using Lambda with Amazon SQS](https://docs.aws.amazon.com/lambda/latest/dg/with-sqs.html),
  the CLI references for
  [sqs](https://docs.aws.amazon.com/cli/latest/reference/sqs/),
  [sns](https://docs.aws.amazon.com/cli/latest/reference/sns/),
  [events](https://docs.aws.amazon.com/cli/latest/reference/events/),
  [pipes](https://docs.aws.amazon.com/cli/latest/reference/pipes/),
  [scheduler](https://docs.aws.amazon.com/cli/latest/reference/scheduler/)
  and [schemas](https://docs.aws.amazon.com/cli/latest/reference/schemas/),
  and the [boto3 SQS](https://docs.aws.amazon.com/boto3/latest/reference/services/sqs.html)
  and [boto3 EventBridge](https://docs.aws.amazon.com/boto3/latest/reference/services/events.html)
  references.

- Read the decision guide [Amazon SQS, Amazon SNS, or Amazon
  EventBridge?](https://docs.aws.amazon.com/decision-guides/latest/decision-guides/sns-or-sqs-or-eventbridge.html)
  before you start and again at the end. Lab 24.5.3 asks you to argue
  with it.

- Avoid using other sites like stackoverflow.com for answers \-- part
  of the skill set you're building is finding answers straight from
  the source, AWS.

- Explore your curiosity. Try to understand why things work the way
  they do. Read more of the documentation than just what you need to
  find the answers.

## Conventions

- **Profile and Region.** Everything runs in the lab account with the
  `lab` profile from module 19, in `us-east-2`. Export
  `AWS_PROFILE=lab` for the Python scripts. CLI examples don't pass
  `--region`.
- **Names.** Every resource and stack name starts with your identifier,
  shown here as `<you>`: `<you>-orders`, `<you>-orders-dlq`,
  `<you>-orders.fifo`, `<you>-order-consumer`. Your EventBridge event
  `source` is `<you>.orders`. Tag everything with `owner=<you>` and
  `topic=24`.
- **Placeholders.** Examples use `123456789012` for the account ID. Write
  `<lab-account-id>` in your answers and keep real account IDs, queue URLs
  and email addresses out of your repository.
- **Starter files.** [starter/send_orders.py](starter/send_orders.py) is a
  load generator that sends fake orders to a queue, a topic or a bus; it
  is not a lab answer. [starter/consumer.yaml](starter/consumer.yaml) and
  [starter/consumer/handler.py](starter/consumer/handler.py) are the
  Lambda consumer for Lesson 24.2, with the interesting parts left as
  `TODO(student)`. [starter/events/](starter/events/) holds sample events
  for Lab 24.4.2. Everything else you write: templates in YAML, code in
  Python 3.13 with boto3.
- **Templates live next to your answers.** Keep `queues.yaml`,
  `fanout.yaml`, `bus.yaml` and `pipes-and-schedules.yaml` in your copy of
  this directory. Each must pass `cfn-lint`.
- DO use the AWS CLI and CloudFormation rather than the console. The
  EventBridge console's sandbox and sample events are fine for *testing*
  a pattern; the rule itself goes in a template.

## Lesson 24.1: Queues with Amazon SQS

### Principle 24.1

*A queue lets the sender and the receiver fail, scale and deploy
independently. The price is that every message will be delivered at
least once, and your consumer has to cope with that.*

### Practice 24.1

SQS stores messages until a consumer receives and **deletes** them.
Receiving a message doesn't remove it; it hides it for the **visibility
timeout**. If the consumer doesn't delete it in time, it reappears and
someone receives it again. After a set number of receives, a **redrive
policy** moves it to a **dead-letter queue** (DLQ). **Standard** queues
offer nearly unlimited throughput with best-effort ordering and
at-least-once delivery. **FIFO** queues keep order within a **message
group** and drop duplicates inside a five-minute window, at a lower
throughput.

Read [How Amazon SQS
works](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-how-it-works.html)
and the [message
quotas](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/quotas-messages.html)
before you start.

#### Lab 24.1.1: A standard queue, by hand

Write `queues.yaml` with one standard queue, `<you>-orders`, using
[AWS::SQS::Queue](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-sqs-queue.html).
Leave every attribute at its default for now, except tags. Deploy it,
then use only the CLI:

- `aws sqs get-queue-attributes --attribute-names All`. Write down the
  visibility timeout, retention period, maximum message size, receive
  wait time and whether SSE is on.
- Send three messages with `aws sqs send-message`.
- Receive one with `aws sqs receive-message`. Immediately run
  `get-queue-attributes` again and compare
  `ApproximateNumberOfMessages` with
  `ApproximateNumberOfMessagesNotVisible`.
- Don't delete it. Wait out the visibility timeout and receive again.
  Compare the `ReceiptHandle` and the `ApproximateReceiveCount`
  attribute (ask for it with `--attribute-names All`).
- Delete it with the *new* receipt handle. Then try to delete with the
  old one. What happens?
- Receive a message and call `change-message-visibility` with a timeout
  of 0. What is that useful for?

##### Question: Who owns a message

_After `receive-message` returns, the message is still in the queue. What
is the consumer's job from that moment, and what happens if it crashes
halfway through? Why is the receipt handle, not the message ID, what you
pass to `delete-message`?_

##### Question: Choosing a visibility timeout

_Your consumer usually takes 2 seconds per message and occasionally 90.
What goes wrong with a 30-second visibility timeout? With a 12-hour one?
How would a consumer that sometimes needs longer extend the timeout for
one message instead of for the whole queue?_

#### Lab 24.1.2: Long polling

With short polling (the default `ReceiveMessageWaitTimeSeconds` of 0),
SQS queries a subset of its servers and returns at once, often with
nothing.

- Purge the queue (`aws sqs purge-queue`; it can take up to a minute).
  Run `receive-message` ten times in a loop on the empty queue and time
  it.
- Run the same loop with `--wait-time-seconds 20`, and send one message
  from a second terminal while it's waiting. When does the receive
  return?
- Set `ReceiveMessageWaitTimeSeconds: 20` on the queue in `queues.yaml`
  and update the stack.

Read [Amazon SQS short and long
polling](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-short-and-long-polling.html).

##### Question: Paying for nothing

_A consumer short-polls an empty queue in a tight loop, one request a
second, all month. How many requests is that, and what does it cost after
the free tier? What does long polling change? Can short polling return
"no messages" when the queue has some?_

#### Lab 24.1.3: A dead-letter queue and redrive

A message that can never be processed (a *poison message*) is received,
fails, reappears and is received again, forever, unless something moves
it aside.

- Add `<you>-orders-dlq` to `queues.yaml`. Give it the maximum retention
  period, and give the main queue a `RedrivePolicy` pointing at it with a
  `maxReceiveCount` of 3. On the DLQ, add a `RedriveAllowPolicy` that
  allows only your main queue as a source.
- Read [Using dead-letter queues in Amazon
  SQS](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html),
  including the section on retention periods.
- Send one message. Receive it three times without deleting it
  (`change-message-visibility` to 0 speeds this up). Receive once more:
  where is it now?
- Add a CloudWatch alarm on the DLQ's `ApproximateNumberOfMessagesVisible`
  greater than 0, notifying the SNS topic you made in module 08 (or a new
  one). Read [Creating alarms for dead-letter
  queues](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/dead-letter-queues-alarms-cloudwatch.html)
  for why the obvious metric, `NumberOfMessagesSent`, is the wrong one.
- Move the message back with
  [`aws sqs start-message-move-task`](https://docs.aws.amazon.com/cli/latest/reference/sqs/start-message-move-task.html)
  and watch it with `list-message-move-tasks`. See [Configuring a
  dead-letter queue
  redrive](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-configure-dead-letter-queue-redrive.html).

##### Question: How many receives

_The Lambda docs recommend a `maxReceiveCount` of at least 5. Why not 1?
What does a very high value cost you while a poison message is stuck in
the main queue? For standard queues with a `maxReceiveCount` above 3, SQS
does something to messages received three or more times: what, and how
does it affect `ApproximateAgeOfOldestMessage`?_

##### Question: When the DLQ expires your message

_A message spends three days in the main queue and then moves to a DLQ
whose retention period is four days. On a standard queue, when is it
deleted? On a FIFO queue? What retention would you set on each, and
why?_

##### Question: Redrive isn't universal

_`start-message-move-task` accepts only DLQs whose sources are SQS
queues. You'll attach SQS queues as DLQs to an SNS subscription (Lesson
24.3) and an EventBridge target (Lesson 24.4). How would you replay the
messages that land in those?_

#### Lab 24.1.4: FIFO queues and message groups

- Add `<you>-orders.fifo` to `queues.yaml`, with content-based
  deduplication **off**, and a FIFO DLQ. (Why must a FIFO queue's DLQ be
  FIFO too?)
- Send the same body twice with `send-message`, the same
  `--message-group-id` and the same `--message-deduplication-id`, a few
  seconds apart. How many messages are in the queue? Send it again with a
  different deduplication ID. Then turn **content-based deduplication**
  on and send the same body twice with no deduplication ID.
- Send 12 orders with `starter/send_orders.py --groups 3`. Receive with
  `--max-number-of-messages 10` without deleting anything. Which groups
  did you get? Receive again before the visibility timeout expires: what
  comes back, and why?
- Read [Using the message group
  ID](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/using-messagegroupid-property.html)
  and [High throughput for FIFO
  queues](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/high-throughput-fifo.html).
  Find the two attributes that turn on high throughput mode and the
  default FIFO throughput in `us-east-2`, with and without it.

##### Question: Ordered by what

_A FIFO queue guarantees order within a message group, not across the
queue. For an online shop, what would you choose as the message group
ID, and what goes wrong if you use a single group ID for everything? If
you use the order ID?_

##### Question: Fair queues are not FIFO

_Since July 2025, a message group ID on a **standard** queue turns on
[fair
queues](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-fair-queues.html).
What does it mean there, and what does it not guarantee? Describe a
workload where you'd want a standard queue with fair queues rather than a
FIFO queue, and which CloudWatch metrics show you it's working. (Try it:
`send_orders.py --tenant` sends a customer ID as the group ID.)_

#### Lab 24.1.5: A consumer in Python

Write `consume.py`, a small long-running consumer in Python 3.13 with
boto3, for `<you>-orders`:

- Long-poll for up to 10 messages at a time.
- "Process" each message by printing its order ID, and treat any order
  with `"poison": true` as a failure (don't delete it).
- Delete successes in one `delete_message_batch` call per receive, and
  check the `Failed` list in the response.
- Keep a set of order IDs you've already processed and skip duplicates.
  (In real life this would be a DynamoDB conditional write, as in Lab
  22.4.4.)
- Stop cleanly on Ctrl-C.

Run it against 50 orders from `send_orders.py --poison-every 7`, then
check both queues.

Start from the
[boto3 SQS guide](https://docs.aws.amazon.com/boto3/latest/guide/sqs.html)
and the `receive_message` and `delete_message_batch` pages in the boto3
reference.

##### Question: Idempotency

_Your in-memory set of processed IDs disappears when the consumer
restarts, and two copies of the consumer don't share it. Where must the
record of "already processed" live for idempotency to survive both? What
would happen to a customer's card if your consumer charged payments and
wasn't idempotent?_

### Retrospective 24.1

#### Question: What the queue bought you

_Before SQS, the order service called the fulfilment service directly.
List three failures that used to break checkout and no longer do. Now list
two new problems the queue introduced. Which metric would you alarm on to
notice that the consumer has stopped?_

## Lesson 24.2: Lambda as a queue consumer

### Principle 24.2

*With an event source mapping, Lambda does the polling, batching and
deleting for you. Your code only decides which messages in a batch failed,
so decide carefully.*

### Practice 24.2

An [event source
mapping](https://docs.aws.amazon.com/lambda/latest/dg/invocation-eventsourcemapping.html)
is a Lambda-side poller: it long-polls the queue, hands your function a
batch, and deletes the batch when the function succeeds. If the function
fails, the whole batch returns to the queue after the visibility timeout,
unless you report **batch item failures**. The queue's redrive policy,
not the function, decides when a message gives up and goes to the DLQ.

Module 09 introduces Lambda itself; this lesson assumes you can deploy a
function from a template. Read [Using Lambda with Amazon
SQS](https://docs.aws.amazon.com/lambda/latest/dg/with-sqs.html) and its
subpages first.

#### Lab 24.2.1: An event source mapping

- Zip [starter/consumer/handler.py](starter/consumer/handler.py) and
  upload it to an S3 bucket named with your identifier.
- Complete the first TODO in
  [starter/consumer.yaml](starter/consumer.yaml): an
  [AWS::Lambda::EventSourceMapping](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-lambda-eventsourcemapping.html)
  from `<you>-orders` to the function, with a parameter that enables or
  disables it.
- Before you deploy, read [Creating and configuring an Amazon SQS event
  source
  mapping](https://docs.aws.amazon.com/lambda/latest/dg/services-sqs-configure.html)
  and change `<you>-orders`' visibility timeout in `queues.yaml` to what
  it recommends for a 20-second function timeout. Deploy both stacks.
- Send 30 orders with no poison. Use `aws logs tail --follow` on the
  function's log group. How many invocations, and what batch sizes?
- Set a batch size of 50 and a batching window of 10 seconds, send 30
  more and compare.
- Set `WorkSeconds` so a batch takes longer than the function timeout.
  What happens to the messages?

##### Question: Six times the timeout

_Why does Lambda want the visibility timeout at least six times the
function timeout, plus the batching window? What does Lambda do if you
try to create a mapping where the function timeout is longer than the
visibility timeout?_

##### Question: Where the DLQ goes

_A Lambda function has its own dead-letter queue setting and on-failure
destinations. Do they apply to messages from an SQS event source mapping?
Where must the DLQ be configured instead, and what's the exam-question
trap here?_

#### Lab 24.2.2: Partial batch responses

- Send 30 orders with `--poison-every 10` to the current handler. Watch
  the logs and the queue metrics for a few minutes. How many times was
  each *good* order in the same batch as a poison order processed?
- Read [Handling errors for an SQS event source in
  Lambda](https://docs.aws.amazon.com/lambda/latest/dg/services-sqs-errorhandling.html).
- Complete the handler's TODO: catch per-message failures and return a
  `batchItemFailures` list. Turn on `ReportBatchItemFailures` in the
  mapping. Redeploy and repeat the test.
- Check the result: the good orders are processed once, the poison orders
  end up in the DLQ after `maxReceiveCount` receives, and the function's
  `Errors` metric stays at zero.
- Break it on purpose: return a made-up `itemIdentifier`. What does
  Lambda do with the batch?

*Optional: rewrite the handler with the [Powertools for AWS Lambda
(Python) batch
processor](https://docs.aws.amazon.com/powertools/python/latest/utilities/batch/)
and compare the amount of code.*

##### Question: Reporting failures without failing

_With partial batch responses your function succeeds even when messages
fail. What does that do to the function's `Errors` metric and to Lambda's
back-off when failures happen? Which SQS metrics tell you the reporting
is broken?_

#### Lab 24.2.3: Concurrency and filtering

- Read [Configuring scaling behavior for SQS event source
  mappings](https://docs.aws.amazon.com/lambda/latest/dg/services-sqs-scaling.html).
- Add a `ScalingConfig` with `MaximumConcurrency: 2` to the mapping. Set
  `WorkSeconds` to 2 and send 200 orders. Watch the function's
  `ConcurrentExecutions` metric and the queue's
  `ApproximateAgeOfOldestMessage`.
- Now remove maximum concurrency and set the function's **reserved
  concurrency** to 2 instead. Send 200 more. Look for `Throttles` and for
  messages that reached the DLQ without ever failing.
- Add `FilterCriteria` so the function only receives orders from the
  `web` channel. Read [Using event filtering with an Amazon SQS event
  source](https://docs.aws.amazon.com/lambda/latest/dg/with-sqs-filtering.html)
  and [Control which events Lambda sends to your
  function](https://docs.aws.amazon.com/lambda/latest/dg/invocation-eventfiltering.html).
  Send 30 orders, then find out what happened to the orders that didn't
  match.

##### Question: Two ways to limit concurrency

_Reserved concurrency and maximum concurrency both cap the function at 2.
Why did one of them send healthy messages to the DLQ? When would you use
each? Where does provisioned mode (minimum and maximum event pollers) fit,
and why can't you combine it with maximum concurrency?_

##### Question: Filters that delete

_What happened to the `store` and `partner` orders? If two teams each put
a filtered mapping on the same queue, what goes wrong? What would you
build instead?_

#### Lab 24.2.4: Lambda and a FIFO queue

- Deploy a second copy of the consumer stack against `<you>-orders.fifo`,
  with partial batch responses on. (What does the handler have to do
  differently for FIFO? Reread the FIFO note in the error-handling docs,
  and change your handler if you need to.)
- Send 60 orders with `--groups 3`, then with `--groups 12`, with
  `WorkSeconds` at 1. Compare the maximum `ConcurrentExecutions`.
- Send 30 orders with `--groups 3 --poison-every 10`. Log the
  `sequence` field. Is order preserved within each group, and what
  happened to the messages behind a poison message in its group?

##### Question: Concurrency follows groups

_Why can't Lambda run more concurrent invocations on a FIFO queue than
there are active message groups? What would you change to process
faster without losing the ordering you actually need?_

### Retrospective 24.2

#### Question: Exactly once

_Event source mappings deliver at least once, even from a FIFO queue.
List every way in this lesson that one order was processed twice, and for
each, say which of these would have prevented a double effect: partial
batch responses, a longer visibility timeout, a FIFO queue, or an
idempotent handler. Read about the [Powertools idempotency
utility](https://docs.aws.amazon.com/powertools/python/latest/utilities/idempotency/)
and say where it stores its records._

## Lesson 24.3: Publish and subscribe with Amazon SNS

### Principle 24.3

*A topic lets a publisher tell many subscribers without knowing who they
are. Put a queue behind each subscriber, and each one gets its own
buffer, its own pace and its own failures.*

### Practice 24.3

SNS pushes each published message to every subscription: SQS queues,
Lambda functions, HTTP endpoints, email and more. A **filter policy** on
a subscription drops the messages that subscriber doesn't want, so the
publisher doesn't have to know. The classic pattern is **fan-out**: one
topic, one SQS queue per consuming service. In these labs a
`<you>-orders` topic feeds a `fulfilment` queue that wants every order
and an `audit` queue that wants only large ones.

Read [What is Amazon
SNS?](https://docs.aws.amazon.com/sns/latest/dg/welcome.html) and
[Fanout to Amazon SQS
queues](https://docs.aws.amazon.com/sns/latest/dg/sns-sqs-as-subscriber.html).

#### Lab 24.3.1: Fan out to queues

Write `fanout.yaml`:

- An SNS topic `<you>-orders`
  ([AWS::SNS::Topic](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-sns-topic.html)).
- Two standard queues, `<you>-fulfilment` and `<you>-audit`, each with a
  DLQ.
- A queue policy
  ([AWS::SQS::QueuePolicy](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-sqs-queuepolicy.html))
  that lets `sns.amazonaws.com` send to both queues, only from your topic
  (`aws:SourceArn`).
- A subscription per queue
  ([AWS::SNS::Subscription](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-sns-subscription.html)).
  Turn on **raw message delivery** for `fulfilment` only.

Publish 5 orders with `send_orders.py --topic-arn`. Receive one message
from each queue and compare the bodies.

##### Question: Raw or wrapped

_What does SNS add around your message when raw delivery is off? When is
that envelope useful, and what breaks in a consumer (for example the
handler from Lesson 24.2) if you switch raw delivery on or off under it?_

##### Question: Why a queue per subscriber

_You could subscribe the Lambda function straight to the topic. What do
you lose compared with topic → queue → function? Think about bursts,
retries, poison messages and a consumer that's down for a day._

#### Lab 24.3.2: Subscription filter policies

- Read [Amazon SNS message
  filtering](https://docs.aws.amazon.com/sns/latest/dg/sns-message-filtering.html),
  [filter policy
  scope](https://docs.aws.amazon.com/sns/latest/dg/sns-message-filtering-scope.html)
  and the pages on filter policy operators.
- Give the `audit` subscription a filter policy on **message attributes**
  (the default scope): only orders whose `total` attribute is at least
  250. `send_orders.py` sets `channel` and `total` as attributes.
- Publish 30 orders and count what arrives in each queue.
- Change the audit subscription to `FilterPolicyScope: MessageBody` and
  rewrite the policy to match orders from the `partner` channel with a
  `coupon` field present. Publish 30 more.

##### Question: Attributes or body

_What does filtering on the body require of the message? Why might you
still prefer attributes? Filter changes can take a while to take effect:
how would you test a new policy without losing or duplicating orders in
production?_

#### Lab 24.3.3: When delivery fails

- Read [Amazon SNS message delivery
  retries](https://docs.aws.amazon.com/sns/latest/dg/sns-message-delivery-retries.html)
  and [Amazon SNS dead-letter
  queues](https://docs.aws.amazon.com/sns/latest/dg/sns-dead-letter-queues.html).
- Add a subscription DLQ (a `RedrivePolicy` on the *subscription*) for
  the `audit` subscription. It needs its own queue policy.
- Break delivery on purpose: remove `sns.amazonaws.com` from the audit
  queue's policy and publish a large order. Where does it end up, how
  fast, and which SNS metric shows it?
- Restore the policy.

##### Question: Client-side and server-side errors

_SNS retries server-side errors to SQS and Lambda endpoints for a very
long time, but doesn't retry client-side errors at all. Which kind was
your broken queue policy? Name another client-side error you could cause
by accident._

##### Question: Encrypted queues

_Your queues use SSE-SQS. If you changed a subscribed queue to SSE-KMS
with the AWS managed key `alias/aws/sqs`, SNS could no longer deliver to
it. Why, and what do you need instead? Read [Configure KMS permissions for
AWS
services](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-key-management.html)._

#### Lab 24.3.4: A FIFO topic

- Read [Message ordering and deduplication strategies using Amazon SNS
  FIFO
  topics](https://docs.aws.amazon.com/sns/latest/dg/sns-fifo-topics.html)
  and [Amazon SNS message delivery for FIFO
  topics](https://docs.aws.amazon.com/sns/latest/dg/fifo-message-delivery.html).
- Add to `fanout.yaml` a FIFO topic `<you>-orders.fifo` with two
  subscribers: your `<you>-orders.fifo` queue from Lab 24.1.4 (disable its
  Lambda mapping first) and a new **standard** queue.
- Try to add an email subscription to it. What happens?
- Publish 12 orders with `--groups 3`. Compare the order of arrival in
  the two queues.
- Read [message archiving and
  replay](https://docs.aws.amazon.com/sns/latest/dg/message-archiving-and-replay-topic-owner.html)
  for FIFO topics. Set an `ArchivePolicy` of one day on the topic. Look up
  `BeginningArchiveTime` with `get-topic-attributes`. You'll remove the
  policy in cleanup, because a topic with an active archive policy can't
  be deleted.

##### Question: FIFO end to end

_A FIFO topic delivering to a standard queue gives up ordering at the
queue. Why would anyone do that? Using the SNS quotas page, what is a
FIFO topic's throughput per topic and per message group, and what does
`FifoThroughputScope` change?_

### Retrospective 24.3

#### Question: Topics versus polling

_An SNS topic pushes; an SQS queue waits to be pulled. A new team wants
"every order, eventually, even if we're down for two days". Another wants
"orders over $250, within a second, to a webhook". Design the
subscriptions for each, including what happens when they fail._

## Lesson 24.4: EventBridge event buses in depth

### Principle 24.4

*An event says what happened, not who should act on it. EventBridge
routes events by their content, so producers and consumers can change
without coordinating, as long as the event itself stays a stable
contract.*

### Practice 24.4

Module 08 wrote rules on the **default bus** for events AWS services emit.
This lesson publishes your own events to a **custom bus**, matches them
with content-based patterns, reshapes them for targets, makes delivery
failures visible, and keeps a replayable history. Every event has the
same envelope (`source`, `detail-type`, `time`, `account`, `region`,
`detail`), and the `detail` is your contract with every consumer you'll
never meet.

Read [Event buses in Amazon
EventBridge](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-event-bus.html)
and [Events in Amazon
EventBridge](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-events.html).

#### Lab 24.4.1: A custom bus and your own events

- Write `bus.yaml` with an event bus `<you>-orders`
  ([AWS::Events::EventBus](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-events-eventbus.html))
  and one catch-all rule that matches `source` `<you>.orders` and sends
  everything to a new standard queue, `<you>-bus-tap`, so you can see
  what arrives. The queue policy lets `events.amazonaws.com` send from
  that rule only.
- Publish 5 orders with
  `send_orders.py --bus-name <you>-orders --source <you>.orders` and
  receive them from the tap queue. Identify every envelope field.
- Read [Sending events with
  PutEvents](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-putevents.html).
  Publish to a bus name that doesn't exist. What does `PutEvents` return?
- Try `Source` values beginning with `aws.`. What happens?

##### Question: A 200 that failed

_`PutEvents` can return HTTP 200 with some entries failed, and a typo in
the bus name drops the event silently. What should every producer do
with the response, and how does `send_orders.py` handle it? What would
you alarm on to catch a producer publishing to the wrong bus?_

##### Question: Naming events

_You chose `source` and `detail-type` values for the order events. What
naming rules would you set for an organization with fifty teams
publishing to shared buses? What belongs in `detail`, what belongs in
`resources`, and what must never go in an event at all?_

#### Lab 24.4.2: Event patterns

EventBridge matches with more than exact values. Read [Creating event
patterns](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-event-patterns.html)
and [Comparison operators for use in event
patterns](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-create-pattern-operators.html).

Using the four sample events in [starter/events/](starter/events/)
(change `you.orders` to your source), write one pattern for each rule
below, and check each against all four events with
[`aws events test-event-pattern`](https://docs.aws.amazon.com/cli/latest/reference/events/test-event-pattern.html).
Record which events each pattern matches in a table in your answers.

1. `OrderPlaced` events with a total over 250 (numeric matching).
2. `OrderPlaced` events from any channel except `partner`.
3. Orders from customers whose ID starts with `vip-`.
4. Orders that have a `coupon` field, whatever its value.
5. Any order that is **either** over 250 **or** from a `vip-` customer
   (`$or`).
6. Any event from your source whose `detail-type` is anything other than
   `OrderPlaced`, written without listing the other types.

Then put patterns 1 and 5 in `bus.yaml` as rules, each sending to its
own queue, and confirm with `send_orders.py` that the counts match your
table's predictions.

##### Question: What a pattern can't do

_Event patterns match; they don't compute. Which of these can a pattern
express, and what would you use for the rest: "total over 250", "total
over 250 in euros after conversion", "the third order from this customer
today", "wildcard in the customer ID"? Why are wildcard rules limited
per bus?_

#### Lab 24.4.3: Targets, transformers, retries and logs

- Give the pattern-1 rule a second target: the `<you>-audit` queue from
  Lesson 24.3, with an [input
  transformer](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-transform-target-input.html)
  that sends a small JSON document: `orderId`, `total`, `customerId`,
  the rule name and the event's ingestion time (both predefined
  variables).
- Give that target a `RetryPolicy` with a maximum event age of 5 minutes
  and 3 attempts, and a `DeadLetterConfig` pointing at a new standard
  queue `<you>-bus-dlq`. Read [How EventBridge retries delivering
  events](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-rule-retry-policy.html)
  and [Using dead-letter queues to process undelivered
  events](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-rule-dlq.html).
  Can the DLQ be FIFO?
- Turn on [event bus
  logging](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-event-bus-logs.html)
  at the `ERROR` level to a CloudWatch Logs log group with 7-day
  retention. The level is the bus's `LogConfig` property; the
  destination is a CloudWatch Logs *log delivery*, which the page above
  explains. Decide whether to include event detail, knowing it puts order
  data in your logs.
- Break the audit target (remove `events.amazonaws.com` from the audit
  queue's policy for this rule) and publish large orders. Find the
  failure three ways: the rule's `FailedInvocations` metric, the message
  in `<you>-bus-dlq` with its `ERROR_CODE` attribute, and the bus log.
  How long did EventBridge retry before giving up?
- Switch the log level to `TRACE` for one publish, read what it records
  for a successful delivery, then set it back to `ERROR`.
- Restore the policy.

##### Question: Retried or not

_Your broken queue policy produced one `ERROR_CODE`. Which errors does
EventBridge send straight to the DLQ without retrying, and which does it
retry for up to 24 hours and 185 attempts by default? Why is the default
retry policy a bad fit for an event that's only useful for five minutes?_

##### Question: Who else can receive

_Since January 2025 a rule can deliver directly to an SQS queue, SNS
topic or Lambda function in **another account**, without an event bus
there. Read [Sending events to an AWS service in another
account](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-service-cross-account.html).
What does the other account have to grant, and what does the rule need?
When would you still send to a bus in the other account instead?_

#### Lab 24.4.4: Archive and replay

- Read [Archiving and replaying
  events](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-archive.html).
- Add an archive
  ([AWS::Events::Archive](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-events-archive.html))
  on `<you>-orders` with an event pattern that keeps only `OrderPlaced`
  events and a retention period of 1 day.
- Publish 20 orders. Wait at least 10 minutes.
- Add a new rule for a "late" consumer: a new queue that should have
  received every order since you started. Replay the archive to that rule
  only (`aws events start-replay` with `Destination.FilterArns`). Follow
  it with `describe-replay`.
- Look at the replayed events in the new queue. Which field marks them as
  replays? Did the replay also reach your other rules? Why not?
- Find the managed rule the archive created on your bus with
  `aws events list-rules --event-bus-name`. What is its pattern for?

##### Question: Replay is a feature for idempotent consumers

_A replay resends events in one-minute slices, not necessarily in the
original order, and existing consumers receive them again unless you
restrict the replay to specific rules. What must be true of a consumer
before you can safely replay to it? How would a consumer that must not
act twice use the `replay-name` field?_

#### Lab 24.4.5: Schemas

- Read [Amazon EventBridge
  schemas](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-schema.html)
  and [Inferring schemas from event bus
  events](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-schemas-infer.html).
- Start schema discovery on `<you>-orders` with
  `aws schemas create-discoverer`. Publish 20 orders with
  `send_orders.py` and, separately, one `OrderCancelled` event from
  [starter/events/order-cancelled.json](starter/events/order-cancelled.json)
  with `aws events put-events`.
- After a few minutes, list the discovered schemas
  (`aws schemas list-schemas --registry-name discovered-schemas`). How
  many versions of the `OrderPlaced` schema are there, and why? (Some
  orders have a `coupon`; some have `poison`.)
- Download Python code bindings for one schema, from the console or with
  `put-code-binding` / `get-code-binding-source`, and read what it
  generated.
- Browse the `aws.events` registry for the schema of one AWS event you
  used in module 08.
- **Delete the discoverer** when you're done.

##### Question: Schema as contract

_Discovery shows you what producers *send*; it doesn't stop them sending
something else. Where would you keep the authoritative schema for
`OrderPlaced`, and how would you stop a producer from shipping a breaking
change? Which changes to `detail` are backward-compatible for the
patterns you wrote in Lab 24.4.2?_

### Retrospective 24.4

#### Question: A bus or a topic

_SNS topics and EventBridge buses both fan out. Compare them for this
lesson's orders: throughput, latency, filtering power, number of targets
per rule or subscriptions per topic, cost per million, replay, schema
support, and delivery to other accounts. When would you put SNS behind
EventBridge, or EventBridge behind SNS?_

## Lesson 24.5: Pipes, Scheduler and choosing

### Principle 24.5

*Most glue code between services is polling, filtering, reshaping and
retrying. Pipes and Scheduler are that glue as configuration; the code
you still write should be the part that is actually yours.*

### Practice 24.5

**EventBridge Pipes** connects one source (SQS, Kinesis, DynamoDB
Streams, Amazon MQ, Amazon MSK or self-managed Kafka) to one target, with
optional filtering, enrichment and input transformation in between, and
charges only for events that pass the filter. **EventBridge Scheduler**
invokes a target on a one-time, rate or cron schedule in any time zone,
with retries, a DLQ and flexible windows, and can call thousands of AWS
API operations directly. The EventBridge docs now call **scheduled
rules** a legacy feature and recommend Scheduler instead.

Read [Amazon EventBridge
Pipes](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes.html)
and [What is Amazon EventBridge
Scheduler?](https://docs.aws.amazon.com/scheduler/latest/UserGuide/what-is-scheduler.html)

#### Lab 24.5.1: A pipe from a queue to a bus

Your partners can only write to an SQS queue. Turn their messages into
proper `OrderPlaced` events on your bus, without a consumer of your own.

Write `pipes-and-schedules.yaml` with:

- A standard queue `<you>-partner-inbox` with a DLQ.
- A small enrichment Lambda function in Python 3.13, written by you,
  that receives a batch of messages and returns, for each, the order plus
  a `tier` field (`vip` if the customer ID starts with `vip-`, else
  `standard`). Keep it short: it is the only code in this lab.
- A pipe
  ([AWS::Pipes::Pipe](https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-pipes-pipe.html))
  from the queue to your `<you>-orders` bus with:
  - a filter that drops messages whose body has `"poison": true`;
  - the enrichment function;
  - a target input template that makes each result the event's `detail`,
    with `detail-type` `OrderPlaced` and source `<you>.partner`;
  - an execution role that allows only what the pipe needs. Read [IAM
    role for EventBridge
    Pipes](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-permissions.html).
- Send 20 orders with `--poison-every 5` to the inbox. Watch them arrive
  on your catch-all tap queue from Lab 24.4.1 (widen its pattern to match
  both sources). Where did the poison orders go?

Read [Event filtering in EventBridge
Pipes](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-event-filtering.html),
[Event enrichment](https://docs.aws.amazon.com/eventbridge/latest/userguide/pipes-enrichment.html)
and [Input
transformation](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-pipes-input-transformation.html).

##### Question: Pipe or event source mapping

_A pipe from SQS and a Lambda event source mapping on SQS both poll a
queue. What does each let you target, and what does each cost? Which
event pattern operators work in a rule but not in a pipe filter? The
enrichment step could have been a Step Functions workflow: which workflow
type does Pipes accept, and why only that one?_

#### Lab 24.5.2: EventBridge Scheduler

- Read [Schedule types in EventBridge
  Scheduler](https://docs.aws.amazon.com/scheduler/latest/UserGuide/schedule-types.html)
  and [Deleting a
  schedule](https://docs.aws.amazon.com/scheduler/latest/UserGuide/managing-schedule-delete.html).
- Add to `pipes-and-schedules.yaml` a schedule group `<you>-orders` and
  an execution role for Scheduler.
- **One-time schedule:** send one test order to `<you>-partner-inbox`,
  15 minutes from now, using the templated SQS target, with
  `ActionAfterCompletion: DELETE`. Check that it arrived and that the
  schedule is gone.
- **Recurring schedule with a universal target:** every weekday at 09:00
  in `America/New_York`, write the current time to an SSM parameter
  `/<you>/orders/last-heartbeat` using the universal target
  `arn:aws:scheduler:::aws-sdk:ssm:putParameter`. Give it a 15-minute
  flexible time window, a retry policy with a maximum event age of one
  hour, and `<you>-bus-dlq` as its DLQ. Read [Using universal
  targets](https://docs.aws.amazon.com/scheduler/latest/UserGuide/managing-targets-universal.html).
  To test it without waiting, temporarily change it to `rate(5 minutes)`.
- Compare with a scheduled rule: write (don't deploy) the
  `AWS::Events::Rule` that would do the weekday job. What can't it do?

##### Question: Time zones and daylight saving

_Your 09:00 New York schedule: what happens on the day clocks go forward
and the day they go back? What would a cron schedule at 02:30 in
`America/Los_Angeles` do on those days? What does `rate(1 days)` do
across a daylight-saving change?_

##### Question: Schedules that pile up

_A one-time schedule without automatic deletion stays in your account
after it runs. Why does that matter to an application that creates a
reminder for every order? For a recurring schedule, what else must you
set before `ActionAfterCompletion: DELETE` has any effect?_

#### Lab 24.5.3: Pick the service

Read the decision guide [Amazon SQS, Amazon SNS, or Amazon
EventBridge?](https://docs.aws.amazon.com/decision-guides/latest/decision-guides/sns-or-sqs-or-eventbridge.html)
again. For each scenario, choose the service or combination (SQS
standard or FIFO, SNS standard or FIFO, EventBridge bus, Pipes,
Scheduler, or Step Functions from module 18) and justify it in two or
three sentences, naming the feature that decided it:

1. Thumbnail generation for uploaded images; bursts of 10,000 uploads,
   each thumbnail takes 30 seconds.
2. Bank account transactions that must be applied in order per account.
3. Tell five internal teams, most of them in other accounts, whenever an
   order ships. Some want only international orders.
4. Send a reminder email 24 hours after an abandoned cart, for millions
   of carts.
5. React within a minute when anyone in the organization disables
   CloudTrail logging.
6. A SaaS service with one shared work queue where one large customer
   often floods it.
7. Re-run last Tuesday's order events through a fixed version of the
   billing service.
8. A three-step order workflow with compensation if payment fails.

##### Question: The decision you can undo

_Which of your choices would be expensive to change a year from now, and
which cheap? What does that suggest about putting a queue in front of
every consumer?_

#### Lab 24.5.4: Clean up the module

Delete in reverse order, and check each step, in `us-east-2`:

- **Scheduler:** delete the recurring schedule and the schedule group
  (`aws scheduler delete-schedule-group` deletes the schedules in it).
  Confirm with `aws scheduler list-schedules` and
  `list-schedule-groups` (the `default` group stays). Delete the SSM
  parameter.
- **Pipes:** delete the `pipes-and-schedules` stack. Confirm with
  `aws pipes list-pipes`.
- **EventBridge:** delete the discoverer if Lab 24.4.5 left it
  (`aws schemas list-discoverers`), and any custom registry you made.
  Delete the archive and any replays you started (`list-archives`,
  `list-replays`), turn off bus logging, then delete the `bus` stack.
  Confirm `aws events list-event-buses` shows only `default`, and
  `list-rules` on the default bus shows nothing of yours from this module.
- **SNS:** set the FIFO topic's `ArchivePolicy` to `{}` (a topic with an
  active archive policy can't be deleted), unsubscribe anything you
  subscribed by CLI (`aws sns list-subscriptions`), then delete the
  `fanout` stack. Confirm with `aws sns list-topics`.
- **Lambda:** delete both consumer stacks. Check
  `aws lambda list-event-source-mappings` for mappings you created by
  hand; an orphaned mapping keeps polling. Delete the code zip and the
  bucket if you made it for this module.
- **SQS:** delete the `queues` stack and any queue made outside a stack.
  Confirm with `aws sqs list-queues --queue-name-prefix <you>`.
- **Alarms and logs:** delete the DLQ alarm and any log groups the stacks
  didn't own: check
  `aws logs describe-log-groups --log-group-name-prefix /aws/lambda/<you>`
  and the bus log group.
- **Check the bill:** tomorrow, look at Cost Explorer grouped by service
  for SQS, SNS, EventBridge and Lambda. Explain every non-zero line.

### Retrospective 24.5

#### Question: What stops a loop

_Lambda stops recursive loops that go through SQS, SNS and S3 after about
16 invocations in a chain. Read [Lambda recursive loop
detection](https://docs.aws.amazon.com/lambda/latest/dg/invocation-recursion.html).
Design a loop with the resources from this module that Lambda would
**not** detect (hint: EventBridge isn't in the list). What guardrails
would you put in place: in the event pattern, in the event itself, in
concurrency settings, and in a billing alarm?_

#### Question: Observability of asynchronous systems

_A customer says their order never shipped. In a synchronous system you'd
read one request's log. Here the order passed through a queue, a pipe, a
bus, two rules and a consumer. What identifier would you carry through
every hop, which logs and metrics from this module would you check, and in
what order?_

## Further Reading

- [Amazon SQS best
  practices](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-best-practices.html):
  processing messages in a timely manner, handling request errors and
  reducing cost.
- [Best practices for implementing partial batch
  responses](https://docs.aws.amazon.com/prescriptive-guidance/latest/lambda-event-filtering-partial-batch-responses-for-sqs/best-practices-partial-batch-responses.html)
  (AWS Prescriptive Guidance).
- [Amazon SQS Extended Client Library for
  Python](https://github.com/awslabs/amazon-sqs-python-extended-client-lib):
  payloads larger than 1 MiB through S3, and the same idea for SNS in
  [Publishing large messages with Amazon
  SNS](https://docs.aws.amazon.com/sns/latest/dg/large-message-payloads.html).
- [EventBridge API
  destinations](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-api-destinations.html):
  call third-party HTTP APIs from a rule or a pipe, with rate limiting
  and managed authentication.
- [EventBridge global
  endpoints](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-global-endpoints.html):
  Regional failover for event ingestion, and how it relates to the DR
  patterns in module 23.
- [Serverless Land patterns](https://serverlessland.com/patterns) for
  worked, deployable examples of every integration in this module. Read
  them after you've written your own.
