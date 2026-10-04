from app.services.rag import answer_question


question = "How can I return an item?"

result = answer_question(question)

print("\nAnswer:")
print(result["answer"])

print("\nSources:")

for i, source in enumerate(result["sources"], start=1):
    print(f"\n--- Source {i} ---")
    print("Distance:", source["distance"])
    print(source["document"])