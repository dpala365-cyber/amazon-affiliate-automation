import os
from openai import OpenAI

with open(os.path.expanduser("~/.openai_key"), "r") as f:
    api_key = f.read().strip()

client = OpenAI(api_key=api_key)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello from PythonAnywhere!"}]
)

print(response.choices[0].message.content)
