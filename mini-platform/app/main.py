from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="Cloud Native Korea Lab AI Docs Agent",
    version="0.1.0"
)

class AskRequest(BaseModel):
    question: str

@app.get("/")
def home():
    return {
        "message": "Cloud Native Korea Lab Mini Platform - Python FastAPI"
    }

@app.get("/health")
def health():
    return {
        "status": "ok"
    }

@app.get("/version")
def version():
    return {
        "version": "0.1.0",
        "language": "Python",
        "framework": "FastAPI"
    }

@app.post("/ask")
def ask(request: AskRequest):
    return {
        "question": request.question,
        "answer": "아직 실제 AI/RAG는 연결하지 않았습니다. 현재는 Python FastAPI 기반 예시 응답입니다.",
        "source": "sample-response"
    }
