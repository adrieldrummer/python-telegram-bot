"""Fluxos de ponta a ponta pela interface."""

from __future__ import annotations

import json
import re
from html import unescape

from app import alunos as servico_alunos
from app.db import sessao
from tests.conftest import entrar


def criar_conta(email="aluna@teste.com", senha="blindagem30", admin=False):
    with sessao() as con:
        servico_alunos.criar(con, "Aluna Teste", email, origem="teste", admin=admin, senha=senha)


def questoes_da_pagina(html: str) -> list[dict]:
    bloco = re.search(r'id="dados-questoes">(.*?)</script>', html, re.S)
    return json.loads(bloco.group(1))


def test_paginas_publicas_abrem(cliente):
    for caminho in ("/", "/entrar", "/recuperar", "/termos", "/privacidade"):
        assert cliente.get(caminho).status_code == 200


def test_pagina_de_vendas_mostra_os_numeros_do_edital(cliente):
    from conteudo import edital, planos as catalogo

    html = cliente.get("/").text
    assert str(edital.VAGAS) in html
    assert edital.BANCA in html
    assert str(edital.TOTAL_QUESTOES_PROVA) in html
    for p in catalogo.PLANOS:
        assert p.nome in html and p.preco in html
    # a oferta de entrada precisa aparecer com o preço prometido
    assert "R$ 47" in html


def test_area_do_aluno_exige_login(cliente):
    resposta = cliente.get("/painel", follow_redirects=False)
    assert resposta.status_code == 303
    assert "/entrar" in resposta.headers["location"]


def test_login_com_senha_errada_falha(cliente):
    criar_conta()
    cliente.get("/entrar")
    csrf = cliente.cookies.get("map_csrf")
    resposta = cliente.post(
        "/entrar", data={"email": "aluna@teste.com", "senha": "errada", "csrf_token": csrf}
    )
    assert resposta.status_code == 401


def test_login_sem_csrf_falha(cliente):
    criar_conta()
    resposta = cliente.post("/entrar", data={"email": "aluna@teste.com", "senha": "blindagem30"})
    assert resposta.status_code == 400


def test_aluno_pendente_nao_entra(cliente):
    with sessao() as con:
        servico_alunos.criar(con, "Pendente", "pendente@teste.com", origem="teste")
    cliente.get("/entrar")
    csrf = cliente.cookies.get("map_csrf")
    resposta = cliente.post(
        "/entrar", data={"email": "pendente@teste.com", "senha": "qualquer123", "csrf_token": csrf}
    )
    assert resposta.status_code == 401


def test_fluxo_completo_do_aluno(cliente):
    criar_conta()
    resposta = entrar(cliente, "aluna@teste.com", "blindagem30")
    assert resposta.status_code == 200
    assert "Dia 1" in resposta.text

    # conta nasce no plano de entrada: essas telas estão liberadas para ela
    for caminho in ("/painel", "/jornada", "/dia/1", "/questoes", "/erros", "/simulados",
                    "/pontos", "/conta", "/modulos", "/planos"):
        assert cliente.get(caminho).status_code == 200, caminho

    # e essas dependem de upgrade
    for caminho in ("/manual", "/certificado", "/modulos/redacao"):
        assert cliente.get(caminho).status_code == 402, caminho

    assert cliente.get("/dia/5").status_code == 403       # dia bloqueado
    assert cliente.get("/simulado/sim-1").status_code == 402
    assert cliente.get("/admin").status_code == 403       # área do admin

    # responde a missão inteira do dia 1 e conclui
    pagina = cliente.get("/dia/1")
    questoes = questoes_da_pagina(pagina.text)
    assert len(questoes) == 20   # diagnóstico do Dia 1
    for q in questoes:
        resposta = cliente.post(
            "/api/responder",
            json={"questao_id": q["id"], "alternativa": q["alternativas"][0]["letra"], "origem": "missao", "dia": 1},
        )
        assert resposta.status_code == 200
        assert "comentario" in resposta.json()

    conclusao = cliente.post("/api/concluir-dia", json={"dia": 1})
    assert conclusao.status_code == 200
    assert conclusao.json()["concluido"]
    assert cliente.get("/dia/2").status_code == 200


def test_concluir_dia_incompleto_e_recusado(cliente):
    criar_conta()
    entrar(cliente, "aluna@teste.com", "blindagem30")
    resposta = cliente.post("/api/concluir-dia", json={"dia": 1})
    assert resposta.status_code == 400
    assert "Faltam" in resposta.json()["erro"]


def test_alternativa_invalida_e_recusada(cliente):
    criar_conta()
    entrar(cliente, "aluna@teste.com", "blindagem30")
    questoes = questoes_da_pagina(cliente.get("/questoes").text)
    resposta = cliente.post(
        "/api/responder", json={"questao_id": questoes[0]["id"], "alternativa": "Z", "origem": "treino"}
    )
    assert resposta.status_code == 400


def test_api_exige_autenticacao(cliente):
    resposta = cliente.post(
        "/api/responder", json={"questao_id": "port-001", "alternativa": "A"}, follow_redirects=False
    )
    assert resposta.status_code in (303, 401, 403)


