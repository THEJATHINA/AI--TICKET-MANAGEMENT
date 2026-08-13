# SupportPilot — Milestone 4

## Member 5 — RAG / LLM

This milestone extends the SupportPilot RAG and LLM system with **optimization, confidence handling, response generation, escalation, and performance monitoring**.

### Structure

```text
agents/
├── confidence.py
├── escalation_agent.py
├── optimization_agent.py
├── prompts.py
└── resolution_agent.py

config/
└── optimization_config.py

rag/
├── generation_timer.py
└── llm.py

utils/
├── statistics.py
└── timers.py
```

### Key Features

* **Optimization Agent** — improves the response-generation workflow.
* **Resolution Agent** — generates support resolutions using RAG/LLM.
* **Escalation Agent** — handles escalation decisions.
* **Confidence Handling** — evaluates generated response reliability.
* **LLM Integration** — manages LLM-based generation.
* **Performance Monitoring** — measures generation time and system statistics.

### Objective

The goal of Milestone 4 is to improve the **reliability, performance, and optimization** of the SupportPilot RAG/LLM pipeline.

**Role:** Member 5
**Milestone:** 4
**Focus:** RAG / LLM / Optimization
