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
