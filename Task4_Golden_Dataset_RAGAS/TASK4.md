Task 4 – Golden Dataset and RAGAS

1. Golden Dataset

Created "golden.jsonl" with 15 questions:

- 8 Simple questions
- 4 Multi-chunk questions
- 3 Unanswerable questions

Each record contains question, answer, source and page information.

2. RAGAS Evaluation

Evaluated the dataset using:

- Faithfulness
- Answer Relevancy
- Context Precision
- Context Recall

3. Before, After and Latest Results

Metric| Before| After| Latest Run
Faithfulness| 0.8667| 0.7667| 0.5385
Answer Relevancy| 0.6331| 0.6285| 0.4245
Context Precision| 0.9333| 0.8889| 0.8583
Context Recall| 1.0000| 1.0000| 1.0000

The latest evaluation completed and generated RAGAS scores. Some evaluation jobs encountered API rate limits and timeout errors. The latest faithfulness score did not meet the target of above 0.85. Further retrieval and generation improvements are required.

4. Failure Analysis

Three low-performing questions were classified:

1. Annual profit – Retrieval failure.
2. Annual revenue – Generation failure.
3. Casual leave question – Generation failure (as classified by the failure analysis script).

5. Improvement Applied

Improved source-document text extraction by extracting actual content from PDF and TXT files instead of treating PDF files as UTF-8 text.

6. Business Summary

The golden dataset was created to measure the quality of the company's RAG question-answering system. RAGAS evaluation measured answer faithfulness, relevance, context precision and context recall.

Context recall remained strong at 1.00, meaning the expected information was available in the evaluation context. However, the latest faithfulness score was 0.5385, which is below the target of above 0.85.

The failure analysis identified retrieval and generation issues in three questions. Source-document text extraction was improved. Some evaluation jobs also encountered API rate limits and timeout errors. Further testing, prompt tuning and retrieval improvements are needed to achieve the target faithfulness score consistently.

7. Output Files

- "data/golden.jsonl"
- "outputs/ragas_results.json"
- "outputs/failure_analysis.json"
- "outputs/improvement_report.json"