import asyncio

from backend.core.rag_pipeline import RAGPipeline


async def main():

    rag = RAGPipeline()

    result = await rag.ask(
        "What is this system used for?"
    )

    print("\n")
    print("=" * 50)

    print(result["answer"])

    print("=" * 50)

    print(
        f"chunks={result['chunks']}"
    )


if __name__ == "__main__":
    asyncio.run(main())