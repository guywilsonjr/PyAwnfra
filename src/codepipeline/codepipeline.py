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

from iam import permissions

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

ACCOUNT_ID = core.Aws.ACCOUNT_ID
PARTITION = core.Aws.PARTITION
REGION = core.Aws.REGION


class CodePipeline(core.Stack):
    PERMS = iam.PolicyStatement(actions=["codebuild:CreateProject"])

    def get_perms(self, project_arn: str) -> iam.PolicyStatement:

        return self.PERMS

    def __init__(
        self, app: core.App, id: str, vpc: ec2.Vpc, secret: core.SecretValue
    ) -> None:
        super().__init__(app, id)
        art = cp.Artifact(artifact_name="GitHubToken")
        iam.PolicyStatement(
            actions=["iam:DeleteRole"],
            resources=["TestAppPyAwnfraPipelin*BuildProject*"],
        )

        build_project_id = "BuildProject"

        build_role = iam.Role(
            self,
            "BuildRole",
            assumed_by=codebuild_service,
            # inline_policies={"BuildPolicy": iam.PolicyDocument(statements=[cb_perms])},
            max_session_duration=core.Duration.hours(1),
        )
        self.project = cb.PipelineProject(
            self,
            build_project_id,
            build_spec=None,
            role=build_role,
            security_groups=None,
            subnet_selection=None,
            timeout=None,
            vpc=None,
        )
        # self.PERMS.add_resources([self.project.project_arn])

        # self.project.add_to_role_policy(self.PERMS)

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
