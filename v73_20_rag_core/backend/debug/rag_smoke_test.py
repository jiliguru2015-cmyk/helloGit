import asyncio

from backend.core.embedding_store import EmbeddingStore
from backend.core.qdrant_store import QdrantStore
from backend.core.ollama_client import OllamaClient


class RAGSmokeTest:

    def __init__(self):

        self.embedder = EmbeddingStore()
        self.vector_db = QdrantStore()
        self.llm = OllamaClient()

    async def run(self, query: str):

        print("\n==============================")
        print("🚀 RAG SMOKE TEST START")
        print("==============================\n")

        # 1️⃣ Embedding
        print("🔹 Step 1: Embedding Query")

        vector = await self.embedder.embed(query)

        print(f"vector dim: {len(vector)}")
        print()

        # 2️⃣ Qdrant Search
        print("🔹 Step 2: Vector Search (Qdrant)")

        results = self.vector_db.search(
            vector,
            top_k=5
        )

        print(f"Retrieved Chunks: {len(results)}")
        print()

        contexts = []

        if not results:
            print("⚠ No vector search results found.\n")

        for i, r in enumerate(results):

            payload = getattr(r, "payload", {}) or {}

            print(f"----- Chunk {i + 1} -----")
            print(f"score = {getattr(r, 'score', 'N/A')}")
            print(f"payload keys = {list(payload.keys())}")

            text = (
                payload.get("text")
                or payload.get("content")
                or payload.get("chunk")
                or ""
            )

            print(f"text preview = {text[:200]}")
            print()

            contexts.append(text)

        # 3️⃣ Prompt Build
        print("🔹 Step 3: Build Prompt")

        context_block = "\n\n".join(
            c for c in contexts if c
        )

        print(f"context length = {len(context_block)} chars")

        if not context_block:
            print("⚠ Prompt contains NO retrieved context")

        print()

        prompt = f"""
You are a helpful AI assistant.

Use ONLY the information provided in the context.

Context:
{context_block}

Question:
{query}

Answer:
"""

        # 4️⃣ LLM
        print("🔹 Step 4: Call Qwen2.5\n")

        answer = ""

        async for token in self.llm.stream_chat(prompt):
            print(token, end="", flush=True)
            answer += token

        print("\n")
        print("==============================")
        print("✅ RAG SMOKE TEST DONE")
        print("==============================")
        print()

        return answer


async def main():

    test = RAGSmokeTest()

    await test.run(
        "What is this system used for?"
    )


if __name__ == "__main__":

    asyncio.run(main())