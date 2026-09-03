# SupportPilot — Technical Q&A for Presentation

---

## 🏗️ ARCHITECTURE & OVERVIEW

---

### Q1. What is SupportPilot and what problem does it solve?

**Answer:**
SupportPilot is an AI-powered IT Helpdesk system built during the Infosys Internship. It automates the full lifecycle of a support ticket — from submission to resolution or escalation — without requiring manual intervention.

The problem it solves: Traditional helpdesks require support agents to manually read, classify, prioritize, and respond to every ticket. This is slow and error-prone. SupportPilot uses AI to do all of that automatically — classifying the ticket, searching a knowledge base for relevant solutions, generating a resolution, deciding if human escalation is needed, creating a Jira ticket if required, and sending email notifications — all within seconds.

---

### Q2. What is the overall architecture of the system?

**Answer:**
The system has three main layers:

1. **Frontend** — A React + Vite web app (runs on port 5173) where users submit tickets and view AI results on a dashboard.
2. **RAG Backend** — A FastAPI Python server (runs on port 8001) that handles the full AI pipeline: ticket creation, classification, resolution, escalation, Jira, and email.
3. **Database** — MySQL (`supportpilot` database) stores users, tickets, AI responses, escalations, Jira tickets, and workflow logs.

The AI pipeline flow is:
```
User submits ticket
  → Diagnosis Agent (classify & prioritize)
  → Retrieval Agent (semantic search in Knowledge Base)
  → Resolution Agent (LLM generates resolution via Groq)
  → Escalation Agent (decide: AI resolve or human escalate)
  → Jira Integration (create Jira ticket if escalated)
  → Email Notification (send email to requester)
  → Database Update (mark ticket RESOLVED or IN_PROGRESS)
```

---

### Q3. What tech stack did you use?

**Answer:**
- **Frontend:** React, Vite, TailwindCSS, TanStack Query (React Query), Lucide Icons
- **Backend:** Python, FastAPI, SQLAlchemy ORM, Uvicorn
- **Database:** MySQL (via PyMySQL driver)
- **AI / LLM:** Groq API (primary model: `openai/gpt-oss-120b`, fallback: `llama-3.1-8b-instant`), LangChain Groq
- **RAG / Embeddings:** SentenceTransformer for semantic vector search against the Knowledge Base
- **Integrations:** Jira REST API, Gmail SMTP (email automation)
- **Environment:** `python-dotenv` for secrets management

---

## 🤖 AI AGENTS

---

### Q4. What is RAG and how did you use it in this project?

**Answer:**
RAG stands for **Retrieval-Augmented Generation**. Instead of letting the LLM generate answers purely from its training data, we first retrieve relevant articles from our own Knowledge Base and then pass those as context to the LLM. This improves accuracy and grounds the AI's response in our specific IT documentation.

In SupportPilot:
- The **Retrieval Agent** takes the ticket subject + description, converts them into a semantic vector using SentenceTransformer, and searches the Knowledge Base for the most similar articles.
- Those retrieved articles are then passed to the **Resolution Agent** (LLM via Groq), which uses them to generate a step-by-step resolution.

This prevents hallucination and ensures the AI gives IT-domain-specific answers.

---

### Q5. Explain the Diagnosis Agent. Is it an LLM?

**Answer:**
No — the Diagnosis Agent is **entirely rule-based**, not an LLM. This was a deliberate design decision.

It uses weighted keyword matching (`SYMPTOM_RULES`) to categorize a ticket into categories like Networking, Password Reset, Hardware, Security, Software, or Email. Each symptom keyword has a weight; the category with the highest total score wins.

Confidence is calculated from three factors:
- **Share** — how much of the total evidence the winning category holds (50% weight)
- **Margin** — how far ahead the winner is from the runner-up (20% weight)
- **Evidence** — absolute amount of evidence found (30% weight)

We chose rule-based over LLM for the Diagnosis Agent because it is fast, deterministic, and doesn't consume API tokens. The LLM is only invoked at the Resolution step where natural language generation is genuinely needed.

---

### Q6. How does the Escalation Agent decide whether to escalate or resolve automatically?

**Answer:**
The Escalation Agent applies 5 rules in sequence:

| Rule | Condition | Action |
|------|-----------|--------|
| Rule 0 | Category is Hardware or Security | Always escalate — needs physical tech or security review |
| Rule 1 | AI resolution generation failed | Escalate to Level 2 Support |
| Rule 2 | Confidence score below threshold (0.70, or 0.45 for routine IT) | Escalate |
| Rule 3 | Priority is P1 (Critical) | Escalate to Priority Support |
| Rule 4 | Severity is CRITICAL | Escalate to Critical Incident Team |
| Rule 5 | LLM output contains explicit escalation phrases | Escalate (skipped for auto-resolve categories) |

