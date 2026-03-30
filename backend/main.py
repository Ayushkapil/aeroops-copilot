"""
AeroOps Copilot — FastAPI application entrypoint.

Start with:
    uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="AeroOps Copilot API",
    description="Modular AI system for aviation safety & operations",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "aeroops-copilot"}


@app.get("/api/sources")
async def list_sources():
    """List available SOP data sources (placeholder)."""
    return {"sources": []}


# Route includes will be added here as modules are implemented
# from router.intent_router import router as intent_router
# app.include_router(intent_router, prefix="/api")
