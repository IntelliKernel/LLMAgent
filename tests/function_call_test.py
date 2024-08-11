from json import loads
import json
from openai import OpenAI

from tool_define_test import ParameterProperties, ToolsBuilder


client = OpenAI()

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
tools = builder.export_json()


def send_messages(messages):
    response = client.chat.completions.create(
        model="deepseek-chat", messages=messages, tools=tools
    )
    return response.choices[0].message


def stream_send_messages(messages):
    response = client.chat.completions.create(
        model="deepseek-chat", messages=messages, tools=tools, stream=True
    )
    return response.choices[0].message


def get_weather(location):
    return "24℃"


def run_function(tool_call):
    print(type(tool_call))
    func_name = tool_call.name
    func_args = json.loads(tool_call.arguments)
    return globals()[func_name](**func_args)


messages = [{"role": "user", "content": "How's the weather in Hangzhou?"}]
message = send_messages(messages)
print(f"User>\t {messages[0]['content']}")
print(f"Model>\t content: {message.content},  tools: {message.tool_calls}")

tool = message.tool_calls[0]
print(f"tool: {tool}")
messages.append(message)

messages.append(
    {"role": "tool", "tool_call_id": tool.id, "content": run_function(tool.function)}
)
message = stream_send_messages(messages)
for chunk in message:
    print(chunk.choices[0].delta.content, end="", flush=False)
