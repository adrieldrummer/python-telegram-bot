# Deploy em servidor próprio (VPS)

Uma VPS pequena (1 vCPU / 1 GB) sustenta o produto com folga. Com SQLite não
há banco externo para pagar nem cuidar.

## Docker + HTTPS automático (recomendado)

```bash
git clone <seu-repo> /opt/mapa && cd /opt/mapa
cp .env.example .env && nano .env       # ver checklist abaixo
nano deploy/Caddyfile                   # trocar pelo seu domínio
cd deploy && docker compose up -d --build
```

O Caddy emite e renova o certificado sozinho. Suba o admin inicial:

```bash
docker compose exec plataforma python scripts/seed.py
docker compose exec plataforma python -c "
from app.db import sessao; from app.alunos import definir_senha, por_email
with sessao() as c: definir_senha(c, por_email(c,'admin@teste.com')['id'], 'SUA-SENHA-FORTE')
"
```

## Sem Docker (systemd + nginx)

```bash
apt install python3-venv nginx
python3 -m venv /opt/mapa/.venv && /opt/mapa/.venv/bin/pip install -r requirements.txt
cp deploy/mapa.service /etc/systemd/system/ && systemctl enable --now mapa
cp deploy/nginx.conf /etc/nginx/sites-available/mapa
ln -s /etc/nginx/sites-available/mapa /etc/nginx/sites-enabled/ && systemctl reload nginx
certbot --nginx -d mapadaaprovacao.com.br -d www.mapadaaprovacao.com.br
```

## Checklist do .env antes de vender

- [ ] `SECRET_KEY` trocada (`python -c "import secrets; print(secrets.token_urlsafe(48))"`)
- [ ] `COOKIE_SEGURO=true`
- [ ] `APP_URL` com o domínio real e https
- [ ] SMTP configurado e domínio com SPF/DKIM
- [ ] `CAKTO_CHECKOUT_URL` e `CAKTO_WEBHOOK_SEGREDO` preenchidos
- [ ] `CAKTO_PERMITIR_SEM_ASSINATURA=false`
- [ ] senha do admin trocada e contas de teste removidas
- [ ] backup do banco agendado

A tela `/admin/configuracao` faz essa checagem sozinha e mostra o que falta.

## Backup

Com SQLite, backup é copiar um arquivo — mas use o comando do próprio SQLite
para não copiar um banco no meio de uma escrita:

```bash
# diário, às 3h
0 3 * * * sqlite3 /dados/plataforma.db ".backup '/backup/mapa-$(date +\%F).db'"
```

Guarde uma cópia fora do servidor. Perder o banco significa perder o progresso
de todos os alunos — o conteúdo do curso está no git e se recupera sozinho.

## Escala

Ordem de grandeza: cada aluno gera ~600 respostas ao longo dos 30 dias. Mil
alunos são ~600 mil linhas — nada para o SQLite. Se você passar disso ou
precisar de mais de uma máquina, defina `DATABASE_URL` apontando para um
Postgres: o mesmo código migra sem alteração (veja `app/db.py`).

Para migrar os dados existentes de SQLite para Postgres, use `pgloader` ou
exporte/importe as tabelas — o esquema é o mesmo, em `app/schema_pg.sql`.
