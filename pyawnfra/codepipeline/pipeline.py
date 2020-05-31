from typing import List
from aws_cdk import (
    core,
    aws_codepipeline as cp,
    aws_codepipeline_actions as cpa,
    aws_codebuild as cb,
    aws_iam as iam,
    aws_s3 as s3,
    aws_kms as kms,
    app_delivery as ad
)


ACCOUNT_ID = core.Aws.ACCOUNT_ID
PARTITION = core.Aws.PARTITION
REGION = core.Aws.REGION

codebuild_service = iam.ServicePrincipal("codebuild.us-west-2.amazonaws.com")
# noinspection PyTypeChecker
codepipeline_service = iam.ServicePrincipal("codepipeline.us-west-2.amazonaws.com")
# noinspection PyTypeCheckerfrom collections import namedtuple

cfn_service = iam.ServicePrincipal("cloudformation.amazonaws.com")
CODEPIPELINE_FULL_ACCESS_POLICY = iam.ManagedPolicy.from_aws_managed_policy_name('AWSCodePipelineFullAccess')
CODEBUILD_FULL_ACCESS_POLICY = iam.ManagedPolicy.from_aws_managed_policy_name('AWSCodeBuildAdminAccess')
CLOUDFORMATION_FULL_ACCESS_POLICY = iam.ManagedPolicy.from_aws_managed_policy_name('AWSCloudFormationFullAccess')
SECRETS_MANAGER_FULL_ACCESS_POLICY = iam.ManagedPolicy.from_aws_managed_policy_name('SecretsManagerReadWrite')
S3_FULL_ACCESS_POLICY = iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess')
KMS_FULL_ACCESS_POLICY = iam.ManagedPolicy.from_aws_managed_policy_name('AWSKeyManagementServicePowerUser')


class RepoData:
    github_user: str
    repo_name: str
    extra_repos: List[str]
    github_token: str

    def __init__(self, github_user, repo_name, github_token):
        self.github_user = github_user
        self.repo_name = repo_name
        self.github_token = github_token


class PipelineParams:
    github_user: str
    primary_repo: RepoData
    extra_repos: List[RepoData]
    github_token: core.SecretValue

    def __init__(self, github_user: str, primary_repo: RepoData, extra_repos: List[RepoData], github_token: core.SecretValue):
        self.github_user = github_user
        self.primary_repo = primary_repo
        self.extra_repos = extra_repos
        self.github_token = github_token

class PipelineStack(core.Stack):

    def __init__(
        self,
        app: core.App,
        stack_id: str,
        build_spec,
        params):

        super().__init__(app, stack_id)

        stack_name = "PipelineStack"
        pipeline_stack = self
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

        artifact_bucket = s3.Bucket(pipeline_stack, "ArtifactBucket")

        source_stage, primary_source_output, extra_source_outputs = self.create_source_stage(params)
        build_stage, build_output = self.create_build_stage(
            pipeline_stack,
            build_project_id,
            'buildspec.yml',
            primary_source_output,
            extra_source_outputs)

        self_update_stage = self.create_self_update_stage(pipeline_stack, build_output)
        self.pipeline = cp.Pipeline(
            pipeline_stack,
            "Pipeline",
            artifact_bucket=artifact_bucket,
            stages=[source_stage, build_stage, self_update_stage],
            role=self.pipeline_role,
            restart_execution_on_update=True)


    def create_source_stage(
            self,
            params: PipelineParams) -> (cp.StageOptions, cp.Artifact, List[cp.Artifact]):
        print(params.primary_repo.repo_name)
        print("{}_source_output".format(params.primary_repo.repo_name.lower()))
        primary_source_output = cp.Artifact(artifact_name="{}SourceArtifact".format(params.primary_repo.repo_name))
        extra_output_list = list()
        extra_source_action_list = list()
        for extra_repo_data in params.extra_repos:
            extra_output = cp.Artifact(artifact_name="{}SourceArtifact".format(extra_repo_data.repo_name))
            print("{}_source_output".format(extra_repo_data.repo_name.lower()))
            extra_output_list.append(extra_output)
            extra_source_action = cpa.GitHubSourceAction(
                oauth_token=params.github_token,
                output=extra_output,
                owner=params.github_user,
                repo=extra_repo_data.repo_name,
                action_name="{}Source".format(extra_repo_data.repo_name))
            extra_source_action_list.append(extra_source_action)

        primary_source_action = cpa.GitHubSourceAction(
            oauth_token=params.github_token,
            output=primary_source_output,
            owner=params.github_user,
            repo=params.primary_repo.repo_name,
            action_name="{}Source".format(params.primary_repo.repo_name))

        return cp.StageOptions(
            stage_name="CodePush",
            actions=[
                primary_source_action] +
                extra_source_action_list), primary_source_output, extra_output_list

    def create_build_stage(
            self,
            pipeline_stack: core.Stack,
            build_project_id: str,
            build_spec: str,
            primary_input:cp.Artifact,
            extra_inputs: List[cp.Artifact]) -> (cp.StageOptions, cp.Artifact):
        build_output = cp.Artifact('BuildArtifact')
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

        self.pipeline_kms_key = kms.Key(pipeline_stack, 'PipelineKey')
        pipeline_kms_policy_statement = iam.PolicyStatement(
            actions=["kms:Decrypt",
                     "kms:Encrypt",
                     "kms:ReEncrypt*",
                     "kms:GenerateDataKey*"],
            resources=['*']
        )
        pipeline_kms_policy_statement.add_arn_principal(self.pipeline_role.role_arn)
        pipeline_kms_policy_statement.add_arn_principal(self.build_role.role_arn)
        self.pipeline_kms_key.node.default_child.key_policy.add_statements(pipeline_kms_policy_statement)

        build_action = cpa.CodeBuildAction(
            input=primary_input,
            extra_inputs=extra_inputs,
            role=self.pipeline_role,
            project=self.project,
            action_name="Build",
            outputs=[build_output])
        return cp.StageOptions(stage_name="Build", actions=[build_action]), build_output

    def create_self_update_stage(self, pipeline_stack: core.Stack, build_output: cp.Artifact) -> cp.StageOptions:
        self.changeset_role = iam.Role(
            pipeline_stack,
            "ChangesetRole",
            assumed_by=cfn_service,
            managed_policies=[
                CLOUDFORMATION_FULL_ACCESS_POLICY,
                S3_FULL_ACCESS_POLICY,
                KMS_FULL_ACCESS_POLICY,
                SECRETS_MANAGER_FULL_ACCESS_POLICY,
                CODEPIPELINE_FULL_ACCESS_POLICY],
            max_session_duration=core.Duration.hours(4))

        self_update_changeset_action = ad.PipelineDeployStackAction(
            admin_permissions=True,
            change_set_name='Changeset-SelfUpdate',
            role=self.changeset_role,
            input=build_output,
            stack=pipeline_stack)

        return cp.StageOptions(
            stage_name="Self-Update",
            actions=[self_update_changeset_action])



