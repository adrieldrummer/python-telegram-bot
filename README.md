# Operação Aprovação — plataforma de estudo

Curso completo, pronto para vender na **Cakto**, construído a partir do e-book
*"O Mapa da Aprovação — como fui aprovado Soldado PM 2ª Classe em 60 dias"*.
O método do e-book foi recomprimido para **30 dias** e transformado em
plataforma: login por e-mail e senha, liberação diária com desbloqueio,
pontos de estudo, aprovação de acesso por e-mail e as ferramentas que o autor
fazia à mão (diagnóstico, caderno de erros e revisão espaçada).

![Operação Aprovação](app/static/img/emblema.png)

---

## O que está pronto

| Área | O que faz |
|------|-----------|
| **Página de vendas** | Landing com hero cinematográfico, as 4 fases, diferenciais, FAQ e botão para o checkout da Cakto |
| **Acesso** | Login e-mail/senha (PBKDF2), sessões assinadas e revogáveis, CSRF, bloqueio por força bruta, recuperação de senha |
| **Aprovação por e-mail** | Compra aprovada na Cakto → aluno criado → e-mail de aprovação com link único → aluno define a senha → Dia 1 liberado |
| **Jornada 30 dias** | 4 fases, 30 aulas escritas, missão diária, desbloqueio sequencial + drip, Chave de Antecipação por pontos |
| **Banco de questões** | 97 questões autorais comentadas, com "armadilha da banca" explicada, filtráveis por matéria e nível |
| **Caderno de Erros** | Classificação do erro (conteúdo / pegadinha / desatenção) e revisão espaçada 1‑3‑7‑15 dias até dominar |
| **Simulados** | 3 provas cronometradas com relatório de tempo e acerto por matéria e curva de evolução |
| **Pontos e patentes** | XP por ação, streak, 20 medalhas, 9 patentes (Recruta → Subtenente), ranking da turma |
| **Manual do Mapa** | O e-book revisado e ampliado: 16 capítulos, 6 deles novos, com download em Markdown |
| **Certificado** | Liberado ao concluir os 30 dias, com as estatísticas reais do aluno |
| **Planos e assinaturas** | 3 planos com recursos próprios, mapeamento automático produto Cakto → plano, renovação, cancelamento e expiração, tela de upgrade |
| **Meta Ads** | Pixel na página de vendas + API de Conversões server-side (Purchase, CompleteRegistration e Refund saindo do webhook) |
| **Painel do admin** | Métricas, funil da jornada, alunos por plano, vencimentos, liberação manual de acesso, compras, webhooks, caixa de e-mails, conteúdo e diagnóstico de configuração |

## Como rodar (2 minutos)

```bash
pip install -r requirements-dev.txt
cp .env.example .env          # ajuste o que quiser; funciona sem editar nada
python scripts/seed.py --demo # cria as contas de teste e simula progresso
python run.py                 # http://localhost:8000
```

### Contas de teste

| Papel | E-mail | Senha |
|-------|--------|-------|
| Administrador | `admin@teste.com` | `admin1234` |
| Aluno | `aluno@teste.com` | `aluno1234` |

> Antes de vender, troque essas senhas (ou apague as contas em `/admin/alunos`).

### Testes

```bash
python -m pytest tests/ -q                      # 89 testes, SQLite
DATABASE_URL="postgres://..." python -m pytest  # mesma suíte, Postgres
```

## Subir online em 5 minutos

Passo a passo clique a clique: [`docs/SUBIR-AGORA.md`](docs/SUBIR-AGORA.md)

[**→ Importar na Vercel**](https://vercel.com/new/import?s=https://github.com/adrieldrummer/python-telegram-bot)
(branch `claude/cakto-course-platform-xfepzk`)

O primeiro deploy funciona **sem configurar nada**: sem `DATABASE_URL` a
plataforma entra em *modo demonstração* — sobe com as contas de teste e uma
tarja amarela avisando que os dados somem a cada reinício. É o suficiente para
navegar e mostrar para alguém.

Para virar produto de verdade, cadastre as variáveis abaixo em
**Settings → Environment Variables** e faça *Redeploy*:

```
DATABASE_URL   = postgresql://postgres.<ref>:<senha>@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
DB_SCHEMA      = mapa_aprovacao
SECRET_KEY     = <python -c "import secrets; print(secrets.token_urlsafe(48))">
COOKIE_SEGURO  = true
APP_URL        = https://seu-projeto.vercel.app
```

O banco já está criado e com as contas de teste dentro — detalhes e a lista
completa de variáveis em [`docs/VERCEL.md`](docs/VERCEL.md).

## Arquitetura

```
app/            aplicação FastAPI
  main.py       montagem, middleware de e-mail, tratamento de erro
  config.py     configuração via .env
  db.py         SQLite ou Postgres (tradução de dialeto num lugar só)
  security.py   senhas, tokens, sessões, CSRF, força bruta
  alunos.py     ciclo de vida: compra → aprovação → ativação → suspensão
  jornada.py    prioridades, desbloqueio, missões, conclusão de dia
  srs.py        caderno de erros e revisão espaçada
  planos.py     assinaturas, validade e liberação de recursos
  marketing.py  pixel do Meta e API de Conversões
  estudo.py     respostas, simulados, relatórios
  gamificacao.py pontos, streak, patentes, medalhas
  mailer.py     fila de e-mails (SMTP ou caixa de saída)
  web/          rotas: publico, aluno, admin, webhooks
  templates/    Jinja2 (interface + e-mails)
  static/       CSS, JS e as artes geradas
conteudo/       o curso e a oferta, versionados em git (sem banco):
  planos.py     planos, preços e recursos de cada um
  trilha/       30 dias em 4 fases
  questoes/     banco por matéria
  simulados.py  montagem determinística das provas
  manual.py     e-book 2ª edição
  materias.py   matérias, pesos e categorias de erro
  patentes.py   patentes e medalhas
deploy/         Dockerfile, docker-compose, Caddy (HTTPS automático)
docs/           deploy, Cakto, domínio e operação
tests/          89 testes automatizados
```

Duas decisões que valem explicação:

1. **O conteúdo não fica no banco.** Aula, questão e simulado são código
   versionado. Corrigir um gabarito é um commit — não uma migração e não um
   formulário de admin que ninguém audita.
2. **O SQL é escrito uma vez.** Todas as consultas usam o dialeto SQLite e são
   traduzidas para Postgres em `app/db.py`. Assim o mesmo código roda no
   notebook, na VPS e na Vercel.

## Publicar

* **Vercel + Supabase** (serverless, sem servidor para cuidar): [`docs/VERCEL.md`](docs/VERCEL.md)
* **VPS com Docker + HTTPS automático**: [`docs/DEPLOY.md`](docs/DEPLOY.md)
* **Integração com a Cakto**: [`docs/CAKTO.md`](docs/CAKTO.md)
* **Domínio e DNS**: [`docs/DOMINIO.md`](docs/DOMINIO.md)
* **Planos e assinaturas**: [`docs/PLANOS.md`](docs/PLANOS.md)
* **Meta Ads (pixel, CAPI e campanhas)**: [`docs/META.md`](docs/META.md)
* **Operação do dia a dia**: [`docs/OPERACAO.md`](docs/OPERACAO.md)

## Aviso

Material educacional independente, sem vínculo com instituições públicas ou
bancas. Os pesos por matéria são leitura estatística de provas anteriores e
não substituem o edital vigente — a plataforma diz isso ao aluno.
