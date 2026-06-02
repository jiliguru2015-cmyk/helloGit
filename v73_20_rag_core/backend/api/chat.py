from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from backend.core.orchestrator import Orchestrator

router = APIRouter()

orchestrator = Orchestrator()


@router.get("/chat/stream")
async def chat_stream(query: str):

    async def gen():

        async for token in orchestrator.ask(query):

            yield f"data: {token}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(gen(), media_type="text/event-stream")