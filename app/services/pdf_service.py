from pathlib import Path
import fitz


def extract_pdf(path: Path) -> list[dict]:
    """Extract page-level text so citations can point to exact PDF pages."""
    pages = []
    with fitz.open(path) as doc:
        for page_number, page in enumerate(doc, start=1):
            text = page.get_text("text").strip()
            if text:
                pages.append({
                    "text": text,
                    "page": page_number,
                    "source": path.name,
                })
    return pages
