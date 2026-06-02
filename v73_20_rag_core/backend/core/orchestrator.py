from backend.core.retrieval.retrieval_pipeline import RetrievalPipeline
from backend.core.ollama_client import OllamaClient


class Orchestrator:

    def __init__(self):

        self.retrieval = RetrievalPipeline()

        self.llm = OllamaClient()

    async def ask(self, query: str):

        retrieval = await self.retrieval.retrieve(query)

        results = retrieval["results"]

        citations = retrieval["citations"]

        contexts = []

        for idx, r in enumerate(results):

            payload = getattr(r, "payload", {}) or {}

            source = payload.get(
                "source",
                "unknown"
            )

            text = payload.get(
                "text",
                ""
            )

            contexts.append(
                f"[Source {idx+1}] {source}\n{text}"
            )

        context_block = "\n\n".join(
            contexts
        )

        source_block = "\n".join(
            [
                f"[{c['id']}] {c['source']}"
                for c in citations
            ]
        )

        prompt = f"""
You are a helpful AI assistant.

Answer ONLY using the provided context.

Context:
{context_block}

Question:
{query}

At the end include sources.

Sources:
{source_block}
"""

        async for token in self.llm.stream_chat(
            prompt
        ):
            yield token