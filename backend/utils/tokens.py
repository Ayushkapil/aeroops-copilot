"""Token estimation and context trimming utilities."""


def estimate_tokens(text: str) -> int:
    """Rough token estimate: ~4 chars per token for English."""
    return len(text) // 4


def trim_context_to_limit(chunks: list[dict], max_tokens: int = 6000) -> list[dict]:
    """Trim chunks to fit within token budget.
    Keeps highest-scored chunks first, drops lowest until under limit.
    """
    total = 0
    kept = []
    for chunk in chunks:
        chunk_tokens = estimate_tokens(chunk.get("content", ""))
        if total + chunk_tokens > max_tokens:
            break
        kept.append(chunk)
        total += chunk_tokens
    return kept
