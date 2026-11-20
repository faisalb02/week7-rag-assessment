from unittest.mock import patch

from src.answer import answer

with patch("src.answer.llm_client.chat.completions.create") as mock_llm:

    result = answer("Who won the world cup?")

    print("Answer:", result)

    if result == "I don't have information on that":
        print("Fallback: PASSED")
    else:
        print("Fallback: FAILED")

    if mock_llm.call_count == 0:
        print("LLM called: NO")
        print("LLM call prevention: PASSED")
    else:
        print("LLM called:", mock_llm.call_count)
        print("LLM call prevention: FAILED")