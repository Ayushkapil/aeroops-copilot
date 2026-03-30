"""
Ingestion: PDF Parser.

Parses PDF documents (FAA SOPs, ASRS reports) and extracts structured
text content suitable for downstream chunking and embedding.
"""

from __future__ import annotations


class PDFParser:
    """
    Parses PDF documents and yields page-level text with metadata.

    Wraps PyMuPDF (fitz) for robust extraction from complex aviation PDFs.

    Typical usage:
        parser = PDFParser()
        pages = parser.parse("data/raw/sop/faa_aim.pdf")
    """

    def parse(self, pdf_path: str) -> list[dict]:
        """
        Parse a PDF file and return page text with metadata.

        Args:
            pdf_path: Path to the PDF file.

        Returns:
            List of dicts with ``page_number`` (int), ``text`` (str), and
            ``source`` (str) keys.

        Raises:
            NotImplementedError: Until PDF parsing is implemented.
        """
        raise NotImplementedError("PDF parsing not yet implemented.")

    def parse_bytes(self, pdf_bytes: bytes, source: str = "upload") -> list[dict]:
        """
        Parse PDF content from raw bytes.

        Args:
            pdf_bytes: Raw PDF file content.
            source: Source identifier string (e.g. filename).

        Returns:
            List of page dicts (same structure as :meth:`parse`).

        Raises:
            NotImplementedError: Until PDF parsing is implemented.
        """
        raise NotImplementedError("PDF parsing not yet implemented.")