If none of the rules trigger, the ticket is marked **RESOLVED** automatically.

The relaxed confidence threshold (0.45) for categories like Networking, Password Reset, and Email was added because these are well-understood problems where even lower-confidence LLM answers are still useful.

---

### Q7. Why did you use two different confidence thresholds in the Escalation Agent?

**Answer:**
LLMs perform very well on common IT issues like password resets, VPN problems, and WiFi issues — even when the formal confidence score is relatively low, the generated resolution is still accurate and actionable. If we applied a strict 0.70 threshold uniformly, these routine tickets would be unnecessarily escalated to human agents.

So we defined two sets:
- **AUTO_RESOLVE_CATEGORIES** (Networking, Password Reset, Software, Email, Access & Permissions) → threshold relaxed to **0.45**
- **HUMAN_REQUIRED_CATEGORIES** (Hardware, Security) → always escalate regardless of confidence

This design choice reduced false escalations significantly while maintaining safety for genuinely complex issues.

---

### Q8. What is the LLM fallback mechanism?

**Answer:**
We implemented a `FallbackLLM` wrapper class in `llm.py`. It wraps two Groq clients:
- **Primary:** `openai/gpt-oss-120b` (more capable)
- **Fallback:** `llama-3.1-8b-instant` (lighter, always available)

When the primary model hits a 429 rate limit error (daily token quota exceeded), the `FallbackLLM` automatically switches to the fallback model for all subsequent requests **without restarting the server or throwing an error**. This ensures the system stays online even when the primary model is exhausted.

---

## 🗄️ DATABASE & API

---

### Q9. What tables does your MySQL database have?

**Answer:**
The `supportpilot` database has these main tables:

| Table | Purpose |
|-------|---------|
| `users` | Stores requester info (name, email, department, role) |
| `tickets` | Core ticket data (subject, description, priority, severity, status) |
| `ticket_responses` | AI-generated resolution text and confidence score |
| `escalations` | Escalation record (assigned team, reason, status) |
| `jira_tickets` | Jira issue key and status linked to a ticket |
| `activity_logs` / `workflow_logs` | Step-by-step audit trail of AI agent actions |
| `knowledge_base` | IT articles used by the Retrieval Agent |
| `feedback` | User feedback (rating, classification correct or not) |

---

### Q10. How does ticket creation work end-to-end?

**Answer:**
1. User fills the form in the React frontend and clicks Submit
2. Frontend POSTs to `POST /api/tickets` on the FastAPI backend
3. Backend runs the **Diagnosis Agent** on the description to get category + priority
4. Creates or reuses a `User` record for the requester's email
5. Creates the `Ticket` record in MySQL with the AI-assigned priority and severity
6. Sends an acknowledgment email to the requester via Gmail SMTP
7. Returns the ticket data (including `ticket_id`) to the frontend
8. Frontend displays a success banner with the ticket ID
9. The AI resolution workflow (`POST /api/tickets/{id}/resolve`) is triggered separately when an agent clicks "Resolve"

---

### Q11. What is the `/api/tickets/{id}/workflow` endpoint used for?

**Answer:**
This endpoint returns the full audit trail and live status of the AI workflow for a specific ticket. The frontend's `ResolutionPanel` calls this to display:
- **Agent status cards** (Diagnosis, Retrieval, Resolution, Escalation — each shows Completed / Active / Standby)
- **Workflow Activity Log** — timestamped step-by-step log of what each AI agent did
- **Integration cards** — whether Jira and Email are Active/Completed/Standby
- **Jira ticket details** — issue key, assignee, priority
- **Email notification content** — what message was sent to the user
- **AI-generated resolution text** with confidence score

---

## 🔗 INTEGRATIONS

---

### Q12. How does the Jira integration work?

**Answer:**
When the Escalation Agent decides to escalate, the `integration_service` makes a REST API call to the Jira Cloud API at `https://supportpilotinfosys.atlassian.net` using Basic Auth (email + API token).

It creates a Jira issue in the `SCRUM` project with the ticket subject, description, priority, and assigned team. The returned Jira issue key (e.g., `SCRUM-14`) is then saved to the `jira_tickets` table in MySQL and displayed on the frontend.

We added a duplicate-check — if a Jira ticket already exists for that support ticket, we skip creation and return the existing key. This prevents duplicate Jira issues if the resolve endpoint is called twice.

---

### Q13. How does the email notification work?

**Answer:**
We use Gmail SMTP with an App Password (not the account password, for security). The `email_service` module sends two types of emails:

