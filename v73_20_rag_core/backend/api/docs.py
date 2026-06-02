from fastapi import APIRouter, UploadFile, File

router = APIRouter()


@router.post("/docs/upload")
async def upload(file: UploadFile = File(...)):
    return {
        "filename": file.filename,
        "status": "received"
    }
