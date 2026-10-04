from fastapi import FastAPI

from app.config import settings
from app.memory.conversation import ConversationMemory
from app.schemas import (
    ChatRequest,
    ChatResponse,
    MessageAnalysisResponse,
    Source
)
from app.services.classifier import analyze_message
from app.services.escalation import (
    escalate_to_support,
    should_escalate
)
from app.services.llm import generate_response
from app.services.rag import load_retriever
from app.services.tools import run_tool_calling
from app.retrieval.hybrid_retriever import HybridRetriever
from app.vector_store.storage import load_documents


app = FastAPI(
    title="AI Support Copilot"
)


conversations: dict[str, ConversationMemory] = {}


def load_hybrid_retriever() -> HybridRetriever:

    documents = load_documents(
        "data/vector_store/documents.json"
    )

    vector_store = load_retriever()

    return HybridRetriever(
        vector_store=vector_store,
        documents=documents
    )


@app.get("/")
def root():
    return {
        "message": "AI Support Copilot API",
        "environment": settings.app_env,
        "model": settings.model_name
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat(request: ChatRequest):

    if request.conversation_id not in conversations:

        conversations[
            request.conversation_id
        ] = ConversationMemory()

    memory = conversations[
        request.conversation_id
    ]

    analysis = analyze_message(
        request.prompt
    )

    # -------------------------
    # High-priority escalation
    # -------------------------

    if should_escalate(
        analysis.priority,
        analysis.intent
    ):

        ticket = escalate_to_support(
            message=request.prompt,
            priority=analysis.priority
        )

        answer = (
            "I've created a support ticket for this issue. "
            f"Your ticket ID is {ticket['ticket_id']}."
        )

        memory.add_message(
            "user",
            request.prompt
        )

        memory.add_message(
            "assistant",
            answer
        )

        return ChatResponse(
            prompt=request.prompt,
            response=answer,
            analysis=MessageAnalysisResponse(
                intent=analysis.intent,
                sentiment=analysis.sentiment,
                priority=analysis.priority
            ),
            sources=[]
        )

    # -------------------------
    # Order-related tool calling
    # -------------------------

    if analysis.intent == "order_status":

        answer = run_tool_calling(
            message=request.prompt,
            conversation_history=memory.get_messages()
        )

        memory.add_message(
            "user",
            request.prompt
        )

        memory.add_message(
            "assistant",
            answer
        )

        return ChatResponse(
            prompt=request.prompt,
            response=answer,
            analysis=MessageAnalysisResponse(
                intent=analysis.intent,
                sentiment=analysis.sentiment,
                priority=analysis.priority
            ),
            sources=[]
        )

    # -------------------------
    # Hybrid RAG retrieval
    # -------------------------

    retriever = load_hybrid_retriever()

    results = retriever.retrieve(
    request.prompt,
    top_k=3
   )

    results = [
        result
        for result in results
        if result["score"] >= 0.75
    ]

    if not results:

        answer = (
            "I don't have enough information "
            "in the knowledge base to answer that."
        )

        return ChatResponse(
            prompt=request.prompt,
            response=answer,
            analysis=MessageAnalysisResponse(
                intent=analysis.intent,
                sentiment=analysis.sentiment,
                priority=analysis.priority
            ),
            sources=[]
        )

    context = "\n\n".join(
        result["document"]["text"]
        for result in results
    )

    answer = generate_response(
        prompt=request.prompt,
        context=context,
        conversation_history=memory.get_messages()
    )

    memory.add_message(
        "user",
        request.prompt
    )

    memory.add_message(
        "assistant",
        answer
    )

    sources = [
        Source(
            text=result["document"]["text"],
            source=result["document"]["source"],
            chunk_id=result["document"]["chunk_id"],
            distance=float(result["score"])
        )
        for result in results
    ]

    return ChatResponse(
        prompt=request.prompt,
        response=answer,
        analysis=MessageAnalysisResponse(
            intent=analysis.intent,
            sentiment=analysis.sentiment,
            priority=analysis.priority
        ),
        sources=sources
    )