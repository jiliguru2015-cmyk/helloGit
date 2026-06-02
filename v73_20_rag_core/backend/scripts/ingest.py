import asyncio
import sys
from pathlib import Path

from backend.core.document_ingest_pipeline import DocumentIngestPipeline


async def ingest_file(file_path: str):

    path = Path(file_path)

    if not path.exists():
        print(f"❌ File not found: {file_path}")
        return

    text = path.read_text(encoding="utf-8", errors="ignore")

    pipeline = DocumentIngestPipeline()

    count = await pipeline.ingest_text(
        text=text,
        source=path.name
    )

    print("\n====================")
    print("✅ INGEST COMPLETE (V73.26)")
    print("====================")
    print(f"file   : {path.name}")
    print(f"chunks : {count}")


async def main():

    if len(sys.argv) < 2:
        print("Usage: python -m backend.scripts.ingest <file_path>")
        return

    await ingest_file(sys.argv[1])


if __name__ == "__main__":
    asyncio.run(main())