from typing import List, Dict
from aws_cdk import core, aws_kms as kms, aws_secretsmanager as sm, aws_iam as iam


class PreDefinedSecret:
    secret_name: str
    secret_value: str

    def __init__(self, secret_name, secret_value):
        self.secret_name = secret_name
        self.secret_value = secret_value


class Secrets(core.Stack):
    '''
    Stack that  holds your secrets
    '''
    kms_key: kms.Key
    undefined_secrets: Dict[str, sm.Secret]
    defined_secrets: Dict[str, sm.CfnSecret]
    authorized_users = list()

    def __init__(
            self,
            app: core.App,
            construct_id: str,
            authorized_users: List[iam.User],
            secret_placeholders=None,
            predefined_secrets=None) -> None:
        '''
        :param authorized_users: Users authorized for 'main' access to all of the secrets both placeholders and predefined
        :param secret_placeholders: Secrets that will need to be updated at a later time
        :param predefined_secrets: Secrets that already have determined secret values
        '''

        super().__init__(app, construct_id)
        self.undefined_secrets = {}
        self.defined_secrets = {}
        self.authorized_users = authorized_users
        self.kms_key = kms.Key(
            self,
            "KMSKey",
            alias=app.node.id,
            removal_policy=core.RemovalPolicy.DESTROY,
            trust_account_identities=True
        )
        self.create_predefined_secrets(predefined_secrets) if predefined_secrets else None
        self.create_placeholders(secret_placeholders) if secret_placeholders else None

    def create_predefined_secrets(self, predefined_secrets: List[PreDefinedSecret]) -> None:
        for secret in predefined_secrets:
            secret_obj = sm.CfnSecret(
                self,
                secret.secret_name,
                kms_key_id=self.kms_key.key_id,
                name=secret.secret_name,
                secret_string=secret.secret_value
            )
            self.defined_secrets[secret.secret_name] = secret_obj

    def create_placeholders(self, secret_placeholders: list) -> None:
        for secret in secret_placeholders:
            secret_obj = sm.Secret(
                self,
                secret,
                encryption_key=self.kms_key,
                secret_name=secret)
            self.undefined_secrets[secret] = secret_obj
