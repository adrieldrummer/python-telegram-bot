# Domínio: opaprova.com

O domínio já está registrado na **Hostinger** e hoje aponta para os
nameservers de estacionamento (`lunar.dns-parking.com` / `solar.dns-parking.com`).
Mantenha esses nameservers — o que muda são os **registros DNS**, editados em
hPanel → Domínios → `opaprova.com` → DNS / Nameservers → *Gerenciar registros DNS*.

## Opção A — apontar para a Vercel (recomendado para começar)

1. Na Vercel, em **Settings → Domains**, adicione `opaprova.com` e `www.opaprova.com`.
2. A Vercel mostra os valores exatos; hoje eles são:

| Tipo | Nome | Valor | TTL |
|------|------|-------|-----|
| A | `@` | `76.76.21.21` | 14400 |
| CNAME | `www` | `cname.vercel-dns.com` | 14400 |

3. Na Hostinger, apague os registros `A` e `CNAME` antigos que apontem para o
   estacionamento e crie os dois acima.
4. Espere a propagação (normalmente minutos, até 24 h no pior caso). A Vercel
   emite o certificado HTTPS sozinha.
5. Atualize a variável `APP_URL` para `https://opaprova.com` e faça *Redeploy* —
   é dela que saem os links dos e-mails de acesso.
6. Atualize a URL do webhook no painel da Cakto para
   `https://opaprova.com/webhooks/cakto`.

> Confira sempre os valores que a própria Vercel exibir: ela pode mudar o IP.

## Opção B — hospedar na sua VPS (Hostinger VPS, Contabo, etc.)

Só funciona em **VPS**. A hospedagem compartilhada da Hostinger roda PHP, não
Python — a plataforma não sobe lá.

| Tipo | Nome | Valor | TTL |
|------|------|-------|-----|
| A | `@` | IP da VPS | 14400 |
| A | `www` | IP da VPS | 14400 |

Depois, na VPS: `deploy/Caddyfile` já está com `opaprova.com` e
`www.opaprova.com`; suba com `docker compose up -d` (veja [`DEPLOY.md`](DEPLOY.md))
que o certificado é emitido automaticamente.

## E-mail no domínio

O e-mail de aprovação é o que entrega o produto — ele **não pode** cair em spam.

1. Escolha um serviço de envio: Hostinger Email, Resend, Brevo, Zoho ou SES.
2. Publique no DNS os registros que o serviço indicar:
   * **MX** — só se você for receber e-mail no domínio
   * **SPF** — `TXT @` com `v=spf1 include:<provedor> ~all`
   * **DKIM** — `CNAME`/`TXT` fornecidos pelo provedor
   * **DMARC** — `TXT _dmarc` com `v=DMARC1; p=none; rua=mailto:voce@opaprova.com`
3. No `.env` (ou nas variáveis da Vercel):

```
SMTP_HOST=...
SMTP_PORTA=587
SMTP_USUARIO=acesso@opaprova.com
SMTP_SENHA=...
EMAIL_REMETENTE="Operação Aprovação <acesso@opaprova.com>"
EMAIL_RESPONDER_PARA=suporte@opaprova.com
SUPORTE_EMAIL=suporte@opaprova.com
```

4. Teste de verdade: crie um acesso em `/admin/novo` com um e-mail seu e veja se
   chega na caixa de entrada (não na promoções/spam).

## Depois de apontar — checklist

- [ ] `APP_URL=https://opaprova.com`
- [ ] `COOKIE_SEGURO=true`
- [ ] Webhook da Cakto atualizado para o domínio novo
- [ ] SPF/DKIM publicados e e-mail de teste recebido
- [ ] `/admin/configuracao` sem alertas
