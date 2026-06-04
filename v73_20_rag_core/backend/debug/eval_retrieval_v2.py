import asyncio

from backend.core.rag_pipeline import (
    RAGPipeline
)

from backend.core.evaluation.evaluator import (
    RetrievalEvaluator
)


async def main():

    rag = RAGPipeline()

    evaluator = RetrievalEvaluator(rag)

    result = await evaluator.evaluate_dataset(
        "backend/debug/eval_dataset_v2.json"
    )

    print()
    print("=" * 50)
    print("FINAL METRICS")
    print("=" * 50)

    for k, v in result.items():
        print(k, "=", v)


if __name__ == "__main__":
    asyncio.run(main())