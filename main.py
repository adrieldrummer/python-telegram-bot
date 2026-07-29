"""Entrypoint na raiz do projeto.

Existe para hospedagens que procuram a aplicação ASGI em `main.py` na raiz —
é o caso do preset FastAPI da Vercel. A aplicação de verdade continua em
`app/main.py`; aqui só reexportamos.
"""

from __future__ import annotations

from app.main import app  # noqa: F401

__all__ = ["app"]
