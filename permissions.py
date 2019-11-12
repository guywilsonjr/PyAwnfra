from aws_cdk.aws_iam import PolicyDocument, PolicyStatement, ServicePrincipal, Anyone

MINIMAL_FUNCTION_ACTIONS = [
    "xray:PutTraceSegments",
    "xray:PutTelemetryRecords",
    "logs:CreateLogGroup",
    "logs:CreateLogStream",
    "logs:DescribeLogGroups",
    "logs:DescribeLogStreams",
    "logs:PutLogEvents",
    "logs:GetLogEvents",
    "logs:FilterLogEvents",
]

DDB_ACTIONS = ["dynamodb:Scan", "dynamodb:PutItem"]
API_INVOKE_STATEMENT_ACTION = "execute-api:Invoke"

"""
cfn role
GetRole
CreateRole
"""

ENDPOINT_SUFFIX = ".amazonaws.com"
API_GATEWAY_ENDPOINT = "apigateway{}".format(ENDPOINT_SUFFIX)
LAMBDA_ENDPOINT = "lambda{}".format(ENDPOINT_SUFFIX)

MINIMAL_FUNCTION_POLICY_STATEMENT = PolicyStatement(
    actions=MINIMAL_FUNCTION_ACTIONS, resources=["*"]
)

MINIMAL_API_POLICY_STATEMENT = PolicyStatement(
    actions=MINIMAL_FUNCTION_ACTIONS,
    resources=["*"],
    principals=[ServicePrincipal(API_GATEWAY_ENDPOINT)],
)

PUBLIC_INVOKE_POLICY_STATEMENT = PolicyStatement(
    actions=[API_INVOKE_STATEMENT_ACTION], resources=["*"], principals=[Anyone()]
)


MINIMAL_PUBLIC_API_POLICY_DOCUMENT = PolicyDocument(
    statements=[MINIMAL_API_POLICY_STATEMENT, PUBLIC_INVOKE_POLICY_STATEMENT]
)


def get_ddb_function_statement(table_arns):
    return PolicyStatement(
        actions=MINIMAL_FUNCTION_ACTIONS + DDB_ACTIONS, resources=table_arns
    )
