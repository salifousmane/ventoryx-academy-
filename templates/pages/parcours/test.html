{% extends "base.html" %}
{% load static %}

{% block title %}Test {{ test.numero }} — {{ site_name }}{% endblock %}

{% block meta_description %}
Test de validation du module {{ module.numero }} — {{ parcours.nom }}. Évaluez vos connaissances en aéronautique.
{% endblock %}

{% block extra_css %}
<style>
    :root {
        --primary: #3B82F6;
        --primary-dark: #2563EB;
        --secondary: #0F1C2E;
        --secondary-light: #1E3A5F;
        --gray: #6C757D;
        --gray-light: #E9ECEF;
        --bg-light: #F8FAFE;
        --white: #ffffff;
        --success: #10b981;
        --danger: #ef4444;
        --warning: #f59e0b;
    }

    .test-container { 
        max-width: 800px; 
        margin: 0 auto; 
        padding: 2rem; 
        animation: fadeIn 0.5s ease-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .test-header {
        background: linear-gradient(135deg, var(--secondary), var(--secondary-light));
        color: white;
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
        text-align: center;
    }
    .test-header h1 { font-family: 'Montserrat', sans-serif; font-size: 1.8rem; color: white; }
    .test-header .breadcrumb { font-size: 0.85rem; opacity: 0.8; margin-bottom: 1rem; }
    .test-header .breadcrumb a { color: rgba(255,255,255,0.7); text-decoration: none; }
    .test-info { display: flex; justify-content: center; gap: 1.5rem; flex-wrap: wrap; font-size: 0.9rem; opacity: 0.9; }
    .test-info span { display: flex; align-items: center; gap: 0.4rem; }

    /* Barre de progression du test */
    .test-progress {
        background: var(--white);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }
    .progress-stats {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
        font-size: 0.85rem;
    }
    .progress-stats span:first-child { font-weight: 600; color: var(--secondary); }
    .progress-stats span:last-child { color: var(--primary); font-weight: 700; }
    .progress-bar {
        background: var(--gray-light);
        border-radius: 10px;
        height: 8px;
        overflow: hidden;
    }
    .progress-fill {
        height: 100%;
        border-radius: 10px;
        background: linear-gradient(90deg, var(--primary), var(--success));
        transition: width 0.5s ease;
    }

    /* Timer */
    .timer {
        background: var(--white);
        border-radius: 12px;
        padding: 0.8rem 1.5rem;
        margin-bottom: 1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }
    .timer-label {
        font-weight: 600;
        color: var(--secondary);
    }
    .timer-value {
        font-size: 1.5rem;
        font-weight: 800;
        font-family: monospace;
        color: var(--primary);
    }
    .timer-warning {
        color: var(--danger);
        animation: pulse 1s infinite;
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }

    .question-card {
        background: var(--white);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.06);
        margin-bottom: 1.5rem;
        transition: transform 0.3s;
    }
    .question-card:hover {
        transform: translateY(-2px);
    }
    .question-numero {
        font-family: 'Montserrat', sans-serif;
        font-size: 0.8rem;
        color: var(--primary);
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
        color: var(--secondary);
        font-weight: 600;
        margin-bottom: 1.5rem;
    }

    /* Spinner de chargement */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 2px solid var(--gray-light);
        border-top-color: var(--primary);
        border-radius: 50%;
        animation: spin 0.8s linear infinite;
        margin-right: 0.5rem;
    }
    @keyframes spin {
        to { transform: rotate(360deg); }
    }

    .btn-valider {
        width: 100%;
        padding: 0.9rem;
        background: var(--primary);
        color: white;
        border: none;
        border-radius: 50px;
        font-weight: 700;
        font-size: 1rem;
        cursor: pointer;
        font-family: 'Montserrat', sans-serif;
        transition: all 0.3s cubic-bezier(0.2, 0.9, 0.4, 1.1);
        margin-top: 1rem;
    }
    .btn-valider:hover {
        background: var(--primary-dark);
        transform: translateY(-2px);
    }
    .btn-valider:disabled {
        background: var(--gray);
        cursor: not-allowed;
        transform: none;
    }

    .resultat-box {
        background: var(--white);
        border-radius: 16px;
        padding: 2.5rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.06);
        animation: fadeIn 0.5s ease-out;
    }
    .resultat-box.reussi { border: 2px solid var(--success); }
    .resultat-box.echec { border: 2px solid var(--danger); }
    .resultat-score {
        font-size: 3rem;
        font-weight: 800;
        font-family: 'Montserrat', sans-serif;
        margin: 1rem 0;
    }
    .resultat-box.reussi .resultat-score { color: var(--success); }
    .resultat-box.echec .resultat-score { color: var(--danger); }

    /* Assistant IA */
    .ia-context {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 1000;
    }
    .ia-toggle {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: linear-gradient(135deg, var(--primary), var(--primary-dark));
        color: white;
        border: none;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        transition: transform 0.3s;
    }
    .ia-toggle:hover { transform: scale(1.1); }
    .ia-panel {
        display: none;
        position: absolute;
        bottom: 60px;
        right: 0;
        width: 320px;
        background: var(--white);
        border-radius: 16px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        overflow: hidden;
    }
    .ia-panel.open { display: block; }

    /* Dark mode */
    body.dark-mode .question-card,
    body.dark-mode .test-progress,
    body.dark-mode .timer,
    body.dark-mode .resultat-box {
        background: #1E1E1E;
    }
    body.dark-mode .progress-stats span:first-child,
    body.dark-mode .timer-label,
    body.dark-mode .question-texte {
        color: #E0E0E0;
    }

    @media (max-width: 768px) {
        .test-container { padding: 1rem; }
        .test-header h1 { font-size: 1.4rem; }
        .question-card { padding: 1.5rem; }
        .timer-value { font-size: 1.2rem; }
    }
