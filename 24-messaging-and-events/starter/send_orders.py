"""Topic 24 starter: send fake order messages to SQS, SNS or EventBridge.

This is a load generator, not a lab answer. Every lesson in the module
uses it to put traffic on whatever you've just built, so the labs can
concentrate on the messaging service rather than on test data.

Examples (run with AWS_PROFILE=lab):

    python send_orders.py --queue-url https://sqs.us-east-2.amazonaws.com/123456789012/you-orders --count 25
    python send_orders.py --queue-url ... --poison-every 5
    python send_orders.py --queue-url ...fifo --groups 3
    python send_orders.py --topic-arn arn:aws:sns:us-east-2:123456789012:you-orders --count 10
    python send_orders.py --bus-name you-orders --source you.orders --count 10

Requires Python 3.13 and boto3.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
import uuid
import zlib
from decimal import Decimal
from typing import Any

import boto3

CHANNELS = ("web", "store", "partner")
BATCH = 10  # SQS, SNS and EventBridge all accept at most 10 entries per batch call


def make_order(n: int, poison_every: int) -> dict[str, Any]:
    """Build one fake order. Every poison_every-th order is marked poison."""
    customer = random.choice(["c-", "c-", "c-", "vip-"]) + f"{random.randint(1, 40):03d}"
    order: dict[str, Any] = {
        "orderId": str(uuid.uuid4()),
        "sequence": n,
        "customerId": customer,
        "channel": random.choice(CHANNELS),
        "items": random.randint(1, 6),
        "total": float(Decimal(random.uniform(5, 400)).quantize(Decimal("0.01"))),
        "currency": "USD",
    }
    if random.random() < 0.2:
        order["coupon"] = "SAVE10"
    if poison_every and n % poison_every == 0:
        order["poison"] = True
    return order


def chunks(items: list[Any], size: int = BATCH) -> list[list[Any]]:
    return [items[i : i + size] for i in range(0, len(items), size)]


def group_for(order: dict[str, Any], groups: int) -> str:
    """Pick a message group ID. Customer-based, folded into `groups` buckets.

    crc32 rather than hash(): Python randomizes str hashes per process, and
    the same customer should land in the same group on every run.
    """
    return f"group-{zlib.crc32(order['customerId'].encode()) % groups}"


def send_sqs(queue_url: str, orders: list[dict[str, Any]], groups: int, tenant: bool) -> int:
    sqs = boto3.client("sqs")
    fifo = queue_url.endswith(".fifo")
    failed = 0
    for batch in chunks(orders):
        entries = []
        for i, order in enumerate(batch):
            entry: dict[str, Any] = {
                "Id": str(i),
                "MessageBody": json.dumps(order),
                "MessageAttributes": {
                    "channel": {"DataType": "String", "StringValue": order["channel"]},
                },
            }
            if fifo:
                entry["MessageGroupId"] = group_for(order, groups)
                # The order ID is a natural deduplication ID. Lab 24.1.3
                # explores content-based deduplication with the CLI.
                entry["MessageDeduplicationId"] = order["orderId"]
            elif tenant:
                # On a standard queue a message group ID turns on fair queues.
                entry["MessageGroupId"] = order["customerId"]
            entries.append(entry)
        resp = sqs.send_message_batch(QueueUrl=queue_url, Entries=entries)
        for f in resp.get("Failed", []):
            failed += 1
            print(f"FAILED {f['Id']}: {f.get('Code')} {f.get('Message')}", file=sys.stderr)
    return failed


def send_sns(topic_arn: str, orders: list[dict[str, Any]], groups: int) -> int:
    sns = boto3.client("sns")
    fifo = topic_arn.endswith(".fifo")
    failed = 0
    for batch in chunks(orders):
        entries = []
        for i, order in enumerate(batch):
            entry: dict[str, Any] = {
                "Id": str(i),
                "Message": json.dumps(order),
                "MessageAttributes": {
                    "channel": {"DataType": "String", "StringValue": order["channel"]},
                    "total": {"DataType": "Number", "StringValue": str(order["total"])},
                },
            }
            if fifo:
                entry["MessageGroupId"] = group_for(order, groups)
                entry["MessageDeduplicationId"] = order["orderId"]
            entries.append(entry)
        resp = sns.publish_batch(TopicArn=topic_arn, PublishBatchRequestEntries=entries)
        for f in resp.get("Failed", []):
            failed += 1
            print(f"FAILED {f['Id']}: {f.get('Code')} {f.get('Message')}", file=sys.stderr)
    return failed


def send_events(bus_name: str, source: str, orders: list[dict[str, Any]]) -> int:
    events = boto3.client("events")
    failed = 0
    for batch in chunks(orders):
        entries = [
            {
                "EventBusName": bus_name,
                "Source": source,
                "DetailType": "OrderPlaced",
                "Detail": json.dumps(order),
            }
            for order in batch
        ]
        resp = events.put_events(Entries=entries)
        # PutEvents returns 200 even when some entries fail. Check each one.
        if resp.get("FailedEntryCount", 0):
            for entry, result in zip(entries, resp["Entries"]):
                if "ErrorCode" in result:
                    failed += 1
                    order_id = json.loads(entry["Detail"])["orderId"]
                    print(f"FAILED {order_id}: {result['ErrorCode']} {result.get('ErrorMessage')}",
                          file=sys.stderr)
    return failed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--queue-url", help="SQS queue URL (standard or .fifo)")
    target.add_argument("--topic-arn", help="SNS topic ARN (standard or .fifo)")
    target.add_argument("--bus-name", help="EventBridge event bus name")
    parser.add_argument("--source", default="stelligent-u.orders",
                        help="EventBridge source (use your identifier, e.g. you.orders)")
    parser.add_argument("--count", type=int, default=10, help="number of orders to send")
    parser.add_argument("--poison-every", type=int, default=0,
                        help="mark every Nth order as poison (0 = none)")
    parser.add_argument("--groups", type=int, default=3,
                        help="number of message groups for FIFO targets")
    parser.add_argument("--tenant", action="store_true",
                        help="set MessageGroupId on a standard queue (fair queues)")
    parser.add_argument("--seed", type=int, help="random seed, for repeatable runs")
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)
    orders = [make_order(n, args.poison_every) for n in range(1, args.count + 1)]

    if args.queue_url:
        failed = send_sqs(args.queue_url, orders, args.groups, args.tenant)
    elif args.topic_arn:
        failed = send_sns(args.topic_arn, orders, args.groups)
    else:
        failed = send_events(args.bus_name, args.source, orders)

    print(f"sent {len(orders) - failed} of {len(orders)} orders")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
