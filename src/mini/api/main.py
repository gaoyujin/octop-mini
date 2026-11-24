"""M0: smallest FastAPI app — one liveness route."""

from __future__ import annotations

from fastapi import FastAPI

app = FastAPI(title="octop-mini", version="0.1.0")


@app.get("/health", summary="Health check")
async def health() -> dict[str, bool]:
    """Liveness probe; official Octop returns more fields — add those in later milestones."""
    return {"ok": True}