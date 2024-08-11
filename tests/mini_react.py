import json
import openai

from tool_define_test import ParameterProperties, ToolsBuilder

client = openai.OpenAI()


# 构建工具
builder = ToolsBuilder()

# 定义一个计算圆面积的工具
builder.add_tool(
    tool_type="function",
    function_name="calculate_circle_area",
    function_description="Calculate the area of a circle given its radius.",
    parameters={
        "radius": ParameterProperties(
            type="number", description="The radius of the circle."
        )
    },
    required=["radius"],
)

# 导出工具为 JSON
tools = builder.export_json()


def calculate_circle_area(radius):
    return str(3.14159 * radius * radius)


def send_messages(messages):
    response = client.chat.completions.create(
        model="deepseek-chat", messages=messages, tools=tools  # 使用你可用的模型名称
    )
    return response.choices[0].message


def run_function(tool_call):
    print(type(tool_call))
    func_name = tool_call.name
    func_args = json.loads(tool_call.arguments)
    return globals()[func_name](**func_args)


messages = [
    {"role": "user", "content": "What is the area of a circle with a radius of 5?"}
]
message = send_messages(messages)
print(f"User>\t {messages[0]['content']}")
print(f"Model>\t content: {message.content}, tools: {message.tool_calls}")

# 获取工具调用
tool = message.tool_calls[0]
print(f"tool: {tool}")

# 执行工具功能
result = run_function(tool.function)
messages.append(message)
messages.append({"role": "tool", "tool_call_id": tool.id, "content": result})

# 发送带有结果的消息
message = send_messages(messages)
print(f"Model>\t {message.content}")
