from pydantic import BaseModel
from typing import List, Dict, Optional


class FunctionModel(BaseModel):
    name: str
    parameters: Dict[str, str]


class ToolsBuilder(BaseModel):
    type: str
    function: FunctionModel


class ReActOutput(BaseModel):
    thinkint: str
    actions: Optional[ToolsBuilder] = None
    observation: Optional[str] = None
    answer: Optional[str] = None


if __name__ == "__main__":
    # 示例数据
    data = {
        "thinkint": "我需要知道北京的天气",
        "actions": {
            "type": "function",
            "function": {
                "name": "get_weather",
                "parameters": {"location": "beijing"},
            },
        },
    }

    # 将数据转换为 Pydantic 模型实例
    llm_output = ReActOutput(**data)

    # 打印模型数据
    print(llm_output)
