import logging
import typing
from aws_cdk import aws_iam as iam, core


logger = logging.getLogger(__name__)

ACCOUNT_ID = core.Aws.ACCOUNT_ID
PARTITION = core.Aws.PARTITION
REGION = core.Aws.REGION


def generate_global_policy_statement(
    service_actions: typing.List[iam.PolicyStatement]
) -> iam.PolicyStatement:
    logger.debug(
        "Generating global policy statement for service actions: ", service_actions
    )
    return iam.PolicyStatement(actions=service_actions, resources=["*"])


def generate_service_actions(
    service: str, action_list: typing.List[str]
) -> typing.List[str]:
    logger.debug(
        "Generating global policy statement for service",
        service,
        " and actions: ",
        action_list,
    )
    print("Service: ", service, "\n", "Action List: ", action_list)
    [print(f"{service}:{action}") for action in action_list]
    service_actions = [f"{service}:{action}" for action in action_list]
    logger.debug("Service Actions: ", service_actions)
    return service_actions


def generate_statement(
    permissions: typing.Tuple[str, typing.List[str], typing.List[str]], id: str
) -> iam.PolicyStatement:

    service = permissions[0]
    actions = permissions[1]
    resource_template_list = permissions[2]
    resources = [resource.replace("*", f"{id}*") for resource in resource_template_list]
    print(
        f"Under permission: {permissions}",
        f"Submitting Service: {service}",
        f"Actions: {actions}",
        f"Resources: {resources}",
    )
    service_actions = generate_service_actions(service, actions)
    print(service, "\n", actions, "\n", service_actions)
    return iam.PolicyStatement(actions=service_actions, resources=resources)


SSM_USER_DATA_ACTIONS = ["ssm:UpdateInstanceInformation"]

SSM_SESSION_MANAGER_ACTIONS = [
    "ssmmessages:CreateDataChannel",
    "ssmmessages:OpenControlChannel",
    "ssmmessages:OpenDataChannel",
    "ssmmessages:CreateControlChannel",
    "s3:GetEncryptionConfiguration",
]

ASG_ACTIONS = {
    "ec2": [
        "DescribeImages",
        "DescribeInstances",
        "DescribeInstanceAttribute",
        "DescribeKeyPairs",
        "DescribeSecurityGroups",
        "DescribeSpotInstanceRequests",
        "DescribeVpcClassicLink",
    ]
}
EC2_GLOBAL_PERMS = (
    "ec2",
    [
        "AllocateAddress",
        "AttachInternetGateway",
        "AssociateRouteTable",
        "CreateTags",
        "CreateInternetGateway",
        "CreateNatGateway",
        "CreateRoute",
        "CreateRouteTable",
        "CreateSubnet",
        "CreateVpc",
        "DeleteInternetGateway",
        "DeleteNatGateway",
        "DeleteRouteTable",
        "DeleteRoute",
        "DeleteSubnet",
        "DeleteTags",
        "DeleteVpc",
        "DescribeAccountAttributes",
        "DescribeAddresses",
        "DescribeAvailabilityZones",
        "DescribeInternetGateways",
        "DescribeNatGateways",
        "DescribeRouteTables",
        "DescribeSubnets",
        "DescribeVpcs",
        "DetachInternetGateway",
        "ModifySubnetAttribute",
        "ModifyVpcAttribute",
        "ReleaseAddress",
    ],
    ["*"],
)
SECRET_PERMISSIONS = (
    "secretsmanager",
    ["GetRandomPassword", "CreateSecret", "TagResource"],
    ["*"],
)

LOCAL_SECRET_PERMS = (
    "secretsmanager",
    ["DeleteSecret"],
    [f"arn:{PARTITION}:secretsmanager:{REGION}:{ACCOUNT_ID}:secret:*"],
)

IAM_ROLE_PERMS = (
    "iam",
    [
        "DeleteRole",
        "GetRole",
        "CreateRole",
        "PutRolePolicy",
        "DeleteRolePolicy",
        "PassRole",
    ],
    [f"arn:{PARTITION}:iam::{ACCOUNT_ID}:role/*"],
)


CB_PROJECT_PERMS = (
    "codebuild",
    ["CreateProject"],
    [f"arn:{PARTITION}:codebuild:{REGION}:{ACCOUNT_ID}:project/*"],
)

LOCAL_SECRET_ACTIONS = generate_service_actions(
    LOCAL_SECRET_PERMS[0], LOCAL_SECRET_PERMS[1]
)
GLOBAL_SECRET_STATEMENT = generate_global_policy_statement(
    generate_service_actions(SECRET_PERMISSIONS[0], SECRET_PERMISSIONS[1])
)

EC2_STATEMENT = generate_global_policy_statement(
    generate_service_actions(EC2_GLOBAL_PERMS[0], EC2_GLOBAL_PERMS[1])
)

CB_STATEMENT = generate_global_policy_statement(
    generate_service_actions(CB_PROJECT_PERMS[0], CB_PROJECT_PERMS[1])
)

IAM_ROLE_ACTIONS = generate_service_actions(IAM_ROLE_PERMS[0], IAM_ROLE_PERMS[1])
print("IAM_ROLE_ACTIONS: ", IAM_ROLE_ACTIONS)
FLAT_RESOURCE_ACTIONS = [IAM_ROLE_PERMS, LOCAL_SECRET_PERMS]
DEPLOY_STATEMENTS = [EC2_STATEMENT, GLOBAL_SECRET_STATEMENT, CB_STATEMENT]
DEPLOY_DOCUMENT = iam.PolicyDocument(statements=DEPLOY_STATEMENTS)


def get_resource_statements(id: str) -> typing.List[iam.PolicyStatement]:
    start = []
    for perms in FLAT_RESOURCE_ACTIONS:
        start.append(generate_statement(perms, id))
    return start


def generate_deploy_doc(id: str) -> iam.PolicyDocument:
    return iam.PolicyDocument(
        statements=get_resource_statements(id) + DEPLOY_STATEMENTS
    )
