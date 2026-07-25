/* Interações gerais: menu, notificações e utilidades de rede. */

(function () {
  const abrir = document.querySelector('.abre-menu');
  const menu = document.querySelector('.menu');
  if (abrir && menu) {
    abrir.addEventListener('click', () => menu.classList.toggle('aberto'));
  }
})();

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