1. **Ticket Received** — sent immediately when a ticket is created: "Your ticket #13 has been received and is being processed by our AI."
2. **Resolution/Escalation** — sent after the workflow completes:
   - If RESOLVED: "Your ticket #13 has been resolved by AI. Resolution: [steps]..."
   - If ESCALATED: "Your ticket #13 has been escalated to [Hardware Support Team]. Reason: [reason]"

---

## ⚛️ FRONTEND

---

### Q14. How does the frontend fetch and display tickets in real time?

**Answer:**
The frontend uses **TanStack React Query** (`useQuery`) to fetch tickets from `GET /api/tickets`. It polls at a configurable interval (default 30 seconds, configurable in Settings) using the `refetchInterval` option.

When a new ticket arrives, the app:
1. Plays an audio chime using the Web Audio API
2. Shows a desktop browser notification (if permission granted)
3. Automatically loads and classifies the latest ticket in the right panel

We also use `queryClient.invalidateQueries()` after a ticket is resolved so the list refreshes immediately without waiting for the next poll.

---

### Q15. What does the Dashboard show?

**Answer:**
The Dashboard has several sections:
- **Live ticket list** — sorted by newest first, showing subject, status badge (OPEN/IN_PROGRESS/RESOLVED), and priority
- **AI Classification panel** — shows the predicted department, sub-category, and confidence score for the selected ticket
- **Resolution Panel** — shows the full AI workflow status, agent cards, activity log, Jira card, email notification, and the generated resolution text
- **Analytics tab** — shows optimization metrics (ticket volume, resolution rates, response times)
- **Settings tab** — lets users configure theme, accent color, language, refresh interval, and notification preferences

---

## 🐛 DEBUGGING / CHALLENGES

---

### Q16. What was the hardest bug you faced in this project?

**Answer:**
The most complex issue was the **port and venv misconfiguration** in `run_all.bat`. The batch file was starting the ticket API (MySQL-backed) on port 8001 using the RAG module's Python virtual environment — which didn't have SQLAlchemy or PyMySQL installed. Meanwhile, the RAG backend was running on port 8000. The frontend's `.env` expected the ticket API on 8000, so tickets couldn't be fetched.

The root cause was that the venv inside `supportpilot-api_new_fast` was built on a different team member's machine (path: `C:\Users\sadiy\...`), so it failed silently with a "file not found" error on our machine.

Fix: Recreated the venv with our local Python, installed all dependencies, swapped the ports back in `run_all.bat`, and updated `VITE_API_BASE_URL` to point to port 8001 where the full RAG API lives.

---

### Q17. How did you handle rate limiting from the Groq API?

**Answer:**
Groq's free tier has a daily token limit. We handled this with the `FallbackLLM` class that catches `RateLimitError (429)` from the primary model and automatically switches to `llama-3.1-8b-instant`. The `_using_fallback` flag is set to `True` so all subsequent requests in that server session go straight to the fallback without trying the primary again. This means the system self-heals without any manual intervention or server restart.

---

### Q18. How did you prevent duplicate Jira tickets and escalation records?

**Answer:**
Before creating any record, we query the database first:
- In `_save_escalation()`: checks if an `Escalation` record already exists for the ticket ID
- In `_handle_integrations()`: checks if a `JiraTicket` record already exists for the ticket ID

If either already exists, the function returns early without creating a duplicate. This makes the resolve endpoint **idempotent** — calling it multiple times on the same ticket produces the same result without side effects.

---

## 💡 DESIGN DECISIONS

---

### Q19. Why did you use FastAPI instead of Flask or Django?

**Answer:**
FastAPI was chosen for three reasons:
1. **Performance** — It's one of the fastest Python frameworks, built on Starlette and Uvicorn (ASGI)
2. **Auto documentation** — FastAPI automatically generates Swagger UI (`/docs`) from type hints, which helped the team test APIs without writing separate tests
3. **Type safety** — Pydantic schemas for request/response validation gave us clear contracts between the frontend and backend, reducing integration bugs

---

### Q20. Why did you use SQLAlchemy instead of raw SQL?

**Answer:**
SQLAlchemy ORM gives us:
- **Database abstraction** — we can switch from MySQL to PostgreSQL or SQLite with minimal code changes
- **Python-native querying** — `db.query(models.Ticket).filter(...)` is more readable and less error-prone than raw SQL string concatenation
- **Auto table creation** — `Base.metadata.create_all(bind=engine)` creates all tables from our model definitions on startup
- **Session management** — The `get_db()` dependency injection ensures every request gets a clean session that's properly closed after use, preventing connection leaks

---
