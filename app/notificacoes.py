"""Notificações e lembretes do aluno.

Elas são **derivadas**, não armazenadas: a cada carregamento a plataforma olha
o estado real do aluno e monta a lista. Guardar notificação em tabela cria o
problema clássico de aviso zumbi — "você tem 3 revisões atrasadas" continua
aparecendo depois de o aluno revisar as três.

O que fica guardado é só o que ele já dispensou (`notificacoes_lidas`), pela
chave do aviso. Se a condição voltar a valer com outro número — de 3 revisões
para 12 —, a chave muda e o aviso reaparece, que é o comportamento certo.

Ordem de prioridade: o que tem prazo primeiro, o que constrói hábito depois,
o que vende por último. Aviso de upgrade acima de revisão atrasada seria
propaganda disfarçada de ajuda.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import timedelta
from typing import Optional

from conteudo import edital, trilha

from . import planos as servico_planos, srs
from .db import buscar_todos, executar, valor
from .security import agora, hoje_txt, ler_data

# marcos da contagem regressiva que merecem um aviso — mais perto da prova,
# mais frequente, porque a decisão do aluno muda de peso
MARCOS_PROVA = (90, 60, 45, 30, 21, 14, 7, 3, 1)
MARCOS_INSCRICAO = (30, 15, 7, 3, 1)


@dataclass(frozen=True)
class Aviso:
    chave: str          # identidade estável; muda quando o conteúdo muda
    tipo: str           # prazo | habito | estudo | plano | conquista
    icone: str
    titulo: str
    texto: str
    url: str = ""
    acao: str = ""
    urgencia: int = 0   # maior = mais para cima
    fixo: bool = False  # não pode ser dispensado enquanto valer


def _dispensadas(con: sqlite3.Connection, aluno_id: int) -> set[str]:
    return {
        linha["chave"]
        for linha in buscar_todos(
            con, "SELECT chave FROM notificacoes_lidas WHERE aluno_id = ?", (aluno_id,)
        )
    }


def dispensar(con: sqlite3.Connection, aluno_id: int, chave: str) -> None:
    executar(
        con,
        "INSERT OR IGNORE INTO notificacoes_lidas (aluno_id, chave) VALUES (?,?)",
        (aluno_id, chave[:120]),
    )


def dispensar_todas(con: sqlite3.Connection, aluno_id: int) -> int:
    avisos = gerar(con, aluno_id, incluir_dispensadas=True)
    for a in avisos:
        if not a.fixo:
            dispensar(con, aluno_id, a.chave)
    return len(avisos)


def _valor(aluno, campo: str, padrao=None):
    try:
        return aluno[campo]
    except (KeyError, IndexError, TypeError):
        return padrao


def _prazo_da_prova() -> list[Aviso]:
    dias = edital.dias_para_prova()
    avisos: list[Aviso] = []

    if dias > 0:
        marco = next((m for m in MARCOS_PROVA if dias == m), None)
        if marco is not None:
            avisos.append(
                Aviso(
                    chave=f"prova-{marco}",
                    tipo="prazo",
                    icone="🎯",
                    titulo=f"Faltam {marco} dias para a prova",
                    texto=(
                        "Hoje é um bom dia para conferir onde você está: abra o mapa de "
                        "prioridades e ataque a matéria mais fraca."
                        if marco > 14
                        else "Reta final: nada de conteúdo novo. Questão, erro e revisão."
                    ),
                    url="/painel",
                    acao="Ver meu progresso",
                    urgencia=90 - marco,
                )
            )
    elif dias == 0:
        avisos.append(
            Aviso(
                chave="prova-hoje",
                tipo="prazo",
                icone="🚨",
                titulo="É hoje",
                texto="Documento com foto, comprovante, caneta preta. Boa prova.",
                urgencia=100,
                fixo=True,
            )
        )

    dias_inscricao = edital.dias_para_inscricao()
    if 0 < dias_inscricao and dias_inscricao in MARCOS_INSCRICAO:
        avisos.append(
            Aviso(
                chave=f"inscricao-{dias_inscricao}",
                tipo="prazo",
                icone="📋",
                titulo=f"Inscrições encerram em {dias_inscricao} dia(s)",
                texto=(
                    "Estudar sem se inscrever não vale nada. Confira sua inscrição no "
                    "site da banca."
                ),
                urgencia=95,
            )
        )
    return avisos


def _habito(con: sqlite3.Connection, aluno) -> list[Aviso]:
    aluno_id = int(_valor(aluno, "id", 0))
    avisos: list[Aviso] = []

    ultimo = (_valor(aluno, "ultimo_dia_estudo") or "").strip()
    streak = int(_valor(aluno, "streak_atual") or 0)
    hoje = hoje_txt()
    ontem = (agora() - timedelta(days=1)).strftime("%Y-%m-%d")

    if ultimo and ultimo != hoje:
        if ultimo == ontem and streak >= 2:
            # a sequência ainda está viva, mas cai na virada do dia
            avisos.append(
                Aviso(
                    chave=f"streak-risco-{streak}",
                    tipo="habito",
                    icone="🔥",
                    titulo=f"Sua sequência de {streak} dias acaba hoje",
                    texto="Uma questão já mantém a sequência viva. Não precisa ser um bloco inteiro.",
                    url="/questoes",
                    acao="Responder uma questão",
                    urgencia=70,
                )
            )
        else:
            data_ultimo = ler_data(ultimo)
            parado = (agora().date() - data_ultimo.date()).days if data_ultimo else 0
            if parado >= 2:
                avisos.append(
                    Aviso(
                        chave=f"sumido-{min(parado, 30)}",
                        tipo="habito",
                        icone="👋",
                        titulo=f"{parado} dias sem estudar",
                        texto=(
                            "Voltar custa menos do que parece: 10 questões hoje e você já "
                            "está de volta ao ritmo."
                        ),
                        url="/questoes",
                        acao="Voltar agora",
                        urgencia=60,
                    )
                )

    if not ultimo:
        avisos.append(
            Aviso(
                chave="primeiro-dia",
                tipo="habito",
                icone="🚀",
                titulo="Comece pelo diagnóstico",
                texto=(
                    "20 questões de todo o edital. Errar aqui é esperado — o resultado é "
                    "o que monta o seu mapa de prioridades."
                ),
                url="/dia/1",
                acao="Abrir o Dia 1",
                urgencia=80,
            )
        )
    return avisos


def _estudo(con: sqlite3.Connection, aluno) -> list[Aviso]:
    aluno_id = int(_valor(aluno, "id", 0))
    avisos: list[Aviso] = []

    atrasadas = srs.total_vencidas(con, aluno_id)
    if atrasadas:
        avisos.append(
            Aviso(
                chave=f"revisao-{atrasadas}",
                tipo="estudo",
                icone="📓",
                titulo=f"{atrasadas} revisão(ões) na fila",
                texto=(
                    "A revisão espaçada é o que impede você de errar duas vezes pelo "
                    "mesmo motivo."
                ),
                url="/erros/revisar",
                acao="Revisar agora",
                urgencia=65 + min(atrasadas, 20),
            )
        )

    nao_classificados = int(
        valor(
            con,
            "SELECT COUNT(*) FROM caderno_erros WHERE aluno_id=? AND status='aberto' AND categoria=''",
            (aluno_id,),
        )
    )
    if nao_classificados >= 5:
        avisos.append(
            Aviso(
                chave=f"classificar-{nao_classificados}",
                tipo="estudo",
                icone="🏷",
                titulo=f"{nao_classificados} erros sem classificação",
                texto=(
                    "Falta de conteúdo, pegadinha ou desatenção pedem remédios "
                    "diferentes — e cada classificação vale 8 pontos."
                ),
                url="/erros",
                acao="Classificar",
                urgencia=40,
            )
        )
    return avisos


def _plano(con: sqlite3.Connection, aluno) -> list[Aviso]:
    avisos: list[Aviso] = []
    resumo = servico_planos.resumo(aluno)

    if resumo["vencido"]:
        avisos.append(
            Aviso(
                chave="plano-vencido",
                tipo="plano",
                icone="🔒",
                titulo="Seu acesso venceu",
                texto=(
                    "Seu progresso, seus pontos e seu caderno de erros continuam salvos. "
                    "Renove para voltar de onde parou."
                ),
                url="/planos",
                acao="Renovar",
                urgencia=98,
                fixo=True,
            )
        )
    else:
        dias = resumo["dias_restantes"]
        if dias is not None and 0 <= dias <= 5:
            avisos.append(
                Aviso(
                    chave=f"plano-vence-{dias}",
                    tipo="plano",
                    icone="⏳",
                    titulo=f"Seu acesso vence em {dias} dia(s)",
                    texto="Renove antes para não perder o ritmo na reta final.",
                    url="/planos",
                    acao="Renovar",
                    urgencia=75,
                )
            )

    saldo = servico_planos.saldo_de_questoes(con, aluno)
    if saldo["limitado"] and saldo["esgotado"]:
        avisos.append(
            Aviso(
                chave="limite-diario",
                tipo="plano",
                icone="📊",
                titulo="Limite de questões de hoje atingido",
                texto=(
                    f"Seu plano permite {saldo['limite']} por dia. Ele reabre amanhã — "
                    "ou some de vez com o upgrade."
                ),
                url="/planos",
                acao="Treinar sem limite",
                urgencia=30,
            )
        )
    return avisos


def _progresso(con: sqlite3.Connection, aluno) -> list[Aviso]:
    aluno_id = int(_valor(aluno, "id", 0))
    avisos: list[Aviso] = []

    concluidos = int(
        valor(
            con,
            "SELECT COUNT(*) FROM progresso_dias WHERE aluno_id=? AND status='concluido'",
            (aluno_id,),
        )
    )
    if concluidos >= trilha.TOTAL_DIAS:
        feitos = int(
            valor(
                con,
                "SELECT COUNT(*) FROM simulados_sessoes WHERE aluno_id=? AND finalizado_em IS NOT NULL",
                (aluno_id,),
            )
        )
        if feitos == 0 and servico_planos.tem_recurso(aluno, "simulados"):
            avisos.append(
                Aviso(
                    chave="sem-simulado",
                    tipo="estudo",
                    icone="⏱",
                    titulo="Você ainda não fez um simulado completo",
                    texto=(
                        "Trilha concluída. Agora o que mais devolve ponto é medir-se em "
                        "60 questões com cronômetro."
                    ),
                    url="/simulados",
                    acao="Fazer um simulado",
                    urgencia=55,
                )
            )
    return avisos


def gerar(
    con: sqlite3.Connection, aluno_id: int, incluir_dispensadas: bool = False
) -> list[Aviso]:
    """Monta a lista de avisos válidos para este aluno, agora."""
    from .db import buscar_um

    aluno = buscar_um(con, "SELECT * FROM alunos WHERE id = ?", (aluno_id,))
    if aluno is None:
        return []

    avisos: list[Aviso] = []
    avisos.extend(_prazo_da_prova())
    avisos.extend(_habito(con, aluno))
    avisos.extend(_estudo(con, aluno))
    avisos.extend(_plano(con, aluno))
    avisos.extend(_progresso(con, aluno))

    if not incluir_dispensadas:
        vistas = _dispensadas(con, aluno_id)
        avisos = [a for a in avisos if a.fixo or a.chave not in vistas]

    avisos.sort(key=lambda a: (-a.urgencia, a.chave))
    return avisos


def contar(con: sqlite3.Connection, aluno_id: int) -> int:
    return len(gerar(con, aluno_id))


__all__ = ["Aviso", "contar", "dispensar", "dispensar_todas", "gerar"]
