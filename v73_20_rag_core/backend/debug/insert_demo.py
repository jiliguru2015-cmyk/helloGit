import asyncio

from backend.core.embedding_store import EmbeddingStore
from backend.core.qdrant_store import QdrantStore


async def main():

    embedder = EmbeddingStore()
    db = QdrantStore()

    text = """
This system is an enterprise AI assistant platform.

It uses:
- FastAPI
- Qdrant
- Ollama
- RAG
"""

    vector = await embedder.embed(text)

    db.upsert(
        _id=1,
        vector=vector,
        payload={
            "text": text
        }
    )

    print("insert success")


if __name__ == "__main__":
    asyncio.run(main())