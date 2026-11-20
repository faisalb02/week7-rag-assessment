def add_metadata(chunks):

    for chunk in chunks:

        source = chunk["metadata"]["source"].lower()

        # Assign department
        if "security" in source:
            department = "IT"
        else:
            department = "HR"

        # Extract year from filename
        if "2024" in source:
            year = 2024
        else:
            year = 2026

        chunk["metadata"]["department"] = department
        chunk["metadata"]["year"] = year

    return chunks


def filter_documents(
    chunks,
    department=None,
    min_year=None
):

    filtered = []

    for chunk in chunks:

        metadata = chunk["metadata"]

        if department is not None:
            if metadata["department"] != department:
                continue

        if min_year is not None:
            if metadata["year"] < min_year:
                continue

        filtered.append(chunk)

    return filtered