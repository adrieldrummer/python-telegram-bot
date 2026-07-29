"""Trilha do aluno: prioridades, desbloqueio, missões e conclusão de dia."""

from __future__ import annotations

import sqlite3
from datetime import timedelta
from typing import Optional

from conteudo import simulados as conteudo_simulados
from conteudo import trilha
from conteudo.materias import IDS as MATERIAS_IDS
from conteudo.materias import POR_ID as MATERIAS_POR_ID
from conteudo.questoes import Questao, selecionar
from conteudo.questoes import questao as buscar_questao

from .config import config
from .db import buscar_todos, buscar_um, executar, valor
from .gamificacao import creditar, debitar
from .security import agora, agora_txt, hoje_txt, ler_data
from .srs import vencidas

TOTAL_DIAS = trilha.TOTAL_DIAS


# --- prioridades -----------------------------------------------------------


def desempenho_por_materia(con: sqlite3.Connection, aluno_id: int) -> dict[str, dict]:
    dados: dict[str, dict] = {}
    for materia_id in MATERIAS_IDS:
        total = int(
            valor(
                con,
                "SELECT COUNT(*) FROM respostas WHERE aluno_id=? AND materia=?",
                (aluno_id, materia_id),
            )
        )
        acertos = int(
            valor(
                con,
                "SELECT COUNT(*) FROM respostas WHERE aluno_id=? AND materia=? AND correta=1",
                (aluno_id, materia_id),
            )
        )
        materia = MATERIAS_POR_ID[materia_id]
        acerto_pct = round(acertos * 100 / total) if total else 0
        # quanto maior o peso e menor o acerto, maior a urgência
        urgencia = materia.peso * (100 - acerto_pct) if total else materia.peso * 60
        dados[materia_id] = {
            "materia": materia,
            "total": total,
            "acertos": acertos,
            "acerto_pct": acerto_pct,
            "urgencia": round(urgencia),
        }
    return dados


def prioridades(con: sqlite3.Connection, aluno_id: int, quantidade: int = 3) -> list[str]:
    dados = desempenho_por_materia(con, aluno_id)
    ordenadas = sorted(dados.items(), key=lambda item: item[1]["urgencia"], reverse=True)
    return [materia_id for materia_id, _ in ordenadas[:quantidade]]


def mapa_prioridades(con: sqlite3.Connection, aluno_id: int) -> list[dict]:
    dados = desempenho_por_materia(con, aluno_id)
    ordenadas = sorted(dados.values(), key=lambda d: d["urgencia"], reverse=True)
    for posicao, item in enumerate(ordenadas, start=1):
        item["posicao"] = posicao
        item["prioritaria"] = posicao <= 3
    return ordenadas


# --- estado dos dias -------------------------------------------------------


def _linha_dia(con: sqlite3.Connection, aluno_id: int, dia: int) -> Optional[sqlite3.Row]:
    return buscar_um(
        con, "SELECT * FROM progresso_dias WHERE aluno_id=? AND dia=?", (aluno_id, dia)
    )


def iniciar_jornada(con: sqlite3.Connection, aluno_id: int) -> None:
    """Libera o dia 1 e marca a data de início (idempotente)."""
    aluno = buscar_um(con, "SELECT inicio_jornada FROM alunos WHERE id=?", (aluno_id,))
    if aluno and not aluno["inicio_jornada"]:
        executar(con, "UPDATE alunos SET inicio_jornada=? WHERE id=?", (hoje_txt(), aluno_id))
    if _linha_dia(con, aluno_id, 1) is None:
        executar(
            con,
            "INSERT OR IGNORE INTO progresso_dias (aluno_id, dia, status) VALUES (?,1,'liberado')",
            (aluno_id,),
        )


def _dias_desde_inicio(aluno: sqlite3.Row) -> int:
    inicio = ler_data(aluno["inicio_jornada"]) if aluno["inicio_jornada"] else None
    if inicio is None:
        return 0
    return max(0, (agora().date() - inicio.date()).days)


