/**
 * parcours.js - Scripts pour les modules de cours et tests
 * Ventoryx Academy
 * Version corrigée et optimisée
 */

(function() {
    'use strict';

    // ============================================================
    // ATTENDRE QUE LE DOM SOIT CHARGÉ
    // ============================================================
    function ready(fn) {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', fn);
        } else {
            fn();
        }
    }

    // ============================================================
    // TERMINER UN COURS
    // ============================================================
    function initTerminerCours() {
        const btnTerminer = document.querySelector('.btn-terminer');
        if (!btnTerminer) return;

        btnTerminer.addEventListener('click', function(e) {
            e.preventDefault();
            const itemId = this.dataset.itemId;
            
            if (!itemId) {
                console.error('Aucun itemId trouvé');
                return;
            }
            
            // Effet visuel
            this.style.opacity = '0.7';
            this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Validation...';
            
            fetch('/parcours/api/terminer-cours/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken(),
                },
                body: JSON.stringify({ item_id: itemId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.ok) {
                    if (window.showToast) {
                        window.showToast('Cours terminé avec succès !', 'success');
                    }
                    setTimeout(() => location.reload(), 1000);
                } else {
                    if (window.showToast) {
                        window.showToast('Erreur : ' + (data.error || 'Inconnue'), 'error');
                    }
                    this.style.opacity = '1';
                    this.innerHTML = '<i class="fas fa-check"></i> Terminer ce cours';
                }
            })
            .catch(error => {
                console.error('Erreur:', error);
                if (window.showToast) {
                    window.showToast('Une erreur est survenue', 'error');
                }
                this.style.opacity = '1';
                this.innerHTML = '<i class="fas fa-check"></i> Terminer ce cours';
            });
        });
    }

    // ============================================================
    // SOUMETTRE UN TEST (module)
    // ============================================================
    function initTestSubmission() {
        const testForm = document.getElementById('testForm');
        if (!testForm) return;

        testForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Désactiver le bouton pendant le traitement
            const submitBtn = testForm.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Correction en cours...';
            }
            
            const formData = new FormData(this);
            
            fetch(window.location.href, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                const resultatDiv = document.getElementById('resultat');
                if (!resultatDiv) return;
                
                resultatDiv.style.display = 'block';
                resultatDiv.scrollIntoView({ behavior: 'smooth' });
                
                if (data.reussi) {
                    resultatDiv.className = 'resultat-box reussi fade-in';
                    resultatDiv.innerHTML = `
                        <i class="fas fa-trophy" style="font-size: 2.5rem; color: #D4AF37;"></i>
                        <h3>Félicitations !</h3>
                        <div class="resultat-score">${data.score}%</div>
                        <p>${data.bonnes_reponses} / ${data.total} bonnes réponses</p>
                        <p>Score minimum requis : 70%</p>
                        <div style="margin-top: 1rem;">
                            <a href="../" class="btn-cours btn-suivant" style="display: inline-block; padding: 0.7rem 1.8rem; background: #0077B6; color: white; border-radius: 50px; text-decoration: none;">
                                <i class="fas fa-arrow-right"></i> Continuer le parcours
                            </a>
                        </div>
                    `;
                    testForm.style.display = 'none';
                    if (window.showToast) {
                        window.showToast('Test réussi !', 'success');
                    }
                } else {
                    resultatDiv.className = 'resultat-box echec fade-in';
                    resultatDiv.innerHTML = `
                        <i class="fas fa-redo" style="font-size: 2.5rem; color: #ef4444;"></i>
                        <h3>Score insuffisant</h3>
                        <div class="resultat-score">${data.score}%</div>
                        <p>${data.bonnes_reponses} / ${data.total} bonnes réponses</p>
                        <p>Vous devez obtenir au moins 70%. Réessayez.</p>
                        <button onclick="location.reload()" class="btn-cours" style="margin-top: 1rem; background: #f59e0b; color: white; border: none; padding: 0.7rem 1.8rem; border-radius: 50px; cursor: pointer; font-family: 'Montserrat', sans-serif; font-weight: 600;">
                            <i class="fas fa-redo"></i> Réessayer
                        </button>
                    `;
                    if (window.showToast) {
                        window.showToast('Score insuffisant, réessayez', 'warning');
                    }
                }
            })
            .catch(error => {
                console.error('Erreur:', error);
                if (window.showToast) {
                    window.showToast('Une erreur est survenue. Veuillez réessayer.', 'error');
                }
            })
            .finally(() => {
                if (submitBtn) {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Valider mes réponses';
                }
            });
        });
    }

    // ============================================================
    // RÉORGANISATION (drag & drop) pour tests
    // ============================================================
    function initDragAndDrop() {
        const sortableLists = document.querySelectorAll('.sortable-list');
        if (!sortableLists.length) return;
        
        sortableLists.forEach(list => {
            const hiddenInput = list.parentElement.querySelector('.ordre-hidden');
            
            function updateHidden() {
                if (hiddenInput) {
                    const order = Array.from(list.querySelectorAll('.sortable-item'))
                        .map(item => item.dataset.id)
                        .join(',');
                    hiddenInput.value = order;
                }
            }
            updateHidden();

            let dragged = null;
            let dragOverElement = null;
            
            // Rendre tous les éléments draggables
            const items = list.querySelectorAll('.sortable-item');
            items.forEach(item => {
                item.setAttribute('draggable', 'true');
                
                item.addEventListener('dragstart', function(e) {
                    dragged = this;
                    this.classList.add('dragging');
                    e.dataTransfer.effectAllowed = 'move';
                    e.dataTransfer.setData('text/plain', '');
                });
                
                item.addEventListener('dragend', function(e) {
                    this.classList.remove('dragging');
                    if (dragOverElement) {
                        dragOverElement.classList.remove('drag-over');
                        dragOverElement = null;
                    }
                    dragged = null;
                    updateHidden();
                });
                
                item.addEventListener('dragover', function(e) {
                    e.preventDefault();
                    e.dataTransfer.dropEffect = 'move';
                    if (dragOverElement) dragOverElement.classList.remove('drag-over');
                    dragOverElement = this;
                    this.classList.add('drag-over');
                });
                
                item.addEventListener('dragleave', function(e) {
                    this.classList.remove('drag-over');
                    if (dragOverElement === this) dragOverElement = null;
                });
                
                item.addEventListener('drop', function(e) {
                    e.preventDefault();
                    this.classList.remove('drag-over');
                    if (dragged && dragged !== this) {
                        const itemsArray = Array.from(list.children);
                        const fromIdx = itemsArray.indexOf(dragged);
                        const toIdx = itemsArray.indexOf(this);
                        if (fromIdx < toIdx) {
                            list.insertBefore(dragged, this.nextSibling);
                        } else {
                            list.insertBefore(dragged, this);
                        }
                        updateHidden();
                    }
                    if (dragOverElement) {
                        dragOverElement.classList.remove('drag-over');
                        dragOverElement = null;
                    }
                });
            });
        });
    }

    // ============================================================
    // AJOUTER DU CSS POUR LE DRAG & DROP
    // ============================================================
    function addDragDropStyles() {
        if (!document.querySelector('#dragDropStyles')) {
            const style = document.createElement('style');
            style.id = 'dragDropStyles';
            style.textContent = `
                .sortable-item {
                    cursor: grab;
                    user-select: none;
                }
                .sortable-item:active {
                    cursor: grabbing;
                }
                .sortable-item.dragging {
                    opacity: 0.4;
                    cursor: grabbing;
                }
                .sortable-item.drag-over {
                    border: 2px dashed #0077B6;
                    background: #e8f4fd;
                }
                .sortable-handle {
                    cursor: grab;
                }
                .fade-in {
                    animation: fadeIn 0.5s ease forwards;
                }
                @keyframes fadeIn {
                    from { opacity: 0; transform: translateY(10px); }
                    to { opacity: 1; transform: translateY(0); }
                }
            `;
            document.head.appendChild(style);
        }
    }

    // ============================================================
    // AFFICHER LE SCORE PRÉCÉDENT
    // ============================================================
    function initPreviousScore() {
        const scoreContainer = document.querySelector('.previous-score');
        if (scoreContainer && scoreContainer.dataset.score) {
            const score = parseInt(scoreContainer.dataset.score);
            if (score > 0) {
                const message = document.createElement('div');
                message.className = 'alert alert-info';
                message.style.marginBottom = '1rem';
                message.innerHTML = `<i class="fas fa-history"></i> Votre dernier score : <strong>${score}%</strong>`;
                const testHeader = document.querySelector('.test-header');
                if (testHeader) {
                    testHeader.insertAdjacentElement('afterend', message);
                }
            }
        }
    }

    // ============================================================
    // COMPTEUR DE QUESTIONS
    // ============================================================
    function initQuestionCounter() {
        const questions = document.querySelectorAll('.question-card');
        const counterContainer = document.querySelector('.question-counter');
        if (!counterContainer || !questions.length) return;
        
        function updateCounter() {
            const answered = Array.from(questions).filter(q => {
                const radios = q.querySelectorAll('input[type="radio"]:checked');
                const checkboxes = q.querySelectorAll('input[type="checkbox"]:checked');
                const textInputs = q.querySelectorAll('.input-texte-trous');
                const textAnswered = Array.from(textInputs).some(input => input.value.trim() !== '');
                return radios.length > 0 || checkboxes.length > 0 || textAnswered;
            }).length;
            
            counterContainer.textContent = `${answered}/${questions.length} répondues`;
        }
        
        // Écouter les changements sur tous les inputs
        questions.forEach(q => {
            const inputs = q.querySelectorAll('input');
            inputs.forEach(input => {
                input.addEventListener('change', updateCounter);
                input.addEventListener('keyup', updateCounter);
            });
        });
        
        updateCounter();
    }

    // ============================================================
    // HELPER : Récupérer le token CSRF
    // ============================================================
    function getCSRFToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        if (cookieValue) return cookieValue;
        
        const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
        return csrfInput ? csrfInput.value : '';
    }

    // ============================================================
    // INITIALISATION
    // ============================================================
    function init() {
        initTerminerCours();
        initTestSubmission();
        initDragAndDrop();
        addDragDropStyles();
        initPreviousScore();
        initQuestionCounter();
    }

    ready(init);

})();
