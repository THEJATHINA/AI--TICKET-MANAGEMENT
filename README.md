# SupportPilot — RAG & Agent Module

## Member 5 — Milestone 3

This branch contains the **Milestone 3 implementation** for the SupportPilot AI Ticket Management System.

The module extends the RAG pipeline with **LLM integration and intelligent support agents** for resolution generation, escalation decisions, and confidence assessment.

---

## Module Structure

```text
app/
├── agents/
│   ├── __init__.py
│   ├── confidence.py
│   ├── escalation_agent.py
│   ├── prompts.py
│   └── resolution_agent.py
│
└── rag/
    ├── __init__.py
    ├── formatter.py
    ├── llm.py
    ├── prompts.py
    └── rag_chain.py
```

---

## Components

### RAG Module

The `app/rag/` package provides the retrieval-augmented generation layer.

| File           | Responsibility                             |
| -------------- | ------------------------------------------ |
| `rag_chain.py` | Coordinates the RAG processing pipeline    |
| `llm.py`       | Handles LLM interaction                    |
| `formatter.py` | Formats retrieved/contextual information   |
| `prompts.py`   | Defines prompts used during RAG processing |
| `__init__.py`  | Initializes the RAG package                |

The RAG pipeline provides relevant knowledge-base context to the LLM before response generation.

---

### Agent Module

The `app/agents/` package contains the intelligent agents introduced/extended for Milestone 3.

| File                  | Responsibility                                                      |
| --------------------- | ------------------------------------------------------------------- |
| `resolution_agent.py` | Generates customer-support resolutions using available context      |
| `escalation_agent.py` | Determines whether a ticket should be escalated                     |
| `confidence.py`       | Calculates/handles confidence associated with generated resolutions |
| `prompts.py`          | Contains prompts used by the agents                                 |
| `__init__.py`         | Initializes the agent package                                       |

---

## Processing Flow

The overall Milestone 3 workflow can be represented as:

```text
Customer Ticket
       │
       ▼
   RAG Pipeline
       │
       ├── Retrieve Relevant Knowledge
       │
       ▼
   Context + Query
       │
       ▼
       LLM
       │
       ▼
 Resolution Agent
       │
       ├───────────────┐
       ▼               ▼
Resolution       Confidence
Generation         Scoring
       │
       ▼
Escalation Agent
       │
       ├── Resolve Automatically
       │
       └── Escalate to Human
```

---

## Resolution Agent

The Resolution Agent uses the retrieved knowledge-base information together with the user ticket to generate a grounded support resolution.

The objective is to ensure that the generated response is based on the information available through the RAG pipeline rather than relying solely on the LLM's general knowledge.

### Responsibilities

* Receive ticket information.
* Use retrieved knowledge as context.
* Generate a customer-support resolution.
* Produce responses appropriate for the ticket.
* Work with confidence scoring and escalation logic.

---

## Confidence Scoring

The confidence component provides a mechanism for estimating how reliable an AI-generated resolution is.

Confidence information can be used by downstream components to determine whether an automatically generated response is sufficiently reliable.

A low-confidence result can be used as a signal for further review or escalation.

---

## Escalation Agent

The Escalation Agent introduces decision logic for determining whether a ticket should be handled automatically or transferred to human support.

The decision can consider factors such as:

* Resolution confidence.
* Ticket characteristics.
* Available knowledge.
* Whether the generated response is sufficiently reliable.
* Other escalation rules defined by the system.

Conceptually:

```text
Generated Resolution
        │
        ▼
Confidence / Rules
        │
   ┌────┴────┐
   ▼         ▼
Resolve    Escalate
   │         │
   ▼         ▼
Customer   Human Agent
```

---

## LLM Integration

The LLM layer is responsible for generating natural-language responses using the context provided by the RAG pipeline.

The architecture separates LLM interaction from the agent logic so that the model integration can be maintained independently.

This separation also makes it easier to modify prompts, models, or generation settings without rewriting the complete agent workflow.

---

## Prompt Management

Prompts are separated into dedicated modules:

```text
app/rag/prompts.py
app/agents/prompts.py
```

This keeps prompt definitions organized and allows RAG-specific and agent-specific instructions to evolve independently.

---

## Key Objectives of Milestone 3

The main objectives of this milestone are:

* Integrate RAG with LLM-based response generation.
* Generate knowledge-grounded support resolutions.
* Introduce a dedicated Resolution Agent.
* Introduce confidence assessment for generated resolutions.
* Introduce escalation decision logic.
* Separate RAG, LLM, and agent responsibilities.
* Establish a foundation for production-oriented AI ticket resolution.

---

## Benefits

The Milestone 3 architecture provides:

* **Grounded responses** through RAG context.
* **Automated resolution** through the Resolution Agent.
* **Reliability assessment** through confidence scoring.
* **Human escalation** for cases that should not be automatically resolved.
* **Modular architecture** separating retrieval, LLM, and agent responsibilities.
* **Extensibility** for future production improvements.

---

## Architecture

```text
                 ┌─────────────────────┐
                 │    Customer Ticket  │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │     RAG Pipeline    │
                 └──────────┬──────────┘
                            │
                     Retrieved Context
                            │
                            ▼
                 ┌─────────────────────┐
                 │        LLM          │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │  Resolution Agent   │
                 └──────────┬──────────┘
                            │
                  ┌─────────┴─────────┐
                  ▼                   ▼
          ┌──────────────┐    ┌──────────────┐
          │  Confidence  │    │  Escalation  │
          │    Score     │    │    Agent     │
          └──────┬───────┘    └──────┬───────┘
                 │                   │
                 └─────────┬─────────┘
                           ▼
                 ┌─────────────────────┐
                 │ Final Support Action│
                 └─────────────────────┘
```

---

## Scope of This Branch

This branch contains only the **Member 5 Milestone 3 RAG and Agent implementation**.

```text
app/
├── agents/
└── rag/
```

Other SupportPilot components are intentionally excluded from this branch.

---

## Milestone Information

| Attribute       | Details                                            |
| --------------- | -------------------------------------------------- |
| Project         | SupportPilot AI Ticket Management System           |
| Milestone       | 3                                                  |
| Team Member     | Member 5                                           |
| Focus           | RAG / LLM / Agents                                 |
| Main Components | RAG, LLM, Resolution Agent, Confidence, Escalation |

---

## Future Enhancements

Potential future improvements include:

* Advanced retrieval and reranking.
* Production vector-store integration.
* More sophisticated confidence scoring.
* Improved escalation policies.
* LLM latency monitoring.
* Response quality evaluation.
* Automated RAG and agent testing.
* Integration with the complete SupportPilot backend.
