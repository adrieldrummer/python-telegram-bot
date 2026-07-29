"""Fila de e-mails: o que fica guardado precisa sair quando o SMTP aparecer."""

from __future__ import annotations

import smtplib

import pytest

from app import mailer
from app.config import config
from app.db import buscar_um, sessao


class ServidorFalso:
    """Substitui o smtplib nos testes — guarda o que seria enviado."""

    enviados: list = []

    def __init__(self, host, porta, timeout=0):
        self.host = host

    def starttls(self):
        pass

    def login(self, usuario, senha):
        pass

    def send_message(self, msg):
        ServidorFalso.enviados.append(msg)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False


def definir_host(valor: str) -> None:
    """`config` é um dataclass congelado; nos testes ligamos e desligamos o SMTP."""
    object.__setattr__(config, "smtp_host", valor)


@pytest.fixture(autouse=True)
def smtp_limpo():
    original = config.smtp_host
    definir_host("")
    ServidorFalso.enviados = []
    yield
    definir_host(original)


def com_smtp(monkeypatch, host="smtp.teste.com"):
    definir_host(host)
    monkeypatch.setattr(smtplib, "SMTP", ServidorFalso)
    ServidorFalso.enviados = []


def test_email_guardado_sem_smtp_sai_quando_o_smtp_chega(banco, monkeypatch):
    """O caso da virada: quem comprou antes do SMTP não pode ficar sem a senha.

    Enquanto não há SMTP o e-mail é gravado com status `caixa_saida`. Se a fila
    só olhasse `na_fila`, esses e-mails ficariam presos para sempre — e são
    justamente os primeiros compradores, os que menos podem ficar sem acesso.
    """
    with sessao() as con:
        email_id = mailer.enfileirar(
            con, "comprador@teste.com", "Acesso aprovado", "<p>Sua senha: Sierra-4783</p>"
        )
        assert buscar_um(con, "SELECT status FROM emails WHERE id=?", (email_id,))["status"] == "caixa_saida"

    com_smtp(monkeypatch)
    resumo = mailer.processar_fila()

    assert resumo["enviados"] == 1
    assert len(ServidorFalso.enviados) == 1
    assert ServidorFalso.enviados[0]["To"] == "comprador@teste.com"
    with sessao() as con:
        assert buscar_um(con, "SELECT status FROM emails WHERE id=?", (email_id,))["status"] == "enviado"


def test_sem_smtp_nada_e_enviado(banco, monkeypatch):
    with sessao() as con:
        mailer.enfileirar(con, "alguem@teste.com", "Oi", "<p>oi</p>")
    assert mailer.processar_fila() == {"enviados": 0, "erros": 0, "pendentes": 0}


def test_falha_de_conexao_guarda_o_motivo(banco, monkeypatch):
    """O texto cru do servidor é o que diz se é senha errada ou domínio não verificado."""
    with sessao() as con:
        email_id = mailer.enfileirar(con, "alguem@teste.com", "Oi", "<p>oi</p>")

    def explode(*args, **kwargs):
        raise smtplib.SMTPAuthenticationError(535, b"authentication failed")

    definir_host("smtp.teste.com")
    monkeypatch.setattr(smtplib, "SMTP", explode)

    resumo = mailer.processar_fila()
    assert resumo["erros"] == 1
    with sessao() as con:
        linha = buscar_um(con, "SELECT status, erro FROM emails WHERE id=?", (email_id,))
    assert linha["status"] == "erro"
    assert "authentication failed" in linha["erro"]


def test_email_com_erro_para_de_ser_tentado_para_sempre(banco, monkeypatch):
    """Sem teto de tentativas, um endereço inválido travaria a fila toda vez."""
    with sessao() as con:
        email_id = mailer.enfileirar(con, "invalido@teste.com", "Oi", "<p>oi</p>")
        from app.db import executar

        executar(
            con,
            "UPDATE emails SET status='erro', tentativas=? WHERE id=?",
            (mailer.MAX_TENTATIVAS_ENVIO, email_id),
        )

    com_smtp(monkeypatch)
    assert mailer.processar_fila()["enviados"] == 0
    assert ServidorFalso.enviados == []
