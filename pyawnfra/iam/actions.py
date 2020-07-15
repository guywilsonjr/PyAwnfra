class IAMActions:
    name: str
    action_names: list

    @staticmethod
    def generate_action_name(name, action_name: str):
        return '{}:{}'.format(name, action_name)

class Route53Actions(IAMActions):
    name = 'route53'
    FULL_ACCESS = IAMActions.generate_action_name(name, '*')
    CREATE_HOSTED_ZONE = IAMActions.generate_action_name(name, 'CreateHostedZone')

class CWLogsActions(IAMActions):
    name = 'logs'
    FULL_ACCESS = IAMActions.generate_action_name(name, '*')


class IAMIAMActions(IAMActions):
    name = 'iam'
    FULL_ACCESS = IAMActions.generate_action_name(name, '*')


class STSActions(IAMActions):
    name = 'sts'
    ASSUME_ROLE = IAMActions.generate_action_name(name, 'AssumeRole')


class CFNActions(IAMActions):
    name = 'cloudformation'
    FULL_ACCESS = IAMActions.generate_action_name(name, '*')


class KMSActions(IAMActions):
    name = 'kms'
    FULL_ACCESS = IAMActions.generate_action_name(name, '*')
    CREATE_KEY = IAMActions.generate_action_name(name, 'CreateKey')


class SecretsManagerActions(IAMActions):
    name = 'secretsmanager'

    FULL_ACCESS = IAMActions.generate_action_name(name, '*')
    CREATE_SECRET = IAMActions.generate_action_name(name, 'CreateSecret')
    LIST_SECRETS = IAMActions.generate_action_name(name, 'ListSecrets')
    GET_RESOURCE_POLICY = IAMActions.generate_action_name(name, 'GetResourcePolicy')
    DESCRIBE_SECRET = IAMActions.generate_action_name(name, 'DescribeSecret')
    PUT_RESOURCE_POLICY = IAMActions.generate_action_name(name, 'PutResourcePolicy')
    PUT_SECRET_VALUE = IAMActions.generate_action_name(name, 'PutSecretValue')
    RESTORE_SECRET = IAMActions.generate_action_name(name, 'RestoreSecret')
    UPDATE_SECRET = IAMActions.generate_action_name(name, 'UpdateSecret')
    DELETE_RESOURCE_POLICY = IAMActions.generate_action_name(name, 'DeleteResourcePolicy')
    DELETE_SECRET = IAMActions.generate_action_name(name, 'DeleteSecret')

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

