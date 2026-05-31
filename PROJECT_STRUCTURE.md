# Structure du Projet Ventoryx Academy

## 📋 Vue d'ensemble

```
ventoryx-academy/
│
├── 📄 Fichiers racine
│   ├── manage.py
│   ├── requirements.txt
│   ├── seed.py
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── .env.example
│   ├── .gitignore
│   ├── README.md
│   ├── .bandit
│   └── PROJECT_STRUCTURE.md
│
├── 🔧 Configuration Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   └── celery.py
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── deploy.yml
│       └── security-check.yml
│
├── 📦 Apps Django (Métier)
│   │
│   ├── core/
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   ├── admin.py
│   │   ├── tests.py
│   │   └── apps.py
│   │   └── services/
│   │       ├── chatbot.py        # GPT-4o Assistant
│   │       ├── translator.py     # 15 langues
│   │       └── tts.py            # Text-to-Speech
│   │
│   ├── users/
│   │   ├── migrations/
│   │   ├── models.py             # User, Subscription, RBAC
│   │   ├── views.py              # Auth, Profile, Settings
│   │   ├── urls.py
│   │   ├── forms.py              # Login, Register, OTP
│   │   ├── admin.py
│   │   ├── tests.py
│   │   └── apps.py
│   │   └── services/
│   │       ├── auth.py           # MFA, OTP, 2FA
│   │       ├── stripe_service.py # Paiements Stripe
│   │       └── rbac.py           # Gestion rôles
│   │
│   ├── parcours/
│   │   ├── migrations/
│   │   ├── models.py             # Module, Cours, Test, Progression
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   ├── admin.py
│   │   ├── tests.py
│   │   └── apps.py
│   │   └── services/
│   │       ├── progress.py       # Suivi progression
│   │       ├── certification.py  # Certificats SHA-256
│   │       └── tests.py          # Gestion tests
│   │
│   ├── blog/
│   │   ├── migrations/
│   │   ├── models.py             # Article, Catégorie
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── tests.py
│   │   └── apps.py
│   │
│   ├── institution/
│   │   ├── migrations/
│   │   ├── models.py             # Département, Job, Certificat
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   ├── admin.py
│   │   ├── tests.py
│   │   └── apps.py
│   │   └── services/
│   │       ├── recruitment.py    # Recrutement
│   │       ├── certificates.py   # Gestion certificats
│   │       └── departments.py    # Gestion départements
│   │
│   ├── messaging/
│   │   ├── migrations/
│   │   ├── models.py             # Message, Notification, Newsletter
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── tests.py
│   │   └── apps.py
│   │   └── services/
│   │       ├── email.py          # Envoi emails
│   │       └── notifications.py  # Gestion notifications
│   │
│   ├── audit/
│   │   ├── migrations/
│   │   ├── models.py             # AuditLog (immutable)
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── tests.py
│   │   └── apps.py
│   │   └── services/
│   │       └── logger.py         # Journal d'audit
│   │
│   ├── forum/
│   │   ├── migrations/
│   │   ├── models.py             # Forum, Sujet, Réponse
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── forms.py
│   │   ├── admin.py
│   │   ├── tests.py
│   │   └── apps.py
│   │
│   └── gestion/
│       ├── migrations/
│       ├── models.py             # Tâches, Campagnes, Tickets
│       ├── views.py
│       ├── urls.py
│       ├── forms.py
│       ├── admin.py
│       ├── tests.py
│       └── apps.py
│       └── services/
│           ├── tasks.py          # Gestion tâches
│           ├── campaigns.py      # Gestion campagnes
│           └── tickets.py        # Gestion tickets
│
├── 🎨 Templates (Django)
│   ├── base.html                 # Base template avec navigation
│   ├── index.html                # Page d'accueil
│   ├── offline.html              # Page hors-ligne PWA
│   ├── sitemap.xml
│   ├── robots.txt
│   │
│   ├── auth/
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── forgot_password.html
│   │   ├── reset_password.html
│   │   ├── otp.html              # Authentification OTP
│   │   ├── validation_secondaire.html
│   │   └── delete_account.html
│   │
│   ├── admin/
│   │   ├── dg.html               # Dashboard DG
│   │   ├── administration_Candidatures.html
│   │   ├── coordinateur_pedagogie.html
│   │   ├── coordinateur_technique.html
│   │   ├── coordinateur_marketing.html
│   │   ├── coordinateur_operations.html
│   │   ├── coordinateur_qualite.html
│   │   ├── coordinateur_support.html
│   │   ├── coordinateur_design.html
│   │   ├── gestionnaire.html
│   │   └── reunion.html
│   │
│   ├── parcours/
│   │   ├── selection_metier.html
│   │   ├── accueil_parcours.html
│   │   ├── cours.html            # + Assistant IA intégré
│   │   ├── test.html
│   │   └── test_global.html
│   │
│   ├── pages/
│   │   ├── a_propos.html
│   │   ├── accessibilite.html
│   │   ├── plan_du_site.html
│   │   ├── remboursement.html
│   │   ├── statut_plateforme.html
│   │   ├── financement_formation.html
│   │   ├── comparez_ventoryx.html
│   │   ├── certificats_blockchain.html
│   │   ├── newsletter_confirmation.html
│   │   └── newsletter_desabonnement.html
│   │   │
│   │   ├── academie/
│   │   │   ├── programme_pnc.html
│   │   │   ├── programme_pilote_de_ligne.html
│   │   │   ├── programme_controleur_aerien.html
│   │   │   ├── programme_technicien_aeronautique.html
│   │   │   ├── programme_mecanicien_avion.html
│   │   │   ├── programme_agent_escale.html
│   │   │   ├── programme_ingenieur_aeronautique.html
│   │   │   └── programme_formation_avancee.html
│   │   │
│   │   ├── support/
│   │   │   ├── blog.html
│   │   │   ├── blog_detail.html
│   │   │   ├── centre_aide.html
│   │   │   ├── contact.html
│   │   │   ├── faq.html
│   │   │   ├── support_technique.html
│   │   │   ├── telechargement.html
│   │   │   └── temoignages.html
│   │   │
│   │   ├── entreprise/
│   │   │   ├── premium.html
│   │   │   ├── inscription_entreprise.html
│   │   │   ├── checkout.html
│   │   │   ├── payment_success.html
│   │   │   ├── payment_cancel.html
│   │   │   ├── offre_entreprise.html
│   │   │   ├── dashboard_entreprise.html
│   │   │   └── payment_success_entreprise.html
│   │   │
│   │   ├── legal/
│   │   │   ├── cgu.html
│   │   │   ├── cgv.html
│   │   │   ├── confidentialite.html
│   │   │   └── mentions_legales.html
│   │   │
│   │   ├── institution/
│   │   │   ├── support_administration.html
│   │   │   ├── qualite_innovation.html
│   │   │   ├── pedagogie_contenu.html
│   │   │   ├── design_experience_utilisateur.html
│   │   │   ├── developpement_technique.html
│   │   │   ├── marketing_communication.html
│   │   │   └── operations_logistique.html
│   │   │
│   │   ├── recrutement/
│   │   │   ├── carriere.html
│   │   │   ├── postuler.html
│   │   │   └── espace_candidat.html
│   │   │
│   │   └── utilisateur/
│   │       ├── tableau_de_bord.html
│   │       ├── verification_certificat.html
│   │       ├── profil.html
│   │       ├── parametres_compte.html
│   │       ├── historique_commandes.html
│   │       ├── mes_certificats.html
│   │       ├── parrainage.html
│   │       ├── devis.html
│   │       └── notifications.html
│   │
│   ├── entreprises/
│   │   ├── offre_entreprise.html
│   │   ├── dashboard_entreprise.html
│   │   └── payment_success_entreprise.html
│   │
│   ├── partenaires/
│   │   ├── partenariats.html
│   │   ├── inscription_partenaire.html
│   │   ├── programme_partenaire.html
│   │   ├── dashboard_partenaire.html
│   │   └── convention_partenaire.html
│   │
│   ├── forum/
│   │   ├── forum_principal.html
│   │   ├── forum_metier.html
│   │   ├── nouveau_sujet.html
│   │   ├── sous_forum.html
│   │   └── sujet.html
│   │
│   ├── messaging/
│   │   ├── contact_list.html
│   │   └── inbox.html
│   │
│   ├── audit/
│   │   └── journal.html
│   │
│   └── errors/
│       ├── 403.html
│       ├── 404.html
│       ├── 429.html
│       ├── 500.html
│       └── maintenance.html
│
├── 📂 Static Files
│   ├── css/
│   │   ├── style.css              # Styles principaux
│   │   ├── parcours.css
│   │   ├── responsive.css
│   │   └── animations.css
│   │
│   ├── js/
│   │   ├── site.js                # JS principal
│   │   ├── parcours.js
│   │   ├── sw.js                  # Service Worker (PWA)
│   │   ├── chatbot.js             # Assistant IA
│   │   ├── translator.js          # Traduction
│   │   ├── notifications.js
│   │   └── pwa.js                 # Gestion PWA
│   │
│   ├── images/
│   │   ├── logo.png
│   │   ├── logo-dark.png
│   │   ├── icon-192.png           # PWA icon
│   │   ├── icon-512.png           # PWA icon
│   │   ├── program-pilote.jpg
│   │   ├── program-pnc.jpg
│   │   ├── program-ingenieur.jpg
│   │   ├── program-controleur.jpg
│   │   ├── program-technicien.jpg
│   │   ├── program-mecanicien.jpg
│   │   ├── program-agent.jpg
│   │   └── program-premium.jpg
│   │
│   └── manifest.json              # PWA Manifest
│
├── 🧪 Tests
│   ├── __init__.py
│   ├── test_core.py
│   ├── test_users.py
│   ├── test_parcours.py
│   ├── test_audit.py
│   ├── test_security.py
│   └── fixtures/
│       ├── users.json
│       ├── parcours.json
│       └── courses.json
│
├── 🌍 Localisation (i18n)
│   ├── fr/LC_MESSAGES/
│   │   ├── django.po
│   │   └── django.mo
│   ├── en/LC_MESSAGES/
│   ├── es/LC_MESSAGES/
│   ├── pt/LC_MESSAGES/
│   ├── ar/LC_MESSAGES/
│   ├── zh/LC_MESSAGES/
│   ├── ru/LC_MESSAGES/
│   ├── de/LC_MESSAGES/
│   ├── it/LC_MESSAGES/
│   ├── ja/LC_MESSAGES/
│   ├── ko/LC_MESSAGES/
│   ├── hi/LC_MESSAGES/
│   ├── tr/LC_MESSAGES/
│   ├── nl/LC_MESSAGES/
│   └── sv/LC_MESSAGES/
│
├── 💾 Media
│   ├── vault/
│   │   ├── contracts/
│   │   ├── certificates/
│   │   └── sensitive_docs/        # Documents sensibles (accès restreint)
│   │
│   └── audio/
│       ├── courses/               # Cours en version audio (TTS)
│       └── archive/
│
├── 📊 Backups
│   ├── db/                        # Sauvegardes BD (rotation 7 jours)
│   ├── media/                     # Sauvegardes média
│   └── logs/
│       ├── ventoryx.log
│       ├── access.log
│       └── error.log
│
└── 🛠️ Utilitaires
    ├── utils/
    │   ├── decorators.py          # @require_role, @log_audit, etc.
    │   ├── exceptions.py
    │   ├── validators.py
    │   ├── helpers.py
    │   └── constants.py
    │
    ├── commands/
    │   ├── seed.py
    │   ├── generate_icons.py      # Génération icônes PWA
    │   ├── backup_db.py
    │   └── cleanup.py
    │
    └── management/commands/
        ├── create_users.py
        ├── generate_report.py
        └── health_check.py
```

