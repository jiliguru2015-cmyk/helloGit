class ResultFusion:

    def build_prompt(self, query: str, contexts: list):

        context_text = "\n\n".join(contexts)

        return f"""
You are a RAG assistant.

Answer using ONLY the context below.

Context:
{context_text}

Question:
{query}

Answer:
"""