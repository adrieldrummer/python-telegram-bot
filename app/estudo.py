"""Processamento de respostas: pontos, caderno de erros e estatísticas."""

from __future__ import annotations

import json
import sqlite3
from typing import Optional

from conteudo.questoes import Questao
from conteudo.simulados import montar, simulado as buscar_simulado

from . import srs
from .db import buscar_todos, buscar_um, executar, valor
from .gamificacao import PONTOS, creditar, registrar_atividade, verificar_medalhas
from .security import agora_txt


def responder(
    con: sqlite3.Connection,
    aluno_id: int,
    questao: Questao,
    alternativa: str,
    origem: str,
    dia: Optional[int] = None,
    tempo_seg: int = 0,
    sessao_id: Optional[int] = None,
) -> dict:
    """Registra a resposta e devolve o retorno completo para a interface."""
    correta = alternativa == questao.correta
    executar(
        con,
        """INSERT INTO respostas
           (aluno_id, questao_id, materia, alternativa, correta, tempo_seg, origem, dia, sessao_id)
           VALUES (?,?,?,?,?,?,?,?,?)""",
        (
            aluno_id,
            questao.id,
            questao.materia,
            alternativa,
            1 if correta else 0,
            max(0, min(tempo_seg, 3600)),
            origem,
            dia,
            sessao_id,
        ),
    )

    pontos = PONTOS["questao"] + (PONTOS["acerto"] if correta else 0)
    dominada = False
    if correta:
        dominada = srs.registrar_acerto(con, aluno_id, questao.id)
        if dominada:
            pontos += PONTOS["revisao_acerto"]
    else:
        srs.registrar_erro(con, aluno_id, questao.id, questao.materia)

    creditar(con, aluno_id, "questao", pontos, f"Questão {questao.id}")
    bonus_streak = registrar_atividade(con, aluno_id)
    medalhas = verificar_medalhas(con, aluno_id)

    return {
        "correta": correta,
        "gabarito": questao.correta,
        "gabarito_texto": questao.alternativa_texto(questao.correta),
        "comentario": questao.comentario,
        "armadilha": questao.armadilha,
        "pontos": pontos,
        "bonus_streak": bonus_streak,
        "dominada": dominada,
        "medalhas": medalhas,
        "no_caderno": not correta,
    }


def classificar_erro(
    con: sqlite3.Connection, aluno_id: int, questao_id: str, categoria: str, anotacao: str
) -> dict:
    ok = srs.classificar(con, aluno_id, questao_id, categoria, anotacao)
    pontos = 0
    if ok:
        pontos = PONTOS["classificar_erro"]
        creditar(con, aluno_id, "correcao", pontos, f"Correção ativa — {questao_id}")
    medalhas = verificar_medalhas(con, aluno_id)
    return {"ok": ok, "pontos": pontos, "medalhas": medalhas}


# --- simulados -------------------------------------------------------------


def iniciar_simulado(con: sqlite3.Connection, aluno_id: int, simulado_id: str) -> Optional[int]:
    if buscar_simulado(simulado_id) is None:
        return None
    aberta = buscar_um(
        con,
        """SELECT id FROM simulados_sessoes
           WHERE aluno_id=? AND simulado_id=? AND finalizado_em IS NULL
           ORDER BY id DESC LIMIT 1""",
        (aluno_id, simulado_id),
    )
    if aberta is not None:
        return int(aberta["id"])
    cur = executar(
        con,
        "INSERT INTO simulados_sessoes (aluno_id, simulado_id, total) VALUES (?,?,?)",
        (aluno_id, simulado_id, len(montar(simulado_id))),
    )
    return int(cur.lastrowid or 0)


