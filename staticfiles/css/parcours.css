/* ============================================================
   PARCOURS - Styles pour les modules de cours et tests
   Ventoryx Academy
   Manifeste : design froid, épuré, autorité institutionnelle
   Version corrigée avec mode sombre et harmonisation des couleurs
   ============================================================ */

:root {
    /* Couleurs principales */
    --parcours-primary: #0F1C2E;
    --parcours-primary-light: #1E3A5F;
    --parcours-accent: #3B82F6;
    --parcours-accent-dark: #2563EB;
    --parcours-accent-light: #60A5FA;
    
    /* États */
    --parcours-success: #10b981;
    --parcours-warning: #f59e0b;
    --parcours-danger: #ef4444;
    --parcours-gold: #D4AF37;
    --parcours-locked: #ADB5BD;
    
    /* Surfaces */
    --parcours-bg: #F8FAFE;
    --parcours-card: #FFFFFF;
    --parcours-border: #E9ECEF;
    --parcours-text: #212529;
    --parcours-text-light: #6C757D;
    
    /* Ombres */
    --parcours-shadow: 0 10px 30px rgba(0,0,0,0.08);
    --parcours-shadow-hover: 0 15px 40px rgba(0,0,0,0.15);
    
    /* Transition */
    --parcours-transition: all 0.3s cubic-bezier(0.2, 0.9, 0.4, 1.1);
    
    /* Bordures */
    --parcours-radius: 16px;
    --parcours-radius-sm: 12px;
}

/* ============ MODE SOMBRE ============ */
body.dark-mode {
    --parcours-bg: #121212;
    --parcours-card: #1E1E1E;
    --parcours-border: #2C2C2C;
    --parcours-text: #E0E0E0;
    --parcours-text-light: #ADB5BD;
    --parcours-shadow: 0 10px 30px rgba(0,0,0,0.2);
    --parcours-shadow-hover: 0 15px 40px rgba(0,0,0,0.3);
}

/* ============ SÉLECTION MÉTIER ============ */
.selection-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 3rem 2rem;
}
.selection-header {
    text-align: center;
    margin-bottom: 4rem;
}
.selection-header h1 {
    font-family: 'Montserrat', sans-serif;
    font-size: 2.2rem;
    color: var(--parcours-primary);
    margin-bottom: 1rem;
}
.selection-header p {
    color: var(--parcours-text-light);
    font-size: 1.1rem;
    max-width: 600px;
    margin: 0 auto;
}
.metiers-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
}
.metier-card {
    background: var(--parcours-card);
    border-radius: var(--parcours-radius);
    padding: 2.5rem 2rem;
    text-align: center;
    box-shadow: var(--parcours-shadow);
    transition: var(--parcours-transition);
    cursor: pointer;
    text-decoration: none;
    color: var(--parcours-text);
    border-top: 4px solid var(--parcours-accent);
    display: block;
}
.metier-card:hover {
    transform: translateY(-8px);
    box-shadow: var(--parcours-shadow-hover);
}
.metier-icon {
    width: 80px;
    height: 80px;
    margin: 0 auto 1.5rem;
    background: linear-gradient(135deg, var(--parcours-accent), var(--parcours-primary));
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 2rem;
    transition: transform 0.3s;
}
.metier-card:hover .metier-icon {
    transform: scale(1.05);
}
.metier-card h3 {
    font-family: 'Montserrat', sans-serif;
    font-size: 1.3rem;
    margin-bottom: 0.5rem;
}
.metier-card p {
    color: var(--parcours-text-light);
    font-size: 0.9rem;
    margin-bottom: 1rem;
}
.metier-stats {
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    font-size: 0.8rem;
    color: var(--parcours-text-light);
}
.metier-stats span {
    display: flex;
    align-items: center;
    gap: 0.3rem;
}
.badge-gratuit, .badge-premium {
    display: inline-block;
    padding: 0.2rem 0.8rem;
    border-radius: 50px;
    font-size: 0.7rem;
    font-weight: 700;
    margin-bottom: 0.8rem;
}
.badge-gratuit { background: var(--parcours-success); color: white; }
.badge-premium { background: var(--parcours-gold); color: var(--parcours-primary); }

