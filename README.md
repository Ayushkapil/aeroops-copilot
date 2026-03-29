# ✈️ AeroOps Copilot

A modular AI system for aviation operations that combines Retrieval-Augmented Generation (RAG), structured incident analysis, and fatigue risk planning into a unified intelligent copilot.

## 🧩 Modules

| Module | Purpose |
|--------|---------|
| **Module A — SOP RAG** | Answers aviation questions grounded in SOP documents with citations |
| **Module B — Incident Analyser** | Converts raw incident reports (PDF) into structured JSON insights |
| **Module C — Fatigue Planner** | Scores pilot schedules for fatigue risk and generates mitigation strategies |

## 🔄 Architecture

User input (text query or file upload) is routed through an **LLM-based intent router** that decides which module(s) to invoke. Modules can chain — e.g. an incident report automatically triggers Module B followed by Module A to surface relevant SOPs.

```
User Input → Intent Router → Module(s) → Cross-Module Chain → Unified Response
```

## 🛠️ Tech Stack

- **Frontend**: React + TailwindCSS
- **Backend**: FastAPI (Python)
- **LLM Interface**: LangChain (model-agnostic: GPT / Claude / Llama via Ollama)
- **Embeddings**: OpenAI text-embedding-ada-002 or nomic-embed-text
- **Reranker**: cross-encoder/ms-marco-MiniLM-L-6-v2
- **Vector DB**: PostgreSQL + pgvector
- **PDF Parsing**: PyMuPDF
- **Schema Validation**: Pydantic
- **Containerisation**: Docker + docker-compose

## 📦 Data Sources

- **NASA ASRS** — Aviation incident narratives (Module B + C ground truth)
- **FAA AIM + Handbooks** — SOP documents (Module A RAG)
- **FAA AC 117-1** — Fatigue rule parameters (Module C)
- **Synthetic schedules** — Generated based on FAA duty/rest limits (Module C)

## 🚀 Getting Started

### Prerequisites
- Docker + Docker Compose
- Python 3.11+
- Node.js 18+
- OpenAI API key (or Ollama for local models)

### 1. Clone the repository
```bash
git clone https://github.com/AyushKapil/aeroops-copilot.git
cd aeroops-copilot
```

### 2. Set up environment variables
```bash
cp backend/.env.example backend/.env
```

### 3. Start the database
```bash
docker-compose up -d
```

### 4. Install backend dependencies
```bash
cd backend && pip install -r requirements.txt
```

### 5. Start the backend
```bash
uvicorn main:app --reload
```

### 6. Install and start the frontend
```bash
cd frontend && npm install && npm run dev
```

## 📊 Evaluation

| RQ | Module | Method | Metric |
|----|--------|--------|--------|
| RQ1 | A | RAG with vs. without reranker | Citation accuracy, MRR |
| RQ2 | B | Module B vs. human-labelled ASRS baseline | Tag accuracy, Timeline F1 |
| RQ3 | C | Module C on ASRS fatigue-tagged incidents | Precision, Recall, F1 |

## 📄 License

MIT