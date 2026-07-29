"""Simulados no formato real da prova — montagem determinística.

A prova objetiva da VUNESP tem 60 questões distribuídas assim: Língua
Portuguesa 20, Matemática 15, Conhecimentos Gerais 15 (História e Geografia/
Atualidades), Informática 5 e Administração Pública 5. Os simulados completos
reproduzem exatamente essa distribuição — treinar em outro formato é treinar
outra prova.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

from .edital import NOTA_MINIMA, PROVA_OBJETIVA
from .questoes import POR_MATERIA, Questao

# a composição oficial, direto do edital
COMPOSICAO_OFICIAL = tuple((materia, quantidade) for materia, _, quantidade in PROVA_OBJETIVA)


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
    recurso: str = "simulados"   # recurso de plano exigido
    oficial: bool = False        # segue a distribuição da prova real


SIMULADOS: tuple[Simulado, ...] = (
    Simulado(
        id="sim-diagnostico",
        nome="Simulado Diagnóstico",
        subtitulo="20 questões · 30 minutos",
        descricao=(
            "Bloco curto para você descobrir, logo no começo, onde estão seus pontos fracos — "
            "com a mesma proporção de matérias da prova real."
        ),
        minutos=30,
        total=20,
        # mesma proporção da prova real, reduzida a 20 questões
        composicao=(
            ("portugues", 7),
            ("matematica", 5),
            ("historia", 2),
            ("geografia", 3),
            ("informatica", 2),
            ("administracao", 1),
        ),
        semente=101,
        dia_liberacao=1,
        capa="simulados",
        recurso="questoes",   # incluído no plano de entrada
    ),
    Simulado(
        id="sim-1",
        nome="Simulado Oficial 1",
        subtitulo="60 questões · 3 horas",
        descricao=(
            "Prova completa no formato VUNESP, conferido contra a prova de 30/11/2025: "
            "20 de Português, 15 de Matemática, 15 de Conhecimentos Gerais (6 de História e "
            "9 de Geografia e Atualidades), 5 de Informática e 5 de Administração Pública."
        ),
        minutos=180,
        total=60,
        composicao=COMPOSICAO_OFICIAL,
        semente=2026,
        dia_liberacao=4,
        capa="simulados",
        oficial=True,
    ),
    Simulado(
        id="sim-2",
        nome="Simulado Oficial 2",
        subtitulo="60 questões · 3 horas",
        descricao=(
            "Segunda prova completa, com outro sorteio de questões. Use para medir evolução e "
            "treinar gestão de tempo com a prova inteira."
        ),
        minutos=180,
        total=60,
        composicao=COMPOSICAO_OFICIAL,
        semente=920,
        dia_liberacao=7,
        capa="simulados",
        oficial=True,
    ),
)

POR_ID = {s.id: s for s in SIMULADOS}
NOTA_DE_CORTE = NOTA_MINIMA


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


def aprovado(acertos: int, total: int) -> bool:
    """Na prova real, a nota de corte é 30 pontos em 60. Aqui, a proporção equivalente."""
    if total <= 0:
        return False
    return (acertos / total) >= (NOTA_DE_CORTE / 60)
