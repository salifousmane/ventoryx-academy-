// static/js/network.js - Gestion réseau et synchronisation

class NetworkManager {
    constructor() {
        this.isOnline = navigator.onLine;
        this.pendingSync = [];
        this.init();
    }
    
    init() {
        // Écouter les changements de connexion
        window.addEventListener('online', () => this.onOnline());
        window.addEventListener('offline', () => this.onOffline());
        
        // Vérifier périodiquement
        setInterval(() => this.checkConnection(), 30000);
        
        // Afficher le statut
        this.showStatus();
    }
    
    onOnline() {
        this.isOnline = true;
        this.showStatus('🟢 Connecté', 'success');
        this.syncPendingData();
        
        // Notifier l'utilisateur
        if ('Notification' in window && Notification.permission === 'granted') {
            new Notification('Connexion rétablie', {
                body: 'Vous êtes de nouveau connecté à internet.',
                icon: '/static/images/icon-192.png'
            });
        }
    }
    
    onOffline() {
        this.isOnline = false;
        this.showStatus('🔴 Hors-ligne (mode dégradé)', 'warning');
        
        // Notifier
        if ('Notification' in window && Notification.permission === 'granted') {
            new Notification('Mode hors-ligne activé', {
                body: 'Vous pouvez continuer à consulter vos cours téléchargés.',
                icon: '/static/images/icon-192.png'
            });
        }
    }
    
    checkConnection() {
        fetch('/health/', { 
            method: 'HEAD', 
            cache: 'no-store',
            headers: { 'X-Health-Check': 'true' }
        })
        .then(response => {
            if (!this.isOnline && response.ok) this.onOnline();
            else if (this.isOnline && !response.ok) this.onOffline();
        })
        .catch(() => {
            if (this.isOnline) this.onOffline();
        });
    }
    
    showStatus(message, type = 'info') {
        let statusDiv = document.getElementById('network-status');
        if (!statusDiv) {
            statusDiv = document.createElement('div');
            statusDiv.id = 'network-status';
            statusDiv.style.cssText = `
                position: fixed; bottom: 20px; right: 20px;
                padding: 8px 16px; border-radius: 50px;
                font-size: 12px; z-index: 10000;
                backdrop-filter: blur(10px);
                transition: all 0.3s;
            `;
            document.body.appendChild(statusDiv);
        }
        
        statusDiv.innerHTML = message;
        statusDiv.style.background = type === 'warning' ? '#fff3cd' : '#d4edda';
        statusDiv.style.color = type === 'warning' ? '#856404' : '#155724';
        
        setTimeout(() => {
            if (statusDiv.innerHTML === message) {
                statusDiv.style.opacity = '0';
                setTimeout(() => statusDiv.remove(), 1000);
            }
        }, 3000);
    }
    
    async syncPendingData() {
        console.log('🔄 Synchronisation des données en attente...');
        
        // Récupérer les données en attente
        const pending = localStorage.getItem('pending_sync');
        if (pending) {
            const data = JSON.parse(pending);
            for (const item of data) {
                try {
                    await fetch(item.url, {
                        method: item.method,
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(item.data)
                    });
                } catch (error) {
                    console.error('Erreur synchronisation:', error);
                }
            }
            localStorage.removeItem('pending_sync');
        }
        
        // Background sync avec Service Worker
        if ('serviceWorker' in navigator && navigator.serviceWorker.controller) {
            navigator.serviceWorker.ready.then(reg => {
                if (reg.sync) {
                    reg.sync.register('sync-downloads');
                }
            });
        }
        
        console.log('✅ Synchronisation terminée');
    }
    
    queueForSync(url, method, data) {
        const pending = JSON.parse(localStorage.getItem('pending_sync') || '[]');
        pending.push({ url, method, data, timestamp: Date.now() });
        localStorage.setItem('pending_sync', JSON.stringify(pending));
        
        this.showStatus('⏳ Données en attente de synchronisation', 'info');
    }
}

// Initialisation
const networkManager = new NetworkManager();

// API exposée globalement
window.networkManager = networkManager;
window.isOnline = () => networkManager.isOnline;
