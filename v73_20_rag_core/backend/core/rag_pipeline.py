from backend.core.embedding_store import EmbeddingStore
from backend.core.qdrant_store import QdrantStore
from backend.core.chunker import TextChunker
from backend.core.doc_store import DocStore
from backend.core.bm25_retriever import BM25Retriever
from backend.core.ollama_client import OllamaClient
from backend.core.rrf_fusion import RRFFusion
from backend.core.context_builder import ContextBuilder
import uuid


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
            max_chunks=5
        )

    async def ingest(self, doc_id: str, text: str):

        chunks = self.chunker.chunk(text)

        for i, chunk in enumerate(chunks):

            vector = await self.embedder.embed(chunk)

            point_id = str(uuid.uuid4())  # ✅ FIX: Qdrant valid ID only

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

            self.doc_store.add(payload)

        return len(chunks)

    # =========================
    # RETRIEVAL
    # =========================
    async def retrieve(self, query: str, top_k=5):

        q_vec = await self.embedder.embed(query)

        dense_results = self.vector_db.search(q_vec, top_k=top_k)

        dense = []
        for r in dense_results:
            text = r.payload.get("text")
            if not text:
                continue

            dense.append({
                "text": text,
                "score": float(getattr(r, "score", 0.0)),
                "source": "dense"
            })

        bm25_results = self.bm25.search(query, top_k=top_k)

        fused = self.rrf.fuse(
            dense,
            bm25_results
        )
        return fused

    def _fusion(self, dense, sparse):

        scores = {}

        def add(item, weight):

            text = item.get("text")
            score = item.get("score", 0.0)

            if not text:
                return

            scores[text] = scores.get(text, 0.0) + score * weight

        for d in dense:
            add(d, 0.7)

        for s in sparse:
            add(s, 0.3)

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        return [
            {"text": t, "score": s}
            for t, s in ranked
        ]

    # =========================
    # ASK (FINAL FIXED)
    # =========================
    async def ask(self, question: str):

        docs = await self.retrieve(question)

        clean_docs = [
            d["text"] for d in docs
            if isinstance(d.get("text"), str) and d["text"].strip()
        ]

        if not clean_docs:
            return {
                "answer": "NO VALID CONTEXT FOUND",
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

        # ✅ FIX: stream_generate must be async iterator
        async for token in self.llm.stream_generate(prompt):
            answer += token

        return {
            "answer": answer,
            "context": docs
        }