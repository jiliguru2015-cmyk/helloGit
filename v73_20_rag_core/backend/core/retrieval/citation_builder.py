class CitationBuilder:

    def build(self, results):

        citations = []

        for idx, r in enumerate(results):

            payload = getattr(r, "payload", {}) or {}

            citations.append(
                {
                    "id": idx + 1,
                    "source": payload.get("source", "unknown"),
                    "chunk_id": payload.get("chunk_id", -1),
                    "text": payload.get("text", "")
                }
            )

        return citations