"""Conteúdo do curso — versionado em git, fora do banco de dados.

Reúne: os fatos do edital, matérias e pesos, a trilha de 7 dias, o banco de
questões, os simulados no formato oficial, os módulos avançados, planos,
patentes/medalhas e o catálogo visual (as "capas" da área do aluno).
"""

from __future__ import annotations

from . import edital, materias, modulos, patentes, planos, questoes, simulados, trilha

TOTAL_DIAS = trilha.TOTAL_DIAS
TOTAL_QUESTOES = len(questoes.QUESTOES)
TOTAL_MODULOS = len(modulos.MODULOS)
TOTAL_AULAS_AVANCADAS = modulos.TOTAL_AULAS

CAPAS = {
    "base": "/static/img/capa-fase1.webp",
    "calculo": "/static/img/capa-fase2.webp",
    "mundo": "/static/img/capa-fase3.webp",
    "fechamento": "/static/img/capa-fase4.webp",
    "capa-fase1": "/static/img/capa-fase1.webp",
    "capa-fase2": "/static/img/capa-fase2.webp",
    "capa-fase3": "/static/img/capa-fase3.webp",
    "capa-fase4": "/static/img/capa-fase4.webp",
    "capa-redacao": "/static/img/capa-manual.webp",
    "capa-taf": "/static/img/capa-taf.webp",
    "capa-etapas": "/static/img/capa-formatura.webp",
    # artes da farda — o que o aluno está buscando no fim da linha
    "farda": "/static/img/capa-farda.webp",
    "bota": "/static/img/capa-bota.webp",
    "formatura": "/static/img/capa-formatura.webp",
    "viatura": "/static/img/capa-viatura.webp",
    "questoes": "/static/img/capa-questoes.webp",
    "erros": "/static/img/capa-erros.webp",
    "simulados": "/static/img/capa-simulados.webp",
    "certificado": "/static/img/capa-certificado.webp",
    "manual": "/static/img/capa-manual.webp",
    "pontos": "/static/img/capa-pontos.webp",
    "hero": "/static/img/hero-farda.webp",
    "hero-mapa": "/static/img/hero.webp",
    "logo": "/static/img/emblema.png",
    "emblema": "/static/img/emblema.png",
    "textura": "/static/img/textura.webp",
}


def capa(chave: str) -> str:
    return CAPAS.get(chave, CAPAS["questoes"])


TREINOS = (
    {
        "id": "questoes",
        "titulo": "Banco de Questões",
        "descricao": f"{TOTAL_QUESTOES} questões comentadas, por matéria e por nível.",
        "capa": CAPAS["questoes"],
        "url": "/questoes",
        "etiqueta": "Treino livre",
        "recurso": "questoes",
    },
    {
        "id": "erros",
        "titulo": "Caderno de Erros",
        "descricao": "Revisão espaçada automática (1-3-7-15 dias) do que você errou.",
        "capa": CAPAS["erros"],
        "url": "/erros",
        "etiqueta": "Diferencial",
        "recurso": "erros",
    },
    {
        "id": "simulados",
        "titulo": "Simulados Oficiais",
        "descricao": "Provas de 60 questões no formato exato da VUNESP, com relatório.",
        "capa": CAPAS["simulados"],
        "url": "/simulados",
        "etiqueta": "Formato da prova",
        "recurso": "simulados",
    },
    {
        "id": "modulos",
        "titulo": "Módulos Avançados",
        "descricao": "Redação, TAF, etapas eliminatórias e aprofundamento por matéria.",
        "capa": CAPAS["capa-redacao"],
        "url": "/modulos",
        "etiqueta": "Além da objetiva",
        "recurso": "avancado",
    },
    {
        "id": "manual",
        "titulo": "Apostila Completa",
        "descricao": "O edital inteiro explicado, para consulta e download.",
        "capa": CAPAS["manual"],
        "url": "/manual",
        "etiqueta": "Leitura",
        "recurso": "manual",
    },
    {
        "id": "pontos",
        "titulo": "Pontos e Patentes",
        "descricao": "Seu progresso em pontos de estudo, medalhas e patentes.",
        "capa": CAPAS["pontos"],
        "url": "/pontos",
        "etiqueta": "Progresso",
        "recurso": "",
    },
)

__all__ = [
    "CAPAS",
    "TOTAL_AULAS_AVANCADAS",
    "TOTAL_DIAS",
    "TOTAL_MODULOS",
    "TOTAL_QUESTOES",
    "TREINOS",
    "capa",
    "edital",
    "materias",
    "modulos",
    "patentes",
    "planos",
    "questoes",
    "simulados",
    "trilha",
]
