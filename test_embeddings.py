from app.ingestion.html_loader import load_html
from app.ingestion.chunker import chunk_text
from app.services.embeddings import generate_embedding


document_path = "data/documents/shopify_returns.html"

text = load_html(document_path)

chunks = chunk_text(text)

print("Number of chunks:", len(chunks))

for i, chunk in enumerate(chunks, start=1):
    embedding = generate_embedding(chunk)

    print(f"\nChunk {i}")
    print("Text length:", len(chunk))
    print("Embedding dimensions:", len(embedding))