"""Painel administrativo: alunos, acessos, compras, webhooks, e-mails e métricas."""

from __future__ import annotations

from urllib.parse import quote_plus

from fastapi import APIRouter, Depends, Form, HTTPException, Request

from conteudo import TOTAL_QUESTOES, planos as catalogo_planos, simulados as conteudo_simulados, trilha
from conteudo.questoes import total_por_materia

from .. import alunos as servico_alunos
from .. import mailer
from .. import planos as servico_planos
from ..config import config
from ..db import buscar_todos, buscar_um, executar, sessao, valor
from ..deps import exigir_admin, redirecionar, responder_template, validar_csrf
from ..gamificacao import estatisticas
from ..jornada import mapa_prioridades, resumo_jornada
from ..security import email_valido, normalizar_email

router = APIRouter(prefix="/admin")


@router.get("")
async def inicio(request: Request, admin=Depends(exigir_admin)):
    with sessao() as con:
        totais = {
            "alunos": int(valor(con, "SELECT COUNT(*) FROM alunos WHERE admin=0")),
            "ativos": int(valor(con, "SELECT COUNT(*) FROM alunos WHERE status='ativo' AND admin=0")),
            "pendentes": int(valor(con, "SELECT COUNT(*) FROM alunos WHERE status='pendente'")),
            "suspensos": int(valor(con, "SELECT COUNT(*) FROM alunos WHERE status='suspenso'")),
            "compras": int(valor(con, "SELECT COUNT(*) FROM compras WHERE status='aprovada'")),
            "receita": float(valor(con, "SELECT COALESCE(SUM(valor),0) FROM compras WHERE status='aprovada'", (), 0.0)),
            "respostas": int(valor(con, "SELECT COUNT(*) FROM respostas")),
            "simulados": int(valor(con, "SELECT COUNT(*) FROM simulados_sessoes WHERE finalizado_em IS NOT NULL")),
            "concluintes": int(valor(con, "SELECT COUNT(*) FROM alunos WHERE concluido_em IS NOT NULL")),
            "emails_fila": int(valor(con, "SELECT COUNT(*) FROM emails WHERE status IN ('na_fila','erro','caixa_saida')")),
        }
        funil = buscar_todos(
            con,
            """SELECT dia, COUNT(*) AS alunos FROM progresso_dias
               WHERE status='concluido' GROUP BY dia ORDER BY dia""",
        )
        recentes = buscar_todos(
            con,
            """SELECT id, nome, email, status, pontos, streak_atual, criado_em, ultimo_login
               FROM alunos WHERE admin=0 ORDER BY id DESC LIMIT 8""",
        )
        webhooks = buscar_todos(
            con, "SELECT * FROM webhooks ORDER BY id DESC LIMIT 5"
        )
        distribuicao = servico_planos.distribuicao(con)
        vencendo = servico_planos.vencendo(con, dias=7)
        ativos_7d = int(
            valor(
                con,
                "SELECT COUNT(DISTINCT aluno_id) FROM respostas WHERE criado_em > datetime('now','-7 day')",
            )
        )
    totais["ativos_7d"] = ativos_7d
    return responder_template(
        request,
        "admin/inicio.html",
        {
            "aluno": admin,
            "totais": totais,
            "funil": funil,
            "recentes": recentes,
            "webhooks": webhooks,
            "distribuicao": distribuicao,
            "vencendo": vencendo,
            "total_dias": trilha.TOTAL_DIAS,
        },
    )


@router.get("/alunos")
async def lista_alunos(request: Request, admin=Depends(exigir_admin), busca: str = "", status: str = ""):
    condicoes = ["1=1"]
    params: list = []
    if busca:
        condicoes.append("(nome LIKE ? OR email LIKE ?)")
        params.extend([f"%{busca}%", f"%{busca}%"])
    if status:
        condicoes.append("status = ?")
        params.append(status)
    with sessao() as con:
        linhas = buscar_todos(
            con,
            f"""SELECT id, nome, email, telefone, status, admin, pontos, streak_atual,
                       criado_em, ativado_em, ultimo_login, origem
                FROM alunos WHERE {' AND '.join(condicoes)}
                ORDER BY id DESC LIMIT 300""",
            params,
        )
    return responder_template(
        request,
        "admin/alunos.html",
        {"aluno": admin, "linhas": linhas, "busca": busca, "status": status},
    )