</style>
{% endblock %}

{% block content %}

<div class="test-container">
    <div class="test-header">
        <div class="breadcrumb">
            <a href="{% url 'parcours:selection_metier' %}">Parcours</a> ›
            <a href="{% url 'parcours:accueil_parcours' metier=metier %}">{{ parcours.nom }}</a> ›
            Module {{ module.numero }}
        </div>
        <h1>{{ test.titre }}</h1>
        <div class="test-info">
            <span><i class="fas fa-question-circle"></i> {{ questions|length }} questions</span>
            <span><i class="fas fa-clock"></i> {{ test.duree_estimee|default:15 }} min</span>
            <span><i class="fas fa-check-circle"></i> Minimum {{ test.score_minimum|default:70 }}%</span>
            {% if deja_reussi %}
            <span style="color: var(--success);"><i class="fas fa-check-circle"></i> Déjà réussi</span>
            {% endif %}
        </div>
    </div>

    <!-- Barre de progression du test -->
    <div class="test-progress" id="testProgress">
        <div class="progress-stats">
            <span>Progression du test</span>
            <span id="questionsProgress">0/{{ questions|length }} répondues</span>
        </div>
        <div class="progress-bar">
            <div class="progress-fill" id="progressFill" style="width: 0%;"></div>
        </div>
    </div>

    <!-- Timer -->
    {% if test.duree_estimee %}
    <div class="timer" id="timerContainer">
        <span class="timer-label"><i class="fas fa-hourglass-half"></i> Temps restant</span>
        <span class="timer-value" id="timerValue">{{ test.duree_estimee }}:00</span>
    </div>
    {% endif %}

    {% if deja_reussi %}
    <div class="resultat-box reussi">
        <i class="fas fa-check-circle" style="font-size:3rem;color:var(--success);"></i>
        <p style="margin-top:1rem;">Vous avez déjà validé ce test avec un score de <strong>{{ derniere_progression.score }}%</strong>.</p>
        <a href="{% url 'parcours:accueil_parcours' metier=metier %}" style="display:inline-block;margin-top:1rem;padding:0.7rem 2rem;background:var(--primary);color:white;border-radius:50px;text-decoration:none;font-weight:600;">
            Retour aux modules
        </a>
    </div>
    {% else %}
    <div id="resultat" style="display:none;"></div>
    <form id="testForm">
        {% csrf_token %}
        {% for question in questions %}
        <div class="question-card" data-question-index="{{ forloop.counter0 }}">
            <div class="question-numero">
                Question {{ forloop.counter }}/{{ questions|length }}
                {% if question.type == 'qcm_multiple' %}
                <span class="question-type-badge badge-multiple">Plusieurs réponses</span>
                {% elif question.type == 'texte_trous' %}
                <span class="question-type-badge badge-texte">Réponse libre</span>
                {% elif question.type == 'reorganisation' %}
                <span class="question-type-badge badge-ordre">Remise en ordre</span>
                {% endif %}
            </div>
            <div class="question-texte">{{ question.texte }}</div>

            {% if question.type == 'texte_trous' %}
            <input type="text" name="question_{{ forloop.counter0 }}" class="input-texte-trous" placeholder="Votre réponse..." autocomplete="off">

            {% elif question.type == 'reorganisation' %}
            <ul class="sortable-list" data-question="{{ forloop.counter0 }}">
                {% for reponse in question.reponses.all %}
                <li class="sortable-item" draggable="true" data-id="{{ reponse.id }}">
                    <span class="sortable-handle"><i class="fas fa-grip-vertical"></i></span>
                    <span>{{ reponse.texte }}</span>
                </li>
                {% endfor %}
            </ul>
            <input type="hidden" name="question_{{ forloop.counter0 }}" class="ordre-hidden">

            {% elif question.type == 'qcm_multiple' %}
            <ul class="reponses-liste">
                {% for reponse in question.reponses.all %}
                <li class="reponse-item">
                    <label>
                        <input type="checkbox" name="question_{{ forloop.parentloop.counter0 }}" value="{{ reponse.id }}">
                        <span>{{ reponse.texte }}</span>
                    </label>
                </li>
                {% endfor %}
            </ul>

            {% else %}
            <ul class="reponses-liste">
                {% for reponse in question.reponses.all %}
                <li class="reponse-item">
                    <label>
                        <input type="radio" name="question_{{ forloop.parentloop.counter0 }}" value="{{ reponse.id }}">
                        <span>{{ reponse.texte }}</span>
                    </label>
                </li>
                {% endfor %}
            </ul>
            {% endif %}
        </div>
        {% empty %}
        <p style="text-align:center;color:var(--gray);">Aucune question pour ce test.</p>
        {% endfor %}

        {% if questions %}
        <button type="submit" class="btn-valider" id="submitBtn"><i class="fas fa-paper-plane"></i> Valider mes réponses</button>
        {% endif %}
    </form>
    {% endif %}
