# backend/core/chunker.py

class TextChunker:

    def chunk(
        self,
        text: str,
        chunk_size: int = 150,
        overlap: int = 30
    ):
        """
        将文本切分为知识点级别的 chunks。

        - 每行一个 chunk，去掉空行。
        - 行超过 chunk_size 时再使用滑动窗口切分。
        """

        if not text:
            return []

        # 按行切分并去除空行
        lines = [line.strip() for line in text.splitlines() if line.strip()]

        chunks = []

        for line in lines:

            # 行短于 chunk_size，直接添加
            if len(line) <= chunk_size:
                chunks.append(line)
                continue

            # 行过长，使用滑动窗口切分
            start = 0
            while start < len(line):
                end = start + chunk_size
                chunk = line[start:end].strip()
                if chunk:
                    chunks.append(chunk)
                start += chunk_size - overlap

        return chunks