from app.services.rag import load_retriever
from app.retrieval.hybrid_retriever import HybridRetriever


def test_retriever():
    vector_store = load_retriever()
    documents = vector_store.documents

    retriever = HybridRetriever(
        vector_store,
        documents
    )

    results = retriever.retrieve(
        "How can I return an item?",
        top_k=3
    )

    assert len(results) > 0
    assert "document" in results[0]
    assert "score" in results[0]