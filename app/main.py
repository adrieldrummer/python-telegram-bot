"""Aplicação FastAPI — Operação Aprovação."""

from __future__ import annotations

import mimetypes
import time
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from . import demo, mailer
from .config import config
from .db import criar_esquema
from .deps import responder_template
from .web import admin, aluno, publico, webhooks

_ultimo_flush = 0.0


@asynccontextmanager
async def ciclo_de_vida(app: FastAPI):
    criar_esquema()
    if config.modo_demo:
        demo.preparar()
    yield


app = FastAPI(
    title=config.app_nome,
    description="Plataforma de estudo do método Operação Aprovação",
    docs_url=None,
    redoc_url=None,
    lifespan=ciclo_de_vida,
)

# o WebP não vem registrado em todo ambiente serverless — sem isto, as capas
# são servidas como "application/octet-stream"
mimetypes.add_type("image/webp", ".webp")
mimetypes.add_type("image/svg+xml", ".svg")


class EstaticosComCache(StaticFiles):
    """Arte e CSS mudam raramente: uma semana de cache poupa banda e função.

    Em página de venda paga isso vira dinheiro — sem cache, cada visitante
    baixa as capas de novo e acorda a função a cada requisição.
    """

    def file_response(self, *args, **kwargs):  # type: ignore[override]
        resposta = super().file_response(*args, **kwargs)
        resposta.headers.setdefault("Cache-Control", "public, max-age=604800")
        return resposta


app.mount(
    "/static",
    EstaticosComCache(directory=str(Path(__file__).parent / "static")),
    name="static",
)


PREFIXOS_DE_FUNCAO = ("/api/index", "/api/main")


@app.middleware("http")
async def normalizar_caminho(request: Request, call_next):
    """Aceita o caminho com ou sem o prefixo da função serverless.

    Dependendo de como a hospedagem roteia (rewrite para `/api/index`), a
    aplicação recebe o caminho da função em vez do caminho que o visitante
    pediu. Sem isso, toda rota responderia 404 em produção e funcionaria no
    desenvolvimento — o pior tipo de bug.
    """
    caminho = request.scope.get("path", "")
    for prefixo in PREFIXOS_DE_FUNCAO:
        if caminho == prefixo or caminho.startswith(prefixo + "/"):
            request.scope["path"] = caminho[len(prefixo) :] or "/"
            request.scope["raw_path"] = request.scope["path"].encode()
            break
    return await call_next(request)


@app.middleware("http")
async def escoar_fila_de_email(request: Request, call_next):
    """Envia e-mails pendentes no máximo uma vez por minuto, sem travar a resposta."""
    global _ultimo_flush
    resposta = await call_next(request)
    if config.smtp_configurado and time.time() - _ultimo_flush > 60:
        _ultimo_flush = time.time()
        try:
            mailer.processar_fila(limite=10)
        except Exception:  # pragma: no cover - envio nunca derruba a requisição
            pass
    return resposta


@app.exception_handler(StarletteHTTPException)
@app.exception_handler(HTTPException)
async def tratar_http(request: Request, exc: HTTPException):
    destino = (exc.headers or {}).get("Location")
    if destino:
        return RedirectResponse(destino, status_code=303)
    if request.url.path.startswith("/api/"):
        return JSONResponse({"erro": exc.detail}, status_code=exc.status_code)
    if exc.status_code in (403, 404):
        return responder_template(
            request,
            "erro.html",
            {
                "codigo": exc.status_code,
                "titulo": "Acesso restrito" if exc.status_code == 403 else "Página não encontrada",
                "mensagem": exc.detail if isinstance(exc.detail, str) else "",
            },
            status_code=exc.status_code,
        )
    return JSONResponse({"erro": exc.detail}, status_code=exc.status_code)


app.include_router(publico.router)
app.include_router(aluno.router)
app.include_router(admin.router)
app.include_router(webhooks.router)


@app.get("/saude", include_in_schema=False)
async def saude():
    """Prontidão da instalação, em booleanos.

    Existe para responder de fora uma pergunta que só o servidor sabe: a
    variável de ambiente entrou mesmo? Na Vercel a variável só passa a valer
    depois de um redeploy, e não há sinal disso na tela — dá para salvar a
    chave, achar que acabou, e descobrir na primeira venda que não.

    Só booleanos: nenhum valor de segredo, nenhuma string de conexão. Saber
    que a chave existe não ajuda ninguém a adivinhá-la.
    """
    return {
        "ok": True,
        "app": config.app_nome,
        "versao": config.versao_estaticos,
        "banco_persistente": not config.modo_demo,
        "webhook_protegido": bool(config.cakto_webhook_segredo),
        "email_configurado": config.smtp_configurado,
    }
