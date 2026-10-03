def build_quiz_prompt(context):

    prompt = f"""
You are an expert interviewer.

Generate 10 interview-style questions from the document.

Requirements:
- Cover important concepts.
- Do not include answers.
- Use numbered points.

Document:

{context}
"""

    return prompt