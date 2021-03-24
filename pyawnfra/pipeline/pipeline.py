from dataclasses import dataclass
from aws_cdk.pipelines import CdkPipeline, SimpleSynthAction
from aws_cdk import core as cdk
from aws_cdk.core import Stack
import aws_cdk.aws_codepipeline as cp
import aws_cdk.aws_codepipeline_actions as cpa


@dataclass(frozen=True)
class PipelineData:
    scope: cdk.App
    name: str
    env: cdk.Environment
    cloud_assembly_artifact: cp.Artifact
    source_action: cpa.BitBucketSourceAction
    synth_action: SimpleSynthAction
    app_stage: cdk.Stage


class PipelineStack(Stack):
    def __init__(self, pipeline_data: PipelineData):
        super().__init__(pipeline_data.scope, pipeline_data.name, env=pipeline_data.env)
        self.pipeline = CdkPipeline(
            self,
            "Pipeline",
            cross_account_keys=False,
            self_mutating=True,
            cloud_assembly_artifact=pipeline_data.cloud_assembly_artifact,
            source_action=pipeline_data.source_action,
            synth_action=pipeline_data.synth_action
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
