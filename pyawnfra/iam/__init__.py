from aws_cdk import aws_iam as iam, region_info as reg

__all__ = ['policy']

# noinspection
codebuild_service = iam.ServicePrincipal("codebuild.us-west-2.amazonaws.com")
# noinspection PyTypeChecker
codepipeline_service = iam.ServicePrincipal("codepipeline.amazonaws.com")
# noinspection PyTypeChecker
cfn_service = iam.ServicePrincipal("cloudformation.amazonaws.com")



class ServicePrincipal:

    def get_service_principal(service, region) -> iam.ServicePrincipal:
        return iam.ServicePrincipal(
            reg
            .RegionInfo
            .get(region)
            .service_principal('{}.amazonaws.com', service))
