from rank_bm25 import BM25Okapi

from app.services.embeddings import generate_embedding
from app.services.rag import load_retriever
from app.vector_store.storage import load_documents


documents = load_documents(
    "data/vector_store/documents.json"
)

vector_store = load_retriever()

query = "How can I request a refund?"

print("\nFAISS distances:")

query_embedding = generate_embedding(query)

semantic_results = vector_store.search(
    query_embedding,
    top_k=len(documents)
)

for result in semantic_results:
    print(
        result["document"]["source"],
        "=>",
        result["distance"]
    )


print("\nBM25 scores:")

tokenized_documents = [
    document["text"].lower().split()
    for document in documents
]

bm25 = BM25Okapi(
    tokenized_documents
)

tokenized_query = query.lower().split()

scores = bm25.get_scores(
    tokenized_query
)

for document, score in zip(documents, scores):
    print(
        document["source"],
        "=>",
        score
    )