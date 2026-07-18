from services.vector_search import search_documents

results = search_documents("VPN connection timeout")

for r in results:
    print(r)