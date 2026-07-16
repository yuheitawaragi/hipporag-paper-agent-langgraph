from vectorstore.qdrant.qdrant_store import QdrantStore

store = QdrantStore()

docs = [
    {"text": "Agentic RAG"},
    {"text": "HippoRAG"},
]

embeddings = [
    [0.1] * 1536,
    [0.2] * 1536,
]

store.build(embeddings, docs)

result = store.search([0.1] * 1536)

print(result)