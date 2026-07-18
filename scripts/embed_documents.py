import os
import chromadb
from sentence_transformers import SentenceTransformer

# ----------------------------
# Load embedding model
# ----------------------------
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# ----------------------------
# Connect to ChromaDB
# ----------------------------
client = chromadb.PersistentClient(path="./database/chromadb")

# Delete old collection if it exists
try:
    client.delete_collection("knowledge_base")
    print("Old collection deleted.")
except:
    print("No previous collection found.")

# Create new collection
collection = client.create_collection("knowledge_base")

# ----------------------------
# Knowledge Base Folder
# ----------------------------
KB_FOLDER = "./knowledge_base"

# ----------------------------
# Metadata for each document
# ----------------------------
kb_metadata = {
    "vpn.txt": {
        "kb_id": "KB001",
        "title": "VPN Troubleshooting Guide",
        "category": "Network",
        "tags": "vpn,network"
    },
    "password.txt": {
        "kb_id": "KB002",
        "title": "Password Reset Guide",
        "category": "Authentication",
        "tags": "password,login"
    },
    "printer.txt": {
        "kb_id": "KB003",
        "title": "Printer Troubleshooting Guide",
        "category": "Hardware",
        "tags": "printer,hardware"
    },
    "network.txt": {
        "kb_id": "KB004",
        "title": "Network Connectivity Troubleshooting",
        "category": "Network",
        "tags": "network,internet"
    },
    "firewall.txt": {
        "kb_id": "KB005",
        "title": "Firewall Troubleshooting Guide",
        "category": "Security",
        "tags": "firewall,vpn"
    },
    "software_installation.txt": {
        "kb_id": "KB006",
        "title": "Software Installation Troubleshooting",
        "category": "Software",
        "tags": "software,installation"
    }
}

print("\nReading knowledge base documents...\n")

# ----------------------------
# Read each document and store in ChromaDB
# ----------------------------
for filename in os.listdir(KB_FOLDER):

    if filename.endswith(".txt"):

        filepath = os.path.join(KB_FOLDER, filename)

        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()

        embedding = model.encode(content).tolist()

        metadata = kb_metadata.get(filename)

        if metadata is None:
            print(f"Skipping {filename}: No metadata found.")
            continue

        collection.add(
            ids=[metadata["kb_id"]],
            documents=[content],
            embeddings=[embedding],
            metadatas=[metadata]
        )

        print(f"Indexed: {filename}")

print("\nAll documents indexed successfully!")