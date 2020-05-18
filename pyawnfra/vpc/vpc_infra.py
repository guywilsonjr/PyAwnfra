from aws_cdk import core, aws_ec2 as ec2


class Vpc(core.Stack):
    def __init__(self, app: core.App, id: str) -> None:
        super().__init__(app, id)
        self.vpc = ec2.Vpc(
            self,
            "VPC",
            cidr="10.0.0.0/16",
            max_azs=1,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name=f"{id}Subnet", subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=24
                )
            ],
        )

        subnet = self.vpc.public_subnets[0]
        route_table = subnet.route_table


"""
environment last on list:
upset about uber callings
"""
