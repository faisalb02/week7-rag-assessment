import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RESULT_FILE = (
    PROJECT_ROOT / "Task4_Golden_Dataset_RAGAS"
    / "outputs" / "ragas_results.json"
)

OUTPUT_FILE = (
    PROJECT_ROOT / "Task4_Golden_Dataset_RAGAS"
    / "outputs" / "failure_analysis.json"
)

with open(RESULT_FILE, "r", encoding="utf-8") as file:
    results = json.load(file)

# Find the 3 lowest faithfulness scores
worst_questions = sorted(
    results,
    key=lambda item: item.get("faithfulness", 0)
)[:3]

failures = []

for item in worst_questions:

    precision = item.get("context_precision", 0)
    recall = item.get("context_recall", 0)

    if precision < 0.85 or recall < 0.85:
        failure_type = "Retrieval Failure"
    else:
        failure_type = "Generation Failure"

    failures.append({
        "question": item.get("user_input", ""),
        "faithfulness": item.get("faithfulness", 0),
        "failure_type": failure_type
    })

print("\nTHREE WORST QUESTIONS")

for failure in failures:
    print("\nQuestion:", failure["question"])
    print("Faithfulness:", failure["faithfulness"])
    print("Failure:", failure["failure_type"])

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(failures, file, indent=4)

print("\nFailure analysis saved:", OUTPUT_FILE)