import asyncio

from backend.core.embedding_store import EmbeddingStore
from backend.core.qdrant_store import QdrantStore
from backend.core.ollama_client import OllamaClient


class RAGVerifyTest:

    def __init__(self):

        self.embedder = EmbeddingStore()
        self.db = QdrantStore()
        self.llm = OllamaClient()

    async def query(self, question: str):

        print("\n==============================")
        print(f"🔍 QUERY: {question}")
        print("==============================\n")

        vector = await self.embedder.embed(question)

        results = self.db.search(vector, top_k=5)

        print(f"Retrieved: {len(results)} chunks\n")

        contexts = []

        for i, r in enumerate(results):

            payload = r.payload if hasattr(r, "payload") else {}

            text = payload.get("text", "")
            source = payload.get("source", "unknown")

            contexts.append(f"[Source: {source}]\n{text}")

            print(f"[{i}] score={getattr(r,'score','N/A')}")
            print(f"source={source}")
            print(f"text={text[:120]}\n")

        context_block = "\n\n".join(contexts)

        prompt = f"""
You are a strict RAG assistant.

Answer ONLY using the context below.

Context:
{context_block}

Question:
{question}

Answer:
"""

        print("🔹 LLM RESPONSE:\n")

        answer = ""

        async for token in self.llm.stream_generate(prompt):
            print(token, end="", flush=True)
            answer += token

        print("\n\n==============================")
        print("DONE")
        print("==============================\n")

        return answer


async def main():

    test = RAGVerifyTest()

    await test.query("What is this system used for?")
    await test.query("What components does it use?")


if __name__ == "__main__":
    asyncio.run(main())