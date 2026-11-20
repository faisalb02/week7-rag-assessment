def chunk_documents(documents, chunk_size=500, overlap=100):

    chunks = []

    for document in documents:

        text = document["text"]

        metadata = document["metadata"]

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk_text = text[start:end]

            if chunk_text.strip():

                chunks.append({
                    "text": chunk_text,
                    "metadata": metadata.copy()
                })

            start += chunk_size - overlap

    return chunks