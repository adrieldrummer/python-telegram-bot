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


def _caminho_do_banco() -> Path:
    """Onde fica o arquivo SQLite.

    Em hospedagem serverless o projeto é somente leitura: a única pasta
    gravável é /tmp. Isso mantém o primeiro deploy funcionando mesmo antes de
    o Postgres estar configurado (modo demonstração).
    """
    bruto = os.getenv("BANCO_CAMINHO", "")
    if bruto:
        caminho = Path(bruto)
        return caminho if caminho.is_absolute() else RAIZ / caminho
    if os.getenv("VERCEL") or os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
        return Path("/tmp/mapa-demo.db")
    return RAIZ / "dados" / "plataforma.db"


@dataclass(frozen=True)
class Config:
    # Produto
    app_nome: str = os.getenv("APP_NOME", "Operação Aprovação")
    app_assinatura: str = os.getenv("APP_ASSINATURA", "Sua missão começa agora.")
    app_subtitulo: str = os.getenv(
        "APP_SUBTITULO", "O edital do Soldado PM-SP 2026 explicado em 7 dias"
    )
    app_url: str = os.getenv("APP_URL", "http://localhost:8000").rstrip("/")
    suporte_email: str = os.getenv("SUPORTE_EMAIL", "suporte@opaprova.com")
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
    banco_caminho: Path = field(default_factory=lambda: _caminho_do_banco())

    # E-mail
    smtp_host: str = os.getenv("SMTP_HOST", "")
    smtp_porta: int = _int("SMTP_PORTA", 587)
    smtp_usuario: str = os.getenv("SMTP_USUARIO", "")
    smtp_senha: str = os.getenv("SMTP_SENHA", "")
    smtp_tls: bool = _bool("SMTP_TLS", True)
    email_remetente: str = os.getenv("EMAIL_REMETENTE", "Operação Aprovação <nao-responda@localhost>")
    email_responder_para: str = os.getenv("EMAIL_RESPONDER_PARA", "")

    # Cakto
    cakto_checkout_url: str = os.getenv("CAKTO_CHECKOUT_URL", "#")
    cakto_webhook_segredo: str = os.getenv("CAKTO_WEBHOOK_SEGREDO", "")
    cakto_header_assinatura: str = os.getenv("CAKTO_HEADER_ASSINATURA", "x-cakto-signature")
    cakto_permitir_sem_assinatura: bool = _bool("CAKTO_PERMITIR_SEM_ASSINATURA", False)

    def checkout_do_plano(self, plano_id: str) -> str:
        """Link de checkout de um plano.

        Cada plano tem seu próprio produto na Cakto, então cada um tem seu link:
        `CAKTO_CHECKOUT_RECRUTA`, `CAKTO_CHECKOUT_OPERACAO`, `CAKTO_CHECKOUT_ELITE`.
        Enquanto o link do plano não existir, cai no checkout geral — assim a
        página de vendas nunca aponta para lugar nenhum.
        """
        chave = f"CAKTO_CHECKOUT_{(plano_id or '').upper().replace('-', '_')}"
        return (os.getenv(chave, "") or "").strip() or self.cakto_checkout_url

    # Meta (Facebook/Instagram) — pixel do navegador + API de Conversões
    meta_pixel_id: str = os.getenv("META_PIXEL_ID", "").strip()
    meta_capi_token: str = os.getenv("META_CAPI_TOKEN", "").strip()
    meta_test_event_code: str = os.getenv("META_TEST_EVENT_CODE", "").strip()
    meta_api_versao: str = os.getenv("META_API_VERSAO", "v21.0").strip()
    # O código de verificação de domínio do Meta é público por natureza: ele é
    # publicado numa meta tag lida por qualquer visitante do site. Fica aqui
    # como padrão para não depender de variável de ambiente — perder essa
    # verificação custa atribuição de venda no iOS, e ela é o tipo de coisa
    # que some num deploy e ninguém percebe.
    meta_verificacao_dominio: str = os.getenv(
        "META_VERIFICACAO_DOMINIO", "2weeeqmpolfisxw5vahq414ugzt9qe"
    ).strip()

    # Jornada
    jornada_drip_diario: bool = _bool("JORNADA_DRIP_DIARIO", True)
    custo_chave_antecipacao: int = _int("CUSTO_CHAVE_ANTECIPACAO", 250)
    meta_acerto_missao: int = _int("META_ACERTO_MISSAO", 60)

    @property
    def versao_estaticos(self) -> str:
        """Identificador que muda a cada publicação.

        CSS e JS são servidos com uma semana de cache — sem isso cada visitante
        rebaixa as capas e acorda a função. Mas cache longo em URL fixa prende o
        visitante na versão antiga por uma semana inteira: foi o que aconteceu
        quando o relógio regressivo entrou e ninguém viu.

        A solução é a URL carregar a versão (`app.css?v=abc123`). Na Vercel, o
        SHA do commit já serve; fora dela, a data de modificação dos arquivos.
        """
        sha = os.getenv("VERCEL_GIT_COMMIT_SHA", "").strip()
        if sha:
            return sha[:10]
        try:
            estaticos = RAIZ / "app" / "static"
            recente = max(
                arquivo.stat().st_mtime
                for arquivo in estaticos.rglob("*")
                if arquivo.is_file() and arquivo.suffix in {".css", ".js"}
            )
            return str(int(recente))
        except (ValueError, OSError):
            return "dev"

    @property
    def serverless(self) -> bool:
        """True quando roda em plataforma sem disco persistente (Vercel/Lambda)."""
        return bool(os.getenv("VERCEL") or os.getenv("AWS_LAMBDA_FUNCTION_NAME"))

    @property
    def modo_demo(self) -> bool:
        """Serverless sem Postgres: sobe, funciona, mas zera a cada reinício.

        Serve para o primeiro deploy funcionar antes de você configurar o
        banco. Assim que `DATABASE_URL` existir, o modo demonstração some
        sozinho e os dados passam a persistir.
        """
        return self.serverless and not self.database_url

    @property
    def pixel_ativo(self) -> bool:
        return bool(self.meta_pixel_id)

    @property
    def capi_ativa(self) -> bool:
        """Eventos server-side sobrevivem a bloqueador de anúncio e iOS."""
        return bool(self.meta_pixel_id and self.meta_capi_token)

    @property
    def smtp_configurado(self) -> bool:
        return bool(self.smtp_host)

    @property
    def smtp_senha_plausivel(self) -> bool:
        """A senha SMTP tem cara de credencial, e não de erro de cópia.

        Não valida a credencial — só descarta os enganos que a Vercel não tem
        como pegar: campo vazio, os pontinhos da máscara copiados no lugar do
        valor, espaço colado junto, ou uma chave cortada pela metade. Sem isso
        a única pista é um `535` do servidor, que não distingue "chave errada"
        de "chave colada errado" — e a variável fica marcada como Sensitive,
        então nem quem configurou consegue reler o que salvou.
        """
        senha = self.smtp_senha
        if not senha or len(senha) < 12:
            return False
        if senha != senha.strip() or any(c.isspace() for c in senha):
            return False
        return not any(c in senha for c in "•●*…")

    @property
    def modo_caixa_saida(self) -> bool:
        """Sem SMTP, os e-mails ficam registrados no banco para consulta no admin."""
        return not self.smtp_configurado


config = Config()
