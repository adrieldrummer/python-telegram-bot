"""Páginas públicas: vendas, login, ativação de acesso e recuperação de senha."""

from __future__ import annotations

from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse

from conteudo import TOTAL_QUESTOES, trilha
from conteudo import planos as catalogo_planos

from .. import alunos, mailer, marketing
from ..config import config
from ..db import buscar_um, sessao
from ..deps import (
    aluno_da_requisicao,
    ip_do,
    redirecionar,
    responder_template,
    validar_csrf,
)
from ..jornada import iniciar_jornada
from ..security import (
    COOKIE_SESSAO,
    abrir_sessao,
    bloqueado_por_tentativas,
    consumir_token,
    criar_token,
    email_valido,
    fechar_sessao,
    hash_token,
    ler_cookie_sessao,
    normalizar_email,
    registrar_tentativa,
    validar_senha,
)

router = APIRouter()


@router.get("/")
async def vendas(request: Request):
    if aluno_da_requisicao(request) is not None:
        return redirecionar("/painel")
    return responder_template(
        request,
        "vendas.html",
        {
            "fases": trilha.FASES,
            "total_questoes": TOTAL_QUESTOES,
            "checkout": config.cakto_checkout_url,
            "planos": catalogo_planos.PLANOS,
        },
    )


@router.get("/entrar")
async def entrar(request: Request, proximo: str = "/painel", erro: str = ""):
    if aluno_da_requisicao(request) is not None:
        return redirecionar("/painel")
    return responder_template(request, "entrar.html", {"proximo": proximo, "erro": erro})


@router.post("/entrar")
async def entrar_post(
    request: Request,
    email: str = Form(""),
    senha: str = Form(""),
    proximo: str = Form("/painel"),
    csrf_token: str = Form(""),
):
    validar_csrf(request, csrf_token)
    ip = ip_do(request)
    with sessao() as con:
        if bloqueado_por_tentativas(con, email, ip):
            return responder_template(
                request,
                "entrar.html",
                {
                    "proximo": proximo,
                    "erro": "Muitas tentativas. Aguarde 15 minutos antes de tentar de novo.",
                    "email": email,
                },
                status_code=429,
            )
        aluno, mensagem = alunos.autenticar(con, email, senha)
        registrar_tentativa(con, email, ip, aluno is not None)
        if aluno is None:
            return responder_template(
                request,
                "entrar.html",
                {"proximo": proximo, "erro": mensagem, "email": email},
                status_code=401,
            )
        iniciar_jornada(con, int(aluno["id"]))
        cookie = abrir_sessao(
            con, int(aluno["id"]), request.headers.get("user-agent", ""), ip
        )

    destino = proximo if proximo.startswith("/") else "/painel"
    if aluno["admin"] and destino == "/painel":
        destino = "/admin"
    resposta = RedirectResponse(destino, status_code=303)
    resposta.set_cookie(
        COOKIE_SESSAO,
        cookie,
        httponly=True,
        samesite="lax",
        secure=config.cookie_seguro,
        max_age=config.sessao_dias * 86400,
    )
    return resposta


@router.post("/sair")
async def sair(request: Request, csrf_token: str = Form("")):
    validar_csrf(request, csrf_token)
    cookie = request.cookies.get(COOKIE_SESSAO, "")
    dados = ler_cookie_sessao(cookie) if cookie else None
    if dados:
        with sessao() as con:
            fechar_sessao(con, dados.get("s", ""))
    resposta = RedirectResponse("/", status_code=303)
    resposta.delete_cookie(COOKIE_SESSAO)
    return resposta


# --- ativação de acesso (aprovação por e-mail) -----------------------------


@router.get("/ativar/{token}")
async def ativar(request: Request, token: str):
    with sessao() as con:
        linha = buscar_um(
            con,
            """SELECT a.* FROM tokens t JOIN alunos a ON a.id = t.aluno_id
               WHERE t.token_hash = ? AND t.tipo = 'ativacao' AND t.usado_em IS NULL""",
            (hash_token(token),),
        )
    if linha is None:
        return responder_template(
            request,
            "token_invalido.html",
            {
                "titulo": "Link de ativação expirado",
                "mensagem": "Peça um novo link de acesso pelo suporte ou use 'Esqueci minha senha'.",
            },
            status_code=410,
        )
    return responder_template(request, "ativar.html", {"token": token, "email": linha["email"], "nome": linha["nome"]})


