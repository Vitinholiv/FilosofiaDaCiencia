const CACHE_NAME = 'timeline-cache-v1';
const CORE_ASSETS = [
  './', './index.html',
  './css/base.css',
  './js/base.js', './js/scroller.js', './js/timeline.js', './css/cy_styles.js',
  './timeline.json'
];

self.addEventListener('install', (event) => {
  event.waitUntil(caches.open(CACHE_NAME).then(async (cache) => {
    await cache.addAll(CORE_ASSETS);
    try {
      const res = await fetch('./img-manifest.json');
      const images = await res.json();
      await cache.addAll(images);
    } catch (e) { console.warn('Não deu pra pré-cachear as imagens:', e); }
  }));
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(caches.keys().then(keys =>
    Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
  ));
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then(cached => cached || fetch(event.request).then(res => {
      if (res.ok) caches.open(CACHE_NAME).then(c => c.put(event.request, res.clone()));
      return res;
    }).catch(() => cached))
  );
});