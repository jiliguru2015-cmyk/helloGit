class RetrievalEngine:

    def deduplicate(self, points):

        seen = set()
        result = []

        for p in points:

            payload = getattr(p, "payload", {}) or {}

            text = payload.get("text", "").strip()

            if not text:
                continue

            if text in seen:
                continue

            seen.add(text)
            result.append(p)

        return result

    def diversify(self, points, max_per_source=2):

        result = []
        source_count = {}

        for p in points:

            payload = getattr(p, "payload", {}) or {}

            source = payload.get("source", "unknown")

            current = source_count.get(source, 0)

            if current >= max_per_source:
                continue

            source_count[source] = current + 1

            result.append(p)

        return result

    def rerank(self, points):

        return sorted(
            points,
            key=lambda x: getattr(x, "score", 0),
            reverse=True
        )

    def process(self, points):

        points = self.deduplicate(points)

        points = self.rerank(points)

        points = self.diversify(points)

        return points