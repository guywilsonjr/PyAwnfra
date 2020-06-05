from typing import List
from aws_cdk import core,aws_kms as kms, aws_secretsmanager as sm, aws_iam as iam


class PreDefinedSecret:
    secret_name: str
    secret_value: str

    def __init__(self, secret_name, secret_value):
        self.secret_name = secret_name
        self.secret_value = secret_value

class SecretStack(core.Stack):
    kms_key: kms.Key
    secrets = {}

    def __init__(self, app: core.App, id: str, secret_placeholders=None, predefined_secrets=None) -> None:
        super().__init__(app, id)

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
            self.secrets[secret.secret_name] = secret_obj

    def create_placeholders(self, secret_placeholders: list) -> None:
        for secret in secret_placeholders:
            secret_obj = sm.Secret(
                self,
                secret,
                encryption_key=self.kms_key,
                secret_name=secret)
            self.secrets[secret] = secret_obj


