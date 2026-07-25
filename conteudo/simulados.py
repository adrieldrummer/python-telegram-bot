"""Simulados cronometrados — montagem determinística a partir do banco de questões."""

from __future__ import annotations

import random
from dataclasses import dataclass

from .questoes import POR_MATERIA, Questao


@dataclass(frozen=True)
class Simulado:
    id: str
    nome: str
    subtitulo: str
    descricao: str
    minutos: int
    total: int
    composicao: tuple[tuple[str, int], ...]
    semente: int
    dia_liberacao: int
    capa: str


SIMULADOS: tuple[Simulado, ...] = (
    Simulado(
        id="sim-1",
        nome="Simulado 1 — Diagnóstico de execução",
        subtitulo="30 questões · 60 minutos",
        descricao=(
            "Primeiro contato com prova cronometrada. O objetivo não é a nota: é descobrir como "
            "você administra o relógio e onde a atenção cai."
        ),
        minutos=60,
        total=30,
        composicao=(
            ("portugues", 6),
            ("constitucional", 5),
            ("matematica", 4),
            ("administrativo", 4),
            ("penal", 4),
            ("legislacao", 3),
            ("atualidades", 2),
            ("informatica", 2),
        ),
        semente=1901,
        dia_liberacao=19,
        capa="simulado-1",
    ),
    Simulado(
        id="sim-2",
        nome="Simulado 2 — Ritmo de prova",
        subtitulo="40 questões · 80 minutos",
        descricao=(
            "Mais longo e mais próximo da prova real. Agora com estratégia definida: três "
            "passadas, transcrição em blocos e pausa técnica planejada."
        ),
        minutos=80,
        total=40,
        composicao=(
            ("portugues", 8),
            ("constitucional", 7),
            ("matematica", 6),
            ("administrativo", 5),
            ("penal", 5),
            ("legislacao", 4),
            ("atualidades", 3),
            ("informatica", 2),
        ),
        semente=2302,
        dia_liberacao=23,
        capa="simulado-2",
    ),
    Simulado(
        id="sim-3",
        nome="Simulado 3 — Ensaio geral",
        subtitulo="50 questões · 100 minutos",
        descricao=(
            "O ensaio geral. Reproduza as condições reais da prova: mesmo horário, mesa limpa, "
            "celular longe. É este número que você leva como referência."
        ),
        minutos=100,
        total=50,
        composicao=(
            ("portugues", 9),
            ("constitucional", 8),
            ("matematica", 8),
            ("administrativo", 6),
            ("penal", 6),
            ("legislacao", 5),
            ("atualidades", 4),
            ("informatica", 4),
        ),
        semente=2603,
        dia_liberacao=26,
        capa="simulado-3",
    ),
)

POR_ID = {s.id: s for s in SIMULADOS}


def simulado(sid: str) -> Simulado | None:
    return POR_ID.get(sid)


def montar(sid: str) -> list[Questao]:
    """Sempre devolve as mesmas questões, na mesma ordem, para o mesmo simulado."""
    s = POR_ID.get(sid)
    if s is None:
        return []
    escolhidas: list[Questao] = []
    for materia, quantidade in s.composicao:
        disponiveis = sorted(POR_MATERIA.get(materia, []), key=lambda q: q.id)
        rnd = random.Random(f"{s.semente}-{materia}")
        rnd.shuffle(disponiveis)
        escolhidas.extend(disponiveis[:quantidade])
    embaralhador = random.Random(s.semente)
    embaralhador.shuffle(escolhidas)
    return escolhidas


def simulados_ate(dia: int) -> list[Simulado]:
    return [s for s in SIMULADOS if s.dia_liberacao <= dia]
