from fastapi import FastAPI
# from pydantic import BaseModel
from app.schemas import ChatRequest, ChatResponse

from app.config import settings
from app.services.llm import generate_response


app = FastAPI(title="AI Support Copilot")

@app.get("/")
def root():
    return {
      "message": "AI Support Copilot API",
      "status": "running",
      "environment": settings.app_env,
      "model": settings.model_name
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    response = generate_response(request.prompt)
     
    return {
      "prompt": request.prompt,
      "response": response
    }

