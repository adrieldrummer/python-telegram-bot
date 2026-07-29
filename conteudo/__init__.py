"""Conteúdo do curso — versionado em git, fora do banco de dados.

Reúne: os fatos do edital, matérias e pesos, a trilha de 7 dias, o banco de
questões, os simulados no formato oficial, os módulos avançados, planos,
patentes/medalhas e o catálogo visual (as "capas" da área do aluno).

Sobre as imagens: elas não são enfeite. Cada arte tem **um** significado fixo
(ver `NARRATIVA`), e esse significado é o mesmo na página de vendas e dentro da
plataforma. Repetir a mesma imagem em contextos diferentes ensina o aluno a
ignorá-la; usar sempre a mesma para a mesma ideia faz o contrário.
"""

from __future__ import annotations

from dataclasses import dataclass

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
    # o que decide a vaga depois da objetiva
    "capa-redacao": "/static/img/capa-redacao.webp",
    "capa-taf": "/static/img/capa-taf.webp",
    "capa-etapas": "/static/img/capa-documentos.webp",
    # o ponto de partida e o ponto de chegada do aluno
    "celular": "/static/img/capa-celular.webp",
    "prova": "/static/img/capa-prova.webp",
    "redacao": "/static/img/capa-redacao.webp",
    "documentos": "/static/img/capa-documentos.webp",
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
    "fundo-auth": "/static/img/fundo-auth.webp",
    "logo": "/static/img/emblema.png",
    "emblema": "/static/img/emblema.png",
    "textura": "/static/img/textura.webp",
}


def capa(chave: str) -> str:
    return CAPAS.get(chave, CAPAS["questoes"])


# --- a linha do tempo visual ------------------------------------------------


@dataclass(frozen=True)
class Momento:
    """Um instante da jornada do candidato, com a imagem que o representa."""

    id: str
    rotulo: str        # onde ele está nessa história
    titulo: str
    legenda: str
    capa: str


NARRATIVA: tuple[Momento, ...] = (
    Momento(
        id="hoje",
        rotulo="Hoje",
        titulo="O celular na mesa da cozinha",
        legenda=(
            "Depois do trabalho, com o que sobrou do dia. É desse ponto que "
            "quase todo aprovado começa — e é para esse ponto que a plataforma "
            "foi feita."
        ),
        capa="celular",
    ),
    Momento(
        id="prova",
        rotulo="20 de setembro",
        titulo="A manhã que decide o ano",
        legenda=(
            f"{edital.TOTAL_QUESTOES_PROVA} questões objetivas e um mínimo de "
            f"{edital.NOTA_MINIMA} pontos. Quem chega treinado no formato não é "
            "surpreendido pelo relógio."
        ),
        capa="prova",
    ),
    Momento(
        id="dissertativa",
        rotulo="Etapa 2",
        titulo="A redação que elimina quem passou",
        legenda=(
            "Prova dissertativa corrigida por estrutura, argumentação e norma-"
            "padrão. Três textos treinados resolvem."
        ),
        capa="redacao",
    ),
    Momento(
        id="etapas",
        rotulo="Etapas 3 a 6",
        titulo="TAF, saúde, psicológico e investigação",
        legenda=(
            "Aqui se perde vaga por certidão atrasada e exame fora do prazo, "
            "não por mérito. Organização é conteúdo."
        ),
        capa="documentos",
    ),
    Momento(
        id="formatura",
        rotulo="A chegada",
        titulo="A formatura",
        legenda=(
            f"{edital.VAGAS} pessoas vão estar nessa formação. O processo até "
            "ela é o que esta plataforma organiza."
        ),
        capa="formatura",
    ),
    Momento(
        id="farda",
        rotulo="Depois",
        titulo="A farda e a rua",
        legenda=(
            f"Salário inicial de R$ {edital.SALARIO_INICIAL:,.2f}".replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
            + ", estabilidade e carreira no policiamento ostensivo."
        ),
        capa="viatura",
    ),
)

NARRATIVA_POR_ID = {m.id: m for m in NARRATIVA}


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
        "capa": CAPAS["prova"],
        "url": "/simulados",
        "etiqueta": "Formato da prova",
        "recurso": "simulados",
    },
    {
        "id": "modulos",
        "titulo": "Módulos Avançados",
        "descricao": "Redação, TAF, etapas eliminatórias e aprofundamento por matéria.",
        "capa": CAPAS["formatura"],
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
