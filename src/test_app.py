from aws_cdk import core, aws_secretsmanager as sm, aws_iam as iam, aws_ec2 as ec2
from codepipeline.codepipeline import CodePipeline
from secretsmanager.secrets import Secrets
from vpc import vpc_infra

import roles

app_id = "TestAppPyAwnfra"
cfn_endpoint = iam.ServicePrincipal("cloudformation.amazonaws.com")


class TestApp(core.Stack):
    def __init__(self, app: core.App, id: str) -> None:
        super().__init__(app, id)
        sec = Secrets(self, id, ["GitHubToken", "GitHubUser"])
        vpc = vpc_infra.Vpc(self, "VPCInfra")
        pipeline = CodePipeline(self, "Pipeline", vpc, sec.secrets[0].secret_value)
        role_infra = roles.RoleInfra(self, "RoleInfra")
        vpc.add_dependency(role_infra)
        pipeline.add_dependency(role_infra)


APP = core.App()

TestApp(app=APP, id="TestAppPyAwnfra")
APP.synth()
