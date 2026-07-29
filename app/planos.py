"""Planos, assinaturas e liberação de recursos.

Regra central: o acesso a uma área da plataforma depende de o plano do aluno
conter o **recurso**, e de o plano não estar vencido. Toda a política vive
aqui — as telas só perguntam `tem_recurso(...)`.
"""

from __future__ import annotations

import sqlite3
from datetime import timedelta
from typing import Optional

from conteudo import planos as catalogo

from .db import buscar_todos, buscar_um, executar, valor as _valor_sql
from .security import agora, agora_txt, hoje_txt, ler_data


def plano_do_aluno(aluno) -> catalogo.Plano:
    return catalogo.plano(_valor(aluno, "plano"))


def _valor(aluno, campo: str, padrao=None):
    try:
        return aluno[campo]
    except (KeyError, IndexError, TypeError):
        return padrao


def vencido(aluno) -> bool:
    limite = _valor(aluno, "plano_ate")
    if not limite:
        return False
    data = ler_data(limite)
    return bool(data and data.date() < agora().date())


def tem_recurso(aluno, recurso: str) -> bool:
    if _valor(aluno, "admin"):
        return True
    if vencido(aluno):
        return False
    return catalogo.tem_recurso(_valor(aluno, "plano") or "", recurso)


def resumo(aluno) -> dict:
    p = plano_do_aluno(aluno)
    limite = _valor(aluno, "plano_ate")
    dias = None
    if limite:
        data = ler_data(limite)
        if data:
            dias = (data.date() - agora().date()).days
    return {
        "plano": p,
        "expira_em": limite,
        "dias_restantes": dias,
        "vencido": vencido(aluno),
        "recursos": {r: catalogo.RECURSOS[r] for r in p.recursos if r in catalogo.RECURSOS},
        "bloqueados": {
            r: nome for r, nome in catalogo.RECURSOS.items() if r not in p.recursos
        },
    }


def aplicar(
    con: sqlite3.Connection,
    aluno_id: int,
    plano_id: str,
    referencia: str = "",
    provedor: str = "cakto",
) -> catalogo.Plano:
    """Coloca o aluno no plano e registra/renova a assinatura correspondente."""
    p = catalogo.plano(plano_id)
    ate = None
    if p.duracao_dias:
        ate = (agora() + timedelta(days=p.duracao_dias)).strftime("%Y-%m-%d")
    executar(
        con,
        "UPDATE alunos SET plano = ?, plano_ate = ? WHERE id = ?",
        (p.id, ate, aluno_id),
    )

    aberta = buscar_um(
        con,
        """SELECT id FROM assinaturas
           WHERE aluno_id = ? AND plano = ? AND status = 'ativa'
           ORDER BY id DESC LIMIT 1""",
        (aluno_id, p.id),
    )
    if aberta is not None:
        executar(
            con,
            "UPDATE assinaturas SET renova_em = ?, atualizado_em = ? WHERE id = ?",
            (ate, agora_txt(), aberta["id"]),
        )
    else:
        executar(
            con,
            """INSERT INTO assinaturas (aluno_id, provedor, referencia, plano, ciclo, status, renova_em)
               VALUES (?,?,?,?,?,'ativa',?)""",
            (aluno_id, provedor, referencia[:120], p.id, p.ciclo, ate),
        )
    return p


def cancelar(con: sqlite3.Connection, aluno_id: int, motivo: str = "") -> None:
    """Cancela a assinatura mas mantém o acesso até o fim do período pago."""
    executar(
        con,
        """UPDATE assinaturas SET status='cancelada', cancelada_em=?, atualizado_em=?
           WHERE aluno_id=? AND status='ativa'""",
        (agora_txt(), agora_txt(), aluno_id),
    )
    if motivo:
        executar(
            con, "UPDATE alunos SET observacoes=? WHERE id=?", (motivo[:400], aluno_id)
        )


