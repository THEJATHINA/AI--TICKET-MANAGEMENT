# Milestone 4 - Knowledge Base / Data Engineer (Member 4)

Task:
- Ensure KB content is comprehensive enough to support the Knowledge
  Base Coverage target
- Identify gaps in KB content based on unresolved/escalated tickets
  from dashboard data

Both parts are implemented, tested, and wired into the dashboard via
two new API endpoints.

===================================================
HOW THIS WORKS (the approach)
===================================================

Role 3 (Vector DB) confirmed two things about the coverage metric:
  - The OFFICIAL "Knowledge Base Coverage" metric counts ANY successful
    retrieval as a match (no similarity threshold). A gap = nothing
    returned.
  - The Retrieval Agent also returns a similarity_score (0-1) per ticket,
    available for deeper analysis.

The catch: because retrieval almost always returns *something*, the
official metric can read high (here 84.2%) even when many matches are
weak and irrelevant. So this deliverable does two things:

  1. Reports the official coverage number (for the dashboard KPI)
  2. Runs a DEEPER gap analysis using similarity_score with a threshold,
     which reveals the effective coverage is actually 52.6% and pinpoints
     exactly which topics need content.

Then it acts on that: 5 new KB articles were added to close the gaps the
analysis found.

===================================================
FILES
===================================================
kb_articles.py         - the KB articles: now 17 (was 10), with 7 new
                         gap-filling articles (KB-111 to KB-117)
coverage_analyzer.py   - NEW: official coverage + deeper gap analysis +
                         per-category gaps + recommendations
sample_ticket_data.py  - NEW: sample tickets with similarity_score, a
                         realistic mix of strong/weak/no matches, so the
                         analyzer can be demonstrated before the real
                         ticket feed exists
coverage_report.py     - NEW: builds a single JSON coverage report for
                         the dashboard, plus a printed summary
test_milestone4.py     - NEW: self-test (15 checks)
ingest.py              - ingestion pipeline (unchanged logic; picks up
                         the 5 new articles automatically)
search.py              - semantic retrieval (unchanged from M2)
api.py                 - UPDATED: 2 new /analytics endpoints
view_table.py          - views the Knowledge_Base table
requirements.txt       - dependencies

===================================================
THE 5 NEW ARTICLES (closing the identified gaps)
===================================================
KB-111  Setting Up Company Email on Mobile Devices   (Email)
KB-112  Application Crashing or Freezing Repeatedly  (Software)
KB-113  Requesting Access to HR and Payroll Systems  (Human Resources)
KB-114  Software Update and Patch Installation Issues(Software)
KB-115  Account Onboarding and Offboarding Requests  (Human Resources)
KB-116  Bluetooth Device Not Connecting or Pairing    (Hardware)
KB-117  Keyboard Not Responding or Missing Keystrokes (Hardware)

KB now spans 7 categories (added Human Resources), with Email and
Software doubled and Hardware expanded - covering every area the gap
analysis flagged, including the Bluetooth and keyboard gaps reported
by Role 3.

===================================================
API ENDPOINTS
===================================================
From Milestone 2:
  GET /knowledge/search?q=<text>&top_k=3

New in Milestone 4 (for the dashboard):
  GET /analytics/kb-coverage
      -> official_coverage_pct, effective_coverage_pct, covered, gaps,
         weak_matches, no_matches
         (feeds the "Knowledge Base Coverage" metric on the dashboard)

  GET /analytics/kb-gaps
      -> gaps_by_category + prioritized content recommendations

===================================================
STEPS TO RUN IN VS CODE
===================================================

1. Unzip and open the "kb_10" folder in VS Code
   (File -> Open Folder -> select kb_10)

2. Terminal -> New Terminal

3. Create a virtual environment (use py -3.12 if plain python is 3.14):
   py -3.12 -m venv venv

4. Activate it:
   Windows: venv\Scripts\activate
   Mac:     source venv/bin/activate

   If Windows blocks the script, run this once then retry:
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned

5. Install packages:
   pip install -r requirements.txt

6. Run the ingestion pipeline (populates ChromaDB + the SQL table):
   python ingest.py
   Expected: "Ingested 17 articles as 17 chunks."
   (First run downloads the embedding model ~80MB, one time.)

7. Run the coverage / gap analysis:
   python coverage_analyzer.py
   -> shows official coverage, deeper gap analysis, gaps by category,
      and content recommendations

8. Generate the dashboard coverage report:
   python coverage_report.py
   -> prints a summary and writes kb_coverage_report.json

9. Run the self-test:
   python test_milestone4.py
   Expected: ALL CHECKS PASSED

10. Start the API:
    uvicorn api:app --reload

11. Test in your browser at http://127.0.0.1:8000/docs
    Try: /analytics/kb-coverage  and  /analytics/kb-gaps

===================================================
CONNECTING TO REAL TICKET DATA LATER
===================================================
Right now the analysis runs on sample_ticket_data.py so it can be
demonstrated before Backend (Role 2) exposes the real aggregated ticket
feed. When that feed is available, replace get_sample_tickets() with the
real source - each ticket just needs: ticket_text, retrieved_kb_id,
similarity_score, category, escalated. Nothing else changes.

===================================================
HONEST NOTES
===================================================
- The sample tickets are realistic examples built to demonstrate the
  analysis, not real collected tickets. The weak/no-match tickets are
  deliberately clustered around a few topics so the gap analysis
  produces a clear recommendation.
- similarity_score is a semantic relevance measure, not an accuracy
  percentage. "Effective coverage" is coverage after treating weak
  matches as gaps - it is a planning tool, not an official metric.
- The GAP_THRESHOLD (0.45) is a starting point agreed with Role 3, and
  can be tuned as real ticket data comes in.
- The 5 new articles are realistic sample content in the same style as
  the original 10, not real company documentation.

===================================================
NOTES FOR TEAMMATES
===================================================
- Role 1 (Frontend): /analytics/kb-coverage gives you both the headline
  coverage % and the honest effective % for the System Optimization panel.
- Role 2 (Backend): when you have the real aggregated ticket feed, point
  the analyzer at it (see "Connecting to real ticket data" above).
- Role 3 (Vector DB): this uses your similarity_score exactly as you
  exposed it; the official-coverage calculation matches your definition.
