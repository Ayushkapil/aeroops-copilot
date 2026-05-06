"""PDF text extraction using PyMuPDF."""

import fitz  # PyMuPDF
from pathlib import Path


def extract_pages(pdf_path: str | Path) -> list[dict]:
    """Extract text from each page of a PDF.
    Returns list of {page_number, text}.
    """
    doc = fitz.open(str(pdf_path))
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text("text")
        if text.strip():
            pages.append({"page_number": i + 1, "text": text.strip()})
    doc.close()
    return pages


def extract_text_from_bytes(file_bytes: bytes) -> list[dict]:
    """Extract text from PDF bytes (for uploaded files)."""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text("text")
        if text.strip():
            pages.append({"page_number": i + 1, "text": text.strip()})
    doc.close()
    return pages


def extract_full_text(pdf_path: str | Path) -> str:
    """Extract all text from PDF as a single string."""
    pages = extract_pages(pdf_path)
    return "\n\n".join(p["text"] for p in pages)
