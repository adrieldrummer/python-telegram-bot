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


def test_narrativa_visual_e_consistente():
    """As imagens contam uma história, e cada uma tem um significado só.

    Se duas etapas da jornada usarem a mesma arte, o aluno para de ler a
    imagem como informação — que é exatamente o que ela deveria ser aqui.
    """
    from conteudo import CAPAS, NARRATIVA

    assert len(NARRATIVA) >= 5
    capas = [m.capa for m in NARRATIVA]
    assert len(capas) == len(set(capas)), "duas etapas dividindo a mesma imagem"
    for m in NARRATIVA:
        assert m.capa in CAPAS, m.id
        assert m.rotulo and m.titulo and m.legenda, m.id
    # a história começa no aluno de hoje e termina na carreira
    assert NARRATIVA[0].id == "hoje"
    assert NARRATIVA[-1].id == "farda"


def test_toda_capa_do_catalogo_aponta_para_arquivo_existente():
    """Capa quebrada só aparece em produção — a menos que um teste olhe."""
    from pathlib import Path

    from conteudo import CAPAS

    estaticos = Path(__file__).resolve().parent.parent / "app" / "static"
    for chave, url in CAPAS.items():
        arquivo = estaticos / url.removeprefix("/static/")
        assert arquivo.exists(), f"{chave} aponta para {url}, que não existe"


def test_gabarito_e_equilibrado_entre_as_cinco_letras():
    """Banco viciado em uma letra ensina o aluno a chutar errado.

    Em 30/11/2025 a VUNESP distribuiu as respostas de forma quase uniforme
    (A 18%, B 23%, C 18%, D 18%, E 22%). Um banco com metade dos gabaritos em
    B treina o reflexo de "na dúvida, marque B" — que é exatamente o hábito que
    derruba o candidato na prova de verdade.
    """
    from collections import Counter

    from conteudo.questoes import POR_MATERIA, QUESTOES

    total = len(QUESTOES)
    contagem = Counter(q.correta for q in QUESTOES)
    assert set(contagem) == set("ABCDE"), "alguma letra não aparece como gabarito"
    for letra in "ABCDE":
        fatia = contagem[letra] / total
        assert 0.12 <= fatia <= 0.28, (
            f"letra {letra} responde por {fatia:.0%} dos gabaritos — o banco está viciado"
        )

    # e nenhuma matéria pode concentrar mais da metade numa letra só
    for materia, lista in POR_MATERIA.items():
        c = Counter(q.correta for q in lista)
        letra, quantas = c.most_common(1)[0]
        assert quantas <= len(lista) * 0.45, (
            f"{materia}: {quantas} de {len(lista)} gabaritos em {letra}"
        )


def test_toda_questao_tem_cinco_alternativas_como_a_prova_real():
    from conteudo.edital import ALTERNATIVAS_POR_QUESTAO
    from conteudo.questoes import QUESTOES

    assert ALTERNATIVAS_POR_QUESTAO == 5
    for q in QUESTOES:
        assert len(q.alternativas) == 5, q.id
        assert [l for l, _ in q.alternativas] == list("ABCDE"), q.id
