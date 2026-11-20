from src.bm25_retriever import build_bm25_index, search_bm25
from src.vector_retriever import vector_search
from src.hybrid_retriever import hybrid_search


questions = [

    {
        "question": "How many casual leaves per year?",
        "expected_source": "leave_policy.txt",
        "expected_text": "12 casual leaves"
    },
    {
        "question": "How many sick leaves are available?",
        "expected_source": "leave_policy.txt",
        "expected_text": "10 sick leaves"
    },
    {
        "question": "What are the company working hours?",
        "expected_source": "attendance_policy.txt",
        "expected_text": "working hours"
    },
    {
        "question": "What is the work from home policy?",
        "expected_source": "work_from_home.txt",
        "expected_text": "work from home"
    },
    {
        "question": "How many public holidays are provided?",
        "expected_source": "holiday_policy.txt",
        "expected_text": "12 public holidays"
    },
    {
        "question": "Does the company provide medical insurance?",
        "expected_source": "medical_policy.txt",
        "expected_text": "medical insurance"
    },
    {
    "question": "How much time off can an employee take for personal reasons?",
    "expected_source": "leave_policy.txt",
    "expected_text": "casual leaves"
    },
    {
        "question": "When should staff members be present at work?",
        "expected_source": "attendance_policy.txt",
        "expected_text": "working hours"
    },
    {
        "question": "Can employees perform their duties from their homes?",
        "expected_source": "work_from_home.txt",
        "expected_text": "work from home"
    },
    {
        "question": "What days off does the company give during the year?",
        "expected_source": "holiday_policy.txt",
        "expected_text": "public holidays"
    },
    {
        "question": "What healthcare coverage is available to workers?",
        "expected_source": "medical_policy.txt",
        "expected_text": "medical insurance"
    },
    {
        "question": "What financial benefits do employees receive?",
        "expected_source": "employee_benefits.pdf",
        "expected_text": "employee benefits"
    }
]



def calculate_hit(results, expected_source, method):

    found = any(
        result["metadata"]["source"] == expected_source
        for result in results
    )

    if found:
        print(method, "HIT")
        return 1

    else:
        print(method, "MISS")
        return 0


def run_evaluation():

    bm25, chunks = build_bm25_index()

    bm25_hits = 0
    vector_hits = 0
    hybrid_hits = 0

    for item in questions:

        question = item["question"]
        expected_source = item["expected_source"]

        print("\nQuestion:", question)

        # BM25
        bm25_results = search_bm25(
            question, bm25, chunks, top_k=3
        )

        bm25_hits += calculate_hit(
            bm25_results, expected_source, "BM25"
        )

        # Vector
        vector_results = vector_search(question, k=3)

        vector_formatted = [
            {
                "metadata": result.payload["metadata"]
            }
            for result in vector_results
        ]

        vector_hits += calculate_hit(
            vector_formatted, expected_source, "Vector"
        )

        # Hybrid
        hybrid_results = hybrid_search(question, top_k=3)

        hybrid_hits += calculate_hit(
            hybrid_results, expected_source, "Hybrid"
        )

    print("\n========== FINAL HIT@3 RESULTS ==========")

    print("BM25:", bm25_hits, "/", len(questions))
    print("Vector:", vector_hits, "/", len(questions))
    print("Hybrid:", hybrid_hits, "/", len(questions))


if __name__ == "__main__":
    run_evaluation()