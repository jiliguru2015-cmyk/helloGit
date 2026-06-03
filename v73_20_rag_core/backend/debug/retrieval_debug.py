import asyncio

from backend.core.rag_pipeline import RAGPipeline


async def main():

    rag = RAGPipeline()

    query = "What components does it use?"

    print("\n====================")
    print("QUERY")
    print("====================")
    print(query)

    print("\n====================")
    print("RESULTS")
    print("====================")

    results = await rag.retrieve(query)

    for i, item in enumerate(results, start=1):

        print(
            f"\n[{i}] score={item['score']:.6f}"
        )

        print(
            item["text"][:300]
        )


if __name__ == "__main__":
    asyncio.run(main())