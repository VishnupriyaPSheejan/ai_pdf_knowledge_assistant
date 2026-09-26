from app.rag.chunking import chunk_pages


def test_chunking_preserves_metadata():
    pages = [{"text": "hello " * 300, "page": 2, "source": "demo.pdf"}]
    chunks = chunk_pages(pages, chunk_size=100, overlap=20)
    assert len(chunks) > 1
    assert all(c["source"] == "demo.pdf" for c in chunks)
    assert all(c["page"] == 2 for c in chunks)
