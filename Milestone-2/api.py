"""
Knowledge Base API (Milestone 2, Member 4).
Exposes GET /knowledge/search for the Backend/RAG modules to query
the vector store and retrieve relevant KB articles.
"""

from fastapi import FastAPI, Query
from search import search_knowledge_base

app = FastAPI(title="Knowledge Base Search API")


@app.get("/knowledge/search")
def knowledge_search(
    q: str = Query(..., description="Search query text"),
    top_k: int = Query(3, description="Number of results to return")
):
    results = search_knowledge_base(q, top_k=top_k)
    return {"query": q, "results": results}
