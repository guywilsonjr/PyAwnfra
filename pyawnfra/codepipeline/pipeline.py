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

import infra_roles
ACCOUNT_ID = core.Aws.ACCOUNT_ID
PARTITION = core.Aws.PARTITION
REGION = core.Aws.REGION


class RepoData:
    '''
    Class representing data needed to create a github source in codepipeline
    '''
    github_user: str
    repo_name: str
    github_token: str

    def __init__(self, github_user, repo_name, github_token):
        self.github_user = github_user
        self.repo_name = repo_name
        self.github_token = github_token


class PipelineParams:
    '''
    Parameters Needed to build a CDK pipeline
    '''
    primary_repo: RepoData
    extra_repos: List[RepoData]
    github_token: core.SecretValue
    build_env_vars: dict

    def __init__(
            self,
            primary_repo: RepoData,
            extra_repos: List[RepoData],
            github_token: core.SecretValue,
            build_env_vars: dict):
        self.primary_repo = primary_repo
        self.extra_repos = extra_repos
        self.github_token = github_token
        self.build_env_vars = build_env_vars


class PipelineStack(core.Stack):

    roles: infra_roles.Roles

    def __init__(
        self,
        app: core.App,
        stack_id: str,
        kms_key: kms.Key,
        params):

        super().__init__(app, stack_id)
        self.roles = infra_roles.Roles(self, 'Roles')
        build_project_id = "BuildProjects"
        artifact_bucket = s3.Bucket(self, "ArtifactBucket")
        source_stage, primary_source_output, extra_source_outputs = self.create_source_stage(params)

        build_stage, build_output = self.create_build_stage(
            build_project_id,
            kms_key,
            params.build_env_vars,
            primary_source_output,
            extra_source_outputs)

        self_update_stage = self.create_self_update_stage(build_output)
        self.pipeline = cp.Pipeline(
            self,
            "Pipeline",
            artifact_bucket=artifact_bucket,
            stages=[source_stage, build_stage, self_update_stage],
            role=self.roles.pipeline_role,
            restart_execution_on_update=True)


        self.roles.pipeline_role.node.try_remove_child('DefaultPolicy')
        self.roles.build_role.node.try_remove_child('DefaultPolicy')
        self.roles.deployment_role.node.try_remove_child('DefaultPolicy')


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
                oauth_token=extra_repo_data.github_token,
                output=extra_output,
                owner=extra_repo_data.github_user,
                repo=extra_repo_data.repo_name,
                action_name="{}Source".format(extra_repo_data.repo_name))
            extra_source_action_list.append(extra_source_action)

        primary_source_action = cpa.GitHubSourceAction(
            oauth_token=params.primary_repo.github_token,
            output=primary_source_output,
            owner=params.primary_repo.github_user,
            repo=params.primary_repo.repo_name,
            action_name="{}Source".format(params.primary_repo.repo_name))

        return cp.StageOptions(
            stage_name="CodePush",
            actions=[
                primary_source_action] +
                extra_source_action_list), primary_source_output, extra_output_list

    def create_build_stage(
            self,
            build_project_id: str,
            kms_key: kms.Key,
            build_env_vars: dict,
            primary_input:cp.Artifact,
            extra_inputs: List[cp.Artifact]) -> (cp.StageOptions, cp.Artifact):
        build_output = cp.Artifact('BuildArtifact')

        self.project = cb.PipelineProject(
            self,
            build_project_id,
            role=self.roles.build_role,
            encryption_key=kms_key,
            environment=cb.BuildEnvironment(
                build_image=cb.LinuxBuildImage.STANDARD_4_0,
                compute_type=cb.ComputeType.SMALL),
            environment_variables=build_env_vars)

        build_action = cpa.CodeBuildAction(
            input=primary_input,
            extra_inputs=extra_inputs,
            role=self.roles.pipeline_role,
            project=self.project,
            action_name="Build",
            outputs=[build_output])
        return cp.StageOptions(stage_name="Build", actions=[build_action]), build_output

    def create_self_update_stage(self, build_output: cp.Artifact) -> cp.StageOptions:

        deploy_action = ad.PipelineDeployStackAction(
            admin_permissions=True,
            change_set_name='Changeset-SelfUpdate',
            role=self.roles.deployment_role,
            input=build_output,
            stack=self)

        return cp.StageOptions(
            stage_name="Self-Update",
            actions=[deploy_action])