@router.post("/ativar/{token}")
async def ativar_post(
    request: Request,
    token: str,
    senha: str = Form(""),
    confirmacao: str = Form(""),
    csrf_token: str = Form(""),
):
    validar_csrf(request, csrf_token)
    if senha != confirmacao:
        return responder_template(
            request, "ativar.html", {"token": token, "erro": "As senhas não conferem."}, status_code=400
        )
    problema = validar_senha(senha)
    if problema:
        return responder_template(
            request, "ativar.html", {"token": token, "erro": problema}, status_code=400
        )

    with sessao() as con:
        aluno_id = consumir_token(con, token, "ativacao")
        if aluno_id is None:
            return responder_template(
                request,
                "token_invalido.html",
                {"titulo": "Link inválido ou já utilizado", "mensagem": "Use 'Esqueci minha senha' para entrar."},
                status_code=410,
            )
        aluno = alunos.ativar(con, aluno_id, senha)
        iniciar_jornada(con, aluno_id)
        if aluno is not None:
            marketing.acesso_ativado(con, aluno)
        cookie = abrir_sessao(con, aluno_id, request.headers.get("user-agent", ""), ip_do(request))

    resposta = RedirectResponse("/painel?boasvindas=1", status_code=303)
    resposta.set_cookie(
        COOKIE_SESSAO,
        cookie,
        httponly=True,
        samesite="lax",
        secure=config.cookie_seguro,
        max_age=config.sessao_dias * 86400,
    )
    return resposta


# --- recuperação de senha --------------------------------------------------


@router.get("/recuperar")
async def recuperar(request: Request):
    return responder_template(request, "recuperar.html", {})


@router.post("/recuperar")
async def recuperar_post(request: Request, email: str = Form(""), csrf_token: str = Form("")):
    validar_csrf(request, csrf_token)
    if email_valido(email):
        with sessao() as con:
            aluno = alunos.por_email(con, email)
            if aluno is not None and aluno["status"] != "suspenso":
                token = criar_token(con, int(aluno["id"]), "recuperacao", horas=6)
                mailer.enviar_recuperacao(con, aluno, token)
    # resposta idêntica em qualquer caso, para não revelar quem é cliente
    return responder_template(
        request,
        "recuperar.html",
        {"enviado": True, "email": normalizar_email(email)},
    )


@router.get("/redefinir/{token}")
async def redefinir(request: Request, token: str):
    return responder_template(request, "redefinir.html", {"token": token})


@router.post("/redefinir/{token}")
async def redefinir_post(
    request: Request,
    token: str,
    senha: str = Form(""),
    confirmacao: str = Form(""),
    csrf_token: str = Form(""),
):
    validar_csrf(request, csrf_token)
    if senha != confirmacao:
        return responder_template(
            request, "redefinir.html", {"token": token, "erro": "As senhas não conferem."}, status_code=400
        )
    problema = validar_senha(senha)
    if problema:
        return responder_template(
            request, "redefinir.html", {"token": token, "erro": problema}, status_code=400
        )
    with sessao() as con:
        aluno_id = consumir_token(con, token, "recuperacao")
        if aluno_id is None:
            return responder_template(
                request,
                "token_invalido.html",
                {"titulo": "Link expirado", "mensagem": "Peça um novo link em 'Esqueci minha senha'."},
                status_code=410,
            )
        alunos.definir_senha(con, aluno_id, senha)
    return redirecionar("/entrar?erro=Senha alterada. Entre com a nova senha.")


@router.get("/termos")
async def termos(request: Request):
    return responder_template(request, "termos.html", {})


@router.get("/privacidade")
async def privacidade(request: Request):
    return responder_template(request, "privacidade.html", {})
