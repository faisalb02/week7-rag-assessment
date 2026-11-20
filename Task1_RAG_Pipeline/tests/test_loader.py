from src.document_loader import load_documents


documents = load_documents()

print("Total documents:", len(documents))

for document in documents:

    print("Source:", document["metadata"]["source"])
    print("Page:", document["metadata"]["page"])
    print("Text:", document["text"][:100])
    print("----------------------")