// ---------- Kai Breakout — Service Worker (offline cache) ----------
// Pre-caches the game's assets so it loads instantly with no network. Bump the
// CACHE_VERSION whenever you ship a new build so old clients fetch the new files.
const CACHE_VERSION = 'kai-breakout-v11';
const ASSETS = [
  './',
  './index.html',
  './kai-breakout.html',
  './KaiBreakout Logo.png',
  './kaiball.png',
  './kaiball silly.png',
  './nozomiball.png',
  './ayaball.png',
  './superkai.png',
  './papaitem.png',
  './papapaddle.png',
  './akhilball.png',
  './akhilball-surprised.png',
  './akhilglasses.png',
  './bigG-idle.png',
  './bigG-casting.png',
  './bigG-hit.png',
  './bigG-dead.png',
  './webapp icon.png',
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE_VERSION).then(cache =>
      // addAll is atomic — if any one asset fails, the whole install fails so
      // we don't end up with a half-cached game. We tolerate that risk by using
      // Promise.allSettled instead, which keeps whatever assets DID load.
      Promise.allSettled(ASSETS.map(url =>
        fetch(url, { cache: 'no-cache' }).then(res => {
          if (res.ok) return cache.put(url, res);
        }).catch(() => {})
      ))
    ).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  // Wipe old caches so updates don't pile up.
  e.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys.filter(k => k !== CACHE_VERSION).map(k => caches.delete(k))
    )).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  // Only handle same-origin GETs. Cross-origin requests (Google Fonts) go to
  // the network as usual.
  if (e.request.method !== 'GET') return;
  const url = new URL(e.request.url);
  if (url.origin !== self.location.origin) return;

  // Cache-first strategy: return cached asset if we have it, otherwise fetch
  // from network and cache the result. If network also fails (offline + not
  // cached), we just let the request reject.
  e.respondWith(
    caches.match(e.request).then(cached => {
      if (cached) {
        // Refresh in the background so the next visit gets the latest.
        fetch(e.request).then(res => {
          if (res && res.ok) caches.open(CACHE_VERSION).then(c => c.put(e.request, res));
        }).catch(() => {});
        return cached;
      }
      return fetch(e.request).then(res => {
        if (res && res.ok) {
          const clone = res.clone();
          caches.open(CACHE_VERSION).then(c => c.put(e.request, clone));
        }
        return res;
      });
    })
  );
});
