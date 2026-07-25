"""Configuração comum dos testes: banco temporário e cliente HTTP."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from app import alunos as servico_alunos  # noqa: E402
from app import db  # noqa: E402
from app.jornada import iniciar_jornada  # noqa: E402


TABELAS = (
    "alunos, tokens, sessoes, compras, webhooks, progresso_dias, respostas, "
    "caderno_erros, simulados_sessoes, eventos_pontos, medalhas_aluno, diario, "
    "emails, tentativas_login"
)


@pytest.fixture()
def banco(tmp_path):
    """Banco limpo por teste.

    Roda tanto em SQLite (padrão) quanto em Postgres — basta exportar
    DATABASE_URL antes de chamar o pytest para exercitar o mesmo conjunto de
    testes no banco que vai para produção.
    """
    if db.usando_postgres():
        db.criar_esquema()
        with db.sessao() as conexao:
            conexao.execute(f"TRUNCATE {TABELAS} RESTART IDENTITY CASCADE")
        yield
        return

    db.definir_banco(tmp_path / "teste.db")
    db.criar_esquema()
    yield
    db.definir_banco(RAIZ / "dados" / "plataforma.db")


@pytest.fixture()
def con(banco):
    with db.sessao() as conexao:
        yield conexao


@pytest.fixture()
def aluno(con):
    registro = servico_alunos.criar(
        con, "Maria Teste", "maria@teste.com", origem="teste", senha="segura12345"
    )
    iniciar_jornada(con, int(registro["id"]))
    return servico_alunos.por_email(con, "maria@teste.com")


@pytest.fixture()
def cliente(banco):
    from fastapi.testclient import TestClient

    from app.main import app

    with TestClient(app) as c:
        yield c


def entrar(cliente, email: str, senha: str):
    cliente.get("/entrar")
    csrf = cliente.cookies.get("map_csrf")
    return cliente.post(
        "/entrar",
        data={"email": email, "senha": senha, "csrf_token": csrf, "proximo": "/painel"},
        follow_redirects=True,
    )
