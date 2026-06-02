import os

class DocumentLoader:

    def load(self, path: str) -> str:

        ext = os.path.splitext(path)[1].lower()

        if ext == ".txt":
            return self._load_txt(path)

        elif ext == ".md":
            return self._load_txt(path)

        elif ext == ".pdf":
            return self._load_pdf(path)

        else:
            raise ValueError(f"Unsupported file type: {ext}")

    def _load_txt(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    def _load_pdf(self, path: str):
        # lightweight PDF parser
        import fitz  # pymupdf

        doc = fitz.open(path)
        text = ""

        for page in doc:
            text += page.get_text()

        return text