"""
Knowledge Base API (Milestone 4, Member 4).

Milestone 2 endpoint:
  GET /knowledge/search        - semantic retrieval over the KB

Milestone 4 endpoints (dashboard/coverage support):
  GET /analytics/kb-coverage   - coverage numbers for the dashboard's
                                 "Knowledge Base Coverage" metric
  GET /analytics/kb-gaps       - the deeper gap analysis + content
                                 recommendations
"""

from fastapi import FastAPI, Query
from search import search_knowledge_base
from coverage_analyzer import official_coverage, gap_analysis, recommend_gaps
from coverage_report import build_report
from sample_ticket_data import get_sample_tickets

app = FastAPI(title="Knowledge Base API (Milestone 4)")


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
# Milestone 4 - coverage & gap analytics for the dashboard
# ------------------------------------------------------------------

@app.get("/analytics/kb-coverage")
def kb_coverage():
    """
    Knowledge Base Coverage metric for the dashboard.

    Returns both the official coverage number (any retrieval = a match,
    matching Role 3's definition) and the effective coverage after
    applying a similarity threshold, so the dashboard can show the honest
    picture alongside the headline number.

    Currently runs on the bundled sample ticket data. When Backend
    (Role 2) exposes the real aggregated ticket feed, swap
    get_sample_tickets() for that source.
    """
    tickets = get_sample_tickets()
    official = official_coverage(tickets)
    deeper = gap_analysis(tickets)
    return {
        "official_coverage_pct": official["coverage_pct"],
        "effective_coverage_pct": deeper["effective_coverage_pct"],
        "total_tickets": official["total_tickets"],
        "covered": official["covered"],
        "gaps": official["gaps"],
        "weak_matches": deeper["weak_match_count"],
        "no_matches": deeper["no_match_count"],
    }


@app.get("/analytics/kb-gaps")
def kb_gaps():
    """
    The deeper gap analysis and prioritized content recommendations -
    which categories need new or expanded KB articles.
    """
    report = build_report()
    return {
        "gaps_by_category": report["gaps_by_category"],
        "recommendations": report["recommendations"],
    }
