# AeroOps Copilot

Unified AI copilot for aviation safety & operations. Built as an LLM Course Project.

## About

AeroOps Copilot is a single AI assistant that flight crews, dispatchers, and safety officers can ask one natural-language question and get a grounded, regulation-aware answer — without juggling separate tools for SOP lookup, incident triage, and crew scheduling.

Under the hood, three specialized modules sit behind a single chat interface:

- **Looking up procedures** — ask about a Standard Operating Procedure (e.g. "what's the rejected-takeoff sequence for the 737?") and get an answer with citations from the actual SOP documents.
- **Making sense of incident reports** — drop in an ASRS-style narrative and the system extracts what happened, contributing factors, and severity into a structured form, then enriches it with related SOPs.
- **Catching fatigue risk in schedules** — upload a duty roster and the system flags rest-rule violations, scores fatigue risk, and surfaces the relevant regulations and mitigations.

An LLM-based intent router decides which module(s) to invoke and chains them together when a question spans more than one (e.g. an incident report that should be cross-checked against SOPs). The goal is to take work that today is split across PDFs, spreadsheets, and tribal knowledge and put it behind one interface that always cites its sources.

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

### Responsible AI use

Consistent with academic-integrity norms for AI-assisted work, we want to be explicit about how Claude was used and where the team stayed in the loop:

- **Reviewed, not rubber-stamped** — every AI-generated change was read, run, and tested by a team member before being committed. Nothing was merged sight-unseen.
- **Domain claims were verified by humans** — anything regulatory or safety-relevant (FAA/DGCA rest rules, SOP wording, fatigue-scoring thresholds) was checked against the source documents in `data/raw/sop/` and the cited regulations, not taken on the model's authority.
- **AI was a collaborator, not a source of truth** — Claude helped design pipelines, write code, and draft documentation. It did not generate the SOPs, ASRS reports, or regulatory text the system reasons over; those come from real published sources.
- **Outputs are grounded and cited** — the runtime system itself is built around retrieval + citation specifically so that *its* answers can be traced back to source documents rather than relying on the LLM's parametric memory.

In short: AI accelerated the build, humans owned the correctness.

## License

[MIT](LICENSE)
