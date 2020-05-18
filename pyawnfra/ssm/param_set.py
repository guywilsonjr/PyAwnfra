from aws_cdk import core, aws_ssm as ssm


class ParamSet(core.Stack):
    def __init__(self, app: core.App, id: str, param_list: list) -> None:
        super().__init__(app, id)
        self.params = []
        for param in param_list:
            param_to_add = ssm.StringParameter(
                self, f"{param}Param", parameter_name=param, string_value="REPLACE ME"
            )
            self.params.append(param_to_add)
