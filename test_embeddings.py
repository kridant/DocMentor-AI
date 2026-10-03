from src.rag.pdf_loader import load_pdf
from src.rag.text_splitter import split_text
from src.rag.embeddings import create_embeddings

text = load_pdf("documents/sample.pdf")

chunks = split_text(text)

embeddings = create_embeddings(chunks)

print("Number of Chunks:", len(chunks))

print("Embedding Shape:")

print(embeddings.shape)