#!/usr/bin/env python3
from aws_cdk import (
    core,
    aws_codepipeline as cp,
    aws_codepipeline_actions as cpa,
    aws_codebuild as cb,
    aws_codecommit as cc,
    aws_ec2 as ec2,
    aws_secretsmanager as sm,
    aws_iam as iam,
    aws_ssm as ssm,
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
codebuild_service = iam.ServicePrincipal("codebuild.us-west-2.amazonaws.com")
codepipeline_service = iam.ServicePrincipal("codepipeline.us-west-2.amazonaws.com")


class CodePipeline(core.Stack):
    PERMS = iam.PolicyStatement(actions=["codebuild:CreateProject"])

    def get_perms(self, project_arn: str) -> iam.PolicyStatement:

        return self.PERMS

    def __init__(self, app: core.App, id: str, vpc: ec2.Vpc, token: str) -> None:
        super().__init__(app, id)

        build_project_id = "BuildProject"
        build_role = iam.Role(
            self,
            "BuildsRole",
            assumed_by=codebuild_service,
            max_session_duration=core.Duration.hours(1),
        )

        pipeline_role = iam.Role(
            self,
            "PipelineRole",
            assumed_by=codepipeline_service,
            max_session_duration=core.Duration.hours(4),
        )
        self.project = cb.PipelineProject(
            self,
            build_project_id,
            environment=cb.BuildEnvironment(
                build_image=cb.LinuxBuildImage.AMAZON_LINUX_2,
                compute_type=cb.ComputeType.SMALL,
            ),
            build_spec=cb.BuildSpec.from_source_filename("buildspec.yml"),
            role=build_role,
        )

        print(self.project.node.children[0].environment)
        artifact = cp.Artifact(artifact_name="Artifact")
        artifact_bucket = s3.Bucket(self, "ArtifactBucket")

        source_action = cpa.GitHubSourceAction(
            oauth_token=token,
            output=artifact,
            owner="guywilsonjr",
            repo="PyAwnfra",
            action_name="Source",
        )
        source_stage = cp.StageOptions(stage_name="CodePush", actions=[source_action])

        build_action = cpa.CodeBuildAction(
            input=artifact, project=self.project, action_name="Build"
        )
        build_stage = cp.StageOptions(stage_name="Build", actions=[build_action])

        cp.Pipeline(
            self,
            "Pipeline",
            artifact_bucket=artifact_bucket,
            stages=[source_stage, build_stage],
            role=pipeline_role,
            restart_execution_on_update=True,
        )
