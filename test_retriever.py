from app.ingestion.html_loader import load_html
from app.ingestion.chunker import chunk_text
from app.services.embeddings import generate_embedding
from app.vector_store.faiss_store import FAISSVectorStore
from app.retrieval.retriever import Retriever


document_path = "data/documents/shopify_returns.html"

text = load_html(document_path)
chunks = chunk_text(text)

embeddings = [
    generate_embedding(chunk)
    for chunk in chunks
]

store = FAISSVectorStore(
    dimension=len(embeddings[0])
)

store.add(
    embeddings,
    chunks
)

retriever = Retriever(store)

query = "How can I return an item?"

results = retriever.retrieve(
    query,
    top_k=3
)

print("\nSearch results:")

for i, result in enumerate(results, start=1):
    print(f"\n--- Result {i} ---")
    print("Distance:", result["distance"])
    print("Document:")
    print(result["document"])