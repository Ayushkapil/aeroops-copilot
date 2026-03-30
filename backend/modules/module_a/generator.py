"""
Module A — SOP RAG Pipeline: Generator.

Generates a grounded, cited answer to the user's SOP question using
the reranked document chunks as context.
"""

from __future__ import annotations

from typing import Any


class SOPAnswerGenerator:
    """
    Generates LLM answers grounded in retrieved SOP document chunks,
    with inline citations referencing the source documents.

    Typical usage:
        generator = SOPAnswerGenerator(llm=langchain_llm)
        result = generator.generate(query, top_chunks)
    """

    def __init__(self, llm: Any = None) -> None:
        """
        Args:
            llm: Initialised LangChain LLM instance.
        """
        self.llm = llm

    def generate(self, query: str, chunks: list[dict]) -> dict:
        """
        Generate an answer with citations from the provided chunks.

        Args:
            query: User's aviation question.
            chunks: Top-reranked document chunks to use as context.

        Returns:
            Dict with ``answer`` (str) and ``citations`` (list[dict]).

        Raises:
            NotImplementedError: Until LLM generation is implemented.
        """
        raise NotImplementedError("LLM answer generation not yet implemented.")
