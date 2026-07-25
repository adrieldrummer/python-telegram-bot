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

from .. import alunos as servico_alunos
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
        "id",
        "data.id",
        "transaction_id",
        "data.transaction_id",
        "order_id",
        "data.order.id",
        "reference",
    )
    produto = _buscar(payload, "product.name", "data.product.name", "product_name", "offer.name")
    oferta = _buscar(payload, "offer.name", "data.offer.name", "offer_id", "data.offer.id")
    bruto = _buscar(payload, "amount", "data.amount", "value", "data.value", "total", "price")
    try:
        valor_pago = float(str(bruto).replace(",", ".")) if bruto else 0.0
    except ValueError:
        valor_pago = 0.0
    # a Cakto costuma mandar centavos em contas com integração antiga
    if valor_pago > 10000:
        valor_pago = valor_pago / 100

    return {
        "email": normalizar_email(email),
        "nome": nome or "Candidato",
        "telefone": telefone,
        "status": status,
        "evento": evento,
        "referencia": referencia,
        "produto": produto,
        "oferta": oferta,
        "valor": valor_pago,
    }


def _assinatura_confere(request: Request, corpo: bytes) -> bool:
    segredo = config.cakto_webhook_segredo
    if not segredo:
        return config.cakto_permitir_sem_assinatura
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
    # aceita tanto HMAC-SHA256 do corpo quanto token compartilhado simples
    if hmac.compare_digest(enviada, assinatura_hmac(corpo, segredo)):
        return True
    return hmac.compare_digest(enviada, segredo)


@router.post("/cakto")
async def cakto(request: Request):
    corpo = await request.body()
    valida = _assinatura_confere(request, corpo)
    try:
        payload = json.loads(corpo.decode("utf-8") or "{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        payload = {}
    if not isinstance(payload, dict):
        payload = {"payload": payload}

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
                if aluno["status"] != "ativo":
                    servico_alunos.aprovar_acesso(con, aluno)
                    resultado = "acesso aprovado e e-mail enviado"
                else:
                    resultado = "compra registrada (aluno já ativo)"
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
                    servico_alunos.suspender(con, int(aluno["id"]), f"evento Cakto: {marcador.strip()}")
                    resultado = "acesso suspenso"
                else:
                    resultado = "evento de cancelamento sem aluno correspondente"
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
                json.dumps(payload, ensure_ascii=False)[:8000],
                resultado,
            ),
        )

    return JSONResponse({"ok": status_http == 200, "resultado": resultado}, status_code=status_http)


@router.get("/cakto")
async def cakto_teste():
    """Endpoint de verificação usado por alguns painéis ao cadastrar a URL."""
    return {"ok": True, "servico": "webhook cakto", "metodo_esperado": "POST"}
