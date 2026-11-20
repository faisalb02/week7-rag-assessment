# Task 3 – Citations and Hallucination Control

## 1. Objective

The objective of this task is to improve the reliability of the RAG system by implementing citation formatting, citation validation, faithfulness checking, prompt comparison, and API key protection.

## 2. Citation Formatting

Implemented citation formatting in `citation_formatter.py`.

Features:
- Each retrieved document chunk includes its source filename.
- Each chunk includes its page number.
- Formatted context helps the LLM identify the source of information.

Example:

[Source: leave_policy.txt, Page 1]

## 3. Citation Validation

Implemented citation validation in `citation_validator.py`.

The system uses regular expressions to extract citations from generated answers and checks whether each citation matches the retrieved document sources and page numbers.

Test Results:
- Total citations tested: 3
- Valid citations: 2
- Invalid citations: 1

The invalid citation was correctly identified.

## 4. Faithfulness Checking

Implemented faithfulness checking in `faithfulness.py`.

The system checks whether each answer claim is present in the provided context.

Test Results:
- Total claims tested: 5
- Supported claims: 5
- Unsupported claims: 0
- Faithfulness score: 100%

Note: The current implementation uses exact text matching. It does not perform semantic verification.

## 5. Prompt Comparison

Compared three prompt versions using 10 questions:
- 7 answerable questions
- 3 unanswerable questions

### Prompt Version 1 – Basic Prompt

Uses a basic prompt without strict context restrictions.

Results:
- All 10 questions received responses.
- Hallucinated answers: 0

### Prompt Version 2 – Only From Context

Instructs the LLM to answer only using the provided context and say "I don't know" when information is unavailable.

Results:
- 8 responses completed successfully.
- 2 responses were interrupted by Gemini API rate limits (429).
- Hallucinated answers: 0 among successfully evaluated unanswerable questions.

### Prompt Version 3 – Context + Citations

Instructs the LLM to answer only using the provided context, cite every factual statement, and say "I don't know" when information is unavailable.

Results:
- 1 question was answered successfully with citations.
- Remaining questions could not be completed because of Gemini API rate limits (429).
- Evaluation is incomplete.

### Prompt Comparison Summary

| Prompt Version | Hallucinated Answers | Evaluation Status |
|---|---:|---|
| Version 1 | 0 | Completed |
| Version 2 | 0 | Partially completed |
| Version 3 | Not fully evaluated | Incomplete |

Note: The evaluation was interrupted by Gemini API rate limits. Incomplete questions were not counted as successful evaluations.

## 6. FastAPI Integration

Implemented a FastAPI endpoint:

POST `/ask`

Features:
- Accepts a user question.
- Retrieves relevant document chunks.
- Generates an answer using the LLM.
- Returns answer and source information.
- Validates citations in the generated answer.
- Protects the endpoint using API key authentication.
- Returns an error when the API key is missing or invalid.
- Handles cases when relevant documents are not found.

## 7. Testing

The following tests were performed:

- Citation validation test
- Faithfulness test
- Prompt comparison test
- Gemini API connection test
- FastAPI endpoint test
- API key authentication test

## 8. Conclusion

Task 3 implements citation formatting, citation validation, faithfulness checking, prompt comparison, and a protected FastAPI endpoint.

Citation validation and faithfulness tests completed successfully. Prompt Version 1 completed, while Versions 2 and 3 were partially evaluated due to Gemini API rate limits.

The RAG system provides source information and validates citations to improve answer reliability.