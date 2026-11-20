from src.citation_formatter import format_context
from src.citation_validator import (
    extract_citations,
    validate_citations
)

# Sample retrieved chunks
retrieved_chunks = [
    {
        "text": "Employees receive 12 casual leaves per year.",
        "metadata": {
            "source": "leave_policy.txt",
            "page": 1
        }
    },
    {
        "text": "Employees receive 10 sick leaves per year.",
        "metadata": {
            "source": "employee_benefits.pdf",
            "page": 1
        }
    }
]

# Format context
context = format_context(retrieved_chunks)

print("FORMATTED CONTEXT:")
print(context)

# AI answer with citations
answer = """
Employees receive 12 casual leaves per year.
[Source: leave_policy.txt, Page 1]

Employees receive 10 sick leaves per year.
[Source: employee_benefits.pdf, Page 1]

Employees receive 30 vacation leaves.
[Source: vacation_policy.pdf, Page 5]
"""

# Extract citations
citations = extract_citations(answer)

print("\nEXTRACTED CITATIONS:")
print(citations)

# Validate citations
results = validate_citations(
    answer,
    retrieved_chunks
)

print("\nCITATION VALIDATION:")

for result in results:
    print(result)

print("\nTOTAL CITATIONS:", len(results))
print(
    "VALID:",
    sum(r["status"] == "VALID" for r in results)
)
print(
    "INVALID:",
    sum(r["status"] == "INVALID" for r in results)
)