import uuid

from backend.core.embedding_store import EmbeddingStore
from backend.core.qdrant_store import QdrantStore
from backend.core.chunker import TextChunker
from backend.core.doc_store import DocStore
from backend.core.bm25_retriever import BM25Retriever
from backend.core.ollama_client import OllamaClient
from backend.core.rrf_fusion import RRFFusion
from backend.core.context_builder import ContextBuilder


class RAGPipeline:

    def __init__(self):

        self.embedder = EmbeddingStore()

        self.vector_db = QdrantStore()

        self.chunker = TextChunker()

        self.doc_store = DocStore()

        self.bm25 = BM25Retriever(
            self.doc_store
        )

        self.llm = OllamaClient()

        self.rrf = RRFFusion()

        self.context_builder = ContextBuilder(
            max_chunks=3
        )

    # =========================
    # INGEST
    # =========================

    async def ingest(
        self,
        doc_id: str,
        text: str
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
                "text": chunk,
                "source": doc_id,
                "chunk_id": i
            }

            self.vector_db.upsert(
                _id=point_id,
                vector=vector,
                payload=payload
            )

            self.doc_store.add(
                payload
            )

        return len(chunks)

    # =========================
    # RETRIEVE
    # =========================

    async def retrieve(
        self,
        query: str,
        top_k=3
    ):

        query_vector = await self.embedder.embed(
            query
        )

        dense_results = self.vector_db.search(
            query_vector,
            top_k=10
        )

        dense = []

        for r in dense_results:

            text = r.payload.get(
                "text"
            )

            if not text:
                continue

            dense.append(
                {
                    "text": text,
                    "score": float(
                        getattr(
                            r,
                            "score",
                            0.0
                        )
                    ),
                    "source": "dense"
                }
            )

        bm25_results = self.bm25.search(
            query,
            top_k=10
        )

        fused = self.rrf.fuse(
            dense,
            bm25_results,
            top_k=top_k
        )

        return fused

    # =========================
    # ASK
    # =========================

    async def ask(
        self,
        question: str
    ):

        docs = await self.retrieve(
            question
        )

        if not docs:

            return {
                "answer":
                "NO VALID CONTEXT FOUND",
                "context": []
            }

        context = self.context_builder.build(
            docs
        )

        prompt = f"""
You are a RAG assistant.

Use ONLY the context below.

Context:
{context}

Question:
{question}

Answer:
"""

        answer = ""

        async for token in self.llm.stream_generate(
            prompt
        ):
            answer += token

        return {
            "answer": answer,
            "context": docs
        }