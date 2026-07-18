from sentence_transformers import SentenceTransformer
import chromadb

# ----------------------------
# Load embedding model
# ----------------------------
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# ----------------------------
# Connect to ChromaDB
# ----------------------------
client = chromadb.PersistentClient(path="./database/chromadb")

collection = client.get_collection("knowledge_base")

print("\nSemantic Search Ready!")
print("Type 'exit' to quit.\n")

while True:

    query = input("Enter your query: ")

    if query.lower() == "exit":
        break

    # Convert query into embedding
    query_embedding = model.encode(query).tolist()

    # Search top 3 documents
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=1
    )

    print("\nTop Matching Articles:\n")

    document = results["documents"][0][0]
    metadata = results["metadatas"][0][0]
    distance = results["distances"][0][0]

    print("\nMost Relevant Article")
    print("=" * 60)
    print(f"Document : {metadata['source']}")
    #print(f"Distance : {distance}")
    print()
    print(document)