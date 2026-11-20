from .embedding import model
from .indexer import client, COLLECTION_NAME


def retrieve_chunks(question, k=4):

    # Convert question into embedding
    question_embedding = model.encode(question).tolist()

    # Search relevant chunks in Qdrant
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=question_embedding,
        limit=k,
    )

    chunks = []

    for point in results.points:
        chunks.append({
            "text": point.payload["text"],
            "metadata": point.payload["metadata"],
            "score": point.score
        })

    return chunks