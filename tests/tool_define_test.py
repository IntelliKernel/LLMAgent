import json
from pydantic import BaseModel, Field
from typing import List, Dict


class ParameterProperties(BaseModel):
    type: str
    description: str


class FunctionParameters(BaseModel):
    type: str = "object"
    properties: Dict[str, ParameterProperties]
    required: List[str]


class FunctionModel(BaseModel):
    name: str
    description: str
    parameters: FunctionParameters


class ToolModel(BaseModel):
    type: str
    function: FunctionModel


class ToolsBuilder(BaseModel):
    tools: List[ToolModel] = []

    def add_tool(
        self,
        tool_type: str,
        function_name: str,
        function_description: str,
        parameters: Dict[str, ParameterProperties],
        required: List[str],
    ):
        function = FunctionModel(
            name=function_name,
            description=function_description,
            parameters=FunctionParameters(properties=parameters, required=required),
        )
        tool = ToolModel(type=tool_type, function=function)
        self.tools.append(tool)

    def export_json(self) -> str:
        return json.loads(self.model_dump_json())["tools"]


if __name__ == "__main__":
    # 使用示例
    builder = ToolsBuilder()

    # 定义一个工具
    builder.add_tool(
        tool_type="function",
        function_name="get_weather",
        function_description="Get weather of a location, the user should supply a location first",
        parameters={
            "location": ParameterProperties(
                type="string", description="The city and state, e.g. San Francisco, CA"
            )
        },
        required=["location"],
    )

    # 导出为 JSON
    json_output = builder.export_json()
    print(json_output)
