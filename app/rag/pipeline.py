from pathlib import Path
from app.core.config import settings
from app.services.pdf_service import extract_pdf
from app.rag.chunking import chunk_pages
from app.rag.index import HybridIndex
from app.services.llm_service import LLMService


class RAGPipeline:
    def __init__(self):
        self.index = HybridIndex(settings.index_dir, settings.embedding_model)
        self.llm = LLMService()

    def ingest(self, paths: list[Path]) -> dict:
        all_pages = []
        for path in paths:
            all_pages.extend(extract_pdf(path))
        chunks = chunk_pages(all_pages, settings.chunk_size, settings.chunk_overlap)
        if not chunks:
            raise ValueError("No extractable text was found in the uploaded PDFs.")
        self.index.build(chunks)
        return {"files": len(paths), "pages": len(all_pages), "chunks": len(chunks)}

    def chat(self, question: str, history: list[dict]) -> dict:
        context = self.index.search(question, settings.top_k)
        answer = self.llm.answer(question, context, history)
        sources = [
            {"source": c["source"], "page": c["page"], "score": c["score"]}
            for c in context
        ]
        return {"answer": answer, "sources": sources}