def encerrar_agora(con: sqlite3.Connection, aluno_id: int) -> None:
    """Encerra o acesso na hora (reembolso, chargeback).

    A data fica no passado de propósito: marcar "hoje" deixaria o aluno com
    acesso até a virada do dia, e reembolso não tem prazo de cortesia.
    """
    ontem = (agora() - timedelta(days=1)).strftime("%Y-%m-%d")
    executar(
        con,
        "UPDATE alunos SET plano_ate = ? WHERE id = ?",
        (ontem, aluno_id),
    )
    executar(
        con,
        """UPDATE assinaturas SET status='expirada', atualizado_em=?
           WHERE aluno_id=? AND status IN ('ativa','cancelada')""",
        (agora_txt(), aluno_id),
    )


def questoes_hoje(con: sqlite3.Connection, aluno_id: int) -> int:
    return int(
        _valor_sql(
            con,
            "SELECT COUNT(*) FROM respostas WHERE aluno_id=? AND substr(criado_em,1,10)=?",
            (aluno_id, hoje_txt()),
        )
    )


def limite_do_dia(aluno) -> int:
    """Teto diário de questões do plano. 0 = sem limite."""
    if _valor(aluno, "admin"):
        return 0
    return catalogo.limite_diario(_valor(aluno, "plano") or "")


def saldo_de_questoes(con: sqlite3.Connection, aluno) -> dict:
    """Quantas questões o aluno ainda pode responder hoje."""
    limite = limite_do_dia(aluno)
    feitas = questoes_hoje(con, int(_valor(aluno, "id", 0)))
    if limite <= 0:
        return {"limitado": False, "limite": 0, "feitas": feitas, "restantes": None, "esgotado": False}
    restantes = max(0, limite - feitas)
    return {
        "limitado": True,
        "limite": limite,
        "feitas": feitas,
        "restantes": restantes,
        "esgotado": restantes <= 0,
    }


def assinaturas_do_aluno(con: sqlite3.Connection, aluno_id: int) -> list:
    return buscar_todos(
        con, "SELECT * FROM assinaturas WHERE aluno_id=? ORDER BY id DESC", (aluno_id,)
    )


def vencendo(con: sqlite3.Connection, dias: int = 5) -> list:
    """Alunos cujo acesso vence nos próximos dias — matéria-prima de renovação."""
    limite = (agora() + timedelta(days=dias)).strftime("%Y-%m-%d")
    return buscar_todos(
        con,
        """SELECT * FROM alunos
           WHERE status='ativo' AND admin=0 AND plano_ate IS NOT NULL
             AND plano_ate <= ? AND plano_ate >= ?
           ORDER BY plano_ate""",
        (limite, hoje_txt()),
    )


def distribuicao(con: sqlite3.Connection) -> list[dict]:
    """Quantos alunos em cada plano — usado no painel do admin."""
    linhas = buscar_todos(
        con,
        """SELECT plano, COUNT(*) AS total FROM alunos
           WHERE admin = 0 GROUP BY plano ORDER BY total DESC""",
    )
    return [
        {
            "plano": catalogo.plano(linha["plano"]),
            "total": int(linha["total"]),
        }
        for linha in linhas
    ]


def checkout_do_plano(plano_id: str, padrao: str = "") -> str:
    """Onde o botão de compra desse plano leva.

    Ordem: link fixo no catálogo → variável de ambiente do plano → checkout geral.
    """
    from .config import config

    p = catalogo.plano(plano_id)
    return p.checkout_url or config.checkout_do_plano(p.id) or padrao


def checkouts() -> dict[str, str]:
    """Mapa {plano_id: link} para as telas montarem os botões."""
    return {p.id: checkout_do_plano(p.id) for p in catalogo.PLANOS}


__all__ = [
    "aplicar",
    "assinaturas_do_aluno",
    "cancelar",
    "checkout_do_plano",
    "checkouts",
    "distribuicao",
    "limite_do_dia",
    "questoes_hoje",
    "saldo_de_questoes",
    "encerrar_agora",
    "plano_do_aluno",
    "resumo",
    "tem_recurso",
    "vencendo",
    "vencido",
]
