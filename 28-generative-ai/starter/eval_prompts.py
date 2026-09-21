"""Topic 28 starter: score prompt variants against a labelled set of tickets.

Lesson 28.2 asks you to treat a prompt like code: change one thing, measure
the result. This script runs every prompt variant in a directory against
tickets.jsonl, parses a label out of each reply, and reports accuracy, token
usage and the tickets each variant got wrong.

A prompt variant is a text file. The first line that starts with "SYSTEM:"
(optional) becomes the system prompt; everything else is the user prompt,
and the string {ticket} is replaced with the ticket text. For example,
prompts/zero-shot.txt:

    SYSTEM: You label customer support tickets.
    Label this ticket as one of billing, shipping, returns, account, other.
    Ticket: {ticket}
    Label:

Examples (AWS_PROFILE=lab):

    python eval_prompts.py prompts/
    python eval_prompts.py prompts/ --model-id us.amazon.nova-micro-v1:0 --repeat 3
    python eval_prompts.py prompts/few-shot.txt --limit 5 --show-replies

Requires Python 3.13 and boto3. Temperature defaults to 0 so that repeated
runs are comparable; Lab 28.2.3 asks you to find out how deterministic that
really is.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import boto3

LABELS = ("billing", "shipping", "returns", "account", "other")
HERE = Path(__file__).resolve().parent


def load_tickets(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def load_variant(path: Path) -> tuple[str | None, str]:
    system: str | None = None
    body: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if system is None and line.startswith("SYSTEM:"):
            system = line.removeprefix("SYSTEM:").strip()
        else:
            body.append(line)
    template = "\n".join(body).strip()
    if "{ticket}" not in template:
        raise SystemExit(f"{path}: the prompt must contain {{ticket}}")
    return system, template


def parse_label(reply: str) -> str | None:
    """Turn the model's reply into one of LABELS, or None if it can't.

    TODO(student): this naive version takes the first word. Make it robust
    to the replies you actually see ("Label: Billing.", JSON, a sentence
    before the answer), or change your prompt so the reply is easy to parse
    (Lab 28.2.2). Never trust the reply to be a valid label: an injected
    ticket (t21) can make it say anything.
    """
    words = reply.strip().split()
    if not words:
        return None
    first = words[0].strip(".,:;\"'").lower()
    return first if first in LABELS else None


def classify(client: Any, model_id: str, system: str | None, prompt: str, max_tokens: int) -> tuple[str, dict[str, int]]:
    request: dict[str, Any] = {
        "modelId": model_id,
        "messages": [{"role": "user", "content": [{"text": prompt}]}],
        "inferenceConfig": {"maxTokens": max_tokens, "temperature": 0.0},
    }
    if system:
        request["system"] = [{"text": system}]
    response = client.converse(**request)
    blocks = response["output"]["message"]["content"]
    return "".join(b.get("text", "") for b in blocks), response.get("usage", {})


def evaluate(client: Any, args: argparse.Namespace, variant: Path, tickets: list[dict[str, str]]) -> None:
    system, template = load_variant(variant)
    correct = 0
    total = 0
    tokens: Counter[str] = Counter()
    misses: list[str] = []

    for _ in range(args.repeat):
        for ticket in tickets:
            prompt = template.replace("{ticket}", ticket["text"])
            reply, usage = classify(client, args.model_id, system, prompt, args.max_tokens)
            tokens["in"] += usage.get("inputTokens", 0)
            tokens["out"] += usage.get("outputTokens", 0)
            label = parse_label(reply)
            total += 1
            if label == ticket["label"]:
                correct += 1
            else:
                misses.append(f"{ticket['id']}: expected {ticket['label']}, got {label!r} from {reply.strip()[:60]!r}")
            if args.show_replies:
                print(f"  {ticket['id']}: {reply.strip()[:100]!r}")

    print(f"{variant.name}: {correct}/{total} correct ({correct / total:.0%}), "
          f"{tokens['in']} input tokens, {tokens['out']} output tokens")
    for miss in misses:
        print(f"    {miss}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("variants", type=Path, help="a prompt file, or a directory of *.txt prompt files")
    parser.add_argument("--tickets", type=Path, default=HERE / "tickets.jsonl")
    parser.add_argument("--model-id", default="amazon.nova-lite-v1:0")
    parser.add_argument("--max-tokens", type=int, default=20)
    parser.add_argument("--repeat", type=int, default=1, help="run the whole set N times")
    parser.add_argument("--limit", type=int, help="only the first N tickets")
    parser.add_argument("--show-replies", action="store_true")
    args = parser.parse_args()

    tickets = load_tickets(args.tickets)[: args.limit]
    variants = sorted(args.variants.glob("*.txt")) if args.variants.is_dir() else [args.variants]
    if not variants:
        parser.error(f"no prompt variants found in {args.variants}")

    calls = len(variants) * len(tickets) * args.repeat
    print(f"{len(variants)} variant(s) x {len(tickets)} tickets x {args.repeat} = {calls} model calls")
    client = boto3.client("bedrock-runtime")
    for variant in variants:
        evaluate(client, args, variant, tickets)
    return 0


if __name__ == "__main__":
    sys.exit(main())
