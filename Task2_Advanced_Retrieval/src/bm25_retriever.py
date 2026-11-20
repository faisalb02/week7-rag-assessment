import re
import sys
from pathlib import Path

from rank_bm25 import BM25Okapi

# Find the main project folder
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

# Reuse Task 1 document loading and chunking
from Task1_RAG_Pipeline.src.document_loader import load_documents
from Task1_RAG_Pipeline.src.chunker import chunk_documents
from src.metadata_filter import add_metadata, filter_documents


def tokenize(text):
    return re.findall(r"\b\w+\b", text.lower())


def build_bm25_index(department=None, min_year=None):

    documents = load_documents()
    chunks = chunk_documents(documents)

    chunks = add_metadata(chunks)

    # Apply department and year filters
    chunks = filter_documents(
        chunks,
        department=department,
        min_year=min_year
    )

    tokenized_chunks = [
        tokenize(chunk["text"])
        for chunk in chunks
    ]

    bm25 = BM25Okapi(tokenized_chunks)

    return bm25, chunks


def search_bm25(query, bm25, chunks, top_k=3):

    tokenized_query = tokenize(query)

    scores = bm25.get_scores(tokenized_query)

    ranked_indices = sorted(
        range(len(scores)),
        key=lambda index: scores[index],
        reverse=True
    )[:top_k]

    results = []

    for rank, index in enumerate(ranked_indices, start=1):

        results.append({
            "rank": rank,
            "score": float(scores[index]),
            "text": chunks[index]["text"],
            "metadata": chunks[index]["metadata"]
        })

    return results