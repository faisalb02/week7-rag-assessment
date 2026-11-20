import time

from src.evaluation import questions
from src.hybrid_retriever import hybrid_search
from src.query_rewriter import rewritten_hybrid_search


def run_comparison():

    original_hits = 0
    rewritten_hits = 0

    original_time = 0
    rewritten_time = 0

    for item in questions:

        question = item["question"]
        expected_source = item["expected_source"]

        print("\nQuestion:", question)

        # Without query rewriting
        start = time.time()

        original_results = hybrid_search(
            question,
            top_k=3
        )

        original_time += time.time() - start

        original_hit = any(
            result["metadata"]["source"] == expected_source
            for result in original_results
        )

        if original_hit:
            original_hits += 1

        # With query rewriting
        rewritten_results, latency = rewritten_hybrid_search(
            question,
            top_k=3
        )

        rewritten_time += latency

        rewritten_hit = any(
            result["metadata"]["source"] == expected_source
            for result in rewritten_results
        )

        if rewritten_hit:
            rewritten_hits += 1

        print("Original Search:", "HIT" if original_hit else "MISS")
        print("Rewritten Search:", "HIT" if rewritten_hit else "MISS")

    total = len(questions)

    print("\n========== QUERY REWRITING RESULTS ==========")

    print("Without Rewriting:", original_hits, "/", total)
    print("With Rewriting:", rewritten_hits, "/", total)

    print("Without Rewriting Latency:", round(original_time, 3), "seconds")
    print("With Rewriting Latency:", round(rewritten_time, 3), "seconds")


if __name__ == "__main__":
    run_comparison()