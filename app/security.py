"""Senhas, sessões assinadas, CSRF, tokens de e-mail e proteção contra força bruta."""

from __future__ import annotations

import base64
import hashlib
import hmac
import re
import secrets
import sqlite3
import unicodedata
from datetime import datetime, timedelta, timezone
from typing import Optional

from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from .config import config
from .db import buscar_um, executar, valor

ITERACOES = 260_000
ALGORITMO = "pbkdf2_sha256"
COOKIE_SESSAO = "map_sessao"
COOKIE_CSRF = "map_csrf"

MAX_TENTATIVAS = 8
JANELA_TENTATIVAS_MIN = 15


# --- data/hora -------------------------------------------------------------


def agora() -> datetime:
    return datetime.now(timezone.utc)


def agora_txt() -> str:
    return agora().strftime("%Y-%m-%d %H:%M:%S")


def hoje_txt() -> str:
    return agora().strftime("%Y-%m-%d")


def ler_data(texto: Optional[str]) -> Optional[datetime]:
    if not texto:
        return None
    texto = texto.strip()
    for formato in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(texto, formato).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


# --- senhas ----------------------------------------------------------------


def gerar_hash_senha(senha: str) -> str:
    sal = secrets.token_bytes(16)
    derivada = hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), sal, ITERACOES)
    return "$".join(
        [
            ALGORITMO,
            str(ITERACOES),
            base64.b64encode(sal).decode(),
            base64.b64encode(derivada).decode(),
        ]
    )


def conferir_senha(senha: str, armazenado: str) -> bool:
    if not armazenado or armazenado.count("$") != 3:
        return False
    algoritmo, iteracoes, sal_b64, hash_b64 = armazenado.split("$")
    if algoritmo != ALGORITMO:
        return False
    try:
        sal = base64.b64decode(sal_b64)
        esperado = base64.b64decode(hash_b64)
        calculado = hashlib.pbkdf2_hmac("sha256", senha.encode("utf-8"), sal, int(iteracoes))
    except (ValueError, TypeError):
        return False
    return hmac.compare_digest(calculado, esperado)


FORCA_MINIMA = 8


def validar_senha(senha: str) -> Optional[str]:
    """Retorna a mensagem de erro, ou None se a senha for aceitável."""
    if len(senha) < FORCA_MINIMA:
        return f"A senha precisa ter pelo menos {FORCA_MINIMA} caracteres."
    if senha.isdigit():
        return "A senha não pode ser só números."
    if senha.lower() in {"12345678", "senha123", "password", "aprovacao"}:
        return "Essa senha é muito comum. Escolha outra."
    return None


# --- e-mail ----------------------------------------------------------------

_RE_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[a-zA-Z]{2,}$")


def normalizar_email(email: str) -> str:
    return (email or "").strip().lower()


def email_valido(email: str) -> bool:
    return bool(_RE_EMAIL.match(normalizar_email(email)))


def primeiro_nome(nome: str) -> str:
    partes = (nome or "").strip().split()
    return partes[0] if partes else "Candidato"


def sem_acentos(texto: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", texto or "") if unicodedata.category(c) != "Mn"
    )


# --- tokens de ativação / recuperação --------------------------------------


def gerar_token() -> str:
    return secrets.token_urlsafe(32)


def hash_token(token: str) -> str:
    return hashlib.sha256(f"{config.secret_key}:{token}".encode("utf-8")).hexdigest()


def criar_token(con: sqlite3.Connection, aluno_id: int, tipo: str, horas: int = 72) -> str:
    token = gerar_token()
    executar(
        con,
        "UPDATE tokens SET usado_em = ? WHERE aluno_id = ? AND tipo = ? AND usado_em IS NULL",
        (agora_txt(), aluno_id, tipo),
    )
    executar(
        con,
        "INSERT INTO tokens (aluno_id, tipo, token_hash, expira_em) VALUES (?,?,?,?)",
        (
            aluno_id,
            tipo,
            hash_token(token),
            (agora() + timedelta(hours=horas)).strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )
    return token


def consumir_token(con: sqlite3.Connection, token: str, tipo: str) -> Optional[int]:
    """Valida o token e o marca como usado. Retorna o id do aluno."""
    linha = buscar_um(
        con,
        "SELECT id, aluno_id, expira_em, usado_em FROM tokens WHERE token_hash = ? AND tipo = ?",
        (hash_token(token), tipo),
    )
    if linha is None or linha["usado_em"]:
        return None
    expira = ler_data(linha["expira_em"])
    if expira is None or expira < agora():
        return None
    executar(con, "UPDATE tokens SET usado_em = ? WHERE id = ?", (agora_txt(), linha["id"]))
    return int(linha["aluno_id"])


# --- sessões ---------------------------------------------------------------

_serializador = URLSafeTimedSerializer(config.secret_key, salt="sessao-aluno")


def abrir_sessao(con: sqlite3.Connection, aluno_id: int, user_agent: str = "", ip: str = "") -> str:
    sessao_id = secrets.token_urlsafe(24)
    expira = (agora() + timedelta(days=config.sessao_dias)).strftime("%Y-%m-%d %H:%M:%S")
    executar(
        con,
        "INSERT INTO sessoes (id, aluno_id, expira_em, user_agent, ip) VALUES (?,?,?,?,?)",
        (sessao_id, aluno_id, expira, user_agent[:250], ip[:60]),
    )
    return _serializador.dumps({"s": sessao_id, "a": aluno_id})


def ler_cookie_sessao(cookie: str) -> Optional[dict]:
    try:
        return _serializador.loads(cookie, max_age=config.sessao_dias * 86400)
    except (BadSignature, SignatureExpired):
        return None


def fechar_sessao(con: sqlite3.Connection, sessao_id: str) -> None:
    executar(con, "UPDATE sessoes SET revogada = 1 WHERE id = ?", (sessao_id,))


def revogar_sessoes_do_aluno(con: sqlite3.Connection, aluno_id: int) -> None:
    executar(con, "UPDATE sessoes SET revogada = 1 WHERE aluno_id = ?", (aluno_id,))


# --- CSRF ------------------------------------------------------------------


def gerar_csrf() -> str:
    return secrets.token_urlsafe(24)


def csrf_valido(enviado: str, cookie: str) -> bool:
    return bool(enviado) and bool(cookie) and hmac.compare_digest(enviado, cookie)


# --- força bruta -----------------------------------------------------------


def registrar_tentativa(con: sqlite3.Connection, email: str, ip: str, sucesso: bool) -> None:
    executar(
        con,
        "INSERT INTO tentativas_login (email, ip, sucesso) VALUES (?,?,?)",
        (normalizar_email(email), ip[:60], 1 if sucesso else 0),
    )


def bloqueado_por_tentativas(con: sqlite3.Connection, email: str, ip: str) -> bool:
    limite = (agora() - timedelta(minutes=JANELA_TENTATIVAS_MIN)).strftime("%Y-%m-%d %H:%M:%S")
    falhas = valor(
        con,
        """SELECT COUNT(*) FROM tentativas_login
           WHERE sucesso = 0 AND criado_em > ? AND (email = ? OR (ip <> '' AND ip = ?))""",
        (limite, normalizar_email(email), ip[:60]),
    )
    return int(falhas) >= MAX_TENTATIVAS


def assinatura_hmac(corpo: bytes, segredo: str) -> str:
    return hmac.new(segredo.encode("utf-8"), corpo, hashlib.sha256).hexdigest()
