// static/js/pwa.js - Gestion PWA et installation

class PWAManager {
    constructor() {
        this.deferredPrompt = null;
        this.isInstalled = false;
        this.init();
    }
    
    async init() {
        // Détecter si déjà installé
        if (window.matchMedia('(display-mode: standalone)').matches) {
            this.isInstalled = true;
            console.log('📱 PWA installée et en cours d\'exécution');
        }
        
        // Écouter l'événement beforeinstallprompt
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            this.deferredPrompt = e;
            this.showInstallBanner();
        });
        
        // Écouter l'installation réussie
        window.addEventListener('appinstalled', () => {
            this.isInstalled = true;
            this.deferredPrompt = null;
            console.log('✅ PWA installée avec succès');
            this.showNotification('Installation réussie !');
        });
        
        // Mettre à jour le service worker
        await this.updateServiceWorker();
    }
    
    showInstallBanner() {
        let banner = document.getElementById('pwa-install-banner');
        if (banner) return;
        
        banner = document.createElement('div');
        banner.id = 'pwa-install-banner';
        banner.innerHTML = `
            <div class="install-banner">
                <div class="install-content">
                    <i class="fas fa-download"></i>
                    <div>
                        <strong>Installer Ventoryx Academy</strong>
                        <small>Accédez hors-ligne et plus rapide</small>
                    </div>
                    <button id="pwa-install-btn">Installer</button>
                    <button id="pwa-close-btn">×</button>
                </div>
            </div>
        `;
        
        banner.style.cssText = `
            position: fixed; bottom: 0; left: 0; right: 0;
            background: #0F1C2E; color: white; padding: 16px;
            z-index: 10000; transform: translateY(100%);
            transition: transform 0.3s ease;
        `;
        
        document.body.appendChild(banner);
        
        // Animation d'entrée
        setTimeout(() => banner.style.transform = 'translateY(0)', 100);
        
        document.getElementById('pwa-install-btn').onclick = () => this.installPWA();
        document.getElementById('pwa-close-btn').onclick = () => {
            banner.style.transform = 'translateY(100%)';
            setTimeout(() => banner.remove(), 300);
            localStorage.setItem('pwa-banner-dismissed', Date.now());
        };
    }
    
    async installPWA() {
        if (!this.deferredPrompt) {
            console.log('Installation non disponible');
            return;
        }
        
        this.deferredPrompt.prompt();
        const result = await this.deferredPrompt.userChoice;
        
        if (result.outcome === 'accepted') {
            console.log('✅ Installation acceptée');
        } else {
            console.log('❌ Installation refusée');
        }
        
        this.deferredPrompt = null;
        
        // Supprimer la bannière
        const banner = document.getElementById('pwa-install-banner');
        if (banner) banner.remove();
    }
    
    async updateServiceWorker() {
        if ('serviceWorker' in navigator) {
            const registration = await navigator.serviceWorker.ready;
            
            // Vérifier les mises à jour toutes les heures
            setInterval(async () => {
                await registration.update();
                console.log('🔄 Vérification mise à jour Service Worker');
            }, 60 * 60 * 1000);
            
            // Notifier l'utilisateur d'une mise à jour
            registration.addEventListener('updatefound', () => {
                const newWorker = registration.installing;
                newWorker.addEventListener('statechange', () => {
                    if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                        this.showUpdateNotification();
                    }
                });
            });
        }
    }
    
    showUpdateNotification() {
        const notification = document.createElement('div');
        notification.innerHTML = `
            <div class="update-notification">
                <i class="fas fa-sync-alt"></i>
                Une nouvelle version est disponible.
                <button id="update-btn">Mettre à jour</button>
            </div>
        `;
        notification.style.cssText = `
            position: fixed; top: 20px; right: 20px;
            background: #0077B6; color: white; padding: 12px 20px;
            border-radius: 50px; z-index: 10000;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        `;
        document.body.appendChild(notification);
        
        document.getElementById('update-btn').onclick = () => {
            window.location.reload();
        };
        
        setTimeout(() => notification.remove(), 10000);
    }
    
    showNotification(message) {
        if ('Notification' in window && Notification.permission === 'granted') {
            new Notification('Ventoryx Academy', { body: message, icon: '/static/images/icon-192.png' });
        } else if ('Notification' in window) {
            Notification.requestPermission();
        }
    }
    
    async getUpdateStatus() {
        const registration = await navigator.serviceWorker.ready;
        return {
            scope: registration.scope,
            active: registration.active?.state,
            waiting: registration.waiting?.state
        };
    }
}

// Initialisation
const pwaManager = new PWAManager();
window.pwaManager = pwaManager;
