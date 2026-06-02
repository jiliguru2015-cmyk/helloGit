class QueryRewriter:

    def rewrite(self, query: str) -> str:

        # v1 规则版（后面可升级 LLM rewrite）
        rules = [
            ("what", "system components architecture includes"),
            ("how", "mechanism workflow process"),
            ("used for", "purpose function goal"),
        ]

        rewritten = query.lower()

        for k, v in rules:
            if k in rewritten:
                rewritten += " " + v

        return rewritten