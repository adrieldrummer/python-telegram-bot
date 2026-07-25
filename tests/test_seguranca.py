"""Senhas, tokens, sessões e proteção contra força bruta."""

from __future__ import annotations

from app import security
from app.db import buscar_um, executar


def test_hash_de_senha_nao_guarda_texto_puro():
    hash_gerado = security.gerar_hash_senha("minhaSenha123")
    assert "minhaSenha123" not in hash_gerado
    assert hash_gerado.startswith("pbkdf2_sha256$")
    assert security.conferir_senha("minhaSenha123", hash_gerado)
    assert not security.conferir_senha("minhaSenha124", hash_gerado)


def test_hashes_diferentes_para_a_mesma_senha():
    assert security.gerar_hash_senha("igual12345") != security.gerar_hash_senha("igual12345")


def test_conferir_senha_com_hash_invalido():
    assert not security.conferir_senha("qualquer", "")
    assert not security.conferir_senha("qualquer", "formato-errado")


def test_validacao_de_senha():
    assert security.validar_senha("1234567") is not None       # curta
    assert security.validar_senha("123456789") is not None     # só números
    assert security.validar_senha("senha123") is not None      # comum
    assert security.validar_senha("blindagem30") is None


def test_email_valido():
    assert security.email_valido("a@b.com.br")
    assert not security.email_valido("sem-arroba")
    assert not security.email_valido("a@b")
    assert security.normalizar_email("  MARIA@Teste.COM ") == "maria@teste.com"


def test_token_de_ativacao_so_pode_ser_usado_uma_vez(con, aluno):
    token = security.criar_token(con, int(aluno["id"]), "ativacao")
    assert security.consumir_token(con, token, "ativacao") == int(aluno["id"])
    assert security.consumir_token(con, token, "ativacao") is None


def test_token_expirado_nao_vale(con, aluno):
    token = security.criar_token(con, int(aluno["id"]), "recuperacao", horas=1)
    executar(
        con,
        "UPDATE tokens SET expira_em='2000-01-01 00:00:00' WHERE token_hash=?",
        (security.hash_token(token),),
    )
    assert security.consumir_token(con, token, "recuperacao") is None


def test_token_de_tipo_errado_nao_vale(con, aluno):
    token = security.criar_token(con, int(aluno["id"]), "ativacao")
    assert security.consumir_token(con, token, "recuperacao") is None


def test_criar_token_invalida_o_anterior(con, aluno):
    primeiro = security.criar_token(con, int(aluno["id"]), "ativacao")
    security.criar_token(con, int(aluno["id"]), "ativacao")
    assert security.consumir_token(con, primeiro, "ativacao") is None


def test_bloqueio_por_tentativas(con):
    for _ in range(security.MAX_TENTATIVAS):
        security.registrar_tentativa(con, "alvo@teste.com", "1.2.3.4", False)
    assert security.bloqueado_por_tentativas(con, "alvo@teste.com", "1.2.3.4")
    assert not security.bloqueado_por_tentativas(con, "outro@teste.com", "9.9.9.9")


def test_sessao_pode_ser_revogada(con, aluno):
    cookie = security.abrir_sessao(con, int(aluno["id"]))
    dados = security.ler_cookie_sessao(cookie)
    assert dados and dados["a"] == int(aluno["id"])
    security.revogar_sessoes_do_aluno(con, int(aluno["id"]))
    linha = buscar_um(con, "SELECT revogada FROM sessoes WHERE id=?", (dados["s"],))
    assert linha["revogada"] == 1


def test_cookie_de_sessao_adulterado_nao_e_aceito(con, aluno):
    cookie = security.abrir_sessao(con, int(aluno["id"]))
    assert security.ler_cookie_sessao(cookie + "x") is None


def test_assinatura_hmac_do_webhook():
    esperado = security.assinatura_hmac(b'{"a":1}', "segredo")
    assert esperado == security.assinatura_hmac(b'{"a":1}', "segredo")
    assert esperado != security.assinatura_hmac(b'{"a":2}', "segredo")
