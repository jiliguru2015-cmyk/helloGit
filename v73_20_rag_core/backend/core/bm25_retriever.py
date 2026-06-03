from rank_bm25 import BM25Okapi


class BM25Retriever:

    def __init__(self, doc_store):

        self.doc_store = doc_store
        self.bm25 = None
        self.chunks = []

    def build(self):

        docs = self.doc_store.load_all()

        self.chunks = [d["text"] for d in docs if "text" in d]

        tokenized_corpus = [
            doc.lower().split()
            for doc in self.chunks
        ]

        self.bm25 = BM25Okapi(tokenized_corpus)

    def search(self, query: str, top_k: int = 5):

        if self.bm25 is None:
            self.build()

        tokenized_query = query.lower().split()

        scores = self.bm25.get_scores(tokenized_query)

        ranked = sorted(
            enumerate(scores),
            key=lambda x: x[1],
            reverse=True
        )[:top_k]

        results = []

        for idx, score in ranked:
            results.append({
                "text": self.chunks[idx],
                "score": float(score),
                "source": "bm25"
            })

        return results