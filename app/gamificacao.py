"""Pontos de estudo, streak, patentes e medalhas."""

from __future__ import annotations

import sqlite3
from datetime import timedelta
from typing import Optional

from conteudo.patentes import MEDALHAS, MEDALHAS_POR_ID, patente_de, progresso_patente, proxima_patente

from .db import buscar_todos, buscar_um, executar, valor
from .security import agora, hoje_txt, ler_data

# Quanto vale cada ação. Ajustável sem tocar no resto do sistema.
PONTOS = {
    "questao": 5,
    "acerto": 5,
    "classificar_erro": 8,
    "revisao_acerto": 6,
    "aula_lida": 25,
    "diario": 15,
    "simulado": 120,
    "diagnostico": 120,
}


def creditar(
    con: sqlite3.Connection, aluno_id: int, tipo: str, pontos: int, descricao: str = ""
) -> None:
    if pontos == 0:
        return
    executar(
        con,
        "INSERT INTO eventos_pontos (aluno_id, tipo, pontos, descricao) VALUES (?,?,?,?)",
        (aluno_id, tipo, pontos, descricao),
    )
    executar(con, "UPDATE alunos SET pontos = pontos + ? WHERE id = ?", (pontos, aluno_id))


def debitar(con: sqlite3.Connection, aluno_id: int, pontos: int, descricao: str) -> bool:
    saldo = int(valor(con, "SELECT pontos FROM alunos WHERE id = ?", (aluno_id,)))
    if saldo < pontos:
        return False
    executar(
        con,
        "UPDATE alunos SET pontos = pontos - ?, pontos_gastos = pontos_gastos + ? WHERE id = ?",
        (pontos, pontos, aluno_id),
    )
    executar(
        con,
        "INSERT INTO eventos_pontos (aluno_id, tipo, pontos, descricao) VALUES (?,?,?,?)",
        (aluno_id, "gasto", -pontos, descricao),
    )
    return True


def registrar_atividade(con: sqlite3.Connection, aluno_id: int) -> int:
    """Atualiza o streak. Devolve o bônus de constância creditado hoje (0 se já houve)."""
    linha = buscar_um(
        con,
        "SELECT ultimo_dia_estudo, streak_atual, streak_recorde FROM alunos WHERE id = ?",
        (aluno_id,),
    )
    if linha is None:
        return 0
    hoje = hoje_txt()
    ultimo = (linha["ultimo_dia_estudo"] or "").strip()
    if ultimo == hoje:
        return 0

    ontem = (agora() - timedelta(days=1)).strftime("%Y-%m-%d")
    streak = int(linha["streak_atual"] or 0)
    streak = streak + 1 if ultimo == ontem else 1
    recorde = max(streak, int(linha["streak_recorde"] or 0))
    executar(
        con,
        "UPDATE alunos SET ultimo_dia_estudo = ?, streak_atual = ?, streak_recorde = ? WHERE id = ?",
        (hoje, streak, recorde, aluno_id),
    )
    bonus = min(streak, 7) * 5
    creditar(con, aluno_id, "streak", bonus, f"Constância: {streak} dia(s) seguidos")
    return bonus


def estatisticas(con: sqlite3.Connection, aluno_id: int) -> dict:
    respondidas = int(valor(con, "SELECT COUNT(*) FROM respostas WHERE aluno_id = ?", (aluno_id,)))
    acertos = int(
        valor(con, "SELECT COUNT(*) FROM respostas WHERE aluno_id = ? AND correta = 1", (aluno_id,))
    )
    simulados = int(
        valor(
            con,
            "SELECT COUNT(*) FROM simulados_sessoes WHERE aluno_id = ? AND finalizado_em IS NOT NULL",
            (aluno_id,),
        )
    )
    melhor_simulado = float(
        valor(
            con,
            """SELECT MAX(CASE WHEN total > 0 THEN acertos * 100.0 / total ELSE 0 END)
               FROM simulados_sessoes WHERE aluno_id = ? AND finalizado_em IS NOT NULL""",
            (aluno_id,),
            0,
        )
    )
    erros_abertos = int(
        valor(
            con,
            "SELECT COUNT(*) FROM caderno_erros WHERE aluno_id = ? AND status = 'aberto'",
            (aluno_id,),
        )
    )
    dominados = int(
        valor(
            con,
            "SELECT COUNT(*) FROM caderno_erros WHERE aluno_id = ? AND status = 'dominado'",
            (aluno_id,),
        )
    )
    classificados = int(
        valor(
            con,
            "SELECT COUNT(*) FROM caderno_erros WHERE aluno_id = ? AND categoria <> ''",
            (aluno_id,),
        )
    )
    dias_concluidos = int(
        valor(
            con,
            "SELECT COUNT(*) FROM progresso_dias WHERE aluno_id = ? AND status = 'concluido'",
            (aluno_id,),
        )
    )
    return {
        "respondidas": respondidas,
        "acertos": acertos,
        "acerto_pct": round(acertos * 100 / respondidas) if respondidas else 0,
        "simulados": simulados,
        "melhor_simulado": round(melhor_simulado),
        "erros_abertos": erros_abertos,
        "dominados": dominados,
        "classificados": classificados,
        "dias_concluidos": dias_concluidos,
    }


