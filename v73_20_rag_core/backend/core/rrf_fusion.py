class RRFFusion:

    def __init__(self, k=60):
        self.k = k

    def fuse(
        self,
        dense_results,
        bm25_results,
        top_k=None
    ):

        scores = {}

        # Dense
        for rank, item in enumerate(
            dense_results,
            start=1
        ):

            text = item.get("text")

            if not text:
                continue

            if text not in scores:
                scores[text] = {
                    "text": text,
                    "score": 0.0
                }

            scores[text]["score"] += (
                1.0 / (self.k + rank)
            )

        # BM25
        for rank, item in enumerate(
            bm25_results,
            start=1
        ):

            text = item.get("text")

            if not text:
                continue

            if text not in scores:
                scores[text] = {
                    "text": text,
                    "score": 0.0
                }

            scores[text]["score"] += (
                1.0 / (self.k + rank)
            )

        results = sorted(
            scores.values(),
            key=lambda x: x["score"],
            reverse=True
        )

        if top_k:
            results = results[:top_k]

        return results