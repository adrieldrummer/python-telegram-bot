"""Acesso ao banco de dados.

A plataforma roda em dois modos, com o mesmo código de aplicação:

* **SQLite** (padrão) — desenvolvimento e servidor próprio (VPS). Zero
  configuração, arquivo em `dados/plataforma.db`.
* **PostgreSQL** — quando existe `DATABASE_URL`. É o modo usado em
  hospedagem sem disco persistente (Vercel + Supabase, por exemplo).

Para não espalhar dialeto SQL pelo projeto, todas as consultas são escritas
no dialeto SQLite e traduzidas aqui quando o destino é Postgres. Os campos de
data continuam sendo TEXTO nos dois bancos, o que mantém idênticos os
`substr(criado_em, 1, 10)` espalhados pelos relatórios.
"""

from __future__ import annotations

import re
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterable, Iterator, Optional

from .config import RAIZ, config

_CAMINHO_ATUAL: Optional[Path] = None


def usando_postgres() -> bool:
    return bool(config.database_url)


def caminho_banco() -> Path:
    return _CAMINHO_ATUAL or config.banco_caminho


def definir_banco(caminho: Path | str) -> None:
    """Usado pelos testes e por scripts para apontar para outro arquivo."""
    global _CAMINHO_ATUAL
    _CAMINHO_ATUAL = Path(caminho)


# --------------------------------------------------------------------------
#  Tradução SQLite → Postgres
# --------------------------------------------------------------------------

_RE_DATETIME_RELATIVO = re.compile(
    r"datetime\(\s*'now'\s*,\s*'([+-]?\d+)\s+(day|days|hour|hours|minute|minutes)'\s*\)",
    re.I,
)


def traduzir(sql: str) -> str:
    """Converte o SQL escrito para SQLite no equivalente em Postgres."""
    convertido = sql
    convertido = _RE_DATETIME_RELATIVO.sub(
        lambda m: f"to_char(now() + interval '{m.group(1)} {m.group(2)}', 'YYYY-MM-DD HH24:MI:SS')",
        convertido,
    )
    convertido = re.sub(
        r"datetime\(\s*'now'\s*\)", "to_char(now(), 'YYYY-MM-DD HH24:MI:SS')", convertido, flags=re.I
    )
    if re.search(r"INSERT\s+OR\s+IGNORE", convertido, re.I):
        convertido = re.sub(r"INSERT\s+OR\s+IGNORE\s+INTO", "INSERT INTO", convertido, flags=re.I)
        if "ON CONFLICT" not in convertido.upper():
            convertido = convertido.rstrip().rstrip(";") + " ON CONFLICT DO NOTHING"
    convertido = re.sub(r"\bLIKE\s+\?", "ILIKE ?", convertido, flags=re.I)
    convertido = convertido.replace("?", "%s")
    return convertido


class CursorPG:
    """Espelha a parte da API de sqlite3.Cursor que a aplicação usa."""

    def __init__(self, cursor, lastrowid: Optional[int] = None):
        self._cursor = cursor
        self.lastrowid = lastrowid

    @property
    def rowcount(self) -> int:
        return self._cursor.rowcount

    def fetchone(self):
        return self._cursor.fetchone()

    def fetchall(self):
        return self._cursor.fetchall()


# tabelas cuja chave primária não é uma coluna `id` — não aceitam RETURNING id
SEM_COLUNA_ID = {"progresso_dias", "medalhas_aluno"}
_RE_INSERT_ALVO = re.compile(r"INSERT\s+INTO\s+([a-z_]+)", re.I)


class ConexaoPG:
    """Adaptador para o código continuar chamando `con.execute(sql, params)`."""

    def __init__(self, conexao):
        self._conexao = conexao

    def execute(self, sql: str, params: Iterable[Any] = ()):  # noqa: A003
        texto = traduzir(sql)
        alvo = _RE_INSERT_ALVO.search(texto)
        precisa_id = (
            texto.lstrip().upper().startswith("INSERT")
            and "RETURNING" not in texto.upper()
            and "ON CONFLICT DO NOTHING" not in texto.upper()
            and bool(alvo)
            and alvo.group(1).lower() not in SEM_COLUNA_ID
        )
        if precisa_id:
            texto = texto.rstrip().rstrip(";") + " RETURNING id"
        cursor = self._conexao.cursor()
        cursor.execute(texto, tuple(params))
        ultimo = None
        if precisa_id:
            try:
                linha = cursor.fetchone()
                if linha is not None:
                    ultimo = int(linha["id"]) if isinstance(linha, dict) else int(linha[0])
            except Exception:  # tabelas sem coluna id
                ultimo = None
        return CursorPG(cursor, ultimo)

    def executescript(self, sql: str) -> None:
        with self._conexao.cursor() as cursor:
            cursor.execute(sql)

    def close(self) -> None:
        self._conexao.close()