/* ============ ACCUEIL PARCOURS (Hub) ============ */
.parcours-container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 3rem 2rem;
}
.parcours-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
    margin-bottom: 2rem;
}
.parcours-header h1 {
    font-family: 'Montserrat', sans-serif;
    font-size: 2rem;
    color: var(--parcours-primary);
}
.btn-retour {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.6rem 1.2rem;
    border-radius: 40px;
    text-decoration: none;
    color: var(--parcours-text-light);
    border: 1px solid var(--parcours-border);
    transition: var(--parcours-transition);
    font-size: 0.9rem;
}
.btn-retour:hover {
    background: var(--parcours-border);
    color: var(--parcours-primary);
}
.progression-globale {
    background: var(--parcours-card);
    border-radius: var(--parcours-radius);
    padding: 1.5rem;
    margin-bottom: 2rem;
    box-shadow: var(--parcours-shadow);
    display: flex;
    align-items: center;
    gap: 1.5rem;
    flex-wrap: wrap;
}
.progression-barre {
    flex: 1;
    min-width: 200px;
    height: 12px;
    background: var(--parcours-border);
    border-radius: 6px;
    overflow: hidden;
}
.progression-remplissage {
    height: 100%;
    background: linear-gradient(90deg, var(--parcours-accent), var(--parcours-success));
    border-radius: 6px;
    transition: width 0.5s ease;
}
.modules-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
}
.module-card {
    background: var(--parcours-card);
    border-radius: var(--parcours-radius);
    padding: 2rem 1.5rem;
    text-align: center;
    box-shadow: var(--parcours-shadow);
    transition: var(--parcours-transition);
    text-decoration: none;
    color: var(--parcours-text);
    position: relative;
    display: block;
}
.module-card:hover {
    transform: translateY(-5px);
    box-shadow: var(--parcours-shadow-hover);
}
.module-card.locked {
    opacity: 0.5;
    cursor: not-allowed;
    pointer-events: none;
}
.module-card.completed {
    border: 2px solid var(--parcours-success);
}
.module-card .module-numero {
    width: 50px;
    height: 50px;
    margin: 0 auto 1rem;
    background: var(--parcours-primary);
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 1.2rem;
}
.module-card.completed .module-numero {
    background: var(--parcours-success);
}
.module-card.locked .module-numero {
    background: var(--parcours-locked);
}
.module-card h3 {
    font-family: 'Montserrat', sans-serif;
    font-size: 1rem;
    margin-bottom: 0.5rem;
}
.lock-icon {
    position: absolute;
    top: 1rem;
    right: 1rem;
    color: var(--parcours-locked);
    font-size: 1.2rem;
}
.module-mini-progression {
    height: 6px;
    background: var(--parcours-border);
    border-radius: 3px;
    margin-top: 1rem;
    overflow: hidden;
}
.module-mini-remplissage {
    height: 100%;
    background: var(--parcours-accent);
    border-radius: 3px;
    transition: width 0.3s ease;
}
.module-progress-text {
    font-size: 0.75rem;
    color: var(--parcours-text-light);
    margin-top: 0.3rem;
    display: block;
}
.test-global-card {
    background: linear-gradient(135deg, var(--parcours-primary), var(--parcours-primary-light));
    color: white;
    border-radius: var(--parcours-radius);
    padding: 2rem;
    text-align: center;
    box-shadow: var(--parcours-shadow);
    text-decoration: none;
    display: block;
    transition: var(--parcours-transition);
}
.test-global-card:hover {
    transform: translateY(-5px);
    box-shadow: var(--parcours-shadow-hover);
}
.test-global-card.locked {
    opacity: 0.5;
    pointer-events: none;
}
.test-global-card h3 {
    font-family: 'Montserrat', sans-serif;
    margin-bottom: 0.5rem;
    color: white;
}
.test-global-card p {
    color: rgba(255,255,255,0.8);
}
.btn-start {
    display: inline-block;
    padding: 0.7rem 2rem;
    background: var(--parcours-gold);
    color: var(--parcours-primary);
    border-radius: 50px;
    text-decoration: none;
    font-weight: 600;
    transition: var(--parcours-transition);
    margin-top: 0.5rem;
}
.btn-start:hover {
    background: #c9a030;
    transform: translateY(-2px);
}

/* ============ DERNIER COURS CONSULTÉ ============ */
.last-course-card {
    background: linear-gradient(135deg, var(--parcours-accent), var(--parcours-accent-dark));
    color: white;
    border-radius: var(--parcours-radius);
    padding: 1rem 1.5rem;
    margin-bottom: 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
}
.last-course-btn {
    background: white;
    color: var(--parcours-accent);
    padding: 0.5rem 1rem;
    border-radius: 50px;
    text-decoration: none;
    font-weight: 600;
    transition: transform 0.3s;
}
.last-course-btn:hover {
    transform: translateX(3px);
}

