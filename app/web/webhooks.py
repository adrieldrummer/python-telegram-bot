"""Webhook da Cakto: compra aprovada libera acesso; reembolso suspende.

A Cakto envia um JSON por evento. Como o formato exato varia conforme a conta
e a versão do painel, a leitura aqui é tolerante: procuramos o e-mail, o nome,
o status e o identificador da transação em vários caminhos possíveis, e
registramos o payload cru para conferência em /admin/webhooks.
"""

from __future__ import annotations

import hmac
import json
from typing import Any, Optional

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from conteudo import planos as catalogo_planos

from .. import alunos as servico_alunos
from .. import marketing
from .. import planos as servico_planos
from ..config import config
from ..db import buscar_um, executar, sessao
from ..security import assinatura_hmac, email_valido, normalizar_email

router = APIRouter(prefix="/webhooks")

STATUS_APROVADO = {
    "paid",
    "approved",
    "aprovado",
    "aprovada",
    "completed",
    "purchase_approved",
    "payment_approved",
    "waiting_payment_confirmed",
    "authorized",
}
# cancelamento de assinatura: mantém o acesso até o fim do período já pago
STATUS_ASSINATURA_CANCELADA = {
    "subscription_canceled",
    "subscription_cancelled",
    "assinatura_cancelada",
    "canceled_subscription",
}
STATUS_CANCELADO = {
    "refunded",
    "refund",
    "reembolsado",
    "chargeback",
    "canceled",
    "cancelled",
    "cancelado",
    "expired",
    "subscription_canceled",
    "dispute",
}


def _buscar(dados: Any, *caminhos: str) -> str:
    """Procura o primeiro caminho existente, no formato 'a.b.c'."""
    for caminho in caminhos:
        atual: Any = dados
        for parte in caminho.split("."):
            if isinstance(atual, dict) and parte in atual:
                atual = atual[parte]
            else:
                atual = None
                break
        if isinstance(atual, (str, int, float)) and str(atual).strip():
            return str(atual).strip()
    return ""


def extrair(payload: dict) -> dict:
    """Normaliza o payload da Cakto para os campos que a plataforma usa."""
    email = _buscar(
        payload,
        "customer.email",
        "data.customer.email",
        "data.customer_email",
        "buyer.email",
        "data.buyer.email",
        "client.email",
        "email",
        "data.email",
    )
    nome = _buscar(
        payload,
        "customer.name",
        "data.customer.name",
        "buyer.name",
        "data.buyer.name",
        "client.name",
        "name",
        "data.name",
    )
    telefone = _buscar(
        payload,
        "customer.phone",
        "data.customer.phone",
        "buyer.phone",
        "data.buyer.phone",
        "phone",
    )
    status = _buscar(
        payload, "status", "data.status", "event", "type", "data.event", "payment_status"
    ).lower()
    evento = _buscar(payload, "event", "type", "data.event", "webhook_event").lower()
    referencia = _buscar(
        payload,
        "data.id",
        "id",
        "data.refId",
        "transaction_id",
        "data.transaction_id",
        "order_id",
        "data.order.id",
        "reference",
    )
    produto = _buscar(payload, "data.product.name", "product.name", "product_name")
    oferta = _buscar(payload, "data.offer.name", "offer.name", "data.offer.id", "offer_id")
    # o link do checkout é o identificador mais estável da oferta: o vendedor
    # renomeia produto e oferta quando quiser, mas o link é o que ele divulgou
    checkout = _buscar(payload, "data.checkoutUrl", "checkoutUrl", "data.checkout_url")
    bruto = _buscar(
        payload, "data.amount", "amount", "data.baseAmount", "value", "data.value",
        "total", "data.offer.price",
    )
    try:
        valor_pago = float(str(bruto).replace(",", ".")) if bruto else 0.0
    except ValueError:
        valor_pago = 0.0
    # a Cakto costuma mandar centavos em contas com integração antiga
    if valor_pago > 10000:
        valor_pago = valor_pago / 100

    # rastreamento: a Cakto devolve o que foi levado na URL do checkout. `fbc`
    # e `fbp` são o que permite ao Meta ligar esta venda ao anúncio que a
    # gerou — sem eles a campanha otimiza vendo só o gasto.
    rastreio = {
        chave: _buscar(payload, f"data.{chave}", chave)
        for chave in ("fbc", "fbp", "utm_source", "utm_medium", "utm_campaign",
                      "utm_content", "utm_term", "sck")
    }

    return {
        "rastreio": {k: v for k, v in rastreio.items() if v},
        "email": normalizar_email(email),
        "nome": nome or "Candidato",
        "telefone": telefone,
        "status": status,
        "evento": evento,
        "referencia": referencia,
        "produto": produto,
        "oferta": oferta,
        "checkout": checkout,
        "valor": valor_pago,
        # assinatura: a Cakto manda o objeto quando o produto é recorrente
        "assinatura": bool(_buscar(payload, "data.subscription.id", "data.subscription")),
    }


