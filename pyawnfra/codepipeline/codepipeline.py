#!/usr/bin/env python3
from aws_cdk import (
    core,
    aws_codepipeline as cp,
    aws_codepipeline_actions as cpa,
    aws_codebuild as cb,
    aws_ec2 as ec2,
    aws_iam as iam,
    aws_s3 as s3,
)
ACCOUNT_ID = core.Aws.ACCOUNT_ID
PARTITION = core.Aws.PARTITION
REGION = core.Aws.REGION


class CodePipeline(core.Stack):
    PERMS = iam.PolicyStatement(actions=["codebuild:CreateProject"])

    def get_perms(self, project_arn: str) -> iam.PolicyStatement:

        return self.PERMS

    def __init__(self, app: core.App, id: str, token: str) -> None:
        super().__init__(app, id)


