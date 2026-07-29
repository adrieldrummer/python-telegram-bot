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
        "product": {"name": "Operação Aprovação"},
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


def test_compra_aprovada_ativa_a_conta_e_envia_login_e_senha(cliente):
    com_segredo(SEGREDO)
    resposta = enviar(cliente, payload_compra())
    assert resposta.status_code == 200
    with sessao() as con:
        aluno = servico_alunos.por_email(con, "comprador@teste.com")
        assert aluno is not None
        # a conta já sai ativa, com senha gerada: o comprador entra direto, sem
        # depender de clicar num link — o passo em que mais gente se perde
        assert aluno["status"] == "ativo"
        assert aluno["senha_hash"], "a compra deveria gerar uma senha"
        assert aluno["senha_temporaria"] == 1

        email = buscar_um(con, "SELECT * FROM emails WHERE aluno_id=?", (aluno["id"],))
        assert email is not None
        corpo = email["corpo_html"]
        assert aluno["email"] in corpo, "o e-mail precisa dizer qual é o login"
        assert "Senha:" in corpo, "o e-mail precisa trazer a senha gerada"
        # e o link de criar a própria senha continua disponível para quem preferir
        assert "/ativar/" in corpo
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


def test_comprador_entra_direto_com_a_senha_do_email(cliente):
    """O caminho completo: compra → e-mail com senha → login sem clicar em link.

    É o passo que a plataforma passou a cobrir: antes o comprador precisava
    abrir o e-mail, clicar, criar senha e só então entrar. Cada etapa a mais
    entre pagar e usar é gente que some pelo caminho.
    """
    import re

    com_segredo(SEGREDO)
    enviar(cliente, payload_compra(email="novato@teste.com"))

    with sessao() as con:
        aluno = servico_alunos.por_email(con, "novato@teste.com")
        corpo = buscar_um(
            con, "SELECT corpo_html FROM emails WHERE aluno_id=?", (aluno["id"],)
        )["corpo_html"]

    achou = re.search(r"Senha:.*?>([A-Z][a-z]+-\d{4})<", corpo, re.S)
    assert achou, "a senha gerada não apareceu no e-mail"
    senha = achou.group(1)

    cliente.get("/entrar")
    resposta = cliente.post(
        "/entrar",
        data={
            "email": "novato@teste.com",
            "senha": senha,
            "csrf_token": cliente.cookies.get("map_csrf"),
        },
        follow_redirects=True,
    )
    assert resposta.status_code == 200
    painel = cliente.get("/painel")
    assert painel.status_code == 200
    # e a plataforma cobra a troca enquanto a senha for a do e-mail
    assert "Troque a senha que veio por e-mail" in painel.text

    # depois de trocar, o aviso some
    cliente.post(
        "/conta/senha",
        data={
            "atual": senha,
            "nova": "minhasenhaforte9",
            "confirmacao": "minhasenhaforte9",
            "csrf_token": cliente.cookies.get("map_csrf"),
        },
        follow_redirects=True,
    )
    with sessao() as con:
        aluno = servico_alunos.por_email(con, "novato@teste.com")
        assert aluno["senha_temporaria"] == 0


# --- o formato real da Cakto ----------------------------------------------

PAYLOAD_CAKTO = {
    "secret": "chave-do-painel-da-cakto",
    "event": "purchase_approved",
    "data": {
        "id": "87956abe-940e-4e8b-8a27-82c482920f64",
        "refId": "9vbgfmg",
        "customer": {
            "name": "Maria Souza",
            "email": "maria.souza@example.com",
            "phone": "34999999999",
            "docNumber": "12345678909",
            "docType": "cpf",
        },
        "offer": {"id": "B8BcHrY", "name": "Oferta principal", "price": 47},
        "offer_type": "main",
        "product": {"name": "Operação Aprovação", "id": "ff3fdf61", "type": "unique"},
        "checkoutUrl": "https://pay.cakto.com.br/3b55ibi_1009316",
        "status": "paid",
        "baseAmount": 47,
        "discount": 0,
        "amount": 47,
        "installments": 1,
        "paymentMethod": "credit_card",
        "paidAt": "2026-06-26T12:00:00.000000+00:00",
    },
}


def enviar_bruto(cliente, corpo: dict):
    """Sem cabeçalho de assinatura: a Cakto autentica pelo campo `secret`."""
    return cliente.post(
        "/webhooks/cakto",
        content=json.dumps(corpo).encode(),
        headers={"content-type": "application/json"},
    )


def test_cakto_autentica_pelo_segredo_no_corpo(cliente):
    """A Cakto manda a chave dentro do JSON, não como assinatura no cabeçalho.

    Este é o formato real do painel. Sem aceitá-lo, toda venda seria recusada
    com 401 e nenhum acesso seria liberado.
    """
    com_segredo("chave-do-painel-da-cakto")
    resposta = enviar_bruto(cliente, PAYLOAD_CAKTO)
    assert resposta.status_code == 200, resposta.text

    with sessao() as con:
        aluno = servico_alunos.por_email(con, "maria.souza@example.com")
        assert aluno is not None
        assert aluno["status"] == "ativo"
        assert aluno["nome"] == "Maria Souza"
        # o link do checkout identificou o plano de entrada
        assert aluno["plano"] == "recruta"


def test_segredo_errado_no_corpo_e_recusado(cliente):
    com_segredo("chave-do-painel-da-cakto")
    intruso = {**PAYLOAD_CAKTO, "secret": "chave-errada"}
    assert enviar_bruto(cliente, intruso).status_code == 401
    with sessao() as con:
        assert valor(con, "SELECT COUNT(*) FROM alunos") == 0


