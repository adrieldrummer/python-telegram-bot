"""Conteúdo do curso — versionado em git, fora do banco de dados.

Reúne: matérias e pesos, trilha de 30 dias, banco de questões, simulados,
patentes/medalhas e o catálogo visual (as "capas" da área do aluno).
"""

from __future__ import annotations

from dataclasses import dataclass

from . import materias, patentes, questoes, simulados, trilha

TOTAL_DIAS = trilha.TOTAL_DIAS
TOTAL_QUESTOES = len(questoes.QUESTOES)


@dataclass(frozen=True)
class Coleção:
    """Uma 'fileira' da área do aluno, no estilo de uma vitrine de streaming."""

    id: str
    titulo: str
    subtitulo: str
    itens: tuple[dict, ...]


def capa_fase(fase_id: str) -> str:
    return f"/static/img/capa-{fase_id}.webp"


CAPAS = {
    "fase1": "/static/img/capa-fase1.webp",
    "fase2": "/static/img/capa-fase2.webp",
    "fase3": "/static/img/capa-fase3.webp",
    "fase4": "/static/img/capa-fase4.webp",
    "questoes": "/static/img/capa-questoes.webp",
    "erros": "/static/img/capa-erros.webp",
    "simulados": "/static/img/capa-simulados.webp",
    "certificado": "/static/img/capa-certificado.webp",
    "manual": "/static/img/capa-manual.webp",
    "pontos": "/static/img/capa-pontos.webp",
    "hero": "/static/img/hero.webp",
    "logo": "/static/img/emblema.png",
    "emblema": "/static/img/emblema.png",
    "textura": "/static/img/textura.webp",
}

TREINOS = (
    {
        "id": "questoes",
        "titulo": "Banco de Questões",
        "descricao": f"{TOTAL_QUESTOES} questões comentadas, filtráveis por matéria e nível.",
        "capa": CAPAS["questoes"],
        "url": "/questoes",
        "etiqueta": "Treino livre",
    },
    {
        "id": "erros",
        "titulo": "Caderno de Erros",
        "descricao": "Revisão espaçada automática (1-3-7-15 dias) do que você errou.",
        "capa": CAPAS["erros"],
        "url": "/erros",
        "etiqueta": "Diferencial",
    },
    {
        "id": "simulados",
        "titulo": "Simulados Cronometrados",
        "descricao": "Três provas completas com relatório de tempo e desempenho por matéria.",
        "capa": CAPAS["simulados"],
        "url": "/simulados",
        "etiqueta": "Prova real",
    },
    {
        "id": "pontos",
        "titulo": "Pontos e Patentes",
        "descricao": "Seu progresso em pontos de estudo, medalhas e patentes.",
        "capa": CAPAS["pontos"],
        "url": "/pontos",
        "etiqueta": "Progresso",
    },
    {
        "id": "manual",
        "titulo": "Manual do Mapa (e-book)",
        "descricao": "O e-book original revisado e ampliado, em formato de leitura.",
        "capa": CAPAS["manual"],
        "url": "/manual",
        "etiqueta": "Leitura",
    },
    {
        "id": "certificado",
        "titulo": "Certificado de Conclusão",
        "descricao": "Liberado ao concluir os 30 dias da jornada.",
        "capa": CAPAS["certificado"],
        "url": "/certificado",
        "etiqueta": "Meta final",
    },
)

__all__ = [
    "CAPAS",
    "TOTAL_DIAS",
    "TOTAL_QUESTOES",
    "TREINOS",
    "materias",
    "patentes",
    "questoes",
    "simulados",
    "trilha",
]
