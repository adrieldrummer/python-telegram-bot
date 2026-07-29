"""A plataforma é usada principalmente no celular — isso precisa ser testado.

Não dá para testar aparência aqui, mas dá para travar as decisões que, se
quebrarem, quebram o celular: o app instalável, o service worker no escopo
certo, a tela de offline e a navegação que só existe para quem está logado.
"""

from __future__ import annotations

import json

from app import alunos as servico_alunos
from app.db import sessao
from tests.conftest import entrar


def criar_conta(email="aluna@teste.com", senha="blindagem30"):
    with sessao() as con:
        servico_alunos.criar(con, "Aluna Teste", email, origem="teste", senha=senha)


def test_manifesto_permite_instalar_na_tela_de_inicio(cliente):
    resposta = cliente.get("/manifest.webmanifest")
    assert resposta.status_code == 200
    dados = json.loads(resposta.text)
    # standalone é o que faz abrir sem a barra do navegador
    assert dados["display"] == "standalone"
    assert dados["start_url"] == "/painel"
    tamanhos = {i["sizes"] for i in dados["icons"]}
    assert {"192x192", "512x512"} <= tamanhos
    # o Android recorta o ícone; sem um "maskable" ele fica com moldura branca
    assert any(i.get("purpose") == "maskable" for i in dados["icons"])


def test_service_worker_vale_para_o_site_inteiro(cliente):
    resposta = cliente.get("/sw.js")
    assert resposta.status_code == 200
    assert "javascript" in resposta.headers["content-type"]
    # servido de /static/ o escopo seria só /static/ — inútil
    assert resposta.headers.get("service-worker-allowed") == "/"
    # respostas de estudo e de pagamento nunca podem sair de cache
    for caminho in ("/api/", "/admin", "/webhooks/"):
        assert caminho in resposta.text


def test_tela_de_offline_abre_sem_login(cliente):
    resposta = cliente.get("/offline")
    assert resposta.status_code == 200
    assert "sem conexão" in resposta.text.lower()


def test_paginas_declaram_viewport_e_area_segura(cliente):
    html = cliente.get("/").text
    assert 'name="viewport"' in html
    # sem viewport-fit=cover o iPhone deixa faixas pretas no entalhe
    assert "viewport-fit=cover" in html
    assert 'rel="manifest"' in html
    assert 'rel="apple-touch-icon"' in html


def test_barra_inferior_so_existe_para_quem_esta_logado(cliente):
    publica = cliente.get("/").text
    assert "barra-inferior" not in publica

    criar_conta()
    entrar(cliente, "aluna@teste.com", "blindagem30")
    painel = cliente.get("/painel").text
    assert "barra-inferior" in painel
    assert "com-barra" in painel          # a classe que abre espaço para a barra
    # os quatro destinos do dia a dia + a gaveta
    for destino in ('href="/painel"', 'href="/jornada"', 'href="/questoes"', 'href="/erros"'):
        assert destino in painel
    assert "abre-gaveta" in painel


def test_robots_protege_area_do_aluno(cliente):
    texto = cliente.get("/robots.txt").text
    for privado in ("/admin", "/painel", "/api/", "/webhooks/"):
        assert f"Disallow: {privado}" in texto
    assert "Sitemap:" in texto


def test_sitemap_lista_apenas_paginas_publicas(cliente):
    xml = cliente.get("/sitemap.xml").text
    assert "<loc>" in xml
    for privado in ("/painel", "/admin", "/conta"):
        assert privado not in xml
