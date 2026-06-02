from fastapi import FastAPI
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
