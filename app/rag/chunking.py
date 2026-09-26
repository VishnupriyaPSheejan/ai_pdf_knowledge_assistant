def chunk_pages(pages: list[dict], chunk_size: int = 800, overlap: int = 120) -> list[dict]:
    chunks = []
    for page in pages:
        text = " ".join(page["text"].split())
        if not text:
            continue
        start = 0
        chunk_no = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            piece = text[start:end].strip()
            if piece:
                chunks.append({
                    "text": piece,
                    "source": page["source"],
                    "page": page["page"],
                    "chunk": chunk_no,
                })
                chunk_no += 1
            if end >= len(text):
                break
            start = max(0, end - overlap)
    return chunks
