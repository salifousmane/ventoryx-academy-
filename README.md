# ventoryx-academy- Version Django

Architecture

· Framework : Django 6.0.6
· Base de données : SQLite (développement) — PostgreSQL recommandé en production
· Frontend : Templates Django + CSS/JS statique
· Sécurité : Argon2, CSRF, CSP, rate limiting, audit immutable
· IA : Assistant GPT-4o intégré, traduction 15 langues, Text-to-Speech
· PWA : Application installable sur tous les appareils (iOS, Android, desktop)

Rôles RBAC (3 niveaux)

Rôle Accès
DG (dashboard + admin + audit)
Coordinateur Son département uniquement
Gestionnaire Ses propres pages et contenus

7 départements : pedagogie, technique, marketing, operations, qualite, support, design

Prérequis système

· Python 3.10 ou supérieur
· SQLite (inclus) — ou PostgreSQL 14+ en production
· 1GB RAM minimum (2GB recommandé)

Installation

```bash
pip install -r requirements.txt
python manage.py migrate
python seed.py
python manage.py createsuperuser
python manage.py runserver
```

Variables d'environnement

Copiez .env.example vers .env et configurez :

```env
# Django
SECRET_KEY=votre_cle_secrete
DEBUG=False
ALLOWED_HOSTS=ventoryx-academy.com,www.ventoryx-academy.com

# Base de données
DATABASE_URL=postgresql://user:password@localhost/ventoryx

# Stripe
STRIPE_PUBLIC_KEY=pk_xxx
STRIPE_SECRET_KEY=sk_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=votre@email.com
EMAIL_HOST_PASSWORD=votre_mot_de_passe
DEFAULT_FROM_EMAIL=noreply@ventoryx-academy.com

# Celery
REDIS_URL=redis://localhost:6379

# OpenAI (Assistant IA)
OPENAI_API_KEY=
```

Utilisateurs par défaut

Mot de passe : ChangeMe!2026 (modifiable via VENTORYX_DEFAULT_PWD)

Rôle Email
DG dg@ventoryx-academy.com
Coordinateur coord.<dept>@ventoryx-academy.com

Structure du projet

```
ventoryx_academy/
├── manage.py
├── settings.py
├── urls.py
├── wsgi.py
├── asgi.py
├── celery.py
├── requirements.txt
├── seed.py
├── .env
├── .env.example
├── .bandit
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── README.md
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── apps/
│   ├── core/              # Accueil, support, légal, chatbot IA, traduction, TTS
│   ├── users/             # Authentification, RBAC, abonnements, Stripe
│   ├── parcours/          # Modules, cours, tests, progression
│   ├── blog/              # Blog et centre d'aide
│   ├── institution/       # Pages institutionnelles, carrières, recrutement, certificats
│   ├── messaging/         # Messages, notifications, newsletter
│   ├── audit/             # Journal d'audit immutable (131 actions tracées)
│   ├── forum/             # Forums communautaires
│   └── gestion/           # Gestion des départements (tâches, campagnes, tickets...)
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── offline.html
│   ├── sitemap.xml
│   ├── robots.txt
│   │
│   ├── auth/
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── forgot_password.html
│   │   ├── reset_password.html
│   │   ├── otp.html
│   │   ├── validation_secondaire.html
│   │   └── delete_account.html
│   │
│   ├── admin/
│   │   ├── dg.html
│   │   ├── administration_Candidatures.html
│   │   ├── coordinateur_pedagogie.html
│   │   ├── coordinateur_technique.html
│   │   ├── coordinateur_marketing.html
│   │   ├── coordinateur_operations.html
│   │   ├── gestionnaire.html
│   │   └── reunion.html
│   │
│   ├── parcours/
│   │   ├── selection_metier.html
│   │   ├── accueil_parcours.html
│   │   ├── cours.html
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
│   │   ├── newsletter_desabonnement.html
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
│   │   │   ├── payment_success_entreprise.html
│   │   │   └── payment_cancel_entreprise.html
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
│   │   ├── payment_success_entreprise.html
│   │   └── payment_cancel_entreprise.html
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
├── static/
│   ├── css/
│   │   ├── style.css
│   │   └── parcours.css
│   ├── js/
│   │   ├── site.js
│   │   ├── parcours.js
│   │   └── sw.js
│   ├── images/
│   │   ├── logo.png
│   │   ├── icon-192.png
│   │   ├── icon-512.png
│   │   ├── program-pilote.jpg
│   │   ├── program-pnc.jpg
│   │   ├── program-ingenieur.jpg
│   │   ├── program-controleur.jpg
│   │   ├── program-technicien.jpg
│   │   ├── program-mecanicien.jpg
│   │   ├── program-agent.jpg
│   │   └── program-premium.jpg
│   └── manifest.json
│
├── tests/
│   ├── __init__.py
│   └── test_core.py
│
├── locale/
│   ├── fr/LC_MESSAGES/
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
├── media/
│   ├── vault/           # Documents sensibles (accès restreint)
│   └── audio/           # Cours en version audio (TTS)
│
└── backups/             # Sauvegardes quotidiennes (rotation 7 jours)
```

