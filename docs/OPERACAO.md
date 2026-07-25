# Operação do dia a dia

## Painel do administrador

| Tela | Para quê |
|------|----------|
| `/admin` | Métricas, funil da jornada e últimos eventos |
| `/admin/alunos` | Busca por nome/e-mail, filtro por situação |
| `/admin/aluno/{id}` | Progresso, prioridades, compras, e-mails e ações |
| `/admin/novo` | Liberar acesso manualmente (venda fora da Cakto, cortesia, correção) |
| `/admin/compras` | Todas as transações registradas |
| `/admin/webhooks` | Eventos recebidos com payload cru — o lugar para depurar integração |
| `/admin/emails` | Caixa de saída: todo e-mail gerado, com pré-visualização |
| `/admin/conteudo` | Inventário do curso (dias, questões por matéria, simulados) |
| `/admin/configuracao` | Diagnóstico de ambiente: o que ainda falta para vender |

## Situações comuns

**"Comprei e não recebi o e-mail"**
→ `/admin/alunos`, busque pelo e-mail. Se o aluno existe, abra o cadastro e
clique em *Reenviar e-mail de aprovação*. Se não existe, o webhook não chegou:
confira `/admin/webhooks` e use `/admin/novo` para liberar na mão.

**"O link expirou"**
→ O aluno pode usar *Esqueci minha senha* na tela de login: o fluxo de
recuperação também ativa a conta. Ou reenvie a aprovação pelo admin.

**Reembolso**
→ O webhook suspende sozinho. Para suspender manualmente, use a ação
*Suspender acesso* no cadastro do aluno (o progresso é preservado).

**Aluno travado num dia**
→ A missão exige o percentual mínimo (`META_ACERTO_MISSAO`, padrão 60%). Ele
deve revisar os erros e refazer o bloco. Se você quiser um curso mais leve,
baixe esse valor ou desligue o drip com `JORNADA_DRIP_DIARIO=false`.

**Quero soltar todo o conteúdo de uma vez**
→ `JORNADA_DRIP_DIARIO=false`: o aluno avança no ritmo dele, mantendo só a
regra de sequência (concluir o dia anterior).

## Rotina semanal sugerida

1. Abra `/admin` e olhe o **funil da jornada**: o dia em que a barra despenca é
   onde os alunos abandonam. Vale um e-mail de resgate — ou uma revisão do
   conteúdo daquele dia.
2. Confira `/admin/emails` por falhas de envio (status *erro*).
3. Rode o backup (veja `DEPLOY.md`).

## Lembretes automáticos

`scripts/enviar_lembretes.py` envia um lembrete para quem tem lembretes
ativados e ainda não estudou hoje, e processa a fila de e-mails. Em VPS, o
`docker-compose` já sobe esse worker. Fora dele:

```bash
0 19 * * *  cd /opt/mapa && .venv/bin/python scripts/enviar_lembretes.py
```

## Editar o conteúdo do curso

Tudo vive em `/conteudo`, versionado no git:

* **aula de um dia** → `conteudo/trilha/fase{1..4}.py`
* **questões** → `conteudo/questoes/{materia}.py` (o formato é o mesmo; o id
  precisa ser único)
* **simulados** → `conteudo/simulados.py` (mude só a composição; as questões
  são sorteadas de forma estável)
* **pesos das matérias** → `conteudo/materias.py`
* **e-book** → `conteudo/manual.py`

Depois de editar, rode `python -m pytest tests/test_conteudo.py -q`: os testes
conferem gabarito válido, ids únicos e a integridade dos simulados.
