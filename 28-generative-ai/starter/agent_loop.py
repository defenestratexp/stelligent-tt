"""Topic 28 starter: the agent loop, by hand, with the Converse API.

An "agent" is a loop: send the conversation and a list of tools to the
model; if it answers with stopReason "tool_use", run the tool it asked for,
append the result, and call the model again; stop when it answers with
"end_turn" (or when you decide it has had enough turns). Lab 28.5.1 has you
finish this loop. Lab 28.5.3 then hands the same job to a managed harness.

The "backend" here is a Python dict of fake orders, so nothing real can
break. One tool, issue_refund, has a side effect on purpose.

Examples (AWS_PROFILE=lab):

    python agent_loop.py "Where is order A1001?"
    python agent_loop.py "Order A1002 arrived broken. I want my money back."
    python agent_loop.py --max-turns 2 "Check every order from A1001 to A1010"

Requires Python 3.13 and boto3. Pick a model that supports tool use
(see the Converse "supported models and model features" table).
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any, Callable

import boto3

# --- a pretend backend -------------------------------------------------------

ORDERS: dict[str, dict[str, Any]] = {
    "A1001": {"status": "shipped", "carrier": "UPS", "total": 129.00, "refunded": False},
    "A1002": {"status": "delivered", "carrier": "USPS", "total": 349.99, "refunded": False},
    "A1003": {"status": "processing", "carrier": None, "total": 42.50, "refunded": False},
}

RETURN_POLICY = (
    "Unused items can be returned within 30 days of delivery for a full refund. "
    "Damaged items can be returned at any time for a replacement or refund."
)


def lookup_order(order_id: str) -> dict[str, Any]:
    order = ORDERS.get(order_id)
    if order is None:
        return {"error": f"no order {order_id}"}
    return {"order_id": order_id, **order}


def get_return_policy() -> dict[str, Any]:
    return {"policy": RETURN_POLICY}


def issue_refund(order_id: str, reason: str) -> dict[str, Any]:
    """A tool with a side effect. Think hard before you let a model call it.

    TODO(student): Lab 28.5.2. Before refunding, require a human to
    approve (for example, input() asking y/N), cap the amount, and log who
    approved it. What should the tool return when the human says no?
    """
    order = ORDERS.get(order_id)
    if order is None:
        return {"error": f"no order {order_id}"}
    if order["refunded"]:
        return {"error": f"order {order_id} was already refunded"}
    order["refunded"] = True
    return {"order_id": order_id, "refunded": order["total"], "reason": reason}


TOOLS: dict[str, Callable[..., dict[str, Any]]] = {
    "lookup_order": lookup_order,
    "get_return_policy": get_return_policy,
    "issue_refund": issue_refund,
}

TOOL_CONFIG: dict[str, Any] = {
    "tools": [
        {
            "toolSpec": {
                "name": "lookup_order",
                "description": "Look up the status, carrier and total of one order by its ID (for example A1001).",
                "inputSchema": {"json": {
                    "type": "object",
                    "properties": {"order_id": {"type": "string"}},
                    "required": ["order_id"],
                }},
            }
        },
        {
            "toolSpec": {
                "name": "get_return_policy",
                "description": "Return the store's return and refund policy.",
                "inputSchema": {"json": {"type": "object", "properties": {}}},
            }
        },
        {
            "toolSpec": {
                "name": "issue_refund",
                "description": "Refund an order in full. Only for delivered orders that qualify under the return policy.",
                "inputSchema": {"json": {
                    "type": "object",
                    "properties": {"order_id": {"type": "string"}, "reason": {"type": "string"}},
                    "required": ["order_id", "reason"],
                }},
            }
        },
    ]
}

SYSTEM_PROMPT = (
    "You are a customer service assistant for an outdoor gear shop. "
    "Use the tools to answer questions about orders. Never guess an order's status."
)

# --- the loop ----------------------------------------------------------------


def run_tool(name: str, tool_input: dict[str, Any]) -> dict[str, Any]:
    """Run one tool the model asked for and return a JSON-serializable result."""
    func = TOOLS.get(name)
    if func is None:
        return {"error": f"unknown tool {name}"}
    try:
        return func(**tool_input)
    except TypeError as err:  # the model sent arguments the tool doesn't take
        return {"error": str(err)}


def agent(client: Any, model_id: str, question: str, max_turns: int) -> str:
    messages: list[dict[str, Any]] = [{"role": "user", "content": [{"text": question}]}]
    usage_in = usage_out = 0

    for turn in range(1, max_turns + 1):
        response = client.converse(
            modelId=model_id,
            system=[{"text": SYSTEM_PROMPT}],
            messages=messages,
            toolConfig=TOOL_CONFIG,
            inferenceConfig={"maxTokens": 512, "temperature": 0.0},
        )
        usage_in += response["usage"]["inputTokens"]
        usage_out += response["usage"]["outputTokens"]
        message = response["output"]["message"]
        messages.append(message)  # the assistant turn, including any toolUse blocks
        stop = response["stopReason"]
        print(f"[turn {turn}: stopReason={stop}, tokens so far in={usage_in} out={usage_out}]")

        if stop != "tool_use":
            return "".join(block.get("text", "") for block in message["content"])

        # TODO(student): Lab 28.5.1. For every content block in `message`
        # that has a "toolUse" key:
        #   - print the tool name and input (you want to see what the model asked for),
        #   - call run_tool(name, input),
        #   - build a toolResult block with the same toolUseId, the result as
        #     {"json": result}, and "status": "error" if the result has an "error" key.
        # Then append ONE user message whose content is the list of toolResult
        # blocks, and let the loop call the model again.
        raise NotImplementedError("finish the tool-use step")

    return f"(stopped after {max_turns} turns without a final answer)"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("question")
    parser.add_argument("--model-id", default="amazon.nova-lite-v1:0")
    parser.add_argument("--max-turns", type=int, default=5)
    args = parser.parse_args()

    client = boto3.client("bedrock-runtime")
    print(agent(client, args.model_id, args.question, args.max_turns))
    print("orders now:", json.dumps(ORDERS, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
