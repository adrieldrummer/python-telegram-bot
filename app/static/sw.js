/* Service worker da Operação Aprovação.

   Objetivo: abrir rápido em 4G ruim e não mostrar a tela de dinossauro quando
   a conexão cai no meio do estudo.

   Estratégia por tipo de pedido:
   - estáticos (CSS, JS, imagens): cache primeiro, rede em segundo plano.
     São versionados pelo nome do cache, então nunca servem conteúdo velho
     depois de um deploy.
   - páginas: rede primeiro, cache como rede de segurança. Progresso, pontos e
     bloqueio de plano mudam a toda hora — servir página do cache mostraria
     estado errado, que é pior que esperar meio segundo.
   - nada de POST, /api/, /admin/ ou /webhooks/: resposta de estudo e de
     pagamento nunca podem sair de cache.
*/

const VERSAO = 'oa-v3';
const CACHE_CASCO = `${VERSAO}-casco`;
const CACHE_PAGINAS = `${VERSAO}-paginas`;

const CASCO = [
  '/static/css/app.css',
  '/static/js/app.js',
  '/static/js/questoes.js',
  '/static/img/emblema.png',
  '/static/img/favicon.png',
  '/static/img/icone-192.png',
  '/offline',
];

self.addEventListener('install', (evento) => {
  evento.waitUntil(
    caches.open(CACHE_CASCO)
      // addAll falha inteiro se um item falhar; aqui um estático ausente não
      // pode impedir o service worker de instalar
      .then((cache) => Promise.allSettled(CASCO.map((url) => cache.add(url))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (evento) => {
  evento.waitUntil(
    caches.keys()
      .then((chaves) => Promise.all(
        chaves.filter((c) => !c.startsWith(VERSAO)).map((c) => caches.delete(c))
      ))
      .then(() => self.clients.claim())
  );
});

function ehEstatico(url) {
  return url.pathname.startsWith('/static/');
}

function foraDoCache(url) {
  return url.pathname.startsWith('/api/')
    || url.pathname.startsWith('/admin')
    || url.pathname.startsWith('/webhooks/')
    || url.pathname.startsWith('/manual/download');
}

self.addEventListener('fetch', (evento) => {
  const pedido = evento.request;
  if (pedido.method !== 'GET') return;

  const url = new URL(pedido.url);
  if (url.origin !== self.location.origin) return;
  if (foraDoCache(url)) return;

  if (ehEstatico(url)) {
    evento.respondWith(
      caches.match(pedido).then((guardado) => {
        const daRede = fetch(pedido).then((resposta) => {
          if (resposta.ok) {
            const copia = resposta.clone();
            caches.open(CACHE_CASCO).then((cache) => cache.put(pedido, copia));
          }
          return resposta;
        }).catch(() => guardado);
        return guardado || daRede;
      })
    );
    return;
  }

  if (pedido.mode === 'navigate') {
    evento.respondWith(
      fetch(pedido)
        .then((resposta) => {
          if (resposta.ok) {
            const copia = resposta.clone();
            caches.open(CACHE_PAGINAS).then((cache) => cache.put(pedido, copia));
          }
          return resposta;
        })
        .catch(() => caches.match(pedido).then((g) => g || caches.match('/offline')))
    );
  }
});
