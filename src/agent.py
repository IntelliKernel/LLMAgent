from enum import Enum
import json
from pkgutil import extend_path
from typing import List, Optional, Dict

from openai import Stream
from pydantic import BaseModel

from .llm import LLM
from .react import ReActOutput
from .sandbox import SandBox
from openai.types.chat.chat_completion import ChatCompletion
from openai.types.chat.chat_completion_chunk import ChatCompletionChunk
from openai.types.chat.chat_completion_message_tool_call import Function
from .llm_tool import ToolsBuilder, ParameterProperties


class Mode(str, Enum):
    CoT = "CoT"
    ReAct = "ReAct"
    FunctionCall = "FunctionCall"


def get_weather(location):
    return "24℃"


def average_dog_weight(name):
    if name in "Scottish Terrier":
        return "Scottish Terriers average 20 lbs"
    elif name in "Border Collie":
        return "a Border Collies average weight is 37 lbs"
    elif name in "玩具贵宾犬":
        return "玩具贵宾犬的平均体重为 7 磅"
    else:
        return "An average dog weights 50 lbs"


def calculate(what):
    return eval(what)


def extract_json(text):
    try:
        json_start = text.find("{")
        json_end = text.rfind("}") + 1
        json_content = text[json_start:json_end].replace("\\_", "_")
        return json_content
    except Exception as e:
        return f"Error extracting JSON: {e}"


class Agent:
    def __init__(
        self,
        query: str,
        api_key: str,
        base_url: str,
        model_name: str,
        messages: List,
        stream: bool = False,
        max_tokens: int = 100,
        top_k: int = 50,
        top_p: float = 0.9,
        temperature: float = 0.6,
        interrupt_repeat: bool = False,
        mode: Mode = Mode.CoT,
        tools: Dict = None,
        sandbox: SandBox = None,
    ):
        self.llm = LLM(
            api_key=api_key,
            base_url=base_url,
            model_name=model_name,
            max_tokens=max_tokens,
            top_k=top_k,
            top_p=top_p,
            temperature=temperature,
            interrupt_repeat=interrupt_repeat,
        )
        self.query = query
        self.messages = messages
        self.stream = stream
        self.mode = mode
        self.tools = tools
        self.sandbox = sandbox

    def chat(self):
        self.messages.append({"role": "user", "content": self.query})

        if self.mode == Mode.CoT:
            response = self.cot(self.messages)
        elif self.mode == Mode.ReAct:
            response = self.react(self.messages)
        elif self.mode == Mode.FunctionCall:
            response = self.function_call(self.messages)
        if isinstance(response, ChatCompletion):
            self.messages.append(
                {"role": "assistant", "content": response.choices[0].message.content}
            )
        elif isinstance(response, ChatCompletionChunk):
            whole_response = ""
            for chunk in response:
                whole_response += chunk.choices[0].delta.content
            self.messages.append({"role": "assistant", "content": whole_response})

        return response

    def cot(self, messages: List) -> ChatCompletion | Stream[ChatCompletionChunk]:
        """
        CoT: chain of thoughts
        """
        self.query += "\n\n 请逐步解释您的推理过程，并得出最终答案。"
        response = self.llm.chat(self.messages, stream=self.stream)
        return response

    def function_call(
        self, messages: List
    ) -> ChatCompletion | Stream[ChatCompletionChunk]:
        """
        FunctionCall: function call
        """
        response = self.llm.chat(self.messages, tools=self.tools)
        self.messages.append(response.choices[0].message)
        self.messages.append(
            {
                "role": "tool",
                "tool_call_id": response.choices[0].message.tool_calls[0].id,
                "content": self.run_function(
                    response.choices[0].message.tool_calls[0].function
                ),
            }
        )
        response = self.llm.chat(self.messages, stream=self.stream, tools=self.tools)
        return response

    def run_function(self, tool_call: Function):

        func_name = tool_call.name
        func_args = json.loads(tool_call.arguments)
        ans = globals()[func_name](**func_args)
        # print(f"run function {tool_call.name}({tool_call.arguments}) = {ans}")
        return str(ans)

    def react(
        self, messages: List, max_turns=5
    ) -> ChatCompletion | Stream[ChatCompletionChunk]:
        """
        ReAct: reactive
        """
        turn = 0

        react_output_example = """
        {
            "thinkint": "我需要知道北京的天气",
            "actions": {
                "type": "function",
                "function": {
                    "name": "get_weather",
                    "parameters": {
                        "location": "beijing"
                    }
                }
            }
        }
        """

        react_prompt = (
            f"""
        这是你可以使用的工具:{self.tools}    
        
        你的输出需要是一个json, 需要遵循json schema:
        {ReActOutput.model_json_schema()}
        
        这里有一个输出的例子:
        """
            + react_output_example
        )
        i = 0
        next_prompt = react_prompt + self.query
        self.messages[-1]["content"] = next_prompt
        while i < max_turns:
            i += 1
            response = self.llm.chat(self.messages)
            result = response.choices[0].message.content
            self.messages.append(
                {"role": "assistant", "content": response.choices[0].message.content}
            )
            # print(f"result: {result}")
            llm_output = ReActOutput(**json.loads(extract_json(result)))
            # print(f"llm_output: {llm_output}")

            if llm_output.actions:
                observation = self.run_function(
                    Function(
                        name=llm_output.actions.function.name,
                        arguments=json.dumps(llm_output.actions.function.parameters),
                    )
                )
                next_prompt = f"Observation: {observation}"
                self.messages.append({"role": "user", "content": next_prompt})
            elif llm_output.answer:
                return llm_output.answer


if __name__ == "__main__":
    pass
