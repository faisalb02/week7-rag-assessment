import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FILE = (
    PROJECT_ROOT / "Task4_Golden_Dataset_RAGAS"
    / "data" / "golden.jsonl"
)

def test_golden_dataset():

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = [
            json.loads(line)
            for line in file
            if line.strip()
        ]

    assert len(data) == 15

    simple = [
        item for item in data
        if item["type"] == "simple"
    ]

    multi_chunk = [
        item for item in data
        if item["type"] == "multi_chunk"
    ]

    unanswerable = [
        item for item in data
        if item["type"] == "unanswerable"
    ]

    assert len(simple) == 8
    assert len(multi_chunk) == 4
    assert len(unanswerable) == 3

    for item in data:
        assert item["question"]
        assert "answer" in item
        assert "source" in item
        assert "page" in item

    print("Golden dataset tests passed!")


if __name__ == "__main__":
    test_golden_dataset()