def test_sem_segredo_nenhum_e_recusado(cliente):
    com_segredo("chave-do-painel-da-cakto")
    sem = {k: v for k, v in PAYLOAD_CAKTO.items() if k != "secret"}
    assert enviar_bruto(cliente, sem).status_code == 401


def test_link_do_checkout_define_o_plano(cliente):
    """O vendedor renomeia produto e oferta; o link é o que ele divulgou."""
    from conteudo import planos as catalogo

    com_segredo("chave-do-painel-da-cakto")
    for plano in catalogo.PLANOS:
        corpo = json.loads(json.dumps(PAYLOAD_CAKTO))
        corpo["data"]["id"] = f"tx-{plano.id}"
        corpo["data"]["customer"]["email"] = f"{plano.id}@example.com"
        corpo["data"]["checkoutUrl"] = plano.checkout_url
        corpo["data"]["product"]["name"] = "Nome trocado pelo vendedor"
        corpo["data"]["offer"]["name"] = "Oferta renomeada"
        corpo["data"]["amount"] = plano.valor
        assert enviar_bruto(cliente, corpo).status_code == 200

        with sessao() as con:
            aluno = servico_alunos.por_email(con, f"{plano.id}@example.com")
            assert aluno["plano"] == plano.id, f"{plano.id} identificado como {aluno['plano']}"


def test_segredo_nao_fica_guardado_no_historico(cliente):
    """O histórico do admin é visível; o segredo não pode viver lá em texto puro."""
    com_segredo("chave-do-painel-da-cakto")
    enviar_bruto(cliente, PAYLOAD_CAKTO)
    with sessao() as con:
        guardado = buscar_um(con, "SELECT payload FROM webhooks ORDER BY id DESC")["payload"]
    assert "chave-do-painel-da-cakto" not in guardado
    assert '"secret": "***"' in guardado


# Payload de exemplo do próprio painel da Cakto, copiado inteiro. Guardar o
# formato completo aqui evita a regressão mais cara possível: uma venda real
# recusada em produção porque um campo novo mudou a leitura.
PAYLOAD_PAINEL = {
    "secret": "chave-do-painel-da-cakto",
    "event": "purchase_approved",
    "data": {
        "id": "87956abe-940e-4e8b-8a27-82c482920f64",
        "refId": "9vbgfmg",
        "customer": {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "phone": "34999999999",
            "docNumber": "12345678909",
            "birthDate": None,
            "docType": "cpf",
        },
        "address": None,
        "shipping": None,
        "affiliate": "affiliate@example.com",
        "offer": {"id": "B8BcHrY", "name": "Special Offer", "price": 100, "image": None},
        "offer_type": "main",
        "product": {
            "name": "Produto Teste",
            "id": "ff3fdf61-e88f-43b5-982a-32d50f112414",
            "short_id": "AckhQ75",
            "supportEmail": "suporte@seudominio.com",
            "type": "unique",
            "invoiceDescription": "",
        },
        "checkout": 12345,
        "subscription": None,
        "subscription_period": 1,
        "parent_order": None,
        "checkoutUrl": "https://pay.cakto.com.br/EXAMPLE",
        "status": "paid",
        "baseAmount": 100,
        "discount": 10,
        "amount": 90,
        "commissions": [
            {"user": "produtor@seudominio.com", "totalAmount": 85.5,
             "type": "producer", "percentage": 95}
        ],
        "fees": 4.5,
        "couponCode": None,
        "reason": None,
        "refund_reason": None,
        "installments": 1,
        "paymentMethod": "credit_card",
        "paymentMethodName": "Cartão de Crédito",
        "paidAt": "2026-06-26T12:00:00.000000+00:00",
        "createdAt": "2026-06-26T12:00:00.000000+00:00",
        "due_date": None,
        "refundedAt": None,
        "chargedbackAt": None,
        "canceledAt": None,
        "utm_source": None, "utm_medium": None, "utm_campaign": None,
        "utm_term": None, "utm_content": None,
        "sck": None, "fbc": None, "fbp": None,
        "card": {"lastDigits": "4323", "holderName": "Card Example", "brand": "visa"},
    },
}


def test_payload_completo_do_painel_libera_o_acesso(cliente):
    """Campos que a plataforma não usa (comissão, cartão, UTM) não atrapalham."""
    com_segredo("chave-do-painel-da-cakto")
    resposta = enviar_bruto(cliente, PAYLOAD_PAINEL)
    assert resposta.status_code == 200, resposta.text

    with sessao() as con:
        aluno = servico_alunos.por_email(con, "john.doe@example.com")
        assert aluno is not None
        assert aluno["status"] == "ativo"
        assert aluno["senha_hash"], "sem senha o comprador não entra"


def test_valor_com_desconto_define_o_plano(cliente):
    """`amount` é o que o cliente pagou; `baseAmount` é o preço de tabela.

    Com cupom de 10, uma Operação Completa de 97 chega como 87. Ler o
    `baseAmount` daria o plano certo pelo preço cheio, mas erraria quando a
    oferta em si mudasse de preço — e o link do checkout, quando existe, já
    resolve antes. O valor só decide quando o link não é reconhecido, e aí o
    que vale é a faixa do que foi pago.
    """
    com_segredo("chave-do-painel-da-cakto")
    corpo = json.loads(json.dumps(PAYLOAD_PAINEL))
    corpo["data"]["id"] = "tx-com-desconto"
    corpo["data"]["customer"]["email"] = "desconto@example.com"
    corpo["data"]["baseAmount"] = 97
    corpo["data"]["discount"] = 10
    corpo["data"]["amount"] = 87
    assert enviar_bruto(cliente, corpo).status_code == 200

    with sessao() as con:
        aluno = servico_alunos.por_email(con, "desconto@example.com")
        assert aluno["plano"] == "operacao"
