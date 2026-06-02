import uuid
from datetime import datetime

from backend.core.embedding_store import EmbeddingStore
from backend.core.qdrant_store import QdrantStore


class DocumentIngestPipeline:

    def __init__(self):

        self.embedder = EmbeddingStore()
        self.db = QdrantStore()

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

            chunks.append(text[start:end])

            start += chunk_size - overlap

        return chunks

    async def ingest(
        self,
        text: str,
        source: str = "unknown"
    ):

        chunks = self.chunk_text(text)

        for i, chunk in enumerate(chunks):

            vector = await self.embedder.embed(chunk)

            self.db.upsert(
                _id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "text": chunk,
                    "source": source,
                    "file_name": source,
                    "chunk_id": i,
                    "created_at": datetime.utcnow().isoformat()
                }
            )

        return {
            "chunks": len(chunks),
            "source": source
        }