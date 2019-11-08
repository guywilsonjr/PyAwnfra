from aws_cdk import core, aws_secretsmanager as sm
from codepipeline.codepipeline import CodePipeline
from secretsmanager.secrets import Secrets


class TestApp(core.Stack):
    def __init__(self, app: core.App, id: str) -> None:
        super().__init__(app, id)
        sec = Secrets(self, id, ["GitHubToken"])
        CodePipeline(self, "Pipeline", sec.secrets[0].secret_value)


APP = core.App()
TestApp(app=APP, id="TestAppPyAwnfra")
APP.synth()
