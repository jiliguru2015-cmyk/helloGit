import uuid

from backend.core.embedding_store import EmbeddingStore
from backend.core.qdrant_store import QdrantStore
from backend.core.bm25_store import BM25Store


class DocumentIngestor:

    def __init__(self):

        self.embedder = EmbeddingStore()
        self.db = QdrantStore()

        self.bm25 = BM25Store()

    def chunk_text(
        self,
        text: str,
        chunk_size=500,
        overlap=100
    ):

        chunks = []

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunks.append(
                text[start:end]
            )

            start += (
                chunk_size - overlap
            )

        return chunks

    async def ingest_text(
        self,
        text: str,
        source: str = "manual"
    ):

        chunks = self.chunk_text(text)

        for i, chunk in enumerate(chunks):

            vector = await self.embedder.embed(
                chunk
            )

            payload = {
                "text": chunk,
                "source": source,
                "chunk_id": i
            }

            point_id = str(
                uuid.uuid4()
            )

            self.db.upsert(
                _id=point_id,
                vector=vector,
                payload=payload
            )

            self.bm25.add_document(
                chunk,
                payload
            )

        return len(chunks)