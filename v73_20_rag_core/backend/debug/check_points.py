from backend.core.qdrant_store import QdrantStore


db = QdrantStore()

info = db.client.get_collection(
    collection_name=db.collection_name
)

print(info)