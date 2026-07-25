"""Modo demonstração.

Quando a plataforma sobe em hospedagem serverless sem `DATABASE_URL`, o banco
vive em /tmp e desaparece a cada reinício. Para que o primeiro deploy já
funcione — e não devolva uma tela de login sem nenhuma conta —, criamos aqui
as duas contas de teste.

Isso só acontece em modo demonstração. Com Postgres configurado, nada é criado
automaticamente: as contas de verdade nascem da compra na Cakto ou da
liberação manual no painel.
"""

from __future__ import annotations

import os

from . import alunos as servico_alunos
from .config import config
from .db import executar, sessao, valor
from .jornada import iniciar_jornada
from .security import agora_txt

CONTAS = (
    {
        "nome": "Administrador (demonstração)",
        "email": os.getenv("DEMO_ADMIN_EMAIL", "admin@teste.com"),
        "senha": os.getenv("DEMO_ADMIN_SENHA", "admin1234"),
        "admin": True,
    },
    {
        "nome": "Aluno de Teste",
        "email": os.getenv("DEMO_ALUNO_EMAIL", "aluno@teste.com"),
        "senha": os.getenv("DEMO_ALUNO_SENHA", "aluno1234"),
        "admin": False,
    },
)


def preparar() -> bool:
    """Cria as contas de demonstração se o banco estiver vazio."""
    if not config.modo_demo:
        return False
    with sessao() as con:
        if int(valor(con, "SELECT COUNT(*) FROM alunos")) > 0:
            return False
        for conta in CONTAS:
            aluno = servico_alunos.criar(
                con,
                conta["nome"],
                conta["email"],
                origem="demo",
                admin=conta["admin"],
                senha=conta["senha"],
            )
            executar(
                con,
                "UPDATE alunos SET status='ativo', ativado_em=? WHERE id=?",
                (agora_txt(), aluno["id"]),
            )
            iniciar_jornada(con, int(aluno["id"]))
    return True
