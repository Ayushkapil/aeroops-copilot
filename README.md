# AeroOps Copilot

Unified AI copilot for aviation safety & operations. Built as an LLM Course Project.

## Modules

| Module | Purpose |
|--------|---------|
| **A — SOP RAG Pipeline** | Answer aviation SOP/policy questions with cited sources |
| **B — Incident Analysis Engine** | Convert ASRS-style incident narratives into structured intelligence |
| **C — Fatigue Risk Planner** | Assess pilot duty schedules for fatigue risk with mitigations |

All modules are integrated through an LLM-based intent router with automatic cross-module chaining.

## Quick Start

### 1. Environment Setup

```bash
cp backend/.env.example backend/.env
# Edit backend/.env with your OPENAI_API_KEY
```

### 2. Start Database

```bash
docker-compose up -d db
```

### 3. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Ingest Sample SOPs

```bash
cd backend
python -m ingestion.ingest_cli --source ../data/raw/sop/
```

### 5. Start Backend

```bash
cd backend
uvicorn main:app --reload --port 8000
```

### 6. Start Frontend

```bash
cd frontend
npm install
npm run dev
```

Visit `http://localhost:5173`

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/health` | Health check |
| `GET` | `/api/sources` | List ingested SOP sources |
| `POST` | `/api/query` | Text query → intent router → response |
| `POST` | `/api/upload/incident` | PDF upload → incident analysis + SOP enrichment |
| `POST` | `/api/upload/schedule` | CSV upload → fatigue scoring + regulation lookup |

## Evaluation

```bash
python evaluation/rq1_rag_eval.py     # RAG pipeline metrics
python evaluation/rq2_incident_eval.py # Incident extraction metrics
python evaluation/rq3_fatigue_eval.py  # Fatigue scoring metrics
```

## Team

Bhavya Sri Kadavakolla, Sahana Madhugiri Shankar, Aryan Ashish Kathale, Ayush Kapileshwar, Linthoi Laishram

## Acknowledgments

This project was built collaboratively with **Claude** (Anthropic), which contributed at the same level as the rest of the team. Rather than enumerating every file or line, the contribution is best understood at the system level:

- **Architecture & module decomposition** — shaping the three-module split (SOP RAG, incident analysis, fatigue planning) and the intent-router pattern that ties them together with cross-module chaining.
- **Pipeline design** — ingestion, chunking, embedding, retrieval, and reranking choices for the RAG layer; structured-extraction schemas for incident analysis; scoring/validation flow for the fatigue planner.
- **Implementation across the stack** — backend services, FastAPI endpoints, Postgres + pgvector wiring, the unified frontend console, and Docker/compose/nginx packaging.
- **Iteration on hard parts** — debugging, refactors, and the judgment calls that come up when a prototype is being turned into something that actually runs end-to-end.

The human team owned the problem framing, domain decisions (aviation safety, regulatory grounding, evaluation criteria), and the final say on what shipped. The point of this note is to be honest about how the work happened, not to itemize it.

## License

[MIT](LICENSE)
