from src.prompts.quiz_prompt import build_quiz_prompt


def generate_quiz(chunks, llm_function):

    context = "\n\n".join(chunks)

    prompt = build_quiz_prompt(context)

    quiz = llm_function(prompt)

    return quiz