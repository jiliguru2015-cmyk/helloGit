import asyncio
from backend.core.rag_pipeline import RAGPipeline


async def main():

    rag = RAGPipeline()

    await rag.ingest(
        "doc1",
        "FastAPI is a backend framework. Qdrant is a vector database. Ollama is a LLM runtime."
    )

    result = await rag.ask("What components does it use?")

    print("\n====================")
    print("ANSWER:")
    print("====================")
    print(result["answer"])

    print("\n====================")
    print("CONTEXT:")
    print("====================")

    for c in result["context"]:
        print(c)


if __name__ == "__main__":
    asyncio.run(main())