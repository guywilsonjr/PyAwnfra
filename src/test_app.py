from aws_cdk import core, aws_secretsmanager as sm, aws_iam as iam
from codepipeline.codepipeline import CodePipeline
from secretsmanager.secrets import Secrets

app_id = "TestAppPyAwnfra"
cfn_endpoint = iam.ServicePrincipal("cloudformation.amazonaws.com")


class TestApp(core.Stack):
    def __init__(self, app: core.App, id: str) -> None:
        super().__init__(app, id)
        sec = Secrets(self, id, ["GitHubToken", "GitHubUser"])
        # CodePipeline(self, "Pipeline", None, sec.secrets[0].secret_value)
        iam.PolicyStatement(actions=["codebuild:CreateProject"], resources=["*"])
        cb_infra_perms = iam.PolicyStatement(
            actions=["codebuild:CreateProject"], resources=[f"*"]
        )
        role_infra_perms = iam.PolicyStatement(
            actions=["iam:DeleteUser", "iam:PutRolePolicy"],
            resources=[f"arn:aws:iam::936272581790:role/{app_id}*"],
        )

        deploy_role = iam.LazyRole(
            self,
            "BuildRole",
            assumed_by=cfn_endpoint,
            inline_policies=[
                iam.PolicyDocument(statements=[cb_infra_perms, role_infra_perms])
            ],
            max_session_duration=core.Duration.hours(1),
        )

        core.CfnOutput(self, "DeployRoleArn", value=deploy_role.role_arn)


APP = core.App()

TestApp(app=APP, id="TestAppPyAwnfra")
APP.synth()
