"""Sobe a aplicação em modo de desenvolvimento.

    python run.py            # http://localhost:8000
    python run.py --porta 9000
"""

from __future__ import annotations

import argparse

import uvicorn


def main() -> None:
    parser = argparse.ArgumentParser(description="Mapa da Aprovação — servidor de desenvolvimento")
    parser.add_argument("--porta", type=int, default=8000)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--recarregar", action="store_true", help="reinicia ao salvar arquivos")
    args = parser.parse_args()

    uvicorn.run(
        "app.main:app",
        host=args.host,
        port=args.porta,
        reload=args.recarregar,
        log_level="info",
    )


if __name__ == "__main__":
    main()
