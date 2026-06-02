from backend.core.qdrant_store import QdrantStore

db = QdrantStore()

points = db.client.scroll(
    collection_name=db.collection_name,
    limit=100
)[0]

print(f"TOTAL={len(points)}")

for p in points:
    print(
        p.id,
        p.payload.get("source"),
        p.payload.get("chunk_id")
    )