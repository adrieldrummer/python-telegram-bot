# Planos, assinaturas e liberação de acesso

## Como funciona

Um plano é um **conjunto de recursos**. As telas nunca perguntam "esse aluno é
do plano X" — perguntam "esse aluno tem o recurso Y". Por isso dá para criar
oferta, combo ou promoção sem tocar em nenhuma tela.

Recursos existentes: `trilha`, `questoes`, `erros`, `simulados`, `avancado`,
`manual`, `certificado`, `ranking`, `atualidades`, `suporte`.

| Plano | Preço | Ciclo | Recursos |
|-------|-------|-------|----------|
| **Recruta** | R$ 47/mês | mensal | trilha, questões (até 30/dia), caderno de erros |
| **Operação Completa** | R$ 97/mês | mensal | + simulados oficiais, módulos avançados, apostila, certificado, ranking |
| **Elite** | R$ 197/mês | mensal | tudo + atualidades e suporte prioritário |

Preços, textos e recursos ficam em `conteudo/planos.py`. Editar é um commit.

## A lógica comercial

A entrada é baixa de propósito: por R$ 47 o aluno tem a trilha de 7 dias que
explica o edital inteiro, o banco de questões e o caderno de erros. É o
suficiente para ele estudar de verdade — e é justamente por estudar de verdade
que ele esbarra nos dois limites do plano:

1. **Teto diário de questões** (`limite_questoes_dia`, hoje 30). A API de
   resposta devolve **402** quando o teto estoura, e o painel mostra a barra de
   consumo do dia antes disso acontecer.
2. **Áreas com cadeado**: simulados oficiais de 60 questões, módulos avançados
   (redação, TAF, etapas eliminatórias, aprofundamentos) e a apostila completa.
   A vitrine dessas áreas abre para todo mundo — quem não tem o recurso vê a
   capa com cadeado e o caminho para o upgrade. Bloquear a vitrine inteira
   esconderia justamente o que se quer vender.

O diagnóstico de 20 questões (`sim-diagnostico`) tem `recurso="questoes"`, ou
seja, entra no plano de entrada: é ele que monta o mapa de prioridades do aluno.

## Ligar com a Cakto

### Links de checkout

Cada plano tem seu próprio produto na Cakto, então cada um tem seu link. A
plataforma procura o link nesta ordem:

1. `checkout_url` fixo no `Plano(...)` em `conteudo/planos.py`;
2. variável de ambiente do plano: `CAKTO_CHECKOUT_<ID EM MAIÚSCULAS>`;
3. `CAKTO_CHECKOUT_URL` (o checkout geral, usado como rede de segurança).

Para a configuração de hoje:

```
CAKTO_CHECKOUT_RECRUTA=https://pay.cakto.com.br/...
CAKTO_CHECKOUT_OPERACAO=https://pay.cakto.com.br/...
CAKTO_CHECKOUT_ELITE=https://pay.cakto.com.br/...
```

Enquanto essas variáveis não existirem, todos os botões apontam para o checkout
geral — a página de vendas nunca fica com botão morto.

### Identificação da compra

Cada plano tem `codigos_cakto`: pedaços de texto que a plataforma procura no
**nome do produto e da oferta** que chegam no webhook. Exemplo:

```python
Plano(id="elite", codigos_cakto=("elite", "197", "vip"), ...)
```

Se o produto na Cakto se chamar *"Operação Aprovação — Elite"*, o aluno entra no
plano Elite automaticamente. Não casando nada pelo nome, a plataforma tenta pelo
**valor pago** (`identificar_por_valor`, tolerância de R$ 20) e, em último caso,
cai no `PLANO_PADRAO` — assim uma venda nunca fica sem acesso.

## Ciclo de vida

| Evento na Cakto | O que acontece |
|-----------------|----------------|
| compra aprovada / renovação | aplica o plano e estende a validade; envia `Purchase` para o Meta |
| assinatura cancelada | marca a assinatura como cancelada, **mas mantém o acesso até o fim do período pago** |
| reembolso / chargeback | encerra o acesso na hora, suspende o aluno e envia `Refund` |

Vencimento é por data (`alunos.plano_ate`). Passou da data, os recursos são
bloqueados e o aluno vê a tela de upgrade — o progresso, os pontos e o caderno
de erros continuam salvos, esperando a renovação.

Conta criada sem compra registrada (liberação manual no admin, por exemplo)
nasce no **plano de entrada**. Dar o plano completo por omissão entregaria de
graça exatamente o que o upgrade vende.

## No dia a dia

* **`/planos`** (aluno): compara os planos e mostra o que está bloqueado.
* **`/modulos`**: vitrine dos módulos avançados, com cadeado para quem ainda não
  tem o recurso `avancado`.
* **`/admin/aluno/{id}`**: mostra plano, validade e histórico de assinaturas, e
  permite trocar de plano ou encerrar na mão — útil para cortesia, correção de
  venda ou acordo com cliente.
* **`/admin`**: distribuição de alunos por plano e a lista de acessos vencendo
  nos próximos 7 dias (matéria-prima da campanha de renovação).

## Criar um plano novo

1. Acrescente um `Plano(...)` em `conteudo/planos.py` com id, preço, recursos,
   `limite_questoes_dia` (0 = sem teto) e `codigos_cakto`.
2. Publique o link do checkout em `CAKTO_CHECKOUT_<ID>`.
3. Rode `python -m pytest tests/test_planos.py -q`.
4. Publique. A página de vendas, a tela de upgrade e o admin passam a mostrar o
   plano novo sozinhos — nenhuma migração de banco é necessária.
