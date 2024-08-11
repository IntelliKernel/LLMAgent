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
