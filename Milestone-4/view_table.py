"""
Helper to view the populated Knowledge_Base SQL table.
Useful for verifying ingestion and for demoing to mentors.
"""

import sqlite3

DB_PATH = "knowledge_base.db"


def view_table():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT article_id, title, category, embedding_id FROM Knowledge_Base")
    rows = cur.fetchall()

    print(f"Knowledge_Base table - {len(rows)} rows\n")
    print(f"{'article_id':10} | {'category':14} | {'embedding_id':14} | title")
    print("-" * 90)
    for r in rows:
        print(f"{r[0]:10} | {r[2]:14} | {r[3]:14} | {r[1]}")
    conn.close()


if __name__ == "__main__":
    view_table()
