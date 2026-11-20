from src.document_loader import load_documents
from src.chunker import chunk_documents
from src.embedding import generate_embeddings
from src.indexer import index_chunks, client, COLLECTION_NAME


# Step 1: Load documents
documents = load_documents()

# Step 2: Create chunks
chunks = chunk_documents(documents)

# Step 3: Generate embeddings
chunks = generate_embeddings(chunks)

# Step 4: First indexing
print("\nFIRST RUN")
index_chunks(chunks)

first_count = client.count(
    collection_name=COLLECTION_NAME
).count

print("Points after first run:", first_count)


# Step 5: Second indexing
print("\nSECOND RUN")
index_chunks(chunks)

second_count = client.count(
    collection_name=COLLECTION_NAME
).count

print("Points after second run:", second_count)


# Step 6: Verify idempotency
if first_count == second_count:
    print("IDEMPOTENCY TEST PASSED")
else:
    print("IDEMPOTENCY TEST FAILED")