from backend.core.qdrant_store import QdrantStore

db = QdrantStore()

print(db.client.get_collections())