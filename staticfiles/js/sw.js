// Service Worker — Ventoryx Academy
// Version complète avec IndexedDB et téléchargement Premium

const CACHE_NAME = 'ventoryx-v1.0.0';
const STATIC_CACHE_NAME = 'ventoryx-static-v1.0.0';
const DYNAMIC_CACHE_NAME = 'ventoryx-dynamic-v1.0.0';

// URLs statiques
const STATIC_URLS = [
    '/', '/offline/',
    '/static/css/style.css', '/static/css/parcours.css',
    '/static/js/site.js', '/static/js/parcours.js',
    '/static/images/logo.png', '/static/images/icon-192.png',
    '/static/images/icon-512.png', '/static/manifest.json'
];

// === INSTALLATION ===
self.addEventListener('install', (event) => {
    console.log('[SW] Installation');
    event.waitUntil(
        caches.open(STATIC_CACHE_NAME).then(cache => cache.addAll(STATIC_URLS))
    );
    self.skipWaiting();
});

// === ACTIVATION ===
self.addEventListener('activate', (event) => {
    console.log('[SW] Activation');
    event.waitUntil(
        caches.keys().then(cacheNames => Promise.all(
            cacheNames.filter(n => n !== STATIC_CACHE_NAME && n !== DYNAMIC_CACHE_NAME)
                      .map(n => caches.delete(n))
        ))
    );
    self.clients.claim();
});

// === INDEXEDDB ===
const DB_NAME = 'ventoryx_courses';
const DB_VERSION = 1;

function openDatabase() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open(DB_NAME, DB_VERSION);
        request.onerror = () => reject(request.error);
        request.onsuccess = () => resolve(request.result);
        request.onupgradeneeded = (event) => {
            const db = event.target.result;
            if (!db.objectStoreNames.contains('courses')) {
                const store = db.createObjectStore('courses', { keyPath: 'id' });
                store.createIndex('downloaded_at', 'downloaded_at');
            }
            if (!db.objectStoreNames.contains('user')) {
                db.createObjectStore('user', { keyPath: 'id' });
            }
        };
    });
}

