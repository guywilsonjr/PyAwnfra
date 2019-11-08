#!/usr/bin/env python3
from aws_cdk import core, aws_codepipeline as cp, aws_codepipeline_actions as cpa


class CodePipeline(core.Stack):
    def __init__(self, app: core.App, id: str, secret) -> None:
        super().__init__(app, id)
        art = cp.Artifact(artifact_name="GitHub")
        aws_codebuild.Project(scope, id, *, artifacts=None, secondary_artifacts=None, secondary_sources=None, source=None, allow_all_outbound=None, badge=None, build_spec=None, cache=None, description=None, encryption_key=None, environment=None, environment_variables=None, project_name=None, role=None, security_groups=None, subnet_selection=None, timeout=None, vpc=None)
        cpa.CodeBuildAction( input=art, project, extra_inputs=None, outputs=, type=None, action_name)
        cpa.GitHubSourceAction(
            oauth_token=secret,
            output=art,
            owner="Guywilsonjr",
            repo="PyAwnfra",
            action_name="Source",
        )
        """
        import_stage = cp.StageOptions(stage_name="Code Push", actions=[cpa])
        build_stage = cp.StageOptions(stage_name="Code Build", actions=[])
        """
        # cp.Pipeline(self, "Pipeline")
