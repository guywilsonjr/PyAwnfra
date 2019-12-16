from aws_cdk import core, aws_secretsmanager as sm


class SecretStack(core.Stack):
    def __init__(self, app: core.App, id: str, secret_placeholders: list) -> None:
        super().__init__(app, id)
        self.create_placeholders(secret_placeholders)

    def create_placeholders(self, secret_placeholders: list) -> None:
        self.secrets = []
        for secret in secret_placeholders:
            secret_obj = sm.Secret(self, secret, secret_name=secret)
            self.secrets.append(secret_obj)

        self.secret_names = secret_placeholders
