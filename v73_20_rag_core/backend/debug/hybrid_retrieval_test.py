import asyncio

from backend.core.rag_pipeline import RAGPipeline


async def main():

    rag = RAGPipeline()

    text = """
FastAPI is used for backend API.

Qdrant is used for vector storage.

Ollama is used for local LLM inference.

RAG combines retrieval and generation.
"""

    print("Ingesting document...")

    count = await rag.ingest(
        "doc1",
        text
    )

    print(f"Chunks inserted: {count}")

    print("\nSearching...\n")

    results = await rag.retrieve_with_scores(
        "What does the system use for vector storage?",
        top_k=5
    )

    for i, r in enumerate(results):

        payload = r.payload or {}

        print(
            f"[{i}] "
            f"score={r.score:.4f}"
        )

        print(
            payload.get(
                "chunk",
                ""
            )
        )

        print("-" * 60)


if __name__ == "__main__":
    asyncio.run(main())