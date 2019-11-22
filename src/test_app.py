from aws_cdk import core, aws_secretsmanager as sm, aws_iam as iam, aws_ec2 as ec2
from codepipeline.codepipeline import CodePipeline
from secretsmanager.secrets import Secrets
from vpc import vpc_infra

from ssm import param_set
import roles

app_id = "TestAppPyAwnfra"
cfn_endpoint = iam.ServicePrincipal("cloudformation.amazonaws.com")

PARAMS = ["GitHubToken"]


class TestApp(core.Stack):
    def __init__(self, app: core.App, id: str) -> None:
        super().__init__(app, id)

        param_set.ParamSet(self, "ParamSet", PARAMS)
        sec = Secrets(self, id, ["GitHubToken"])
        vpc = vpc_infra.Vpc(self, "VPCInfra")
        token = sm.Secret.from_secret_arn(
            self, "TokenSecret", sec.secrets[0].secret_arn
        ).secret_value
        pipeline = CodePipeline(self, "Pipeline", vpc, token)
        role_infra = roles.RoleInfra(self, "RoleInfra")

        vpc.add_dependency(role_infra)

        pipeline.add_dependency(role_infra)
        pipeline.add_dependency(vpc)


APP = core.App()

TestApp(app=APP, id="TestAppPyAwnfra")
APP.synth()
