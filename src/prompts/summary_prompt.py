def build_summary_prompt(context):

    prompt = f"""
You are an expert document assistant.

Summarize the following document content.

Requirements:
- Keep the summary concise.
- Use bullet points.
- Highlight important concepts.
- Do not invent information.
- Use only the provided context.

Context:

{context}
"""

    return prompt