---

## 🎯 Organisation par Responsabilités

### **1. Apps Django (Domaines métier)**

| App | Responsabilité | Modèles clés |
|-----|----------------|--------------|
| **core** | Accueil, support, IA | ChatSession, Ticket |
| **users** | Auth, RBAC, abonnement | User, Role, Subscription |
| **parcours** | Apprentissage | Module, Course, Test, Progress |
| **blog** | Contenu éditorial | Article, Category, Comment |
| **institution** | Infos institutionnelles | Department, Job, Certification |
| **messaging** | Comms internes/externes | Message, Notification, Newsletter |
| **audit** | Traçabilité | AuditLog (immuable) |
| **forum** | Communauté | Forum, Topic, Post, Reply |
| **gestion** | Opérations internes | Task, Campaign, Ticket |

### **2. Rôles & Permissions (RBAC)**

```python
ROLES = {
    'DG': ['dashboard_admin', 'audit_full', 'all_departments'],
    'Coordinateur': ['department_only', 'manage_content', 'manage_team'],
    'Gestionnaire': ['own_pages', 'own_content'],
    'Utilisateur': ['view_courses', 'take_tests', 'view_profile']
}

DEPARTMENTS = [
    'pedagogie', 'technique', 'marketing', 
    'operations', 'qualite', 'support', 'design'
]
```

