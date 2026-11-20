from src.bm25_retriever import build_bm25_index, search_bm25
from src.vector_retriever import vector_search


def reciprocal_rank_fusion(bm25_results, vector_results, k=60):

    scores = {}
    documents = {}

    # BM25 rankings
    for result in bm25_results:

        key = (
            result["metadata"]["source"],
            result["text"]
        )

        scores[key] = scores.get(key, 0) + (
            1 / (k + result["rank"])
        )

        documents[key] = result

    # Vector rankings
    for rank, result in enumerate(vector_results, start=1):

        key = (
            result["metadata"]["source"],
            result["text"]
        )

        scores[key] = scores.get(key, 0) + (
            1 / (k + rank)
        )

        documents[key] = result

    # Sort by combined RRF score
    ranked_results = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    final_results = []

    for rank, (key, score) in enumerate(ranked_results, start=1):

        document = documents[key]

        final_results.append({
            "rank": rank,
            "rrf_score": score,
            "text": document["text"],
            "metadata": document["metadata"]
        })

    return final_results


def hybrid_search(
    question,
    top_k=3,
    department=None,
    min_year=None
):

    # BM25 retrieval with metadata filter
    bm25, chunks = build_bm25_index(
        department=department,
        min_year=min_year
    )

    bm25_results = search_bm25(
        question, bm25, chunks, top_k=top_k
    )

    # Vector retrieval with metadata filter
    vector_results = vector_search(
        question,
        k=top_k,
        department=department,
        min_year=min_year
    )

    return reciprocal_rank_fusion(
        bm25_results, vector_results
    )[:top_k]