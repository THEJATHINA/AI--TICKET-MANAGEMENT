# SupportPilot — RAG Module

## Member 5 — Milestone 2

This module implements the **Retrieval-Augmented Generation (RAG)** component of SupportPilot. It is responsible for combining retrieved knowledge-base information with an LLM to generate grounded customer-support responses.

The RAG module is designed to reduce unsupported or hallucinated responses by providing the language model with relevant knowledge-base context before generating an answer.

---

## Module Structure

```text
app/
└── rag/
    ├── __init__.py
    ├── formatter.py
    ├── llm.py
    ├── prompts.py
    └── rag_chain.py
```

### Files

| File           | Responsibility                                                         |
| -------------- | ---------------------------------------------------------------------- |
| `__init__.py`  | Initializes the RAG package                                            |
| `formatter.py` | Formats retrieved information and generated responses                  |
| `llm.py`       | Handles LLM configuration and response generation                      |
| `prompts.py`   | Contains prompts used for grounded response generation                 |
| `rag_chain.py` | Connects retrieval, context preparation, prompting, and LLM generation |

---

## RAG Workflow

The module follows the general RAG pipeline:

```text
User Query
    ↓
Retrieve Relevant Knowledge
    ↓
Retrieved Context
    ↓
Format Context
    ↓
RAG Prompt
    ↓
LLM
    ↓
Grounded Response
```

The retrieved knowledge-base information is supplied to the LLM as context so that the generated response is based on available support information rather than relying only on the model's general knowledge.

---

## Main Components

### 1. Retrieval Context

Relevant knowledge-base information is passed into the RAG pipeline as context.

The retrieved information provides the factual basis for the response.

### 2. Context Formatting

`formatter.py` prepares retrieved content in a consistent format before it is supplied to the LLM.

This keeps the prompt structure clean and makes the retrieved information easier for the model to interpret.

### 3. Prompt Management

`prompts.py` contains the prompts used by the RAG pipeline.

The prompts instruct the LLM to:

* Use the supplied knowledge-base context.
* Generate customer-support-oriented responses.
* Avoid inventing unsupported information.
* Provide an appropriate response when sufficient information is not available.

### 4. LLM Integration

`llm.py` handles interaction with the configured Large Language Model.

The LLM receives the user query together with the relevant retrieved context.

### 5. RAG Chain

`rag_chain.py` coordinates the complete RAG process.

It connects the retrieved knowledge, formatting, prompts, and LLM generation into a single response-generation pipeline.

---

## Objective

The objective of this milestone is to provide SupportPilot with a dedicated RAG layer capable of generating responses that are **grounded in the organization's knowledge base**.

This allows the system to move beyond a standalone LLM response and use retrieved support information as the primary source of context.

---

## Expected Benefits

* Knowledge-grounded responses
* Reduced hallucination
* Better customer-support accuracy
* Reusable RAG architecture
* Separation of retrieval, prompting, formatting, and LLM logic
* Easier future integration with vector databases and retrieval systems

---

## Integration

This module is intended to be integrated with the larger SupportPilot architecture.

```text
Support Query
     ↓
SupportPilot
     ↓
Retrieval Layer
     ↓
RAG Module
     ↓
LLM
     ↓
Generated Resolution
```

The RAG module can therefore act as the response-generation layer between knowledge retrieval and the SupportPilot resolution workflow.

---

## Milestone

**Milestone:** 2
**Role:** Member 5
**Area:** RAG / LLM
**Project:** SupportPilot AI Ticket Management System

---

## Current Scope

This branch contains only the Member 5 RAG implementation:

```text
app/rag/
```

The module is intentionally separated from the other SupportPilot components so that it can be developed, tested, and integrated independently.

## Future Enhancements

Potential future improvements include:

* Integration with a production vector database
* Improved semantic retrieval
* Retrieval confidence scoring
* Better context ranking
* Response confidence estimation
* LLM latency monitoring
* Improved hallucination prevention
* Integration with the Resolution Agent
* Rich structured responses for the frontend
