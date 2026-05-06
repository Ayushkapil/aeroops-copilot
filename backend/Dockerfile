FROM python:3.11-slim

# System deps for psycopg2 and PyMuPDF
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python deps (cached unless requirements.txt changes)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Pre-download models at build time so startup is fast
RUN python -c "\
from sentence_transformers import CrossEncoder, SentenceTransformer; \
CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2'); \
SentenceTransformer('all-MiniLM-L6-v2')"

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
