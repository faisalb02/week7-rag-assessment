from pathlib import Path

from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

from src.metadata_filter import add_metadata, filter_documents

# Main project folder
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to Task 1 Qdrant database
client = QdrantClient(
    path=str(PROJECT_ROOT / "Task1_RAG_Pipeline" / "qdrant_db")
)

COLLECTION_NAME = "company_documents"


def vector_search(question, k=3, department=None, min_year=None):

    # Convert question into embedding
    query_embedding = model.encode(question).tolist()

    # Search similar chunks
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_embedding,
        limit=100,
        with_payload=True
    )

    # Convert Qdrant results into chunk format
    chunks = []

    for point in results.points:
        chunks.append({
            "text": point.payload["text"],
            "metadata": point.payload["metadata"]
        })

    # Add department and year metadata
    chunks = add_metadata(chunks)

    # Apply metadata filters
    chunks = filter_documents(
        chunks,
        department=department,
        min_year=min_year
    )

    # Return only top-k matching results
    return chunks[:k]