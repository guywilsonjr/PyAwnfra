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
    syth_action: SimpleSynthAction
    source_action: cpa.BitBucketSourceAction


class PipelineStack(Stack):
    def __init__(self, pipeline_data: PipelineData):
        super().__init__(pipeline_data.scope,pipeline_data.name, env=pipeline_data.env)
        cloud_assembly_artifact = cp.Artifact('CloudAs')

        self.pipeline = CdkPipeline(
            self,
            "Pipeline",
            cross_account_keys=False,
            self_mutating=True,
            cloud_assembly_artifact=cloud_assembly_artifact,
            source_action=pipeline_data.source_action,
            synth_action=pipeline_data.syth_action
        )
        cfn_build_project = self.node.children[1].node.children[0].node.children[4].node.children[0].node.children[1].node.children[1]
        # Need Privileged mode for starting docker
        cfn_build_project.add_property_override("Environment.PrivilegedMode", "true")
        # Updating from v4 by default in aws-cdk to v5
        cfn_build_project.add_property_override("Environment.Image", "aws/codebuild/standard:5.0")
        # Only clone the last commit. Don't clone the history
        cfn_build_project.add_property_override("Source.GitCloneDepth", 1)

        self.pipeline.add_application_stage(pipeline_data.app_stage)
