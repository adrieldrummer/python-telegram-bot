# Publicar na Vercel (com Supabase)

A Vercel é serverless: o disco é efêmero. Por isso, em produção a plataforma
precisa de um Postgres externo — aqui usamos o Supabase.

## 1. O banco já está criado

O schema `mapa_aprovacao` foi criado no projeto Supabase **lembraai**
(`rsqenkjerdjlwrzbneys`), com as 14 tabelas e as contas de teste:

| Papel | E-mail | Senha |
|-------|--------|-------|
| Administrador | `admin@teste.com` | `admin1234` |
| Aluno | `aluno@teste.com` | `aluno1234` |

> Trocar essas senhas antes de vender é obrigatório. Depois de logar como
> admin, use `/conta` para trocar a sua e `/admin/alunos` para apagar a de teste.

### Pegar a string de conexão

No painel da Supabase: **Project Settings → Database → Connection string →
URI**, e escolha o modo **Transaction pooler** (porta 6543) — é o indicado para
funções serverless, que abrem e fecham conexão a cada requisição.

O formato é:

```
postgresql://postgres.rsqenkjerdjlwrzbneys:SUA_SENHA@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
```

A senha é a do banco (definida na criação do projeto). Se você não a tem,
gere outra em **Database → Reset database password**.

## 1b. Prefere ver funcionando antes de configurar?

Faça o deploy sem nenhuma variável de ambiente. Sem `DATABASE_URL`, a
plataforma entra em **modo demonstração**: o banco vai para `/tmp`, as contas
de teste são criadas automaticamente no boot e uma tarja amarela avisa que os
dados somem a cada reinício. Tudo funciona — jornada, questões, caderno de
erros, simulados, admin —, só não persiste.

Assim que você cadastrar `DATABASE_URL`, o modo demonstração desaparece
sozinho e nada é criado automaticamente: as contas passam a nascer só da
compra na Cakto ou da liberação manual no painel.

## 2. Importar o repositório

1. Acesse <https://vercel.com/new>
2. **Import Git Repository** → escolha `adrieldrummer/python-telegram-bot`
3. Branch: `claude/cakto-course-platform-xfepzk`
4. Framework preset: **Other** (o `vercel.json` já define o build Python)
5. Antes de clicar em Deploy, cadastre as variáveis de ambiente abaixo

## 3. Variáveis de ambiente

Obrigatórias:

| Chave | Valor |
|-------|-------|
| `DATABASE_URL` | a URI do pooler da Supabase (passo 1) |
| `DB_SCHEMA` | `mapa_aprovacao` |
| `SECRET_KEY` | gere com `python -c "import secrets; print(secrets.token_urlsafe(48))"` |
| `COOKIE_SEGURO` | `true` |
| `APP_URL` | `https://seu-projeto.vercel.app` (troque depois pelo domínio próprio) |

Recomendadas:

| Chave | Para quê |
|-------|----------|
| `CAKTO_CHECKOUT_URL` | link do checkout nos botões de compra |
| `CAKTO_WEBHOOK_SEGREDO` | valida a assinatura do webhook |
| `SMTP_HOST`, `SMTP_PORTA`, `SMTP_USUARIO`, `SMTP_SENHA` | envio real de e-mail |
| `EMAIL_REMETENTE` | `Mapa da Aprovação <acesso@seudominio.com.br>` |
| `SUPORTE_EMAIL` | e-mail que aparece para o aluno |
| `JORNADA_DRIP_DIARIO` | `false` libera o próximo dia assim que o anterior é concluído |

Sem SMTP a plataforma entra em **modo caixa de saída**: nada é enviado, mas
todo e-mail (com o link de ativação) fica visível em `/admin/emails`. Dá para
testar o fluxo inteiro de venda antes de configurar o servidor de e-mail.

## 4. Deploy

Clique em **Deploy**. Ao terminar, abra a URL e entre com a conta de admin.
Confira `/admin/configuracao` — a tela lista o que ainda falta ajustar.

## 5. Domínio próprio

Em **Settings → Domains**, adicione `mapadaaprovacao.com.br`. A Vercel mostra
os registros DNS; o passo a passo está em [`DOMINIO.md`](DOMINIO.md). Depois,
atualize `APP_URL` para o domínio final — ele é usado nos links dos e-mails.

## Limitações conhecidas do modo serverless

* **Envio de e-mail** acontece durante a requisição (no máximo uma vez por
  minuto). Como cada função morre ao responder, o cron dos lembretes
  (`scripts/enviar_lembretes.py`) não roda sozinho — configure um
  [Vercel Cron Job](https://vercel.com/docs/cron-jobs) apontando para
  `/saude` ou rode o script de outra máquina apontando para o mesmo banco.
* **Arquivos estáticos** são servidos pela função Python. Funciona bem no
  volume de um lançamento; se o tráfego crescer, mova `/static` para um CDN.
* **Cold start** de ~1 s na primeira visita depois de ocioso.

Se preferir um servidor sempre quente, com SQLite e sem depender de nada,
o caminho é [`DEPLOY.md`](DEPLOY.md) — uma VPS de R$ 30/mês aguenta o produto
inteiro.
