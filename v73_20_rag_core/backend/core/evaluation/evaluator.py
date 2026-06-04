import json

from backend.core.evaluation.retrieval_metrics import (
    RetrievalMetrics
)


class RetrievalEvaluator:

    def __init__(self, rag):

        self.rag = rag

    async def evaluate_dataset(
        self,
        dataset_path
    ):

        with open(
            dataset_path,
            "r",
            encoding="utf-8"
        ) as f:

            dataset = json.load(f)

        total_recall = 0
        total_precision = 0
        total_hit = 0
        total_mrr = 0

        count = len(dataset)

        for sample in dataset:
            query = sample["query"]
            expected = sample["expected"]

            docs = await self.rag.retrieve(
                query
            )

            texts = [
                d["text"]
                for d in docs
                if d.get("text")
            ]
            print()
            print("=" * 50)
            print("QUERY :", query)
            print("EXPECTED :", expected)
            for idx, t in enumerate(texts[:3], start=1):
                print(f"[{idx}] {t[:120]}")

            total_recall += (
                RetrievalMetrics.recall_at_k(
                    texts,
                    expected
                )
            )

            total_precision += (
                RetrievalMetrics.precision_at_k(
                    texts,
                    expected
                )
            )

            total_hit += (
                RetrievalMetrics.hit_rate(
                    texts,
                    expected
                )
            )

            total_mrr += (
                RetrievalMetrics.mrr(
                    texts,
                    expected
                )
            )

        return {
            "Recall@K":
                round(total_recall / count, 4),

            "Precision@K":
                round(total_precision / count, 4),

            "HitRate":
                round(total_hit / count, 4),

            "MRR":
                round(total_mrr / count, 4)
        }