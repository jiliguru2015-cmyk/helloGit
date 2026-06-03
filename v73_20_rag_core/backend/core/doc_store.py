import json
import os


class DocStore:

    def __init__(self, path="backend/data/chunks.jsonl"):

        self.path = path

        os.makedirs(os.path.dirname(self.path), exist_ok=True)

        print(f"📦 DocStore ACTIVE PATH: {os.path.abspath(self.path)}")

    def add(self, payload: dict):

        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")

    def load_all(self):

        if not os.path.exists(self.path):
            return []

        docs = []

        with open(self.path, "r", encoding="utf-8") as f:

            for line in f:
                line = line.strip()
                if not line:
                    continue

                try:
                    docs.append(json.loads(line))
                except:
                    continue

        return docs

    def clear(self):

        if os.path.exists(self.path):
            os.remove(self.path)