"""Matérias do edital, com o peso que elas realmente têm na prova.

O `peso` aqui não é uma escala inventada de 1 a 5: é o **número de questões**
que a matéria vale na prova objetiva da VUNESP (60 no total). Isso faz o mapa
de prioridades do aluno responder à pergunta certa — "onde estão os pontos?" —
em vez de a uma opinião.
"""

from __future__ import annotations

from dataclasses import dataclass

from .edital import PROVA_OBJETIVA, TOTAL_QUESTOES_PROVA


@dataclass(frozen=True)
class Materia:
    id: str
    nome: str
    curta: str
    bloco: str  # "linguagens" | "exatas" | "gerais" | "institucional"
    peso: int  # questões na prova objetiva
    cor: str
    resumo: str
    armadilha: str
    temas: tuple[str, ...]


MATERIAS: tuple[Materia, ...] = (
    Materia(
        id="portugues",
        nome="Língua Portuguesa e Interpretação de Texto",
        curta="Português",
        bloco="linguagens",
        peso=20,
        cor="#2f6fed",
        resumo=(
            "Um terço da prova. Sozinha, vale mais que Informática e Administração Pública "
            "somadas — e é a matéria em que dá para subir mais rápido."
        ),
        armadilha="Responder pelo que você achou que o texto disse, e não pelo que ele diz.",
        temas=(
            "Leitura e interpretação de textos",
            "Sinônimos e antônimos",
            "Sentido próprio e figurado",
            "Pontuação",
            "Classes de palavras",
            "Concordância verbal e nominal",
            "Regência verbal e nominal",
            "Colocação pronominal",
            "Crase",
        ),
    ),
    Materia(
        id="matematica",
        nome="Matemática e Raciocínio Lógico",
        curta="Matemática",
        bloco="exatas",
        peso=15,
        cor="#e0663c",
        resumo=(
            "Quinze questões que se repetem em poucos temas: porcentagem, regra de três, "
            "equações, geometria básica e lógica. É a matéria mais previsível do edital."
        ),
        armadilha="Montar a conta antes de identificar se a proporção é direta ou inversa.",
        temas=(
            "Números inteiros e racionais",
            "MMC",
            "Razão, proporção e porcentagem",
            "Regra de três simples",
            "Média aritmética",
            "Equações e sistemas do 1º grau",
            "Sistema métrico",
            "Tabelas e gráficos",
            "Perímetro, área, volume e Teorema de Pitágoras",
            "Raciocínio lógico e situações-problema",
        ),
    ),
    Materia(
        id="historia",
        nome="História Geral e do Brasil",
        curta="História",
        bloco="gerais",
        peso=6,
        cor="#8a6d1f",
        resumo=(
            "Recorte fechado: guerras mundiais, Guerra Fria, Era Vargas, regime militar e "
            "redemocratização. Estudar por linha do tempo rende mais que decorar data solta."
        ),
        armadilha="Trocar causa por consequência — a banca adora inverter a ordem dos fatos.",
        temas=(
            "Primeira Guerra Mundial",
            "Nazifascismo e Segunda Guerra Mundial",
            "Guerra Fria",
            "Globalização e neoliberalismo",
            "Revolução de 1930 e Era Vargas",
            "Constituições republicanas",
            "Regime militar (1964–1985)",
            "Abertura política e redemocratização",
        ),
    ),
    Materia(
        id="geografia",
        nome="Geografia e Atualidades",
        curta="Geografia",
        bloco="gerais",
        peso=9,
        cor="#1f9d76",
        resumo=(
            "Natureza brasileira, população, economia e meio ambiente — mais atualidades dos "
            "últimos seis meses, com atenção ao estado de São Paulo."
        ),
        armadilha="Estudar notícia isolada em vez de tema recorrente.",
        temas=(
            "Nova ordem mundial e geopolítica",
            "Problemas e impactos ambientais",
            "Relevo, hidrografia, clima e biomas",
            "População brasileira",
            "Atividades econômicas e fontes de energia",
            "Atualidades (últimos seis meses)",
        ),
    ),
    Materia(
        id="informatica",
        nome="Noções de Informática",
        curta="Informática",
        bloco="gerais",
        peso=5,
        cor="#5a6270",
        resumo=(
            "Cinco questões baratas: Windows 10, Word, Excel e PowerPoint 2016, e-mail, "
            "internet, Google Workspace e Teams. Pouca teoria, muita repetição."
        ),
        armadilha="Decorar atalho sem entender o que a função faz.",
        temas=(
            "MS-Windows 10",
            "MS-Word 2016",
            "MS-Excel 2016",
            "MS-PowerPoint 2016",
            "Correio eletrônico",
            "Internet e navegação",
            "Google Workspace",
            "Microsoft Teams",
        ),
    ),
    Materia(
        id="administracao",
        nome="Noções de Administração Pública",
        curta="Adm. Pública",
        bloco="institucional",
        peso=5,
        cor="#7a5af5",
        resumo=(
            "Constituição Federal (direitos fundamentais, Administração e segurança pública), "
            "Constituição do Estado de São Paulo, Lei de Acesso à Informação e o Decreto "
            "estadual 68.155/2023."
        ),
        armadilha="Misturar o que está na Constituição Federal com o que é da Constituição paulista.",
        temas=(
            "Direitos e garantias fundamentais (CF, Título II)",
            "Administração Pública e militares dos Estados (CF, Título III)",
            "Segurança pública (CF, Título V)",
            "Poderes Executivo e Judiciário e Justiça Militar (CE-SP)",
            "Administração Pública e servidores (CE-SP)",
            "Segurança pública e Polícia Militar (CE-SP)",
            "Lei de Acesso à Informação (Lei 12.527/2011)",
            "Decreto estadual 68.155/2023",
        ),
    ),
)

POR_ID = {m.id: m for m in MATERIAS}
IDS = tuple(m.id for m in MATERIAS)
TOTAL_QUESTOES_PROVA = TOTAL_QUESTOES_PROVA
DISTRIBUICAO_PROVA = PROVA_OBJETIVA

CATEGORIAS_ERRO = {
    "conteudo": {
        "nome": "Falta de conteúdo",
        "icone": "📚",
        "acao": "Você não sabia a regra. Ação: revisar a explicação daquele tema — só ela.",
    },
    "pegadinha": {
        "nome": "Pegadinha de interpretação",
        "icone": "🎯",
        "acao": "Você sabia, mas caiu no jeito que a banca escreveu. Ação: reler grifando o comando.",
    },
    "desatencao": {
        "nome": "Desatenção",
        "icone": "⏱",
        "acao": "Você sabia e errou por pressa. Ação: reduzir ritmo e conferir a alternativa marcada.",
    },
}


def materia(id_materia: str) -> Materia:
    return POR_ID[id_materia]


def nome_materia(id_materia: str) -> str:
    m = POR_ID.get(id_materia)
    return m.nome if m else id_materia


def peso_relativo(id_materia: str) -> float:
    """Quanto a matéria vale, em percentual da prova."""
    m = POR_ID.get(id_materia)
    return round(m.peso * 100 / TOTAL_QUESTOES_PROVA, 1) if m else 0.0
