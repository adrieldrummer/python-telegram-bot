/* Interações gerais: menu, gaveta do celular, notificações e rede. */

/* Menu do visitante (gaveta a partir do topo). */
(function () {
  const abrir = document.querySelector('.abre-menu');
  const menu = document.querySelector('.menu');
  if (!abrir || !menu) return;
  abrir.addEventListener('click', () => {
    const aberto = menu.classList.toggle('aberto');
    abrir.setAttribute('aria-expanded', String(aberto));
  });
  menu.addEventListener('click', (e) => {
    if (e.target.tagName === 'A') menu.classList.remove('aberto');
  });
})();

/* Gaveta "Mais" da barra inferior do aluno. */
(function () {
  const botao = document.querySelector('.abre-gaveta');
  const gaveta = document.querySelector('.gaveta');
  if (!botao || !gaveta) return;
  const painel = gaveta.querySelector('.gaveta-painel');

  function abrir() {
    gaveta.hidden = false;
    // o próximo quadro garante a transição: sem isso o navegador
    // aplica o estado final de uma vez e a gaveta "aparece" sem animar
    requestAnimationFrame(() => gaveta.classList.add('aberta'));
    botao.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
  }
  function fechar() {
    gaveta.classList.remove('aberta');
    botao.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
    setTimeout(() => { gaveta.hidden = true; }, 240);
  }

  botao.addEventListener('click', () => (gaveta.classList.contains('aberta') ? fechar() : abrir()));
  gaveta.addEventListener('click', (e) => { if (e.target === gaveta) fechar(); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && !gaveta.hidden) fechar(); });

  /* arrastar para baixo fecha — o gesto que todo app de celular tem */
  let inicio = null;
  painel.addEventListener('touchstart', (e) => { inicio = e.touches[0].clientY; }, { passive: true });
  painel.addEventListener('touchmove', (e) => {
    if (inicio === null) return;
    const arrasto = e.touches[0].clientY - inicio;
    // só arrasta quando a gaveta já está no topo da própria rolagem
    if (arrasto > 0 && painel.scrollTop <= 0) painel.style.transform = `translateY(${arrasto}px)`;
  }, { passive: true });
  painel.addEventListener('touchend', (e) => {
    const arrasto = e.changedTouches[0].clientY - (inicio || 0);
    painel.style.transform = '';
    inicio = null;
    if (arrasto > 90) fechar();
  });
})();

/* Instalação na tela de início: guarda o convite do navegador e oferece
   quando houver um botão pedindo por ele. */
(function () {
  let convite = null;
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    convite = e;
    document.querySelectorAll('[data-instalar]').forEach((b) => { b.hidden = false; });
  });
  document.addEventListener('click', (e) => {
    const botao = e.target.closest('[data-instalar]');
    if (!botao || !convite) return;
    convite.prompt();
    convite = null;
    botao.hidden = true;
  });
})();

/* Service worker: casco em cache para abrir rápido no 4G e uma tela
   decente quando a conexão cai no meio do estudo. */
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js').catch(() => {});
  });
}

/* --- fila de respostas pendentes -------------------------------------------
   No celular a conexão cai no meio do bloco de questões: túnel, elevador,
   4G ruim. Sem isso, a resposta some e o aluno refaz a questão achando que
   o site "perdeu" o estudo dele. A resposta fica guardada no aparelho e sobe
   sozinha quando a conexão volta.
   ------------------------------------------------------------------------- */

const FILA = 'oa_respostas_pendentes';

function lerFila() {
  try {
    return JSON.parse(localStorage.getItem(FILA) || '[]');
  } catch (e) {
    return [];
  }
}

function gravarFila(itens) {
  try {
    localStorage.setItem(FILA, JSON.stringify(itens.slice(-200)));
  } catch (e) {
    /* aparelho sem espaço: melhor perder a fila do que travar a tela */
  }
}

