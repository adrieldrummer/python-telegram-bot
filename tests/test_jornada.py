"""Regras de desbloqueio, missões, pontos e conclusão de dia."""

from __future__ import annotations

from app import estudo, jornada
from app.config import config
from app.db import buscar_um
from app.gamificacao import estatisticas


def responder_missao(con, aluno_id, dia, acerto=True):
    questoes = jornada.questoes_da_missao(con, aluno_id, dia)
    acertos = 0
    for i, q in enumerate(questoes):
        certo = acerto or i % 3 == 0  # quando "acerto=False", erra a maioria
        letra = q.correta if certo else next(l for l, _ in q.alternativas if l != q.correta)
        resultado = estudo.responder(con, aluno_id, q, letra, origem="missao", dia=dia)
        acertos += 1 if resultado["correta"] else 0
    return acertos, len(questoes)


def test_dia_1_ja_nasce_liberado(con, aluno):
    lista = jornada.estado(con, int(aluno["id"]))
    assert lista[0]["liberado"]
    assert not lista[1]["liberado"]
    assert "Dia 1" in lista[1]["motivo"]


def test_concluir_dia_1_libera_o_dia_2(con, aluno):
    aluno_id = int(aluno["id"])
    acertos, total = responder_missao(con, aluno_id, 1)
    resultado = jornada.concluir_dia(con, aluno_id, 1, acertos, total)
    assert resultado["concluido"]
    assert resultado["proximo"] == 2
    lista = jornada.estado(con, aluno_id)
    assert lista[1]["liberado"]


def test_missao_abaixo_da_meta_nao_conclui_o_dia(con, aluno):
    aluno_id = int(aluno["id"])
    acertos, total = responder_missao(con, aluno_id, 1)
    jornada.concluir_dia(con, aluno_id, 1, acertos, total)  # dia 1 (diagnóstico) sempre fecha
    acertos, total = responder_missao(con, aluno_id, 2, acerto=False)
    resultado = jornada.concluir_dia(con, aluno_id, 2, acertos, total)
    assert not resultado["concluido"]
    assert resultado["acerto_pct"] < config.meta_acerto_missao
    assert not jornada.estado(con, aluno_id)[2]["liberado"]


def test_diagnostico_conclui_por_participacao(con, aluno):
    """O Dia 1 mede o ponto de partida — errar muito não pode travar o aluno."""
    aluno_id = int(aluno["id"])
    acertos, total = responder_missao(con, aluno_id, 1, acerto=False)
    resultado = jornada.concluir_dia(con, aluno_id, 1, acertos, total)
    assert resultado["concluido"]
    assert buscar_um(con, "SELECT diagnostico_em FROM alunos WHERE id=?", (aluno_id,))["diagnostico_em"]


def test_dia_bloqueado_nao_da_acesso(con, aluno):
    assert jornada.acesso_ao_dia(con, int(aluno["id"]), 10) is None


def test_antecipacao_exige_pontos(con, aluno):
    aluno_id = int(aluno["id"])
    acertos, total = responder_missao(con, aluno_id, 1)
    jornada.concluir_dia(con, aluno_id, 1, acertos, total)
    # o dia 2 já está liberado pelo encadeamento; forçamos o cenário do drip
    ok, mensagem = jornada.antecipar(con, aluno_id, 3)
    assert not ok
    assert "Dia 2" in mensagem


def test_prioridades_seguem_peso_e_erro(con, aluno):
    aluno_id = int(aluno["id"])
    responder_missao(con, aluno_id, 1, acerto=False)
    lista = jornada.mapa_prioridades(con, aluno_id)
    assert len(lista) == 8
    assert lista[0]["urgencia"] >= lista[-1]["urgencia"]
    assert lista[0]["prioritaria"]


def test_missao_de_prioridade_usa_materias_fracas(con, aluno):
    aluno_id = int(aluno["id"])
    acertos, total = responder_missao(con, aluno_id, 1, acerto=False)
    jornada.concluir_dia(con, aluno_id, 1, acertos, total)
    questoes = jornada.questoes_da_missao(con, aluno_id, 2)
    prioridades = set(jornada.prioridades(con, aluno_id))
    assert {q.materia for q in questoes} <= prioridades


def test_aula_lida_credita_pontos_uma_vez_so(con, aluno):
    aluno_id = int(aluno["id"])
    assert jornada.marcar_aula_lida(con, aluno_id, 1)
    pontos = buscar_um(con, "SELECT pontos FROM alunos WHERE id=?", (aluno_id,))["pontos"]
    assert not jornada.marcar_aula_lida(con, aluno_id, 1)
    assert buscar_um(con, "SELECT pontos FROM alunos WHERE id=?", (aluno_id,))["pontos"] == pontos


def test_diario_credita_uma_vez(con, aluno):
    aluno_id = int(aluno["id"])
    jornada.salvar_diario(con, aluno_id, 1, "primeiro registro")
    pontos = buscar_um(con, "SELECT pontos FROM alunos WHERE id=?", (aluno_id,))["pontos"]
    jornada.salvar_diario(con, aluno_id, 1, "editado depois")
    assert buscar_um(con, "SELECT pontos FROM alunos WHERE id=?", (aluno_id,))["pontos"] == pontos
    assert jornada.ler_diario(con, aluno_id, 1) == "editado depois"


def test_estatisticas_acompanham_as_respostas(con, aluno):
    aluno_id = int(aluno["id"])
    responder_missao(con, aluno_id, 1)
    st = estatisticas(con, aluno_id)
    assert st["respondidas"] == 24
    assert st["acerto_pct"] == 100
