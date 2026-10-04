from pathlib import Path

from app.ingestion.html_loader import load_html
from app.ingestion.chunker import chunk_text
from app.services.embeddings import generate_embedding
from app.vector_store.faiss_store import FAISSVectorStore
from app.vector_store.storage import save_documents


DOCUMENTS_DIR = Path("data/documents")

INDEX_PATH = "data/vector_store/shopify.index"
DOCUMENTS_PATH = "data/vector_store/documents.json"


def load_documents() -> list[dict]:

    documents = []

    for file_path in DOCUMENTS_DIR.glob("*.html"):

        print(f"Loading: {file_path.name}")

        text = load_html(
            str(file_path)
        )

        chunks = chunk_text(
            text
        )

        print(
            f"  Created {len(chunks)} chunk(s)."
        )

        for chunk_id, chunk in enumerate(chunks):

            documents.append({
                "text": chunk,
                "source": file_path.name,
                "chunk_id": chunk_id,
                "document_id": (
                    f"{file_path.stem}_{chunk_id}"
                )
            })

    return documents


def main():

    print("Loading documents...")

    documents = load_documents()

    if not documents:
        raise ValueError(
            "No HTML documents found in data/documents."
        )

    print(
        f"\nTotal chunks: {len(documents)}"
    )

    print("\nGenerating embeddings...")

    embeddings = [
        generate_embedding(
            document["text"]
        )
        for document in documents
    ]

    print("\nCreating FAISS index...")

    store = FAISSVectorStore(
        dimension=len(embeddings[0])
    )

    store.add(
        embeddings,
        documents
    )

    print("\nSaving FAISS index...")

    store.save(
        INDEX_PATH
    )

    print("Saving document metadata...")

    save_documents(
        documents,
        DOCUMENTS_PATH
    )

    print("\nIndex built successfully.")


if __name__ == "__main__":
    main()