async function getDownloadedCourse(courseId) {
    try {
        const db = await openDatabase();
        return new Promise((resolve, reject) => {
            const tx = db.transaction(['courses'], 'readonly');
            const request = tx.objectStore('courses').get(courseId.toString());
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    } catch { return null; }
}

// === FETCH ===
self.addEventListener('fetch', (event) => {
    const url = new URL(event.request.url);
    
    if (event.request.method !== 'GET') return;
    if (url.pathname.startsWith('/api/')) return;
    if (url.pathname.startsWith('/admin/')) return;
    
    // REQUÊTES DE COURS (Network First + IndexedDB)
    if (url.pathname.startsWith('/cours/') || url.pathname.startsWith('/parcours/cours/')) {
        event.respondWith(handleCourseRequest(event.request));
        return;
    }
    
    // FICHIERS STATIQUES (Cache First)
    if (url.pathname.match(/\.(css|js|png|jpg|jpeg|svg|ico|woff2?)$/)) {
        event.respondWith(handleStaticRequest(event.request));
        return;
    }
    
    // PAGES HTML (Network First)
    event.respondWith(handlePageRequest(event.request));
});

async function handleCourseRequest(request) {
    const url = new URL(request.url);
    const courseId = url.pathname.split('/').filter(Boolean).pop();
    
    // 1. IndexedDB (cours téléchargés Premium)
    const downloaded = await getDownloadedCourse(courseId);
    if (downloaded?.content) {
        return new Response(downloaded.content, {
            headers: { 'Content-Type': 'text/html', 'X-Offline': 'true' }
        });
    }
    
    // 2. Cache dynamique
    const cached = await caches.match(request);
    if (cached) return cached;
    
    // 3. Réseau
    try {
        const response = await fetch(request);
        if (response?.status === 200) {
            const clone = response.clone();
            const cache = await caches.open(DYNAMIC_CACHE_NAME);
            cache.put(request, clone);
            return response;
        }
    } catch {}
    
    // 4. Fallback offline
    return caches.match('/offline/').then(offline => offline || new Response('Hors ligne', { status: 503 }));
}

async function handleStaticRequest(request) {
    const cached = await caches.match(request);
    if (cached) return cached;
    
    try {
        const response = await fetch(request);
        if (response?.status === 200) {
            const cache = await caches.open(STATIC_CACHE_NAME);
            cache.put(request, response.clone());
            return response;
        }
    } catch {}
    
    return caches.match('/static/images/icon-512.png');
}

async function handlePageRequest(request) {
    try {
        const response = await fetch(request);
        if (response?.status === 200) {
            const cache = await caches.open(DYNAMIC_CACHE_NAME);
            cache.put(request, response.clone());
            return response;
        }
    } catch {}
    
    const cached = await caches.match(request);
    if (cached) return cached;
    return caches.match('/offline/').then(offline => offline || new Response('Hors ligne', { status: 503 }));
}

// === MESSAGES (API de communication) ===
self.addEventListener('message', (event) => {
    const { type, payload } = event.data;
    
    if (type === 'SKIP_WAITING') {
        self.skipWaiting();
        return;
    }
    
    if (type === 'DOWNLOAD_COURSE') {
        event.waitUntil(handleMessageDownload(payload));
    }
    
    if (type === 'DELETE_COURSE') {
        event.waitUntil(handleMessageDelete(payload));
    }
    
    if (type === 'GET_DOWNLOADED_COURSES' && event.ports[0]) {
        handleMessageGetCourses(event);
    }
    
    if (type === 'SET_PREMIUM_STATUS') {
        handleMessageSetPremium(payload);
    }
});

async function handleMessageDownload(payload) {
    const { courseId, title, content, size } = payload;
    const db = await openDatabase();
    const tx = db.transaction(['courses'], 'readwrite');
    tx.objectStore('courses').put({
        id: courseId, title: title, content: content,
        size: size || 30, downloaded_at: new Date().toISOString()
    });
    await tx.complete;
    
    const cache = await caches.open(DYNAMIC_CACHE_NAME);
    cache.put(`/cours/${courseId}/`, new Response(content, { headers: { 'Content-Type': 'text/html' } }));
}

async function handleMessageDelete(payload) {
    const { courseId } = payload;
    const db = await openDatabase();
    const tx = db.transaction(['courses'], 'readwrite');
    tx.objectStore('courses').delete(courseId);
    await tx.complete;
    
    const cache = await caches.open(DYNAMIC_CACHE_NAME);
    await cache.delete(`/cours/${courseId}/`);
}

async function handleMessageGetCourses(event) {
    const db = await openDatabase();
    const courses = await new Promise((resolve) => {
        const tx = db.transaction(['courses'], 'readonly');
        const request = tx.objectStore('courses').getAll();
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => resolve([]);
    });
    event.ports[0].postMessage({ type: 'DOWNLOADED_COURSES', courses });
}

async function handleMessageSetPremium(payload) {
    const { isPremium } = payload;
    const db = await openDatabase();
    const tx = db.transaction(['user'], 'readwrite');
    tx.objectStore('user').put({ id: 'current', is_premium: isPremium });
    await tx.complete;
}

// === BACKGROUND SYNC ===
self.addEventListener('sync', (event) => {
    if (event.tag === 'sync-downloads') {
        event.waitUntil(syncPending());
    }
});

async function syncPending() {
    console.log('[SW] Synchronisation en arrière-plan');
}

// === PUSH NOTIFICATIONS ===
self.addEventListener('push', (event) => {
    const data = event.data ? event.data.json() : {};
    event.waitUntil(
        self.registration.showNotification(data.title || 'Ventoryx Academy', {
            body: data.body || 'Nouveautés disponibles',
            icon: '/static/images/icon-192.png',
            data: { url: data.url || '/' }
        })
    );
});

self.addEventListener('notificationclick', (event) => {
    event.notification.close();
    event.waitUntil(clients.openWindow(event.notification.data.url));
});