/* ============ COURS ============ */
.cours-container {
    max-width: 900px;
    margin: 0 auto;
    padding: 2rem;
}
.cours-navigation {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;
    flex-wrap: wrap;
    gap: 0.5rem;
}
.cours-breadcrumb {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: var(--parcours-text-light);
    font-size: 0.85rem;
    flex-wrap: wrap;
}
.cours-breadcrumb a {
    color: var(--parcours-accent);
    text-decoration: none;
}
.cours-breadcrumb a:hover {
    text-decoration: underline;
}
.cours-contenu {
    background: var(--parcours-card);
    border-radius: var(--parcours-radius);
    padding: 3rem 2rem;
    box-shadow: var(--parcours-shadow);
    margin-bottom: 2rem;
    min-height: 400px;
    transition: transform 0.3s;
}
.cours-contenu:hover {
    transform: translateY(-3px);
}
.cours-contenu h1 {
    font-family: 'Montserrat', sans-serif;
    font-size: 1.8rem;
    color: var(--parcours-primary);
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 2px solid var(--parcours-border);
}
.cours-contenu h2 {
    font-family: 'Montserrat', sans-serif;
    font-size: 1.3rem;
    color: var(--parcours-primary);
    margin: 2rem 0 1rem;
}
.cours-contenu p {
    margin-bottom: 1rem;
    line-height: 1.8;
    color: var(--parcours-text);
}
.cours-contenu ul, .cours-contenu ol {
    margin-bottom: 1.5rem;
    padding-left: 1.5rem;
}
.cours-contenu li {
    margin-bottom: 0.5rem;
    line-height: 1.7;
}
.cours-meta {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
    font-size: 0.8rem;
    color: var(--parcours-text-light);
}
.btn-cours {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.8rem 1.8rem;
    border-radius: 50px;
    font-weight: 600;
    text-decoration: none;
    transition: var(--parcours-transition);
    cursor: pointer;
    border: none;
    font-size: 0.95rem;
    font-family: 'Montserrat', sans-serif;
}
.btn-precedent {
    background: transparent;
    border: 2px solid var(--parcours-border);
    color: var(--parcours-text-light);
}
.btn-precedent:hover {
    border-color: var(--parcours-accent);
    color: var(--parcours-accent);
    transform: translateX(-3px);
}
.btn-suivant {
    background: var(--parcours-accent);
    color: white;
}
.btn-suivant:hover {
    background: var(--parcours-accent-dark);
    transform: translateX(3px);
}
.btn-terminer {
    background: var(--parcours-success);
    color: white;
}
.btn-terminer:hover {
    background: #059669;
    transform: translateY(-2px);
}
.btn-ia {
    background: linear-gradient(135deg, var(--parcours-primary), var(--parcours-primary-light));
    color: white;
}
.btn-ia:hover {
    transform: scale(1.02);
}
.cours-compteur {
    font-size: 0.85rem;
    color: var(--parcours-text-light);
}
.cours-actions {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
}

