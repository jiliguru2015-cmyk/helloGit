from backend.core.hybrid_retriever import HybridRetriever
from backend.core.reranker import Reranker
from backend.core.prompt_builder import PromptBuilder
from backend.core.generator import Generator

from backend.core.embedding_store import EmbeddingStore
from backend.core.qdrant_store import QdrantStore
from backend.core.chunker import TextChunker

import uuid


class RAGPipeline:

    def __init__(self):

        self.embedder = EmbeddingStore()
        self.vector_db = QdrantStore()
        self.chunker = TextChunker()

        self.retriever = HybridRetriever()

        self.reranker = Reranker()

        self.prompt_builder = PromptBuilder()

        self.generator = Generator()

    async def ingest(
        self,
        doc_id: str,
        text: str
    ):

        chunks = self.chunker.chunk(
            text
        )

        for i, chunk in enumerate(chunks):

            vector = await self.embedder.embed(
                chunk
            )

            payload = {
                "doc_id": doc_id,
                "chunk": chunk,
                "index": i
            }

            self.vector_db.upsert(
                _id=str(uuid.uuid4()),
                vector=vector,
                payload=payload
            )

        return len(chunks)

    async def retrieve(
        self,
        query: str,
        top_k=5
    ):

        return await self.retriever.retrieve(
            query=query,
            top_k=top_k
        )

    async def ask(
        self,
        question: str
    ):

        retrieved = await self.retrieve(
            question
        )

        reranked = self.reranker.rerank(
            question,
            retrieved
        )

        prompt = self.prompt_builder.build(
            question,
            reranked
        )

        answer = await self.generator.generate(
            prompt
)
        return {
            "question": question,
            "contexts": reranked,
            "answer": answer
        }