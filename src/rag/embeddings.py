from sentence_transformers import SentenceTransformer
print("Loading Embedding Model...")
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


def create_embeddings(chunks):
    embeddings = model.encode(chunks)

    return embeddings