def liberar_proximo(con: sqlite3.Connection, aluno_id: int, dia_concluido: int, antecipado: bool = False) -> Optional[int]:
    proximo = dia_concluido + 1
    if proximo > TOTAL_DIAS:
        return None
    if _linha_dia(con, aluno_id, proximo) is None:
        executar(
            con,
            "INSERT INTO progresso_dias (aluno_id, dia, status, antecipado) VALUES (?,?,'liberado',?)",
            (aluno_id, proximo, 1 if antecipado else 0),
        )
    return proximo


def estado(con: sqlite3.Connection, aluno_id: int) -> list[dict]:
    """Estado de todos os dias da trilha, já com a regra de desbloqueio aplicada."""
    aluno = buscar_um(con, "SELECT * FROM alunos WHERE id=?", (aluno_id,))
    registros = {
        linha["dia"]: linha
        for linha in buscar_todos(con, "SELECT * FROM progresso_dias WHERE aluno_id=?", (aluno_id,))
    }
    decorridos = _dias_desde_inicio(aluno) if aluno else 0

    lista: list[dict] = []
    anterior_concluido = True
    for d in trilha.DIAS:
        registro = registros.get(d.numero)
        concluido = bool(registro and registro["status"] == "concluido")
        liberado_por_registro = registro is not None
        # regra 1: sequencial — o dia anterior precisa estar concluído
        # regra 2: ritmo — com drip diário, 1 dia de calendário por dia da trilha
        dentro_do_ritmo = (not config.jornada_drip_diario) or (d.numero <= decorridos + 1)
        antecipado = bool(registro and registro["antecipado"])
        liberado = concluido or liberado_por_registro or (anterior_concluido and dentro_do_ritmo)

        motivo = ""
        if not liberado:
            if not anterior_concluido:
                motivo = f"Conclua o Dia {d.numero - 1} para liberar"
            else:
                motivo = "Liberação amanhã — ou use uma Chave de Antecipação"

        lista.append(
            {
                "dia": d,
                "numero": d.numero,
                "fase": trilha.FASES_POR_ID[d.fase],
                "concluido": concluido,
                "liberado": liberado,
                "antecipado": antecipado,
                "motivo": motivo,
                "pode_antecipar": (not liberado) and anterior_concluido,
                "acerto_pct": int(registro["acerto_pct"]) if registro else 0,
                "aula_lida": bool(registro and registro["aula_lida_em"]),
                "questoes_feitas": int(registro["questoes_feitas"]) if registro else 0,
                "concluido_em": registro["concluido_em"] if registro else None,
            }
        )
        anterior_concluido = concluido
    return lista


def dia_atual(con: sqlite3.Connection, aluno_id: int) -> dict:
    """Primeiro dia liberado e não concluído — o 'continue de onde parou'."""
    lista = estado(con, aluno_id)
    for item in lista:
        if item["liberado"] and not item["concluido"]:
            return item
    return lista[-1]


def acesso_ao_dia(con: sqlite3.Connection, aluno_id: int, numero: int) -> Optional[dict]:
    for item in estado(con, aluno_id):
        if item["numero"] == numero:
            return item if item["liberado"] else None
    return None


def antecipar(con: sqlite3.Connection, aluno_id: int, numero: int) -> tuple[bool, str]:
    """Gasta pontos para liberar o próximo dia antes do prazo do drip."""
    for item in estado(con, aluno_id):
        if item["numero"] != numero:
            continue
        if item["liberado"]:
            return False, "Esse dia já está liberado."
        if not item["pode_antecipar"]:
            return False, f"Conclua o Dia {numero - 1} primeiro."
        custo = config.custo_chave_antecipacao
        if not debitar(con, aluno_id, custo, f"Chave de Antecipação — Dia {numero}"):
            return False, f"Você precisa de {custo} pontos para antecipar."
        executar(
            con,
            "INSERT OR IGNORE INTO progresso_dias (aluno_id, dia, status, antecipado) VALUES (?,?,'liberado',1)",
            (aluno_id, numero),
        )
        return True, f"Dia {numero} liberado com a Chave de Antecipação."
    return False, "Dia inválido."


