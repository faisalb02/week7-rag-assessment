from src.bm25_retriever import (
    build_bm25_index,
    search_bm25
)

from src.vector_retriever import vector_search
from src.hybrid_retriever import hybrid_search


question = "How many casual leaves per year?"


# -------------------------
# BM25 RETRIEVAL
# -------------------------

bm25, chunks = build_bm25_index()

bm25_results = search_bm25(
    question,
    bm25,
    chunks,
    top_k=3
)

print("Question:", question)
print("\n========== BM25 TOP 3 RESULTS ==========")

for result in bm25_results:
    print("\nRank:", result["rank"])
    print("Score:", round(result["score"], 4))
    print("Source:", result["metadata"]["source"])
    print("Text:", result["text"][:150])
    print("--------------------")


# -------------------------
# VECTOR RETRIEVAL
# -------------------------

vector_results = vector_search(question, k=3)

print("\n========== VECTOR TOP 3 RESULTS ==========")

for rank, result in enumerate(vector_results, start=1):
    print("\nRank:", rank)
    print("Source:", result["metadata"]["source"])
    print("Department:", result["metadata"]["department"])
    print("Year:", result["metadata"]["year"])
    print("Text:", result["text"][:150])
    print("--------------------")


# -------------------------
# HYBRID RETRIEVAL
# -------------------------

hybrid_results = hybrid_search(
    question,
    top_k=3
)

print("\n========== HYBRID TOP 3 RESULTS ==========")

for result in hybrid_results:
    print("\nRank:", result["rank"])
    print("RRF Score:", round(result["rrf_score"], 5))
    print("Source:", result["metadata"]["source"])
    print("Text:", result["text"][:150])
    print("--------------------")


# -------------------------
# METADATA FILTERING
# -------------------------

filtered_results = hybrid_search(
    question,
    top_k=3,
    department="HR",
    min_year=2026
)

print("\n========== HR + CURRENT YEAR FILTER ==========")

for result in filtered_results:
    print("Source:", result["metadata"]["source"])
    print("Department:", result["metadata"]["department"])
    print("Year:", result["metadata"]["year"])
    print("--------------------")