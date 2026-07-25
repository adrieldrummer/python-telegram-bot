"""Caderno de erros e revisão espaçada."""

from __future__ import annotations

from app import estudo, srs
from app.db import buscar_um, executar
from conteudo.questoes import QUESTOES

Q1 = QUESTOES[0]
Q2 = QUESTOES[1]


def errar(con, aluno_id, questao=Q1):
    letra = next(l for l, _ in questao.alternativas if l != questao.correta)
    return estudo.responder(con, aluno_id, questao, letra, origem="treino")


def acertar(con, aluno_id, questao=Q1):
    return estudo.responder(con, aluno_id, questao, questao.correta, origem="treino")


def test_erro_entra_no_caderno(con, aluno):
    aluno_id = int(aluno["id"])
    resultado = errar(con, aluno_id)
    assert not resultado["correta"]
    resumo = srs.resumo(con, aluno_id)
    assert resumo["abertos"] == 1


def test_acerto_nao_entra_no_caderno(con, aluno):
    aluno_id = int(aluno["id"])
    acertar(con, aluno_id)
    assert srs.resumo(con, aluno_id)["abertos"] == 0


def test_tres_acertos_seguidos_dominam_a_questao(con, aluno):
    aluno_id = int(aluno["id"])
    errar(con, aluno_id)
    for _ in range(2):
        resultado = acertar(con, aluno_id)
        assert not resultado["dominada"]
    resultado = acertar(con, aluno_id)
    assert resultado["dominada"]
    resumo = srs.resumo(con, aluno_id)
    assert resumo["abertos"] == 0 and resumo["dominados"] == 1


def test_errar_de_novo_reinicia_o_ciclo(con, aluno):
    aluno_id = int(aluno["id"])
    errar(con, aluno_id)
    acertar(con, aluno_id)
    errar(con, aluno_id)
    linha = buscar_um(
        con, "SELECT nivel_srs, acertos_seguidos FROM caderno_erros WHERE aluno_id=?", (aluno_id,)
    )
    assert linha["nivel_srs"] == 0
    assert linha["acertos_seguidos"] == 0


def test_intervalos_crescem_a_cada_acerto(con, aluno):
    aluno_id = int(aluno["id"])
    errar(con, aluno_id)
    primeira = buscar_um(con, "SELECT proxima_revisao FROM caderno_erros WHERE aluno_id=?", (aluno_id,))
    acertar(con, aluno_id)
    segunda = buscar_um(con, "SELECT proxima_revisao FROM caderno_erros WHERE aluno_id=?", (aluno_id,))
    assert segunda["proxima_revisao"] > primeira["proxima_revisao"]


def test_apenas_questoes_vencidas_aparecem_na_revisao(con, aluno):
    aluno_id = int(aluno["id"])
    errar(con, aluno_id)
    assert srs.vencidas(con, aluno_id) == []          # volta só amanhã
    executar(
        con,
        "UPDATE caderno_erros SET proxima_revisao='2020-01-01' WHERE aluno_id=?",
        (aluno_id,),
    )
    assert len(srs.vencidas(con, aluno_id)) == 1


def test_classificacao_de_erro_credita_pontos(con, aluno):
    aluno_id = int(aluno["id"])
    errar(con, aluno_id)
    antes = buscar_um(con, "SELECT pontos FROM alunos WHERE id=?", (aluno_id,))["pontos"]
    resultado = estudo.classificar_erro(con, aluno_id, Q1.id, "pegadinha", "confundi o comando")
    assert resultado["ok"] and resultado["pontos"] > 0
    depois = buscar_um(con, "SELECT pontos FROM alunos WHERE id=?", (aluno_id,))["pontos"]
    # a primeira classificação também desbloqueia a medalha "Erro Vira Aula"
    bonus_medalhas = sum(m["pontos"] for m in resultado["medalhas"])
    assert depois == antes + resultado["pontos"] + bonus_medalhas


def test_categoria_invalida_e_recusada(con, aluno):
    aluno_id = int(aluno["id"])
    errar(con, aluno_id)
    assert not estudo.classificar_erro(con, aluno_id, Q1.id, "inventada", "")["ok"]


def test_resumo_aponta_categoria_dominante(con, aluno):
    aluno_id = int(aluno["id"])
    errar(con, aluno_id, Q1)
    errar(con, aluno_id, Q2)
    estudo.classificar_erro(con, aluno_id, Q1.id, "desatencao", "")
    estudo.classificar_erro(con, aluno_id, Q2.id, "desatencao", "")
    assert srs.resumo(con, aluno_id)["categoria_dominante"] == "desatencao"
