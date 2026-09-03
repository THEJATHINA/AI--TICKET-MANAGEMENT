<h1 align="center">
  <br>
  🤖 SupportPilot AI
  <br>
  <sub><sup>AI-Powered Customer Support Platform with Ticket Resolution Agent</sup></sub>
</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black" />
  <img src="https://img.shields.io/badge/Vite-8-646CFF?style=for-the-badge&logo=vite&logoColor=white" />
  <img src="https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white" />
  <img src="https://img.shields.io/badge/Groq-Llama%203.3%2070B-F55036?style=for-the-badge&logo=meta&logoColor=white" />
  <img src="https://img.shields.io/badge/Jira-Atlassian%20API-0052CC?style=for-the-badge&logo=jira&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" />
</p>

<p align="center">
  <b>SupportPilot</b> is a production-grade, multi-agent AI system that fully automates IT support ticket workflows — from intelligent classification and LLM-driven resolution to Jira escalation and automated email notifications.
</p>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Live Architecture](#-live-architecture)
- [Key Features](#-key-features)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [AI Agent Pipeline](#-ai-agent-pipeline)
- [Escalation Logic](#-escalation-logic)
- [API Reference](#-api-reference)
- [Getting Started](#-getting-started)
- [Frontend Pages](#-frontend-pages)
- [Integrations](#-integrations)
- [Database Schema](#-database-schema)
- [Testing](#-testing)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌐 Overview

**SupportPilot** is an AI-powered enterprise IT helpdesk system built during the **Infosys Internship Project**. It replaces manual IT ticket triaging with a fully automated, multi-agent AI pipeline that:

- **Classifies** tickets instantly using rule-based NLP (Networking, Hardware, Password Reset, Software, Security, etc.)
- **Retrieves** relevant KB articles using Sentence Transformer embeddings (RAG)
- **Resolves** tickets autonomously with Groq's Llama 3.3 70B LLM
- **Escalates** unresolvable tickets to human teams, automatically creating Jira issues
- **Notifies** users via automated Gmail SMTP emails at every stage

> **Before SupportPilot:** IT agents manually read, categorize, research, reply, and create Jira issues — taking 20–60 minutes per ticket.
> **After SupportPilot:** The entire pipeline completes in **< 5 seconds** per ticket.

---

## 🏗 Live Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        USER BROWSER                                 │
│              React 19 + Vite  (localhost:5173)                      │
└────────────────────────┬────────────────────────────────────────────┘
                         │  REST API calls
          ┌──────────────▼──────────────────────────────┐
          │         FastAPI — RAG Backend                │
          │    (localhost:8000)  —  Main API Server      │
          │                                              │
          │  ┌─────────────────────────────────────┐    │
          │  │         AI Orchestrator              │    │
          │  │                                      │    │
          │  │  [1] Diagnosis Agent                 │    │
          │  │         ↓                            │    │
          │  │  [2] Retrieval Agent (RAG)           │    │
          │  │         ↓                            │    │
          │  │  [3] Resolution Agent (Groq LLM)     │    │
          │  │         ↓                            │    │
          │  │  [4] Escalation Agent                │    │
          │  └─────────────┬───────────────────────┘    │
          │                │                             │
          │     ┌──────────▼──────────┐                 │
          │     │  External Services  │                 │
          │     │  - Jira REST API    │                 │
          │     │  - Gmail SMTP       │                 │
          │     └─────────────────────┘                 │
          └──────────────┬──────────────────────────────┘
                         │
          ┌──────────────▼──────────────────────────────┐
          │         FastAPI — Classify Backend           │
          │    (localhost:8001)  —  Diagnosis API        │
          └──────────────┬──────────────────────────────┘
                         │
          ┌──────────────▼──────────────────────────────┐
          │              MySQL Database                  │
          │  Tables: tickets, users, ticket_responses,  │
          │          escalations, jira_tickets,          │
          │          workflow_logs, feedback             │
          └─────────────────────────────────────────────┘
```

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🧠 **Multi-Agent AI Pipeline** | 4 specialized agents chained: Diagnosis → Retrieval → Resolution → Escalation |
| 🔍 **Intelligent Classification** | Rule-based NLP with weighted symptom matching across 6+ IT categories |
| 📚 **RAG-Powered Resolution** | Sentence Transformer embeddings + SQLite KB search feeds context to the LLM |
| 🤖 **LLM Resolution (Groq)** | Llama 3.3 70B generates step-by-step resolutions in under 2 seconds |
| 📊 **Real-Time Dashboard** | Live metrics: total, open, resolved, escalated tickets + severity breakdown |
| 🎫 **Jira Auto-Integration** | Escalated tickets automatically create Jira issues via Atlassian REST API v3 |
| 📧 **Gmail SMTP Automation** | Automated resolution and escalation emails sent on every ticket action |
| 📈 **Analytics Dashboard** | AI confidence scores, category distribution, and ticket status trends |
| 🌍 **Multi-Language UI** | Interface supports English, Spanish, French, and German |
| 🌙 **Dark / Light Mode** | Full theme support with persistent user preferences |
| 🔌 **Live Integration Config** | Admin UI to configure Jira and Gmail credentials with test-connection validation |
| 📋 **Workflow Audit Logs** | Complete pipeline execution logs stored per ticket for auditability |

---

## 🛠 Technology Stack

### Backend

| Component | Technology | Version |
|-----------|-----------|---------|
| API Framework | FastAPI + Uvicorn | 0.115+ |
| ORM | SQLAlchemy | 2.x |
| LLM Provider | Groq API (Llama 3.3 70B Versatile) | Latest |
| Embeddings | Sentence Transformers (all-MiniLM-L6-v2) | 3.x |
| Vector Store | SQLite (local knowledge base) | — |
| Database | MySQL | 8.0+ |
| Email | Gmail SMTP via smtplib (SSL port 465) | stdlib |
| Jira | Atlassian REST API v3 | — |
| Environment | Python venv + python-dotenv | — |

### Frontend

| Component | Technology | Version |
|-----------|-----------|---------|
| Framework | React | 19.x |
| Build Tool | Vite | 8.x |
| Data Fetching | TanStack Query | 5.x |
| HTTP Client | Axios | 1.x |
| Icons | Lucide React | 1.x |
| Styling | Tailwind CSS v4 | 4.x |
| Font | Geist Variable | — |

---

## 📁 Project Structure

```
files/
├── ticket-app/                     # React Frontend (Vite)
│   ├── src/
│   │   ├── App.jsx                 # Main app with sidebar navigation
│   │   ├── components/
│   │   │   ├── TicketForm.jsx      # New ticket submission form
│   │   │   ├── ClassificationResults.jsx  # AI diagnosis display
│   │   │   ├── ResolutionPanel.jsx        # LLM resolution viewer
│   │   │   ├── AgentWorkflowPanel.jsx     # 4-agent pipeline UI
│   │   │   ├── DashboardOptimization.jsx  # Analytics dashboard
│   │   │   ├── IntegrationsPage.jsx       # Jira + Email config
│   │   │   └── SettingsPage.jsx           # User preferences
│   │   ├── api/
│   │   │   ├── ticketApi.js        # Ticket CRUD API calls
│   │   │   └── classifyApi.js      # Diagnosis API calls
│   │   └── lib/
│   │       └── validateTicket.js   # Client-side form validation
│   ├── package.json
│   └── vite.config.js
│
├── rag_module/                     # RAG + Main API Backend (Port 8000)
│   ├── app/
│   │   ├── main.py                 # FastAPI app entry point
│   │   ├── models.py               # SQLAlchemy ORM models
│   │   ├── schemas.py              # Pydantic request/response schemas
│   │   ├── database.py             # DB engine + session factory
│   │   ├── resolve.py              # Resolution router
│   │   ├── analytics_router.py     # Analytics endpoints
│   │   ├── integrations_router.py  # Jira + Email config endpoints
│   │   ├── agents/
│   │   │   ├── diagnose.py         # Diagnosis Agent (NLP classifier)
│   │   │   ├── diagnosis_rules.py  # Weighted symptom rules + KB mappings
│   │   │   ├── resolution_agent.py # Groq LLM resolution generator
│   │   │   ├── escalation_agent.py # Escalation decision engine
│   │   │   ├── retrieval_agent.py  # RAG KB retrieval
│   │   │   ├── prompts.py          # LLM system/user prompts
│   │   │   └── confidence.py       # Confidence scoring utilities
│   │   └── services/
│   │       ├── resolution_workflow_service.py  # Full pipeline orchestrator
│   │       ├── jira_service.py     # Atlassian Jira API client
│   │       ├── email_service.py    # Gmail SMTP client
│   │       ├── vector_search.py    # Sentence Transformer vector search
│   │       ├── ingest.py           # KB article ingestion
│   │       └── kb_articles.py      # Knowledge base article store
│   ├── requirements.txt
│   └── .env
│
├── supportpilot-api_new_fast/      # Classification API Backend (Port 8001)
│   └── supportpilot-api/app/
│       └── main.py                 # Diagnosis-only FastAPI app
│
├── database/                       # SQL schema files
├── run_all.bat                     # One-click Windows startup
└── README.md                       # This file
```

---

## 🤖 AI Agent Pipeline

When a user clicks **"Resolve"** on a ticket, the `ResolutionWorkflowService` executes a chained 4-agent pipeline:

### Agent 1 — Diagnosis Agent

- Tokenizes and normalizes ticket subject + description
- Applies weighted symptom rules across 6 IT categories
- Computes a confidence score using: evidence share (50%) + margin (20%) + absolute evidence (30%)
- Outputs: predicted_category, confidence, matched_symptoms, suggested_kb_ids, suggested_priority

```python
# Example output
{
  "predicted_category": "Networking",
  "confidence": 0.82,
  "matched_symptoms": ["vpn", "keeps disconnecting"],
  "suggested_priority": "High"
}
```

### Agent 2 — Retrieval Agent (RAG)

- Uses Sentence Transformers (all-MiniLM-L6-v2) to embed the ticket description
- Performs cosine similarity search against the embedded KB article store
- Returns top-N relevant KB article chunks as context for the LLM

### Agent 3 — Resolution Agent

- Constructs a rich prompt: ticket description + KB context + category metadata
- Calls Groq API (Llama 3.3 70B Versatile) with a structured system prompt
- Stores the generated resolution in the ticket_responses table

### Agent 4 — Escalation Agent

- Applies a deterministic 5-rule decision tree
- If escalated → calls Jira Service → sends escalation email
- If resolved → updates ticket status to RESOLVED → sends resolution email
- All steps logged to workflow_logs for audit

---

## 🚦 Escalation Logic

| Rule | Condition | Action | Team |
|------|-----------|--------|------|
| **Rule 0** | Category is Hardware or Security | Always escalate | Hardware Support / Security Operations |
| **Rule 1** | LLM resolution failed | Escalate | Level 2 Support |
| **Rule 2** | Confidence < 70% (< 45% for routine IT) | Escalate | Level 2 Support |
| **Rule 3** | Priority is P1 (Critical) | Escalate | Priority Support |
| **Rule 4** | Severity is CRITICAL | Escalate | Critical Incident Team |
| **Rule 5** | LLM explicitly recommends human review | Escalate | Level 2 Support |
| **Default** | None triggered | Auto-resolve | — |

**Auto-Resolve:** Networking, Password Reset, Software, Email, Access & Permissions
**Always-Escalate:** Hardware, Security

---

## 📡 API Reference

### Ticket Management

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/tickets | Create a new support ticket |
| GET | /api/tickets | List all tickets |
| GET | /api/tickets/{id} | Get a specific ticket |
| POST | /api/tickets/{id}/resolve | Trigger the full AI resolution pipeline |
| GET | /api/tickets/{id}/workflow | Get workflow logs, agent statuses, integrations |
| POST | /api/tickets/{id}/feedback | Submit resolution feedback |

### Ticket Create — Request

```json
POST /api/tickets
{
  "subject": "VPN keeps disconnecting during remote work",
  "description": "My VPN disconnects every 10 minutes on a stable fiber connection.",
  "requester_email": "john.doe@company.com",
  "department": "IT"
}
```

### Ticket Create — Response

```json
{
  "ticket_id": 42,
  "subject": "VPN keeps disconnecting during remote work",
  "status": "OPEN",
  "priority": "P3",
  "severity": "MEDIUM",
  "created_at": "2026-09-03T17:00:00"
}
```

### Ticket Resolve — Response

```json
{
  "ticket_id": 42,
  "status": "RESOLVED",
  "generated_response": "Step 1: Check your VPN client version...",
  "confidence_score": 0.84,
  "escalated": false,
  "assigned_team": null
}
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+ and npm
- MySQL 8.0+
- Git

### Environment Configuration

**RAG Backend — `rag_module/.env`**

```env
# MySQL Database
DB_HOST=127.0.0.1
DB_PORT=3306
DB_NAME=supportpilot
DB_USER=root
DB_PASSWORD=your_mysql_password

# Groq LLM API (free at console.groq.com)
GROQ_API_KEY=your_groq_api_key_here

# Gmail SMTP
GMAIL_ADDRESS=your.support@gmail.com
GMAIL_APP_PASSWORD=your_16_char_app_password

# Jira Integration
JIRA_URL=https://your-org.atlassian.net
JIRA_EMAIL=admin@your-org.com
JIRA_API_TOKEN=your_jira_api_token
JIRA_PROJECT_KEY=SCRUM
```

**Frontend — `ticket-app/.env`**

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_CLASSIFY_API_URL=http://localhost:8001
```

### Database Setup

```bash
mysql -u root -p -e "CREATE DATABASE supportpilot CHARACTER SET utf8mb4;"
mysql -u root -p supportpilot < database/supportpilot_schema_v2.sql
```

### Running the Application

#### Option A — One-Click (Windows)

```batch
run_all.bat
```

Starts all 3 services. Visit http://localhost:5173 after ~30 seconds.

#### Option B — Manual

```bash
# Terminal 1 — RAG Backend (Port 8000)
cd rag_module
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --port 8000 --host 127.0.0.1

# Terminal 2 — Classification Backend (Port 8001)
cd supportpilot-api_new_fast/supportpilot-api
python -m venv venv
venv\Scripts\activate
uvicorn app.main:app --port 8001 --host 127.0.0.1

# Terminal 3 — React Frontend (Port 5173)
cd ticket-app
npm install
npm run dev
```

---

## 🖥 Frontend Pages

| Page | Description |
|------|-------------|
| **Dashboard** | Real-time metrics: total/open/resolved/escalated + severity breakdown |
| **Tickets** | Ticket list with search/filter + new ticket form + AI classification panel |
| **AI Agent** | Full-screen 4-agent pipeline view with live logs and integration status |
| **Integrations** | Admin config for Jira URL/credentials and Gmail SMTP |
| **Analytics** | AI classification analytics with confidence scores and category distribution |
| **Settings** | Dark/light mode, language (EN/ES/FR/DE), notification preferences |

---

## 🔌 Integrations

### Jira (Atlassian REST API v3)

On escalation:
1. Creates a Jira issue with ticket details and escalation reason
2. Stores the Jira issue key (e.g., SCRUM-42) in the database
3. Displays the key in the Agent Workflow panel
4. Includes the key in the escalation email

### Gmail SMTP

Three automated emails:
- **Ticket Received** — sent immediately on ticket creation
- **Resolution Email** — sent when AI auto-resolves
- **Escalation Email** — sent when ticket is escalated to a human team

---

## 🗄 Database Schema

| Table | Description |
|-------|-------------|
| users | Ticket requester accounts (auto-created) |
| tickets | Core ticket records with status, priority, severity |
| ticket_responses | AI-generated resolutions with confidence scores |
| escalations | Escalation records with assigned team and reason |
| jira_tickets | Jira issue keys linked to escalated tickets |
| workflow_logs | Step-by-step agent execution audit trail |
| feedback | User satisfaction ratings |

---

## 🧪 Testing

```bash
cd rag_module
venv\Scripts\activate

# Run all tests
pytest

# Specific test files
pytest test_agents.py -v
pytest test_escalation.py -v

# Test Diagnosis Agent standalone
python -m app.agents.diagnose
```

**Swagger API Docs:**
- Main API: http://localhost:8000/docs
- Classification API: http://localhost:8001/docs

---

## 🤝 Contributing

Built as an **Infosys Internship Project** by a team of 5 members:

| Role | Contribution |
|------|-------------|
| Member 1 | React Frontend — UI, Ticket Form, Dashboard |
| Member 2 | Backend API — FastAPI, MySQL, ORM Models |
| Member 3 | Retrieval Agent — RAG, Sentence Transformers, KB ingestion |
| Member 4 | Diagnosis Agent — NLP classification, symptom rules |
| Member 5 | Resolution + Escalation Agents, Groq LLM, Jira + Email |

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Built with ❤️ using FastAPI, React, Groq LLM, and MySQL<br>
  <b>SupportPilot — Infosys Internship Project 2026</b>
</p>
