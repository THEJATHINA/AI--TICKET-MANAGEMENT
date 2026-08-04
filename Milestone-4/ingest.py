"""
Milestone 2 - Knowledge Base Data Engineer (Member 4)
Full ingestion pipeline:
1. Chunk articles (300-word rule, split long ones by section)
2. Tag metadata (category, last_updated, tags, source, kb_id)
3. Generate embeddings and store in ChromaDB (vector store)
4. Populate the Knowledge_Base SQL table (article_id, title, content,
   category, embedding_id) - linking the relational DB to the vector store
"""

import sqlite3
import chromadb
from kb_articles import get_articles

CHUNK_MIN_WORDS = 500
DB_PATH = "knowledge_base.db"
CHROMA_PATH = "./chroma_db"


def chunk_article(article):
    """Short articles = 1 chunk. Long articles = split by section."""
    content = article["content"]
    if len(content.split()) < CHUNK_MIN_WORDS:
        return [{
            "chunk_id": f"{article['kb_id']}-C1",
            "text": content.strip(),
            "section": "full_article",
        }]

    sections = ["Overview", "Symptoms", "Troubleshooting Steps", "Resolution"]
    chunks = []
    for i, section in enumerate(sections):
        if section not in content:
            continue
        start = content.index(section)
        nxt = sections[i + 1] if i + 1 < len(sections) else None
        end = content.index(nxt) if (nxt and nxt in content) else len(content)
        chunks.append({
            "chunk_id": f"{article['kb_id']}-C{i+1}",
            "text": content[start:end].strip(),
            "section": section,
        })
    return chunks


def build_metadata(article, chunk):
    return {
        "kb_id": article["kb_id"],
        "title": article["title"],
        "category": article["category"],
        "tags": ", ".join(article["tags"]),
        "last_updated": article["last_updated"],
        "source": article["kb_id"],
        "section": chunk["section"],
        "chunk_id": chunk["chunk_id"],
        # optional fields, included when available
        "priority": article.get("priority", ""),
        "version": article.get("version", ""),
        "author": article.get("author", ""),
    }


def create_sql_table():
    """Creates the Knowledge_Base table per the required schema."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS Knowledge_Base")
    cur.execute("""
        CREATE TABLE Knowledge_Base (
            article_id   TEXT PRIMARY KEY,
            title        TEXT NOT NULL,
            content      TEXT NOT NULL,
            category     TEXT NOT NULL,
            embedding_id TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn


def ingest():
    # --- 1. Set up ChromaDB vector store ---
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    # reset collection for a clean run
    try:
        client.delete_collection("knowledge_base")
    except Exception:
        pass
    collection = client.get_or_create_collection(
        name="knowledge_base",
        metadata={"description": "IT support knowledge base"}
    )

    # --- 2. Set up SQL table ---
    conn = create_sql_table()
    cur = conn.cursor()

    articles = get_articles()
    ids, documents, metadatas = [], [], []

    for article in articles:
        chunks = chunk_article(article)
        # embedding_id links the SQL row to its vector chunk(s) in ChromaDB.
        # For single-chunk articles it's the chunk_id; for multi-chunk we
        # store the first chunk id as the primary reference.
        primary_embedding_id = chunks[0]["chunk_id"]

        for chunk in chunks:
            ids.append(chunk["chunk_id"])
            documents.append(chunk["text"])
            metadatas.append(build_metadata(article, chunk))

        # --- 3. Insert into the Knowledge_Base SQL table ---
        cur.execute("""
            INSERT INTO Knowledge_Base
            (article_id, title, content, category, embedding_id)
            VALUES (?, ?, ?, ?, ?)
        """, (
            article["kb_id"],
            article["title"],
            article["content"],
            article["category"],
            primary_embedding_id,
        ))

    # --- 4. Store embeddings in ChromaDB ---
    collection.upsert(ids=ids, documents=documents, metadatas=metadatas)

    conn.commit()
    conn.close()

    print(f"Ingested {len(articles)} articles as {len(ids)} chunks.")
    print(f"- ChromaDB vector store: {CHROMA_PATH}")
    print(f"- Knowledge_Base SQL table: {DB_PATH}")


if __name__ == "__main__":
    ingest()
