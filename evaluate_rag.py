from app.services.rag import load_retriever
from app.retrieval.hybrid_retriever import HybridRetriever
from evaluation_dataset import EVALUATION_DATASET


def reciprocal_rank(
    retrieved_documents: list[str],
    relevant_document: str
) -> float:

    for rank, document in enumerate(
        retrieved_documents,
        start=1
    ):
        if document == relevant_document:
            return 1 / rank

    return 0.0


def evaluate(k: int = 3) -> None:

    vector_store = load_retriever()

    documents = vector_store.documents

    retriever = HybridRetriever(
        vector_store,
        documents
    )

    hits = 0
    reciprocal_ranks = []

    for item in EVALUATION_DATASET:

        results = retriever.retrieve(
            item["query"],
            top_k=k
        )

        retrieved_documents = [
            result["document"]["source"]
            for result in results
        ]

        relevant_document = item[
            "relevant_document"
        ]

        if relevant_document in retrieved_documents:
            hits += 1

        reciprocal_ranks.append(
            reciprocal_rank(
                retrieved_documents,
                relevant_document
            )
        )

        print(f"\nQuery: {item['query']}")
        print(f"Expected: {relevant_document}")
        print(f"Retrieved: {retrieved_documents}")

    total = len(EVALUATION_DATASET)

    hit_at_k = hits / total
    mrr = sum(reciprocal_ranks) / total

    print("\n--------------------")
    print("RAG Evaluation")
    print("--------------------")
    print(f"Hit@{k}: {hit_at_k:.2f}")
    print(f"MRR:     {mrr:.2f}")


if __name__ == "__main__":
    evaluate(k=3)