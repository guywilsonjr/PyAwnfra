from aws_cdk import aws_iam as iam, region_info as reg

__all__ = ['policy']


CODEBUILD_PRINCIPAL = iam.ServicePrincipal("codebuild.amazonaws.com")
CODEPIPELINE_PRINCIPAL = iam.ServicePrincipal("codepipeline.amazonaws.com")
CFN_PRINCIPAL = iam.ServicePrincipal("cloudformation.amazonaws.com")



class ServicePrincipal:

    def get_service_principal(service, region) -> iam.ServicePrincipal:
        return iam.ServicePrincipal(
            reg
            .RegionInfo
            .get(region)
            .service_principal('{}.amazonaws.com', service))