def finalizar_simulado(
    con: sqlite3.Connection, aluno_id: int, sessao_id: int, duracao_seg: int
) -> dict:
    sessao = buscar_um(
        con, "SELECT * FROM simulados_sessoes WHERE id=? AND aluno_id=?", (sessao_id, aluno_id)
    )
    if sessao is None:
        return {}

    respostas = buscar_todos(
        con,
        "SELECT materia, correta, tempo_seg FROM respostas WHERE aluno_id=? AND sessao_id=?",
        (aluno_id, sessao_id),
    )
    total = len(respostas)
    acertos = sum(1 for r in respostas if r["correta"])
    por_materia: dict[str, dict] = {}
    for r in respostas:
        item = por_materia.setdefault(r["materia"], {"total": 0, "acertos": 0, "tempo": 0})
        item["total"] += 1
        item["acertos"] += 1 if r["correta"] else 0
        item["tempo"] += int(r["tempo_seg"] or 0)
    for item in por_materia.values():
        item["pct"] = round(item["acertos"] * 100 / item["total"]) if item["total"] else 0
        item["tempo_medio"] = round(item["tempo"] / item["total"]) if item["total"] else 0

    tempo_total = sum(int(r["tempo_seg"] or 0) for r in respostas)
    relatorio = {
        "por_materia": por_materia,
        "tempo_medio": round(tempo_total / total) if total else 0,
        "duracao_seg": duracao_seg,
    }
    executar(
        con,
        """UPDATE simulados_sessoes
           SET finalizado_em=?, duracao_seg=?, acertos=?, total=?, relatorio=?
           WHERE id=?""",
        (agora_txt(), duracao_seg, acertos, total, json.dumps(relatorio, ensure_ascii=False), sessao_id),
    )
    creditar(con, aluno_id, "simulado", PONTOS["simulado"], f"Simulado {sessao['simulado_id']}")
    medalhas = verificar_medalhas(con, aluno_id)
    return {
        "acertos": acertos,
        "total": total,
        "pct": round(acertos * 100 / total) if total else 0,
        "relatorio": relatorio,
        "medalhas": medalhas,
    }


def historico_simulados(con: sqlite3.Connection, aluno_id: int) -> list[dict]:
    linhas = buscar_todos(
        con,
        """SELECT * FROM simulados_sessoes
           WHERE aluno_id=? AND finalizado_em IS NOT NULL ORDER BY id""",
        (aluno_id,),
    )
    resultado = []
    for linha in linhas:
        try:
            relatorio = json.loads(linha["relatorio"] or "{}")
        except json.JSONDecodeError:
            relatorio = {}
        s = buscar_simulado(linha["simulado_id"])
        resultado.append(
            {
                "id": linha["id"],
                "simulado_id": linha["simulado_id"],
                "nome": s.nome if s else linha["simulado_id"],
                "acertos": linha["acertos"],
                "total": linha["total"],
                "pct": round(linha["acertos"] * 100 / linha["total"]) if linha["total"] else 0,
                "duracao_min": round((linha["duracao_seg"] or 0) / 60),
                "finalizado_em": linha["finalizado_em"],
                "relatorio": relatorio,
            }
        )
    return resultado


def respostas_da_sessao(con: sqlite3.Connection, aluno_id: int, sessao_id: int) -> dict[str, str]:
    return {
        linha["questao_id"]: linha["alternativa"]
        for linha in buscar_todos(
            con,
            "SELECT questao_id, alternativa FROM respostas WHERE aluno_id=? AND sessao_id=?",
            (aluno_id, sessao_id),
        )
    }


def respondidas_do_dia(con: sqlite3.Connection, aluno_id: int, dia: int) -> dict[str, dict]:
    linhas = buscar_todos(
        con,
        """SELECT questao_id, alternativa, correta FROM respostas
           WHERE aluno_id=? AND dia=? ORDER BY id""",
        (aluno_id, dia),
    )
    return {
        linha["questao_id"]: {"alternativa": linha["alternativa"], "correta": bool(linha["correta"])}
        for linha in linhas
    }


def evolucao_semanal(con: sqlite3.Connection, aluno_id: int) -> list[dict]:
    """Acerto por dia dos últimos 14 dias — alimenta o gráfico do painel."""
    linhas = buscar_todos(
        con,
        """SELECT substr(criado_em, 1, 10) AS data,
                  COUNT(*) AS total,
                  SUM(correta) AS acertos
           FROM respostas WHERE aluno_id=?
           GROUP BY substr(criado_em, 1, 10)
           ORDER BY data DESC LIMIT 14""",
        (aluno_id,),
    )
    dados = [
        {
            "data": linha["data"],
            "total": int(linha["total"]),
            "acertos": int(linha["acertos"] or 0),
            "pct": round(int(linha["acertos"] or 0) * 100 / int(linha["total"])) if linha["total"] else 0,
        }
        for linha in linhas
    ]
    return list(reversed(dados))


def total_respostas(con: sqlite3.Connection, aluno_id: int) -> int:
    return int(valor(con, "SELECT COUNT(*) FROM respostas WHERE aluno_id=?", (aluno_id,)))
