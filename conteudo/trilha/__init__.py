"""Trilha de 30 dias — a versão de plataforma do 'Mapa da Aprovação'.

O e-book original dividia 60 dias em quatro fases. Aqui o método foi
recomprimido para 30 dias sem perder nenhuma das quatro etapas: o que muda é
a densidade diária e o fato de a plataforma fazer por você o trabalho que o
autor fazia na mão — diagnóstico, priorização, caderno de erros e revisão.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class Fase:
    id: str
    numero: int
    nome: str
    subtitulo: str
    dia_inicial: int
    dia_final: int
    cor: str
    objetivo: str
    medalha: str


@dataclass(frozen=True)
class Missao:
    """O que precisa ser feito para o dia contar como concluído."""

    tipo: str  # diagnostico | questoes | revisao | simulado | planejamento
    titulo: str
    quantidade: int = 0
    materias: tuple[str, ...] = ()
    usar_prioridades: bool = False
    simulado_id: str = ""
    descricao: str = ""


@dataclass(frozen=True)
class Dia:
    numero: int
    fase: str
    titulo: str
    promessa: str
    tempo_min: int
    aula: tuple[str, ...]
    chave: str
    tarefas: tuple[str, ...]
    missao: Missao
    frase: str
    pontos_base: int = 60
    diario: str = ""  # pergunta do diário de bordo


FASES: tuple[Fase, ...] = (
    Fase(
        id="fase1",
        numero=1,
        nome="Diagnóstico e Prioridade",
        subtitulo="Dias 1 a 6",
        dia_inicial=1,
        dia_final=6,
        cor="#2f6fed",
        objetivo=(
            "Descobrir, com dados e não com achismo, onde você está forte e onde está perdendo "
            "pontos — e transformar isso em uma ordem de prioridade."
        ),
        medalha="fase1",
    ),
    Fase(
        id="fase2",
        numero=2,
        nome="Imersão em Questões",
        subtitulo="Dias 7 a 18",
        dia_inicial=7,
        dia_final=18,
        cor="#e0663c",
        objetivo=(
            "Estudar através das questões, com correção ativa de cada erro e revisão espaçada do "
            "que você já errou. É a fase que mais transforma candidato."
        ),
        medalha="fase2",
    ),
    Fase(
        id="fase3",
        numero=3,
        nome="Simulados e Ajuste Fino",
        subtitulo="Dias 19 a 26",
        dia_inicial=19,
        dia_final=26,
        cor="#1f9d76",
        objetivo=(
            "Treinar prova, não conteúdo: gestão de tempo, ordem de resolução, controle da "
            "ansiedade e resistência mental nas últimas questões."
        ),
        medalha="fase3",
    ),
    Fase(
        id="fase4",
        numero=4,
        nome="Blindagem e Reta Final",
        subtitulo="Dias 27 a 30",
        dia_inicial=27,
        dia_final=30,
        cor="#7a5af5",
        objetivo=(
            "Reduzir volume, revisar só o que ainda dói, cuidar do corpo e da cabeça e chegar "
            "descansado — não exausto — no dia da prova."
        ),
        medalha="fase4",
    ),
)

FASES_POR_ID = {f.id: f for f in FASES}

from .fase1 import DIAS as _D1  # noqa: E402
from .fase2 import DIAS as _D2  # noqa: E402
from .fase3 import DIAS as _D3  # noqa: E402
from .fase4 import DIAS as _D4  # noqa: E402

DIAS: tuple[Dia, ...] = tuple(_D1 + _D2 + _D3 + _D4)
TOTAL_DIAS = len(DIAS)
POR_NUMERO: dict[int, Dia] = {d.numero: d for d in DIAS}


def dia(numero: int) -> Optional[Dia]:
    return POR_NUMERO.get(numero)


def fase_do_dia(numero: int) -> Fase:
    d = POR_NUMERO.get(numero)
    return FASES_POR_ID[d.fase] if d else FASES[0]


def dias_da_fase(fase_id: str) -> list[Dia]:
    return [d for d in DIAS if d.fase == fase_id]


__all__ = [
    "DIAS",
    "FASES",
    "FASES_POR_ID",
    "POR_NUMERO",
    "TOTAL_DIAS",
    "Dia",
    "Fase",
    "Missao",
    "dia",
    "dias_da_fase",
    "fase_do_dia",
]
