from pathlib import Path
from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel, Field
from app.core.config import settings
from app.rag.pipeline import RAGPipeline

router = APIRouter()
pipeline = RAGPipeline()


class ChatRequest(BaseModel):
    question: str = Field(min_length=1)
    history: list[dict] = Field(default_factory=list)


@router.get("/health")
def health():
    return {"status": "ok", "indexed_chunks": len(pipeline.index.chunks)}


@router.post("/documents/index")
async def index_documents(files: list[UploadFile] = File(...)):
    paths = []
    try:
        for file in files:
            if not file.filename or not file.filename.lower().endswith(".pdf"):
                raise HTTPException(status_code=400, detail="Only PDF files are supported.")
            safe_name = Path(file.filename).name
            path = settings.upload_dir / safe_name
            path.write_bytes(await file.read())
            paths.append(path)
        return pipeline.ingest(paths)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/chat")
def chat(request: ChatRequest):
    try:
        return pipeline.chat(request.question, request.history)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
