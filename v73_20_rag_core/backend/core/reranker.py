class Reranker:

    def rerank(
        self,
        query: str,
        chunks: list
    ):
        """
        V73.27

        先占位实现。

        后续:
        CrossEncoder
        BGE-Reranker
        Cohere Rerank

        都挂这里。
        """

        if not chunks:
            return []

        scored = []

        query_terms = set(
            query.lower().split()
        )

        for chunk in chunks:

            text = ""

            if isinstance(chunk, dict):
                text = chunk.get("text", "")
            else:
                text = str(chunk)

            score = 0

            lower_text = text.lower()

            for term in query_terms:
                if term in lower_text:
                    score += 1

            scored.append(
                (score, chunk)
            )

        scored.sort(
            key=lambda x: x[0],
            reverse=True
        )

        return [
            item[1]
            for item in scored
        ]