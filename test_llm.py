from app.services.llm import generate_response


def test_generate_response(monkeypatch):
    def fake_chat(**kwargs):
        return {
            "message": {
                "content": "A customer support chatbot helps customers resolve their questions."
            }
        }

    monkeypatch.setattr("app.services.llm.ollama.chat", fake_chat)

    response = generate_response(
        "Explain what a customer support chatbot does in one sentence.",
        "A customer support chatbot helps customers resolve their questions."
    )

    assert isinstance(response, str)
    assert len(response) > 0