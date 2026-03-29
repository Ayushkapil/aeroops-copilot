# Software Requirements Specification (SRS)

## AeroOps Copilot — AI-Powered Aviation Safety & Operations Assistant

| Field | Value |
|-------|-------|
| **Document Version** | 1.0 |
| **Date** | 2026-03-29 |
| **Author** | Ayush Kapil |
| **Repository** | [Ayushkapil/aeroops-copilot](https://github.com/Ayushkapil/aeroops-copilot) |
| **Status** | Draft |

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Overall Description](#2-overall-description)
3. [System Architecture](#3-system-architecture)
4. [Functional Requirements](#4-functional-requirements)
5. [API Specification](#5-api-specification)
6. [Non-Functional Requirements](#6-non-functional-requirements)
7. [Data Requirements](#7-data-requirements)
8. [Evaluation & Validation](#8-evaluation--validation)
9. [Appendices](#9-appendices)

---

## 1. Introduction

### 1.1 Purpose

This Software Requirements Specification (SRS) document provides a comprehensive description of the AeroOps Copilot system. It details the functional and non-functional requirements, system architecture, data requirements, and evaluation methodology. This document is intended for developers, evaluators, and stakeholders involved in the development and assessment of the system.

### 1.2 Scope

AeroOps Copilot is a modular AI system for aviation safety and operations. The system comprises three core modules unified under an agentic workflow:

- **Module A (SOP RAG Pipeline):** Retrieval-Augmented Generation system for answering aviation questions with cited references from standard operating procedures and regulatory documents.
- **Module B (Incident Analysis Engine):** Automated extraction of structured data from aviation incident report PDFs using LLM-based analysis.
- **Module C (Fatigue Risk Planner):** Assessment of pilot fatigue risk from duty schedules using hybrid rule-based and LLM reasoning.

The system features a React-based frontend and a FastAPI backend, with an LLM-powered intent router that automatically classifies and routes user inputs to the appropriate module.

### 1.3 Definitions, Acronyms, and Abbreviations

| Term | Definition |
|------|-----------|
| **AIM** | Aeronautical Information Manual (FAA publication) |
| **ASRS** | Aviation Safety Reporting System (NASA) |
| **NTSB** | National Transportation Safety Board |
| **SOP** | Standard Operating Procedure |
| **RAG** | Retrieval-Augmented Generation |
| **MRR** | Mean Reciprocal Rank |
| **F1** | F1 Score (harmonic mean of precision and recall) |
| **pgvector** | PostgreSQL extension for vector similarity search |
| **LLM** | Large Language Model |
| **TCAS** | Traffic Collision Avoidance System |
| **CFR** | Code of Federal Regulations |
| **AC** | Advisory Circular (FAA publication) |
| **PHAK** | Pilot's Handbook of Aeronautical Knowledge |
| **CSV** | Comma-Separated Values |
| **PDF** | Portable Document Format |

### 1.4 References

| # | Reference | URL |
|---|-----------|-----|
| 1 | FAA Aeronautical Information Manual | https://www.faa.gov/air_traffic/publications/atpubs/aim_html/ |
| 2 | FAA Pilot's Handbook of Aeronautical Knowledge | https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/phak |
| 3 | FAA Advisory Circulars | https://www.faa.gov/regulations_policies/advisory_circulars |
| 4 | NASA Aviation Safety Reporting System | https://asrs.arc.nasa.gov |
| 5 | NTSB Accident Reports | https://www.ntsb.gov |
| 6 | SKYbrary Aviation Safety | https://skybrary.aero |
| 7 | 14 CFR Part 117 — Flight and Duty Limitations | https://www.ecfr.gov/current/title-14/chapter-I/subchapter-G/part-117 |
| 8 | FAA AC 117-1 — Flightcrew Member Rest | https://www.faa.gov |
| 9 | LangChain Documentation | https://docs.langchain.com |
| 10 | pgvector Documentation | https://github.com/pgvector/pgvector |

---

## 2. Overall Description

### 2.1 Product Perspective

AeroOps Copilot is a standalone web application that integrates multiple AI capabilities into a unified aviation safety assistant. It is designed as a project to demonstrate the application of modern AI techniques (RAG, LLM-based extraction, hybrid scoring) in the aviation domain.

The system interacts with:
- **Users** via a React web frontend
- **External LLM APIs** (OpenAI or compatible) via LangChain
- **PostgreSQL + pgvector** database for vector storage and retrieval
- **File uploads** (PDF incident reports, CSV schedules) from users

### 2.2 User Classes and Characteristics

| User Class | Description | Technical Level |
|------------|-------------|-----------------|
| **Pilots** | Query SOPs, upload schedules for fatigue assessment | Low–Medium |
| **Safety Officers** | Analyse incident reports, review fatigue risk assessments | Medium |
| **Operations Personnel** | Schedule planning, regulatory compliance checking | Medium |
| **Researchers / Evaluators** | Assess system performance using evaluation suite | High |
| **Developers** | Extend, maintain, and deploy the system | High |

### 2.3 Operating Environment

- **Client:** Modern web browser (Chrome 90+, Firefox 90+, Safari 15+, Edge 90+)
- **Server:** Linux-based container environment (Docker)
- **Database:** PostgreSQL 15+ with pgvector extension
- **Python:** 3.11+
- **Node.js:** 18+

### 2.4 Design and Implementation Constraints

| Constraint | Description |
|-----------|-------------|
| **LLM Dependency** | System requires access to an LLM API (OpenAI or compatible) |
| **Embedding Model** | Must be consistent across ingestion and retrieval (same model) |
| **Database** | PostgreSQL with pgvector extension required |
| **Free Tier Limits** | Supabase free tier: 500 MB database, limited API requests |
| **PDF Quality** | Module B requires text-based PDFs (not scanned images) |
| **CSV Format** | Module C expects specific column format for schedule data |

### 2.5 Assumptions and Dependencies

| # | Assumption / Dependency |
|---|------------------------|
| 1 | Users have a stable internet connection |
| 2 | OpenAI API (or compatible LLM API) is available and accessible |
| 3 | FAA/NASA/NTSB data sources remain publicly accessible |
| 4 | Supabase free tier is sufficient for development and demonstration |
| 5 | Uploaded PDFs contain extractable text (not scanned images) |
| 6 | Pilot schedule CSVs follow the documented column format |

---

## 3. System Architecture

### 3.1 High-Level Architecture

```
┌─────────────────┐     REST API      ┌─────────────────────┐
│  React Frontend │ ◄──────────────────► │   FastAPI Backend    │
│  (Vercel)       │                   │   (Render)           │
└─────────────────┘                   └──────────┬──────────┘
                                                  │
                              ┌────────────────────┼────────────────────┐
                              │                    │                    │
                      ┌───────▼──────┐   ┌────────▼───────┐  ┌────────▼───────┐
                      │   Module A   │   │   Module B     │  │   Module C     │
                      │   SOP RAG    │   │   Incident     │  │   Fatigue      │
                      └───────┬──────┘   └────────┬───────┘  └────────┬───────┘
                              │                    │                    │
                      ┌───────▼──────┐             │                   │
                      │  pgvector    │   ┌─────────▼──────────┐        │
                      │  (Supabase)  │   │  Chain B → A       │        │
                      └──────────────┘   └────────────────────┘        │
                                                          ┌────────────▼────────┐
                                                          │  Chain C → A        │
                                                          └─────────────────────┘
```

### 3.2 Module Architecture

#### Module A — SOP RAG Pipeline

```
User Query → Embedding Model → pgvector Search (top-20) → Cross-Encoder Reranker → Top-5 Chunks → LLM Generation → Structured Response
```

#### Module B — Incident Analysis Engine

```
PDF Upload → PyMuPDF Extraction → LLM Structured Extraction → Pydantic Validation → Structured Output → Chain B → A
```

#### Module C — Fatigue Risk Planner

```
CSV Upload → Rule-Based Scorer (0–100) → LLM Reasoning → Risk Classification → Chain C → A (if HIGH)
```

### 3.3 Intent Router (Agentic Workflow)

| Input Type | Classification | Routed To |
|-----------|---------------|-----------|
| Text query | `intent: sop_query` | Module A |
| PDF file upload | `intent: incident_report` | Module B → Module A |
| CSV file upload | `intent: fatigue_schedule` | Module C → Module A (conditional) |

### 3.4 Cross-Module Chains

**Chain B → A:** Module B completes incident analysis → event tags + phase of flight → auto-retrieve relevant SOPs.

**Chain C → A:** Module C detects HIGH fatigue risk (score ≥ 70) → auto-retrieve rest requirement regulations from FAA AC 117-1 and 14 CFR Part 117.

---

## 4. Functional Requirements

### 4.1 Module A — SOP RAG Pipeline

| ID | Requirement | Priority |
|----|------------|----------|
| FR-A01 | System SHALL accept free-text aviation queries from users | Must |
| FR-A02 | System SHALL generate vector embeddings for user queries using the configured embedding model | Must |
| FR-A03 | System SHALL retrieve top-20 candidate chunks from pgvector using cosine similarity | Must |
| FR-A04 | System SHALL rerank candidate chunks using cross-encoder model and select top-5 | Must |
| FR-A05 | System SHALL generate natural language answers using LLM with retrieved chunks as context | Must |
| FR-A06 | System SHALL include inline citations (source document, chunk ID, relevance score) | Must |
| FR-A07 | System SHALL return a confidence score (0.0–1.0) with each response | Should |
| FR-A08 | System SHALL support session-based conversation context | Should |
| FR-A09 | System SHALL display cited source chunks in a collapsible citation panel | Should |

### 4.2 Module B — Incident Analysis Engine

| ID | Requirement | Priority |
|----|------------|----------|
| FR-B01 | System SHALL accept PDF file uploads of aviation incident reports | Must |
| FR-B02 | System SHALL extract raw text from uploaded PDFs using PyMuPDF | Must |
| FR-B03 | System SHALL use LLM to extract structured data from incident narratives | Must |
| FR-B04 | System SHALL validate extracted data against Pydantic schema | Must |
| FR-B05 | System SHALL extract: timeline, phase of flight, event tags, contributing factors, sop_links | Must |
| FR-B06 | System SHALL auto-chain to Module A to retrieve relevant SOPs based on extracted tags | Must |
| FR-B07 | System SHALL display incident timeline in a visual timeline component | Should |
| FR-B08 | System SHALL handle malformed or unreadable PDFs gracefully with user feedback | Should |
| FR-B09 | System SHALL reject non-PDF file uploads with appropriate error message | Must |

### 4.3 Module C — Fatigue Risk Planner

| ID | Requirement | Priority |
|----|------------|----------|
| FR-C01 | System SHALL accept CSV file uploads of pilot duty schedules | Must |
| FR-C02 | System SHALL parse CSV columns: date, duty_start, duty_end, rest_before, rest_after | Must |
| FR-C03 | System SHALL compute fatigue score (0–100) for each duty period using rule-based scoring | Must |
| FR-C04 | System SHALL compute an overall schedule fatigue risk score | Must |
| FR-C05 | System SHALL classify risk as LOW (0–39), MODERATE (40–69), or HIGH (70–100) | Must |
| FR-C06 | System SHALL use LLM to generate contextual reasoning for the risk assessment | Must |
| FR-C07 | System SHALL provide specific mitigation recommendations | Must |
| FR-C08 | System SHALL auto-chain to Module A for rest regulations when risk is HIGH | Must |
| FR-C09 | System SHALL display fatigue scores in a dashboard with visual indicators | Should |
| FR-C10 | System SHALL reject malformed CSV files with descriptive error messages | Must |

### 4.4 Intent Router

| ID | Requirement | Priority |
|----|------------|----------|
| FR-R01 | System SHALL classify user input intent using LLM-based classification | Must |
| FR-R02 | System SHALL route text queries to Module A | Must |
| FR-R03 | System SHALL route PDF uploads to Module B | Must |
| FR-R04 | System SHALL route CSV uploads to Module C | Must |
| FR-R05 | System SHALL handle ambiguous inputs by defaulting to Module A with a clarification prompt | Should |

### 4.5 Frontend

| ID | Requirement | Priority |
|----|------------|----------|
| FR-F01 | System SHALL provide a chat interface for text-based queries (Module A) | Must |
| FR-F02 | System SHALL provide a file upload interface for PDF reports (Module B) | Must |
| FR-F03 | System SHALL provide a file upload interface for CSV schedules (Module C) | Must |
| FR-F04 | System SHALL display incident analysis results in a structured IncidentViewer component | Must |
| FR-F05 | System SHALL display fatigue risk results in a FatigueDashboard component | Must |
| FR-F06 | System SHALL display source citations in a collapsible CitationPanel | Should |
| FR-F07 | System SHALL provide a navigation sidebar for switching between modules | Must |
| FR-F08 | System SHALL be responsive across desktop and tablet screen sizes | Should |
| FR-F09 | System SHALL show loading states during API calls | Must |

---

## 5. API Specification

### POST /api/chat

Send a text query to Module A (SOP RAG Pipeline).

**Request Body:**
```json
{
  "query": "string (required)",
  "session_id": "string (optional)"
}
```

**Response (200 OK):**
```json
{
  "answer": "string",
  "citations": [
    {
      "source": "string",
      "chunk_id": "string",
      "text": "string",
      "relevance_score": 0.95
    }
  ],
  "module": "A",
  "confidence": 0.87,
  "session_id": "string"
}
```

### POST /api/upload/incident

Upload an incident report PDF for Module B analysis.

**Request:** multipart/form-data with `file` (PDF, max 10 MB)

**Response (200 OK):**
```json
{
  "incident_analysis": {
    "timeline": [{"time": "string", "event": "string"}],
    "phase_of_flight": "string",
    "event_tags": ["string"],
    "contributing_factors": ["string"],
    "sop_links": ["string"]
  },
  "related_sops": {
    "answer": "string",
    "citations": []
  },
  "module": "B",
  "chained_to": "A"
}
```

### POST /api/upload/schedule

Upload a pilot schedule CSV for Module C fatigue assessment.

**Request:** multipart/form-data with `file` (CSV, max 5 MB)

**Response (200 OK):**
```json
{
  "fatigue_assessment": {
    "overall_risk_score": 72,
    "risk_level": "HIGH",
    "duty_periods": [
      {
        "date": "2026-03-15",
        "duty_hours": 12.5,
        "rest_before": 8.0,
        "score": 75,
        "flags": ["extended_duty", "insufficient_rest"]
      }
    ],
    "reasoning": "string",
    "mitigations": ["string"],
    "regulatory_references": ["string"]
  },
  "related_regulations": {
    "answer": "string",
    "citations": []
  },
  "module": "C",
  "chained_to": "A"
}
```

### POST /api/route

Unified agentic endpoint — auto-classifies and routes to the appropriate module.

**Request:** multipart/form-data with `query` (optional) and `file` (optional). At least one required.

**Response:** Same as routed module, plus:
```json
{
  "routed_to": "A | B | C",
  "intent": "sop_query | incident_report | fatigue_schedule"
}
```

### GET /api/health

**Response (200 OK):**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "modules": {"module_a": "operational", "module_b": "operational", "module_c": "operational"},
  "database": "connected"
}
```

---

## 6. Non-Functional Requirements

### 6.1 Performance

| ID | Requirement | Target |
|----|------------|--------|
| NFR-P01 | Module A query response time | < 5 seconds |
| NFR-P02 | Module B PDF analysis time | < 15 seconds (≤ 10 pages) |
| NFR-P03 | Module C schedule assessment time | < 10 seconds (≤ 30 days) |
| NFR-P04 | Frontend initial page load | < 3 seconds |
| NFR-P05 | Intent router classification | < 1 second |
| NFR-P06 | pgvector similarity search | < 500 ms |

### 6.2 Security

| ID | Requirement |
|----|------------|
| NFR-S01 | API keys and secrets SHALL NOT be committed to version control |
| NFR-S02 | Environment variables SHALL be used for all sensitive configuration |
| NFR-S03 | Uploaded files SHALL be validated for type and size before processing |
| NFR-S04 | CORS SHALL be configured to allow only the frontend origin |

### 6.3 Scalability

| ID | Requirement |
|----|------------|
| NFR-SC01 | System SHALL support at least 10 concurrent users |
| NFR-SC02 | Vector database SHALL support at least 50,000 embedded chunks |
| NFR-SC03 | System architecture SHALL support horizontal scaling via containerisation |

### 6.4 Maintainability

| ID | Requirement |
|----|------------|
| NFR-M01 | Code SHALL follow PEP 8 style guidelines (Python) |
| NFR-M02 | All modules SHALL be independently testable |
| NFR-M03 | Docker configuration SHALL allow single-command deployment |
| NFR-M04 | API docs SHALL be auto-generated via FastAPI/Swagger |
| NFR-M05 | LLM provider SHALL be swappable via LangChain abstraction |

---

## 7. Data Requirements

### 7.1 Data Source Inventory

| Source | Format | Module(s) | Est. Volume |
|--------|--------|-----------|-------------|
| FAA AIM | PDF | A | ~3,000 chunks |
| FAA PHAK | PDF | A | ~1,500 chunks |
| FAA Advisory Circulars | PDF | A | ~2,000 chunks |
| SKYbrary Articles | HTML/PDF | A | ~1,500 chunks |
| NASA ASRS Reports | Text/PDF | B, C | ~200 reports |
| NTSB Accident Reports | PDF | B | ~100 reports |
| FAA AC 117-1 | PDF | C | ~50 chunks |

**Total Estimated Chunks:** ~8,050+

### 7.2 Database Schema

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE sop_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_document VARCHAR(255) NOT NULL,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    embedding VECTOR(1536),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(source_document, chunk_index)
);

CREATE INDEX ON sop_chunks
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);

CREATE TABLE incident_analyses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    filename VARCHAR(255),
    raw_text TEXT,
    analysis JSONB NOT NULL,
    sop_recommendations JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE fatigue_assessments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    filename VARCHAR(255),
    schedule_data JSONB NOT NULL,
    assessment JSONB NOT NULL,
    regulation_references JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE chat_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    messages JSONB DEFAULT '[]',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

---

## 8. Evaluation & Validation

### 8.1 Research Questions

**RQ1:** Does cross-encoder reranking improve RAG retrieval quality?
- Module A | 50 aviation questions | Citation Accuracy, MRR@5

**RQ2:** Can LLM-based extraction match human-labelled incident analysis?
- Module B | 30 ASRS reports | Tag Accuracy, Timeline F1

**RQ3:** How accurately does the fatigue scorer predict fatigue-related incidents?
- Module C | 40 ASRS fatigue-tagged cases | Precision, Recall, F1

### 8.2 Acceptance Criteria

| Criterion | Threshold |
|-----------|-----------|
| Module A MRR@5 with reranker | ≥ 0.70 |
| Module A citation accuracy | ≥ 80% |
| Module B tag accuracy | ≥ 0.80 |
| Module B timeline F1 | ≥ 0.75 |
| Module C fatigue F1 | ≥ 0.70 |

---

## 9. Appendices

### Appendix A: Fatigue Scoring Rules (Module C)

| Factor | Scoring Rule | Weight |
|--------|-------------|--------|
| Duty period length | > 10 hrs: +10; > 12 hrs: +20; > 14 hrs: +35 | High |
| Rest before duty | < 10 hrs: +15; < 8 hrs: +30 | High |
| Time of day (WOCL) | Duty during 02:00–06:00: +20 | Medium |
| Consecutive duty days | > 5 days: +10; > 6 days: +25 | Medium |
| Cumulative duty (7-day) | > 50 hrs: +15; > 60 hrs: +30 | High |
| Time zone crossings | > 3 zones: +10; > 6 zones: +20 | Medium |

Score: **0–39** LOW | **40–69** MODERATE | **70–100** HIGH

---

*End of Software Requirements Specification*