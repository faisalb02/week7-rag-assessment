from src.retriever import retrieve_chunks
from src.context_manager import fit_context
import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")

question = "How many casual leaves per year?"

for k in [2, 5, 10]:

    chunks = retrieve_chunks(question, k=k)

    selected_chunks = fit_context(chunks, budget=3000)

    context = "\n".join(
        chunk["text"] for chunk in selected_chunks
    )

    token_count = len(encoding.encode(context))

    print("\nk =", k)
    print("Retrieved chunks:", len(chunks))
    print("Selected chunks:", len(selected_chunks))
    print("Total context tokens:", token_count)
    print("Within budget:", token_count <= 3000)