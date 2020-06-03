from aws_cdk import core,aws_kms as kms, aws_secretsmanager as sm, aws_iam as iam
CODEPIPELINE_FULL_ACCESS_POLICY = iam.ManagedPolicy.from_aws_managed_policy_name('AWSCodePipelineFullAccess')
CODEBUILD_FULL_ACCESS_POLICY = iam.ManagedPolicy.from_aws_managed_policy_name('AWSCodeBuildAdminAccess')
CLOUDFORMATION_FULL_ACCESS_POLICY = iam.ManagedPolicy.from_aws_managed_policy_name('AWSCloudFormationFullAccess')
SECRETS_MANAGER_FULL_ACCESS_POLICY = iam.ManagedPolicy.from_aws_managed_policy_name('SecretsManagerReadWrite')
S3_FULL_ACCESS_POLICY = iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess')
KMS_FULL_ACCESS_POLICY = iam.ManagedPolicy.from_aws_managed_policy_name('AWSKeyManagementServicePowerUser')
codepipeline_service = iam.ServicePrincipal("codepipeline.amazonaws.com")

class SecretStack(core.Stack):
    def __init__(self, app: core.App, id: str, secret_placeholders: list) -> None:
        super().__init__(app, id)

        self.kms_key = kms.Key(self, "KMSKey")
        self.create_placeholders(secret_placeholders)
        self.role = iam.Role(
            self,
            "testrole",
            assumed_by=codepipeline_service,
            managed_policies=[
                S3_FULL_ACCESS_POLICY,
                KMS_FULL_ACCESS_POLICY,
                SECRETS_MANAGER_FULL_ACCESS_POLICY,
                CODEPIPELINE_FULL_ACCESS_POLICY],
            max_session_duration=core.Duration.hours(4))
        pipeline_kms_policy_statement = iam.PolicyStatement(
            actions=["kms:Decrypt",
                     "kms:Encrypt",
                     "kms:ReEncrypt*",
                     "kms:GenerateDataKey*"],
            resources=['*']
        )
        pipeline_kms_policy_statement.add_arn_principal(self.role.role_arn)
        self.kms_key.node.default_child.key_policy.add_statements(pipeline_kms_policy_statement)

    def create_placeholders(self, secret_placeholders: list) -> None:
        self.secrets = []
        for secret in secret_placeholders:
            secret_obj = sm.Secret(
                self,
                secret,
                encryption_key=self.kms_key,
                secret_name=secret)
            self.secrets.append(secret_obj)
        self.secret_names = secret_placeholders

