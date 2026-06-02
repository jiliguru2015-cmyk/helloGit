from backend.core.ollama_client import OllamaClient


class Generator:

    def __init__(self):
        self.llm = OllamaClient()

    async def generate(
        self,
        prompt: str
    ) -> str:

        answer = ""

        async for token in self.llm.stream_generate(
            prompt
        ):
            answer += token

        return answer