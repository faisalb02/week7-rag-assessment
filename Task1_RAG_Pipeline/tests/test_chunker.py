from src.document_loader import load_documents
from src.chunker import chunk_documents


# Load original documents
documents = load_documents()

# Split documents into chunks
chunks = chunk_documents(documents)

print("Total documents:", len(documents))

print("Total chunks:", len(chunks))

for chunk in chunks[:5]:

    print("Source:", chunk["metadata"]["source"])

    print("Chunk text:", chunk["text"])

    print("----------------------")