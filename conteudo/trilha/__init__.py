"""Trilha de 7 dias — a apostila explicativa do edital PM-SP 2026.

A ideia do material é essa: explicar cada tópico do edital de forma clara, para
o aluno **entender** o assunto em vez de memorizar conteúdo em excesso e
esquecer tudo antes de terminar a leitura. Depois de entender, o que fixa é
resolver questão e revisar erro — e é isso que a plataforma automatiza.
"""

from __future__ import annotations

from dataclasses import dataclass
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

    tipo: str  # questoes | revisao | simulado | diagnostico
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
    diario: str = ""


FASES: tuple[Fase, ...] = (
    Fase(
        id="base",
        numero=1,
        nome="A base da prova",
        subtitulo="Dias 1 e 2",
        dia_inicial=1,
        dia_final=2,
        cor="#2f6fed",
        objetivo=(
            "Português e Matemática valem 35 das 60 questões. Começar por elas é começar "
            "por onde estão os pontos."
        ),
        medalha="fase1",
    ),
    Fase(
        id="calculo",
        numero=2,
        nome="Cálculo e memória",
        subtitulo="Dias 3 e 4",
        dia_inicial=3,
        dia_final=4,
        cor="#e0663c",
        objetivo="Fechar geometria e raciocínio lógico e montar a linha do tempo de História.",
        medalha="fase2",
    ),
    Fase(
        id="mundo",
        numero=3,
        nome="Mundo e ferramentas",
        subtitulo="Dias 5 e 6",
        dia_inicial=5,
        dia_final=6,
        cor="#1f9d76",
        objetivo="Geografia, atualidades e as cinco questões baratas de Informática.",
        medalha="fase3",
    ),
    Fase(
        id="fechamento",
        numero=4,
        nome="Instituição e fechamento",
        subtitulo="Dia 7",
        dia_inicial=7,
        dia_final=7,
        cor="#7a5af5",
        objetivo="Administração Pública, revisão do mapa inteiro e o plano até o dia da prova.",
        medalha="fase4",
    ),
)

FASES_POR_ID = {f.id: f for f in FASES}

from .dias import DIAS as _DIAS  # noqa: E402

DIAS: tuple[Dia, ...] = tuple(_DIAS)
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
