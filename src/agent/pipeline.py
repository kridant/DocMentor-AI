from src.rag.pdf_loader import load_pdf
from src.rag.text_splitter import split_text
from src.rag.embeddings import create_embeddings
from src.rag.vector_store import create_faiss_index


def process_document(uploaded_file):
    """
    Converts a PDF into a searchable FAISS index.

    Returns:
        index  : FAISS vector index
        chunks : List of text chunks
    """

    text = load_pdf(uploaded_file)

    chunks = split_text(text)

    embeddings = create_embeddings(chunks)

    index = create_faiss_index(embeddings)

    return index, chunks