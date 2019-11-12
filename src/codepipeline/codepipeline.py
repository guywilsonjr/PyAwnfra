#!/usr/bin/env python3
from aws_cdk import (
    core,
    aws_codepipeline as cp,
    aws_codepipeline_actions as cpa,
    aws_codebuild as cb,
    aws_ec2 as ec2,
    aws_secretsmanager as sm,
    aws_iam as iam,
)

codebuild_service = iam.ServicePrincipal("codebuild.us-west-2.amazonaws.com")

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


class CodePipeline(core.Stack):
    def __init__(
        self, app: core.App, id: str, vpc: ec2.Vpc, secret: core.SecretValue
    ) -> None:
        super().__init__(app, id)
        art = cp.Artifact(artifact_name="GitHubToken")
        iam.PolicyStatement(
            actions=["iam:DeleteRole"],
            resources=["TestAppPyAwnfraPipelin*BuildProject*"],
        )
        cb_perms = iam.PolicyStatement(
            actions=["codebuild:CreateProject"], resources=[f"{id}*"]
        )
        # iam.PolicyDocument(statements=[])
        # Turnoff all outbound traffic iam:DeleteRole codebuild:CreateProject
        build_role = iam.LazyRole(
            self,
            "BuildRole",
            assumed_by=codebuild_service,
            inline_policies=None,
            max_session_duration=core.Duration.hours(1),
        )
        cbpp = cb.PipelineProject(
            self,
            "BuildProject",
            build_spec=None,
            role=build_role,
            security_groups=None,
            subnet_selection=None,
            timeout=None,
            vpc=None,
        )
        iam.PolicyStatement(
            actions=["codebuild:CreateProject"], resources=[cbpp.project_arn]
        )

        """
        cpa.CodeBuildAction(
            input=art,
            project=cbpp,
            extra_inputs=None,
            outputs=None,
            type=None,
            action_name="act1test",
        )
        cpa.GitHubSourceAction(
            oauth_token=secret,
            output=art,
            owner="Guywilsonjr",
            repo="PyAwnfra",
            action_name="Source",
        )
        """
        """
        import_stage = cp.StageOptions(stage_name="Code Push", actions=[cpa])
        build_stage = cp.StageOptions(stage_name="Code Build", actions=[])
        git clone --mirror https://github.com/awslabs/aws-demo-php-simple-app.git my-repo-replica
        """
        # cp.Pipeline(self, "Pipeline")
