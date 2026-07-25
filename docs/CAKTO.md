# Integração com a Cakto

O fluxo é este:

```
compra aprovada na Cakto
        │  webhook
        ▼
plataforma cria o aluno (status: pendente)
        │  e-mail de aprovação com link único (7 dias)
        ▼
aluno define a senha  →  status: ativo  →  Dia 1 liberado
```

Reembolso ou chargeback chega pelo mesmo webhook e **suspende** o acesso,
mantendo todo o progresso salvo caso a compra seja reativada.

## 1. Produto e checkout

1. Crie o produto na Cakto e copie o link do checkout.
2. Coloque o link em `CAKTO_CHECKOUT_URL` — ele alimenta todos os botões de
   compra da página de vendas.

## 2. Webhook

No painel da Cakto, cadastre a URL:

```
https://SEU-DOMINIO/webhooks/cakto
```

Eventos que interessam: **compra aprovada/paga** e
**reembolso/chargeback/cancelamento**. Se a sua conta permitir enviar todos,
tudo bem: eventos não reconhecidos são registrados e ignorados.

Defina um segredo no painel e repita o mesmo valor em `CAKTO_WEBHOOK_SEGREDO`.
A plataforma aceita duas formas de assinatura, sem precisar de ajuste:

* HMAC-SHA256 do corpo da requisição (o formato mais comum), ou
* o próprio segredo como token no cabeçalho.

O cabeçalho lido é o de `CAKTO_HEADER_ASSINATURA` (padrão `x-cakto-signature`);
também são aceitos `x-webhook-signature`, `x-signature` e `?token=` na URL.
Se a sua conta usar outro nome, basta trocar a variável.

> **Nunca** deixe `CAKTO_PERMITIR_SEM_ASSINATURA=true` em produção: qualquer
> pessoa poderia liberar acesso enviando um JSON.

## 3. Testar antes de vender

1. Faça uma compra de teste (ou use o modo sandbox da Cakto).
2. Abra `/admin/webhooks` — o evento aparece com a assinatura validada e o
   resultado ("acesso aprovado e e-mail enviado").
3. Abra `/admin/emails` e clique no e-mail de aprovação: o link de ativação
   está lá, mesmo sem SMTP configurado.
4. Abra o link em uma aba anônima, crie a senha e confira se o Dia 1 abre.

## 4. Quando o webhook falha

Nem toda venda dispara webhook (queda de rede, evento perdido, venda por fora).
Para esses casos existe `/admin/novo`: você informa nome e e-mail e a
plataforma manda o mesmo e-mail de aprovação, registrando a compra como
liberação manual.

Se o aluno perder o e-mail, abra o cadastro dele em `/admin/aluno/{id}` e
clique em **Reenviar e-mail de aprovação** — o link antigo é invalidado na hora.

## Campos que o webhook entende

O leitor é tolerante a formatos: procura o e-mail em `customer.email`,
`data.customer.email`, `buyer.email`, `client.email` e `email`; o mesmo vale
para nome, telefone, status, valor e identificador da transação. O payload cru
fica gravado em `/admin/webhooks`, então, se a sua conta usar um formato
diferente, dá para ver exatamente o que chegou e ajustar.

A idempotência é garantida pelo identificador da transação: o mesmo evento
recebido duas vezes não cria duas compras nem reenvia e-mail.
