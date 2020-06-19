from aws_cdk import aws_iam as iam


class SecretsManagerActions:

    def generate_action_name(action_name: str):
        return 'secretsmanager:{}'.format(action_name)

    CREATE_SECRET = generate_action_name('CreateSecret')
    LIST_SECRETS = generate_action_name('ListSecrets')
    GET_RESOURCE_POLICY = generate_action_name('GetResourcePolicy')
    DESCRIBE_SECRET = generate_action_name('DescribeSecret')
    PUT_RESOURCE_POLICY = generate_action_name('PutResourcePolicy')
    PUT_SECRET_VALUE = generate_action_name('PutSecretValue')
    RESTORE_SECRET = generate_action_name('RestoreSecret')
    UPDATE_SECRET = generate_action_name('UpdateSecret')
    DELETE_RESOURCE_POLICY = generate_action_name('DeleteResourcePolicy')
    DELETE_SECRET = generate_action_name('DeleteSecret')

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

