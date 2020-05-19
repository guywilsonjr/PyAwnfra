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
import pyawnfra.iam as pyiam
ACCOUNT_ID = core.Aws.ACCOUNT_ID
PARTITION = core.Aws.PARTITION
REGION = core.Aws.REGION


class CodePipeline(core.Stack):
    PERMS = iam.PolicyStatement(actions=["codebuild:CreateProject"])

    def get_perms(self, project_arn: str) -> iam.PolicyStatement:

        return self.PERMS

    def __init__(
        self,
        app: core.App,
        id: str,
        repo_name,
        repo_user,
        token: str) -> None:
        super().__init__(app, id)

        stack_name = "PipelineStack"
        pipeline_stack = core.Stack(self, stack_name)
        build_project_id = "BuildProjects"

        pipeline_role = iam.Role(pipeline_stack, "PipelineRole", assumed_by=codepipeline_service,
            managed_policies=[pyiam.S3_FULL_ACCESS_POLICY, pyiam.KMS_FULL_ACCESS_POLICY, pyiam.SECRETS_MANAGER_FULL_ACCESS_POLICY],
            max_session_duration=core.Duration.hours(4))

        self.build_role = iam.Role(pipeline_stack, "BuildRole", assumed_by=codebuild_service,
            managed_policies=[pyiam.CODEBUILD_FULL_ACCESS_POLICY, pyiam.S3_FULL_ACCESS_POLICY, pyiam.KMS_FULL_ACCESS_POLICY,
                pyiam.SECRETS_MANAGER_FULL_ACCESS_POLICY], max_session_duration=core.Duration.hours(4))

        self.project = cb.PipelineProject(pipeline_stack, build_project_id, build_spec=cb.BuildSpec.from_source_filename("buildspec.yml"),
            role=self.build_role, environment=cb.BuildEnvironment(build_image=cb.LinuxBuildImage.STANDARD_3_0, compute_type=cb.ComputeType.SMALL))

        source_output = cp.Artifact(artifact_name="source-output")
        build_output = cp.Artifact(artifact_name="build-output")
        artifact_bucket = s3.Bucket(pipeline_stack, "ArtifactBucket")

        source_action = cpa.GitHubSourceAction(oauth_token=token, output=source_output, owner=repo_owner, repo=repo_name, action_name="Source")
        source_stage = cp.StageOptions(stage_name="CodePush", actions=[source_action])

        build_action = cpa.CodeBuildAction(input=source_output, role=pipeline_role, project=self.project, action_name="Build", outputs=[build_output])
        build_stage = cp.StageOptions(stage_name="Build", actions=[build_action])
        self.pipeline = cp.Pipeline(pipeline_stack, "Pipeline", artifact_bucket=artifact_bucket, stages=[source_stage, build_stage],
            role=pipeline_role, restart_execution_on_update=True)


        core.CfnOutput()


