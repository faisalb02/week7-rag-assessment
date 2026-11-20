def format_context(chunks):

    formatted_context = []

    for chunk in chunks:

        text = chunk["text"]

        metadata = chunk["metadata"]

        source = metadata["source"]

        page = metadata["page"]

        formatted_chunk = (
            f"[Source: {source}, Page {page}]\n"
            f"{text}"
        )

        formatted_context.append(formatted_chunk)

    return "\n\n".join(formatted_context)