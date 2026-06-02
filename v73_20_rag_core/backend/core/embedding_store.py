import ollama
from backend.config import settings


class EmbeddingStore:

    def __init__(self):
        self.model = settings.EMBEDDING_MODEL

    async def embed(self, text: str):

        res = ollama.embeddings(
            model=self.model,
            prompt=text
        )

        return res["embedding"]
