import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")


def fit_context(chunks, budget):

    selected_chunks = []
    total_tokens = 0

    for chunk in chunks:

        chunk_tokens = len(
            encoding.encode(chunk["text"])
        )

        if total_tokens + chunk_tokens <= budget:
            selected_chunks.append(chunk)
            total_tokens += chunk_tokens
        else:
            break

    return selected_chunks