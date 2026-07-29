"""Pixel do Meta e API de Conversões."""

from __future__ import annotations

import hashlib

from app import marketing
from app.config import config
from tests.conftest import entrar


def com_pixel(pixel: str = "", token: str = ""):
    object.__setattr__(config, "meta_pixel_id", pixel)
    object.__setattr__(config, "meta_capi_token", token)


def test_dados_do_usuario_vao_com_hash():
    dados = marketing.dados_do_usuario(
        email="Maria@Teste.com ", telefone="(11) 98888-7777", nome="Maria Silva", aluno_id=7
    )
    assert dados["em"] == [hashlib.sha256(b"maria@teste.com").hexdigest()]
    assert dados["ph"] == [hashlib.sha256(b"5511988887777").hexdigest()]
    assert dados["fn"] == [hashlib.sha256(b"maria").hexdigest()]
    assert dados["ln"] == [hashlib.sha256(b"silva").hexdigest()]
    assert dados["external_id"] == [hashlib.sha256(b"7").hexdigest()]
    # nada em texto puro
    assert "maria@teste.com" not in str(dados)


def test_dados_do_usuario_ignora_campos_vazios():
    assert marketing.dados_do_usuario() == {}


def test_capi_desligada_nao_envia_nada():
    com_pixel("", "")
    resultado = marketing.enviar_evento("Purchase", "x", {"em": ["abc"]})
    assert resultado["enviado"] is False
    assert "não configurada" in resultado["motivo"]


def test_pixel_so_aparece_quando_configurado(cliente):
    com_pixel("", "")
    assert "connect.facebook.net" not in cliente.get("/").text

    com_pixel("123456789", "")
    pagina = cliente.get("/").text
    assert "connect.facebook.net" in pagina
    assert "fbq('init', '123456789')" in pagina
    assert "data-checkout" in pagina        # botões marcados para InitiateCheckout
    com_pixel("", "")


def test_verificacao_de_dominio_aparece_quando_configurada(cliente):
    object.__setattr__(config, "meta_verificacao_dominio", "abc123")
    assert 'name="facebook-domain-verification" content="abc123"' in cliente.get("/").text
    object.__setattr__(config, "meta_verificacao_dominio", "")


def test_evento_de_compra_tem_id_estavel(con, aluno, monkeypatch):
    """O mesmo evento server-side e browser-side precisa deduplicar no Meta."""
    enviados = []

    def falso(nome, event_id, user_data, custom_data=None, origem="website", url="", con=None):
        enviados.append({"nome": nome, "event_id": event_id, "custom": custom_data})
        return {"enviado": True}

    monkeypatch.setattr(marketing, "enviar_evento", falso)
    marketing.compra_aprovada(con, aluno, "tx-123", 197.0, "Operação Completa")
    assert enviados[0]["nome"] == "Purchase"
    assert enviados[0]["event_id"] == "compra-tx-123"
    assert enviados[0]["custom"]["value"] == 197.0
    assert enviados[0]["custom"]["currency"] == "BRL"
