"""Topic 28 starter: call a Bedrock model with the Converse API and show what it cost.

This is a small experiment harness for Lessons 28.1 and 28.2, not a lab
answer. It sends one prompt (optionally several times), prints the reply,
the stop reason, the token usage and the latency, and estimates the price
of the call from a table you fill in yourself.

Examples (run with AWS_PROFILE=lab; the Region comes from the profile):

    python converse.py "Explain an IAM role in one sentence."
    python converse.py --model-id amazon.nova-lite-v1:0 --temperature 1.0 --runs 3 "Name a colour."
    python converse.py --model-id us.amazon.nova-micro-v1:0 "Hello"
    python converse.py --system-file system.txt --prompt-file ticket.txt --max-tokens 50
    python converse.py --guardrail-id abc123 --guardrail-version 1 "..."
    python converse.py --meta lab=28.1.2 --meta owner=you "Hello"

Requires Python 3.13 and a recent boto3 (Converse, requestMetadata and
serviceTier need a 2025-or-later SDK). No credentials or account IDs belong
in this file: boto3 finds them through your profile.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import boto3
from botocore.exceptions import ClientError

DEFAULT_MODEL = "amazon.nova-lite-v1:0"  # in-Region in us-east-2 (checked Sept 2026)

# USD per 1 million tokens, Standard tier, on-demand, for YOUR Region.
# TODO(student): fill these in from https://aws.amazon.com/bedrock/pricing/
# (or the AWS Price List API) for every model you try, and note the date.
# Keys are model IDs or inference profile IDs exactly as you pass them.
PRICES_PER_MILLION: dict[str, tuple[float, float]] = {
    # "amazon.nova-lite-v1:0": (input_price, output_price),
}


def read_text(value: str | None, path: str | None) -> str | None:
    """Return inline text, or the contents of a file, or None."""
    if path:
        return Path(path).read_text(encoding="utf-8")
    return value


def estimate_cost(model_id: str, usage: dict[str, int]) -> float | None:
    """Estimate the on-demand price of one call from its token usage.

    TODO(student): implement this from PRICES_PER_MILLION. Return None when
    the model isn't in the table. Think about what the formula ignores:
    prompt-cache reads and writes, batch and Flex discounts, and guardrail
    text units, which are billed separately.
    """
    return None


def parse_meta(pairs: list[str]) -> dict[str, str]:
    meta: dict[str, str] = {}
    for pair in pairs:
        key, _, value = pair.partition("=")
        if not key:
            raise SystemExit(f"--meta expects key=value, got {pair!r}")
        meta[key] = value
    return meta


def build_request(args: argparse.Namespace, prompt: str, system: str | None) -> dict[str, Any]:
    inference: dict[str, Any] = {"maxTokens": args.max_tokens}
    if args.temperature is not None:
        inference["temperature"] = args.temperature
    if args.top_p is not None:
        inference["topP"] = args.top_p
    if args.stop:
        inference["stopSequences"] = args.stop

    request: dict[str, Any] = {
        "modelId": args.model_id,
        "messages": [{"role": "user", "content": [{"text": prompt}]}],
        "inferenceConfig": inference,
    }
    if system:
        request["system"] = [{"text": system}]
    if args.guardrail_id:
        request["guardrailConfig"] = {
            "guardrailIdentifier": args.guardrail_id,
            "guardrailVersion": args.guardrail_version,
            "trace": "enabled",
        }
    if args.meta:
        request["requestMetadata"] = parse_meta(args.meta)
    return request


def reply_text(response: dict[str, Any]) -> str:
    blocks = response.get("output", {}).get("message", {}).get("content", [])
    return "".join(block.get("text", "") for block in blocks)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("prompt", nargs="?", help="the user prompt (or use --prompt-file)")
    parser.add_argument("--prompt-file")
    parser.add_argument("--system", help="system prompt text")
    parser.add_argument("--system-file")
    parser.add_argument("--model-id", default=DEFAULT_MODEL, help="model ID or inference profile ID")
    parser.add_argument("--temperature", type=float)
    parser.add_argument("--top-p", type=float)
    parser.add_argument("--max-tokens", type=int, default=512)
    parser.add_argument("--stop", action="append", help="stop sequence (repeatable)")
    parser.add_argument("--runs", type=int, default=1, help="send the same request N times")
    parser.add_argument("--guardrail-id")
    parser.add_argument("--guardrail-version", default="DRAFT")
    parser.add_argument("--meta", action="append", default=[], help="requestMetadata key=value (repeatable)")
    parser.add_argument("--show-trace", action="store_true", help="print the guardrail trace, if any")
    args = parser.parse_args()

    prompt = read_text(args.prompt, args.prompt_file)
    if not prompt:
        parser.error("give a prompt or --prompt-file")
    system = read_text(args.system, args.system_file)

    client = boto3.client("bedrock-runtime")
    request = build_request(args, prompt, system)

    total_cost = 0.0
    priced = True
    for run in range(1, args.runs + 1):
        try:
            response = client.converse(**request)
        except ClientError as err:
            error = err.response.get("Error", {})
            print(f"{error.get('Code')}: {error.get('Message')}", file=sys.stderr)
            return 1

        usage = response.get("usage", {})
        cost = estimate_cost(args.model_id, usage)
        if cost is None:
            priced = False
        else:
            total_cost += cost

        print(f"--- run {run} ---")
        print(reply_text(response))
        print(
            f"[stopReason={response.get('stopReason')} "
            f"in={usage.get('inputTokens')} out={usage.get('outputTokens')} "
            f"latencyMs={response.get('metrics', {}).get('latencyMs')} "
            f"cost={'n/a' if cost is None else f'${cost:.8f}'}]"
        )
        if args.show_trace and "trace" in response:
            print(json.dumps(response["trace"], indent=2, default=str))

    if args.runs > 1:
        print(f"=== {args.runs} runs, estimated total {'n/a' if not priced else f'${total_cost:.8f}'} ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
