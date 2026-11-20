from pathlib import Path

from src.faithfulness import check_faithfulness
from test_prompts import load_context


# Load actual company documents
context = load_context()


# Manually split 5 answers into individual claims
manual_answers = [
    "Employees are eligible for 12 casual leaves per year.",
    "Employees are eligible for 10 sick leaves per year.",
    "The standard working hours are 10:00 AM to 6:00 PM.",
    "Employees can request work from home with manager approval.",
    "The company provides 12 public holidays every year."
]


print("MANUAL FAITHFULNESS CHECK")

results = check_faithfulness(manual_answers, context)

supported = 0
unsupported = 0

for result in results:

    print("\nClaim:", result["claim"])
    print("Status:", result["status"])

    if result["status"] == "SUPPORTED":
        supported += 1
    else:
        unsupported += 1


print("\nTOTAL CLAIMS:", len(results))
print("SUPPORTED:", supported)
print("UNSUPPORTED:", unsupported)