from app.services.embeddings import generate_embedding
from app.vector_store.faiss_store import FAISSVectorStore
from app.vector_store.storage import load_documents


INDEX_PATH = "data/vector_store/shopify.index"
DOCUMENTS_PATH = "data/vector_store/documents.json"


documents = load_documents(DOCUMENTS_PATH)

store = FAISSVectorStore.load(
    INDEX_PATH,
    documents
)

query = "How can I return an item?"

query_embedding = generate_embedding(query)

results = store.search(
    query_embedding,
    top_k=3
)

print("\nSearch results:")

for i, result in enumerate(results, start=1):
    print(f"\n--- Result {i} ---")
    print("Distance:", result["distance"])
    print("Document:")
    print(result["document"])