def _hora_local(texto: Optional[str]) -> Optional[int]:
    data = ler_data(texto)
    return data.hour if data else None


def verificar_medalhas(con: sqlite3.Connection, aluno_id: int) -> list[dict]:
    """Concede as medalhas conquistadas desde a última verificação."""
    ja_tem = {
        linha["medalha_id"]
        for linha in buscar_todos(
            con, "SELECT medalha_id FROM medalhas_aluno WHERE aluno_id = ?", (aluno_id,)
        )
    }
    aluno = buscar_um(con, "SELECT * FROM alunos WHERE id = ?", (aluno_id,))
    if aluno is None:
        return []
    st = estatisticas(con, aluno_id)
    streak = int(aluno["streak_atual"] or 0)

    horas = [
        _hora_local(linha["criado_em"])
        for linha in buscar_todos(
            con, "SELECT criado_em FROM respostas WHERE aluno_id = ? LIMIT 400", (aluno_id,)
        )
    ]
    fases_concluidas = {
        f"fase{n}": int(
            valor(
                con,
                "SELECT COUNT(*) FROM progresso_dias WHERE aluno_id = ? AND status='concluido' AND dia BETWEEN ? AND ?",
                (aluno_id, ini, fim),
            )
        )
        >= (fim - ini + 1)
        for n, (ini, fim) in enumerate(((1, 6), (7, 18), (19, 26), (27, 30)), start=1)
    }

    condicoes = {
        "diagnostico": bool(aluno["diagnostico_em"]),
        "primeira_missao": st["dias_concluidos"] >= 1,
        "streak3": streak >= 3,
        "streak7": streak >= 7,
        "streak15": streak >= 15,
        "streak30": streak >= 30,
        "q100": st["respondidas"] >= 100,
        "q300": st["respondidas"] >= 300,
        "q600": st["respondidas"] >= 600,
        "erro_categorizado": st["classificados"] >= 1,
        "erros_dominados10": st["dominados"] >= 10,
        "simulado1": st["simulados"] >= 1,
        "simulado3": st["simulados"] >= 3,
        "nota70": st["melhor_simulado"] >= 70,
        "madrugador": any(h is not None and h < 7 for h in horas),
        "coruja": any(h is not None and h >= 22 for h in horas),
        "fase1": fases_concluidas["fase1"],
        "fase2": fases_concluidas["fase2"],
        "fase3": fases_concluidas["fase3"],
        "fase4": fases_concluidas["fase4"],
    }

    novas: list[dict] = []
    for medalha in MEDALHAS:
        if medalha.id in ja_tem or not condicoes.get(medalha.id):
            continue
        executar(
            con,
            "INSERT OR IGNORE INTO medalhas_aluno (aluno_id, medalha_id) VALUES (?,?)",
            (aluno_id, medalha.id),
        )
        if medalha.pontos:
            creditar(con, aluno_id, "medalha", medalha.pontos, f"Medalha: {medalha.nome}")
        novas.append({"id": medalha.id, "nome": medalha.nome, "icone": medalha.icone,
                      "descricao": medalha.descricao, "pontos": medalha.pontos})
    return novas


def medalhas_do_aluno(con: sqlite3.Connection, aluno_id: int) -> list[dict]:
    conquistadas = {
        linha["medalha_id"]: linha["conquistada_em"]
        for linha in buscar_todos(
            con, "SELECT medalha_id, conquistada_em FROM medalhas_aluno WHERE aluno_id = ?", (aluno_id,)
        )
    }
    return [
        {
            "id": m.id,
            "nome": m.nome,
            "icone": m.icone,
            "descricao": m.descricao,
            "pontos": m.pontos,
            "conquistada": m.id in conquistadas,
            "em": conquistadas.get(m.id, ""),
        }
        for m in MEDALHAS
    ]


def resumo_patente(pontos: int) -> dict:
    atual = patente_de(pontos)
    prox = proxima_patente(pontos)
    return {
        "atual": atual,
        "proxima": prox,
        "progresso": progresso_patente(pontos),
        "faltam": (prox.pontos - pontos) if prox else 0,
    }


def extrato(con: sqlite3.Connection, aluno_id: int, limite: int = 40) -> list[sqlite3.Row]:
    return buscar_todos(
        con,
        "SELECT * FROM eventos_pontos WHERE aluno_id = ? ORDER BY id DESC LIMIT ?",
        (aluno_id, limite),
    )


def ranking(con: sqlite3.Connection, limite: int = 20) -> list[sqlite3.Row]:
    """Ranking anônimo por pontos (mostra apenas o primeiro nome)."""
    return buscar_todos(
        con,
        """SELECT id, nome, pontos, streak_atual FROM alunos
           WHERE status = 'ativo' AND admin = 0
           ORDER BY pontos DESC, streak_atual DESC LIMIT ?""",
        (limite,),
    )


__all__ = [
    "MEDALHAS_POR_ID",
    "PONTOS",
    "creditar",
    "debitar",
    "estatisticas",
    "extrato",
    "medalhas_do_aluno",
    "ranking",
    "registrar_atividade",
    "resumo_patente",
    "verificar_medalhas",
]
