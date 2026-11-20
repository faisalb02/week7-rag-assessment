from src.metadata_filter import add_metadata, filter_documents

# Sample documents
chunks = [
    {
        "text": "Old leave policy: 10 casual leaves.",
        "metadata": {
            "source": "leave_policy_2024.txt"
        }
    },
    {
        "text": "Current leave policy: 12 casual leaves.",
        "metadata": {
            "source": "leave_policy_2026.txt"
        }
    },
    {
        "text": "Employee security policy.",
        "metadata": {
            "source": "data_security.pdf"
        }
    }
]

# Add department and year metadata
chunks = add_metadata(chunks)

print("========== ALL DOCUMENTS ==========")

for chunk in chunks:
    print(
        chunk["metadata"]["source"],
        chunk["metadata"]
    )

# Filter only HR department
hr_documents = filter_documents(
    chunks,
    department="HR"
)

print("\n========== HR DOCUMENTS ==========")

for chunk in hr_documents:
    print(chunk["metadata"]["source"])

# Remove outdated documents
current_documents = filter_documents(
    chunks,
    min_year=2026
)

print("\n========== CURRENT DOCUMENTS ONLY ==========")

for chunk in current_documents:
    print(chunk["metadata"]["source"])


# Demonstrate outdated document removal from answer context

demo_chunks = [
    {
        "text": "Employees get 8 casual leaves per year.",
        "metadata": {
            "source": "leave_policy_2024.txt",
            "department": "HR",
            "year": 2024
        }
    },
    {
        "text": "Employees get 12 casual leaves per year.",
        "metadata": {
            "source": "leave_policy_2026.txt",
            "department": "HR",
            "year": 2026
        }
    }
]

print("\nBEFORE FILTERING - ANSWER CONTEXT")

for chunk in demo_chunks:
    print(chunk["text"], chunk["metadata"]["year"])

filtered_chunks = filter_documents(
    demo_chunks,
    department="HR",
    min_year=2026
)

print("\nAFTER FILTERING - ANSWER CONTEXT")

for chunk in filtered_chunks:
    print(chunk["text"], chunk["metadata"]["year"])    