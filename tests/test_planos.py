"""Planos, assinaturas e liberação de recursos."""

from __future__ import annotations

import json

from app import planos as servico
from app.db import buscar_um, executar, sessao
from app.security import assinatura_hmac
from conteudo import planos as catalogo
from tests.conftest import entrar
from tests.test_webhook import SEGREDO, com_segredo, payload_compra


def test_identificacao_por_nome_do_produto():
    assert catalogo.identificar("Operação Aprovação — plano Elite", "") == "elite"
    assert catalogo.identificar("", "oferta recruta") == "recruta"
    assert catalogo.identificar("qualquer coisa", "") == catalogo.PLANO_PADRAO


def test_recursos_crescem_com_o_plano():
    recruta = set(catalogo.plano("recruta").recursos)
    operacao = set(catalogo.plano("operacao").recursos)
    elite = set(catalogo.plano("elite").recursos)
    assert recruta < operacao < elite
    assert "simulados" not in recruta and "simulados" in operacao


def test_aplicar_plano_define_validade_e_assinatura(con, aluno):
    aluno_id = int(aluno["id"])
    plano = servico.aplicar(con, aluno_id, "operacao", "tx-1")
    assert plano.id == "operacao"
    atualizado = buscar_um(con, "SELECT plano, plano_ate FROM alunos WHERE id=?", (aluno_id,))
    assert atualizado["plano"] == "operacao"
    assert atualizado["plano_ate"]  # tem data de expiração
    assinaturas = servico.assinaturas_do_aluno(con, aluno_id)
    assert len(assinaturas) == 1 and assinaturas[0]["status"] == "ativa"


def test_renovacao_nao_duplica_assinatura(con, aluno):
    aluno_id = int(aluno["id"])
    servico.aplicar(con, aluno_id, "elite", "tx-1")
    servico.aplicar(con, aluno_id, "elite", "tx-2")
    assert len(servico.assinaturas_do_aluno(con, aluno_id)) == 1


def test_recurso_bloqueado_no_plano_menor(con, aluno):
    aluno_id = int(aluno["id"])
    servico.aplicar(con, aluno_id, "recruta")
    atualizado = buscar_um(con, "SELECT * FROM alunos WHERE id=?", (aluno_id,))
    assert servico.tem_recurso(atualizado, "questoes")
    assert not servico.tem_recurso(atualizado, "simulados")


def test_plano_vencido_bloqueia_tudo(con, aluno):
    aluno_id = int(aluno["id"])
    servico.aplicar(con, aluno_id, "elite")
    executar(con, "UPDATE alunos SET plano_ate='2020-01-01' WHERE id=?", (aluno_id,))
    atualizado = buscar_um(con, "SELECT * FROM alunos WHERE id=?", (aluno_id,))
    assert servico.vencido(atualizado)
    assert not servico.tem_recurso(atualizado, "questoes")


def test_admin_passa_por_qualquer_gate(con):
    from app import alunos as servico_alunos

    servico_alunos.criar(con, "Chefe", "chefe@teste.com", admin=True, senha="comandante30")
    chefe = servico_alunos.por_email(con, "chefe@teste.com")
    executar(con, "UPDATE alunos SET plano='recruta' WHERE id=?", (chefe["id"],))
    chefe = servico_alunos.por_email(con, "chefe@teste.com")
    assert servico.tem_recurso(chefe, "simulados")


def test_cancelamento_mantem_acesso_ate_o_fim(con, aluno):
    aluno_id = int(aluno["id"])
    servico.aplicar(con, aluno_id, "elite")
    servico.cancelar(con, aluno_id, "pediu cancelamento")
    atualizado = buscar_um(con, "SELECT * FROM alunos WHERE id=?", (aluno_id,))
    assert not servico.vencido(atualizado)          # ainda dentro do período pago
    assert servico.assinaturas_do_aluno(con, aluno_id)[0]["status"] == "cancelada"


def test_reembolso_encerra_na_hora(con, aluno):
    aluno_id = int(aluno["id"])
    servico.aplicar(con, aluno_id, "elite")
    servico.encerrar_agora(con, aluno_id)
    atualizado = buscar_um(con, "SELECT * FROM alunos WHERE id=?", (aluno_id,))
    assert not servico.tem_recurso(atualizado, "questoes")
    assert servico.assinaturas_do_aluno(con, aluno_id)[0]["status"] == "expirada"


# --- integração com o webhook e com as telas -------------------------------


def enviar(cliente, corpo: dict):
    bruto = json.dumps(corpo).encode()
    from app.config import config

    return cliente.post(
        "/webhooks/cakto",
        content=bruto,
        headers={
            "content-type": "application/json",
            config.cakto_header_assinatura: assinatura_hmac(bruto, SEGREDO),
        },
    )


def test_webhook_coloca_o_aluno_no_plano_comprado(cliente):
    com_segredo(SEGREDO)
    compra = payload_compra(referencia="tx-plano-1")
    compra["product"] = {"name": "Operação Aprovação — Recruta"}
    assert enviar(cliente, compra).status_code == 200
    with sessao() as con:
        alvo = buscar_um(con, "SELECT * FROM alunos WHERE email='comprador@teste.com'")
        assert alvo["plano"] == "recruta"


