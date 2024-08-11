from pydantic_settings import BaseSettings
from src.llm_tool import ParameterProperties, ToolsBuilder
from src.agent import Agent, Mode


class EnvSettings(BaseSettings):
    OPENAI_API_KEY: str
    OPENAI_BASE_URL: str


env_settings = EnvSettings()

if __name__ == "__main__":

    # CoT
    agent = Agent(
        query="怎么计算 2 + 2",
        api_key=env_settings.OPENAI_API_KEY,
        base_url=env_settings.OPENAI_BASE_URL,
        model_name="deepseek-chat",
        max_tokens=1500,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant.",
            }
        ],
        stream=True,
        mode=Mode.CoT,
    )

    response = agent.chat()
    print("CoT response:")
    for chunk in response:
        print(chunk.choices[0].delta.content, end="", flush=True)
    print()

    # # function call
    # builder = ToolsBuilder()

    # # 定义一个工具
    # builder.add_tool(
    #     tool_type="function",
    #     function_name="calculate",
    #     function_description="Calculate the result of a math expression",
    #     parameters={
    #         "what": ParameterProperties(
    #             type="string", description="The math expression"
    #         )
    #     },
    #     required=["what"],
    # )

    # agent = Agent(
    #     query="怎么计算 2 + 2",
    #     api_key=env_settings.OPENAI_API_KEY,
    #     base_url=env_settings.OPENAI_BASE_URL,
    #     model_name="deepseek-chat",
    #     max_tokens=1500,
    #     messages=[
    #         {
    #             "role": "system",
    #             "content": "You are a helpful assistant.",
    #         }
    #     ],
    #     stream=True,
    #     mode=Mode.FunctionCall,
    #     tools=builder.export_json(),
    # )

    # response = agent.chat()
    # print("Function call response:")
    # for chunk in response:
    #     print(chunk.choices[0].delta.content, end="", flush=True)
    # print()

    # # ReAct
    # builder = ToolsBuilder()

    # # 定义一个工具
    # builder.add_tool(
    #     tool_type="function",
    #     function_name="get_weather",
    #     function_description="Get weather of a location, the user should supply a location first",
    #     parameters={
    #         "location": ParameterProperties(
    #             type="string", description="The city and state, e.g. San Francisco, CA"
    #         )
    #     },
    #     required=["location"],
    # )

    # builder.add_tool(
    #     tool_type="function",
    #     function_name="average_dog_weight",
    #     function_description="Get the average weight of a dog breed",
    #     parameters={
    #         "name": ParameterProperties(
    #             type="string", description="The name of the dog breed"
    #         )
    #     },
    #     required=["name"],
    # )

    # builder.add_tool(
    #     tool_type="function",
    #     function_name="calculate",
    #     function_description="Calculate the result of a math expression",
    #     parameters={
    #         "what": ParameterProperties(
    #             type="string", description="The math expression"
    #         )
    #     },
    #     required=["what"],
    # )

    # # 导出为 JSON
    # tools = builder.export_json()

    # agent = Agent(
    #     query="我有两只狗，一只Scottish Terrier和一只Border Collie。\n它们的总体重是多少",
    #     api_key=env_settings.OPENAI_API_KEY,
    #     base_url=env_settings.OPENAI_BASE_URL,
    #     model_name="deepseek-chat",
    #     max_tokens=1500,
    #     messages=[
    #         {
    #             "role": "system",
    #             "content": """You are a helpful and thoughtful assistant. Your task is to reason through complex problems step by step.
    #                         For each user query, first, think carefully about the next best action. Then, decide on an action or function to call,
    #                         execute the action, observe the results, and use the observations to continue your reasoning.
    #                         Continue this process until you reach a final conclusion or answer the user's question.
    #                         If needed, explain your reasoning to the user as you proceed.""",
    #         }
    #     ],
    #     stream=False,
    #     mode=Mode.ReAct,
    #     tools=tools,
    # )

    # response = agent.chat()
    # print("ReAct response:")
    # print(f"{response}")
