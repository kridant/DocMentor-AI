def build_prompt(question, context, conversation):

    prompt = f"""
You are an AI assistant that answers questions about a PDF document.

Previous Conversation:
{conversation}

Relevant Context:
{context}

Current Question:
{question}

Instructions:
- Answer only using the provided context.
- If the answer is not present, say that it is not available in the document.
- Keep your answer clear and concise.
"""

    return prompt