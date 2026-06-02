from pathlib import Path

ROOT = Path("v73_20_rag_core")


def write_file(path, content):
    file_path = ROOT / path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding="utf-8")
    print("created:", file_path)


# ---------------------------
# requirements
# ---------------------------
def generate_requirements():
    write_file(
        "requirements.txt",
        """fastapi
uvicorn
aiohttp
python-multipart
qdrant-client
ollama
pydantic
python-dotenv
python-docx
pymupdf
"""
    )


# ---------------------------
# config
# ---------------------------
def generate_config():
    write_file(
        "backend/config.py",
        """from pydantic import BaseModel


class Settings(BaseModel):
    APP_NAME: str = "v73.20 RAG Core"

    OLLAMA_BASE_URL: str = "http://localhost:11434"

    LLM_MODEL: str = "qwen2.5"

    EMBEDDING_MODEL: str = "nomic-embed-text"

    QDRANT_HOST: str = "localhost"

    QDRANT_PORT: int = 6333

    COLLECTION_NAME: str = "enterprise_docs"

    TOP_K: int = 5


settings = Settings()
"""
    )


# ---------------------------
# app
# ---------------------------
def generate_app():
    write_file(
        "backend/app.py",
        """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.chat import router as chat_router
from backend.api.docs import router as docs_router

app = FastAPI(title="v73.20 RAG Core")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api")
app.include_router(docs_router, prefix="/api")


@app.get("/")
async def root():
    return {"status": "ok", "version": "v73.20"}
"""
    )


# ---------------------------
# api init
# ---------------------------
def generate_api_init():
    write_file("backend/api/__init__.py", "")


def generate_core_init():
    write_file("backend/core/__init__.py", "")


# ---------------------------
# chat API
# ---------------------------
def generate_chat_api():
    write_file(
        "backend/api/chat.py",
        """from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from backend.core.ollama_client import OllamaClient

router = APIRouter()

client = OllamaClient()


@router.get("/chat/stream")
async def chat_stream(query: str):

    async def gen():

        async for token in client.stream_generate(query):
            yield f"data: {token}\\n\\n"

        yield "data: [DONE]\\n\\n"

    return StreamingResponse(gen(), media_type="text/event-stream")
"""
    )


# ---------------------------
# docs API
# ---------------------------
def generate_docs_api():
    write_file(
        "backend/api/docs.py",
        """from fastapi import APIRouter, UploadFile, File

router = APIRouter()


@router.post("/docs/upload")
async def upload(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "status": "received"
    }
"""
    )


# ---------------------------
# ollama client
# ---------------------------
def generate_ollama_client():
    write_file(
        "backend/core/ollama_client.py",
        """import ollama
from backend.config import settings


class OllamaClient:

    def __init__(self):
        self.model = settings.LLM_MODEL

    async def stream_generate(self, prompt: str):

        stream = ollama.generate(
            model=self.model,
            prompt=prompt,
            stream=True
        )

        for chunk in stream:
            yield chunk.get("response", "")
"""
    )


# ---------------------------
# embedding
# ---------------------------
def generate_embedding():
    write_file(
        "backend/core/embedding_store.py",
        """import ollama
from backend.config import settings


class EmbeddingStore:

    def __init__(self):
        self.model = settings.EMBEDDING_MODEL

    async def embed(self, text: str):

        res = ollama.embeddings(
            model=self.model,
            prompt=text
        )

        return res["embedding"]
"""
    )


# ---------------------------
# qdrant
# ---------------------------
def generate_qdrant():
    write_file(
        "backend/core/qdrant_store.py",
        """from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from backend.config import settings


class QdrantStore:

    def __init__(self):

        self.client = QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT
        )

        self.collection = settings.COLLECTION_NAME

    def ensure(self):

        cols = self.client.get_collections().collections
        names = [c.name for c in cols]

        if self.collection in names:
            return

        self.client.create_collection(
            collection_name=self.collection,
            vectors_config=VectorParams(
                size=768,
                distance=Distance.COSINE
            )
        )

    def upsert(self, _id, vector, payload):

        self.ensure()

        self.client.upsert(
            collection_name=self.collection,
            points=[
                PointStruct(
                    id=_id,
                    vector=vector,
                    payload=payload
                )
            ]
        )

    def search(self, vector, top_k=5):

        self.ensure()

        return self.client.search(
            collection_name=self.collection,
            query_vector=vector,
            limit=top_k
        )
"""
    )


# ---------------------------
# main
# ---------------------------
def generate_all():

    print("\n=== v73.20 RAG CORE FIXED ===\n")

    generate_requirements()
    generate_config()
    generate_app()
    generate_api_init()
    generate_core_init()
    generate_chat_api()
    generate_docs_api()
    generate_ollama_client()
    generate_embedding()
    generate_qdrant()

    print("\nDONE\n")


if __name__ == "__main__":
    generate_all()