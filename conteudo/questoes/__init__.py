"""Banco de questões da plataforma.

Todas as questões são autorais, escritas no estilo de cobrança das provas de
Soldado PM 2ª Classe (múltipla escolha, cinco alternativas, uma correta), com
comentário de correção ativa — que é o método central do e-book: cada erro
vira aula, cada padrão de erro vira um ponto de atenção.

Cada questão tem, além do gabarito, o campo `armadilha`: o que a banca queria
que você fizesse de errado. É o que transforma "errei" em "sei por que errei".
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Iterable, Optional, Sequence


@dataclass(frozen=True)
class Questao:
    id: str
    materia: str
    tema: str
    nivel: str  # facil | medio | dificil
    enunciado: str
    alternativas: tuple[tuple[str, str], ...]
    correta: str
    comentario: str
    armadilha: str = ""

    def alternativa_texto(self, letra: str) -> str:
        for chave, texto in self.alternativas:
            if chave == letra:
                return texto
        return ""


from . import (  # noqa: E402  (import após a definição de Questao, de propósito)
    administracao,
    geografia,
    historia,
    informatica,
    matematica,
    portugues,
)

QUESTOES: tuple[Questao, ...] = tuple(
    portugues.QUESTOES
    + matematica.QUESTOES
    + historia.QUESTOES
    + geografia.QUESTOES
    + informatica.QUESTOES
    + administracao.QUESTOES
)

POR_ID: dict[str, Questao] = {q.id: q for q in QUESTOES}

POR_MATERIA: dict[str, list[Questao]] = {}
for _q in QUESTOES:
    POR_MATERIA.setdefault(_q.materia, []).append(_q)

NIVEL_PESO = {"facil": 1, "medio": 2, "dificil": 3}


def questao(qid: str) -> Optional[Questao]:
    return POR_ID.get(qid)


def total_por_materia() -> dict[str, int]:
    return {materia: len(lista) for materia, lista in POR_MATERIA.items()}


def selecionar(
    materias: Sequence[str] | None = None,
    quantidade: int = 10,
    excluir: Iterable[str] = (),
    nivel: str | None = None,
    semente: int | None = None,
) -> list[Questao]:
    """Sorteia questões de forma estável (mesma semente → mesma prova).

    Distribui a quantidade pedida entre as matérias solicitadas, de modo que o
    aluno não receba um bloco inteiro de uma única matéria por acaso.
    """
    excluidas = set(excluir)
    alvo = [m for m in (materias or list(POR_MATERIA)) if m in POR_MATERIA]
    if not alvo:
        alvo = list(POR_MATERIA)

    rnd = random.Random(semente)
    baldes: list[list[Questao]] = []
    for m in alvo:
        disponiveis = [
            q
            for q in POR_MATERIA[m]
            if q.id not in excluidas and (nivel is None or q.nivel == nivel)
        ]
        rnd.shuffle(disponiveis)
        baldes.append(disponiveis)

    escolhidas: list[Questao] = []
    indice = 0
    while len(escolhidas) < quantidade and any(baldes):
        balde = baldes[indice % len(baldes)]
        if balde:
            escolhidas.append(balde.pop())
        else:
            baldes = [b for b in baldes if b]
            if not baldes:
                break
            continue
        indice += 1

    if len(escolhidas) < quantidade and (nivel or excluidas):
        # completa ignorando o filtro de nível para não devolver bloco curto
        resto = [q for q in QUESTOES if q not in escolhidas and q.id not in excluidas]
        rnd.shuffle(resto)
        escolhidas.extend(resto[: quantidade - len(escolhidas)])

    return escolhidas[:quantidade]


def por_ids(ids: Sequence[str]) -> list[Questao]:
    return [POR_ID[i] for i in ids if i in POR_ID]


__all__ = [
    "POR_ID",
    "POR_MATERIA",
    "QUESTOES",
    "Questao",
    "por_ids",
    "questao",
    "selecionar",
    "total_por_materia",
]
