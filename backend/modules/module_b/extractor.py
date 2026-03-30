"""
Module B — Incident Analysis Engine: PDF Extractor.

Extracts raw text content from uploaded aviation incident PDF reports
using PyMuPDF (fitz).
"""

from __future__ import annotations


class PDFTextExtractor:
    """
    Extracts plain text from PDF incident reports page-by-page.

    Typical usage:
        extractor = PDFTextExtractor()
        text = extractor.extract(pdf_bytes)
    """

    def extract(self, pdf_bytes: bytes) -> str:
        """
        Extract all text from a PDF document provided as raw bytes.

        Args:
            pdf_bytes: Raw PDF file content.

        Returns:
            Concatenated plain text from all pages.

        Raises:
            NotImplementedError: Until PyMuPDF extraction is implemented.
        """
        raise NotImplementedError("PDF text extraction not yet implemented.")

    def extract_from_path(self, pdf_path: str) -> str:
        """
        Extract text from a PDF file located at the given path.

        Args:
            pdf_path: Filesystem path to the PDF.

        Returns:
            Concatenated plain text from all pages.

        Raises:
            NotImplementedError: Until PyMuPDF extraction is implemented.
        """
        raise NotImplementedError("PDF text extraction not yet implemented.")
