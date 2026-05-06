"""Section-aware text chunking with hierarchical metadata."""

import re
import hashlib

HEADING_PATTERNS = [
    (re.compile(r"^(Chapter\s+\d+[\.\d]*)\s*[—–-]?\s*(.*)", re.IGNORECASE | re.MULTILINE), "chapter"),
    (re.compile(r"^(Section\s+\d+[\.\d]*)\s*[—–-]?\s*(.*)", re.IGNORECASE | re.MULTILINE), "section"),
    (re.compile(r"^(\d+\.\d+[\.\d]*)\s+([A-Z].*)", re.MULTILINE), "subsection"),
    (re.compile(r"^([A-Z][A-Z\s]{4,})$", re.MULTILINE), "heading"),
    (re.compile(r"^((?:PART|FAR|AC)\s+\d+[\.\d\-]*)\s*[—–-]?\s*(.*)", re.IGNORECASE | re.MULTILINE), "regulation"),
]

CHECKLIST_RE = re.compile(
    r"(?:^|\n)\s*(?:\d+[\.\)]\s|[a-z][\.\)]\s|•\s|[-–]\s|STEP\s+\d+|NOTE:|CAUTION:|WARNING:)",
    re.IGNORECASE
)


def detect_sections(text: str) -> list[dict]:
    sections = []
    for pattern, level in HEADING_PATTERNS:
        for match in pattern.finditer(text):
            title = match.group(0).strip()
            sections.append({"position": match.start(), "level": level, "title": title[:120]})
    sections.sort(key=lambda x: x["position"])
    return sections


def get_section_at_position(sections: list[dict], pos: int) -> dict:
    result = {"chapter": "General", "section": "General", "subsection": ""}
    for s in sections:
        if s["position"] > pos:
            break
        result[s["level"]] = s["title"]
    return result


def is_checklist_content(text: str) -> bool:
    matches = len(CHECKLIST_RE.findall(text))
    return matches >= 2


def chunk_text(
    text: str,
    source_file: str,
    page_number: int = 0,
    chunk_size: int = 1500,
    overlap: int = 300,
) -> list[dict]:
    sections = detect_sections(text)
    chunks = []
    start = 0
    idx = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        if end < len(text):
            nl = text.rfind("\n\n", start + chunk_size // 3, end)
            if nl > start:
                end = nl
            else:
                nl = text.rfind("\n", start + chunk_size // 2, end)
                if nl > start:
                    end = nl

        chunk_str = text[start:end].strip()
        if len(chunk_str) < 20:
            start = end
            continue

        section_info = get_section_at_position(sections, start)
        content_hash = hashlib.sha256(
            f"{source_file}:{page_number}:{idx}:{chunk_str[:100]}".encode()
        ).hexdigest()

        chunks.append({
            "content": chunk_str,
            "metadata": {
                "source_file": source_file,
                "page_number": page_number,
                "chapter": section_info["chapter"],
                "section_title": section_info["section"],
                "subsection": section_info["subsection"],
                "chunk_index": idx,
                "is_checklist": is_checklist_content(chunk_str),
                "char_count": len(chunk_str),
            },
            "content_hash": content_hash,
        })
        idx += 1
        start = end - overlap if end < len(text) else len(text)

    return chunks


def chunk_pages(pages: list[dict], source_file: str) -> list[dict]:
    all_chunks = []
    for page in pages:
        page_chunks = chunk_text(
            page["text"],
            source_file=source_file,
            page_number=page["page_number"],
        )
        all_chunks.extend(page_chunks)
    return all_chunks
