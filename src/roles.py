from aws_cdk import core, aws_iam as iam, aws_ssm as ssm
from iam import permissions


class RoleInfra(core.Stack):
    cfn_endpoint = iam.ServicePrincipal("cloudformation.amazonaws.com")

    def __init__(self, app: core.App, id: str) -> None:
        super().__init__(app, id)
        deploy_role = iam.LazyRole(
            self,
            "DeployRole",
            assumed_by=self.cfn_endpoint,
            max_session_duration=core.Duration.hours(1),
            inline_policies={
                f"{id}DeployRole": permissions.generate_deploy_doc(app.node.id)
            },
        )
        core.CfnOutput(self, "DeployRoleArn", value=deploy_role.role_arn)
