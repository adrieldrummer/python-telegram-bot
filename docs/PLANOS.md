# Planos, assinaturas e liberação de acesso

## Como funciona

Um plano é um **conjunto de recursos**. As telas nunca perguntam "esse aluno é
do plano X" — perguntam "esse aluno tem o recurso Y". Por isso dá para criar
oferta, combo ou promoção sem tocar em nenhuma tela.

Recursos existentes: `trilha`, `questoes`, `erros`, `simulados`, `manual`,
`certificado`, `ranking`, `suporte`.

| Plano | Preço | Acesso | Recursos |
|-------|-------|--------|----------|
| **Recruta** | R$ 97 (único) | 6 meses | trilha, questões, caderno de erros |
| **Operação Completa** | R$ 197 (único) | 12 meses | + simulados, manual, certificado, ranking |
| **Elite** | R$ 29,90/mês | enquanto assinar | tudo + suporte prioritário |

Preços, textos e recursos ficam em `conteudo/planos.py`. Editar é um commit.

## Ligar com a Cakto

Cada plano tem `codigos_cakto`: pedaços de texto que a plataforma procura no
**nome do produto e da oferta** que chegam no webhook. Exemplo:

```python
Plano(id="elite", codigos_cakto=("elite", "assinatura", "mensal"), ...)
```

Se o produto na Cakto se chamar *"Operação Aprovação — Assinatura Elite"*, o
aluno entra no plano Elite automaticamente. Não casando nada, ele cai no
`PLANO_PADRAO` (hoje, Operação Completa) — assim uma venda nunca fica sem acesso.

Coloque também o `checkout_url` de cada plano; a página de vendas usa esse link
em cada botão, e o `CAKTO_CHECKOUT_URL` global vira só o fallback.

## Ciclo de vida

| Evento na Cakto | O que acontece |
|-----------------|----------------|
| compra aprovada / renovação | aplica o plano e estende a validade; envia `Purchase` para o Meta |
| assinatura cancelada | marca a assinatura como cancelada, **mas mantém o acesso até o fim do período pago** |
| reembolso / chargeback | encerra o acesso na hora, suspende o aluno e envia `Refund` |

Vencimento é por data (`alunos.plano_ate`). Passou da data, os recursos são
bloqueados e o aluno vê a tela de upgrade — o progresso, os pontos e o caderno
de erros continuam salvos, esperando a renovação.

## No dia a dia

* **`/planos`** (aluno): compara os planos e mostra o que está bloqueado.
* **`/admin/aluno/{id}`**: mostra plano, validade e histórico de assinaturas, e
  permite trocar de plano ou encerrar na mão — útil para cortesia, correção de
  venda ou acordo com cliente.
* **`/admin`**: distribuição de alunos por plano e a lista de acessos vencendo
  nos próximos 7 dias (matéria-prima da campanha de renovação).

## Criar um plano novo

1. Acrescente um `Plano(...)` em `conteudo/planos.py` com id, preço, recursos,
   `checkout_url` e `codigos_cakto`.
2. Rode `python -m pytest tests/test_planos.py -q`.
3. Publique. A página de vendas, a tela de upgrade e o admin passam a mostrar o
   plano novo sozinhos — nenhuma migração de banco é necessária.
