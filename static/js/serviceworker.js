var staticCacheName = "django-pwa-v" + new Date().getTime();
var filesToCache = [
    '/',
    '/static/css/style.css',
];

// Cache on install
self.addEventListener("install", event => {
    self.skipWaiting();
    event.waitUntil(
        caches.open(staticCacheName)
            .then(cache => {
                return cache.addAll(filesToCache);
            })
    )
});

// Take control of all pages immediately 
self.addEventListener('activate', event => {
    event.waitUntil(self.clients.claim());
    event.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.filter(cacheName => cacheName.startsWith("django-pwa-"))
                    .filter(cacheName => cacheName !== staticCacheName)
                    .map(cacheName => caches.delete(cacheName))
            );
        })
    );
});

// Serve from cache
self.addEventListener("fetch", event => {
    // Skip non-GET requests entirely (like POST logins)
    if (event.request.method !== "GET") {
        return; 
    }

    event.respondWith(
        caches.match(event.request)
            .then(response => {
                // If it's in the cache, return it
                if (response) {
                    return response;
                }
                // Otherwise, try to fetch from network
                return fetch(event.request).catch(() => {
                    // Final offline fallback: if it's the root page, try to return it from cache
                    if (event.request.mode === 'navigate') {
                        return caches.match('/');
                    }
                    return null;
                });
            })
    )
});
