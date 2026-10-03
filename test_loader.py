from app.ingestion.html_loader import load_html


text = load_html("data/documents/shopify_returns.html")

print(text[:3000])