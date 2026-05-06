"""PDF text extraction for incident reports."""

import fitz
import io


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from uploaded PDF bytes."""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    doc.close()
    return text.strip()


def extract_text_from_file(file_path: str) -> str:
    """Extract text from a PDF file path."""
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    doc.close()
    return text.strip()
