class TextChunker:

    def chunk(self, text: str, chunk_size=800, overlap=150):

        paragraphs = text.split("\n")

        chunks = []
        buffer = ""

        for p in paragraphs:

            if len(buffer) + len(p) > chunk_size:

                chunks.append(buffer.strip())
                buffer = buffer[-overlap:]  # overlap

            buffer += " " + p

        if buffer:
            chunks.append(buffer.strip())

        return chunks