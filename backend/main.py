"""AeroOps Copilot — FastAPI Backend."""

import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db_client = None


def get_db():
    global db_client
    if db_client is None:
        from db.pgvector_client import PgVectorClient
        db_client = PgVectorClient()
        try:
            db_client.init_db()
        except Exception as e:
            logger.warning(f"DB init failed (may not be running): {e}")
    return db_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("AeroOps Copilot starting up...")
    try:
        get_db()
    except Exception:
        logger.warning("Database not available at startup")
    yield
    if db_client:
        db_client.close()


app = FastAPI(
    title="AeroOps Copilot",
    description="Unified AI copilot for aviation safety & operations",
    version="1.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    intent: str
    module: str
    response: dict
    chained_results: Optional[dict] = None
    sources: list = []

class HealthResponse(BaseModel):
    status: str


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    return {"status": "ok"}


@app.get("/api/sources")
async def get_sources():
    try:
        db = get_db()
        sources = db.get_all_sources()
        return {"sources": sources}
    except Exception as e:
        return {"sources": [], "error": str(e)}


@app.post("/api/query", response_model=QueryResponse)
async def handle_query(req: QueryRequest):
    """Text query → intent router → response."""
    try:
        from router.intent_router import route_query
        result = route_query(req.query, get_db())
        return result
    except Exception as e:
        logger.error(f"Query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/query/checklist")
async def query_checklist(req: QueryRequest):
    """Text query → retrieve checklist-relevant chunks → structured output."""
    try:
        from modules.module_a.retriever import SOPRetriever
        from modules.module_a.reranker import rerank
        from modules.module_a.checklist_generator import generate_checklist

        retriever = SOPRetriever(get_db())
        chunks = retriever.retrieve_checklist(req.query, top_k=30)
        ranked = rerank(req.query, chunks, top_k=8)
        result = generate_checklist(req.query, ranked)

        return {
            "intent": "checklist_query",
            "module": "A",
            "response": result,
            "sources": result.get("citations", []),
        }
    except Exception as e:
        logger.error(f"Checklist query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/upload/incident")
async def upload_incident(file: UploadFile = File(...), query: Optional[str] = Form(None)):
    """PDF upload → Module B (incident analysis) → Chain B→A (SOP enrichment)."""
    try:
        from modules.module_b.extractor import extract_text_from_pdf
        from modules.module_b.analyzer import analyze_incident
        from modules.module_b.large_doc_analyzer import analyze_large_incident
        from pipelines.chain_b_to_a import enrich_with_sop

        content = await file.read()

        if file.filename.endswith(".pdf"):
            narrative = extract_text_from_pdf(content)
        else:
            narrative = content.decode("utf-8", errors="ignore")

        if not narrative.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from file")

        # Choose analyzer based on document size
        if len(narrative) > 15000:
            logger.info(f"Large document ({len(narrative)} chars), using chunk-and-merge")
            analysis = analyze_large_incident(narrative)
        else:
            analysis = analyze_incident(narrative)

        # Chain B→A: enrich with SOP excerpts
        try:
            enriched = enrich_with_sop(analysis, get_db())
        except Exception as e:
            logger.warning(f"SOP enrichment failed: {e}")
            enriched = analysis
            enriched["sop_enrichment"] = []

        return {
            "intent": "incident_analysis",
            "module": "B",
            "response": enriched,
            "chained_results": {"sop_enrichment": enriched.get("sop_enrichment", [])},
            "sources": [],
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Incident upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/upload/schedule")
async def upload_schedule(file: UploadFile = File(...)):
    """CSV upload → Module C (fatigue scoring) → Chain C→A (regulation lookup)."""
    try:
        from modules.module_c.validator import validate_schedule
        from modules.module_c.scorer import score_schedule
        from modules.module_c.llm_reasoner import reason
        from pipelines.chain_c_to_a import enrich_with_regulations

        content = await file.read()

        validation = validate_schedule(content)
        if not validation["valid"]:
            raise HTTPException(status_code=400, detail={"errors": validation["errors"]})

        assessment = score_schedule(validation["data"])

        if assessment["entries"]:
            worst = max(assessment["entries"], key=lambda x: x["score"])
            llm_result = reason(
                worst["score"],
                worst["risk_level"],
                worst["entry"],
                worst["violations"],
            )
            assessment["llm_reasoning"] = llm_result

        try:
            enriched = enrich_with_regulations(assessment, get_db())
        except Exception as e:
            logger.warning(f"Regulation enrichment failed: {e}")
            enriched = assessment
            enriched["regulation_enrichment"] = []

        return {
            "intent": "fatigue_assessment",
            "module": "C",
            "response": enriched,
            "chained_results": {"regulation_enrichment": enriched.get("regulation_enrichment", [])},
            "sources": [],
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Schedule upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