### **3. Services Externes**

- **OpenAI (GPT-4o)** : Assistant IA sur toutes pages cours
- **Stripe** : Paiements sécurisés (PCI-DSS)
- **Redis** : Cache + Celery
- **PostgreSQL** : Données critiques
- **TTS Engine** : Synthèse vocale

### **4. Sécurité**

- Argon2id : Hachage mots de passe
- CSRF : Protection formulaires
- MFA : OTP (DG) + validation secondaire (coordinateurs)
- Rate Limiting : login/register/contact
- Audit Immuable : 131 actions tracées
- Vault : Documents sensibles (accès restreint)

---

## ⚙️ Configuration & Déploiement

### **Fichiers de Configuration**

```
.env                    # Variables d'environnement
.env.example           # Template
docker-compose.yml     # Containerisation
Dockerfile             # Image Docker
requirements.txt       # Dépendances Python
```

### **CI/CD**

```
.github/workflows/
├── ci.yml             # Tests + analyse sécurité
├── deploy.yml         # Déploiement production
└── security-check.yml # Bandit + Safety
```

### **Celery Beat (Tâches automatisées)**

```python
CELERY_BEAT_SCHEDULE = {
    'backup-db': {...},              # Sauvegardes quotidiennes
    'cleanup-sessions': {...},       # Nettoyage sessions
    'send-reminders': {...},         # Relances utilisateurs
    'generate-reports': {...},       # Rapports mensuels
    'cleanup-audit': {...},          # Archivage audit
    'health-check': {...},           # Monitoring
}
```

