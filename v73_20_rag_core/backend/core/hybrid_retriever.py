from backend.core.retriever import Retriever


class HybridRetriever:

    def __init__(self):

        self.vector_retriever = Retriever()

    async def retrieve(
        self,
        query: str,
        top_k: int = 5
    ):

        results = await self.vector_retriever.retrieve(
            query=query,
            top_k=top_k
        )

        return results