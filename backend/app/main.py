from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import settings
from app.schemas.analysis import ClaimInput
from app.services.demo_engine import (
    available_dashboard,
    build_demo_analysis,
    demo_investigations,
    model_performance,
    research_analytics,
    trend_claims,
)

app = FastAPI(title=settings.app_name, version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}


@app.get("/api/dashboard")
def dashboard() -> dict[str, Any]:
    return available_dashboard()


@app.get("/api/investigations")
def investigations() -> list[dict[str, Any]]:
    return demo_investigations()


@app.get("/api/investigations/{investigation_id}")
def investigation_detail(investigation_id: str) -> dict[str, Any]:
    try:
        item = next(i for i in demo_investigations() if i["id"] == investigation_id)
        return item
    except StopIteration as exc:
        raise HTTPException(status_code=404, detail="Investigation not found") from exc


@app.post("/api/analyze")
def analyze(payload: ClaimInput) -> dict[str, Any]:
    result = build_demo_analysis(payload)
    return result.model_dump()


@app.get("/api/models/performance")
def models_performance() -> list[dict[str, Any]]:
    return model_performance()


@app.get("/api/trending")
def trending() -> list[dict[str, Any]]:
    return trend_claims()


@app.get("/api/research")
def research() -> dict[str, Any]:
    return research_analytics()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", reload=True)
