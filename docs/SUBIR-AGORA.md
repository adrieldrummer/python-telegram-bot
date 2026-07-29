# Subir agora — passo a passo (5 minutos)

Feito uma vez, os deploys seguintes são automáticos: todo push na branch
publica sozinho.

---

## Parte 1 — colocar no ar (2 minutos)

1. Abra <https://vercel.com/new>
2. **Import Git Repository** → autorize o GitHub, se ele pedir → escolha
   **`adrieldrummer/python-telegram-bot`**
3. Na tela de configuração:
   * **Framework Preset**: *Other*
   * **Root Directory**: deixe na raiz (`./`)
   * **Branch**: `claude/cakto-course-platform-xfepzk`
   * Não mexa em Build Command nem em Output Directory — o `vercel.json`
     já cuida disso
4. Clique em **Deploy**

Ao terminar, abra a URL `…vercel.app`. O site sobe em **modo demonstração**
(tarja amarela), com estas contas:

| Papel | E-mail | Senha |
|-------|--------|-------|
| Administrador | `admin@teste.com` | `admin1234` |
| Aluno | `aluno@teste.com` | `aluno1234` |

Nesse modo os dados somem a cada reinício — é só para você navegar e conferir.

---

## Parte 2 — banco de verdade (2 minutos)

1. No painel da **Supabase**, projeto **lembraai** → *Project Settings* →
   *Database* → *Connection string* → aba **URI** → modo **Transaction pooler**
   (porta 6543). Copie. Se não souber a senha, use *Reset database password*.
2. Na Vercel: *Settings* → **Environment Variables** → cole uma a uma:

```
DATABASE_URL   = postgresql://postgres.rsqenkjerdjlwrzbneys:SUA_SENHA@aws-0-sa-east-1.pooler.supabase.com:6543/postgres
DB_SCHEMA      = mapa_aprovacao
SECRET_KEY     = fzR2jFNWPL3nk6EdqddWpIlkE8e5ExnGoD9dYFDzTnPGWz1NKVPg_onsXUWhUTam
COOKIE_SEGURO  = true
APP_URL        = https://SEU-PROJETO.vercel.app
```

3. *Deployments* → nos três pontinhos do último deploy → **Redeploy**.

A tarja amarela some e os dados passam a persistir. O schema
`mapa_aprovacao` já está criado com as mesmas contas de teste acima.

> Troque as senhas de teste depois de entrar: `/conta` para a sua e
> `/admin/alunos` para apagar a do aluno de demonstração.

---

## Parte 3 — domínio opaprova.com (2 minutos + propagação)

1. Vercel → *Settings* → **Domains** → adicione `opaprova.com` e `www.opaprova.com`.
2. No **hPanel da Hostinger** → Domínios → `opaprova.com` → DNS / Nameservers →
   *Gerenciar registros DNS*, apague os registros do estacionamento e crie:

| Tipo | Nome | Valor | TTL |
|------|------|-------|-----|
| A | `@` | `76.76.21.21` | 14400 |
| CNAME | `www` | `cname.vercel-dns.com` | 14400 |

(Use sempre os valores que a Vercel mostrar na tela — ela pode mudar o IP.)

3. Quando o domínio ficar verde na Vercel, mude `APP_URL` para
   `https://opaprova.com` e faça *Redeploy*. Esse valor alimenta os links dos
   e-mails de acesso.
4. Atualize a URL do webhook no painel da Cakto para
   `https://opaprova.com/webhooks/cakto`.

---

## Parte 4 — ligar venda e anúncio

Depois que o domínio estiver no ar, cadastre também:

```
CAKTO_CHECKOUT_URL      = link do checkout principal
CAKTO_WEBHOOK_SEGREDO   = o mesmo segredo configurado na Cakto
META_PIXEL_ID           = id do pixel
META_CAPI_TOKEN         = token da API de Conversões
META_VERIFICACAO_DOMINIO= conteúdo da meta tag de verificação do domínio
SMTP_HOST / SMTP_PORTA / SMTP_USUARIO / SMTP_SENHA
EMAIL_REMETENTE         = Operação Aprovação <acesso@opaprova.com>
SUPORTE_EMAIL           = suporte@opaprova.com
```

Confira em `/admin/configuracao`: a tela lista item por item o que ainda falta.

---

## Se preferir que eu faça

Gere um token em <https://vercel.com/account/tokens> (escopo *Full Account*,
validade curta) e me mande. Com ele eu faço o deploy, cadastro as variáveis,
conecto o domínio, testo o fluxo inteiro e te devolvo a URL funcionando.
Depois é só revogar o token na mesma tela.
