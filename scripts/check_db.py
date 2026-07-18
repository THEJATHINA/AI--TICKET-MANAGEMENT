import chromadb

client = chromadb.PersistentClient(path="./database/chromadb")

collection = client.get_collection("knowledge_base")

data = collection.get(include=["documents", "metadatas"])

print("Total Documents:", len(data["ids"]))

for i in range(len(data["ids"])):
    print("=" * 50)
    print("ID:", data["ids"][i])
    print("Metadata:", data["metadatas"][i])
    print("Document:")
    print(data["documents"][i])