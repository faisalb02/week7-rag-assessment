Task 2 – Advanced Retrieval Report

1. BM25, Vector and Hybrid Retrieval

Created 12 evaluation questions:

- 6 exact-term questions
- 6 meaning-based questions

Hit@3 results:

- BM25: 10/12 (83.33%)
- Vector: 12/12 (100%)
- Hybrid: 12/12 (100%)

2. Reciprocal Rank Fusion (RRF)

Implemented Reciprocal Rank Fusion using the formula:

"1 / (60 + rank)"

Combined BM25 and vector retrieval results using RRF to produce hybrid rankings.

Compared BM25, vector and hybrid retrieval performance using Hit@3.

3. Cross-Encoder Reranking

Implemented a Cross-Encoder reranker to rerank hybrid retrieval candidates.

Evaluation results:

- Questions evaluated: 10
- Correct chunks found before reranking: 10/10
- Correct chunks placed in Top 5 after reranking: 10/10
- Hybrid retrieval returned 22 candidate records in the test.

Note: The reranker requests up to 50 candidates, but only 22 candidate records were returned by the current hybrid retrieval results. The Cross-Encoder reranked the available candidates.

4. Query Rewriting

Implemented query rewriting with three alternative phrasings for each original question. The results were merged using RRF.

Comparison results:

Metric| Original Query| Rewritten Query
Hit@3| 12/12 (100%)| 12/12 (100%)
Latency| 0.435 seconds| 1.541 seconds

Query rewriting did not improve Hit@3 and increased retrieval latency because multiple queries were processed.

5. Metadata Filtering

Implemented metadata filtering based on:

- Department
- Year

Tested department filtering and year-based filtering.

Demonstrated that the outdated 2024 leave policy was removed when filtering for documents from 2026 onwards. Only the 2026 leave policy remained in the answer context.

Note: The outdated-document removal demonstration used synthetic test documents. The original company documents do not contain verified year metadata. Year assignments for the original documents are demonstration assumptions, not verified publication years.

Conclusion

BM25, vector retrieval, hybrid search using RRF, Cross-Encoder reranking, query rewriting and metadata filtering were implemented and tested.

Hybrid retrieval achieved 100% Hit@3. Cross-Encoder reranking successfully placed all 10 evaluated correct chunks within the Top 5.

Query rewriting maintained the same Hit@3 score but increased latency. Metadata filtering successfully demonstrated the removal of an outdated document using synthetic test data.