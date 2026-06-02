from pydantic import BaseModel


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
