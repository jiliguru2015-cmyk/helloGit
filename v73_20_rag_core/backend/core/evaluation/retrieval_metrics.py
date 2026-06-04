class RetrievalMetrics:

    @staticmethod
    def recall_at_k(
        retrieved_texts,
        expected_keywords,
    ):

        retrieved_blob = " ".join(
            retrieved_texts
        ).lower()

        hits = 0

        for keyword in expected_keywords:

            if keyword.lower() in retrieved_blob:
                hits += 1

        return hits / len(expected_keywords)

    @staticmethod
    def precision_at_k(
        retrieved_texts,
        expected_keywords,
    ):

        relevant = 0

        for text in retrieved_texts:

            text_lower = text.lower()

            for keyword in expected_keywords:

                if keyword.lower() in text_lower:
                    relevant += 1
                    break

        if not retrieved_texts:
            return 0

        return relevant / len(retrieved_texts)

    @staticmethod
    def hit_rate(
        retrieved_texts,
        expected_keywords,
    ):

        blob = " ".join(
            retrieved_texts
        ).lower()

        for keyword in expected_keywords:

            if keyword.lower() in blob:
                return 1

        return 0

    @staticmethod
    def mrr(
        retrieved_texts,
        expected_keywords,
    ):

        for idx, text in enumerate(
            retrieved_texts,
            start=1
        ):

            lower = text.lower()

            for keyword in expected_keywords:

                if keyword.lower() in lower:
                    return 1 / idx

        return 0