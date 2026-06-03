class ContextBuilder:

    def __init__(self, max_chunks=5):
        self.max_chunks = max_chunks

    def build(self, docs):

        context_chunks = []
        seen = set()

        for doc in docs:

            text = doc.get("text")

            if not text:
                continue

            if text in seen:
                continue

            seen.add(text)

            context_chunks.append(text)

            if len(context_chunks) >= self.max_chunks:
                break

        return "\n\n".join(context_chunks)