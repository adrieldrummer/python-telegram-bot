# Imagem de produção — servidor próprio (VPS) com SQLite ou Postgres.
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /opt/mapa

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY conteudo ./conteudo
COPY scripts ./scripts
COPY run.py ./

# o banco SQLite (quando usado) vive em volume separado
RUN mkdir -p /dados
ENV BANCO_CAMINHO=/dados/plataforma.db

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
