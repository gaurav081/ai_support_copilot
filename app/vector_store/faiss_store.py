import faiss
import numpy as np


class FAISSVectorStore:

    def __init__(self, dimension: int):

        self.dimension = dimension

        self.index = faiss.IndexFlatL2(dimension)

        self.documents = []

    def add(
        self,
        embeddings: list[list[float]],
        documents: list[dict]
    ) -> None:

        vectors = np.array(
            embeddings,
            dtype="float32"
        )

        if vectors.ndim != 2:
            raise ValueError(
                "Embeddings must be a 2-dimensional list."
            )

        if vectors.shape[1] != self.dimension:
            raise ValueError(
                f"Expected vectors with dimension {self.dimension}, "
                f"got {vectors.shape[1]}"
            )

        if len(vectors) != len(documents):
            raise ValueError(
                "Number of embeddings must match "
                "number of documents."
            )

        self.index.add(vectors)

        self.documents.extend(documents)

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 3
    ) -> list[dict]:

        if not self.documents:
            return []

        query_vector = np.array(
            [query_embedding],
            dtype="float32"
        )

        distances, indices = self.index.search(
            query_vector,
            min(top_k, len(self.documents))
        )

        results = []

        for distance, index in zip(
            distances[0],
            indices[0]
        ):

            if index == -1:
                continue

            document = self.documents[index]

            results.append({
                "document": document,
                "distance": float(distance)
            })

        return results

    def save(self, index_path: str) -> None:

        faiss.write_index(
            self.index,
            index_path
        )

    @classmethod
    def load(
        cls,
        index_path: str,
        documents: list[dict]
    ):

        index = faiss.read_index(
            index_path
        )

        store = cls(index.d)

        store.index = index

        store.documents = documents

        return store