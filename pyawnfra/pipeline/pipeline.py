from typing import List
from dataclasses import dataclass
from aws_cdk.pipelines import CdkPipeline, SimpleSynthAction
from aws_cdk.core import Stack
from aws_cdk import core as cdk, aws_iam as iam, aws_codepipeline as cp, aws_codepipeline_actions as cpa, aws_codebuild as cb


@dataclass(frozen=True)
class PipelineData:
    scope: cdk.Stack
    name: str
    github_owner: str
    github_connection_arn: str
    repo_name: str
    repo_branch: str
    env: cdk.Environment
    build_env: dict
    synth_install_commands: List[str]
    app_stage: cdk.Stage


class PipelineStack(Stack):
    def __init__(self, pipeline_data: PipelineData):
        super().__init__(pipeline_data.scope, pipeline_data.name, env=pipeline_data.env)
        self.source_artifact = cp.Artifact('Source')
        self.cloud_assembly_artifact = cp.Artifact('CloudAs')
        self.pipeline = CdkPipeline(
            self,
            "Pipeline",
            self_mutating=True,
            cross_account_keys=False,
            cloud_assembly_artifact=self.cloud_assembly_artifact,
            source_action=cpa.BitBucketSourceAction(
            role=iam.LazyRole(
                self,
                'SourceRole',
                assumed_by=iam.AccountPrincipal(self.account),
                managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess')]
            ),
            action_name="Ship",
            connection_arn=pipeline_data.github_connection_arn,
            owner=pipeline_data.github_owner,
            repo=pipeline_data.repo_name,
            branch=pipeline_data.repo_branch,
            output=self.source_artifact
        ),
            synth_action=SimpleSynthAction(
                install_commands=pipeline_data.synth_install_commands,
                environment=cb.BuildEnvironment(
                    environment_variables={env_key: cb.BuildEnvironmentVariable(value=pipeline_data.build_env[env_key]) for env_key in pipeline_data.build_env},
                    build_image=cb.LinuxBuildImage.STANDARD_5_0,
                    compute_type=cb.ComputeType.SMALL,
                    privileged=True),
                synth_command='cdk synth',
                action_name='Synthesize',
                cloud_assembly_artifact=self.cloud_assembly_artifact,
                source_artifact=self.source_artifact
            )
        )
        pipeline = self.pipeline.node.try_find_child('Pipeline')
        build_stage = pipeline.node.try_find_child('Build')
        synth_action = build_stage.node.try_find_child('Synthesize')
        build_proj = synth_action.node.try_find_child('CdkBuildProject')
        cfn_build_project = build_proj.node.default_child

        # Need Privileged mode for starting docker
        cfn_build_project.add_property_override("Environment.PrivilegedMode", "true")
        # Updating from v4 by default in aws-cdk to v5
        cfn_build_project.add_property_override("Environment.Image", "aws/codebuild/standard:5.0")
        # Only clone the last commit. Don't clone the history
        cfn_build_project.add_property_override("Source.GitCloneDepth", 1)

        self.pipeline.add_application_stage(pipeline_data.app_stage)
