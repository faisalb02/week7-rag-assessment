from src.hybrid_retriever import hybrid_search
from src.reranker import rerank_documents
from src.evaluation import questions


print("\n========== RERANKING EVALUATION ==========")

total_questions = 0
found_before = 0
found_after = 0

for item in questions[:10]:

    question = item["question"]
    expected_source = item["expected_source"]
    expected_text = item["expected_text"].lower()

    # Retrieve candidates (maximum 50)
    before_results = hybrid_search(question, top_k=50)

    # Identify the correct chunk using source and text
    correct_chunk = next(
        (
            result for result in before_results
            if result["metadata"]["source"] == expected_source
            and expected_text in result["text"].lower()
        ),
        None
    )

    # If correct chunk is not found
    if correct_chunk is None:

        print("\nQuestion:", question)
        print("Expected keyword:", expected_text)
        print("Available chunks from expected source:")

        for result in before_results:
            if result["metadata"]["source"] == expected_source:
                print(result["text"])

        print("Correct chunk: Not found in candidates")
        continue

    # Find exact chunk rank before reranking
    before_rank = next(
        rank
        for rank, result in enumerate(before_results, start=1)
        if result["text"] == correct_chunk["text"]
        and result["metadata"]["source"] == expected_source
    )

    # Cross-encoder reranking
    after_results = rerank_documents(
        question,
        before_results,
        top_k=5
    )

    # Find exact chunk rank after reranking
    after_rank = next(
        (
            rank
            for rank, result in enumerate(after_results, start=1)
            if result["text"] == correct_chunk["text"]
            and result["metadata"]["source"] == expected_source
        ),
        "Not in Top 5"
    )

    total_questions += 1
    found_before += 1

    if after_rank != "Not in Top 5":
        found_after += 1

    print("\nQuestion:", question)
    print("Correct Source:", expected_source)
    print("Candidates:", len(before_results))
    print("Before Reranking Rank:", before_rank)
    print("After Reranking Rank:", after_rank)
    print("------------------------------")


print("\n========== FINAL SUMMARY ==========")
print("Questions evaluated:", total_questions)
print("Correct chunks found before:", found_before)
print("Correct chunks in Top 5 after:", found_after)