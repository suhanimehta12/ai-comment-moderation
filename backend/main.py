"""
main.py
-------
FastAPI backend for the AI Comment Moderation System.

Run locally:
    uvicorn main:app --reload --port 8000

Endpoints:
    POST /moderate-comment   → classify a single comment
    GET  /health             → liveness probe
"""

from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator

from model import load_or_train_model, predict_comment

# ---------------------------------------------------------------------------
# App lifecycle
# ---------------------------------------------------------------------------

models: dict = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    global models
    models = load_or_train_model()
    yield
    models.clear()


app = FastAPI(
    title="AI Comment Moderation API",
    description="Detects toxicity, spam, and sentiment in social media comments.",
    version="1.0.0",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# CORS (allow React dev server + any deployed frontend)
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten to your Vercel URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------


class CommentRequest(BaseModel):
    comment: str

    @field_validator("comment")
    @classmethod
    def comment_must_not_be_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("comment must not be empty")
        if len(v) > 5000:
            raise ValueError("comment must be 5000 characters or fewer")
        return v.strip()


class ModerationResponse(BaseModel):
    comment: str
    toxicity: str           # "Toxic" | "Non-Toxic"
    spam: str               # "Spam"  | "Not Spam"
    sentiment: str          # "Positive" | "Negative" | "Neutral"
    confidence: float       # 0.0 – 1.0
    all_scores: Optional[dict] = None


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.get("/health")
async def health():
    return {"status": "ok", "models_loaded": bool(models)}


@app.post("/moderate-comment", response_model=ModerationResponse)
async def moderate_comment(req: CommentRequest):
    if not models:
        raise HTTPException(status_code=503, detail="Models not loaded yet")

    try:
        result = predict_comment(req.comment, models)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Prediction error: {exc}")

    return ModerationResponse(**result)
