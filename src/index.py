# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_codebuild as codebuild
import aws_cdk.aws_codepipeline as codepipeline, aws_cdk.aws_iam as iam
import aws_cdk.aws_codepipeline_actions as codepipeline_actions, aws_cdk.aws_secretsmanager as sm
import aws_cdk.core as core
import secretsmanager.secrets as secrets
import aws_cdk.app_delivery as cicd


GITHUB_USER_KEY = "GitHubUser"
GITHUB_TOKEN_SECRET_KEY = "GitHubToken"
SECRETS = [GITHUB_USER_KEY, GITHUB_TOKEN_SECRET_KEY]


class MyServiceStackA(core.Stack):
    def __init__(self, stack_app: core.App, stack_id: str) -> None:
        super().__init__(stack_app, stack_id)
        sm.Secret(self, 'TestSecretA')


class MyServiceStackB(core.Stack):
    def __init__(self, stack_app: core.App, stack_id: str) -> None:
        super().__init__(stack_app, stack_id)
        sm.Secret(self, 'TestSecretB')


app = core.App(auto_synth=True)

# We define a stack that contains the CodePipeline
pipeline_stack = core.Stack(app, "PipelineStack")
pipeline = codepipeline.Pipeline(pipeline_stack, "CodePipeline", # Mutating a CodePipeline can cause the currently propagating state to be
                                 # "lost". Ensure we re-run the latest change through the pipeline after it's
                                 # been mutated so we're sure the latest state is fully deployed through.
                                 restart_execution_on_update=True)

# Configure the CodePipeline source - where your CDK App's source code is hosted
source_output = codepipeline.Artifact()
sec = secrets.SecretStack(pipeline_stack, "SecretInfra", SECRETS)
token = sm.Secret.from_secret_arn(pipeline_stack, "TokenSecret", sec.secrets[1].secret_arn).secret_value
source = codepipeline_actions.GitHubSourceAction(
    oauth_token=token,
    output=source_output,
    owner="guywilsonjr",
    repo="PyAwnfra",
    action_name="GitHub")
pipeline.add_stage(stage_name="source", actions=[source])

project = codebuild.PipelineProject(pipeline_stack, "CodeBuild")
synthesized_app = codepipeline.Artifact()
build_action = codepipeline_actions.CodeBuildAction(action_name="CodeBuild", project=project, input=source_output, outputs=[synthesized_app])
pipeline.add_stage(stage_name="build", actions=[build_action])

# Optionally, self-update the pipeline stack
self_update_stage = pipeline.add_stage(stage_name="SelfUpdate")
self_update_stage.add_action(cicd.PipelineDeployStackAction(stack=pipeline_stack, input=synthesized_app, admin_permissions=True, change_set_name="DeploySelfUpdate"))

# Now add our service stacks
deploy_stage = pipeline.add_stage(stage_name="Deploy")
service_stack_a = MyServiceStackA(app, "ServiceStackA")
# Add actions to deploy the stacks in the deploy stage:
deploy_service_aAction = cicd.PipelineDeployStackAction(stack=service_stack_a, input=synthesized_app, change_set_name="DeployA",
    # See the note below for details about this option.
    admin_permissions=True)
deploy_stage.add_action(deploy_service_aAction)
# Add the necessary permissions for you service deploy action. This role is
# is passed to CloudFormation and needs the permissions necessary to deploy
# stack. Alternatively you can enable [Administrator](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_job-functions.html#jf_administrator) permissions above,
# users should understand the privileged nature of this role.


service_stack_b = MyServiceStackB(app, "ServiceStackB")
#deploy_stage.add_action(    cicd.PipelineDeployStackAction(stack=service_stack_b, change_set_name="DeployB", input=synthesized_app, create_change_set_run_order=998, admin_permissions=True))

app.synth()