def conectar():
    if usando_postgres():
        import psycopg
        from psycopg.rows import dict_row

        bruto = psycopg.connect(config.database_url, autocommit=True, row_factory=dict_row)
        if config.db_schema and config.db_schema != "public":
            with bruto.cursor() as cursor:
                cursor.execute(f'SET search_path TO "{config.db_schema}", public')
        return ConexaoPG(bruto)

    destino = caminho_banco()
    destino.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(destino, timeout=15, isolation_level=None)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    con.execute("PRAGMA journal_mode = WAL")
    con.execute("PRAGMA busy_timeout = 8000")
    return con


@contextmanager
def sessao() -> Iterator[Any]:
    con = conectar()
    try:
        yield con
    finally:
        con.close()


@contextmanager
def transacao() -> Iterator[Any]:
    con = conectar()
    try:
        con.execute("BEGIN")
        yield con
        con.execute("COMMIT")
    except Exception:
        con.execute("ROLLBACK")
        raise
    finally:
        con.close()


def criar_esquema() -> None:
    arquivo = "schema_pg.sql" if usando_postgres() else "schema.sql"
    sql = (Path(__file__).parent / arquivo).read_text(encoding="utf-8")
    if usando_postgres() and config.db_schema != "public":
        sql = (
            f'CREATE SCHEMA IF NOT EXISTS "{config.db_schema}";\n'
            f'SET search_path TO "{config.db_schema}";\n\n' + sql
        )
    with sessao() as con:
        con.executescript(sql)
    aplicar_migracoes()


# colunas acrescentadas depois da primeira versão do esquema
COLUNAS_NOVAS: tuple[tuple[str, str, str], ...] = (
    # sem compra registrada, o aluno nasce no plano de entrada — dar o plano
    # completo por omissão entregaria de graça o que é vendido no upgrade
    ("alunos", "plano", "TEXT NOT NULL DEFAULT 'recruta'"),
    ("alunos", "plano_ate", "TEXT"),
)


def aplicar_migracoes() -> list[str]:
    """Acrescenta colunas que faltam em bancos criados por versões anteriores."""
    aplicadas: list[str] = []
    with sessao() as con:
        for tabela, coluna, definicao in COLUNAS_NOVAS:
            if usando_postgres():
                con.execute(
                    f"ALTER TABLE {tabela} ADD COLUMN IF NOT EXISTS {coluna} {definicao}"
                )
                continue
            existentes = {
                linha["name"] for linha in con.execute(f"PRAGMA table_info({tabela})").fetchall()
            }
            if coluna not in existentes:
                con.execute(f"ALTER TABLE {tabela} ADD COLUMN {coluna} {definicao}")
                aplicadas.append(f"{tabela}.{coluna}")
    return aplicadas


# --- helpers de consulta ---------------------------------------------------


def buscar_um(con, sql: str, params: Iterable[Any] = ()):
    return con.execute(sql, tuple(params)).fetchone()


def buscar_todos(con, sql: str, params: Iterable[Any] = ()) -> list:
    return list(con.execute(sql, tuple(params)).fetchall())


def executar(con, sql: str, params: Iterable[Any] = ()):
    return con.execute(sql, tuple(params))


def valor(con, sql: str, params: Iterable[Any] = (), padrao: Any = 0) -> Any:
    linha = buscar_um(con, sql, params)
    if linha is None:
        return padrao
    resultado = list(linha.values())[0] if isinstance(linha, dict) else linha[0]
    return padrao if resultado is None else resultado


__all__ = [
    "RAIZ",
    "buscar_todos",
    "buscar_um",
    "caminho_banco",
    "conectar",
    "criar_esquema",
    "definir_banco",
    "executar",
    "sessao",
    "traduzir",
    "transacao",
    "usando_postgres",
    "valor",
]
