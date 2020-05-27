from typing import List
from collections import namedtuple
from aws_cdk import (
    core,
    aws_codepipeline as cp,
    aws_codepipeline_actions as cpa,
    aws_codebuild as cb,
    aws_iam as iam,
    aws_s3 as s3,
)
import pyawnfra.iam as pyiam


ACCOUNT_ID = core.Aws.ACCOUNT_ID
PARTITION = core.Aws.PARTITION
REGION = core.Aws.REGION

codebuild_service = iam.ServicePrincipal("codebuild.us-west-2.amazonaws.com")
# noinspection PyTypeChecker
codepipeline_service = iam.ServicePrincipal("codepipeline.us-west-2.amazonaws.com")
# noinspection PyTypeChecker
cfn_service = iam.ServicePrincipal("cloudformation.amazonaws.com")
CODEPIPELINE_FULL_ACCESS_POLICY = iam.ManagedPolicy.from_aws_managed_policy_name('AWSCodePipelineFullAccess')
CODEBUILD_FULL_ACCESS_POLICY = iam.ManagedPolicy.from_aws_managed_policy_name('AWSCodeBuildAdminAccess')
CLOUDFORMATION_FULL_ACCESS_POLICY = iam.ManagedPolicy.from_aws_managed_policy_name('AWSCloudFormationFullAccess')
SECRETS_MANAGER_FULL_ACCESS_POLICY = iam.ManagedPolicy.from_aws_managed_policy_name('SecretsManagerReadWrite')
S3_FULL_ACCESS_POLICY = iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess')
KMS_FULL_ACCESS_POLICY = iam.ManagedPolicy.from_aws_managed_policy_name('AWSKeyManagementServicePowerUser')
pipeline_kms_policy_statement = iam.PolicyStatement(
            actions=["kms:Decrypt",
                     "kms:Encrypt",
                     "kms:ReEncrypt*",
                     "kms:GenerateDataKey*"],
            resources=['*']
        )

class PipelineParams:
    repo_user: str
    primary_git_repo: str
    extra_repos: List[str]
    github_token: str


class CodePipeline(core.Stack):

    def __init__(
        self,
        app: core.App,
        stack_id: str,
        build_spec,
        params) -> None:

        super().__init__(app, stack_id)

        stack_name = "PipelineStack"
        pipeline_stack = core.Stack(self, stack_name)
        build_project_id = "BuildProjects"

        self.pipeline_role = iam.Role(
            pipeline_stack,
            "PipelineRole",
            assumed_by=codepipeline_service,
            managed_policies=[
                S3_FULL_ACCESS_POLICY,
                KMS_FULL_ACCESS_POLICY,
                SECRETS_MANAGER_FULL_ACCESS_POLICY,
                CODEPIPELINE_FULL_ACCESS_POLICY],
            max_session_duration=core.Duration.hours(4))

        self.build_role = iam.Role(
            pipeline_stack,
            "BuildRole",
            assumed_by=codebuild_service,
            managed_policies=[
                CODEBUILD_FULL_ACCESS_POLICY,
                S3_FULL_ACCESS_POLICY,
                KMS_FULL_ACCESS_POLICY,
                SECRETS_MANAGER_FULL_ACCESS_POLICY],
            max_session_duration=core.Duration.hours(4))

        self.project = cb.PipelineProject(
            pipeline_stack,
            build_project_id,
            build_spec=cb.BuildSpec.from_source_filename(build_spec),
            role=self.build_role,
            environment=cb.BuildEnvironment(
                build_image=cb.LinuxBuildImage.STANDARD_4_0,
                compute_type=cb.ComputeType.SMALL))

        source_output = cp.Artifact(artifact_name="source-output")
        build_output = cp.Artifact(artifact_name="build-output")
        artifact_bucket = s3.Bucket(pipeline_stack, "ArtifactBucket")

        source_action = cpa.GitHubSourceAction(
            oauth_token=params.token,
            output=source_output,
            owner=params.repo_owner,
            repo=params.repo_name,
            action_name="Source")
        source_stage = cp.StageOptions(
            stage_name="CodePush",
            actions=[source_action])


        build_action = cpa.CodeBuildAction(
            input=source_output,
            role=self.pipeline_role,
            project=self.project,
            action_name="Build",
            outputs=[build_output])
        build_stage = cp.StageOptions(stage_name="Build", actions=[build_action])
        self.pipeline = cp.Pipeline(
            pipeline_stack,
            "Pipeline",
            artifact_bucket=artifact_bucket,
            stages=[source_stage, build_stage],
            role=self.pipeline_role,
            restart_execution_on_update=True)


