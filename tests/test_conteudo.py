"""O conteúdo do curso precisa ser íntegro — gabarito errado é prejuízo direto."""

from __future__ import annotations

from conteudo import edital, manual, modulos, planos, simulados, trilha
from conteudo.materias import IDS as MATERIAS_IDS
from conteudo.materias import POR_ID as MATERIAS_POR_ID
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


def test_materias_espelham_a_prova_objetiva():
    """O peso de cada matéria é o número de questões que ela vale na prova."""
    assert {m for m, _, _ in edital.PROVA_OBJETIVA} == set(MATERIAS_IDS)
    for chave, _, quantidade in edital.PROVA_OBJETIVA:
        assert MATERIAS_POR_ID[chave].peso == quantidade, chave
    assert edital.TOTAL_QUESTOES_PROVA == 60


def test_trilha_cobre_o_edital_em_sete_dias():
    numeros = [d.numero for d in trilha.DIAS]
    assert numeros == list(range(1, trilha.TOTAL_DIAS + 1))
    assert trilha.TOTAL_DIAS == 7
    for d in trilha.DIAS:
        assert d.fase in trilha.FASES_POR_ID
        assert d.aula and d.tarefas and d.missao.titulo
        assert d.missao.tipo in {"diagnostico", "questoes", "revisao", "simulado", "planejamento"}


def test_fases_cobrem_todos_os_dias_sem_buraco():
    cobertos: list[int] = []
    for f in trilha.FASES:
        cobertos.extend(range(f.dia_inicial, f.dia_final + 1))
    assert sorted(cobertos) == list(range(1, trilha.TOTAL_DIAS + 1))


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


def test_simulado_oficial_respeita_a_distribuicao_do_edital():
    for s in simulados.SIMULADOS:
        if not s.oficial:
            continue
        montado = simulados.montar(s.id)
        assert len(montado) == edital.TOTAL_QUESTOES_PROVA, s.id
        for chave, _, quantidade in edital.PROVA_OBJETIVA:
            achadas = sum(1 for q in montado if q.materia == chave)
            assert achadas == quantidade, f"{s.id}/{chave}"


def test_selecao_respeita_materia_e_quantidade():
    escolhidas = selecionar(["portugues"], quantidade=5, semente=1)
    assert len(escolhidas) == 5
    assert {q.materia for q in escolhidas} == {"portugues"}


def test_selecao_nao_repete_questao_excluida():
    primeiras = selecionar(["portugues"], quantidade=4, semente=7)
    seguintes = selecionar(["portugues"], quantidade=4, excluir={q.id for q in primeiras}, semente=7)
    assert not ({q.id for q in primeiras} & {q.id for q in seguintes})


def test_manual_exporta_markdown_completo():
    texto = manual.markdown()
    assert "Edital PM-SP 2026" in texto
    assert manual.TOTAL_CAPITULOS == trilha.TOTAL_DIAS + 2  # abertura + dias + fechamento
    for capitulo in manual.CAPITULOS:
        assert capitulo.titulo in texto


def test_modulos_avancados_exigem_recurso_de_plano():
    assert modulos.MODULOS
    for m in modulos.MODULOS:
        assert m.recurso in planos.RECURSOS, m.id
        assert m.aulas, m.id
        assert not planos.tem_recurso(planos.PLANO_ENTRADA, m.recurso), m.id
        for materia_id in m.materias:
            assert materia_id in MATERIAS_IDS, m.id


def test_edital_nao_promete_data_no_passado():
    """Guarda-chuva contra conteúdo desatualizado silenciosamente."""
    assert edital.FIM_INSCRICOES < edital.DATA_PROVA