</div>

<!-- Assistant IA contextuel -->
<div class="ia-context">
    <button class="ia-toggle" onclick="toggleIaPanel()">
        <i class="fas fa-robot"></i>
    </button>
    <div class="ia-panel" id="iaPanel">
        <div style="background: var(--primary); color: white; padding: 0.8rem; display: flex; justify-content: space-between;">
            <strong><i class="fas fa-robot"></i> Assistant IA</strong>
            <button onclick="toggleIaPanel()" style="background: none; border: none; color: white;">✕</button>
        </div>
        <div style="padding: 0.8rem; max-height: 300px; overflow-y: auto;" id="iaMessages">
            <div style="background: var(--bg-light); padding: 0.5rem; border-radius: 12px; margin-bottom: 0.5rem;">
                👋 Besoin d'aide pour ce test ? Posez votre question sur le sujet !
            </div>
        </div>
        <div style="padding: 0.8rem; border-top: 1px solid var(--gray-light); display: flex; gap: 0.5rem;">
            <input type="text" id="iaInput" placeholder="Posez votre question..." style="flex: 1; padding: 0.5rem; border-radius: 20px; border: 1px solid var(--gray-light);">
            <button onclick="sendIaQuestion()" style="background: var(--primary); color: white; border: none; padding: 0.5rem 1rem; border-radius: 20px;">Envoyer</button>
        </div>
    </div>