window.MAPA = {
  csrf() {
    const meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.content : '';
  },

  async postJSON(url, dados) {
    const resposta = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRF-Token': this.csrf() },
      body: JSON.stringify(dados),
    });
    let corpo = {};
    try {
      corpo = await resposta.json();
    } catch (e) {
      corpo = {};
    }
    if (!resposta.ok) {
      const erro = new Error(corpo.erro || corpo.detail || 'Não foi possível concluir a ação.');
      erro.status = resposta.status;
      throw erro;
    }
    return corpo;
  },

  /* Guarda uma resposta que não conseguiu subir. */
  enfileirar(url, dados) {
    const itens = lerFila();
    // a mesma questão não entra duas vezes: reenviar duplicaria pontos
    const chave = (d) => `${d.questao_id}|${d.sessao_id || ''}|${d.dia || ''}`;
    if (itens.some((i) => chave(i.dados) === chave(dados))) return;
    itens.push({ url: url, dados: dados, em: Date.now() });
    gravarFila(itens);
    this.mostrarPendentes();
  },

  pendentes() {
    return lerFila().length;
  },

  mostrarPendentes() {
    const total = this.pendentes();
    let selo = document.querySelector('[data-pendentes]');
    if (!total) {
      if (selo) selo.remove();
      return;
    }
    if (!selo) {
      selo = document.createElement('div');
      selo.className = 'selo-pendentes';
      selo.setAttribute('data-pendentes', '');
      document.body.appendChild(selo);
    }
    selo.textContent = `${total} resposta${total > 1 ? 's' : ''} aguardando conexão`;
  },

  /* Tenta subir tudo que ficou para trás. Silencioso: se falhar de novo,
     continua guardado para a próxima tentativa. */
  async esvaziarFila() {
    const itens = lerFila();
    if (!itens.length || !navigator.onLine) return;
    const restantes = [];
    let enviadas = 0;
    for (const item of itens) {
      try {
        const resposta = await fetch(item.url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', 'X-CSRF-Token': this.csrf() },
          body: JSON.stringify(item.dados),
        });
        // 4xx que não é de rede: a resposta não vai ser aceita nunca,
        // insistir só encheria a fila para sempre
        if (resposta.ok || (resposta.status >= 400 && resposta.status < 500)) {
          if (resposta.ok) {
            enviadas += 1;
            // o placar do topo precisa refletir os pontos que acabaram de entrar
            try {
              const corpo = await resposta.json();
              this.atualizarPontos(corpo.pontos_totais);
              this.medalhas(corpo.medalhas);
            } catch (e) {
              /* resposta sem corpo útil não impede a fila de andar */
            }
          }
        } else {
          restantes.push(item);
        }
      } catch (e) {
        restantes.push(item);
      }
    }
    gravarFila(restantes);
    this.mostrarPendentes();
    if (enviadas) {
      this.aviso(`${enviadas} resposta(s) guardada(s) foram salvas agora.`, 'ok');
    }
  },

  aviso(texto, tipo) {
    let caixa = document.querySelector('.toaster');
    if (!caixa) {
      caixa = document.createElement('div');
      caixa.className = 'toaster';
      document.body.appendChild(caixa);
    }
    const item = document.createElement('div');
    item.className = 'toast' + (tipo === 'ok' ? ' ok' : '');
    item.innerHTML = texto;
    caixa.appendChild(item);
    setTimeout(() => {
      item.style.opacity = '0';
      item.style.transition = 'opacity 300ms';
      setTimeout(() => item.remove(), 320);
    }, 5200);
  },

  medalhas(lista) {
    (lista || []).forEach((m) => {
      this.aviso(`<strong>${m.icone} ${m.nome}</strong><br><span class="suave">${m.descricao}</span>`, 'ok');
    });
  },

  atualizarPontos(total) {
    const alvo = document.querySelector('[data-pontos]');
    if (alvo && typeof total === 'number') {
      alvo.textContent = total.toLocaleString('pt-BR');
    }
  },
};

/* Sobe o que ficou pendente ao abrir a página e assim que a conexão voltar. */
(function () {
  function tentar() {
    if (window.MAPA) window.MAPA.esvaziarFila();
  }
  window.addEventListener('online', tentar);
  document.addEventListener('visibilitychange', function () {
    if (document.visibilityState === 'visible') tentar();
  });
  window.addEventListener('load', function () {
    window.MAPA.mostrarPendentes();
    tentar();
  });
})();

/* --- movimento -------------------------------------------------------------
   Revelação ao rolar e contadores que sobem. Ambos degradam sozinhos: sem
   IntersectionObserver, o conteúdo simplesmente aparece; com
   prefers-reduced-motion, o número vai direto ao valor final.
   ------------------------------------------------------------------------- */
