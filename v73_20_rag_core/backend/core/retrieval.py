class HybridRetriever:

    def merge(
        self,
        vector_results,
        bm25_results,
        top_k=5
    ):

        merged = {}

        for r in vector_results:

            text = r.payload.get(
                "text",
                ""
            )

            merged[text] = merged.get(
                text,
                0
            ) + r.score

        for text, score in bm25_results:

            merged[text] = merged.get(
                text,
                0
            ) + score

        ranked = sorted(
            merged.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return ranked[:top_k]