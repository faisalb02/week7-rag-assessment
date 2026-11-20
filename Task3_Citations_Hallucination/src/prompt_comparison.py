import time
import os
from pathlib import Path

from openai import OpenAI
from dotenv import load_dotenv


# Load root project .env file
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")


# Gemini API configuration
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


# 10 questions: 7 answerable + 3 unanswerable
questions = [
    {"question": "How many casual leaves per year?", "answerable": True},
    {"question": "How many sick leaves are available?", "answerable": True},
    {"question": "What are the company working hours?", "answerable": True},
    {"question": "What is the work from home policy?", "answerable": True},
    {"question": "How many public holidays are provided?", "answerable": True},
    {"question": "Does the company provide medical insurance?", "answerable": True},
    {"question": "What healthcare benefits are provided?", "answerable": True},
    {"question": "What is the company's annual profit?", "answerable": False},
    {"question": "Who is the company CEO?", "answerable": False},
    {"question": "What is the company's annual revenue?", "answerable": False}
]


def create_prompt(question, context, version):

    if version == 1:
        return f"""
Answer the following question.

Context:
{context}

Question:
{question}
"""

    elif version == 2:
        return f"""
Answer ONLY using the provided context.
If the answer is not available, say I don't know.

Context:
{context}

Question:
{question}
"""

    else:
        return f"""
Answer ONLY using the provided context.
Do not use outside knowledge.

Cite every factual statement using:
[Source: filename, Page number]

If the answer is not available in the context,
say I don't know.

Context:
{context}

Question:
{question}
"""


def ask_model(prompt):

    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0
            )

            return response.choices[0].message.content or ""

        except Exception as error:
            print(f"API error: {error}")

            if attempt == 2:
                print("Maximum retries reached.")
                return ""

            print("Retrying in 5 seconds...")
            time.sleep(5)


def is_refusal(answer):

    refusal_phrases = [
        "i don't know",
        "i do not know",
        "no information",
        "not mentioned",
        "not available",
        "does not contain",
        "there is no information",
        "not provided",
        "cannot be found"
    ]

    return any(
        phrase in answer.lower()
        for phrase in refusal_phrases
    )


def run_comparison(context, versions=[1, 2, 3]):

    for version in versions:

        hallucinations = 0

        print(f"\nPROMPT VERSION {version}")

        for item in questions:

            question = item["question"]

            prompt = create_prompt(
                question,
                context,
                version
            )

            answer = ask_model(prompt)

            if not item["answerable"]:
                if answer and not is_refusal(answer):
                    hallucinations += 1

            print("\nQuestion:", question)
            print("Answer:", answer)

        print("\nHallucinated answers:", hallucinations)