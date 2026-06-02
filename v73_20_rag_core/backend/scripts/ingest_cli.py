import asyncio
import sys
from pathlib import Path

from backend.core.pipeline.document_ingest_pipeline import DocumentIngestPipeline


async def main(file_path: str):

    path = Path(file_path)

    if not path.exists():
        print(f"File not found: {file_path}")
        return

    text = path.read_text(encoding="utf-8")

    pipeline = DocumentIngestPipeline()
    result = await pipeline.ingest(text, source=path.name)

    print("\n===================")
    print("INGEST DONE")
    print("===================")
    print(result)


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python -m backend.scripts.ingest_cli <file.txt>")
        sys.exit(1)

    asyncio.run(main(sys.argv[1]))