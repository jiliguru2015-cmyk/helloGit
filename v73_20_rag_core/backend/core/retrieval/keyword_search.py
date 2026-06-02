class KeywordSearch:

    def search(self, query: str, results):

        query = query.lower()

        matched = []

        for r in results:

            payload = getattr(r, "payload", {}) or {}

            text = payload.get("text", "")

            if query in text.lower():
                matched.append(r)

        return matched