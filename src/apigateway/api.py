from aws_cdk.core import Stack
from aws_cdk.aws_apigateway import LambdaRestApi



class LambdaAPI(Stack):
    def __init__(self):
        pass
    
    def create_lambda(
            self,
            id: str,
            code: S3Code,
            handler: str,
            runtime: str,
            env: dict,
            timeout: int) -> None:

        role = Role(
            self,
            '{}{}nRole'.format(self.id, id),
            assumed_by=ServicePrincipal('lambda.amazonaws.com'))

        return Function(
            self,
            '{}{}Function'.format(self.id, id),
            timeout=core.Duration.seconds(timeout),
            code=code,
            handler=handler,
            environment=env,
            tracing=Tracing.ACTIVE,
            initial_policy=[MINIMAL_FUNCTION_POLICY_STATEMENT],
            runtime=Runtime(
                name='python3.7',
                supports_inline_code=True,
            ),
            role=role
        )

    def create_api(
            self,
            function: Function,
            resources: dict,
            domain: str,
            cert_arn: str) -> LambdaRestApi:
        cert = Certificate.from_certificate_arn(
            self, '{}Cert'.format(self.id), certificate_arn=cert_arn)
        domain_options = DomainNameOptions(
            domain_name=domain,
            certificate=cert,
            endpoint_type=EndpointType.EDGE)

        api = LambdaRestApi(
            self,
            '{}API'.format(self.id),
            domain_name=domain_options,
            handler=function,
            proxy=False,
            endpoint_types=[
                EndpointType.EDGE],
            cloud_watch_role=False,
            policy=MINIMAL_PUBLIC_API_POLICY_DOCUMENT,
            deploy=True,
            default_method_options={
                'authorizationType': AuthorizationType.NONE})

        api.root.add_method(
            http_method='GET',
            integration=LambdaIntegration(function),
            authorization_type=AuthorizationType.NONE)
        for resource, methods in self.api_resources.items():
            res = api.root.add_resource(resource)
            for method in methods:
                if resource in self.API_CHILD_RESOURCES:
                    child_res = res.add_resource(self.API_CHILD_RESOURCES[resource])
                    child_res.add_method(
                        http_method=method,
                        integration=LambdaIntegration(function),
                        authorization_type=AuthorizationType.NONE)
                        
                method = res.add_method(
                    http_method=method,
                    integration=LambdaIntegration(function),
                    authorization_type=AuthorizationType.NONE)
        return api

    def route_domain_to_api(
            self,
            domain: str,
            api: RestApi,
            hosted_zone_id: str) -> None:
        api_target = ApiGatewayDomain(api.domain_name)
        hosted_zone = HostedZone.from_hosted_zone_attributes(
            self, '{}HostedZone'.format(
                self.id), hosted_zone_id=hosted_zone_id, zone_name=domain)
        ARecord(
            self,
            '{}RouteRecord'.format(
                self.id),
            target=RecordTarget(alias_target=api_target),
            zone=hosted_zone,
            record_name=domain)
            
    def create_metrics(self, id, app_name, metrics):
        pass
