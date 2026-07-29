/* Player de questões — usado na missão do dia, no treino livre,
   na revisão do caderno de erros e no simulado. */

(function () {
  const raiz = document.querySelector('[data-player]');
  if (!raiz) return;

  const dados = JSON.parse(document.getElementById('dados-questoes').textContent);
  const modo = raiz.dataset.modo; // missao | treino | revisao | simulado
  const dia = raiz.dataset.dia ? parseInt(raiz.dataset.dia, 10) : null;
  const sessaoId = raiz.dataset.sessao ? parseInt(raiz.dataset.sessao, 10) : null;
  const origem = raiz.dataset.origem || 'treino';
  const simulado = modo === 'simulado';

  const alvoQuestao = raiz.querySelector('[data-questao]');
  const alvoPontos = raiz.querySelector('[data-navegacao]');
  const alvoContador = raiz.querySelector('[data-contador]');
  const botaoAnterior = raiz.querySelector('[data-anterior]');
  const botaoProximo = raiz.querySelector('[data-proximo]');
  const botaoConcluir = raiz.querySelector('[data-concluir]');

  const estado = dados.map((q) => ({
    questao: q,
    respondida: q.respondida ? q.respondida.alternativa : null,
    correta: q.respondida ? q.respondida.correta : null,
    retorno: null,
    classificada: null,
  }));
  let indice = estado.findIndex((e) => !e.respondida);
  if (indice < 0) indice = 0;
  let inicioQuestao = Date.now();

  const CATEGORIAS = [
    { id: 'conteudo', rotulo: '📚 Falta de conteúdo' },
    { id: 'pegadinha', rotulo: '🎯 Pegadinha' },
    { id: 'desatencao', rotulo: '⏱ Desatenção' },
  ];

  function escapar(texto) {
    const div = document.createElement('div');
    div.textContent = texto == null ? '' : texto;
    return div.innerHTML;
  }

  function desenharNavegacao() {
    if (!alvoPontos) return;
    alvoPontos.innerHTML = '';
    estado.forEach((item, i) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'pontinho';
      if (item.respondida) b.classList.add(simulado ? 'ok' : item.correta ? 'ok' : 'nok');
      if (i === indice) b.classList.add('atual');
      b.title = `Questão ${i + 1}`;
      b.addEventListener('click', () => {
        indice = i;
        desenhar();
      });
      alvoPontos.appendChild(b);
    });
    const feitas = estado.filter((e) => e.respondida).length;
    if (alvoContador) {
      alvoContador.textContent = `${feitas} de ${estado.length} respondidas`;
    }
    if (botaoConcluir) {
      botaoConcluir.disabled = feitas < estado.length && !simulado;
      botaoConcluir.classList.toggle('esconder', feitas === 0 && simulado);
    }
  }

  function desenhar() {
    const item = estado[indice];
    const q = item.questao;
    inicioQuestao = Date.now();

    const alternativas = q.alternativas
      .map((alt) => {
        let classe = '';
        if (item.respondida && !simulado) {
          if (alt.letra === item.retorno?.gabarito) classe = 'correta';
          else if (alt.letra === item.respondida) classe = 'errada';
        } else if (item.respondida && simulado && alt.letra === item.respondida) {
          classe = 'correta';
        }
        return `<button type="button" class="alternativa ${classe}" data-letra="${alt.letra}" ${
          item.respondida && !simulado ? 'disabled' : ''
        }>
            <span class="letra">${alt.letra}</span>
            <span>${escapar(alt.texto)}</span>
          </button>`;
      })
      .join('');

    alvoQuestao.innerHTML = `
      <article class="questao">
        <header class="questao-cabecalho">
          <span class="etiqueta" style="border-color:${q.cor};color:#fff">${escapar(q.materia_nome)}</span>
          <span class="etiqueta">${escapar(q.tema)}</span>
          <span class="etiqueta">${escapar(q.nivel)}</span>
          <span class="apagado" style="margin-left:auto">Questão ${indice + 1}/${estado.length}</span>
        </header>
        <div class="questao-corpo">
          <div class="questao-enunciado">${escapar(q.enunciado)}</div>
          <div class="alternativas">${alternativas}</div>
          <div data-retorno></div>
        </div>
      </article>`;

    alvoQuestao.querySelectorAll('.alternativa').forEach((botao) => {
      botao.addEventListener('click', () => responder(botao.dataset.letra));
    });

    if (item.retorno && !simulado) desenharRetorno(item);
    if (botaoAnterior) botaoAnterior.disabled = indice === 0;
    if (botaoProximo) botaoProximo.disabled = indice >= estado.length - 1;
    desenharNavegacao();
  }

  function desenharRetorno(item) {
    const caixa = alvoQuestao.querySelector('[data-retorno]');
    if (!caixa || !item.retorno) return;
    const r = item.retorno;
    const classificacao = !r.correta
      ? `<div class="mt-1">
           <strong style="font-size:.88rem">Por que você errou?</strong>
           <div class="categorias" data-categorias>
             ${CATEGORIAS.map(
               (c) =>
                 `<button type="button" class="categoria-btn ${
                   item.classificada === c.id ? 'escolhida' : ''
                 }" data-categoria="${c.id}">${c.rotulo}</button>`
             ).join('')}
           </div>
           <p class="apagado mt-1" style="font-size:.8rem;margin:.5rem 0 0">
             Classificar alimenta sua revisão espaçada — e vale 8 pontos.
           </p>
         </div>`
      : '';

    caixa.innerHTML = `
      <div class="retorno ${r.correta ? 'acerto' : 'erro'}">
        <h4>${r.correta ? '✅ Acertou' : '❌ Errou'} · +${r.pontos} pontos${
      r.dominada ? ' · questão dominada 🧠' : ''
    }</h4>
        ${
          r.correta
            ? ''
            : `<p><strong>Gabarito: ${r.gabarito}</strong> — ${escapar(r.gabarito_texto)}</p>`
        }
        <p>${escapar(r.comentario)}</p>
        ${r.armadilha ? `<p class="armadilha"><strong>Armadilha da banca:</strong> ${escapar(r.armadilha)}</p>` : ''}
        ${classificacao}
      </div>`;

    caixa.querySelectorAll('[data-categoria]').forEach((botao) => {
      botao.addEventListener('click', async () => {
        try {
          const resposta = await window.MAPA.postJSON('/api/classificar', {
            questao_id: item.questao.id,
            categoria: botao.dataset.categoria,
            anotacao: '',
          });
          item.classificada = botao.dataset.categoria;
          caixa.querySelectorAll('[data-categoria]').forEach((b) => b.classList.remove('escolhida'));
          botao.classList.add('escolhida');
          if (resposta.pontos) window.MAPA.aviso(`+${resposta.pontos} pontos por correção ativa`, 'ok');
          window.MAPA.medalhas(resposta.medalhas);
        } catch (erro) {
          window.MAPA.aviso(erro.message);
        }
      });
    });
  }

  async function responder(letra) {
    const item = estado[indice];
    if (item.respondida && !simulado) return;
    const tempo = Math.round((Date.now() - inicioQuestao) / 1000);
    try {
      const retorno = await window.MAPA.postJSON('/api/responder', {
        questao_id: item.questao.id,
        alternativa: letra,
        origem: origem,
        dia: dia,
        tempo_seg: tempo,
        sessao_id: sessaoId,
      });
      item.respondida = letra;
      item.correta = retorno.correta;
      item.retorno = retorno;
      window.MAPA.atualizarPontos(retorno.pontos_totais);
      if (retorno.bonus_streak) {
        window.MAPA.aviso(`🔥 +${retorno.bonus_streak} pontos de constância`, 'ok');
      }
      window.MAPA.medalhas(retorno.medalhas);
      // aviso antecipado: descobrir o teto do plano na última questão frustra
      if (typeof retorno.restantes_hoje === 'number' && retorno.restantes_hoje <= 5) {
        window.MAPA.aviso(
          retorno.restantes_hoje > 0
            ? `Restam ${retorno.restantes_hoje} questões hoje no seu plano.`
            : 'Você fechou o limite de questões de hoje. Faça upgrade para treinar sem teto.'
        );
      }
      desenhar();
      if (simulado) {
        setTimeout(() => {
          if (indice < estado.length - 1) {
            indice += 1;
            desenhar();
          }
        }, 180);
      }
    } catch (erro) {
      window.MAPA.aviso(erro.message);
      // 402 é sempre limite de plano: leva o aluno para onde ele resolve isso
      if (erro.status === 402) setTimeout(() => { window.location.href = '/planos'; }, 2200);
    }
  }

  if (botaoAnterior) {
    botaoAnterior.addEventListener('click', () => {
      if (indice > 0) {
        indice -= 1;
        desenhar();
      }
    });
  }
  if (botaoProximo) {
    botaoProximo.addEventListener('click', () => {
      if (indice < estado.length - 1) {
        indice += 1;
        desenhar();
      }
    });
  }

  if (botaoConcluir && modo === 'missao') {
    botaoConcluir.addEventListener('click', async () => {
      botaoConcluir.disabled = true;
      try {
        const retorno = await window.MAPA.postJSON('/api/concluir-dia', { dia: dia });
        if (retorno.concluido) {
          window.location.href = `/jornada?concluido=${dia}`;
        } else {
          window.MAPA.aviso(retorno.motivo || 'Missão ainda não concluída.');
          botaoConcluir.disabled = false;
        }
      } catch (erro) {
        window.MAPA.aviso(erro.message);
        botaoConcluir.disabled = false;
      }
    });
  }

  window.MAPA_PLAYER = {
    estado,
    finalizarSimulado: async function (duracao) {
      const retorno = await window.MAPA.postJSON('/api/simulado/finalizar', {
        sessao_id: sessaoId,
        duracao_seg: duracao,
      });
      return retorno;
    },
  };

  desenhar();
})();
