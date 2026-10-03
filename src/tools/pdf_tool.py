from src.rag.embeddings import create_embeddings
from src.rag.retriever import retrieve_chunks


def search_pdf(question, index, chunks):

    # Convert the user's question into an embedding
    query_embedding = create_embeddings([question])

    # Retrieve the most relevant chunks
    relevant_chunks = retrieve_chunks(
        query_embedding,
        index,
        chunks,
        k=3
    )

    return relevant_chunks