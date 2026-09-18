"""Specification for lab25/guardrails.py (Lab 25.4.2).

These tests describe what your two aspects must do. They fail until you
implement them. Copy this file to tests/unit/ in your project and run
`python -m pytest` from the project root.
"""
import aws_cdk as cdk
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_s3 as s3
from aws_cdk.assertions import Annotations, Match

from lab25.guardrails import AllowedLambdaRuntimes, RequireTags

REQUIRED = ["owner", "topic"]
ALLOWED = [lambda_.Runtime.PYTHON_3_13]


def _stack(runtime=lambda_.Runtime.PYTHON_3_13, tags=None):
    """One bucket and one function, with the guardrails applied."""
    app = cdk.App()
    stack = cdk.Stack(app, "GuardrailTest")
    s3.Bucket(stack, "Bucket")
    lambda_.Function(
        stack,
        "Fn",
        runtime=runtime,
        handler="index.handler",
        code=lambda_.Code.from_inline("def handler(event, context):\n    return None\n"),
    )
    for key, value in (tags or {}).items():
        cdk.Tags.of(stack).add(key, value)
    cdk.Aspects.of(stack).add(RequireTags(REQUIRED), priority=cdk.AspectPriority.READONLY)
    cdk.Aspects.of(stack).add(AllowedLambdaRuntimes(ALLOWED), priority=cdk.AspectPriority.READONLY)
    return stack


def test_untagged_resources_are_errors():
    annotations = Annotations.from_stack(_stack())
    annotations.has_error("/GuardrailTest/Bucket/Resource", Match.string_like_regexp("owner"))
    annotations.has_error("/GuardrailTest/Bucket/Resource", Match.string_like_regexp("topic"))


def test_tagged_resources_pass():
    stack = _stack(tags={"owner": "student", "topic": "25"})
    Annotations.from_stack(stack).has_no_error("*", Match.any_value())


def test_one_missing_tag_is_reported_by_name():
    stack = _stack(tags={"owner": "student"})
    annotations = Annotations.from_stack(stack)
    annotations.has_error("/GuardrailTest/Bucket/Resource", Match.string_like_regexp("topic"))
    annotations.has_no_error("/GuardrailTest/Bucket/Resource", Match.string_like_regexp("owner"))


def test_disallowed_runtime_is_an_error():
    stack = _stack(runtime=lambda_.Runtime.PYTHON_3_9, tags={"owner": "student", "topic": "25"})
    Annotations.from_stack(stack).has_error(
        "/GuardrailTest/Fn/Resource", Match.string_like_regexp("python3.9")
    )


def test_allowed_runtime_passes():
    stack = _stack(tags={"owner": "student", "topic": "25"})
    Annotations.from_stack(stack).has_no_error("/GuardrailTest/Fn/Resource", Match.any_value())
