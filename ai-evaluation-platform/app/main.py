from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from fastapi import FastAPI
from pydantic import BaseModel, Field


APP_VERSION = "0.1.0"


class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1)
    task_type: Literal["text", "audio"] = "text"
    language: str = "ko"
    description: str | None = None


class Task(BaseModel):
    id: str
    title: str
    task_type: Literal["text", "audio"]
    language: str
    status: Literal["open", "closed"]
    description: str | None
    created_at: datetime


app = FastAPI(
    title="Cloud Native AI Evaluation Platform",
    version=APP_VERSION,
    description="A cloud-native platform for AI data evaluation workflows.",
)

tasks: list[Task] = []


@app.get("/")
def home():
    return {
        "service": "Cloud Native AI Evaluation Platform",
        "status": "running",
        "version": APP_VERSION,
        "message": "AI evaluation workflow API is ready.",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/version")
def version():
    return {
        "version": APP_VERSION,
        "project": "ai-evaluation-platform",
        "framework": "FastAPI",
    }


@app.post("/tasks", status_code=201, response_model=Task)
def create_task(request: TaskCreate):
    task = Task(
        id=str(uuid4()),
        title=request.title,
        task_type=request.task_type,
        language=request.language,
        status="open",
        description=request.description,
        created_at=datetime.now(timezone.utc),
    )

    tasks.append(task)
    return task


@app.get("/tasks", response_model=list[Task])
def list_tasks():
    return tasks