</div>

{% endblock %}

{% block extra_js %}
<script>
    // ============ COMPTEUR DE PROGRESSION ============
    function updateProgress() {
        const total = {{ questions|length }};
        let answered = 0;
        
        {% for question in questions %}
            {% if question.type == 'texte_trous' %}
            if (document.querySelector('[name="question_{{ forloop.counter0 }}"]')?.value.trim()) answered++;
            {% elif question.type == 'reorganisation' %}
            if (document.querySelector('[name="question_{{ forloop.counter0 }}"]')?.value) answered++;
            {% else %}
            if (document.querySelectorAll('[name="question_{{ forloop.counter0 }}"]:checked').length > 0) answered++;
            {% endif %}
        {% endfor %}
        
        document.getElementById('questionsProgress').innerText = `${answered}/${total} répondues`;
        const percent = (answered / total) * 100;
        document.getElementById('progressFill').style.width = `${percent}%`;
    }
    
    // Écouter les changements sur tous les champs
    document.querySelectorAll('input, select, textarea').forEach(el => {
        el.addEventListener('change', updateProgress);
        el.addEventListener('input', updateProgress);
    });
    updateProgress();

    // ============ TIMER ============
    {% if test.duree_estimee and not deja_reussi %}
    let timeLeft = {{ test.duree_estimee }} * 60;
    const timerElement = document.getElementById('timerValue');
    const timerInterval = setInterval(() => {
        if (timeLeft <= 0) {
            clearInterval(timerInterval);
            timerElement.innerHTML = "0:00";
            timerElement.classList.add('timer-warning');
            alert("⏰ Temps écoulé ! Vos réponses vont être soumises.");
            document.getElementById('testForm').dispatchEvent(new Event('submit'));
        } else {
            timeLeft--;
            const minutes = Math.floor(timeLeft / 60);
            const seconds = timeLeft % 60;
            timerElement.innerHTML = `${minutes}:${seconds.toString().padStart(2, '0')}`;
            if (timeLeft <= 60) {
                timerElement.classList.add('timer-warning');
            }
        }
    }, 1000);
    {% endif %}

    // ============ RÉORGANISATION (drag & drop) ============
    document.querySelectorAll('.sortable-list').forEach(list => {
        const hiddenInput = list.parentElement.querySelector('.ordre-hidden');
        function updateHidden() {
            hiddenInput.value = Array.from(list.querySelectorAll('.sortable-item')).map(item => item.dataset.id).join(',');
            updateProgress();
        }
        updateHidden();

        let dragged = null;
        list.querySelectorAll('.sortable-item').forEach(item => {
            item.addEventListener('dragstart', function(e) { dragged = this; this.classList.add('dragging'); });
            item.addEventListener('dragend', function(e) { this.classList.remove('dragging'); dragged = null; });
            item.addEventListener('dragover', function(e) { e.preventDefault(); });
            item.addEventListener('drop', function(e) {
                e.preventDefault();
                if (dragged && dragged !== this) {
                    const items = Array.from(list.children);
                    const fromIdx = items.indexOf(dragged);
                    const toIdx = items.indexOf(this);
                    list.insertBefore(dragged, fromIdx < toIdx ? this.nextSibling : this);
                    updateHidden();
                }
            });
        });
    });

    // ============ SOUMISSION DU TEST ============
    document.getElementById('testForm')?.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Mise à jour des ordres
        document.querySelectorAll('.sortable-list').forEach(list => {
            const hidden = list.parentElement.querySelector('.ordre-hidden');
            hidden.value = Array.from(list.querySelectorAll('.sortable-item')).map(item => item.dataset.id).join(',');
        });
        
        const submitBtn = document.getElementById('submitBtn');
        const originalText = submitBtn.innerHTML;
        submitBtn.innerHTML = '<span class="loading-spinner"></span> Vérification en cours...';
        submitBtn.disabled = true;
        
        const formData = new FormData(this);
        fetch(window.location.href, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: formData
        })
        .then(r => r.json())
        .then(data => {
            const div = document.getElementById('resultat');
            div.style.display = 'block';
            if (data.reussi) {
                div.className = 'resultat-box reussi';
                div.innerHTML = `<i class="fas fa-trophy" style="font-size:2.5rem;color:#D4AF37;"></i><h3>Félicitations !</h3><div class="resultat-score">${data.score}%</div><p>${data.bonnes_reponses}/${data.total} bonnes réponses</p><p style="color:var(--gray);">Score minimum : 70%</p><a href="{% url 'parcours:accueil_parcours' metier=metier %}" style="display:inline-block;margin-top:1rem;padding:0.7rem 2rem;background:var(--primary);color:white;border-radius:50px;text-decoration:none;font-weight:600;">Continuer le parcours</a>`;
                document.getElementById('testForm').style.display = 'none';
                document.querySelector('.test-progress').style.display = 'none';
                {% if test.duree_estimee %}
                clearInterval(timerInterval);
                {% endif %}
            } else {
                div.className = 'resultat-box echec';
                div.innerHTML = `<i class="fas fa-redo" style="font-size:2.5rem;color:var(--danger);"></i><h3>Score insuffisant</h3><div class="resultat-score">${data.score}%</div><p>${data.bonnes_reponses}/${data.total} bonnes réponses</p><p style="color:var(--gray);">Minimum requis : 70%</p><button onclick="location.reload()" style="margin-top:1rem;padding:0.7rem 2rem;background:var(--warning);color:white;border:none;border-radius:50px;font-weight:600;cursor:pointer;"><i class="fas fa-redo"></i> Réessayer</button>`;
            }
            document.getElementById('resultat').scrollIntoView({ behavior: 'smooth' });
        })
        .catch(() => {
            alert('Une erreur est survenue. Veuillez réessayer.');
            submitBtn.innerHTML = originalText;
            submitBtn.disabled = false;
        });
    });

    // ============ ASSISTANT IA ============
    function toggleIaPanel() {
        document.getElementById('iaPanel').classList.toggle('open');
    }

    function sendIaQuestion() {
        const input = document.getElementById('iaInput');
        const question = input.value.trim();
        if (!question) return;
        
        const messages = document.getElementById('iaMessages');
        messages.innerHTML += `<div style="background: var(--primary); color: white; padding: 0.5rem; border-radius: 12px; margin-bottom: 0.5rem; text-align: right;">${question}</div>`;
        messages.innerHTML += `<div style="background: var(--bg-light); padding: 0.5rem; border-radius: 12px; margin-bottom: 0.5rem;"><span class="loading-spinner" style="width:14px;height:14px;"></span> Réflexion...</div>`;
        input.value = '';
        messages.scrollTop = messages.scrollHeight;
        
        fetch('/api/chatbot/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: JSON.stringify({
                question: `À propos du test "${test.titre}" du module "${module.nom}", ${question}`,
                context: 'test'
            })
        }).then(r => r.json()).then(data => {
            const loading = messages.querySelector('.loading-spinner')?.parentElement;
            if (loading) loading.remove();
            messages.innerHTML += `<div style="background: var(--bg-light); padding: 0.5rem; border-radius: 12px; margin-bottom: 0.5rem;">🤖 ${data.reponse || 'Je recherche la réponse...'}</div>`;
            messages.scrollTop = messages.scrollHeight;
        }).catch(() => {
            const loading = messages.querySelector('.loading-spinner')?.parentElement;
            if (loading) loading.remove();
            messages.innerHTML += `<div style="background: #f8d7da; padding: 0.5rem; border-radius: 12px; margin-bottom: 0.5rem;">⚠️ Service indisponible. Réessayez plus tard.</div>`;
            messages.scrollTop = messages.scrollHeight;
        });
    }
</script>
{% endblock %}
