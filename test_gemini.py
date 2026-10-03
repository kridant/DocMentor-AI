from src.llm.gemini import generate_response

question = "What is binary search in 3 lines?"

answer = generate_response(question)

print(answer)