from datetime import datetime, timezone
from typing import Any, Literal
from uuid import uuid4

from fastapi import FastAPI, HTTPException
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


class SampleCreate(BaseModel):
    task_id: str = Field(..., min_length=1)
    sample_type: Literal["text", "audio"] = "text"
    content: str | None = None
    transcript: str | None = None
    language: str = "ko"
    metadata: dict[str, Any] = Field(default_factory=dict)


class Sample(BaseModel):
    id: str
    task_id: str
    sample_type: Literal["text", "audio"]
    content: str | None
    transcript: str | None
    language: str
    metadata: dict[str, Any]
    created_at: datetime


app = FastAPI(
    title="Cloud Native AI Evaluation Platform",
    version=APP_VERSION,
    description="A cloud-native platform for AI data evaluation workflows.",
)

tasks: list[Task] = []
samples: list[Sample] = []


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


@app.post("/samples", status_code=201, response_model=Sample)
def create_sample(request: SampleCreate):
    task_exists = any(task.id == request.task_id for task in tasks)

    if not task_exists:
        raise HTTPException(
            status_code=404,
            detail=f"Task not found: {request.task_id}",
        )

    sample = Sample(
        id=str(uuid4()),
        task_id=request.task_id,
        sample_type=request.sample_type,
        content=request.content,
        transcript=request.transcript,
        language=request.language,
        metadata=request.metadata,
        created_at=datetime.now(timezone.utc),
    )

    samples.append(sample)
    return sample


@app.get("/samples", response_model=list[Sample])
def list_samples():
    return samples


@app.get("/samples/{sample_id}", response_model=Sample)
def get_sample(sample_id: str):
    for sample in samples:
        if sample.id == sample_id:
            return sample

    raise HTTPException(
        status_code=404,
        detail=f"Sample not found: {sample_id}",
    )
