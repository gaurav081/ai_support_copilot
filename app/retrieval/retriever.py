from app.services.embeddings import generate_embedding
from app.vector_store.faiss_store import FAISSVectorStore


class Retriever:
    def __init__(self, vector_store: FAISSVectorStore):
        self.vector_store = vector_store

    def retrieve(
        self,
        query: str,
        top_k: int = 3
    ) -> list[dict]:

        query_embedding = generate_embedding(query)

        results = self.vector_store.search(
            query_embedding,
            top_k=top_k
        )

        return results