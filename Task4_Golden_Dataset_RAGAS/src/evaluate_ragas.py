import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall
)
from ragas.run_config import RunConfig
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env")

# Import only Task 1 retrieval function
from Task1_RAG_Pipeline.src.retriever import retrieve_chunks


DATA_FILE = (
    PROJECT_ROOT / "Task4_Golden_Dataset_RAGAS"
    / "data" / "golden.jsonl"
)

OUTPUT_DIR = (
    PROJECT_ROOT / "Task4_Golden_Dataset_RAGAS"
    / "outputs"
)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# OpenRouter configuration
# Configure Gemini LLM
api_key = os.getenv("ZAI_API_KEY")

if not api_key:
    raise ValueError("ZAI_API_KEY missing in .env")

llm = ChatOpenAI(
    model=os.getenv("ZAI_MODEL", "glm-4.7-flash"),
    api_key=api_key,
    base_url="https://api.z.ai/api/paas/v4",
    temperature=0,
    max_retries=2
)

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

answer_relevancy.strictness = 1


# Load golden dataset
with open(DATA_FILE, "r", encoding="utf-8") as file:
    golden_data = [
        json.loads(line)
        for line in file
        if line.strip()
    ]

questions = []
answers = []
ground_truths = []
contexts = []

print("Preparing RAGAS dataset...")

for index, item in enumerate(golden_data, start=1):
    question = item["question"]

    print(f"Processing question {index}/{len(golden_data)}")

    # Retrieve actual chunks from Task 1
    chunks = retrieve_chunks(question, k=4)

    context_texts = [
        chunk["text"]
        for chunk in chunks
        if isinstance(chunk, dict) and chunk.get("text")
    ]

    if not context_texts:
        context_texts = ["No relevant context available."]

    # Generate answer using OpenRouter
    prompt = f"""
    Answer the question using only the context below.
    If the answer is not available, say:
    "The information is not available in the provided documents."

    Context:
    {" ".join(context_texts)}

    Question:
    {question}

    Answer:
    """

    try:
        response = llm.invoke(prompt)
        generated_answer = response.content

        if not generated_answer:
            generated_answer = "No answer generated."

    except Exception as error:
        print(f"Answer generation failed: {error}")
        generated_answer = "Unable to generate answer."

    questions.append(question)
    answers.append(generated_answer)
    ground_truths.append(item["answer"])
    contexts.append(context_texts)


print(f"\nDataset prepared: {len(questions)} questions")

dataset = Dataset.from_dict({
    "question": questions,
    "answer": answers,
    "ground_truth": ground_truths,
    "contexts": contexts
})


# Run RAGAS evaluation
print("\nStarting RAGAS evaluation...")

result = evaluate(
    dataset=dataset,
    metrics=[
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall
    ],
    llm=llm,
    embeddings=embeddings,
    run_config=RunConfig(max_workers=1)
)

print("\nRAGAS RESULTS")
print(result)


# Save results
results_file = OUTPUT_DIR / "ragas_results.json"

results_data = json.loads(
    result.to_pandas().to_json(orient="records")
)

with open(results_file, "w", encoding="utf-8") as file:
    json.dump(
        results_data,
        file,
        indent=4,
        ensure_ascii=False
    )

print("\nResults saved successfully!")
print("Saved at:", results_file)