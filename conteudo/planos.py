"""Planos comercializados e o que cada um libera dentro da plataforma.

Um plano é um conjunto de **recursos**. As telas perguntam "esse aluno tem o
recurso X?" — nunca "esse aluno é do plano Y". Assim dá para criar oferta nova,
promoção ou combo sem mexer em nenhuma tela.

O casamento com a Cakto é feito por `codigos_cakto`: coloque ali o id (ou um
pedaço do nome) do produto/oferta como ele chega no webhook. Se nada casar, o
aluno entra no `PLANO_PADRAO`.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# --- recursos disponíveis --------------------------------------------------

RECURSOS = {
    "trilha": "Jornada de 30 dias com desbloqueio diário",
    "questoes": "Banco de questões comentadas",
    "erros": "Caderno de Erros com revisão espaçada",
    "simulados": "Simulados cronometrados com relatório",
    "manual": "Manual do Mapa (e-book completo)",
    "certificado": "Certificado de conclusão",
    "ranking": "Ranking da turma",
    "suporte": "Suporte prioritário por e-mail",
}


@dataclass(frozen=True)
class Plano:
    id: str
    nome: str
    chamada: str
    preco: str
    preco_de: str = ""
    ciclo: str = "único"  # único | mensal | anual
    duracao_dias: int = 0  # 0 = sem expiração (vitalício / enquanto durar o acesso)
    recursos: tuple[str, ...] = ()
    destaque: bool = False
    checkout_url: str = ""
    codigos_cakto: tuple[str, ...] = ()
    beneficios: tuple[str, ...] = field(default_factory=tuple)


PLANOS: tuple[Plano, ...] = (
    Plano(
        id="recruta",
        nome="Recruta",
        chamada="O método completo, no seu ritmo.",
        preco="R$ 97",
        ciclo="único",
        duracao_dias=180,
        recursos=("trilha", "questoes", "erros"),
        codigos_cakto=("recruta", "essencial", "basico"),
        beneficios=(
            "Jornada de 30 dias com missão diária",
            "Banco completo de questões comentadas",
            "Caderno de Erros com revisão espaçada",
            "6 meses de acesso",
        ),
    ),
    Plano(
        id="operacao",
        nome="Operação Completa",
        chamada="Tudo o que aprova: método, simulados e manual.",
        preco="R$ 197",
        preco_de="R$ 297",
        ciclo="único",
        duracao_dias=365,
        recursos=("trilha", "questoes", "erros", "simulados", "manual", "certificado", "ranking"),
        destaque=True,
        codigos_cakto=("operacao", "completo", "completa"),
        beneficios=(
            "Tudo do plano Recruta",
            "3 simulados cronometrados com relatório por matéria",
            "Manual do Mapa — e-book revisado e ampliado",
            "Certificado de conclusão",
            "1 ano de acesso",
        ),
    ),
    Plano(
        id="elite",
        nome="Elite",
        chamada="Para quem vai prestar mais de um concurso.",
        preco="R$ 29,90/mês",
        ciclo="mensal",
        duracao_dias=31,
        recursos=tuple(RECURSOS),
        codigos_cakto=("elite", "assinatura", "mensal"),
        beneficios=(
            "Tudo da Operação Completa",
            "Acesso enquanto a assinatura estiver ativa",
            "Novas questões e simulados a cada atualização",
            "Suporte prioritário por e-mail",
        ),
    ),
)

POR_ID = {p.id: p for p in PLANOS}
PLANO_PADRAO = "operacao"


def plano(plano_id: str) -> Plano:
    return POR_ID.get(plano_id or "", POR_ID[PLANO_PADRAO])


def tem_recurso(plano_id: str, recurso: str) -> bool:
    return recurso in plano(plano_id).recursos


def identificar(*textos: str) -> str:
    """Descobre o plano a partir do que a Cakto mandou (produto, oferta, etc.)."""
    alvo = " ".join(t.lower() for t in textos if t)
    if not alvo.strip():
        return PLANO_PADRAO
    for p in PLANOS:
        for codigo in p.codigos_cakto:
            if codigo and codigo.lower() in alvo:
                return p.id
    return PLANO_PADRAO


def nome_do_recurso(recurso: str) -> str:
    return RECURSOS.get(recurso, recurso)