# --- missões ---------------------------------------------------------------


def questoes_da_missao(con: sqlite3.Connection, aluno_id: int, numero: int) -> list[Questao]:
    """Monta o bloco do dia — estável para o mesmo aluno e o mesmo dia."""
    d = trilha.dia(numero)
    if d is None:
        return []
    missao = d.missao
    semente = aluno_id * 1000 + numero

    if missao.tipo == "diagnostico":
        # com simulado associado, o diagnóstico segue a proporção real da prova —
        # medir com peso errado gera prioridade errada para os 6 dias seguintes
        if missao.simulado_id:
            return conteudo_simulados.montar(missao.simulado_id)
        return selecionar(list(MATERIAS_IDS), quantidade=missao.quantidade, semente=semente)

    if missao.tipo == "simulado":
        return conteudo_simulados.montar(missao.simulado_id)

    if missao.tipo == "revisao":
        pendentes = vencidas(con, aluno_id, limite=missao.quantidade)
        questoes = [
            q for q in (buscar_questao(linha["questao_id"]) for linha in pendentes) if q is not None
        ]
        if len(questoes) < missao.quantidade:
            # sem erros suficientes na fila, completa com questões novas das prioridades
            faltam = missao.quantidade - len(questoes)
            ja = {q.id for q in questoes}
            questoes.extend(
                selecionar(
                    prioridades(con, aluno_id),
                    quantidade=faltam,
                    excluir=ja,
                    semente=semente,
                )
            )
        return questoes

    materias = list(missao.materias)
    if missao.usar_prioridades or not materias:
        materias = prioridades(con, aluno_id) if missao.usar_prioridades else list(MATERIAS_IDS)
    return selecionar(materias, quantidade=missao.quantidade or 10, semente=semente)


def marcar_aula_lida(con: sqlite3.Connection, aluno_id: int, numero: int) -> bool:
    registro = _linha_dia(con, aluno_id, numero)
    if registro is None:
        executar(
            con,
            "INSERT INTO progresso_dias (aluno_id, dia, status, aula_lida_em) VALUES (?,?,'liberado',?)",
            (aluno_id, numero, agora_txt()),
        )
        creditar(con, aluno_id, "aula", 25, f"Aula do Dia {numero}")
        return True
    if registro["aula_lida_em"]:
        return False
    executar(
        con,
        "UPDATE progresso_dias SET aula_lida_em=? WHERE aluno_id=? AND dia=?",
        (agora_txt(), aluno_id, numero),
    )
    creditar(con, aluno_id, "aula", 25, f"Aula do Dia {numero}")
    return True


