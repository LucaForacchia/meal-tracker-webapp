/* MealTracker service worker
 *
 * Cache strategy (the app stays online-only for DATA — backend payloads are
 * never cached, they never even pass through this worker):
 *  - static assets (same-origin /static/* and known CDN libraries):
 *      cache-first, with runtime caching of successful responses
 *  - navigations (same-origin HTML pages):
 *      network-first, falling back to the last cached copy of the page
 *      (the "app shell" — shows the last visited page when offline); the page
 *      itself shows "Non connesso al server. Copia del ..." (see base.html)
 *  - everything else (POST requests, backend API, /ping, unknown origins):
 *      left to the default network behavior
 */
// Bump to drop the copies cached by previous versions (activate deletes other caches)
const CACHE_NAME = 'mealtracker-v2';

const PRECACHE_URLS = [
  '/manifest.json',
  '/static/script_autocomplete.js',
  '/static/icons/icon-192.png',
  '/static/icons/icon-512.png',
  '/static/icons/icon-maskable-512.png',
  /* CDN libraries used by base.html (all HTTPS) */
  'https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css',
  'https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css',
  'https://fonts.googleapis.com/css?family=Roboto|Varela+Round|Open+Sans',
  'https://fonts.googleapis.com/icon?family=Material+Icons',
  'https://code.jquery.com/jquery-3.2.1.slim.min.js',
  'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js',
  'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js'
];

const CDN_ORIGINS = [
  'https://stackpath.bootstrapcdn.com',
  'https://maxcdn.bootstrapcdn.com',
  'https://cdnjs.cloudflare.com',
  'https://code.jquery.com',
  'https://fonts.googleapis.com',
  'https://fonts.gstatic.com'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(PRECACHE_URLS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(
        keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
      ))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const { request } = event;

  // Only GET requests are handled; everything else goes to the network.
  if (request.method !== 'GET') return;

  const url = new URL(request.url);

  // Same-origin navigations: network-first with fallback to last cached page.
  if (request.mode === 'navigate' && url.origin === self.location.origin) {
    event.respondWith(networkFirst(request));
    return;
  }

  // Static assets and CDN libraries: cache-first.
  const isStatic = url.origin === self.location.origin && url.pathname.startsWith('/static/');
  const isCdn = CDN_ORIGINS.includes(url.origin);
  if (isStatic || isCdn) {
    event.respondWith(cacheFirst(request));
  }
  // Anything else (backend API, other origins): default network behavior.
});

async function cacheFirst(request) {
  const cached = await caches.match(request);
  if (cached) return cached;

  const response = await fetch(request);
  if (response && response.ok) {
    const cache = await caches.open(CACHE_NAME);
    cache.put(request, response.clone());
  }
  return response;
}

async function networkFirst(request) {
  try {
    const response = await fetch(request);
    if (response && response.ok) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, response.clone());
    }
    return response;
  } catch (error) {
    const cached = await caches.match(request);
    if (cached) return cached;
    throw error;
  }
}
