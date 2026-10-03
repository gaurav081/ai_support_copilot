from app.ingestion.html_loader import load_html
from app.ingestion.chunker import chunk_text
from app.services.embeddings import generate_embedding
from app.vector_store.faiss_store import FAISSVectorStore


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

store.add(embeddings, chunks)

query = "How can I return an item?"

query_embedding = generate_embedding(query)

results = store.search(
    query_embedding,
    top_k=3
)

print("Search results:")

for result in results:
    print("\nDistance:", result["distance"])
    print("Document:", result["document"][:200])