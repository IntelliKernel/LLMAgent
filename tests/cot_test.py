from openai import OpenAI

client = OpenAI()
prompt = """
问题：假设有5个朋友，他们各自带了一个苹果到聚会上，并决定分享苹果。每个人把苹果切成了8块，然后均匀分给了在场的每个人。每个人最终得到了多少块苹果？

请逐步解释您的推理过程，并得出最终答案。
"""

response = client.chat.completions.create(
    model="deepseek-chat",  # 或者使用 "gpt-3.5-turbo"
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ],
    max_tokens=1500,
    temperature=0.5,
    stream=True,
)

for chunk in response:
    print(chunk.choices[0].delta.content, end="", flush=True)