---

## 📈 Parcours Disponibles

| Métier | Modules | Cours | Tests | Prix |
|--------|---------|-------|-------|------|
| PNC | 4 | 80 | 16 | 29€/mois |
| Pilote de Ligne | 4 | 80 | 16 | 29€/mois |
| Ingénieur Aéronautique | 4 | 80 | 16 | 29€/mois |
| Contrôleur Aérien | 4 | 80 | 16 | Gratuit |
| Technicien Aéronautique | 4 | 80 | 16 | Gratuit |
| Mécanicien Avion | 4 | 80 | 16 | 29€/mois |
| Agent d'Escale | 4 | 80 | 16 | 29€/mois |
| Formation Avancée (Premium) | 6 | 90 | 0 | Abonnement Annuel |

---

## 🚀 Points d'Entrée Clés

### **URLs Principales**

```
/                           → Accueil
/auth/login                 → Connexion
/auth/register              → Inscription
/parcours/                  → Sélection parcours
/parcours/<id>/cours/       → Cours + Assistant IA
/admin/dg                   → Dashboard DG
/admin/coordinateur/<dept>  → Dashboard coordinateur
/audit/journal              → Journal d'audit
/health                     → Health check
```

### **API Endpoints (si applicable)**

```
/api/courses/               → Récupérer cours
/api/progress/              → Suivi progression
/api/ai/chat/               → Assistant IA
/api/translations/          → Traductions
/api/certificates/          → Certificats
/api/audit/logs/            → Journal d'audit
```

---

## 📝 Prochaines Étapes

1. ✅ **Initialiser les apps Django**
2. ✅ **Créer les modèles de données**
3. ✅ **Configurer les services externes (OpenAI, Stripe)**
4. ✅ **Implémenter l'authentification & RBAC**
5. ✅ **Développer les templates de base**
6. ✅ **Intégrer le PWA**
7. ✅ **Mettre en place Celery Beat**
8. ✅ **Configurer CI/CD**
9. ✅ **Tests & audit sécurité**
10. ✅ **Déploiement production**

---

## 📚 Documentation Complète

- **Modèles de données** : `docs/models.md`
- **API Documentation** : `docs/api.md`
- **Guide de déploiement** : `docs/deployment.md`
- **Guide sécurité** : `docs/security.md`
- **Workflow de contribution** : `CONTRIBUTING.md`
