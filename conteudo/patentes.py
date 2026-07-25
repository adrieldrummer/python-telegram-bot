"""Pontos de estudo → patentes e medalhas."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Patente:
    id: str
    nome: str
    pontos: int
    insignia: str
    lema: str


PATENTES: tuple[Patente, ...] = (
    Patente("recruta", "Recruta", 0, "▫", "Todo aprovado começou aqui."),
    Patente("aluno", "Aluno-Soldado", 250, "▪", "Você provou que consegue manter o ritmo."),
    Patente("sd2", "Soldado 2ª Classe", 700, "★", "A patente do seu objetivo. Agora é treino."),
    Patente("sd1", "Soldado 1ª Classe", 1400, "★★", "Consistência virou hábito."),
    Patente("cabo", "Cabo", 2300, "★★★", "Você já responde melhor do que 80% dos candidatos."),
    Patente("sgt3", "3º Sargento", 3400, "◆", "Constância de quem faz simulado sem medo."),
    Patente("sgt2", "2º Sargento", 4800, "◆◆", "Erro virou dado, e dado virou plano."),
    Patente("sgt1", "1º Sargento", 6500, "◆◆◆", "Poucos chegam aqui — e eles passam."),
    Patente("subten", "Subtenente", 9000, "❖", "Você terminou o mapa inteiro. Vá buscar a farda."),
)


def patente_de(pontos: int) -> Patente:
    atual = PATENTES[0]
    for p in PATENTES:
        if pontos >= p.pontos:
            atual = p
    return atual


def proxima_patente(pontos: int):
    for p in PATENTES:
        if pontos < p.pontos:
            return p
    return None


def progresso_patente(pontos: int) -> int:
    """Percentual (0-100) até a próxima patente."""
    atual = patente_de(pontos)
    prox = proxima_patente(pontos)
    if prox is None:
        return 100
    faixa = prox.pontos - atual.pontos
    if faixa <= 0:
        return 100
    return max(0, min(100, round((pontos - atual.pontos) * 100 / faixa)))


@dataclass(frozen=True)
class Medalha:
    id: str
    nome: str
    icone: str
    descricao: str
    pontos: int = 0


MEDALHAS: tuple[Medalha, ...] = (
    Medalha("diagnostico", "Mapa Aberto", "🧭", "Concluiu o diagnóstico e conheceu suas prioridades reais.", 50),
    Medalha("primeira_missao", "Primeiro Tiro", "🎯", "Completou a primeira missão diária.", 20),
    Medalha("streak3", "Três Dias de Pé", "🔥", "Três dias seguidos de estudo.", 30),
    Medalha("streak7", "Semana Blindada", "🛡", "Sete dias seguidos sem furar o bloco.", 80),
    Medalha("streak15", "Meio Mapa Sem Falhar", "⚡", "Quinze dias seguidos de constância.", 150),
    Medalha("streak30", "Constância de Farda", "🏅", "Trinta dias seguidos. Isso é raro.", 300),
    Medalha("q100", "Cem Questões", "💯", "Respondeu 100 questões na plataforma.", 60),
    Medalha("q300", "Trezentas Questões", "🔢", "Respondeu 300 questões.", 120),
    Medalha("q600", "Máquina de Questões", "⚙", "Respondeu 600 questões.", 250),
    Medalha("erro_categorizado", "Erro Vira Aula", "📓", "Classificou o primeiro erro no Caderno de Erros.", 25),
    Medalha("erros_dominados10", "Dez Erros Domados", "🧠", "Dominou 10 questões que você errava.", 100),
    Medalha("simulado1", "Primeiro Simulado", "⏱", "Fez o primeiro simulado cronometrado.", 80),
    Medalha("simulado3", "Sangue Frio", "❄", "Concluiu três simulados completos.", 200),
    Medalha("nota70", "Zona de Aprovação", "📈", "Atingiu 70% de acerto em um simulado.", 180),
    Medalha("madrugador", "Bloco da Manhã", "🌅", "Estudou antes das 7h da manhã.", 40),
    Medalha("coruja", "Turno da Noite", "🌙", "Estudou depois das 22h — depois dos filhos dormirem.", 40),
    Medalha("fase1", "Fase 1 Concluída", "1️⃣", "Diagnóstico e priorização finalizados.", 70),
    Medalha("fase2", "Fase 2 Concluída", "2️⃣", "Imersão em questões finalizada.", 120),
    Medalha("fase3", "Fase 3 Concluída", "3️⃣", "Simulados e ajuste fino finalizados.", 160),
    Medalha("fase4", "Mapa Completo", "🏁", "Trinta dias concluídos. Você fez o percurso inteiro.", 400),
)

MEDALHAS_POR_ID = {m.id: m for m in MEDALHAS}
