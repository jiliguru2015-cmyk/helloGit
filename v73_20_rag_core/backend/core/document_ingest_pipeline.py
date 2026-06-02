import hashlib
import time

from backend.core.embedding_store import EmbeddingStore
from backend.core.qdrant_store import QdrantStore


class DocumentIngestPipeline:

    def __init__(self):

        self.embedder = EmbeddingStore()
        self.db = QdrantStore()

    # -----------------------------
    # Chunking（简单稳定版）
    # -----------------------------
    def chunk_text(self, text: str, chunk_size=400, overlap=80):

        chunks = []
        start = 0

        while start < len(text):

            end = start + chunk_size
            chunk = text[start:end].strip()

            if chunk:
                chunks.append(chunk)

            start += chunk_size - overlap

        return chunks

    # -----------------------------
    # deterministic id（关键）
    # -----------------------------
    def _make_id(self, source: str, index: int, chunk: str):

        raw = f"{source}_{index}_{chunk[:30]}"
        return hashlib.md5(raw.encode()).hexdigest()

    # -----------------------------
    # main ingest
    # -----------------------------
    async def ingest_text(self, text: str, source: str = "manual"):

        chunks = self.chunk_text(text)

        for i, chunk in enumerate(chunks):

            vector = await self.embedder.embed(chunk)

            point_id = self._make_id(source, i, chunk)

            payload = {
                "text": chunk,
                "source": source,
                "chunk_id": i,
                "doc_id": source,
                "type": "text_chunk",
                "timestamp": time.time()
            }

            self.db.upsert(
                _id=point_id,
                vector=vector,
                payload=payload
            )

        return len(chunks)