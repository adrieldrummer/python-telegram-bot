"""Caderno de Erros com revisão espaçada.

O e-book descreve o hábito manual: anotar o motivo do erro e revisar nos
intervalos livres. Aqui isso vira sistema — cada erro entra numa fila com
intervalos de 1, 3, 7 e 15 dias, e só sai depois de três acertos seguidos.
"""

from __future__ import annotations

import sqlite3
from datetime import timedelta

from conteudo.materias import CATEGORIAS_ERRO

from .db import buscar_todos, buscar_um, executar, valor
from .security import agora, agora_txt, hoje_txt

INTERVALOS = (1, 3, 7, 15)  # dias por nível
ACERTOS_PARA_DOMINAR = 3


def _proxima_data(nivel: int) -> str:
    dias = INTERVALOS[min(nivel, len(INTERVALOS) - 1)]
    return (agora() + timedelta(days=dias)).strftime("%Y-%m-%d")


def registrar_erro(con: sqlite3.Connection, aluno_id: int, questao_id: str, materia: str) -> None:
    """Coloca (ou devolve) a questão no caderno, reiniciando o ciclo."""
    existente = buscar_um(
        con,
        "SELECT id, status FROM caderno_erros WHERE aluno_id = ? AND questao_id = ?",
        (aluno_id, questao_id),
    )
    if existente is None:
        executar(
            con,
            """INSERT INTO caderno_erros (aluno_id, questao_id, materia, nivel_srs, proxima_revisao)
               VALUES (?,?,?,0,?)""",
            (aluno_id, questao_id, materia, _proxima_data(0)),
        )
        return
    executar(
        con,
        """UPDATE caderno_erros
           SET status='aberto', nivel_srs=0, acertos_seguidos=0,
               proxima_revisao=?, atualizado_em=?
           WHERE id=?""",
        (_proxima_data(0), agora_txt(), existente["id"]),
    )


def registrar_acerto(con: sqlite3.Connection, aluno_id: int, questao_id: str) -> bool:
    """Acerto numa questão do caderno. Devolve True se ela foi dominada agora."""
    linha = buscar_um(
        con,
        "SELECT * FROM caderno_erros WHERE aluno_id = ? AND questao_id = ? AND status='aberto'",
        (aluno_id, questao_id),
    )
    if linha is None:
        return False
    acertos = int(linha["acertos_seguidos"]) + 1
    nivel = min(int(linha["nivel_srs"]) + 1, len(INTERVALOS) - 1)
    if acertos >= ACERTOS_PARA_DOMINAR:
        executar(
            con,
            """UPDATE caderno_erros
               SET status='dominado', acertos_seguidos=?, nivel_srs=?, proxima_revisao=NULL,
                   atualizado_em=?
               WHERE id=?""",
            (acertos, nivel, agora_txt(), linha["id"]),
        )
        return True
    executar(
        con,
        """UPDATE caderno_erros
           SET acertos_seguidos=?, nivel_srs=?, proxima_revisao=?, atualizado_em=?
           WHERE id=?""",
        (acertos, nivel, _proxima_data(nivel), agora_txt(), linha["id"]),
    )
    return False


def classificar(
    con: sqlite3.Connection, aluno_id: int, questao_id: str, categoria: str, anotacao: str = ""
) -> bool:
    if categoria not in CATEGORIAS_ERRO:
        return False
    cur = executar(
        con,
        """UPDATE caderno_erros SET categoria=?, anotacao=?, atualizado_em=?
           WHERE aluno_id=? AND questao_id=?""",
        (categoria, anotacao[:600], agora_txt(), aluno_id, questao_id),
    )
    return cur.rowcount > 0


def vencidas(con: sqlite3.Connection, aluno_id: int, limite: int = 20) -> list[sqlite3.Row]:
    """Questões cujo prazo de revisão chegou (as mais antigas primeiro)."""
    return buscar_todos(
        con,
        """SELECT * FROM caderno_erros
           WHERE aluno_id = ? AND status='aberto'
             AND (proxima_revisao IS NULL OR proxima_revisao <= ?)
           ORDER BY proxima_revisao IS NULL DESC, proxima_revisao, id
           LIMIT ?""",
        (aluno_id, hoje_txt(), limite),
    )


def total_vencidas(con: sqlite3.Connection, aluno_id: int) -> int:
    """Quantas revisões estão atrasadas. COUNT em vez de contar linhas trazidas."""
    return int(
        valor(
            con,
            """SELECT COUNT(*) FROM caderno_erros
               WHERE aluno_id = ? AND status='aberto'
                 AND (proxima_revisao IS NULL OR proxima_revisao <= ?)""",
            (aluno_id, hoje_txt()),
        )
    )


def abertas(con: sqlite3.Connection, aluno_id: int, materia: str = "") -> list[sqlite3.Row]:
    if materia:
        return buscar_todos(
            con,
            """SELECT * FROM caderno_erros WHERE aluno_id=? AND status='aberto' AND materia=?
               ORDER BY proxima_revisao, id""",
            (aluno_id, materia),
        )
    return buscar_todos(
        con,
        "SELECT * FROM caderno_erros WHERE aluno_id=? AND status='aberto' ORDER BY proxima_revisao, id",
        (aluno_id,),
    )


def resumo(con: sqlite3.Connection, aluno_id: int) -> dict:
    total_aberto = int(
        valor(con, "SELECT COUNT(*) FROM caderno_erros WHERE aluno_id=? AND status='aberto'", (aluno_id,))
    )
    dominados = int(
        valor(con, "SELECT COUNT(*) FROM caderno_erros WHERE aluno_id=? AND status='dominado'", (aluno_id,))
    )
    pendentes = total_vencidas(con, aluno_id)
    por_categoria = {
        chave: int(
            valor(
                con,
                "SELECT COUNT(*) FROM caderno_erros WHERE aluno_id=? AND categoria=?",
                (aluno_id, chave),
            )
        )
        for chave in CATEGORIAS_ERRO
    }
    sem_categoria = int(
        valor(
            con,
            "SELECT COUNT(*) FROM caderno_erros WHERE aluno_id=? AND status='aberto' AND categoria=''",
            (aluno_id,),
        )
    )
    dominante = ""
    if any(por_categoria.values()):
        dominante = max(por_categoria, key=lambda k: por_categoria[k])
    return {
        "abertos": total_aberto,
        "dominados": dominados,
        "pendentes": pendentes,
        "por_categoria": por_categoria,
        "sem_categoria": sem_categoria,
        "categoria_dominante": dominante,
        "categorias": CATEGORIAS_ERRO,
    }


__all__ = [
    "ACERTOS_PARA_DOMINAR",
    "CATEGORIAS_ERRO",
    "INTERVALOS",
    "abertas",
    "classificar",
    "registrar_acerto",
    "registrar_erro",
    "resumo",
    "total_vencidas",
    "vencidas",
]