def concluir_dia(
    con: sqlite3.Connection, aluno_id: int, numero: int, acertos: int, total: int
) -> dict:
    """Fecha o dia se a missão bateu a meta de acerto. Devolve o que aconteceu."""
    d = trilha.dia(numero)
    if d is None:
        return {"concluido": False, "motivo": "Dia inválido."}

    acerto_pct = round(acertos * 100 / total) if total else 0
    registro = _linha_dia(con, aluno_id, numero)
    if registro is None:
        executar(
            con,
            "INSERT INTO progresso_dias (aluno_id, dia, status) VALUES (?,?,'liberado')",
            (aluno_id, numero),
        )
        registro = _linha_dia(con, aluno_id, numero)

    executar(
        con,
        """UPDATE progresso_dias
           SET missao_em=?, acerto_pct=?, questoes_feitas=questoes_feitas+?
           WHERE aluno_id=? AND dia=?""",
        (agora_txt(), acerto_pct, total, aluno_id, numero),
    )

    # o diagnóstico e a revisão fecham por participação; os demais, por desempenho
    exige_meta = d.missao.tipo in {"questoes", "simulado"}
    meta = config.meta_acerto_missao
    if exige_meta and acerto_pct < meta:
        return {
            "concluido": False,
            "acerto_pct": acerto_pct,
            "meta": meta,
            "motivo": (
                f"Você fez {acerto_pct}% e a meta do dia é {meta}%. O bloco continua liberado: "
                "revise os erros no Caderno e refaça para concluir o dia."
            ),
        }

    ja_concluido = registro is not None and registro["status"] == "concluido"
    if not ja_concluido:
        executar(
            con,
            "UPDATE progresso_dias SET status='concluido', concluido_em=? WHERE aluno_id=? AND dia=?",
            (agora_txt(), aluno_id, numero),
        )
        creditar(con, aluno_id, "dia", d.pontos_base, f"Dia {numero} concluído — {d.titulo}")
        if d.missao.tipo == "diagnostico":
            executar(con, "UPDATE alunos SET diagnostico_em=? WHERE id=?", (agora_txt(), aluno_id))

    proximo = liberar_proximo(con, aluno_id, numero)
    if numero == TOTAL_DIAS:
        executar(
            con,
            "UPDATE alunos SET concluido_em=COALESCE(concluido_em, ?) WHERE id=?",
            (agora_txt(), aluno_id),
        )

    return {
        "concluido": True,
        "ja_estava": ja_concluido,
        "acerto_pct": acerto_pct,
        "pontos": d.pontos_base,
        "proximo": proximo,
        "titulo_proximo": trilha.dia(proximo).titulo if proximo else "",
        "final": numero == TOTAL_DIAS,
    }


def salvar_diario(con: sqlite3.Connection, aluno_id: int, numero: int, texto: str) -> bool:
    if not texto.strip():
        return False
    ja_existe = buscar_um(
        con, "SELECT id FROM diario WHERE aluno_id=? AND dia=?", (aluno_id, numero)
    )
    executar(
        con,
        """INSERT INTO diario (aluno_id, dia, texto) VALUES (?,?,?)
           ON CONFLICT(aluno_id, dia) DO UPDATE SET texto=excluded.texto""",
        (aluno_id, numero, texto.strip()[:4000]),
    )
    if ja_existe is None:
        creditar(con, aluno_id, "diario", 15, f"Diário de bordo — Dia {numero}")
    return True


def ler_diario(con: sqlite3.Connection, aluno_id: int, numero: int) -> str:
    linha = buscar_um(
        con, "SELECT texto FROM diario WHERE aluno_id=? AND dia=?", (aluno_id, numero)
    )
    return linha["texto"] if linha else ""


def previsao_conclusao(con: sqlite3.Connection, aluno_id: int) -> Optional[str]:
    aluno = buscar_um(con, "SELECT inicio_jornada FROM alunos WHERE id=?", (aluno_id,))
    inicio = ler_data(aluno["inicio_jornada"]) if aluno and aluno["inicio_jornada"] else None
    if inicio is None:
        return None
    return (inicio + timedelta(days=TOTAL_DIAS - 1)).strftime("%d/%m/%Y")


def resumo_jornada(con: sqlite3.Connection, aluno_id: int) -> dict:
    lista = estado(con, aluno_id)
    concluidos = sum(1 for item in lista if item["concluido"])
    atual = dia_atual(con, aluno_id)
    fases = []
    for fase in trilha.FASES:
        dias_fase = [i for i in lista if i["dia"].fase == fase.id]
        feitos = sum(1 for i in dias_fase if i["concluido"])
        fases.append(
            {
                "fase": fase,
                "total": len(dias_fase),
                "concluidos": feitos,
                "pct": round(feitos * 100 / len(dias_fase)) if dias_fase else 0,
                "liberada": any(i["liberado"] for i in dias_fase),
            }
        )
    return {
        "dias": lista,
        "concluidos": concluidos,
        "total": TOTAL_DIAS,
        "pct": round(concluidos * 100 / TOTAL_DIAS),
        "atual": atual,
        "fases": fases,
        "previsao": previsao_conclusao(con, aluno_id),
    }
