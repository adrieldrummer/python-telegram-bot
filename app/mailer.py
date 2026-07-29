"""Fila de e-mails: enfileira no banco e envia por SMTP.

Sem SMTP configurado a plataforma entra em *modo caixa de saída*: nada é
perdido, tudo fica gravado e visível em /admin/emails — útil em
desenvolvimento e para conferir o texto antes de ligar o domínio.
"""

from __future__ import annotations

import html
import re
import smtplib
import sqlite3
from email.message import EmailMessage
from email.utils import formataddr, parseaddr
from pathlib import Path
from typing import Any, Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .config import config
from .db import buscar_todos, executar, sessao
from .security import agora_txt, primeiro_nome

_ambiente = Environment(
    loader=FileSystemLoader(str(Path(__file__).parent / "templates")),
    autoescape=select_autoescape(["html"]),
)

MAX_TENTATIVAS_ENVIO = 4


def _texto_simples(corpo_html: str) -> str:
    texto = re.sub(r"<(style|script).*?</\1>", "", corpo_html, flags=re.S | re.I)
    texto = re.sub(r"<br\s*/?>", "\n", texto, flags=re.I)
    texto = re.sub(r"</(p|div|h1|h2|h3|li|tr)>", "\n", texto, flags=re.I)
    texto = re.sub(r"<[^>]+>", "", texto)
    texto = html.unescape(texto)
    return re.sub(r"\n{3,}", "\n\n", texto).strip()


def renderizar(modelo: str, **contexto: Any) -> str:
    contexto.setdefault("config", config)
    return _ambiente.get_template(f"emails/{modelo}.html").render(**contexto)


def enfileirar(
    con: sqlite3.Connection,
    destinatario: str,
    assunto: str,
    corpo_html: str,
    tipo: str = "geral",
    aluno_id: Optional[int] = None,
) -> int:
    cur = executar(
        con,
        """INSERT INTO emails (aluno_id, destinatario, assunto, corpo_html, corpo_texto, tipo, status)
           VALUES (?,?,?,?,?,?,?)""",
        (
            aluno_id,
            destinatario,
            assunto,
            corpo_html,
            _texto_simples(corpo_html),
            tipo,
            "na_fila" if config.smtp_configurado else "caixa_saida",
        ),
    )
    return int(cur.lastrowid or 0)


def _montar_mensagem(linha: sqlite3.Row) -> EmailMessage:
    msg = EmailMessage()
    nome, endereco = parseaddr(config.email_remetente)
    msg["From"] = formataddr((nome or config.app_nome, endereco or "nao-responda@localhost"))
    msg["To"] = linha["destinatario"]
    msg["Subject"] = linha["assunto"]
    if config.email_responder_para:
        msg["Reply-To"] = config.email_responder_para
    msg.set_content(linha["corpo_texto"] or _texto_simples(linha["corpo_html"]))
    msg.add_alternative(linha["corpo_html"], subtype="html")
    return msg


def processar_fila(limite: int = 30) -> dict[str, int]:
    """Envia os e-mails pendentes. Retorna um resumo do que aconteceu."""
    resumo = {"enviados": 0, "erros": 0, "pendentes": 0}
    if not config.smtp_configurado:
        return resumo

    with sessao() as con:
        pendentes = buscar_todos(
            con,
            """SELECT * FROM emails
               WHERE status IN ('na_fila','erro') AND tentativas < ?
               ORDER BY id LIMIT ?""",
            (MAX_TENTATIVAS_ENVIO, limite),
        )
        if not pendentes:
            return resumo

        try:
            servidor = smtplib.SMTP(config.smtp_host, config.smtp_porta, timeout=25)
            if config.smtp_tls:
                servidor.starttls()
            if config.smtp_usuario:
                servidor.login(config.smtp_usuario, config.smtp_senha)
        except Exception as exc:  # pragma: no cover - depende de rede
            for linha in pendentes:
                executar(
                    con,
                    "UPDATE emails SET status='erro', tentativas=tentativas+1, erro=? WHERE id=?",
                    (f"conexao: {exc}"[:400], linha["id"]),
                )
            resumo["erros"] = len(pendentes)
            return resumo

        with servidor:
            for linha in pendentes:
                try:
                    servidor.send_message(_montar_mensagem(linha))
                    executar(
                        con,
                        "UPDATE emails SET status='enviado', enviado_em=?, tentativas=tentativas+1, erro='' WHERE id=?",
                        (agora_txt(), linha["id"]),
                    )
                    resumo["enviados"] += 1
                except Exception as exc:  # pragma: no cover - depende de rede
                    executar(
                        con,
                        "UPDATE emails SET status='erro', tentativas=tentativas+1, erro=? WHERE id=?",
                        (str(exc)[:400], linha["id"]),
                    )
                    resumo["erros"] += 1
    return resumo


