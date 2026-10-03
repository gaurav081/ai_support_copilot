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
        documents: list[str]
    ) -> None:

        vectors = np.array(
            embeddings,
            dtype="float32"
        )

        if vectors.shape[1] != self.dimension:
            raise ValueError(
                f"Expected vectors with dimension {self.dimension}, "
                f"got {vectors.shape[1]}"
            )

        self.index.add(vectors)
        self.documents.extend(documents)

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 3
    ) -> list[dict]:

        query_vector = np.array(
            [query_embedding],
            dtype="float32"
        )

        distances, indices = self.index.search(
            query_vector,
            min(top_k, len(self.documents))
        )

        results = []

        for distance, index in zip(distances[0], indices[0]):
            if index == -1:
                continue

            results.append({
                "document": self.documents[index],
                "distance": float(distance)
            })

        return results