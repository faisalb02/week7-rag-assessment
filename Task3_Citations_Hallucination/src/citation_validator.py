import re


def extract_citations(answer):

    pattern = r"\[Source: (.*?), Page (\d+)\]"

    citations = re.findall(pattern, answer)

    return [
        {
            "source": source,
            "page": int(page)
        }
        for source, page in citations
    ]


def validate_citations(answer, retrieved_chunks):

    citations = extract_citations(answer)

    valid_sources = []

    for chunk in retrieved_chunks:

        valid_sources.append({
            "source": chunk["metadata"]["source"],
            "page": chunk["metadata"]["page"]
        })

    results = []

    for citation in citations:

        if citation in valid_sources:

            results.append({
                "citation": citation,
                "status": "VALID"
            })

        else:

            results.append({
                "citation": citation,
                "status": "INVALID"
            })

    return results