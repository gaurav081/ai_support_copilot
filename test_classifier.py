from app.services.classifier import analyze_message


message = (
    "My order arrived damaged and I want to return it."
)

result = analyze_message(message)

print("\nAnalysis:")
print(result.model_dump())