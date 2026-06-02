class ContextBuilder:

    def build(
        self,
        results
    ):

        chunks = []

        for r in results:

            payload = r.payload or {}

            text = (
                payload.get("text")
                or payload.get("chunk")
                or ""
            )

            if text:
                chunks.append(text)

        return "\n\n".join(chunks)