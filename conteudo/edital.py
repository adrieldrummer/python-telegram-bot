"""Os fatos do concurso, num lugar só.

Tudo aqui vem do edital do concurso de Soldado PM 2ª Classe da Polícia Militar
do Estado de São Paulo (2026), organizado pela Fundação VUNESP. Os números
aparecem na página de vendas, no painel do aluno e na montagem dos simulados —
mudou o edital, muda um arquivo.

⚠️ Confira sempre o edital oficial: datas e regras podem ser retificadas.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Etapa:
    id: str
    nome: str
    descricao: str
    eliminatoria: bool
    dica: str


CONCURSO = "Soldado PM 2ª Classe — Polícia Militar do Estado de São Paulo"
ANO = 2026
BANCA = "Fundação VUNESP"
VAGAS = 2000
SALARIO_INICIAL = 5482.51
TAXA_INSCRICAO = 100.00

DATA_PROVA = date(2026, 9, 20)
FIM_INSCRICOES = date(2026, 8, 21)

REQUISITOS = (
    "Ensino médio completo",
    "Idade de 17 a 30 anos",
    "Altura mínima de 1,60 m (homens) e 1,55 m (mulheres)",
    "CNH nas categorias entre B e E",
    "Estar quite com as obrigações militares e eleitorais",
)

# Distribuição da prova objetiva: 60 questões.
# Conferida contra a prova aplicada em 30/11/2025 pela VUNESP (Soldado PM 2ª Classe),
# que trouxe: Português 1–20, Matemática 21–35, Conhecimentos Gerais 36–50
# (História 36–41 e Geografia/Atualidades 42–50), Informática 51–55 e
# Administração Pública 56–60.
# O peso de cada matéria aqui é literalmente o número de questões que ela vale.
PROVA_OBJETIVA = (
    ("portugues", "Língua Portuguesa e Interpretação de Texto", 20),
    ("matematica", "Matemática", 15),
    ("historia", "História (Conhecimentos Gerais)", 6),
    ("geografia", "Geografia e Atualidades (Conhecimentos Gerais)", 9),
    ("informatica", "Noções de Informática", 5),
    ("administracao", "Noções de Administração Pública", 5),
)

# A prova é de múltipla escolha com CINCO alternativas (A a E) — o banco de
# questões da plataforma segue o mesmo formato.
ALTERNATIVAS_POR_QUESTAO = 5
PROVA_REFERENCIA = "Prova objetiva de 30/11/2025 (VUNESP), versão 3"
TOTAL_QUESTOES_PROVA = sum(q for _, _, q in PROVA_OBJETIVA)
NOTA_MINIMA = 30  # pontos, de 60

ETAPAS = (
    Etapa(
        id="objetiva",
        nome="Prova objetiva",
        descricao=(
            f"{TOTAL_QUESTOES_PROVA} questões de múltipla escolha. É preciso somar pelo menos "
            f"{NOTA_MINIMA} pontos para seguir no concurso."
        ),
        eliminatoria=True,
        dica="É aqui que a maioria cai — e é o foco da trilha de 7 dias.",
    ),
    Etapa(
        id="dissertativa",
        nome="Prova dissertativa",
        descricao="Redação avaliada por estrutura, argumentação e domínio da norma-padrão.",
        eliminatoria=True,
        dica="Quem treina três redações no modelo da banca não é surpreendido.",
    ),
    Etapa(
        id="taf",
        nome="Teste de aptidão física (TAF)",
        descricao="Provas físicas de resistência e força, com índices mínimos por sexo e idade.",
        eliminatoria=True,
        dica="Oito semanas de preparo consistente resolvem — começar na véspera, não.",
    ),
    Etapa(
        id="saude",
        nome="Exames de saúde",
        descricao="Avaliação médica e odontológica, com exames laboratoriais e de imagem.",
        eliminatoria=True,
        dica="Muita reprovação vem de exame não entregue ou fora do prazo, não de doença.",
    ),
    Etapa(
        id="psicologico",
        nome="Avaliação psicológica",
        descricao="Testes e entrevista para verificar o perfil exigido para a função policial.",
        eliminatoria=True,
        dica="Não existe 'gabarito': existe coerência entre o que você responde e quem você é.",
    ),
    Etapa(
        id="investigacao",
        nome="Investigação social",
        descricao="Análise da vida pregressa, documentos, certidões e conduta do candidato.",
        eliminatoria=True,
        dica="Comece a juntar certidões agora; é a etapa que mais atrasa candidato desatento.",
    ),
)


def dias_para_prova(hoje: date | None = None) -> int:
    return (DATA_PROVA - (hoje or date.today())).days


def dias_para_inscricao(hoje: date | None = None) -> int:
    return (FIM_INSCRICOES - (hoje or date.today())).days


def questoes_da_materia(materia_id: str) -> int:
    for chave, _, quantidade in PROVA_OBJETIVA:
        if chave == materia_id:
            return quantidade
    return 0


def resumo() -> dict:
    """Bloco de fatos usado nas telas."""
    return {
        "concurso": CONCURSO,
        "ano": ANO,
        "banca": BANCA,
        "vagas": VAGAS,
        "salario": SALARIO_INICIAL,
        "taxa": TAXA_INSCRICAO,
        "data_prova": DATA_PROVA,
        "fim_inscricoes": FIM_INSCRICOES,
        "dias_prova": dias_para_prova(),
        "dias_inscricao": dias_para_inscricao(),
        "total_questoes": TOTAL_QUESTOES_PROVA,
        "nota_minima": NOTA_MINIMA,
        "requisitos": REQUISITOS,
        "etapas": ETAPAS,
        "prova": PROVA_OBJETIVA,
    }
