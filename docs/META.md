# Meta Ads: pixel, API de Conversões e campanhas

A plataforma rastreia o funil em duas camadas ao mesmo tempo. É proposital: o
pixel sozinho perde de 20% a 40% dos eventos (bloqueador de anúncio, iOS, aba
fechada antes de carregar), e é justamente o evento perdido que a campanha
precisa para otimizar.

| Evento | Onde dispara | Camada |
|--------|--------------|--------|
| `PageView` | todas as páginas | pixel |
| `InitiateCheckout` | clique em qualquer botão de compra | pixel |
| `CompleteRegistration` | aluno cria a senha e ativa a conta | **servidor (CAPI)** |
| `Purchase` | webhook de compra aprovada da Cakto | **servidor (CAPI)** |
| `Refund` | webhook de reembolso/chargeback | **servidor (CAPI)** |

`Purchase` vem do servidor porque o checkout acontece no domínio da Cakto —
o pixel do nosso site nem chega a ver a compra. Com a CAPI, o evento sai do
webhook com os dados do comprador com hash, e o Meta atribui à campanha certa.

## 1. Configurar

No **Gerenciador de Eventos** → Fontes de dados → seu pixel:

| Variável | Onde achar |
|----------|-----------|
| `META_PIXEL_ID` | id do pixel (número no topo da tela) |
| `META_CAPI_TOKEN` | Configurações → API de Conversões → *Gerar token de acesso* |
| `META_TEST_EVENT_CODE` | aba *Testar eventos* — use durante a configuração e apague depois |
| `META_VERIFICACAO_DOMINIO` | Business Manager → Segurança da marca → Domínios → meta tag |

Sem `META_PIXEL_ID` nada é injetado na página — nenhum script de terceiro
carrega. Sem `META_CAPI_TOKEN` os eventos de servidor são ignorados em
silêncio, e o site continua funcionando normalmente.

## 2. Testar antes de gastar dinheiro

1. Preencha `META_TEST_EVENT_CODE` e faça um deploy.
2. Abra a página de vendas → o `PageView` aparece na aba *Testar eventos*.
3. Clique em um plano → `InitiateCheckout`.
4. Faça uma compra de teste na Cakto → `Purchase` chega **pelo servidor**
   (origem "server"). Confira também em `/admin/webhooks`: cada envio para o
   Meta fica registrado ali com o retorno da API.
5. Apague o `META_TEST_EVENT_CODE` antes de subir campanha de verdade.

## 3. Qualidade do evento

A CAPI manda: e-mail, telefone, primeiro e último nome (tudo com SHA-256, nunca
em texto puro) e um `external_id` derivado do id do aluno. Isso costuma render
uma nota de correspondência boa no painel do Meta. Se você quiser subir mais,
o próximo passo é capturar `_fbp`/`_fbc` no clique do checkout e repassar à
Cakto como parâmetro — dá para fazer depois, sem mexer no resto.

**Deduplicação:** cada evento tem `event_id` estável (`compra-<transação>`,
`ativacao-<aluno>`). Se um dia o mesmo evento for disparado pelos dois lados,
o Meta conta uma vez só.

## 4. Estrutura de campanha sugerida para o lançamento

Nada aqui é obrigatório — é o esqueleto que costuma funcionar para infoproduto
de concurso, e que a plataforma já suporta rastrear:

* **Campanha 1 — Vendas (aquisição fria)**: otimização para `Purchase`, público
  amplo com interesses de concurso público/PM, criativos de dor ("estudou muito
  e reprovou") e de método ("o edital inteiro em 7 dias").
* **Campanha 2 — Remarketing**: público de quem disparou `InitiateCheckout` e
  não comprou em 7 dias. Criativo de objeção (garantia, tempo de estudo diário).
* **Campanha 3 — Retenção/upgrade**: lista de e-mails de alunos no plano
  Recruta (exportável do `/admin/alunos`) como público personalizado, anúncio
  do plano Operação Completa.

Quando as campanhas estiverem no ar, o `/admin` mostra o outro lado da conta:
funil da jornada, alunos ativos nos últimos 7 dias e vencimentos próximos —
os números que dizem se o tráfego virou aluno de verdade ou só clique.
