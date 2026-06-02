from collections import Counter


class BM25Store:

    def __init__(self):

        self.documents = []

    def add_document(
        self,
        text,
        payload
    ):

        self.documents.append(
            {
                "text": text,
                "payload": payload
            }
        )

    def search(
        self,
        query,
        top_k=5
    ):

        query_terms = query.lower().split()

        scored = []

        for doc in self.documents:

            text = doc["text"].lower()

            tf = Counter(
                text.split()
            )

            score = 0

            for term in query_terms:
                score += tf.get(term, 0)

            scored.append(
                (
                    score,
                    doc
                )
            )

        scored.sort(
            key=lambda x: x[0],
            reverse=True
        )

        return scored[:top_k]