import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RESULT_FILE = (
    PROJECT_ROOT / "Task4_Golden_Dataset_RAGAS"
    / "outputs" / "ragas_results.json"
)

OUTPUT_FILE = (
    PROJECT_ROOT / "Task4_Golden_Dataset_RAGAS"
    / "outputs" / "improvement_report.json"
)

with open(RESULT_FILE, "r", encoding="utf-8") as file:
    results = json.load(file)

metrics = [
    "faithfulness",
    "answer_relevancy",
    "context_precision",
    "context_recall"
]

before = {}

for metric in metrics:
    values = [
        item[metric]
        for item in results
        if isinstance(item.get(metric), (int, float))
    ]

    before[metric] = (
        sum(values) / len(values) if values else 0
    )

report = {
    "before_metrics": before,
    "target_faithfulness": 0.85,
    "faithfulness_target_met": before["faithfulness"] > 0.85,
    "fix_applied": (
        "Extract actual text from PDF and TXT source documents "
        "instead of reading PDF files as UTF-8 text."
    ),
    "note": (
        "These are current evaluation scores. "
        "A separate post-fix evaluation is required "
        "to calculate genuine after metrics."
    )
}

with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
    json.dump(report, file, indent=4)

print("\nIMPROVEMENT REPORT")
print(json.dumps(report, indent=4))
print("\nReport saved:", OUTPUT_FILE)