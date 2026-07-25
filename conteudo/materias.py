"""Matérias do concurso, peso relativo e blocos de estudo.

⚠️ Os pesos abaixo são uma leitura estatística das provas anteriores do
concurso de Soldado PM 2ª Classe de São Paulo — servem para priorizar o
estudo, não substituem o edital vigente. A plataforma exibe esse aviso ao
aluno na tela de prioridades.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Materia:
    id: str
    nome: str
    curta: str
    bloco: str  # "linguagens" | "exatas" | "direito" | "geral"
    peso: int  # 1 a 5 — quanto mais alto, mais cai
    cor: str
    resumo: str
    armadilha: str


MATERIAS: tuple[Materia, ...] = (
    Materia(
        id="portugues",
        nome="Língua Portuguesa",
        curta="Português",
        bloco="linguagens",
        peso=5,
        cor="#2f6fed",
        resumo=(
            "A matéria que mais decide aprovação: cai em peso alto e é onde o candidato "
            "com pressa costuma perder pontos fáceis de interpretação e concordância."
        ),
        armadilha="Ler o enunciado rápido demais e responder pelo que você acha que o texto disse.",
    ),
    Materia(
        id="matematica",
        nome="Matemática e Raciocínio Lógico",
        curta="Matemática",
        bloco="exatas",
        peso=4,
        cor="#e0663c",
        resumo=(
            "Poucos temas se repetem muito: porcentagem, regra de três, razão e proporção, "
            "equações do 1º grau, sequências e lógica proposicional."
        ),
        armadilha="Tentar resolver tudo na fórmula grande quando a questão pede estimativa.",
    ),
    Materia(
        id="constitucional",
        nome="Direito Constitucional",
        curta="Constitucional",
        bloco="direito",
        peso=5,
        cor="#1f9d76",
        resumo=(
            "Direitos e garantias fundamentais (art. 5º), organização do Estado e segurança "
            "pública (art. 144) concentram a maioria absoluta das questões."
        ),
        armadilha="Trocar 'todos' por 'brasileiros natos' e engolir generalizações absolutas.",
    ),
    Materia(
        id="administrativo",
        nome="Direito Administrativo",
        curta="Administrativo",
        bloco="direito",
        peso=4,
        cor="#7a5af5",
        resumo=(
            "Princípios da Administração (LIMPE), atos administrativos, poderes e "
            "responsabilidade do Estado — muita decoreba com pegadinha de exceção."
        ),
        armadilha="Confundir anulação com revogação e discricionariedade com arbitrariedade.",
    ),
    Materia(
        id="penal",
        nome="Direito Penal",
        curta="Penal",
        bloco="direito",
        peso=4,
        cor="#c2385c",
        resumo=(
            "Aplicação da lei penal, crimes contra a pessoa e o patrimônio, e crimes "
            "praticados por funcionário público contra a Administração."
        ),
        armadilha="Misturar elementos de furto, roubo e extorsão nas alternativas.",
    ),
    Materia(
        id="legislacao",
        nome="Legislação Especial e Institucional",
        curta="Legislação",
        bloco="direito",
        peso=3,
        cor="#8a6d1f",
        resumo=(
            "Drogas, estatutos (Criança e Adolescente, Idoso), violência doméstica, "
            "abuso de autoridade e a legislação da própria instituição."
        ),
        armadilha="Achar que toda conduta com droga é tráfico — o porte para uso tem regra própria.",
    ),
    Materia(
        id="atualidades",
        nome="Atualidades e Cidadania",
        curta="Atualidades",
        bloco="geral",
        peso=2,
        cor="#0f8ba8",
        resumo=(
            "Segurança pública, políticas sociais, meio ambiente e temas de cidadania. "
            "Estudo de manutenção: pouco tempo, alta frequência."
        ),
        armadilha="Estudar notícia solta em vez de tema recorrente.",
    ),
    Materia(
        id="informatica",
        nome="Noções de Informática",
        curta="Informática",
        bloco="geral",
        peso=2,
        cor="#5a6270",
        resumo=(
            "Pacote de escritório, navegadores, segurança da informação e conceitos "
            "básicos de rede. Ponto barato: pouca teoria, muita questão repetida."
        ),
        armadilha="Decorar atalho sem entender o que a função faz.",
    ),
)

POR_ID = {m.id: m for m in MATERIAS}
IDS = tuple(m.id for m in MATERIAS)

CATEGORIAS_ERRO = {
    "conteudo": {
        "nome": "Falta de conteúdo",
        "icone": "📚",
        "acao": "Você não sabia a regra. Ação: revisar a teoria específica desse tema — só ela.",
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
