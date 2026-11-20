import os
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

from src.citation_formatter import format_context
from src.citation_validator import validate_citations


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

DB_PATH = (
    PROJECT_ROOT
    / "Task1_RAG_Pipeline"
    / "qdrant_db"
)

COLLECTION_NAME = "company_documents"

# Load embedding model
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# Connect to Task 1 Qdrant database
qdrant_client = QdrantClient(
    path=str(DB_PATH)
)

# OpenRouter client
llm_client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "openrouter/free"
)

RAG_API_KEY = os.getenv("RAG_API_KEY")


# Retrieve relevant chunks
def retrieve_chunks(question, k=4):

    question_embedding = embedding_model.encode(
        question
    ).tolist()

    results = qdrant_client.query_points(
        collection_name=COLLECTION_NAME,
        query=question_embedding,
        limit=k
    )

    chunks = []

    for point in results.points:

        chunks.append({
            "text": point.payload["text"],
            "metadata": point.payload["metadata"],
            "score": point.score
        })

    return chunks


app = FastAPI(title="Task 3 Citation API")


class AskRequest(BaseModel):
    question: str


@app.post("/ask")
def ask_question(
    request: AskRequest,
    x_api_key: str = Header(None)
):

    # Check API key configuration
    if not RAG_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="RAG_API_KEY is not configured"
        )

    # Check API key
    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail="API key missing"
        )

    if x_api_key != RAG_API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Invalid API key"
        )

    # Retrieve chunks
    chunks = retrieve_chunks(
        request.question,
        k=4
    )

    # Check search results
    if not chunks or chunks[0]["score"] < 0.35:
        raise HTTPException(
            status_code=404,
            detail="No relevant documents found"
        )

    # Format context with source citations
    context = format_context(chunks)

    prompt = f"""
Answer ONLY using the provided context.
Do not use outside knowledge.

Cite every factual statement using:
[Source: filename, Page number]

If the answer is not available, say:
I don't have information on that.

Context:
{context}

Question:
{request.question}

Answer:
"""

    # Get LLM response
    response = llm_client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    answer = response.choices[0].message.content or ""

    # Validate citations
    citation_results = validate_citations(
        answer,
        chunks
    )

    # Prepare sources
    sources = [
        {
            "source": chunk["metadata"]["source"],
            "page": chunk["metadata"]["page"]
        }
        for chunk in chunks
    ]

    return {
        "answer": answer,
        "sources": sources,
        "citation_validation": citation_results
    }