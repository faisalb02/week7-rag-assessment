import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from .retriever import retrieve_chunks

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY missing in .env")

llm_client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)

MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
SCORE_THRESHOLD = 0.35


def answer(question, k=4):
    chunks = retrieve_chunks(question, k)

    if not chunks or chunks[0]["score"] < SCORE_THRESHOLD:
        return "I don't have information on that"

    context = "\n".join(chunk["text"] for chunk in chunks)

    prompt = f"""
Answer ONLY using the context below.
If the answer is not present, say:
I don't have information on that.

Context:
{context}

Question:
{question}

Answer:
"""

    response = llm_client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content or ""