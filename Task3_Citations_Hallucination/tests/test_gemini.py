import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv("../.env")

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model=os.getenv("GEMINI_MODEL", "gemini-4-hydrogen"),
    messages=[
        {
            "role": "user",
            "content": "Say Gemini API working successfully"
        }
    ]
)

print(response.choices[0].message.content)