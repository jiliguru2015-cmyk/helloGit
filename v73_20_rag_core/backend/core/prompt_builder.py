class PromptBuilder:

    def build(
        self,
        query: str,
        results
    ):

        contexts = []

        for r in results:

            payload = getattr(
                r,
                "payload",
                {}
            )

            text = payload.get(
                "text",
                ""
            )

            contexts.append(text)

        context_block = "\n\n".join(contexts)

        return f"""
You are a strict RAG assistant.

Answer ONLY using context.

Context:
{context_block}

Question:
{query}

Answer:
"""