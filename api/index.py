"""Ponto de entrada para hospedagem serverless (Vercel).

A Vercel procura um objeto ASGI chamado `app` dentro de /api. Aqui só
reexportamos a aplicação — toda a lógica continua em /app.

Requisito: definir DATABASE_URL (Postgres/Supabase) nas variáveis de ambiente
do projeto. Sem banco externo, o sistema de arquivos serverless é efêmero e
os dados dos alunos se perderiam a cada cold start.
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from app.main import app  # noqa: E402,F401
