from pathlib import Path

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


# PDF save location
OUTPUT_DIR = Path(__file__).parent / "data" / "documents"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# PDF 1: Employee Benefits
benefits = [
    "Employees receive 12 casual leaves per year.",
    "Employees receive 10 sick leaves per year.",
    "Employees receive 15 earned leaves per year.",
    "Employees are eligible for company medical insurance.",
    "Employees receive annual performance reviews.",
    "Eligible employees can receive travel expense reimbursement.",
    "Employees can request work from home with manager approval."
]


# PDF 2: Data Security
security = [
    "Employees must keep company information confidential.",
    "Employees must use strong passwords for company accounts.",
    "Passwords must not be shared with other employees.",
    "Company data must only be accessed through approved systems.",
    "Employees must not share confidential files with unauthorized persons.",
    "Lost company devices must be reported immediately to IT.",
    "Employees must follow company cybersecurity guidelines."
]


def create_pdf(filename, title, content):

    file_path = OUTPUT_DIR / filename

    pdf = SimpleDocTemplate(str(file_path))

    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph(title, styles["Title"]))

    elements.append(Spacer(1, 20))

    for item in content:

        elements.append(
            Paragraph(item, styles["Normal"])
        )

        elements.append(Spacer(1, 12))

    pdf.build(elements)

    print("Created:", filename)


create_pdf(
    "employee_benefits.pdf",
    "Employee Benefits Policy",
    benefits
)

create_pdf(
    "data_security.pdf",
    "Company Data Security Policy",
    security
)