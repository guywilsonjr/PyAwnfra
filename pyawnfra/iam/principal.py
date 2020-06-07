from aws_cdk import aws_iam as iam, region_info as reg
#TODO https://guywilsonjr.myjetbrains.com/youtrack/issue/DR-1
codebuild_service = iam.ServicePrincipal("codebuild.us-west-2.amazonaws.com")
# noinspection PyTypeChecker
codepipeline_service = iam.ServicePrincipal("codepipeline.us-west-2.amazonaws.com")
# noinspection PyTypeCheckerfrom collections import namedtuple
cfn_service = iam.ServicePrincipal("cloudformation.amazonaws.com")


def get_service_principal(service, region) -> iam.ServicePrincipal:
    reg.RegionInfo.get(region).service_principal(service)
    return iam.ServicePrincipal("codebuild.us-west-2.amazonaws.com")