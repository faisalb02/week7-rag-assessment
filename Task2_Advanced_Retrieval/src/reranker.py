from sentence_transformers import CrossEncoder
from src.hybrid_retriever import hybrid_search

# Load Cross-Encoder model
reranker_model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank_documents(question, candidates, top_k=5):

    # Question and document pairs
    pairs = [
        [question, document["text"]]
        for document in candidates
    ]

    # Calculate relevance scores
    scores = reranker_model.predict(pairs)

    # Add reranking scores
    for document, score in zip(candidates, scores):
        document["rerank_score"] = float(score)

    # Sort by highest score
    reranked_results = sorted(
        candidates,
        key=lambda document: document["rerank_score"],
        reverse=True
    )

    # Return best 5 documents
    return reranked_results[:top_k]


def hybrid_rerank_search(question):

    # First retrieve top 50 using Hybrid Search
    candidates = hybrid_search(question, top_k=50)

    # Then rerank and return top 5
    return rerank_documents(
        question,
        candidates,
        top_k=5
    )