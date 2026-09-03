from rag import search_documents


query = "How many days can employees work remotely?"

results = search_documents(query)


print("\n===== RAG SEARCH RESULTS =====\n")

for document in results["documents"][0]:
    print(document)
    print("\n" + "-" * 60)