(function () {
  const paradinho = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const alvos = document.querySelectorAll('.revela, .revela-fila');

  if (paradinho || !('IntersectionObserver' in window)) {
    alvos.forEach((el) => el.classList.add('visivel'));
    document.querySelectorAll('[data-contar]').forEach((el) => {
      el.textContent = Number(el.dataset.contar).toLocaleString('pt-BR');
    });
    return;
  }

  const observador = new IntersectionObserver(
    (entradas) => {
      entradas.forEach((e) => {
        if (!e.isIntersecting) return;
        e.target.classList.add('visivel');
        observador.unobserve(e.target);
      });
    },
    // 12% do bloco visível já dispara: esperar metade faz o efeito chegar tarde
    { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
  );
  alvos.forEach((el) => observador.observe(el));

  /* contadores: sobem até o valor real quando entram na tela */
  const contadores = new IntersectionObserver((entradas) => {
    entradas.forEach((e) => {
      if (!e.isIntersecting) return;
      const el = e.target;
      contadores.unobserve(el);
      const destino = Number(el.dataset.contar || '0');
      const duracao = 900;
      const inicio = performance.now();
      function passo(agora) {
        const t = Math.min((agora - inicio) / duracao, 1);
        // desacelera no fim: número que para de repente parece travado
        const suave = 1 - Math.pow(1 - t, 3);
        el.textContent = Math.round(destino * suave).toLocaleString('pt-BR');
        if (t < 1) requestAnimationFrame(passo);
      }
      requestAnimationFrame(passo);
    });
  }, { threshold: 0.5 });
  document.querySelectorAll('[data-contar]').forEach((el) => contadores.observe(el));
})();

/* --- relógio regressivo -----------------------------------------------------
   Conta até o instante da prova, atualizando a cada segundo. O alvo vem do
   servidor com fuso explícito, então a conta usa dois instantes absolutos e
   fica certa em qualquer fuso do aluno.
   ------------------------------------------------------------------------- */
(function () {
  const relogios = document.querySelectorAll('[data-relogio]');
  if (!relogios.length) return;

  function dois(n) {
    return String(n).padStart(2, '0');
  }

  function pintar(el, restante) {
    const casas = {
      dias: Math.floor(restante / 86400),
      horas: Math.floor((restante % 86400) / 3600),
      minutos: Math.floor((restante % 3600) / 60),
      segundos: Math.floor(restante % 60),
    };
    Object.keys(casas).forEach(function (nome) {
      const alvo = el.querySelector('[data-' + nome + ']');
      if (!alvo) return;
      // dias sem zero à esquerda: "52" lê melhor que "052"
      const texto = nome === 'dias' ? String(casas[nome]) : dois(casas[nome]);
      if (alvo.textContent !== texto) {
        alvo.textContent = texto;
        if (nome === 'segundos') {
          alvo.classList.remove('bate');
          // reinicia a animação: sem o reflow o navegador ignora a reaplicação
          void alvo.offsetWidth;
          alvo.classList.add('bate');
        }
      }
    });
    // a última semana acende o relógio
    el.classList.toggle('urgente', restante < 7 * 86400);
  }

  function encerrar(el, texto) {
    el.classList.add('encerrado');
    el.innerHTML = '<strong class="relogio-fim">' + texto + '</strong>';
  }

  function tique() {
    const agora = Date.now();
    let ativos = 0;
    relogios.forEach(function (el) {
      if (el.classList.contains('encerrado')) return;
      const alvo = new Date(el.dataset.relogio).getTime();
      if (Number.isNaN(alvo)) return;
      const restante = Math.floor((alvo - agora) / 1000);
      if (restante <= 0) {
        // até 6 horas depois do início ainda é "hoje"; passou disso, acabou
        encerrar(el, restante > -6 * 3600 ? 'É agora. Boa prova. 🎯' : 'A prova já foi.');
        return;
      }
      pintar(el, restante);
      ativos += 1;
    });
    if (ativos) setTimeout(tique, 1000);
  }

  tique();
  // ao voltar para a aba, corrige o atraso acumulado enquanto ela estava oculta
  document.addEventListener('visibilitychange', function () {
    if (document.visibilityState === 'visible') tique();
  });
})();