@router.get("/aluno/{aluno_id}")
async def detalhe_aluno(request: Request, aluno_id: int, admin=Depends(exigir_admin)):
    with sessao() as con:
        alvo = buscar_um(con, "SELECT * FROM alunos WHERE id=?", (aluno_id,))
        if alvo is None:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        stats = estatisticas(con, aluno_id)
        resumo = resumo_jornada(con, aluno_id)
        prioridades = mapa_prioridades(con, aluno_id)
        compras = buscar_todos(con, "SELECT * FROM compras WHERE aluno_id=? ORDER BY id DESC", (aluno_id,))
        emails = buscar_todos(
            con, "SELECT * FROM emails WHERE aluno_id=? ORDER BY id DESC LIMIT 20", (aluno_id,)
        )
        pontos = buscar_todos(
            con, "SELECT * FROM eventos_pontos WHERE aluno_id=? ORDER BY id DESC LIMIT 20", (aluno_id,)
        )
        assinaturas = servico_planos.assinaturas_do_aluno(con, aluno_id)
        plano = servico_planos.resumo(alvo)
    return responder_template(
        request,
        "admin/aluno.html",
        {
            "aluno": admin,
            "alvo": alvo,
            "stats": stats,
            "resumo": resumo,
            "prioridades": prioridades,
            "compras": compras,
            "emails": emails,
            "pontos": pontos,
            "assinaturas": assinaturas,
            "plano": plano,
            "planos": catalogo_planos.PLANOS,
        },
    )


@router.post("/aluno/{aluno_id}/acao")
async def acao_aluno(
    request: Request,
    aluno_id: int,
    acao: str = Form(""),
    motivo: str = Form(""),
    novo_plano: str = Form(""),
    csrf_token: str = Form(""),
    admin=Depends(exigir_admin),
):
    validar_csrf(request, csrf_token)
    with sessao() as con:
        alvo = buscar_um(con, "SELECT * FROM alunos WHERE id=?", (aluno_id,))
        if alvo is None:
            raise HTTPException(status_code=404, detail="Aluno não encontrado")
        if acao == "aprovar":
            servico_alunos.aprovar_acesso(con, alvo)
            aviso = "E-mail de aprovação enviado."
        elif acao == "suspender":
            servico_alunos.suspender(con, aluno_id, motivo or "suspensão manual")
            aviso = "Acesso suspenso."
        elif acao == "reativar":
            servico_alunos.reativar(con, aluno_id)
            aviso = "Acesso reativado."
        elif acao == "plano":
            plano = servico_planos.aplicar(con, aluno_id, novo_plano, "ajuste manual", "manual")
            aviso = f"Plano alterado para {plano.nome}."
        elif acao == "encerrar_plano":
            servico_planos.encerrar_agora(con, aluno_id)
            aviso = "Assinatura encerrada."
        elif acao == "tornar_admin":
            executar(con, "UPDATE alunos SET admin=1 WHERE id=?", (aluno_id,))
            aviso = "Aluno virou administrador."
        elif acao == "remover_admin":
            executar(con, "UPDATE alunos SET admin=0 WHERE id=?", (aluno_id,))
            aviso = "Permissão de administrador removida."
        else:
            aviso = "Ação desconhecida."
    return redirecionar(f"/admin/aluno/{aluno_id}?aviso={aviso.replace(' ', '+')}")


@router.get("/novo")
async def novo_aluno(request: Request, admin=Depends(exigir_admin), aviso: str = ""):
    return responder_template(request, "admin/novo.html", {"aluno": admin, "aviso": aviso})


@router.post("/novo")
async def criar_aluno(
    request: Request,
    nome: str = Form(""),
    email: str = Form(""),
    telefone: str = Form(""),
    csrf_token: str = Form(""),
    admin=Depends(exigir_admin),
):
    validar_csrf(request, csrf_token)
    if not email_valido(email):
        return redirecionar("/admin/novo?aviso=E-mail inválido")
    with sessao() as con:
        alvo = servico_alunos.criar(con, nome, email, telefone, origem="manual")
        servico_alunos.aprovar_acesso(con, alvo)
        servico_alunos.registrar_compra(
            con, int(alvo["id"]), "manual", "aprovada", normalizar_email(email), produto="Liberação manual"
        )
    return redirecionar(f"/admin/aluno/{alvo['id']}?aviso=Acesso+aprovado+e+e-mail+enviado")


@router.get("/compras")
async def compras(request: Request, admin=Depends(exigir_admin)):
    with sessao() as con:
        linhas = buscar_todos(
            con,
            """SELECT c.*, a.nome FROM compras c LEFT JOIN alunos a ON a.id = c.aluno_id
               ORDER BY c.id DESC LIMIT 200""",
        )
    return responder_template(request, "admin/compras.html", {"aluno": admin, "linhas": linhas})


@router.get("/webhooks")
async def webhooks(request: Request, admin=Depends(exigir_admin)):
    with sessao() as con:
        linhas = buscar_todos(con, "SELECT * FROM webhooks ORDER BY id DESC LIMIT 100")
    return responder_template(request, "admin/webhooks.html", {"aluno": admin, "linhas": linhas})


@router.get("/emails")
async def emails(request: Request, admin=Depends(exigir_admin), aviso: str = ""):
    with sessao() as con:
        linhas = buscar_todos(con, "SELECT * FROM emails ORDER BY id DESC LIMIT 100")
    return responder_template(
        request,
        "admin/emails.html",
        {"aluno": admin, "linhas": linhas, "aviso": aviso, "modo_caixa": config.modo_caixa_saida},
    )


