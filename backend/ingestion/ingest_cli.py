"""CLI for ingesting SOP PDFs into pgvector."""

import argparse
import logging
from pathlib import Path
from tqdm import tqdm

from ingestion.pdf_parser import extract_pages
from ingestion.chunker import chunk_pages
from ingestion.embedder import embed_and_store
from db.pgvector_client import PgVectorClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def ingest_directory(source_dir: str):
    db = PgVectorClient()
    db.init_db()

    source_path = Path(source_dir)
    pdf_files = list(source_path.glob("*.pdf")) + list(source_path.glob("*.txt"))

    if not pdf_files:
        logger.warning(f"No PDF/TXT files found in {source_dir}")
        return

    for fp in tqdm(pdf_files, desc="Ingesting documents"):
        logger.info(f"Processing {fp.name}")

        if fp.suffix == ".pdf":
            pages = extract_pages(fp)
        else:
            text = fp.read_text(encoding="utf-8", errors="ignore")
            pages = [{"page_number": 1, "text": text}]

        chunks = chunk_pages(pages, source_file=fp.name)

        # Skip already ingested
        new_chunks = [c for c in chunks if not db.chunk_exists(c["content_hash"])]
        if not new_chunks:
            logger.info(f"Skipping {fp.name} — already ingested.")
            continue

        embed_and_store(new_chunks, db)
        logger.info(f"Ingested {len(new_chunks)} chunks from {fp.name}")

    db.close()
    logger.info("Ingestion complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest SOP documents")
    parser.add_argument("--source", required=True, help="Directory containing PDF/TXT files")
    args = parser.parse_args()
    ingest_directory(args.source)
