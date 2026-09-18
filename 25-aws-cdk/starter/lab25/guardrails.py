"""Guardrail aspects for Lab 25.4.2.

Copy this file to lab25/guardrails.py in your CDK project. The tests in
tests/unit/test_guardrails.py describe what each aspect must do.

Both aspects only read the construct tree and report problems with
Annotations. They never change a resource. Register them with
priority=cdk.AspectPriority.READONLY so they run after mutating aspects
such as Tags.
"""
from typing import Iterable

import jsii
import aws_cdk as cdk
from aws_cdk import aws_lambda as lambda_
from constructs import IConstruct


@jsii.implements(cdk.IAspect)
class RequireTags:
    """Error on every taggable CloudFormation resource missing a required tag."""

    def __init__(self, keys: Iterable[str]) -> None:
        self.keys = list(keys)

    def visit(self, node: IConstruct) -> None:
        # TODO(student): only look at L1 resources (cdk.CfnResource) that
        # can carry tags (cdk.TagManager.is_taggable). Read the tags the
        # resource will be deployed with, and for each key in self.keys
        # that is missing or empty, add an error annotation that names the
        # key: cdk.Annotations.of(node).add_error(...).
        pass


@jsii.implements(cdk.IAspect)
class AllowedLambdaRuntimes:
    """Error on every Lambda function whose runtime is not on the allow list."""

    def __init__(self, runtimes: Iterable[lambda_.Runtime]) -> None:
        self.allowed = {runtime.name for runtime in runtimes}

    def visit(self, node: IConstruct) -> None:
        # TODO(student): only look at lambda_.CfnFunction. Its runtime is a
        # string such as "python3.13", or None for container images, or an
        # unresolved token (check cdk.Token.is_unresolved). Add an error
        # annotation that names the runtime when it is not in self.allowed.
        pass
