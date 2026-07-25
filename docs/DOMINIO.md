# Domínio e DNS

## 1. Registrar

Registre em qualquer registradora (Registro.br para `.com.br`, Cloudflare ou
Namecheap para `.com`). Sugestões coerentes com a marca:

* `mapadaaprovacao.com.br`
* `mapadaaprovacao.com`
* `soldadopm.com.br`

Prefira um domínio curto e fácil de ditar: ele vai aparecer no remetente dos
e-mails e na barra do navegador do aluno.

## 2. Apontar para a plataforma

### Na Vercel

Em **Settings → Domains**, adicione o domínio. A Vercel indica dois registros:

| Tipo | Nome | Valor |
|------|------|-------|
| A | `@` | `76.76.21.21` |
| CNAME | `www` | `cname.vercel-dns.com` |

(Confirme os valores na tela — a Vercel pode atualizá-los.)

### Em VPS própria

| Tipo | Nome | Valor |
|------|------|-------|
| A | `@` | IP da VPS |
| A (ou CNAME) | `www` | IP da VPS (ou `@`) |

Depois é só subir o Caddy: ele emite o certificado assim que o DNS propagar.

## 3. E-mail no seu domínio

Enviar do próprio domínio muda a taxa de entrega — e o e-mail de aprovação é
o que dá acesso ao produto, então ele **não pode** cair em spam.

1. Crie a conta em um serviço de envio (Resend, Brevo, Amazon SES, Zoho).
2. Cadastre o domínio e publique os registros que ele indicar:
   * **SPF** — `TXT @` com `v=spf1 include:<provedor> ~all`
   * **DKIM** — `CNAME`/`TXT` fornecidos pelo provedor
   * **DMARC** — `TXT _dmarc` com `v=DMARC1; p=none; rua=mailto:voce@dominio`
3. Preencha `SMTP_HOST`, `SMTP_PORTA`, `SMTP_USUARIO`, `SMTP_SENHA` e
   `EMAIL_REMETENTE` no `.env`.
4. Teste: crie um acesso em `/admin/novo` para um e-mail seu e veja se chega.

Use um remetente dedicado (`acesso@seudominio.com.br`) e mantenha
`EMAIL_RESPONDER_PARA` no e-mail de suporte que você realmente lê.

## 4. Depois de apontar

* Atualize `APP_URL` — todos os links dos e-mails saem dele.
* Atualize a URL do webhook no painel da Cakto.
* Ative `COOKIE_SEGURO=true`.
* Confira `/admin/configuracao`: a tela valida esses itens.
