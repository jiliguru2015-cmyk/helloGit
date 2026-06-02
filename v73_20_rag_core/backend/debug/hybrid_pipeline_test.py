import asyncio

from backend.core.rag_pipeline import RAGPipeline


async def main():

    rag = RAGPipeline()

    result = await rag.ask(
        "What components does it use?"
    )

    print(result["answer"])


if __name__ == "__main__":
    asyncio.run(main())