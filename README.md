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
