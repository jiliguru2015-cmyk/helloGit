import ollama

from backend.config import settings


class OllamaClient:

    def __init__(self):
        self.model = settings.LLM_MODEL

    async def stream_chat(self, prompt: str):
        """
        Streaming generation interface
        Used by:
            - orchestrator.py
            - rag_smoke_test.py
            - chat SSE endpoint
        """

        stream = ollama.generate(
            model=self.model,
            prompt=prompt,
            stream=True
        )

        for chunk in stream:
            yield chunk.get("response", "")

    async def stream_generate(self, prompt: str):
        """
        Backward compatibility alias.
        Older code may still call stream_generate().
        """

        async for token in self.stream_chat(prompt):
            yield token