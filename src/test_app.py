from aws_cdk import core, aws_secretsmanager as sm, aws_iam as iam, aws_ec2 as ec2
from codepipeline.codepipeline import CodePipeline
from secretsmanager import secrets
from vpc import vpc_infra

from ssm import param_set
import roles

app_id = "TestAppPyAwnfra"
cfn_endpoint = iam.ServicePrincipal("cloudformation.amazonaws.com")

GITHUB_USER_KEY = "GitHubUser"
GITHUB_TOKEN_SECRET_KEY = "GitHubToken"
SECRETS = [GITHUB_USER_KEY, GITHUB_TOKEN_SECRET_KEY]
PARAMS = []

managed_policy_names = ["AmazonEC2FullAccess", "AWSCodePipelineFullAccess"]


class TestApp(core.Stack):
    def __init__(self, app: core.App, id: str) -> None:
        super().__init__(app, id)

        # param_set.ParamSet(self, "ParamSet", PARAMS)
        sec = secrets.SecretStack(self, "SecretInfra", SECRETS)
        vpc = vpc_infra.Vpc(self, "VPCInfra")
        token = sm.Secret.from_secret_arn(
            self, "TokenSecret", sec.secrets[1].secret_arn
        ).secret_value
        pipeline = CodePipeline(self, "Pipelines", vpc, token)
        pipeline.add_dependency(vpc)


APP = core.App()

TestApp(app=APP, id="TestAppPyAwnfra")
APP.synth()
