from app.retrieval.hybrid_retriever import HybridRetriever
from app.services.rag import load_retriever
from app.vector_store.storage import load_documents


DOCUMENTS_PATH = "data/vector_store/documents.json"


documents = load_documents(
    DOCUMENTS_PATH
)

vector_store = load_retriever()

retriever = HybridRetriever(
    vector_store=vector_store,
    documents=documents
)

results = retriever.retrieve(
    "How can I request a refund?",
    top_k=3
)

for result in results:

    print("\n-------------------------")

    print(
        "Hybrid score:",
        round(result["score"], 4)
    )

    print(
        "Semantic score:",
        round(result["semantic_score"], 4)
    )

    print(
        "Keyword score:",
        round(result["keyword_score"], 4)
    )

    print(
        "Source:",
        result["document"]["source"]
    )

    print(
        "Text:",
        result["document"]["text"]
    )