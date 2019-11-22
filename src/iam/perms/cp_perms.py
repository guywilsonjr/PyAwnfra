VPC_PERMS = (
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

SECRET_PERMISSIONS = ("secretsmanager", ["GetRandomPassword", "CreateSecret"], ["*"])


# Fix secrets use secret Ids aka secret name. This should be more of a function or something
LOCAL_SECRET_PERMS = (
    "secretsmanager",
    ["DeleteSecret", "TagResource"],
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
        "UpdateAssumeRolePolicyDocument",
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

CP_PERMS = (
    "codepipeline",
    [
        "CreatePipeline",
        "DeletePipeline",
        "GetPipeline",
        "UpdatePipeline",
        "GetPipelineState",
        "ListPipelines",
    ],
    ["*"],
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
