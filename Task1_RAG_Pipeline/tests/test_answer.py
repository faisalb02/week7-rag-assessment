from src.answer import answer

questions = [
    "How many casual leaves per year?",
    "How many sick leaves per year?",
    "How many earned leaves per year?",
    "When are salaries paid?",
    "What are the working hours?",
    "Does the company provide medical insurance?",
    "Who won the world cup?",
    "What is the company CEO name?",
    "What is the company's stock price?",
    "How many employees work in the company?"
]

for i, question in enumerate(questions, start=1):

    print(f"\nTest {i}")
    print("Question:", question)

    result = answer(question, k=4)

    print("Answer:", result)
    print("----------------------")