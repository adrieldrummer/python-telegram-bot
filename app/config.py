"""Configuração da plataforma, lida de variáveis de ambiente / arquivo .env."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def _carregar_env(caminho: Path) -> None:
    """Lê um .env simples (CHAVE=valor) sem depender de bibliotecas externas."""
    if not caminho.exists():
        return
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#") or "=" not in linha:
            continue
        chave, _, valor = linha.partition("=")
        chave = chave.strip()
        valor = valor.strip().strip('"').strip("'")
        os.environ.setdefault(chave, valor)


_carregar_env(RAIZ / ".env")


def _bool(nome: str, padrao: bool) -> bool:
    valor = os.getenv(nome)
    if valor is None or valor == "":
        return padrao
    return valor.strip().lower() in {"1", "true", "sim", "yes", "on"}


def _int(nome: str, padrao: int) -> int:
    try:
        return int(os.getenv(nome, "") or padrao)
    except ValueError:
        return padrao


@dataclass(frozen=True)
class Config:
    # Produto
    app_nome: str = os.getenv("APP_NOME", "Mapa da Aprovação")
    app_subtitulo: str = os.getenv(
        "APP_SUBTITULO", "Método de 30 dias para Soldado PM 2ª Classe — SP"
    )
    app_url: str = os.getenv("APP_URL", "http://localhost:8000").rstrip("/")
    suporte_email: str = os.getenv("SUPORTE_EMAIL", "suporte@exemplo.com.br")
    suporte_whatsapp: str = os.getenv("SUPORTE_WHATSAPP", "")

    # Segurança
    secret_key: str = os.getenv("SECRET_KEY", "chave-de-desenvolvimento-nao-use-em-producao")
    cookie_seguro: bool = _bool("COOKIE_SEGURO", False)
    sessao_dias: int = _int("SESSAO_DIAS", 30)

    # Banco — com DATABASE_URL definido, a plataforma usa PostgreSQL
    database_url: str = (
        os.getenv("DATABASE_URL", "") or os.getenv("POSTGRES_URL", "")
    ).strip()
    # schema do Postgres (permite conviver com outros produtos no mesmo banco)
    db_schema: str = os.getenv("DB_SCHEMA", "public").strip() or "public"
    banco_caminho: Path = field(
        default_factory=lambda: (RAIZ / os.getenv("BANCO_CAMINHO", "dados/plataforma.db"))
        if not os.path.isabs(os.getenv("BANCO_CAMINHO", "dados/plataforma.db"))
        else Path(os.getenv("BANCO_CAMINHO", "dados/plataforma.db"))
    )

    # E-mail
    smtp_host: str = os.getenv("SMTP_HOST", "")
    smtp_porta: int = _int("SMTP_PORTA", 587)
    smtp_usuario: str = os.getenv("SMTP_USUARIO", "")
    smtp_senha: str = os.getenv("SMTP_SENHA", "")
    smtp_tls: bool = _bool("SMTP_TLS", True)
    email_remetente: str = os.getenv("EMAIL_REMETENTE", "Mapa da Aprovação <nao-responda@localhost>")
    email_responder_para: str = os.getenv("EMAIL_RESPONDER_PARA", "")

    # Cakto
    cakto_checkout_url: str = os.getenv("CAKTO_CHECKOUT_URL", "#")
    cakto_webhook_segredo: str = os.getenv("CAKTO_WEBHOOK_SEGREDO", "")
    cakto_header_assinatura: str = os.getenv("CAKTO_HEADER_ASSINATURA", "x-cakto-signature")
    cakto_permitir_sem_assinatura: bool = _bool("CAKTO_PERMITIR_SEM_ASSINATURA", False)

    # Jornada
    jornada_drip_diario: bool = _bool("JORNADA_DRIP_DIARIO", True)
    custo_chave_antecipacao: int = _int("CUSTO_CHAVE_ANTECIPACAO", 250)
    meta_acerto_missao: int = _int("META_ACERTO_MISSAO", 60)

    @property
    def smtp_configurado(self) -> bool:
        return bool(self.smtp_host)

    @property
    def modo_caixa_saida(self) -> bool:
        """Sem SMTP, os e-mails ficam registrados no banco para consulta no admin."""
        return not self.smtp_configurado


config = Config()
