"""
Ingestion: Text Chunker.

Splits extracted document text into overlapping chunks suitable for
embedding and pgvector storage.
"""

from __future__ import annotations


class TextChunker:
    """
    Splits long document texts into fixed-size overlapping chunks.

    Supports both character-based and sentence-aware chunking strategies.

    Typical usage:
        chunker = TextChunker(chunk_size=512, chunk_overlap=64)
        chunks = chunker.chunk(pages)
    """

    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 64) -> None:
        """
        Args:
            chunk_size: Target size of each chunk in characters.
            chunk_overlap: Number of overlapping characters between adjacent chunks.
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(self, pages: list[dict]) -> list[dict]:
        """
        Split page texts into overlapping chunks.

        Args:
            pages: List of page dicts from :class:`~ingestion.pdf_parser.PDFParser`.

        Returns:
            List of chunk dicts with ``text`` (str), ``source`` (str), and
            ``page_number`` (int) keys.

        Raises:
            NotImplementedError: Until chunking logic is implemented.
        """
        raise NotImplementedError("Text chunking not yet implemented.")
