from src.retriever import retrieve_chunks

question = "How many casual leaves per year?"

results = retrieve_chunks(question, k=4)

for chunk in results:
    print("Score:", chunk["score"])
    print("Source:", chunk["metadata"]["source"])
    print("Text:", chunk["text"])
    print("-------------------")