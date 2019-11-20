from aws_cdk import core, aws_ssm as ssm


class Secrets(core.Stack):
    def __init__(self, app: core.App, id: str, secret_placeholders: list) -> None:
        super().__init__(app, id)
        self.secret_map = dict()
        self.secrets = [
            sm.Secret(self, f"{secret}", secret_name=f"{secret}")
            for secret in secret_placeholders
        ]
