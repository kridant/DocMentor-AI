from sentence_transformers import SentenceTransformer

from src.rag.pdf_loader import load_pdf
from src.rag.text_splitter import split_text
from src.rag.embeddings import create_embeddings
from src.rag.vector_store import create_faiss_index
from src.rag.retriever import retrieve_chunks


text = load_pdf("documents/sample.pdf")

chunks = split_text(text)

embeddings = create_embeddings(chunks)

index = create_faiss_index(embeddings)

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

query = "What is this document about?"

query_embedding = model.encode([query])

results = retrieve_chunks(query_embedding,index,chunks)

print(results[0])