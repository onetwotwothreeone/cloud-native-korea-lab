"""Minimal FastAPI app for the HYEAN/GWAN prototype."""

from fastapi import FastAPI

from app.api.routes_gwan import router as gwan_router

app = FastAPI(
    title="HYEAN/GWAN Interface Payload Prototype",
    version="0.2.0",
    description="Validates and generates structured GWAN outputs for the HYEAN Operator Interface.",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(gwan_router)
