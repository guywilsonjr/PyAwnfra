from aws_cdk.iam import aws_iam as iam


IAM_CFN_SERVICE = "cloudformation"
SSM_SERVICE = "ssm"
SECRETS_MANAGER_SERVICE = "secretsmanager"
CDK_ACTIONS = {IAM_CFN_SERVICE: ["GetTemplate", "DescribeStacks"]}
SSM_USER_DATA_ACTIONS = ["ssm:UpdateInstanceInformation"]
SECRETS_MANAGER_CFN_ACTIONS = {
    SECRETS_MANAGER_SERVICE: ["GetRandomPassword", "DeleteSecret"]
}
SSM_SESSION_MANAGER_ACTIONS = [
    "ssmmessages:CreateDataChannel",
    "ssmmessages:OpenControlChannel",
    "ssmmessages:OpenDataChannel",
    "ssmmessages:CreateControlChannel",
    "s3:GetEncryptionConfiguration",
]

ALL_CLOUD_FORMATION_ACTIONS = ["cloudformation:*"]

SSM_POLICY = iam.Policy(
    self,
    "SSMPolicy",
    statements=iam.PolicyStatement(
        actions=SSM_SESSION_MANAGER_ACTIONS + SSM_USER_DATA_ACTIONS, resources="*"
    ),
)

CODE_PIPELINE_POLICY = iam.ManagedPolicy.from_aws_managed_policy_name(
    "AWSCodePipelineFullAccess"
)


def attach_ssm_policy(role: IAM.IRole) -> None:
    SSM_POLICY.attach_to_role(role)


def attach_code_pipeline_policy(role: IAM.IRole) -> None:
    CODE_PIPELINE_POLICY.attach_to_role(role)