Parcours disponibles

Métier Modules Cours Tests Prix
PNC 4 80 16 29€/mois
Pilote de Ligne 4 80 16 29€/mois
Ingénieur Aéronautique 4 80 16 29€/mois
Contrôleur Aérien 4 80 16 Gratuit
Technicien Aéronautique 4 80 16 Gratuit
Mécanicien Avion 4 80 16 29€/mois
Agent d'Escale 4 80 16 29€/mois
Formation Avancée (Premium) 6 90 0 Abonnement Annuel

Fonctionnalités

· Assistant IA (GPT-4o) accessible sur toutes les pages de cours
· 15 langues : FR, EN, ES, PT, AR, ZH, RU, DE, IT, JA, KO, HI, TR, NL, SV
· Traduction automatique du contenu des cours
· Audio des cours (Text-to-Speech) dans la langue choisie
· PWA installable sur téléphone, tablette et ordinateur
· Mode hors-ligne pour les cours déjà chargés
· Certificats SHA-256 vérifiables publiquement
· Paiement Stripe (PCI-DSS)
· Journal d'audit immutable avec chaîne de hachage
· 6 tâches automatisées (Celery Beat) : backups, nettoyage, relances, rapports

Sécurité

· Argon2id pour les mots de passe
· Protection CSRF sur tous les formulaires
· Rate limiting sur login/register/contact
· Verrouillage compte après 5 échecs (15 min)
· Journal d'audit immutable (131 actions tracées)
· Vault sécurisé pour documents sensibles
· En-têtes de sécurité (CSP, X-Frame-Options, Referrer-Policy)
· Protection anti-bot (honeypot, time-trap)
· MFA contextuel : validation OTP (DG) et validation secondaire (coordinateurs)
· Health check : endpoint /health/ pour monitoring
· Paiement sécurisé : Stripe Checkout avec webhooks

Commandes utiles

Lancer Celery

```bash
celery -A ventoryx_academy worker -l info
celery -A ventoryx_academy beat -l info
```

Générer les icônes PWA

```bash
python generate_icons.py
```

Lancer les tests

```bash
python manage.py test apps/
bandit -r apps/
safety check
```

Sauvegarde manuelle

```bash
python manage.py dbbackup
python manage.py mediabackup
```

CI/CD

Tests automatisés, analyse de sécurité (bandit + safety) et vérification des migrations via GitHub Actions (.github/workflows/ci.yml).

Lancement production

```bash
gunicorn wsgi:application -w 4 -b 0.0.0.0:5000
```

Déploiement Docker

```bash
docker build -t ventoryx-academy .
docker-compose up -d
```

SSL / HTTPS

```bash
certbot --nginx -d ventoryx-academy.com
```

Monitoring

· Health check : https://ventoryx-academy.com/health/
· Logs : logs/ventoryx.log
· Statut plateforme : /statut/

Licence

Propriétaire — Tous droits réservés. © Ventoryx Academy

Contribution

Les pull requests sont les bienvenues. Merci de suivre :

1. Fork le projet
2. Créer une branche (git checkout -b feature/ma-fonctionnalite)
3. Commit (git commit -m 'Ajout fonctionnalité')
4. Push (git push origin feature/ma-fonctionnalite)
5. Ouvrir une Pull Request

Feuille de route

· Contenu vidéo + sous-titres
· Badges Open Badges + partage LinkedIn
· Simulateurs interactifs (horizon artificiel, anémomètre)
· Parrainage (1 mois offert)
· Partenariats avec écoles aéronautiques
· Application mobile native (iOS/Android)
