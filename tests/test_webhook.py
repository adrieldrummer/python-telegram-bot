"""Webhook da Cakto: assinatura, idempotência e ciclo de acesso."""

from __future__ import annotations

import json

from app import alunos as servico_alunos
from app.config import config
from app.db import buscar_um, sessao, valor
from app.security import assinatura_hmac
from app.web.webhooks import extrair

SEGREDO = "segredo-de-teste"


def payload_compra(email="comprador@teste.com", referencia="tx-1"):
    return {
        "event": "purchase_approved",
        "id": referencia,
        "status": "paid",
        "amount": 197.0,
        "customer": {"name": "Comprador Teste", "email": email, "phone": "11999999999"},
        "product": {"name": "Mapa da Aprovação"},
    }


def enviar(cliente, corpo: dict, segredo: str | None = SEGREDO):
    bruto = json.dumps(corpo).encode()
    cabecalhos = {"content-type": "application/json"}
    if segredo is not None:
        cabecalhos[config.cakto_header_assinatura] = assinatura_hmac(bruto, segredo)
    return cliente.post("/webhooks/cakto", content=bruto, headers=cabecalhos)


def com_segredo(valor_novo: str):
    object.__setattr__(config, "cakto_webhook_segredo", valor_novo)


def test_extrair_le_formatos_diferentes():
    dados = extrair({"data": {"customer": {"email": "A@B.com", "name": "Ana"}, "status": "APPROVED"}})
    assert dados["email"] == "a@b.com"
    assert dados["nome"] == "Ana"
    assert dados["status"] == "approved"


def test_extrair_converte_centavos():
    assert extrair({"amount": 19700})["valor"] == 197.0
    assert extrair({"amount": "197,00"})["valor"] == 197.0


def test_webhook_sem_assinatura_e_recusado(cliente):
    com_segredo(SEGREDO)
    resposta = enviar(cliente, payload_compra(), segredo=None)
    assert resposta.status_code == 401
    with sessao() as con:
        assert valor(con, "SELECT COUNT(*) FROM alunos") == 0


def test_webhook_com_assinatura_errada_e_recusado(cliente):
    com_segredo(SEGREDO)
    resposta = enviar(cliente, payload_compra(), segredo="outro-segredo")
    assert resposta.status_code == 401


def test_compra_aprovada_cria_aluno_pendente_e_envia_email(cliente):
    com_segredo(SEGREDO)
    resposta = enviar(cliente, payload_compra())
    assert resposta.status_code == 200
    with sessao() as con:
        aluno = servico_alunos.por_email(con, "comprador@teste.com")
        assert aluno is not None
        assert aluno["status"] == "pendente"
        assert not aluno["senha_hash"]
        email = buscar_um(con, "SELECT * FROM emails WHERE aluno_id=?", (aluno["id"],))
        assert email is not None
        assert "/ativar/" in email["corpo_html"]
        assert valor(con, "SELECT COUNT(*) FROM compras WHERE status='aprovada'") == 1


def test_evento_repetido_nao_duplica(cliente):
    com_segredo(SEGREDO)
    enviar(cliente, payload_compra())
    enviar(cliente, payload_compra())
    with sessao() as con:
        assert valor(con, "SELECT COUNT(*) FROM compras") == 1
        assert valor(con, "SELECT COUNT(*) FROM alunos") == 1


def test_reembolso_suspende_o_acesso(cliente):
    com_segredo(SEGREDO)
    enviar(cliente, payload_compra())
    reembolso = payload_compra(referencia="tx-2")
    reembolso["event"] = "refunded"
    reembolso["status"] = "refunded"
    enviar(cliente, reembolso)
    with sessao() as con:
        aluno = servico_alunos.por_email(con, "comprador@teste.com")
        assert aluno["status"] == "suspenso"


def test_payload_sem_email_e_rejeitado(cliente):
    com_segredo(SEGREDO)
    resposta = enviar(cliente, {"event": "purchase_approved", "id": "tx-sem-email"})
    assert resposta.status_code == 422


def test_ativacao_pelo_link_do_email(cliente):
    """Fluxo completo: compra → e-mail de aprovação → criação de senha → login."""
    com_segredo(SEGREDO)
    enviar(cliente, payload_compra())
    with sessao() as con:
        aluno = servico_alunos.por_email(con, "comprador@teste.com")
        corpo = buscar_um(con, "SELECT corpo_html FROM emails WHERE aluno_id=?", (aluno["id"],))["corpo_html"]
    token = corpo.split("/ativar/")[1].split('"')[0].split("<")[0].strip()

    pagina = cliente.get(f"/ativar/{token}")
    assert pagina.status_code == 200
    csrf = cliente.cookies.get("map_csrf")
    resposta = cliente.post(
        f"/ativar/{token}",
        data={"senha": "aprovacao30dias", "confirmacao": "aprovacao30dias", "csrf_token": csrf},
        follow_redirects=True,
    )
    assert resposta.status_code == 200
    with sessao() as con:
        aluno = servico_alunos.por_email(con, "comprador@teste.com")
        assert aluno["status"] == "ativo"
        assert aluno["senha_hash"]
