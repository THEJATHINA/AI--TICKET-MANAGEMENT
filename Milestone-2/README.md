# Milestone 2 - Knowledge Base / Data Engineer (Member 4)

Sources and structures IT knowledge base content, builds the ingestion
pipeline (chunking + metadata tagging), and populates BOTH:
- a Knowledge_Base SQL table (article_id, title, content, category, embedding_id)
- a ChromaDB vector store (for semantic search by the RAG module)

## Files
- kb_articles.py   -> 10 detailed IT knowledge base articles, each a
                      distinct IT support scenario (300-500 words)
- ingest.py        -> ingestion pipeline: chunks, tags metadata,
                      builds embeddings in ChromaDB, populates SQL table
- search.py        -> semantic search (query -> top-k relevant chunks)
- api.py           -> FastAPI endpoint: GET /knowledge/search
- view_table.py    -> helper to view the populated Knowledge_Base SQL table
- requirements.txt -> Python dependencies

## The 10 articles (each a distinct IT scenario)
KB-101  VPN Troubleshooting Guide                       (Networking)
KB-102  Resetting Your Network Password                 (Password Reset)
KB-103  Network Firewall Configuration                  (Networking)
KB-104  Outlook Email Sync Issues                       (Email)
KB-105  Laptop Overheating and Shutdown Issues          (Hardware)
KB-106  Installing and Licensing Software Requests      (Software)
KB-107  Reporting Suspicious Emails and Phishing        (Security)
KB-108  Wireless Network Connectivity Issues            (Networking)
KB-109  Multi-Factor Authentication Setup and Issues    (Security)
KB-110  Printer Connectivity and Print Queue Issues     (Hardware)

## Chunking rule (per RAG engineer's spec: 300-500 words per chunk)
Every article is written to land within 300-500 words (verified: range
312-400 words), each kept as a single well-sized chunk. The pipeline's
section-splitting logic (for any article over 500 words) is included and
applies automatically to longer content added later.

## Metadata schema (per RAG engineer's spec)

Required fields (all implemented):
{
  "kb_id": "KB-101",
  "title": "VPN Troubleshooting Guide",
  "category": "Networking",
  "tags": ["VPN", "Remote Access"],
  "last_updated": "2026-07-15",
  "source": "KB-101"
}

Optional fields (also implemented): priority, version, author

## Knowledge_Base SQL table schema (per task requirement)
article_id   TEXT PRIMARY KEY
title        TEXT
content      TEXT
category     TEXT
embedding_id TEXT   -> links each row to its chunk in the ChromaDB vector store

===================================================
STEPS TO RUN IN VS CODE
===================================================

1. Unzip and open the "kb_10" folder in VS Code
2. Terminal -> New Terminal
3. Create a virtual environment:
   python -m venv venv
4. Activate it:
   Windows: venv\Scripts\activate
   Mac:     source venv/bin/activate
5. Install packages:
   pip install -r requirements.txt
6. Run the ingestion pipeline (populates BOTH the SQL table and ChromaDB):
   python ingest.py
   -> First run downloads the embedding model (~80MB, one time, needs
      internet). Expect: "Ingested 10 articles as 10 chunks."
7. View the populated Knowledge_Base SQL table:
   python view_table.py
8. Test the search directly:
   python search.py
9. Start the search API:
   uvicorn api:app --reload
10. Test in your browser:
    http://127.0.0.1:8000/docs
    Try GET /knowledge/search with q = "my vpn keeps disconnecting"

===================================================
API
===================================================
GET /knowledge/search?q=<query>&top_k=3

Response includes: kb_id, title, category, tags, last_updated, source,
section, content, relevance_score, priority, version, author

===================================================
HONEST NOTE
===================================================
These 10 articles are realistic sample content written to build and
demonstrate the pipeline end-to-end -- they are not real company
documentation. The pipeline (chunking, metadata, embeddings, SQL
population) works identically whether the source is sample or real
content, so real internal IT docs can be dropped into kb_articles.py
and re-ingested anytime.

===================================================
NOTES FOR TEAMMATES
===================================================
- Vector store: ChromaDB, collection name "knowledge_base"
- SQL table: SQLite (knowledge_base.db) for zero-setup local running.
  Same schema and logic port directly to PostgreSQL if the team
  standardizes on that.
- embedding_id links each SQL row to its ChromaDB chunk, so the RAG
  module can cross-reference relational and vector stores.
