def rewrite_query(question):

    rewrites = [
        question,

        f"What is the company policy regarding {question}",

        f"Explain the rules and guidelines for {question}",

        f"What information is available about {question}"
    ]

    return rewrites


import time

from src.hybrid_retriever import hybrid_search


def rewritten_hybrid_search(question, top_k=3):

    start_time = time.time()

    # Original + 3 rewritten questions
    queries = rewrite_query(question)

    all_rankings = []

    # Search for all 4 questions
    for query in queries:

        results = hybrid_search(query, top_k=top_k)

        all_rankings.append(results)

    # Combine results using RRF
    scores = {}
    documents = {}

    for ranking in all_rankings:

        for rank, result in enumerate(ranking, start=1):

            key = (
                result["metadata"]["source"],
                result["text"]
            )

            scores[key] = scores.get(key, 0) + (
                1 / (60 + rank)
            )

            documents[key] = result

    # Sort by RRF score
    ranked_results = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True
    )

    final_results = []

    for rank, (key, score) in enumerate(
        ranked_results[:top_k], start=1
    ):

        document = documents[key]

        final_results.append({
            "rank": rank,
            "rrf_score": score,
            "text": document["text"],
            "metadata": document["metadata"]
        })

    latency = time.time() - start_time

    return final_results, latency