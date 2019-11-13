from aws_cdk.iam import aws_iam as iam

def generate_actions(service_action_map: dict) -> list:
    service_action_list = []
    for service, action_list in service_action_map
         [service_action_list.append(f'{service}:{action}') for action in action_list]
         
    return service_action_list
    
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

ASG_ACTIONS = {'ec2': ['DescribeImages', 'DescribeInstances', 'DescribeInstanceAttribute', 'DescribeKeyPairs', 'DescribeSecurityGroups', 'DescribeSpotInstanceRequests', 'DescribeVpcClassicLink']}
DEPLOY_ACTIONS = {'iam': ['CreateRole']}

DEPLOY_SERVICE_ACTIONS = generate_actions(DEPLOY_ACTIONS)

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

