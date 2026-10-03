from app.ingestion.chunker import chunk_text

from app.ingestion.html_loader import load_html

DOCUMENT_PATH = "data/documents/shopify_returns.html"

def ingest_document():
    text = load_html(DOCUMENT_PATH)

    chunks = chunk_text(text)

    print(f"Document length: {len(text)} characters")
    print(f"Number of chunks: {len(chunks)}")

    for i, chunk in enumerate(chunks[:3]):
        print(f"\n--- Chunk {i + 1} ---")
        print(chunk[:500])

if __name__ == "__main__":
    ingest_document()