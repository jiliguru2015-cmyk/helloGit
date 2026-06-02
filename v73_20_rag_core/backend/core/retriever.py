from backend.core.embedding_store import EmbeddingStore
from backend.core.qdrant_store import QdrantStore


class Retriever:

    def __init__(self):

        self.embedder = EmbeddingStore()
        self.db = QdrantStore()

    async def retrieve(
        self,
        query: str,
        top_k: int = 5
    ):

        vector = await self.embedder.embed(query)

        return self.db.search(
            vector,
            top_k=top_k
        )