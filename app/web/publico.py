"""Páginas públicas: vendas, login, ativação de acesso e recuperação de senha."""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, Form, Request
from fastapi.responses import JSONResponse, PlainTextResponse, RedirectResponse, Response

from conteudo import TOTAL_QUESTOES, edital, modulos as catalogo_modulos, trilha
from conteudo import planos as catalogo_planos

from .. import alunos, mailer, marketing, planos as servico_planos
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
            "ed": edital.resumo(),
            "dias": trilha.DIAS,
            "fases": trilha.FASES,
            "modulos": catalogo_modulos.ordenados(),
            "total_questoes": TOTAL_QUESTOES,
            "checkout": config.cakto_checkout_url,
            "checkouts": servico_planos.checkouts(),
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


# --- aplicativo instalável (PWA), robots e sitemap -------------------------


@router.get("/manifest.webmanifest", include_in_schema=False)
async def manifesto():
    """O que o celular usa para instalar a plataforma na tela de início."""
    return JSONResponse(
        {
            "name": config.app_nome,
            "short_name": "Op. Aprovação",
            "description": config.app_subtitulo,
            "lang": "pt-BR",
            "start_url": "/painel",
            "scope": "/",
            # standalone: abre sem a barra do navegador, com cara de aplicativo
            "display": "standalone",
            "orientation": "portrait",
            "background_color": "#050505",
            "theme_color": "#050505",
            "categories": ["education"],
            "icons": [
                {"src": "/static/img/icone-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
                {"src": "/static/img/icone-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
                {"src": "/static/img/icone-maskable-192.png", "sizes": "192x192", "type": "image/png", "purpose": "maskable"},
                {"src": "/static/img/icone-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
            ],
            "shortcuts": [
                {"name": "Continuar a trilha", "url": "/jornada"},
                {"name": "Treinar questões", "url": "/questoes"},
                {"name": "Caderno de Erros", "url": "/erros"},
            ],
        },
        media_type="application/manifest+json",
        headers={"Cache-Control": "public, max-age=86400"},
    )


@router.get("/sw.js", include_in_schema=False)
async def serviceworker():
    """O service worker precisa ser servido da raiz para valer no site inteiro.

    Em /static/sw.js o escopo dele seria só /static/ — inútil.
    """
    arquivo = Path(__file__).resolve().parent.parent / "static" / "sw.js"
    return Response(
        arquivo.read_text(encoding="utf-8"),
        media_type="application/javascript",
        headers={"Cache-Control": "no-cache", "Service-Worker-Allowed": "/"},
    )


@router.get("/offline", include_in_schema=False)
async def offline(request: Request):
    return responder_template(request, "offline.html", {})


@router.get("/robots.txt", include_in_schema=False)
async def robots():
    # a área do aluno e o admin não têm nada a fazer em buscador
    linhas = [
        "User-agent: *",
        "Allow: /$",
        "Disallow: /admin",
        "Disallow: /painel",
        "Disallow: /api/",
        "Disallow: /webhooks/",
        "Disallow: /ativar/",
        "Disallow: /redefinir/",
        "",
        f"Sitemap: {config.app_url}/sitemap.xml",
        "",
    ]
    return PlainTextResponse("\n".join(linhas))


@router.get("/sitemap.xml", include_in_schema=False)
async def sitemap():
    publicas = ("/", "/entrar", "/termos", "/privacidade")
    urls = "".join(
        f"<url><loc>{config.app_url}{caminho}</loc>"
        f"<changefreq>{'daily' if caminho == '/' else 'yearly'}</changefreq>"
        f"<priority>{'1.0' if caminho == '/' else '0.3'}</priority></url>"
        for caminho in publicas
    )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f"{urls}</urlset>"
    )
    return Response(xml, media_type="application/xml")