def _assinatura_confere(request: Request, corpo: bytes, payload: dict) -> bool:
    """Confere se a chamada veio mesmo da Cakto.

    A Cakto manda a chave secreta **dentro do corpo**, no campo `secret` do
    JSON — não como assinatura em cabeçalho. As outras formas continuam
    aceitas porque o painel varia entre contas e porque outros provedores
    (ou um proxy próprio) podem assinar por cabeçalho.

    A comparação é sempre por `compare_digest`: comparar segredo com `==`
    vaza, pelo tempo de resposta, quantos caracteres iniciais bateram.
    """
    segredo = config.cakto_webhook_segredo
    if not segredo:
        return config.cakto_permitir_sem_assinatura

    # 1) o jeito da Cakto: campo "secret" no corpo
    do_corpo = _buscar(payload, "secret", "data.secret", "webhook_secret")
    if do_corpo and hmac.compare_digest(do_corpo, segredo):
        return True

    # 2) cabeçalho: HMAC-SHA256 do corpo ou token compartilhado
    enviada = (
        request.headers.get(config.cakto_header_assinatura)
        or request.headers.get("x-webhook-signature")
        or request.headers.get("x-signature")
        or request.query_params.get("token")
        or ""
    ).strip()
    if not enviada:
        return False
    enviada = enviada.split("=")[-1].strip()
    if hmac.compare_digest(enviada, assinatura_hmac(corpo, segredo)):
        return True
    return hmac.compare_digest(enviada, segredo)


def _sem_segredo(payload: dict) -> dict:
    """Remove a chave secreta antes de guardar o payload.

    O histórico em /admin/webhooks existe para conferência e fica visível para
    qualquer administrador. Guardar o segredo ali seria deixá-lo em texto puro
    no banco, à toa.
    """
    limpo = dict(payload)
    for campo in ("secret", "webhook_secret"):
        if campo in limpo:
            limpo[campo] = "***"
    if isinstance(limpo.get("data"), dict) and "secret" in limpo["data"]:
        limpo["data"] = {**limpo["data"], "secret": "***"}
    return limpo


