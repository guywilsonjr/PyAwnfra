from aws_cdk import aws_iam as iam


class SecretsManagerActions:
    CREATE_SECRET = 'CreateSecret'
    LIST_SECRETS = 'ListSecrets'
    GET_RESOURCE_POLICY = 'GetResourcePolicy'
    DESCRIBE_SECRET = 'DescribeSecret'
    PUT_RESOURCE_POLICY = 'PutResourcePolicy'
    PUT_SECRET_VALUE = 'PutSecretValue'
    RESTORE_SECRET = 'RestoreSecret'
    UPDATE_SECRET = 'UpdateSecret'
    DELETE_RESOURCE_POLICY = 'DeleteResourcePolicy'
    DELETE_SECRET = 'DeleteSecret'

    MAIN_ACTIONS = [
        CREATE_SECRET,
        LIST_SECRETS,
        GET_RESOURCE_POLICY,
        DESCRIBE_SECRET,
        PUT_RESOURCE_POLICY,
        PUT_SECRET_VALUE,
        RESTORE_SECRET,
        UPDATE_SECRET,
        DELETE_RESOURCE_POLICY,
        DELETE_SECRET
    ]

