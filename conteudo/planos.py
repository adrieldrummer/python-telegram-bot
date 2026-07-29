"""Planos e o que cada um libera.

Modelo de entrada baixa: R$ 47/mês dá acesso à trilha de 7 dias, ao banco de
questões e ao caderno de erros — o suficiente para o aluno entender o edital e
começar a treinar. O que decide aprovação depois disso (redação, TAF, etapas
eliminatórias, simulados completos e aprofundamentos) fica nos planos
superiores.

Um plano é um conjunto de **recursos**. As telas perguntam "tem o recurso X?" —
nunca "é do plano Y". Assim, criar oferta ou promoção não mexe em nenhuma tela.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

# --- recursos disponíveis --------------------------------------------------

RECURSOS = {
    "trilha": "Trilha de 7 dias explicando o edital inteiro",
    "questoes": "Banco de questões comentadas",
    "erros": "Caderno de Erros com revisão espaçada",
    "simulados": "Simulados oficiais de 60 questões",
    "avancado": "Módulos avançados (redação, TAF, etapas e aprofundamentos)",
    "manual": "Apostila completa em formato de leitura e download",
    "certificado": "Certificado de conclusão",
    "ranking": "Ranking da turma",
    "atualidades": "Boletim de atualidades até o dia da prova",
    "suporte": "Suporte prioritário por e-mail",
}

# limites do plano de entrada — o aluno usa a plataforma inteira, com teto diário
LIMITE_QUESTOES_DIA_PADRAO = 30


# Links de checkout da Cakto. Ficam aqui, versionados, porque são endereços
# públicos — vão para a página de vendas de qualquer forma. Um link por plano:
# a Cakto identifica o produto pelo link, e é o que faz o webhook devolver a
# oferta certa. `app.planos.checkout_do_plano` ainda permite sobrescrever por
# variável de ambiente (CAKTO_CHECKOUT_<PLANO>) sem tocar no código.


@dataclass(frozen=True)
class Plano:
    id: str
    nome: str
    chamada: str
    preco: str
    valor: float
    preco_de: str = ""
    ciclo: str = "mensal"
    duracao_dias: int = 31
    recursos: tuple[str, ...] = ()
    limite_questoes_dia: int = 0  # 0 = sem limite
    destaque: bool = False
    checkout_url: str = ""
    codigos_cakto: tuple[str, ...] = ()
    beneficios: tuple[str, ...] = field(default_factory=tuple)
    para_quem: str = ""


PLANOS: tuple[Plano, ...] = (
    Plano(
        id="recruta",
        nome="Recruta",
        chamada="Entenda o edital inteiro em 7 dias e comece a treinar hoje.",
        preco="R$ 47/mês",
        valor=47.0,
        ciclo="mensal",
        duracao_dias=31,
        recursos=("trilha", "questoes", "erros"),
        limite_questoes_dia=LIMITE_QUESTOES_DIA_PADRAO,
        checkout_url="https://pay.cakto.com.br/3b55ibi_1009316",
        codigos_cakto=("recruta", "mensal", "47"),
        para_quem="Para quem está começando e precisa entender o que estudar.",
        beneficios=(
            "Trilha de 7 dias explicando cada tópico do edital",
            "Banco de questões comentadas, com correção ativa",
            "Caderno de Erros com revisão espaçada automática",
            "Simulado diagnóstico de 20 questões",
            f"Até {LIMITE_QUESTOES_DIA_PADRAO} questões por dia",
        ),
    ),
    Plano(
        id="operacao",
        nome="Operação Completa",
        chamada="Tudo o que decide a vaga: simulados oficiais e módulos avançados.",
        preco="R$ 97/mês",
        valor=97.0,
        preco_de="R$ 147/mês",
        ciclo="mensal",
        duracao_dias=31,
        recursos=(
            "trilha",
            "questoes",
            "erros",
            "simulados",
            "avancado",
            "manual",
            "certificado",
            "ranking",
        ),
        destaque=True,
        checkout_url="https://pay.cakto.com.br/yqm8hs9",
        codigos_cakto=("operacao", "completa", "completo", "97"),
        para_quem="Para quem vai fazer a prova de 20 de setembro e quer chegar pronto.",
        beneficios=(
            "Tudo do plano Recruta, sem limite diário de questões",
            "Simulados oficiais de 60 questões, no formato da VUNESP",
            "Módulos avançados: redação, TAF e etapas eliminatórias",
            "Aprofundamento de Português e Matemática",
            "Apostila completa para download e certificado de conclusão",
        ),
    ),
    Plano(
        id="elite",
        nome="Elite",
        chamada="Acompanhamento até o dia da prova — e depois dela.",
        preco="R$ 197/mês",
        valor=197.0,
        ciclo="mensal",
        duracao_dias=31,
        recursos=tuple(RECURSOS),
        checkout_url="https://pay.cakto.com.br/y8zqtwu",
        codigos_cakto=("elite", "197", "vip"),
        para_quem="Para quem quer preparação completa, incluindo as etapas pós-objetiva.",
        beneficios=(
            "Tudo da Operação Completa",
            "Boletim de atualidades toda semana até a prova",
            "Novos simulados e questões a cada atualização",
            "Suporte prioritário por e-mail",
            "Acesso mantido durante todas as etapas do concurso",
        ),
    ),
)

POR_ID = {p.id: p for p in PLANOS}
PLANO_PADRAO = "recruta"
PLANO_ENTRADA = "recruta"


def plano(plano_id: str) -> Plano:
    return POR_ID.get(plano_id or "", POR_ID[PLANO_PADRAO])


def tem_recurso(plano_id: str, recurso: str) -> bool:
    return recurso in plano(plano_id).recursos


def limite_diario(plano_id: str) -> int:
    return plano(plano_id).limite_questoes_dia


def identificar(*textos: str) -> str:
    """Descobre o plano pelo que a Cakto mandou: produto, oferta ou checkout.

    O link do checkout é conferido primeiro porque é o identificador mais
    estável — o vendedor renomeia produto e oferta quando quiser, mas o link
    é o que ele divulgou e não muda sem trocar a campanha inteira.
    """
    return identificar_ou_nada(*textos) or PLANO_PADRAO


def _slugs(url: str) -> tuple[str, ...]:
    """Identificadores extraíveis de um link de checkout.

    Os três planos são três ofertas do mesmo produto na Cakto, então o nome do
    produto chega igual nas três vendas: o link é o único campo que diz qual
    oferta foi comprada. Só que ele nem sempre volta idêntico ao divulgado —
    pode vir sem o sufixo da oferta, com barra no fim ou com parâmetros de
    campanha grudados. Comparar a URL inteira falharia em todos esses casos, e
    falhar aqui é liberar o plano errado numa venda de verdade.
    """
    caminho = url.lower().split("?")[0].split("#")[0].rstrip("/")
    slug = caminho.rsplit("/", 1)[-1]
    if not slug:
        return ()
    base = slug.split("_")[0]
    return (slug,) if base == slug else (slug, base)


def _casa_codigo(codigo: str, alvo: str) -> bool:
    """Código puramente numérico só casa como palavra inteira.

    "47" solto casaria dentro de "1470" ou do id de uma oferta como "B47xyz" —
    e aí uma venda de Elite viraria Recruta por acidente de substring.
    """
    codigo = (codigo or "").lower()
    if not codigo:
        return False
    if codigo.isdigit():
        return re.search(rf"\b{re.escape(codigo)}\b", alvo) is not None
    return codigo in alvo


def identificar_ou_nada(*textos: str) -> str:
    """Como `identificar`, mas devolve string vazia quando nada casa.

    A diferença importa: `identificar` devolve o plano padrão quando não
    reconhece nada, e o padrão é justamente o plano de entrada. Quem precisa
    saber se houve reconhecimento de verdade — para só então tentar pelo valor
    pago — não consegue distinguir "achei recruta" de "não achei nada".
    """
    alvo = " ".join(t.lower() for t in textos if t)
    if not alvo.strip():
        return ""

    # do slug mais específico para o mais genérico: se um dia dois planos
    # compartilharem o prefixo do link, casar pelo pedaço curto primeiro
    # devolveria o plano errado
    candidatos = [(slug, p.id) for p in PLANOS for slug in _slugs(p.checkout_url)]
    candidatos.sort(key=lambda item: -len(item[0]))
    for slug, plano_id in candidatos:
        if slug in alvo:
            return plano_id

    for p in PLANOS:
        for codigo in p.codigos_cakto:
            if _casa_codigo(codigo, alvo):
                return p.id
    return ""


def identificar_por_valor(valor: float) -> str:
    """Fallback quando o nome do produto não diz nada: casa pelo valor pago."""
    if valor <= 0:
        return PLANO_PADRAO
    mais_proximo = min(PLANOS, key=lambda p: abs(p.valor - valor))
    return mais_proximo.id if abs(mais_proximo.valor - valor) <= 20 else PLANO_PADRAO


def nome_do_recurso(recurso: str) -> str:
    return RECURSOS.get(recurso, recurso)


def planos_com(recurso: str) -> list[Plano]:
    return [p for p in PLANOS if recurso in p.recursos]
