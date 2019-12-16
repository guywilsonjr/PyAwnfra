from aws_cdk import core, aws_iam as iam


class RoleStack(core.Stack):
    def __init__(self, app: core.App, id: str, mps: list) -> None:
        super().__init__(app, id)
        self.deploy_role = iam.LazyRole(
            self,
            "DeployRole",
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(pn) for pn in mps
            ],
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
        )
