from backend.core.embedding_store import EmbeddingStore
from backend.core.qdrant_store import QdrantStore

from backend.core.retrieval.query_rewriter import QueryRewriter
from backend.core.retrieval.keyword_search import KeywordSearch
from backend.core.retrieval.citation_builder import CitationBuilder


class RetrievalPipeline:

    def __init__(self):

        self.embedder = EmbeddingStore()

        self.db = QdrantStore()

        self.rewriter = QueryRewriter()

        self.keyword_search = KeywordSearch()

        self.citation_builder = CitationBuilder()

    async def retrieve(
        self,
        query: str,
        top_k=5
    ):

        rewritten_query = self.rewriter.rewrite(query)

        vector = await self.embedder.embed(rewritten_query)

        vector_results = self.db.search(
            vector,
            top_k=top_k
        )

        keyword_results = self.keyword_search.search(
            query,
            vector_results
        )

        merged = []

        seen = set()

        for r in vector_results + keyword_results:

            pid = getattr(r, "id", None)

            if pid in seen:
                continue

            seen.add(pid)

            merged.append(r)

        citations = self.citation_builder.build(
            merged
        )

        return {
            "results": merged,
            "citations": citations
        }