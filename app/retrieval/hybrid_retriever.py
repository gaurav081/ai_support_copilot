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
        # Semantic retrieval
        # -------------------------

        query_embedding = generate_embedding(
            query
        )

        semantic_results = self.vector_store.search(
            query_embedding,
            top_k=len(self.documents)
        )

        semantic_rank = {}

        for rank, result in enumerate(
            semantic_results
        ):

            document_id = result["document"]["document_id"]

            semantic_rank[document_id] = rank


        # -------------------------
        # Keyword retrieval
        # -------------------------

        tokenized_query = query.lower().split()

        bm25_scores = self.bm25.get_scores(
            tokenized_query
        )

        keyword_order = sorted(
            range(len(self.documents)),
            key=lambda index: bm25_scores[index],
            reverse=True
        )

        keyword_rank = {}

        for rank, index in enumerate(
            keyword_order
        ):

            document_id = self.documents[index]["document_id"]

            keyword_rank[document_id] = rank


        # -------------------------
        # Rank fusion
        # -------------------------

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

            semantic_score = 1 / (
                1 + semantic_position
            )

            keyword_score = 1 / (
                1 + keyword_position
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


        results.sort(
            key=lambda result: result["score"],
            reverse=True
        )

        return results[:top_k]