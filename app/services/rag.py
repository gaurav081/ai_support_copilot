from app.vector_store.faiss_store import FAISSVectorStore


INDEX_PATH = "data/vector_store/shopify.index"
DOCUMENTS_PATH = "data/vector_store/documents.json"


def load_retriever() -> FAISSVectorStore:

    from app.vector_store.storage import load_documents

    documents = load_documents(
        DOCUMENTS_PATH
    )

    return FAISSVectorStore.load(
        INDEX_PATH,
        documents
    )