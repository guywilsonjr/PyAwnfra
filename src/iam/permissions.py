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
    service_actions = generate_service_actions(service, actions)
    return iam.PolicyStatement(actions=service_actions, resources=resources)


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
GLOBAL_SECRET_PERMISSIONS = (
    "secretsmanager",
    ["GetRandomPassword", "CreateSecret", "TagResource", "GetSecretValue"],
    ["*"],
)


# Fix secrets use secret Ids aka secret name. This should be more of a function or something
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
        "GetRolePolicy",
        "PutRolePolicy",
        "CreateRole",
        "PutRolePolicy",
        "DeleteRolePolicy",
        "DetachRolePolicy",
        "PassRole",
        "AttachRolePolicy",
        "UpdateAssumeRolePolicy",
    ],
    [f"arn:{PARTITION}:iam::{ACCOUNT_ID}:role/*"],
)

S3_GLOBAL_PERMS = ("s3", ["CreateBucket", "DeleteBucket", "PutObject"], ["*"])

S3_GLOBAL_STATEMENT = generate_global_policy_statement(
    generate_service_actions(S3_GLOBAL_PERMS[0], S3_GLOBAL_PERMS[1])
)

CB_PROJECT_PERMS = (
    "codebuild",
    ["CreateProject", "UpdateProject", "BatchGetProjects"],
    [f"arn:{PARTITION}:codebuild:{REGION}:{ACCOUNT_ID}:project/*"],
)
# GetParams is global
SSM_GLOBAL_PERMS = (
    "ssm",
    ["GetParameters", "PutParameter", "AddTagsToResource", "DeleteParameter"],
    ["*"],
)
SSM_GLOBAL_STATEMENT = generate_global_policy_statement(
    generate_service_actions(SSM_GLOBAL_PERMS[0], SSM_GLOBAL_PERMS[1])
)
LOCAL_SECRET_ACTIONS = generate_service_actions(
    LOCAL_SECRET_PERMS[0], LOCAL_SECRET_PERMS[1]
)
GLOBAL_SECRET_STATEMENT = generate_global_policy_statement(
    generate_service_actions(GLOBAL_SECRET_PERMISSIONS[0], GLOBAL_SECRET_PERMISSIONS[1])
)

EC2_STATEMENT = generate_global_policy_statement(
    generate_service_actions(EC2_GLOBAL_PERMS[0], EC2_GLOBAL_PERMS[1])
)

CB_STATEMENT = generate_global_policy_statement(
    generate_service_actions(CB_PROJECT_PERMS[0], CB_PROJECT_PERMS[1])
)

CP_PERMS = (
    "codepipeline",
    [
        "CreatePipeline",
        "DeletePipeline",
        "GetPipeline",
        "UpdatePipeline",
        "GetPipelineState",
        "ListPipelines",
        "DeleteWebhook",
        "DeregisterWebhookWithThirdParty",
        "ListWebhooks",
        "PutWebhook",
        "RegisterWebhookWithThirdParty",
    ],
    ["*"],
)
CP_STATEMENT = generate_global_policy_statement(
    generate_service_actions(CP_PERMS[0], CP_PERMS[1])
)


# GetParams is global
EVENT_RULE_PERMS = (
    "events",
    [
        "PutRule",
        "DescribeRule",
        "RemoveTargets",
        "PutTargets",
        "ListRules",
        "DeleteRule",
    ],
    ["*"],
)
EVENT_RULE_STATEMENT = generate_global_policy_statement(
    generate_service_actions(EVENT_RULE_PERMS[0], EVENT_RULE_PERMS[1])
)

IAM_ROLE_ACTIONS = generate_service_actions(IAM_ROLE_PERMS[0], IAM_ROLE_PERMS[1])
FLAT_RESOURCE_ACTIONS = [IAM_ROLE_PERMS, LOCAL_SECRET_PERMS]
DEPLOY_STATEMENTS = [
    EVENT_RULE_STATEMENT,
    CP_STATEMENT,
    EC2_STATEMENT,
    GLOBAL_SECRET_STATEMENT,
    CB_STATEMENT,
    SSM_GLOBAL_STATEMENT,
    S3_GLOBAL_STATEMENT,
]
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
