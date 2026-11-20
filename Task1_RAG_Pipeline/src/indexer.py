import uuid
from pathlib import Path

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)

COLLECTION_NAME = "company_documents"

DB_PATH = Path(__file__).resolve().parents[1] / "qdrant_db"

client = QdrantClient(path=str(DB_PATH))


def index_chunks(chunks):

    # Create collection only if it does not exist
    if not client.collection_exists(COLLECTION_NAME):

        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )

    points = []

    for chunk in chunks:

        metadata = chunk["metadata"]

        # Generate stable ID
        unique_text = (
            metadata.get("source", "")
            + str(metadata.get("page", ""))
            + chunk["text"]
        )

        point_id = str(
            uuid.uuid5(uuid.NAMESPACE_DNS, unique_text)
        )

        point = PointStruct(
            id=point_id,
            vector=chunk["embedding"],
            payload={
                "text": chunk["text"],
                "metadata": metadata
            }
        )

        points.append(point)

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print("Successfully indexed:", len(points))

    return len(points)