def test_troca_de_senha_encerra_a_sessao(cliente):
    criar_conta()
    entrar(cliente, "aluna@teste.com", "blindagem30")
    csrf = cliente.cookies.get("map_csrf")
    cliente.post(
        "/conta/senha",
        data={"atual": "blindagem30", "nova": "novasenha30", "confirmacao": "novasenha30", "csrf_token": csrf},
        follow_redirects=True,
    )
    assert cliente.get("/painel", follow_redirects=False).status_code == 303
    assert entrar(cliente, "aluna@teste.com", "novasenha30").status_code == 200


def test_recuperacao_nao_revela_se_email_existe(cliente):
    criar_conta()
    cliente.get("/recuperar")
    csrf = cliente.cookies.get("map_csrf")
    conhecido = cliente.post("/recuperar", data={"email": "aluna@teste.com", "csrf_token": csrf})
    desconhecido = cliente.post("/recuperar", data={"email": "ninguem@teste.com", "csrf_token": csrf})
    assert conhecido.status_code == desconhecido.status_code == 200
    assert "Verifique seu e-mail" in conhecido.text and "Verifique seu e-mail" in desconhecido.text


def test_painel_do_admin(cliente):
    criar_conta("chefe@teste.com", "comandante30", admin=True)
    resposta = entrar(cliente, "chefe@teste.com", "comandante30")
    assert "Administração" in resposta.text
    for caminho in ("/admin", "/admin/alunos", "/admin/compras", "/admin/webhooks", "/admin/emails", "/admin/conteudo", "/admin/configuracao", "/admin/novo"):
        assert cliente.get(caminho).status_code == 200, caminho


def test_admin_libera_acesso_manual(cliente):
    criar_conta("chefe@teste.com", "comandante30", admin=True)
    entrar(cliente, "chefe@teste.com", "comandante30")
    csrf = cliente.cookies.get("map_csrf")
    resposta = cliente.post(
        "/admin/novo",
        data={"nome": "Convidado", "email": "convidado@teste.com", "telefone": "", "csrf_token": csrf},
        follow_redirects=True,
    )
    assert resposta.status_code == 200
    with sessao() as con:
        novo = servico_alunos.por_email(con, "convidado@teste.com")
        assert novo is not None and novo["status"] == "pendente"


def test_simulado_corrigido_explica_cada_erro(cliente):
    """Simulado sem correção comentada é só um número — e número não ensina."""
    from app import estudo, planos as servico_planos
    from app.db import buscar_um, sessao as abrir
    from conteudo.simulados import montar

    criar_conta()
    with abrir() as con:
        alvo = servico_alunos.por_email(con, "aluna@teste.com")
        aluno_id = int(alvo["id"])
        servico_planos.aplicar(con, aluno_id, "operacao")   # simulados liberados

        sessao_id = estudo.iniciar_simulado(con, aluno_id, "sim-diagnostico")
        questoes = montar("sim-diagnostico")
        # acerta a primeira metade, erra a segunda de propósito
        for i, q in enumerate(questoes):
            if i % 2 == 0:
                letra = q.correta
            else:
                letra = next(l for l, _ in q.alternativas if l != q.correta)
            estudo.responder(
                con, aluno_id, q, letra, origem="simulado",
                sessao_id=sessao_id, tempo_seg=20 if i % 4 == 1 else 60,
            )
        estudo.finalizar_simulado(con, aluno_id, sessao_id, 900)
        erradas = [q for i, q in enumerate(questoes) if i % 2 == 1]

    entrar(cliente, "aluna@teste.com", "blindagem30")
    pagina = cliente.get(f"/simulado/sim-diagnostico/relatorio/{sessao_id}")
    assert pagina.status_code == 200
    # aspas e acentos saem escapados no HTML; comparar o texto cru dá falso negativo
    html = unescape(pagina.text)

    assert "Correção comentada" in html
    # toda questão errada precisa trazer gabarito e explicação
    for q in erradas:
        assert q.enunciado[:40] in html, q.id
        assert q.comentario[:40] in html, q.id
    assert "Gabarito" in html and "Você marcou" in html
    # e o aviso de quem respondeu rápido demais
    assert "leitura do enunciado" in html


def test_correcao_do_simulado_cobre_acertos_e_erros(cliente):
    """A correção devolve a prova inteira, não só o que o aluno errou."""
    from app import estudo, planos as servico_planos
    from app.db import sessao as abrir
    from conteudo.simulados import montar

    criar_conta("outra@teste.com")
    with abrir() as con:
        alvo = servico_alunos.por_email(con, "outra@teste.com")
        aluno_id = int(alvo["id"])
        servico_planos.aplicar(con, aluno_id, "operacao")
        sessao_id = estudo.iniciar_simulado(con, aluno_id, "sim-diagnostico")
        questoes = montar("sim-diagnostico")
        for q in questoes:
            estudo.responder(con, aluno_id, q, q.correta, origem="simulado", sessao_id=sessao_id)
        correcao = estudo.correcao_da_sessao(con, aluno_id, sessao_id)

    assert len(correcao) == len(questoes)
    assert all(i["acertou"] for i in correcao)
    assert [i["numero"] for i in correcao] == list(range(1, len(questoes) + 1))
    for item in correcao:
        assert item["texto_gabarito"], item["questao"].id
        assert item["questao"].comentario
