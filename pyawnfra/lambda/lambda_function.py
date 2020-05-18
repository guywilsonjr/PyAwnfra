#!/usr/bin/env python3
from aws_cdk.core import Stack, App, Duration
from aws_cdk.aws_lambda import Function, Code, Runtime, Tracing
#from aws_cdk.iam import Role, ServicePrincipal


class LambdaFunction(Stack):
    '''
    This is a thin wrapper around a lambda function to create it in a separate stack
    '''

    def __init__(
            self,
            app: App,
            id: str,
            code_txt: str,
            runtime: str,
            handler: str,
            env: dict,
            policy: str) -> None:
                
        super().__init__(app, id)
        function_role = Role(
            self,
            'NonLazyRole',
            assumed_by=ServicePrincipal('lambda.amazonaws.com'))
        self.function = Function(
            self,
            'Function'.format('{}'.format(id)),
            code=Code.inline(code_txt),
            runtime=Runtime('python3.7', supports_inline_code=True),
            handler='index.create',
            environment=env,
            initial_policy=[policy],
            tracing=Tracing.ACTIVE,
            role=function_role
        )
