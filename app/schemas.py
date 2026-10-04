from pydantic import BaseModel


class ChatRequest(BaseModel):
    conversation_id: str
    prompt: str


class MessageAnalysisResponse(BaseModel):
    intent: str
    sentiment: str
    priority: str


class Source(BaseModel):
    text: str
    source: str
    chunk_id: int
    distance: float


class ChatResponse(BaseModel):
    prompt: str
    response: str
    analysis: MessageAnalysisResponse
    sources: list[Source]