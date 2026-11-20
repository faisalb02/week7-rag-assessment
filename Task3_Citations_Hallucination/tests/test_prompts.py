from pathlib import Path
from pypdf import PdfReader

from src.prompt_comparison import run_comparison


# Task 1 documents folder
DATA_DIR = (
    Path(__file__).parent.parent.parent
    / "Task1_RAG_Pipeline"
    / "data"
    / "documents"
)


def load_context():

    all_chunks = []

    for file_path in DATA_DIR.iterdir():

        if file_path.suffix == ".txt":

            text = file_path.read_text(encoding="utf-8")

            all_chunks.append(
                f"[Source: {file_path.name}, Page 1]\n{text}"
            )

        elif file_path.suffix == ".pdf":

            reader = PdfReader(file_path)

            for page_number, page in enumerate(
                reader.pages, start=1
            ):

                text = page.extract_text() or ""

                all_chunks.append(
                    f"[Source: {file_path.name}, Page {page_number}]\n{text}"
                )

    return "\n\n".join(all_chunks)


if __name__ == "__main__":

    context = load_context()

    print("Documents loaded successfully!")
    print("Context length:", len(context))

    run_comparison(context,versions=[3])