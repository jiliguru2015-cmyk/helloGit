import uuid

from backend.core.embedding_store import EmbeddingStore
from backend.core.qdrant_store import QdrantStore
from backend.core.doc_store import DocStore
from backend.core.chunker import TextChunker


class DocumentIngestor:

    def __init__(self):

        self.embedder = EmbeddingStore()
        self.db = QdrantStore()
        self.doc_store = DocStore()

        # 使用统一 Chunker
        self.chunker = TextChunker()

    async def ingest_text(
        self,
        text,
        source="manual"
    ):

        chunks = self.chunker.chunk(text)

        for i, chunk in enumerate(chunks):

            vector = await self.embedder.embed(
                chunk
            )

            point_id = str(
                uuid.uuid4()
            )

            payload = {
                "id": point_id,
                "text": chunk,
                "source": source,
                "chunk_id": i
            }

            self.db.upsert(
                _id=point_id,
                vector=vector,
                payload=payload
            )

            self.doc_store.add(
                payload
            )

        return len(chunks)