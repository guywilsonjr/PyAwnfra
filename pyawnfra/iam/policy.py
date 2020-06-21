from aws_cdk import aws_iam as iam


class Policy:
    CODEPIPELINE_FULL_ACCESS_POLICY = iam.ManagedPolicy.from_aws_managed_policy_name('AWSCodePipelineFullAccess')
    CODEBUILD_FULL_ACCESS_POLICY = iam.ManagedPolicy.from_aws_managed_policy_name('AWSCodeBuildAdminAccess')
    CLOUDFORMATION_FULL_ACCESS_POLICY = iam.ManagedPolicy.from_aws_managed_policy_name('AWSCloudFormationFullAccess')
    IAM_FULL_ACCESS_POLICY = iam.ManagedPolicy.from_aws_managed_policy_name('IAMFullAccess')
    SECRETS_MANAGER_FULL_ACCESS_POLICY = iam.ManagedPolicy.from_aws_managed_policy_name('SecretsManagerReadWrite')
    S3_FULL_ACCESS_POLICY = iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess')
    KMS_FULL_ACCESS_POLICY = iam.ManagedPolicy.from_aws_managed_policy_name('AWSKeyManagementServicePowerUser')