@router.get("/email/{email_id}")
async def ver_email(request: Request, email_id: int, admin=Depends(exigir_admin)):
    with sessao() as con:
        linha = buscar_um(con, "SELECT * FROM emails WHERE id=?", (email_id,))
    if linha is None:
        raise HTTPException(status_code=404, detail="E-mail não encontrado")
    return responder_template(request, "admin/email.html", {"aluno": admin, "linha": linha})


@router.post("/emails/processar")
async def processar_emails(request: Request, csrf_token: str = Form(""), admin=Depends(exigir_admin)):
    validar_csrf(request, csrf_token)
    resumo = mailer.processar_fila(limite=50)
    aviso = f"Enviados: {resumo['enviados']} · Erros: {resumo['erros']}"
    if config.modo_caixa_saida:
        aviso = "SMTP não configurado — os e-mails ficam na caixa de saída."
    return redirecionar(f"/admin/emails?aviso={quote_plus(aviso)}")


@router.post("/emails/teste")
async def testar_email(request: Request, csrf_token: str = Form(""), admin=Depends(exigir_admin)):
    """Manda um e-mail de verdade para o próprio administrador.

    Existe porque "as variáveis estão salvas" e "o e-mail chega" são duas
    afirmações diferentes, e só a segunda importa. Senha errada, porta
    bloqueada ou remetente de domínio não verificado só aparecem no momento do
    envio — e a primeira vez que isso pode acontecer não deve ser na compra de
    um cliente.
    """
    validar_csrf(request, csrf_token)
    if not config.smtp_configurado:
        return redirecionar(
            "/admin/emails?aviso=" + quote_plus("SMTP não configurado — não há para onde enviar.")
        )

    corpo = (
        "<p>Se você está lendo isto, o envio de e-mail da "
        f"{config.app_nome} está funcionando.</p>"
        f"<p>Remetente: {config.email_remetente}<br>"
        f"Servidor: {config.smtp_host}:{config.smtp_porta}</p>"
        "<p>Confira se esta mensagem chegou na caixa de entrada e não no spam. "
        "Se caiu no spam, falta verificar o domínio no provedor de envio.</p>"
    )
    with sessao() as con:
        mailer.enfileirar(
            con,
            admin["email"],
            f"Teste de envio — {config.app_nome}",
            corpo,
            tipo="teste",
            aluno_id=int(admin["id"]),
        )
    resumo = mailer.processar_fila(limite=5)

    if resumo["enviados"]:
        aviso = f"E-mail de teste enviado para {admin['email']}. Confira a caixa de entrada e o spam."
    else:
        with sessao() as con:
            falha = buscar_um(
                con, "SELECT erro FROM emails WHERE tipo='teste' ORDER BY id DESC"
            )
        # o texto cru do servidor é o que resolve: "535 authentication failed"
        # e "domain not verified" pedem consertos completamente diferentes
        aviso = f"Falhou: {(falha['erro'] if falha else '') or 'sem detalhe do servidor'}"
    return redirecionar(f"/admin/emails?aviso={quote_plus(aviso)}")


@router.get("/conteudo")
async def conteudo(request: Request, admin=Depends(exigir_admin)):
    return responder_template(
        request,
        "admin/conteudo.html",
        {
            "aluno": admin,
            "dias": trilha.DIAS,
            "fases": trilha.FASES,
            "por_materia": total_por_materia(),
            "total_questoes": TOTAL_QUESTOES,
            "simulados": conteudo_simulados.SIMULADOS,
        },
    )


@router.get("/configuracao")
async def configuracao(request: Request, admin=Depends(exigir_admin)):
    checagens = [
        ("Domínio configurado", config.app_url, not config.app_url.startswith("http://localhost")),
        ("Cookies seguros (HTTPS)", "ativado" if config.cookie_seguro else "desativado", config.cookie_seguro),
        ("Chave secreta trocada", "ok" if len(config.secret_key) > 30 and "desenvolvimento" not in config.secret_key else "usando padrão", "desenvolvimento" not in config.secret_key),
        ("SMTP", config.smtp_host or "não configurado (modo caixa de saída)", config.smtp_configurado),
        ("Checkout Cakto", config.cakto_checkout_url, config.cakto_checkout_url.startswith("http")),
        ("Segredo do webhook Cakto", "configurado" if config.cakto_webhook_segredo else "ausente", bool(config.cakto_webhook_segredo)),
        ("Webhook sem assinatura", "permitido" if config.cakto_permitir_sem_assinatura else "bloqueado", not config.cakto_permitir_sem_assinatura),
        ("Liberação diária (drip)", "ativa" if config.jornada_drip_diario else "ritmo livre", True),
    ]
    return responder_template(
        request,
        "admin/configuracao.html",
        {"aluno": admin, "checagens": checagens, "webhook_url": f"{config.app_url}/webhooks/cakto"},
    )