/* ============ TEST ============ */
.test-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
}
.test-header {
    background: linear-gradient(135deg, var(--parcours-primary), var(--parcours-primary-light));
    color: white;
    border-radius: var(--parcours-radius);
    padding: 2rem;
    margin-bottom: 2rem;
    text-align: center;
}
.test-header h1 {
    font-family: 'Montserrat', sans-serif;
    font-size: 1.8rem;
    color: white;
}
.test-info {
    display: flex;
    justify-content: center;
    gap: 1.5rem;
    flex-wrap: wrap;
    font-size: 0.9rem;
    opacity: 0.9;
}
.test-info span {
    display: flex;
    align-items: center;
    gap: 0.4rem;
}
.test-progress {
    background: var(--parcours-card);
    border-radius: var(--parcours-radius-sm);
    padding: 1rem;
    margin-bottom: 1.5rem;
    box-shadow: var(--parcours-shadow);
}
.progress-stats {
    display: flex;
    justify-content: space-between;
    font-size: 0.8rem;
    margin-bottom: 0.5rem;
}
.timer {
    background: var(--parcours-card);
    border-radius: var(--parcours-radius-sm);
    padding: 0.8rem 1.5rem;
    margin-bottom: 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 1rem;
}
.timer-warning {
    color: var(--parcours-danger);
    animation: pulse 1s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.6; }
}
.question-card {
    background: var(--parcours-card);
    border-radius: var(--parcours-radius);
    padding: 2rem;
    margin-bottom: 1.5rem;
    box-shadow: var(--parcours-shadow);
    transition: transform 0.3s;
}
.question-card:hover {
    transform: translateY(-2px);
}
.question-numero {
    font-family: 'Montserrat', sans-serif;
    font-size: 0.8rem;
    color: var(--parcours-accent);
    font-weight: 700;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.8rem;
    flex-wrap: wrap;
}
.question-type-badge {
    display: inline-block;
    padding: 0.15rem 0.6rem;
    border-radius: 10px;
    font-size: 0.7rem;
    font-weight: 700;
}
.badge-multiple { background: #fef3c7; color: #92400e; }
.badge-texte { background: #ede9fe; color: #5b21b6; }
.badge-ordre { background: #fce7f3; color: #9d174d; }

.question-texte {
    font-size: 1.05rem;
    color: var(--parcours-primary);
    font-weight: 600;
    margin-bottom: 1.5rem;
}
.reponses-liste {
    list-style: none;
}
.reponse-item {
    margin-bottom: 0.6rem;
}
.reponse-item label {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    padding: 0.8rem 1rem;
    border: 1px solid var(--parcours-border);
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.2s ease;
}
.reponse-item label:hover {
    background: var(--parcours-bg);
    border-color: var(--parcours-accent);
}
.reponse-item input[type="radio"], 
.reponse-item input[type="checkbox"] {
    width: 18px;
    height: 18px;
    accent-color: var(--parcours-accent);
    flex-shrink: 0;
}
.reponse-item span {
    color: var(--parcours-text);
}
.input-texte-trous {
    width: 100%;
    padding: 0.8rem 1rem;
    border: 1px solid var(--parcours-border);
    border-radius: 10px;
    font-size: 1rem;
    font-family: 'Open Sans', sans-serif;
    background: var(--parcours-card);
    color: var(--parcours-text);
}
.input-texte-trous:focus {
    outline: none;
    border-color: var(--parcours-accent);
}
.sortable-list {
    list-style: none;
}
.sortable-item {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    padding: 0.8rem 1rem;
    background: var(--parcours-bg);
    border: 1px solid var(--parcours-border);
    border-radius: 10px;
    margin-bottom: 0.5rem;
    cursor: grab;
    user-select: none;
    transition: background 0.2s;
}
.sortable-item:active {
    cursor: grabbing;
}
.sortable-handle {
    color: var(--parcours-locked);
    font-size: 1.2rem;
    cursor: grab;
}
.sortable-item.dragging {
    opacity: 0.4;
}
.sortable-item.drag-over {
    border: 2px dashed var(--parcours-accent);
    background: rgba(59,130,246,0.05);
}
.btn-valider {
    width: 100%;
    padding: 0.9rem;
    background: var(--parcours-accent);
    color: white;
    border: none;
    border-radius: 50px;
    font-weight: 700;
    font-size: 1rem;
    cursor: pointer;
    font-family: 'Montserrat', sans-serif;
    transition: var(--parcours-transition);
    margin-top: 1rem;
}
.btn-valider:hover {
    background: var(--parcours-accent-dark);
    transform: translateY(-2px);
}
.btn-valider:disabled {
    background: var(--parcours-locked);
    cursor: not-allowed;
    transform: none;
}
.loading-spinner {
    display: inline-block;
    width: 20px;
    height: 20px;
    border: 2px solid var(--parcours-border);
    border-top-color: var(--parcours-accent);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    margin-right: 0.5rem;
}
@keyframes spin {
    to { transform: rotate(360deg); }
}
.resultat-box {
    background: var(--parcours-card);
    border-radius: var(--parcours-radius);
    padding: 2.5rem;
    text-align: center;
    box-shadow: var(--parcours-shadow);
    animation: fadeIn 0.5s ease;
}
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
.resultat-box.reussi {
    border: 2px solid var(--parcours-success);
}
.resultat-box.echec {
    border: 2px solid var(--parcours-danger);
}
.resultat-score {
    font-size: 3rem;
    font-weight: 800;
    font-family: 'Montserrat', sans-serif;
    margin: 1rem 0;
}
.resultat-box.reussi .resultat-score {
    color: var(--parcours-success);
}
.resultat-box.echec .resultat-score {
    color: var(--parcours-danger);
}
.certificat-preview {
    background: var(--parcours-bg);
    border-radius: var(--parcours-radius-sm);
    padding: 1rem;
    margin-top: 1rem;
}

/* ============ TEST GLOBAL ============ */
.modules-summary {
    display: flex;
    justify-content: center;
    gap: 0.8rem;
    flex-wrap: wrap;
    margin-top: 1rem;
}
.module-badge {
    background: rgba(255,255,255,0.2);
    padding: 0.3rem 0.8rem;
    border-radius: 50px;
    font-size: 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}

/* ============ RESPONSIVE ============ */
@media (max-width: 768px) {
    .selection-header h1,
    .parcours-header h1 {
        font-size: 1.5rem;
    }
    .cours-contenu {
        padding: 1.5rem;
    }
    .cours-contenu h1 {
        font-size: 1.4rem;
    }
    .modules-grid {
        grid-template-columns: 1fr;
    }
    .metiers-grid {
        grid-template-columns: 1fr;
    }
    .cours-actions {
        flex-direction: column;
        align-items: stretch;
    }
    .btn-cours {
        text-align: center;
        justify-content: center;
    }
    .test-info {
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
    }
    .test-header h1 {
        font-size: 1.4rem;
    }
    .progression-globale {
        flex-direction: column;
        text-align: center;
    }
    .last-course-card {
        flex-direction: column;
        text-align: center;
    }
}

/* ============ ANIMATIONS ============ */
@keyframes slideIn {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.fade-in {
    animation: fadeInUp 0.5s ease forwards;
}
