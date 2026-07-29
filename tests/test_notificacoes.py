"""Lembretes do aluno.

O ponto delicado aqui é o aviso zumbi: um lembrete que continua na tela
depois de o aluno resolver o que ele pedia. Como os avisos são derivados do
estado, e não gravados, esses testes travam justamente essa propriedade.
"""

from __future__ import annotations

from datetime import timedelta

from app import alunos as servico_alunos, estudo, notificacoes, planos as servico_planos
from app.db import buscar_um, executar, sessao
from app.security import agora, hoje_txt
from conteudo.questoes import QUESTOES
from tests.conftest import entrar


def errar(con, aluno_id, questoes, vencer=True):
    """Erra as questões e (por padrão) faz a revisão delas vencer hoje.

    A revisão espaçada agenda o primeiro retorno para o dia seguinte, então um
    erro recém-cometido não está atrasado — o cenário que interessa aqui é o do
    aluno que errou dias atrás e não voltou.
    """
    for q in questoes:
        letra = next(l for l, _ in q.alternativas if l != q.correta)
        estudo.responder(con, aluno_id, q, letra, origem="treino")
    if vencer:
        ontem = (agora() - timedelta(days=1)).strftime("%Y-%m-%d")
        executar(
            con,
            "UPDATE caderno_erros SET proxima_revisao=? WHERE aluno_id=? AND status='aberto'",
            (ontem, aluno_id),
        )


def chaves(con, aluno_id):
    return {a.chave for a in notificacoes.gerar(con, aluno_id)}


def tipos(con, aluno_id):
    return {a.chave: a.tipo for a in notificacoes.gerar(con, aluno_id)}


def test_aluno_novo_e_convidado_para_o_diagnostico(con, aluno):
    aluno_id = int(aluno["id"])
    assert "primeiro-dia" in chaves(con, aluno_id)


def test_revisao_atrasada_vira_aviso_e_some_quando_resolvida(con, aluno):
    aluno_id = int(aluno["id"])
    erradas = QUESTOES[:4]
    errar(con, aluno_id, erradas)

    atual = chaves(con, aluno_id)
    assert "revisao-4" in atual, "quatro erros deveriam gerar o aviso de revisão"

    # o aluno revisa tudo: o aviso precisa sumir sozinho
    for q in erradas:
        estudo.responder(con, aluno_id, q, q.correta, origem="revisao")
    executar(
        con,
        "UPDATE caderno_erros SET status='dominado' WHERE aluno_id=?",
        (aluno_id,),
    )
    assert not [c for c in chaves(con, aluno_id) if c.startswith("revisao-")]


def test_dispensar_esconde_o_aviso_mas_ele_volta_se_a_situacao_piorar(con, aluno):
    aluno_id = int(aluno["id"])
    errar(con, aluno_id, QUESTOES[:3])
    assert "revisao-3" in chaves(con, aluno_id)

    notificacoes.dispensar(con, aluno_id, "revisao-3")
    assert "revisao-3" not in chaves(con, aluno_id)

    # de 3 para 6 erros: a chave muda, e o aviso volta — que é o certo,
    # porque a situação não é mais a mesma que ele dispensou
    errar(con, aluno_id, QUESTOES[3:6])
    assert "revisao-6" in chaves(con, aluno_id)


def test_sequencia_em_risco_avisa_no_dia_seguinte(con, aluno):
    aluno_id = int(aluno["id"])
    ontem = (agora() - timedelta(days=1)).strftime("%Y-%m-%d")
    executar(
        con,
        "UPDATE alunos SET ultimo_dia_estudo=?, streak_atual=5 WHERE id=?",
        (ontem, aluno_id),
    )
    assert "streak-risco-5" in chaves(con, aluno_id)

    # estudou hoje: nada de aviso de sequência
    executar(
        con, "UPDATE alunos SET ultimo_dia_estudo=? WHERE id=?", (hoje_txt(), aluno_id)
    )
    assert not [c for c in chaves(con, aluno_id) if c.startswith("streak-risco")]


def test_aluno_sumido_recebe_convite_para_voltar(con, aluno):
    aluno_id = int(aluno["id"])
    faz_dias = (agora() - timedelta(days=6)).strftime("%Y-%m-%d")
    executar(
        con,
        "UPDATE alunos SET ultimo_dia_estudo=?, streak_atual=0 WHERE id=?",
        (faz_dias, aluno_id),
    )
    assert "sumido-6" in chaves(con, aluno_id)


def test_plano_vencido_avisa_e_nao_pode_ser_dispensado(con, aluno):
    aluno_id = int(aluno["id"])
    servico_planos.aplicar(con, aluno_id, "operacao")
    executar(con, "UPDATE alunos SET plano_ate='2020-01-01' WHERE id=?", (aluno_id,))

    avisos = notificacoes.gerar(con, aluno_id)
    vencido = next(a for a in avisos if a.chave == "plano-vencido")
    assert vencido.fixo, "acesso vencido não pode ser escondido pelo aluno"

    notificacoes.dispensar_todas(con, aluno_id)
    assert "plano-vencido" in chaves(con, aluno_id)


def test_prioridade_coloca_prazo_acima_de_venda(con, aluno):
    """Aviso de upgrade acima de revisão atrasada seria propaganda disfarçada."""
    aluno_id = int(aluno["id"])
    servico_planos.aplicar(con, aluno_id, "recruta")
    executar(con, "UPDATE alunos SET plano_ate='2020-01-01' WHERE id=?", (aluno_id,))
    errar(con, aluno_id, QUESTOES[:2])

    ordem = [a.chave for a in notificacoes.gerar(con, aluno_id)]
    assert ordem.index("plano-vencido") < ordem.index("revisao-2")
    # e os avisos de urgência maior vêm sempre primeiro
    urgencias = [a.urgencia for a in notificacoes.gerar(con, aluno_id)]
    assert urgencias == sorted(urgencias, reverse=True)


def test_contador_bate_com_a_lista(con, aluno):
    aluno_id = int(aluno["id"])
    assert notificacoes.contar(con, aluno_id) == len(notificacoes.gerar(con, aluno_id))


# --- pela interface --------------------------------------------------------


def criar_conta(email="aluna@teste.com", senha="blindagem30"):
    with sessao() as con:
        servico_alunos.criar(con, "Aluna Teste", email, origem="teste", senha=senha)


def test_central_de_avisos_abre_e_dispensa(cliente):
    criar_conta()
    entrar(cliente, "aluna@teste.com", "blindagem30")

    pagina = cliente.get("/avisos")
    assert pagina.status_code == 200
    assert "Comece pelo diagnóstico" in pagina.text

    resposta = cliente.post("/api/avisos/dispensar", json={"chave": "primeiro-dia"})
    assert resposta.status_code == 200
    assert resposta.json()["ok"]
    assert "Comece pelo diagnóstico" not in cliente.get("/avisos").text


def test_dispensar_sem_chave_e_recusado(cliente):
    criar_conta()
    entrar(cliente, "aluna@teste.com", "blindagem30")
    assert cliente.post("/api/avisos/dispensar", json={}).status_code == 400


def test_sino_aparece_com_contador_em_toda_tela(cliente):
    criar_conta()
    entrar(cliente, "aluna@teste.com", "blindagem30")
    for caminho in ("/painel", "/questoes", "/erros"):
        html = cliente.get(caminho).text
        assert 'class="sino' in html, caminho
        assert "sino-contador" in html, caminho

    # visitante não tem sino
    cliente.post("/sair", data={"csrf_token": cliente.cookies.get("map_csrf")})
    assert "sino-contador" not in cliente.get("/").text
