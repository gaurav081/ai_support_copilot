from rank_bm25 import BM25Okapi

from app.config import settings
from app.vector_store.faiss_store import FAISSVectorStore


class HybridRetriever:

    def __init__(
        self,
        vector_store: FAISSVectorStore,
        documents: list[dict]
    ):
        self.vector_store = vector_store
        self.documents = documents

        tokenized_documents = [
            document["text"].lower().split()
            for document in documents
        ]

        self.bm25 = BM25Okapi(tokenized_documents)

    def retrieve(
        self,
        query: str,
        top_k: int = 3
    ) -> list[dict]:

        # Keyword retrieval using BM25
        tokenized_query = query.lower().split()

        bm25_scores = self.bm25.get_scores(
            tokenized_query
        )

        keyword_order = sorted(
            range(len(self.documents)),
            key=lambda index: bm25_scores[index],
            reverse=True
        )

        keyword_rank = {
            self.documents[index]["document_id"]: rank
            for rank, index in enumerate(keyword_order)
        }

        # Keyword-only mode: avoids loading the embedding model.
        if settings.retrieval_mode == "keyword":
            results = []

            for index in keyword_order[:top_k]:
                document = self.documents[index]
                document_id = document["document_id"]
                keyword_score = 1 / (
                    1 + keyword_rank[document_id]
                )

                results.append({
                    "document": document,
                    "score": keyword_score,
                    "semantic_score": 0.0,
                    "keyword_score": keyword_score
                })

            return results

        # Hybrid mode: combine semantic and keyword retrieval.
        from app.services.embeddings import generate_embedding

        query_embedding = generate_embedding(query)

        semantic_results = self.vector_store.search(
            query_embedding,
            top_k=len(self.documents)
        )

        semantic_rank = {
            result["document"]["document_id"]: rank
            for rank, result in enumerate(semantic_results)
        }

        results = []

        for document in self.documents:
            document_id = document["document_id"]

            semantic_position = semantic_rank.get(
                document_id,
                len(self.documents)
            )

            keyword_position = keyword_rank.get(
                document_id,
                len(self.documents)
            )

            semantic_score = 1 / (1 + semantic_position)
            keyword_score = 1 / (1 + keyword_position)

            hybrid_score = (
                0.7 * semantic_score
                + 0.3 * keyword_score
            )

            results.append({
                "document": document,
                "score": hybrid_score,
                "semantic_score": semantic_score,
                "keyword_score": keyword_score
            })

        results.sort(
            key=lambda result: result["score"],
            reverse=True
        )

        return results[:top_k]
