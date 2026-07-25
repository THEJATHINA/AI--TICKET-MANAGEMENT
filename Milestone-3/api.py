"""
Knowledge Base API (Milestone 3, Member 4).

Milestone 2 endpoint:
  GET /knowledge/search          - semantic retrieval over the KB

Milestone 3 endpoints (agent support):
  GET /diagnose                  - symptom -> category analysis for the
                                   Diagnosis Agent
  GET /knowledge/reasoning/{id}  - structured reasoning data for one article
  GET /knowledge/related/{id}    - cross-referenced articles (multi-hop)
  GET /knowledge/chain/{id}      - "if this does not fix it, try next"
  GET /workflow/analyze          - combined diagnose + retrieve, the full
                                   handoff package for the agent pipeline
"""

from fastapi import FastAPI, Query, HTTPException

from search import search_knowledge_base
from diagnose import diagnose_ticket
from kb_reasoning import get_reasoning, get_related, get_reasoning_chain

app = FastAPI(title="Knowledge Base API (Milestone 3)")


# ------------------------------------------------------------------
# Milestone 2 - retrieval
# ------------------------------------------------------------------

@app.get("/knowledge/search")
def knowledge_search(
    q: str = Query(..., description="Search query text"),
    top_k: int = Query(3, description="Number of results to return"),
):
    results = search_knowledge_base(q, top_k=top_k)
    return {"query": q, "results": results}


# ------------------------------------------------------------------
# Milestone 3 - Diagnosis Agent support
# ------------------------------------------------------------------

@app.get("/diagnose")
def diagnose(
    text: str = Query(..., description="Raw ticket description"),
    top_n: int = Query(3, description="How many candidate categories to return"),
):
    """Maps ticket text to likely categories with confidence and a KB shortlist."""
    return diagnose_ticket(text, top_n=top_n)


@app.get("/knowledge/reasoning/{kb_id}")
def article_reasoning(kb_id: str):
    """Structured reasoning data: symptoms, ordered steps, escalation rules."""
    data = get_reasoning(kb_id.upper())
    if data is None:
        raise HTTPException(status_code=404, detail=f"No reasoning data for {kb_id}")
    return {"kb_id": kb_id.upper(), **data}


@app.get("/knowledge/related/{kb_id}")
def article_related(kb_id: str):
    """Cross-referenced articles, for multi-hop agent reasoning."""
    related = get_related(kb_id.upper())
    if not related:
        raise HTTPException(status_code=404, detail=f"No related articles for {kb_id}")
    return {"kb_id": kb_id.upper(), "related_articles": related}


@app.get("/knowledge/chain/{kb_id}")
def article_chain(kb_id: str):
    """The ordered fallback path if the first article does not resolve it."""
    chain = get_reasoning_chain(kb_id.upper())
    if not chain:
        raise HTTPException(status_code=404, detail=f"No reasoning chain for {kb_id}")
    return {"kb_id": kb_id.upper(), "chain": chain}


# ------------------------------------------------------------------
# Milestone 3 - combined workflow handoff
# ------------------------------------------------------------------

@app.get("/workflow/analyze")
def workflow_analyze(
    text: str = Query(..., description="Raw ticket description"),
    top_k: int = Query(3, description="Number of KB results to retrieve"),
):
    """
    One call covering the Diagnosis -> Retrieval handoff.

    Returns the diagnosis, the retrieved articles, and the reasoning
    package (ordered steps, escalation rules, fallback chain) that the
    Resolution and Escalation Agents need - so they do not each have to
    make their own lookups.
    """
    diagnosis = diagnose_ticket(text, top_n=top_k)
    retrieved = search_knowledge_base(text, top_k=top_k)

    # Attach reasoning to each retrieved article
    for article in retrieved:
        reasoning = get_reasoning(article["kb_id"])
        if reasoning:
            article["reasoning"] = {
                "prerequisites": reasoning["prerequisites"],
                "resolution_steps": reasoning["resolution_steps"],
                "related_articles": reasoning["related_articles"],
                "next_if_unresolved": reasoning.get("next_if_unresolved"),
                "escalate_to": reasoning["escalate_to"],
                "escalate_when": reasoning["escalate_when"],
                "auto_resolvable": reasoning["auto_resolvable"],
            }

    primary = retrieved[0]["kb_id"] if retrieved else None

    return {
        "ticket_text": text,
        "diagnosis": {
            "predicted_category": diagnosis["predicted_category"],
            "confidence": diagnosis["confidence"],
            "matched_symptoms": diagnosis["matched_symptoms"],
            "suggested_priority": diagnosis["suggested_priority"],
            "suggested_kb_ids": diagnosis["suggested_kb_ids"],
            "needs_clarification": diagnosis["needs_clarification"],
            "clarifying_questions": diagnosis["clarifying_questions"],
        },
        "retrieved_articles": retrieved,
        "reasoning_chain": get_reasoning_chain(primary) if primary else [],
    }
