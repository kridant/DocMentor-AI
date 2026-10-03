from src.rag.embeddings import create_embeddings
from src.rag.retriever import retrieve_chunks

from src.prompts.summary_prompt import build_summary_prompt


def summarize_document(chunks, llm_function):

    context = "\n\n".join(chunks)
    prompt = build_summary_prompt(context)

    summary = llm_function(prompt)

    return summary