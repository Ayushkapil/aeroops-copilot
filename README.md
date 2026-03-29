<div align="center">

# ✈️ AeroOps Copilot

**A modular AI system for aviation safety & operations**

*Combining RAG-powered SOP retrieval, structured incident analysis, and fatigue risk planning into a unified intelligent copilot.*

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?logo=react&logoColor=black)](https://react.dev)
[![LangChain](https://img.shields.io/badge/LangChain-🦜-green)](https://langchain.com)
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)](https://docker.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Modules](#-modules)
- [Tech Stack](#️-tech-stack)
- [Repository Structure](#-repository-structure)
- [Getting Started](#-getting-started)
- [API Endpoints](#-api-endpoints)
- [Data Sources](#-data-sources)
- [Evaluation Plan](#-evaluation-plan)
- [Roadmap](#️-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌍 Overview

AeroOps Copilot is a modular AI system designed to assist aviation professionals with **safety-critical decision-making**. It integrates three specialised modules under an agentic workflow, where an LLM-based intent router dynamically classifies user input and orchestrates the appropriate pipeline(s).

### The Problem

Aviation professionals must navigate thousands of pages of SOPs, incident reports, and fatigue regulations — often under time pressure. Existing tools are fragmented and require manual lookup.

### The Solution

AeroOps Copilot provides a **single conversational interface** that can:
- Answer SOP questions with cited sources
- Analyse incident reports into structured intelligence
- Assess pilot schedules for fatigue risk with actionable mitigations

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🔍 **SOP RAG with Reranking** | Semantic search + cross-encoder reranking for precise, cited answers |
| 📄 **PDF Incident Analysis** | Upload an incident PDF → get structured JSON (timeline, tags, factors) |
| 😴 **Fatigue Risk Scoring** | Upload a pilot schedule CSV → rule-based + LLM risk assessment |
| 🔗 **Cross-Module Chaining** | Incident analysis auto-queries relevant SOPs; high fatigue auto-fetches rest regulations |
| 🤖 **Agentic Intent Router** | LLM classifier routes text/PDF/CSV to the right module(s) automatically |
| 📊 **Citation Panel** | Every RAG answer includes traceable source citations |

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    React Frontend                        │
│  ┌──────────┐  ┌────────────────┐  ┌─────────────────┐  │
│  │   Chat   │  │ IncidentViewer │  │ FatigueDashboard│  │
│  └────┬─────┘  └───────┬────────┘  └───────┬─────────┘  │
│       └────────────────┼────────────────────┘            │
└────────────────────────┼─────────────────────────────────┘
                         │ REST API
┌────────────────────────┼─────────────────────────────────┐
│                   FastAPI Backend                         │
│                        │                                  │
│              ┌─────────▼──────────┐                       │
│              │   Intent Router    │                       │
│              │  (LLM Classifier)  │                       │
│              └──┬──────┬───────┬──┘                       │
│                 │      │       │                          │
│        ┌────────▼┐  ┌──▼────┐  ┌▼────────┐               │
│        │Module A │  │Mod. B │  │Module C  │               │
│        │SOP RAG  │  │Incid. │  │Fatigue   │               │
│        └────┬────┘  └──┬────┘  └┬────────┘               │
│             │          │        │                         │
│             │    ┌─────▼────┐   │                         │
│             ◄────┤Chain B→A │   │                         │
│             │    └──────────┘   │                         │
│             │    ┌─────────────▼┐                         │
│             ◄────┤ Chain C→A    │                         │
│             │    └──────────────┘                         │
│        ┌────▼──────────────────────┐                      │
│        │  PostgreSQL + pgvector    │                      │
│        │      (Supabase)           │                      │
│        └───────────────────────────┘                      │
└───────────────────────────────────────────────────────────┘
```

### Agentic Workflow

```
User Input
    ↓
Intent Router (LLM classifier)
├── PDF uploaded       → Module B → auto-chains to Module A (SOP lookup)
├── CSV uploaded       → Module C → auto-chains to Module A (if high risk)
└── Text query         → Module A (direct RAG)
    ↓
Unified Response Formatter
    ↓
React Frontend
```

---

## 🧩 Modules

### Module A — SOP RAG Pipeline

> *"What are the fuel reserve requirements for IFR flights?"*

1. User asks an aviation question
2. Query is embedded → top-20 chunks retrieved from pgvector
3. Cross-encoder reranker selects top-5 most relevant chunks
4. LLM generates a grounded answer with **inline citations**

**Data**: FAA AIM, FAA Pilot Handbook, FAA Advisory Circulars, SKYbrary

### Module B — Incident Analysis Engine

> *Upload an ASRS incident PDF → get structured intelligence*

1. PyMuPDF extracts text from uploaded PDF
2. LLM extracts structured JSON fields
3. Pydantic validates the output schema

**Output Schema**:
```json
{
  "timeline": [...],
  "phase_of_flight": "approach",
  "event_tags": ["runway_incursion", "communication_failure"],
  "contributing_factors": ["fatigue", "inadequate_briefing"],
  "sop_links": ["AIM 4-3-18", "AC 91-73B"]
}
```

**Data**: NASA ASRS reports, NTSB accident reports

### Module C — Fatigue Risk Planner

> *Upload a pilot schedule CSV → get fatigue risk assessment*

1. Rule-based scorer calculates a fatigue score (0–100)
2. LLM provides contextual reasoning and risk classification
3. Mitigation recommendations are generated

**Risk Levels**: 🟢 Low (0–30) · 🟡 Moderate (31–60) · 🔴 High (61–100)

**Data**: NASA ASRS fatigue-tagged incidents, FAA AC 117-1

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 18 + TailwindCSS + shadcn/ui |
| **Backend** | FastAPI (Python 3.11+) |
| **LLM Interface** | LangChain (model-agnostic: GPT / Claude / Llama via Ollama) |
| **Embeddings** | OpenAI `text-embedding-ada-002` or `nomic-embed-text` |
| **Reranker** | `cross-encoder/ms-marco-MiniLM-L-6-v2` (HuggingFace) |
| **Vector DB** | PostgreSQL + pgvector (Supabase) |
| **PDF Parsing** | PyMuPDF |
| **Schema Validation** | Pydantic v2 |
| **Containerisation** | Docker + docker-compose |
| **Deployment** | Vercel (frontend) · Render (backend) · Supabase (DB) |

---

## 📁 Repository Structure

```
aeroops-copilot/
├── frontend/                        # React Application
│   ├── src/
│   │   ├── components/
│   │   │   ├── Chat/                # Chat interface components
│   │   │   ├── IncidentViewer/      # Incident analysis display
│   │   │   ├── FatigueDashboard/    # Fatigue risk visualisation
│   │   │   ├── CitationPanel/       # Source citation sidebar
│   │   │   └── Sidebar/            # Navigation sidebar
│   │   ├── pages/
│   │   │   ├── Home.jsx
│   │   │   ├── Chat.jsx
│   │   │   ├── UploadReport.jsx
│   │   │   └── UploadSchedule.jsx
│   │   └── api/                     # API client utilities
│   └── package.json
│
├── backend/
│   ├── main.py                      # FastAPI app entrypoint
│   ├── router/
│   │   └── intent_router.py         # LLM-based intent classification
│   ├── modules/
│   │   ├── module_a/                # SOP RAG Pipeline
│   │   │   ├── retriever.py         # pgvector similarity search
│   │   │   ├── reranker.py          # Cross-encoder reranking
│   │   │   └── generator.py         # LLM answer generation
│   │   ├── module_b/                # Incident Analysis Engine
│   │   │   ├── extractor.py         # PDF text extraction
│   │   │   ├── analyzer.py          # LLM structured extraction
│   │   │   └── schema.py            # Pydantic output schemas
│   │   └── module_c/                # Fatigue Risk Planner
│   │       ├── scorer.py            # Rule-based fatigue scoring
│   │       ├── llm_reasoner.py      # LLM contextual reasoning
│   │       └── validator.py         # Schedule validation
│   ├── pipelines/
│   │   ├── chain_b_to_a.py          # Incident → SOP chain
│   │   └── chain_c_to_a.py          # Fatigue → SOP chain
│   ├── ingestion/
│   │   ├── pdf_parser.py            # PDF document parsing
│   │   ├── chunker.py               # Text chunking strategies
│   │   └── embedder.py              # Embedding generation
│   ├── db/
│   │   └── pgvector_client.py       # Vector DB operations
│   └── requirements.txt
│
├── data/
│   ├── raw/                         # Original source documents
│   │   ├── asrs/                    # NASA ASRS reports
│   │   └── sop/                     # FAA SOPs & handbooks
│   └── processed/
│       ├── chunks/                  # Embedded text chunks
│       └── fatigue_cases/           # Processed fatigue data
│
├── evaluation/
│   ├── rq1_rag_eval.py              # RAG pipeline evaluation
│   ├── rq2_incident_eval.py         # Incident extraction evaluation
│   └── rq3_fatigue_eval.py          # Fatigue scoring evaluation
│
├── docs/
│   ├── architecture.md              # Detailed architecture docs
│   └── SRS.md                       # Software Requirements Specification
│
├── .env.example                     # Environment variable template
├── docker-compose.yml               # Container orchestration
├── LICENSE
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

| Requirement | Version |
|-------------|---------|
| Python | 3.11+ |
| Node.js | 18+ |
| Docker | Latest |
| OpenAI API Key | — (or use Ollama for local models) |

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/AyushKapil/aeroops-copilot.git
cd aeroops-copilot

# 2. Set up environment variables
cp backend/.env.example backend/.env
# Edit backend/.env with your API keys

# 3. Start the database (PostgreSQL + pgvector)
docker-compose up -d

# 4. Install and start the backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# 5. Install and start the frontend (in a new terminal)
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173` and the API at `http://localhost:8000`.

### Using Docker (Full Stack)

```bash
docker-compose --profile full up -d
```

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for embeddings & LLM | Yes* |
| `SUPABASE_URL` | Supabase project URL | Yes |
| `SUPABASE_KEY` | Supabase service role key | Yes |
| `OLLAMA_BASE_URL` | Ollama endpoint (if using local models) | No |
| `LLM_MODEL` | LLM model name (default: `gpt-4`) | No |
| `EMBEDDING_MODEL` | Embedding model name | No |
|
* *Not required if using Ollama for local inference*

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/query` | Send a text query (routed via intent router) |
| `POST` | `/api/upload/incident` | Upload an incident PDF for analysis |
| `POST` | `/api/upload/schedule` | Upload a pilot schedule CSV |
| `GET` | `/api/health` | Health check |
| `GET` | `/api/sources` | List available SOP data sources |

---

## 📦 Data Sources

| Module | Dataset | Source |
|--------|---------|--------|
| Module A | FAA AIM, Pilot Handbook, Advisory Circulars, SKYbrary | [faa.gov](https://www.faa.gov), [skybrary.aero](https://skybrary.aero) |
| Module B | NASA ASRS narratives, NTSB accident reports | [asrs.arc.nasa.gov](https://asrs.arc.nasa.gov), [ntsb.gov](https://www.ntsb.gov) |
| Module C | NASA ASRS fatigue-tagged incidents, FAA AC 117-1 | [asrs.arc.nasa.gov](https://asrs.arc.nasa.gov), [faa.gov](https://www.faa.gov) |

---

## 📊 Evaluation Plan

Three research questions guide the evaluation:

| RQ | Module | Method | Metrics |
|----|--------|--------|---------|
| **RQ1** | A — SOP RAG | RAG with vs. without reranker | Citation Accuracy, MRR@5 |
| **RQ2** | B — Incident | Module B vs. human-labelled ASRS baseline | Tag Accuracy, Timeline F1 |
| **RQ3** | C — Fatigue | Module C on ASRS fatigue-tagged incidents | Precision, Recall, F1 |

### Ground Truth Strategy
- **Module A**: Expert-curated Q&A pairs from FAA documents
- **Module B**: Human-labelled ASRS incident structure
- **Module C**: NASA ASRS fatigue-tagged incidents (avoids circular evaluation)

---

## 🗺️ Roadmap

- [x] Project architecture & design
- [x] Repository setup
- [ ] Data ingestion pipeline + pgvector setup
- [ ] Module A: SOP RAG with reranker
- [ ] Module B: Incident analysis engine
- [ ] Module C: Fatigue risk planner
- [ ] Intent router + cross-module chains
- [ ] React frontend (Chat, IncidentViewer, FatigueDashboard)
- [ ] Evaluation suite
- [ ] Deployment (Vercel + Render + Supabase)
- [ ] Demo & documentation

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ❤️ for aviation safety**

[Report Bug](https://github.com/AyushKapil/aeroops-copilot/issues) · [Request Feature](https://github.com/AyushKapil/aeroops-copilot/issues)

</div>
