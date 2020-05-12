from aws_cdk import(core,
    aws_secretsmanager as sm,
    aws_iam as iam,
    app_delivery as ad,
    aws_s3 as s3,
    aws_codebuild as cb,
    aws_codepipeline as cp,
    aws_codepipeline_actions as cpa)

from codepipeline.codepipeline import CodePipeline
from secretsmanager import secrets
from vpc import vpc_infra


app_id = "TestAppPyAwnfra"
# noinspection PyTypeChecker
codebuild_service = iam.ServicePrincipal("codebuild.us-west-2.amazonaws.com")
# noinspection PyTypeChecker
codepipeline_service = iam.ServicePrincipal("codepipeline.us-west-2.amazonaws.com")
# noinspection PyTypeChecker
cfn_endpoint = iam.ServicePrincipal("cloudformation.amazonaws.com")

GITHUB_USER_KEY = "GitHubUser"
GITHUB_TOKEN_SECRET_KEY = "GitHubToken"
SECRETS = [GITHUB_USER_KEY, GITHUB_TOKEN_SECRET_KEY]
PARAMS = []
managed_policy_names = ["AmazonEC2FullAccess", "AWSCodePipelineFullAccess"]


class TestApp(core.Stack):
    def __init__(self, app: core.App, stack_id: str) -> None:
        '''
        Initializes test_app
        :param app: CDK test_app Object
        :param stack_id: arbitrary stack ID name
        '''
        super().__init__(app, stack_id)
        # noinspection PyTypeChecker
        sec = secrets.SecretStack(self, "SecretInfra", SECRETS)
        # noinspection PyTypeChecker
        vpc = vpc_infra.Vpc(self, "VPCInfra")
        token = sm.Secret.from_secret_arn(
            self, "TokenSecret", sec.secrets[1].secret_arn
        ).secret_value
        pipeline = CodePipeline(self, "Pipelines", token)
        build_project_id = "BuildProject"

        pipeline_role = iam.Role(self, "PipelineRole", assumed_by=iam.CompositePrincipal(codepipeline_service, codebuild_service), max_session_duration=core.Duration.hours(4), )
        self.project = cb.PipelineProject(self, build_project_id,
            environment=cb.BuildEnvironment(
                build_image=cb.LinuxBuildImage.STANDARD_3_0,
                compute_type=cb.ComputeType.SMALL),
            build_spec=cb.BuildSpec.from_source_filename("buildspec.yml"), role=pipeline_role)

        print(self.project.node.children[0].environment)
        source_output = cp.Artifact(artifact_name="source-output")
        build_output = cp.Artifact(artifact_name="build-output")
        artifact_bucket = s3.Bucket(self, "ArtifactBucket")

        source_action = cpa.GitHubSourceAction(
            oauth_token=token,
            output=source_output,
            owner="guywilsonjr",
            repo="PyAwnfra",
            action_name="Source")
        source_stage = cp.StageOptions(stage_name="CodePush", actions=[source_action])

        build_action = cpa.CodeBuildAction(
            input=source_output,
            project=self.project,
            action_name="Build",
            outputs=[build_output])
        build_stage = cp.StageOptions(stage_name="Build", actions=[build_action])
        cp.Pipeline(
            self,
            "Pipeline",
            artifact_bucket=artifact_bucket,
            stages=[source_stage, build_stage],
            role=pipeline_role,
            restart_execution_on_update=True)

# noinspection PyArgumentList
test_app = core.App()
TestApp(app=test_app, stack_id="TestAppPyAwnfra")
test_app.synth()
