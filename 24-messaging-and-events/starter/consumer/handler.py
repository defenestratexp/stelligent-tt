"""Topic 24 starter: an SQS consumer for Lesson 24.2.

As shipped, this handler processes a batch the naive way: the first
message that fails raises, the whole invocation fails, and every message
in the batch becomes visible again, including the ones that succeeded.
Lab 24.2.2 asks you to change that.

Runtime: Python 3.13. Handler: handler.lambda_handler
"""

from __future__ import annotations

import json
import logging
import os
import time
from typing import Any

logger = logging.getLogger()
logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))

# Seconds of pretend work per message. Raise it in Lab 24.2.1 to watch
# what happens when a batch outlives the queue's visibility timeout.
WORK_SECONDS = float(os.environ.get("WORK_SECONDS", "0.2"))


class PoisonMessageError(Exception):
    """A message this consumer will never be able to process."""


def process(order: dict[str, Any]) -> None:
    """Do the 'work' for one order. Raises on a poison order."""
    if order.get("poison"):
        raise PoisonMessageError(f"order {order.get('orderId')} is poison")
    time.sleep(WORK_SECONDS)
    logger.info(json.dumps({"processed": order.get("orderId"),
                            "sequence": order.get("sequence"),
                            "total": order.get("total")}))


def lambda_handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    records = event.get("Records", [])
    logger.info(json.dumps({"batchSize": len(records)}))

    # TODO(student) Lab 24.2.2: process every record, catch the failures,
    # and return {"batchItemFailures": [{"itemIdentifier": <messageId>}, ...]}
    # so only the failed messages go back to the queue. Remember what the
    # docs say about FIFO queues: stop at the first failure and report
    # that message and every message after it.
    for record in records:
        order = json.loads(record["body"])
        process(order)

    return {}
