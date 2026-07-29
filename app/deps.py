"""Dependências compartilhadas: sessão do aluno, templates e proteção CSRF."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Optional

from fastapi import HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from conteudo import CAPAS, TOTAL_DIAS, TOTAL_QUESTOES
from conteudo.materias import CATEGORIAS_ERRO, MATERIAS

from .config import config
from .db import buscar_um, sessao
from .gamificacao import resumo_patente
from .security import (
    COOKIE_CSRF,
    COOKIE_SESSAO,
    agora,
    gerar_csrf,
    ler_cookie_sessao,
    ler_data,
    primeiro_nome,
)

templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))
templates.env.globals.update(
    {
        "config": config,
        "CAPAS": CAPAS,
        "MATERIAS": MATERIAS,
        "CATEGORIAS_ERRO": CATEGORIAS_ERRO,
        "TOTAL_DIAS": TOTAL_DIAS,
        "TOTAL_QUESTOES": TOTAL_QUESTOES,
    }
)


def primeiro(nome: str) -> str:
    return primeiro_nome(nome)


templates.env.filters["primeiro_nome"] = primeiro


def ip_do(request: Request) -> str:
    encaminhado = request.headers.get("x-forwarded-for", "")
    if encaminhado:
        return encaminhado.split(",")[0].strip()
    return request.client.host if request.client else ""


def _sessao_valida(con: sqlite3.Connection, cookie: str) -> Optional[sqlite3.Row]:
    dados = ler_cookie_sessao(cookie)
    if not dados:
        return None
    linha = buscar_um(
        con,
        "SELECT * FROM sessoes WHERE id = ? AND revogada = 0",
        (dados.get("s", ""),),
    )
    if linha is None:
        return None
    expira = ler_data(linha["expira_em"])
    if expira is None or expira < agora():
        return None
    return linha


def aluno_da_requisicao(request: Request) -> Optional[sqlite3.Row]:
    """Devolve o aluno logado, ou None. Não levanta exceção."""
    cookie = request.cookies.get(COOKIE_SESSAO, "")
    if not cookie:
        return None
    with sessao() as con:
        linha_sessao = _sessao_valida(con, cookie)
        if linha_sessao is None:
            return None
        aluno = buscar_um(con, "SELECT * FROM alunos WHERE id = ?", (linha_sessao["aluno_id"],))
        if aluno is None or aluno["status"] != "ativo":
            return None
        return aluno


def exigir_aluno(request: Request) -> sqlite3.Row:
    aluno = aluno_da_requisicao(request)
    if aluno is None:
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            headers={"Location": "/entrar?proximo=" + request.url.path},
        )
    return aluno


def exigir_admin(request: Request) -> sqlite3.Row:
    aluno = exigir_aluno(request)
    if not aluno["admin"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso restrito")
    return aluno


def bloqueio_por_plano(request: Request, aluno, recurso: str):
    """Devolve a tela de upgrade quando o plano do aluno não cobre o recurso."""
    from conteudo import planos as catalogo

    from . import planos as servico_planos

    if servico_planos.tem_recurso(aluno, recurso):
        return None
    resumo = servico_planos.resumo(aluno)
    return responder_template(
        request,
        "upgrade.html",
        {
            "aluno": aluno,
            "recurso": recurso,
            "recurso_nome": catalogo.nome_do_recurso(recurso),
            "meu_plano": resumo["plano"],
            "vencido": resumo["vencido"],
            "expira_em": resumo["expira_em"],
            "planos": catalogo.PLANOS,
        },
        status_code=402,
    )


def csrf_do(request: Request) -> str:
    return request.cookies.get(COOKIE_CSRF, "") or gerar_csrf()


def validar_csrf(request: Request, enviado: str) -> None:
    cookie = request.cookies.get(COOKIE_CSRF, "")
    if not cookie or not enviado or cookie != enviado:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sessão expirada. Recarregue a página.")


def responder_template(
    request: Request, nome: str, contexto: Optional[dict] = None, status_code: int = 200
):
    dados = dict(contexto or {})
    dados.setdefault("request", request)
    aluno = dados.get("aluno")
    if aluno is None:
        aluno = aluno_da_requisicao(request)
        dados["aluno"] = aluno
    if aluno is not None:
        dados.setdefault("patente", resumo_patente(int(aluno["pontos"])))
    token = csrf_do(request)
    dados["csrf_token"] = token
    resposta = templates.TemplateResponse(request, nome, dados, status_code=status_code)
    if request.cookies.get(COOKIE_CSRF, "") != token:
        resposta.set_cookie(
            COOKIE_CSRF,
            token,
            httponly=False,
            samesite="lax",
            secure=config.cookie_seguro,
            max_age=config.sessao_dias * 86400,
        )
    return resposta


def redirecionar(destino: str, status_code: int = 303) -> RedirectResponse:
    return RedirectResponse(destino, status_code=status_code)
