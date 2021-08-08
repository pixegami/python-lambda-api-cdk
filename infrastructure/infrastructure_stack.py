from aws_cdk import core as cdk

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core
from aws_cdk import aws_lambda
from aws_cdk.aws_apigatewayv2_integrations import LambdaProxyIntegration
from aws_cdk.aws_apigatewayv2 import HttpApi, HttpMethod


class InfrastructureStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        random_drink_lambda = aws_lambda.Function(
            self,
            id="RandomDrinkCDKFunction",
            code=aws_lambda.Code.from_asset("./compute"),
            handler="random_drink.lambda_handler",
            runtime=aws_lambda.Runtime.PYTHON_3_8
        )

        random_drink_integration = LambdaProxyIntegration(
            handler=random_drink_lambda
        )

        http_api = HttpApi(self, "RandomDrinkHttpApi")
        http_api.add_routes(
            path="/random_drink",
            methods=[HttpMethod.ANY],
            integration=random_drink_integration
        )
