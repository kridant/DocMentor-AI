from src.rag.pdf_loader import load_pdf

text = load_pdf("documents/sample.pdf")

print(text[:1000])