// static/js/storage.js - Gestion du stockage local

class StorageManager {
    constructor() {
        this.quota = 0;
        this.usage = 0;
        this.init();
    }
    
    async init() {
        await this.updateStorageInfo();
        this.checkLowStorage();
        
        // Écouter les changements de stockage
        window.addEventListener('storage', () => this.updateStorageInfo());
    }
    
    async updateStorageInfo() {
        if ('storage' in navigator && 'estimate' in navigator.storage) {
            const estimate = await navigator.storage.estimate();
            this.quota = estimate.quota;
            this.usage = estimate.usage;
            
            const usageMB = (this.usage / (1024 * 1024)).toFixed(2);
            const quotaMB = (this.quota / (1024 * 1024)).toFixed(0);
            const percent = ((this.usage / this.quota) * 100).toFixed(1);
            
            console.log(`💾 Stockage: ${usageMB} MB / ${quotaMB} MB (${percent}%)`);
            
            // Mettre à jour l'affichage si présent
            const storageElement = document.getElementById('storage-info');
            if (storageElement) {
                storageElement.innerHTML = `
                    <i class="fas fa-hdd"></i> ${usageMB} MB / ${quotaMB} MB
                    <div class="storage-bar"><div style="width: ${percent}%;"></div></div>
                `;
            }
        }
    }
    
    async checkLowStorage() {
        const percent = (this.usage / this.quota) * 100;
        
        if (percent > 80 && percent < 90) {
            this.showWarning('Stockage faible', 'Plus que 20% d\'espace disponible.');
        } else if (percent > 90) {
            this.showWarning('Stockage critique', 'Veuillez libérer de l\'espace en supprimant des cours.');
        }
    }
    
    async clearOldCache(daysOld = 30) {
        if ('caches' in window) {
            const cacheNames = await caches.keys();
            const now = Date.now();
            const cutoff = now - (daysOld * 24 * 60 * 60 * 1000);
            
            for (const name of cacheNames) {
                const cache = await caches.open(name);
                const requests = await cache.keys();
                
                for (const request of requests) {
                    const response = await cache.match(request);
                    if (response) {
                        const dateHeader = response.headers.get('date');
                        if (dateHeader) {
                            const cacheDate = new Date(dateHeader).getTime();
                            if (cacheDate < cutoff) {
                                await cache.delete(request);
                                console.log('🗑️ Cache supprimé:', request.url);
                            }
                        }
                    }
                }
            }
        }
    }
    
    showWarning(title, message) {
        const warningDiv = document.createElement('div');
        warningDiv.className = 'storage-warning';
        warningDiv.innerHTML = `
            <div class="warning-content">
                <i class="fas fa-exclamation-triangle"></i>
                <strong>${title}</strong> ${message}
                <button onclick="this.parentElement.parentElement.remove()">OK</button>
            </div>
        `;
        warningDiv.style.cssText = `
            position: fixed; bottom: 20px; left: 20px; right: 20px;
            background: #fff3cd; color: #856404; padding: 12px;
            border-radius: 8px; z-index: 10000; text-align: center;
        `;
        document.body.appendChild(warningDiv);
        
        setTimeout(() => warningDiv.remove(), 10000);
    }
    
    async getCourseSize(courseId) {
        const db = await this.openDatabase();
        return new Promise((resolve) => {
            const tx = db.transaction(['courses'], 'readonly');
            const request = tx.objectStore('courses').get(courseId.toString());
            request.onsuccess = () => resolve(request.result?.size || 0);
            request.onerror = () => resolve(0);
        });
    }
    
    openDatabase() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open('ventoryx_courses', 1);
            request.onerror = () => reject(request.error);
            request.onsuccess = () => resolve(request.result);
            request.onupgradeneeded = (event) => {
                const db = event.target.result;
                if (!db.objectStoreNames.contains('courses')) {
                    db.createObjectStore('courses', { keyPath: 'id' });
                }
            };
        });
    }
}

// Initialisation
const storageManager = new StorageManager();
window.storageManager = storageManager;
