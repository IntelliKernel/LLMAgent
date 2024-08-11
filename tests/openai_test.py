from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"},
    ],
    max_tokens=100,
    temperature=0.6,
    top_p=0.9,
    stream=False,
)

print(response.choices[0].message.content)