@router.post("/cakto")
async def cakto(request: Request):
    corpo = await request.body()
    try:
        payload = json.loads(corpo.decode("utf-8") or "{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        payload = {}
    if not isinstance(payload, dict):
        payload = {"payload": payload}

    valida = _assinatura_confere(request, corpo, payload)
    dados = extrair(payload)
    resultado = ""
    status_http = 200

    with sessao() as con:
        # idempotência: o mesmo evento nunca é processado duas vezes
        if dados["referencia"]:
            ja_visto = buscar_um(
                con, "SELECT id FROM webhooks WHERE evento_id = ?", (dados["referencia"],)
            )
            if ja_visto is not None:
                return JSONResponse({"ok": True, "resultado": "evento já processado"})

        if not valida:
            resultado = "assinatura inválida"
            status_http = 401
        elif not email_valido(dados["email"]):
            resultado = "payload sem e-mail válido"
            status_http = 422
        else:
            marcador = f"{dados['status']} {dados['evento']}"
            aprovado = any(chave in marcador for chave in STATUS_APROVADO)
            cancelado = any(chave in marcador for chave in STATUS_CANCELADO)
            assinatura_cancelada = any(
                chave in marcador for chave in STATUS_ASSINATURA_CANCELADA
            )
            if assinatura_cancelada:
                cancelado = False   # o acesso continua até o fim do período pago
            # link do checkout > nome do produto/oferta > valor pago > padrão
            plano_id = catalogo_planos.identificar_ou_nada(
                dados["checkout"], dados["produto"], dados["oferta"]
            )
            if not plano_id and dados["valor"]:
                plano_id = catalogo_planos.identificar_por_valor(dados["valor"])
            if not plano_id:
                plano_id = catalogo_planos.PLANO_PADRAO

            aluno = servico_alunos.por_email(con, dados["email"])
            if aprovado:
                if aluno is None:
                    aluno = servico_alunos.criar(
                        con, dados["nome"], dados["email"], dados["telefone"], origem="cakto"
                    )
                servico_alunos.registrar_compra(
                    con,
                    int(aluno["id"]),
                    dados["referencia"] or "sem-referencia",
                    "aprovada",
                    dados["email"],
                    dados["produto"],
                    dados["oferta"],
                    dados["valor"],
                )
                plano = servico_planos.aplicar(
                    con, int(aluno["id"]), plano_id, dados["referencia"] or ""
                )
                marketing.compra_aprovada(
                    con,
                    aluno,
                    dados["referencia"] or f"aluno-{aluno['id']}",
                    dados["valor"],
                    plano.nome,
                    rastreio=dados["rastreio"],
                )
                if aluno["status"] != "ativo":
                    servico_alunos.aprovar_acesso(con, aluno)
                    # sem SMTP o e-mail é gravado e não sai; dizer "enviado" no
                    # histórico esconderia justamente o problema que faz o
                    # comprador pagar e nunca receber a senha
                    destino = (
                        "e-mail enviado"
                        if config.smtp_configurado
                        else "e-mail SÓ NA CAIXA DE SAÍDA — sem SMTP não foi entregue"
                    )
                    resultado = f"acesso aprovado ({plano.nome}) e {destino}"
                else:
                    resultado = f"compra registrada — plano {plano.nome}"
            elif cancelado:
                if aluno is not None:
                    servico_alunos.registrar_compra(
                        con,
                        int(aluno["id"]),
                        dados["referencia"] or "sem-referencia",
                        "reembolsada",
                        dados["email"],
                        dados["produto"],
                        dados["oferta"],
                        dados["valor"],
                    )
                    servico_planos.encerrar_agora(con, int(aluno["id"]))
                    marketing.reembolso(
                        con, aluno, dados["referencia"] or f"aluno-{aluno['id']}", dados["valor"]
                    )
                    servico_alunos.suspender(con, int(aluno["id"]), f"evento Cakto: {marcador.strip()}")
                    resultado = "acesso suspenso e assinatura encerrada"
                else:
                    resultado = "evento de cancelamento sem aluno correspondente"
            elif assinatura_cancelada:
                if aluno is not None:
                    servico_planos.cancelar(
                        con, int(aluno["id"]), f"assinatura cancelada na Cakto ({marcador.strip()})"
                    )
                    resultado = "assinatura cancelada — acesso mantido até o fim do período"
                else:
                    resultado = "cancelamento de assinatura sem aluno correspondente"
            else:
                resultado = f"evento ignorado ({marcador.strip() or 'sem status'})"

        executar(
            con,
            """INSERT INTO webhooks (provedor, evento_id, tipo, assinatura_ok, payload, resultado)
               VALUES (?,?,?,?,?,?)""",
            (
                "cakto",
                dados["referencia"] or None,
                (dados["evento"] or dados["status"])[:80],
                1 if valida else 0,
                json.dumps(_sem_segredo(payload), ensure_ascii=False)[:8000],
                resultado,
            ),
        )

    return JSONResponse({"ok": status_http == 200, "resultado": resultado}, status_code=status_http)


@router.get("/cakto")
async def cakto_teste():
    """Endpoint de verificação usado por alguns painéis ao cadastrar a URL."""
    return {"ok": True, "servico": "webhook cakto", "metodo_esperado": "POST"}
