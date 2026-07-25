"""Ciclo de vida do aluno: compra → aprovação por e-mail → ativação → acesso."""

from __future__ import annotations

import sqlite3
from typing import Optional

from . import mailer
from .db import buscar_um, executar
from .security import (
    agora_txt,
    conferir_senha,
    criar_token,
    gerar_hash_senha,
    normalizar_email,
    revogar_sessoes_do_aluno,
)

STATUS_ATIVO = "ativo"
STATUS_PENDENTE = "pendente"
STATUS_SUSPENSO = "suspenso"


def por_email(con: sqlite3.Connection, email: str) -> Optional[sqlite3.Row]:
    return buscar_um(con, "SELECT * FROM alunos WHERE email = ?", (normalizar_email(email),))


def por_id(con: sqlite3.Connection, aluno_id: int) -> Optional[sqlite3.Row]:
    return buscar_um(con, "SELECT * FROM alunos WHERE id = ?", (aluno_id,))


def criar(
    con: sqlite3.Connection,
    nome: str,
    email: str,
    telefone: str = "",
    origem: str = "cakto",
    admin: bool = False,
    senha: str = "",
) -> sqlite3.Row:
    existente = por_email(con, email)
    if existente is not None:
        return existente
    cur = executar(
        con,
        """INSERT INTO alunos (nome, email, telefone, origem, admin, senha_hash, status)
           VALUES (?,?,?,?,?,?,?)""",
        (
            (nome or "Candidato").strip()[:120],
            normalizar_email(email),
            (telefone or "").strip()[:40],
            origem,
            1 if admin else 0,
            gerar_hash_senha(senha) if senha else "",
            STATUS_ATIVO if senha else STATUS_PENDENTE,
        ),
    )
    return buscar_um(con, "SELECT * FROM alunos WHERE id = ?", (int(cur.lastrowid or 0),))


def aprovar_acesso(con: sqlite3.Connection, aluno: sqlite3.Row, reenvio: bool = False) -> str:
    """Envia (ou reenvia) o e-mail de aprovação com o link de criação de senha."""
    token = criar_token(con, int(aluno["id"]), "ativacao", horas=168)
    if aluno["status"] == STATUS_SUSPENSO:
        executar(
            con, "UPDATE alunos SET status=? WHERE id=?", (STATUS_PENDENTE, aluno["id"])
        )
        aluno = por_id(con, int(aluno["id"]))
    mailer.enviar_aprovacao(con, aluno, token)
    return token


def ativar(con: sqlite3.Connection, aluno_id: int, senha: str) -> Optional[sqlite3.Row]:
    executar(
        con,
        "UPDATE alunos SET senha_hash=?, status=?, ativado_em=COALESCE(ativado_em, ?) WHERE id=?",
        (gerar_hash_senha(senha), STATUS_ATIVO, agora_txt(), aluno_id),
    )
    aluno = por_id(con, aluno_id)
    if aluno is not None:
        mailer.enviar_boas_vindas(con, aluno)
    return aluno


def definir_senha(con: sqlite3.Connection, aluno_id: int, senha: str) -> None:
    executar(
        con,
        "UPDATE alunos SET senha_hash=?, status=? WHERE id=?",
        (gerar_hash_senha(senha), STATUS_ATIVO, aluno_id),
    )
    revogar_sessoes_do_aluno(con, aluno_id)


def suspender(con: sqlite3.Connection, aluno_id: int, motivo: str = "") -> None:
    executar(
        con,
        "UPDATE alunos SET status=?, observacoes=? WHERE id=?",
        (STATUS_SUSPENSO, motivo[:400], aluno_id),
    )
    revogar_sessoes_do_aluno(con, aluno_id)
    aluno = por_id(con, aluno_id)
    if aluno is not None:
        mailer.enviar_acesso_suspenso(con, aluno, motivo or "solicitação de reembolso")


def reativar(con: sqlite3.Connection, aluno_id: int) -> None:
    executar(con, "UPDATE alunos SET status=? WHERE id=?", (STATUS_ATIVO, aluno_id))


def autenticar(con: sqlite3.Connection, email: str, senha: str) -> tuple[Optional[sqlite3.Row], str]:
    aluno = por_email(con, email)
    if aluno is None or not aluno["senha_hash"]:
        return None, "E-mail ou senha incorretos."
    if not conferir_senha(senha, aluno["senha_hash"]):
        return None, "E-mail ou senha incorretos."
    if aluno["status"] == STATUS_SUSPENSO:
        return None, "Seu acesso está suspenso. Fale com o suporte."
    if aluno["status"] == STATUS_PENDENTE:
        return None, "Seu acesso ainda não foi ativado. Verifique o e-mail de aprovação."
    executar(con, "UPDATE alunos SET ultimo_login=? WHERE id=?", (agora_txt(), aluno["id"]))
    return aluno, ""


def registrar_compra(
    con: sqlite3.Connection,
    aluno_id: Optional[int],
    referencia: str,
    status: str,
    email: str,
    produto: str = "",
    oferta: str = "",
    valor_pago: float = 0.0,
) -> None:
    executar(
        con,
        """INSERT INTO compras (aluno_id, referencia, status, email, produto, oferta, valor)
           VALUES (?,?,?,?,?,?,?)""",
        (aluno_id, referencia[:120], status, normalizar_email(email), produto[:160], oferta[:160], valor_pago),
    )
