from src.rag.pdf_loader import load_pdf
from src.rag.text_splitter import split_text

text = load_pdf("documents/sample.pdf")

chunks = split_text(text)

print(f"Total Chunks: {len(chunks)}")

print("\nFirst Chunk:\n")
print(chunks[0])