def test_gate_bloqueia_simulado_no_plano_recruta(cliente):
    from app import alunos as servico_alunos

    with sessao() as con:
        servico_alunos.criar(con, "Aluna", "aluna@teste.com", senha="blindagem30")
        alvo = servico_alunos.por_email(con, "aluna@teste.com")
        servico.aplicar(con, int(alvo["id"]), "recruta")

    entrar(cliente, "aluna@teste.com", "blindagem30")
    # a vitrine de simulados abre — o bloqueio é por simulado, pelo recurso dele
    vitrine = cliente.get("/simulados")
    assert vitrine.status_code == 200
    bloqueado = cliente.get("/simulado/sim-1")
    assert bloqueado.status_code == 402
    assert "não está no seu plano" in bloqueado.text
    # o diagnóstico é prometido no plano de entrada e precisa abrir
    assert cliente.get("/simulado/sim-diagnostico").status_code == 200
    assert cliente.get("/questoes").status_code == 200   # esse continua liberado
    assert cliente.get("/planos").status_code == 200


def test_upgrade_libera_o_recurso(cliente):
    from app import alunos as servico_alunos

    with sessao() as con:
        servico_alunos.criar(con, "Aluna", "aluna@teste.com", senha="blindagem30")
        alvo = servico_alunos.por_email(con, "aluna@teste.com")
        servico.aplicar(con, int(alvo["id"]), "recruta")
    entrar(cliente, "aluna@teste.com", "blindagem30")
    assert cliente.get("/simulado/sim-1").status_code == 402

    with sessao() as con:
        alvo = servico_alunos.por_email(con, "aluna@teste.com")
        servico.aplicar(con, int(alvo["id"]), "operacao")
    # o gate de plano saiu; sobra só o da trilha (o Dia 4 ainda não foi liberado)
    assert cliente.get("/simulado/sim-1").status_code == 403


# --- limite diário do plano de entrada -------------------------------------


def test_saldo_diario_conta_apenas_as_questoes_de_hoje(con, aluno):
    from conteudo.questoes import QUESTOES

    from app import estudo

    aluno_id = int(aluno["id"])
    servico.aplicar(con, aluno_id, "recruta")
    atualizado = buscar_um(con, "SELECT * FROM alunos WHERE id=?", (aluno_id,))
    limite = servico.limite_do_dia(atualizado)
    assert limite > 0

    for q in QUESTOES[:3]:
        estudo.responder(con, aluno_id, q, q.correta, origem="treino")

    saldo = servico.saldo_de_questoes(con, atualizado)
    assert saldo["limitado"] and saldo["feitas"] == 3
    assert saldo["restantes"] == limite - 3
    assert not saldo["esgotado"]


def test_plano_superior_nao_tem_teto_diario(con, aluno):
    aluno_id = int(aluno["id"])
    servico.aplicar(con, aluno_id, "operacao")
    atualizado = buscar_um(con, "SELECT * FROM alunos WHERE id=?", (aluno_id,))
    saldo = servico.saldo_de_questoes(con, atualizado)
    assert not saldo["limitado"] and saldo["restantes"] is None


def test_api_recusa_questao_depois_do_limite_diario(cliente):
    from conteudo.questoes import QUESTOES

    from app import alunos as servico_alunos, estudo

    with sessao() as con:
        servico_alunos.criar(con, "Aluna", "aluna@teste.com", senha="blindagem30")
        alvo = servico_alunos.por_email(con, "aluna@teste.com")
        aluno_id = int(alvo["id"])
        servico.aplicar(con, aluno_id, "recruta")
        alvo = buscar_um(con, "SELECT * FROM alunos WHERE id=?", (aluno_id,))
        limite = servico.limite_do_dia(alvo)
        for q in QUESTOES[:limite]:
            estudo.responder(con, aluno_id, q, q.correta, origem="treino")

    entrar(cliente, "aluna@teste.com", "blindagem30")
    sobrando = QUESTOES[limite]
    resposta = cliente.post(
        "/api/responder",
        json={"questao_id": sobrando.id, "alternativa": sobrando.correta, "origem": "treino"},
    )
    assert resposta.status_code == 402
    assert "limite" in resposta.json()["erro"].lower()


def test_modulo_avancado_exige_upgrade(cliente):
    from app import alunos as servico_alunos

    with sessao() as con:
        servico_alunos.criar(con, "Aluna", "aluna@teste.com", senha="blindagem30")
        alvo = servico_alunos.por_email(con, "aluna@teste.com")
        servico.aplicar(con, int(alvo["id"]), "recruta")

    entrar(cliente, "aluna@teste.com", "blindagem30")
    # o download da apostila não pode ser porta dos fundos do gate de leitura
    assert cliente.get("/manual").status_code == 402
    assert cliente.get("/manual/download").status_code == 402

    # a vitrine abre para todo mundo — é ela que vende o upgrade
    vitrine = cliente.get("/modulos")
    assert vitrine.status_code == 200
    assert "Redação" in vitrine.text
    assert cliente.get("/modulos/redacao").status_code == 402

    with sessao() as con:
        alvo = servico_alunos.por_email(con, "aluna@teste.com")
        servico.aplicar(con, int(alvo["id"]), "operacao")
    assert cliente.get("/modulos/redacao").status_code == 200