# --- e-mails do produto ----------------------------------------------------


def enviar_aprovacao(con: sqlite3.Connection, aluno: sqlite3.Row, token: str) -> None:
    """E-mail de APROVAÇÃO: confirma a compra e abre o cadastro de senha."""
    link = f"{config.app_url}/ativar/{token}"
    corpo = renderizar(
        "aprovacao",
        nome=primeiro_nome(aluno["nome"]),
        link=link,
        email=aluno["email"],
    )
    enfileirar(
        con,
        aluno["email"],
        f"✅ Acesso aprovado — {config.app_nome}",
        corpo,
        tipo="aprovacao",
        aluno_id=aluno["id"],
    )


def enviar_boas_vindas(con: sqlite3.Connection, aluno: sqlite3.Row) -> None:
    corpo = renderizar(
        "boas_vindas",
        nome=primeiro_nome(aluno["nome"]),
        link=f"{config.app_url}/painel",
    )
    enfileirar(
        con,
        aluno["email"],
        "Sua conta está ativa — comece pelo Diagnóstico (Dia 1)",
        corpo,
        tipo="boas_vindas",
        aluno_id=aluno["id"],
    )


def enviar_recuperacao(con: sqlite3.Connection, aluno: sqlite3.Row, token: str) -> None:
    corpo = renderizar(
        "recuperacao",
        nome=primeiro_nome(aluno["nome"]),
        link=f"{config.app_url}/redefinir/{token}",
    )
    enfileirar(
        con,
        aluno["email"],
        "Redefinição de senha",
        corpo,
        tipo="recuperacao",
        aluno_id=aluno["id"],
    )


def enviar_dia_concluido(
    con: sqlite3.Connection, aluno: sqlite3.Row, dia: int, titulo_proximo: str, pontos: int
) -> None:
    corpo = renderizar(
        "dia_concluido",
        nome=primeiro_nome(aluno["nome"]),
        dia=dia,
        proximo=dia + 1,
        titulo_proximo=titulo_proximo,
        pontos=pontos,
        streak=aluno["streak_atual"],
        link=f"{config.app_url}/jornada",
    )
    enfileirar(
        con,
        aluno["email"],
        f"Dia {dia} concluído — Dia {dia + 1} liberado 🔓",
        corpo,
        tipo="dia_concluido",
        aluno_id=aluno["id"],
    )


def enviar_conquista(con: sqlite3.Connection, aluno: sqlite3.Row, titulo: str, texto: str) -> None:
    corpo = renderizar(
        "conquista",
        nome=primeiro_nome(aluno["nome"]),
        titulo=titulo,
        texto=texto,
        link=f"{config.app_url}/painel",
    )
    enfileirar(
        con, aluno["email"], f"🎖 {titulo}", corpo, tipo="conquista", aluno_id=aluno["id"]
    )


def enviar_lembrete(con: sqlite3.Connection, aluno: sqlite3.Row, mensagem: str) -> None:
    corpo = renderizar(
        "lembrete",
        nome=primeiro_nome(aluno["nome"]),
        mensagem=mensagem,
        streak=aluno["streak_atual"],
        link=f"{config.app_url}/jornada",
    )
    enfileirar(
        con,
        aluno["email"],
        "Seu bloco de hoje está esperando",
        corpo,
        tipo="lembrete",
        aluno_id=aluno["id"],
    )


def enviar_conclusao(con: sqlite3.Connection, aluno: sqlite3.Row) -> None:
    corpo = renderizar(
        "conclusao",
        nome=primeiro_nome(aluno["nome"]),
        link=f"{config.app_url}/certificado",
    )
    enfileirar(
        con,
        aluno["email"],
        "🏁 Você concluiu o Operação Aprovação",
        corpo,
        tipo="conclusao",
        aluno_id=aluno["id"],
    )


def enviar_acesso_suspenso(con: sqlite3.Connection, aluno: sqlite3.Row, motivo: str) -> None:
    corpo = renderizar("suspensao", nome=primeiro_nome(aluno["nome"]), motivo=motivo)
    enfileirar(
        con,
        aluno["email"],
        "Seu acesso foi suspenso",
        corpo,
        tipo="suspensao",
        aluno_id=aluno["id"],
    )
