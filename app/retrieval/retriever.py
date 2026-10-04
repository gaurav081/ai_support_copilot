from rank_bm25 import BM25Okapi

from app.services.embeddings import generate_embedding
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

        self.bm25 = BM25Okapi(
            tokenized_documents
        )

    def retrieve(
        self,
        query: str,
        top_k: int = 3
    ) -> list[dict]:

        # -------------------------
        # 1. FAISS semantic search
        # -------------------------

        query_embedding = generate_embedding(
            query
        )

        semantic_results = self.vector_store.search(
            query_embedding,
            top_k=len(self.documents)
        )

        semantic_distances = [
            result["distance"]
            for result in semantic_results
        ]

        max_distance = max(
            semantic_distances,
            default=0
        )

        semantic_scores = {}

        for result in semantic_results:

            document_id = result["document"]["document_id"]

            distance = result["distance"]

            if max_distance == 0:
                score = 1.0
            else:
                score = 1 - (
                    distance / max_distance
                )

            semantic_scores[document_id] = max(
                0.0,
                score
            )

        # -------------------------
        # 2. BM25 keyword search
        # -------------------------

        tokenized_query = query.lower().split()

        bm25_scores = self.bm25.get_scores(
            tokenized_query
        )

        max_bm25_score = max(
            bm25_scores,
            default=0
        )

        keyword_scores = {}

        for index, score in enumerate(
            bm25_scores
        ):

            document_id = self.documents[index]["document_id"]

            if max_bm25_score <= 0:
                normalized_score = 0.0
            else:
                normalized_score = (
                    max(0.0, float(score))
                    / max_bm25_score
                )

            keyword_scores[document_id] = (
                normalized_score
            )

        # -------------------------
        # 3. Weighted hybrid score
        # -------------------------

        results = []

        for document in self.documents:

            document_id = document["document_id"]

            semantic_score = semantic_scores.get(
                document_id,
                0.0
            )

            keyword_score = keyword_scores.get(
                document_id,
                0.0
            )

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

        # -------------------------
        # 4. Rank results
        # -------------------------

        results.sort(
            key=lambda result: result["score"],
            reverse=True
        )

        return results[:top_k]