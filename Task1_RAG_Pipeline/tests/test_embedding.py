from src.document_loader import load_documents
from src.chunker import chunk_documents
from src.embedding import generate_embeddings


# Step 1: Load documents
documents = load_documents()

# Step 2: Create chunks
chunks = chunk_documents(documents)

# Step 3: Generate embeddings
chunks = generate_embeddings(chunks)

print("Total chunks:", len(chunks))

print("Embedding dimension:", len(chunks[0]["embedding"]))

print("First embedding:", chunks[0]["embedding"][:5])