# --- terreno pronto para os links de checkout da Cakto ---------------------


def test_todo_plano_tem_link_de_checkout_proprio():
    """Botão de compra sem destino é venda perdida — e todo plano precisa do seu.

    Um link único por plano também é o que permite ao webhook saber qual oferta
    foi comprada, já que a Cakto identifica o produto pelo link.
    """
    links = servico.checkouts()
    assert set(links) == {p.id for p in catalogo.PLANOS}
    for plano, url in links.items():
        assert url.startswith("https://"), f"{plano} sem link válido: {url!r}"
    assert len(set(links.values())) == len(links), "dois planos dividindo o mesmo checkout"


def test_variavel_de_ambiente_sobrepoe_o_link_do_catalogo(monkeypatch, cliente):
    """Trocar um checkout em produção não pode depender de deploy."""
    catalogo_url = catalogo.plano("recruta").checkout_url
    assert catalogo_url  # o link do catálogo é o padrão

    monkeypatch.setenv("CAKTO_CHECKOUT_RECRUTA", "https://pay.cakto.com.br/promo-de-lancamento")
    assert servico.checkouts()["recruta"] == "https://pay.cakto.com.br/promo-de-lancamento"
    # os outros seguem com o link do catálogo
    assert servico.checkouts()["elite"] == catalogo.plano("elite").checkout_url

    html = cliente.get("/").text
    assert "https://pay.cakto.com.br/promo-de-lancamento" in html


def test_pagina_de_vendas_leva_para_os_checkouts_reais(cliente):
    html = cliente.get("/").text
    for plano, url in servico.checkouts().items():
        assert url in html, f"o botão do plano {plano} não aponta para o checkout"


def test_identificacao_do_plano_segue_a_ordem_de_confianca():
    """Link do checkout vence nome; nome vence valor; e nada é 'nada'.

    A distinção entre "não reconheci" e "reconheci o plano de entrada" é
    delicada porque o plano de entrada é o próprio padrão. Sem separar os dois,
    uma compra do Recruta identificada corretamente pelo nome era tratada como
    falha de reconhecimento e caía na identificação por valor.
    """
    recruta = catalogo.plano("recruta")
    elite = catalogo.plano("elite")

    # nada casa → string vazia, não o plano padrão
    assert catalogo.identificar_ou_nada("produto qualquer") == ""
    assert catalogo.identificar("produto qualquer") == catalogo.PLANO_PADRAO

    # o nome reconhece
    assert catalogo.identificar_ou_nada("Operação Aprovação — Recruta") == "recruta"

    # o link vence o nome, porque o vendedor renomeia o produto quando quiser
    assert catalogo.identificar_ou_nada(elite.checkout_url, "plano recruta") == "elite"

    # e o valor só entra quando nome e link não dizem nada
    assert catalogo.identificar_por_valor(recruta.valor) == "recruta"
    assert catalogo.identificar_por_valor(elite.valor) == "elite"


def test_link_do_checkout_casa_mesmo_alterado():
    """Os três planos são ofertas do mesmo produto: só o link os distingue.

    Como o nome do produto chega igual nas três vendas, se o link não casar a
    venda cai no plano padrão — que é o mais barato. Vender Elite e entregar
    Recruta é o erro mais caro que essa função pode cometer.
    """
    recruta = catalogo.POR_ID["recruta"]
    elite = catalogo.POR_ID["elite"]

    # exatamente como está cadastrado
    assert catalogo.identificar_ou_nada(recruta.checkout_url) == "recruta"
    # com barra no fim
    assert catalogo.identificar_ou_nada(recruta.checkout_url + "/") == "recruta"
    # com parâmetros de campanha grudados
    assert catalogo.identificar_ou_nada(elite.checkout_url + "?utm_source=ig") == "elite"
    # sem o sufixo da oferta, como alguns painéis devolvem
    assert catalogo.identificar_ou_nada("https://pay.cakto.com.br/3b55ibi") == "recruta"
    # só o slug, sem domínio
    assert catalogo.identificar_ou_nada("y8zqtwu") == "elite"


def test_codigo_numerico_nao_casa_no_meio_de_outro_numero():
    """"47" dentro de "1470" ou de um id de oferta viraria Recruta por acidente."""
    assert catalogo.identificar_ou_nada("pedido 1470 sem plano") == ""
    assert catalogo.identificar_ou_nada("oferta B47xyz") == ""
    # como palavra inteira continua valendo
    assert catalogo.identificar_ou_nada("plano de R$ 47,00") == "recruta"
