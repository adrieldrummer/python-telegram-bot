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
    bloqueado = cliente.get("/simulados")
    assert bloqueado.status_code == 402
    assert "não está no seu plano" in bloqueado.text
    assert cliente.get("/questoes").status_code == 200   # esse continua liberado
    assert cliente.get("/planos").status_code == 200


def test_upgrade_libera_o_recurso(cliente):
    from app import alunos as servico_alunos

    with sessao() as con:
        servico_alunos.criar(con, "Aluna", "aluna@teste.com", senha="blindagem30")
        alvo = servico_alunos.por_email(con, "aluna@teste.com")
        servico.aplicar(con, int(alvo["id"]), "recruta")
    entrar(cliente, "aluna@teste.com", "blindagem30")
    assert cliente.get("/simulados").status_code == 402

    with sessao() as con:
        alvo = servico_alunos.por_email(con, "aluna@teste.com")
        servico.aplicar(con, int(alvo["id"]), "operacao")
    assert cliente.get("/simulados").status_code == 200
