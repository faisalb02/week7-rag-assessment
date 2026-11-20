from pathlib import Path
from pypdf import PdfReader


DATA_DIR = Path(__file__).parent.parent / "data" / "documents"


def load_documents():

    documents = []

    for file_path in DATA_DIR.iterdir():

        if file_path.suffix == ".txt":

            text = file_path.read_text(encoding="utf-8")

            documents.append({
                "text": text,
                "metadata": {
                    "source": file_path.name,
                    "page": 1
                }
            })

        elif file_path.suffix == ".pdf":

            reader = PdfReader(file_path)

            for page_number, page in enumerate(reader.pages, start=1):

                text = page.extract_text() or ""

                documents.append({
                    "text": text,
                    "metadata": {
                        "source": file_path.name,
                        "page": page_number
                    }
                })

    return documents