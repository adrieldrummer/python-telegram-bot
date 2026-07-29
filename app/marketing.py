"""Rastreamento de conversão do Meta (Facebook/Instagram).

Duas camadas, propositalmente redundantes:

1. **Pixel no navegador** — dispara PageView, ViewContent e InitiateCheckout.
   Simples, mas perde entre 20% e 40% dos eventos (bloqueador de anúncio,
   iOS, aba fechada rápido).
2. **API de Conversões (CAPI)** — dispara Purchase e CompleteRegistration do
   servidor, a partir do webhook da Cakto. Não depende do navegador do
   comprador e é o que faz a otimização de campanha funcionar de verdade.

Os dois lados mandam o mesmo `event_id` quando o evento é o mesmo, então o
Meta deduplica sozinho. Nenhuma falha aqui pode derrubar uma requisição: se o
Meta estiver fora, o aluno continua comprando e estudando.
"""

from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import time
from typing import Any, Optional

from .config import config
from .db import executar
from .security import normalizar_email

TEMPO_LIMITE = 6.0


def _hash(valor: str) -> str:
    return hashlib.sha256(valor.strip().lower().encode("utf-8")).hexdigest()


def _telefone_normalizado(telefone: str) -> str:
    numeros = re.sub(r"\D", "", telefone or "")
    if not numeros:
        return ""
    if not numeros.startswith("55") and len(numeros) in (10, 11):
        numeros = "55" + numeros
    return numeros


def dados_do_usuario(
    email: str = "",
    telefone: str = "",
    nome: str = "",
    aluno_id: Optional[int] = None,
    ip: str = "",
    user_agent: str = "",
    fbp: str = "",
    fbc: str = "",
) -> dict:
    """Monta o bloco `user_data` já com hash — o Meta exige SHA-256."""
    dados: dict[str, Any] = {}
    email = normalizar_email(email)
    if email:
        dados["em"] = [_hash(email)]
    fone = _telefone_normalizado(telefone)
    if fone:
        dados["ph"] = [_hash(fone)]
    partes = (nome or "").strip().split()
    if partes:
        dados["fn"] = [_hash(partes[0])]
        if len(partes) > 1:
            dados["ln"] = [_hash(partes[-1])]
    if aluno_id:
        dados["external_id"] = [_hash(str(aluno_id))]
    if ip:
        dados["client_ip_address"] = ip
    if user_agent:
        dados["client_user_agent"] = user_agent
    if fbp:
        dados["fbp"] = fbp
    if fbc:
        dados["fbc"] = fbc
    return dados


def enviar_evento(
    nome: str,
    event_id: str,
    user_data: dict,
    custom_data: Optional[dict] = None,
    origem: str = "website",
    url: str = "",
    con: Optional[sqlite3.Connection] = None,
) -> dict:
    """Envia um evento pela API de Conversões. Nunca levanta exceção."""
    if not config.capi_ativa:
        return {"enviado": False, "motivo": "CAPI não configurada"}

    evento = {
        "event_name": nome,
        "event_time": int(time.time()),
        "event_id": event_id,
        "action_source": origem,
        "user_data": user_data,
    }
    if url:
        evento["event_source_url"] = url
    if custom_data:
        evento["custom_data"] = custom_data

    corpo: dict[str, Any] = {"data": [evento]}
    if config.meta_test_event_code:
        corpo["test_event_code"] = config.meta_test_event_code

    endereco = (
        f"https://graph.facebook.com/{config.meta_api_versao}/"
        f"{config.meta_pixel_id}/events?access_token={config.meta_capi_token}"
    )

    try:
        import httpx

        resposta = httpx.post(endereco, json=corpo, timeout=TEMPO_LIMITE)
        ok = resposta.status_code == 200
        resultado = {
            "enviado": ok,
            "status": resposta.status_code,
            "resposta": resposta.text[:400],
        }
    except Exception as exc:  # pragma: no cover - depende de rede
        resultado = {"enviado": False, "erro": str(exc)[:300]}

    if con is not None:
        _registrar(con, nome, event_id, resultado)
    return resultado


def _registrar(con: sqlite3.Connection, nome: str, event_id: str, resultado: dict) -> None:
    """Guarda o envio junto dos webhooks — é lá que se depura integração."""
    try:
        executar(
            con,
            """INSERT INTO webhooks (provedor, evento_id, tipo, assinatura_ok, payload, resultado)
               VALUES (?,?,?,?,?,?)""",
            (
                "meta-capi",
                f"capi-{event_id}",
                nome,
                1 if resultado.get("enviado") else 0,
                json.dumps(resultado, ensure_ascii=False)[:2000],
                "evento enviado" if resultado.get("enviado") else "falha no envio",
            ),
        )
    except Exception:  # pragma: no cover - registro nunca derruba o fluxo
        pass


# --- eventos do funil ------------------------------------------------------


def compra_aprovada(
    con: sqlite3.Connection,
    aluno,
    referencia: str,
    valor: float,
    plano_nome: str = "",
) -> dict:
    return enviar_evento(
        "Purchase",
        event_id=f"compra-{referencia}",
        user_data=dados_do_usuario(
            email=aluno["email"],
            telefone=aluno["telefone"] or "",
            nome=aluno["nome"],
            aluno_id=int(aluno["id"]),
        ),
        custom_data={
            "currency": "BRL",
            "value": round(float(valor or 0), 2),
            "content_name": plano_nome or config.app_nome,
            "content_type": "product",
        },
        origem="website",
        url=f"{config.app_url}/",
        con=con,
    )


def acesso_ativado(con: sqlite3.Connection, aluno) -> dict:
    return enviar_evento(
        "CompleteRegistration",
        event_id=f"ativacao-{aluno['id']}",
        user_data=dados_do_usuario(
            email=aluno["email"],
            nome=aluno["nome"],
            aluno_id=int(aluno["id"]),
        ),
        custom_data={"status": "conta ativada"},
        origem="website",
        url=f"{config.app_url}/painel",
        con=con,
    )


def reembolso(con: sqlite3.Connection, aluno, referencia: str, valor: float) -> dict:
    """O Meta não tem evento nativo de estorno; usamos um evento próprio."""
    return enviar_evento(
        "Refund",
        event_id=f"reembolso-{referencia}",
        user_data=dados_do_usuario(email=aluno["email"], aluno_id=int(aluno["id"])),
        custom_data={"currency": "BRL", "value": round(float(valor or 0), 2)},
        origem="system_generated",
        con=con,
    )
