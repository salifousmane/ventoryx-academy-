/**
 * site.js - Script global Ventoryx Academy
 * Version corrigée avec URLs cohérentes.
 */

(function() {
    'use strict';

    function ready(fn) {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', fn);
        } else {
            fn();
        }
    }

    // ============ NOTIFICATIONS (cloche + panneau) ============
    function initNotifications() {
        const bell = document.getElementById('notificationBell');
        const panel = document.getElementById('notificationPanel');

        if (bell && panel) {
            bell.addEventListener('click', function(e) {
                e.stopPropagation();
                panel.classList.toggle('show');
                chargerNotifications();
            });

            document.addEventListener('click', function(e) {
                if (!bell.contains(e.target) && !panel.contains(e.target)) {
                    panel.classList.remove('show');
                }
            });
        }
    }

    function chargerNotifications() {
        const panel = document.getElementById('notificationPanel');
        if (!panel) return;

        // CORRECTION : URL corrigée vers messaging
        fetch('/messaging/notifications/')
            .then(response => response.json())
            .then(data => {
                if (data.notifications && data.notifications.length > 0) {
                    let html = '';
                    data.notifications.slice(0, 10).forEach(notif => {
                        const notifClass = notif.est_lue ? '' : 'style="background: rgba(0,119,182,0.05); border-left: 3px solid #0077B6;"';
                        html += `
                            <div ${notifClass} style="padding: 0.8rem 1rem; border-bottom: 1px solid #E9ECEF;">
                                <div style="font-size: 0.85rem; ${!notif.est_lue ? 'font-weight: 600;' : ''}">${escapeHtml(notif.titre)}</div>
                                <div style="font-size: 0.75rem; color: #6C757D;">${escapeHtml(notif.message)}</div>
                                <div style="font-size: 0.65rem; color: #ADB5BD;">${new Date(notif.date).toLocaleString('fr-FR')}</div>
                            </div>
                        `;
                    });
                    if (data.non_lues > 0) {
                        const badge = document.getElementById('notificationBadge');
                        if (badge) {
                            badge.textContent = data.non_lues;
                            badge.style.display = 'flex';
                        }
                    }
                    panel.innerHTML = html;
                } else {
                    panel.innerHTML = `
                        <div style="padding: 2rem; text-align: center; color: #6C757D;">
                            <i class="fas fa-bell-slash" style="font-size: 1.5rem; display: block; margin-bottom: 0.5rem;"></i>
                            Aucune notification
                        </div>
                    `;
                }
            })
            .catch(error => {
                console.error('Erreur chargement notifications:', error);
            });
    }

    function escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // ============ TOAST NOTIFICATION ============
    window.showToast = function(message, type) {
        type = type || 'info';
        const colors = {
            success: '#10b981',
            error: '#ef4444',
            warning: '#f59e0b',
            info: '#3b82f6'
        };

        const toast = document.createElement('div');
        toast.style.cssText = `
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            background: ${colors[type] || colors.info};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 10px;
            font-family: 'Montserrat', sans-serif;
            font-weight: 600;
            font-size: 0.9rem;
            z-index: 9999;
            box-shadow: 0 8px 24px rgba(0,0,0,0.2);
            animation: slideIn 0.3s ease;
        `;
        toast.textContent = message;
        document.body.appendChild(toast);

        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transition = 'opacity 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 3500);
    };

    // ============ CSRF TOKEN ============
    function getCSRFToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith('csrftoken=')) {
                return cookie.substring('csrftoken='.length);
            }
        }
        return document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    }

    // ============ FORMULAIRE DE CONTACT (honeypot) ============
    function initContactForm() {
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', function(e) {
                const honeypot = form.querySelector('input[name="website"]');
                if (honeypot && honeypot.value.trim() !== '') {
                    e.preventDefault();
                    return false;
                }
            });
        });
    }

    // ============ MENU MOBILE ============
    function initMobileMenu() {
        const menuToggle = document.getElementById('menuToggle');
        const mainNav = document.getElementById('mainNav');

        if (menuToggle && mainNav) {
            menuToggle.addEventListener('click', function(e) {
                e.stopPropagation();
                mainNav.classList.toggle('active');
            });

            document.addEventListener('click', function(e) {
                if (!e.target.closest('nav') && !e.target.closest('.menu-toggle')) {
                    mainNav.classList.remove('active');
                }
            });
        }
    }

    // ============ MESSAGES FLASH ============
    function initFlashMessages() {
        const flashMessages = document.querySelectorAll('.message');
        flashMessages.forEach(function(msg) {
            setTimeout(function() {
                msg.style.opacity = '0';
                msg.style.transition = 'opacity 0.3s ease';
                setTimeout(function() {
                    if (msg.parentNode) msg.parentNode.removeChild(msg);
                }, 300);
            }, 5000);
        });
    }

    // ============ INITIALISATION ============
    function init() {
        initMobileMenu();
        initFlashMessages();
        initNotifications();
        initContactForm();
        
        if (!document.querySelector('#toastAnimationStyle')) {
            const style = document.createElement('style');
            style.id = 'toastAnimationStyle';
            style.textContent = `
                @keyframes slideIn {
                    from { transform: translateX(100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
            `;
            document.head.appendChild(style);
        }
    }

    ready(init);

})(); ============ ANIMATION AU SCROLL ============
    function initScrollAnimation() {
        if (!('IntersectionObserver' in window)) return;

        const observerOptions = { threshold: 0.1, rootMargin: '0px 0px -50px 0px' };
        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        document.querySelectorAll('.stat-card, .card, .communication-card, .metier-card, .module-card').forEach(function(card) {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            observer.observe(card);
        });
    }

    // ============ ESCAPE HTML ============
    function escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    // ============ FORMULAIRE DE CONTACT (honeypot) ============
    function initContactForm() {
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', function(e) {
                const honeypot = form.querySelector('input[name="website"]');
                if (honeypot && honeypot.value.trim() !== '') {
                    e.preventDefault();
                    return false;
                }
            });
        });
    }

    // ============ INITIALISATION ============
    function init() {
        initMobileMenu();
        initFlashMessages();
        initNotifications();
        initActionButtons();
        initScrollAnimation();
        initContactForm();
        
        // Ajouter l'animation CSS pour les toasts si non présente
        if (!document.querySelector('#toastAnimationStyle')) {
            const style = document.createElement('style');
            style.id = 'toastAnimationStyle';
            style.textContent = `
                @keyframes slideIn {
                    from { transform: translateX(100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
            `;
            document.head.appendChild(style);
        }
    }

    ready(init);

})();
