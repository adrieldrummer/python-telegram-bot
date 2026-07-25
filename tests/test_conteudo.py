"""O conteúdo do curso precisa ser íntegro — gabarito errado é prejuízo direto."""

from __future__ import annotations

from conteudo import manual, simulados, trilha
from conteudo.materias import IDS as MATERIAS_IDS
from conteudo.questoes import POR_MATERIA, QUESTOES, selecionar


def test_ids_de_questoes_sao_unicos():
    ids = [q.id for q in QUESTOES]
    assert len(ids) == len(set(ids))


def test_toda_questao_tem_gabarito_valido():
    for q in QUESTOES:
        letras = [letra for letra, _ in q.alternativas]
        assert len(letras) >= 4, q.id
        assert len(letras) == len(set(letras)), q.id
        assert q.correta in letras, q.id
        assert q.comentario.strip(), q.id
        assert q.materia in MATERIAS_IDS, q.id
        assert q.nivel in {"facil", "medio", "dificil"}, q.id


def test_todas_as_materias_tem_questoes():
    for materia_id in MATERIAS_IDS:
        assert len(POR_MATERIA.get(materia_id, [])) >= 10, materia_id


def test_trilha_tem_30_dias_em_sequencia():
    numeros = [d.numero for d in trilha.DIAS]
    assert numeros == list(range(1, 31))
    for d in trilha.DIAS:
        assert d.fase in trilha.FASES_POR_ID
        assert d.aula and d.tarefas and d.missao.titulo
        assert d.missao.tipo in {"diagnostico", "questoes", "revisao", "simulado", "planejamento"}


def test_missoes_de_simulado_apontam_para_simulado_existente():
    for d in trilha.DIAS:
        if d.missao.tipo == "simulado":
            assert simulados.simulado(d.missao.simulado_id) is not None, d.numero


def test_simulados_montam_a_quantidade_prometida():
    for s in simulados.SIMULADOS:
        montado = simulados.montar(s.id)
        assert len(montado) == s.total
        assert len({q.id for q in montado}) == s.total  # sem repetição
        # montagem estável: mesma prova em toda execução
        assert [q.id for q in simulados.montar(s.id)] == [q.id for q in montado]


def test_selecao_respeita_materia_e_quantidade():
    escolhidas = selecionar(["penal"], quantidade=5, semente=1)
    assert len(escolhidas) == 5
    assert {q.materia for q in escolhidas} == {"penal"}


def test_selecao_nao_repete_questao_excluida():
    primeiras = selecionar(["portugues"], quantidade=4, semente=7)
    seguintes = selecionar(["portugues"], quantidade=4, excluir={q.id for q in primeiras}, semente=7)
    assert not ({q.id for q in primeiras} & {q.id for q in seguintes})


def test_manual_exporta_markdown_completo():
    texto = manual.markdown()
    assert "# O Mapa da Aprovação" in texto
    assert manual.NOVOS >= 5
    for capitulo in manual.CAPITULOS:
        assert capitulo.titulo in texto
