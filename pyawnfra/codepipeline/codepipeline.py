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


"""
iam:DeleteRole  TestAppPyAwnfraPipelineC9F231D6-BuildRole41B77417-1JDP0IG2BNARN
#env:
  #secrets-manager:
     # key: secret-id:json-key:version-stage:version-id
     # key: secret-id:json-key:version-stage:version-id
  #exported-variables:
     # - variable
     # - variable
  #git-credential-helper: yes

phases:
  install:
    #If you use the Ubuntu standard image 2.0 or later, you must specify runtime-versions.
    #If you specify runtime-versions and use an image other than Ubuntu standard image 2.0, the build fails.
    runtime-versions:
      # name: version
      # name: version
      python: 3.7
    commands:
       - yum install node
       - npm install -g aws-cdk
  #pre_build:
    #commands:
      # - command
      # - command
  build:
    commands:
      # - command
      # - command
  #post_build:
    #commands:
      # - command
      # - command
#artifacts:
  #files:
    # - location
    # - location
  #name: $(date +%Y-%m-%d)
  #discard-paths: yes
  #base-directory: location
#cache:
  #paths:
    # - paths
"""

ACCOUNT_ID = core.Aws.ACCOUNT_ID
PARTITION = core.Aws.PARTITION
REGION = core.Aws.REGION


class CodePipeline(core.Stack):
    PERMS = iam.PolicyStatement(actions=["codebuild:CreateProject"])

    def get_perms(self, project_arn: str) -> iam.PolicyStatement:

        return self.PERMS

    def __init__(self, app: core.App, id: str, token: str) -> None:
        super().__init__(app, id)


