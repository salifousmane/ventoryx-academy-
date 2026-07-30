# Ventoryx Academy — Plateforme de Formation Aéronautique

**Version Django 6.0.7 · Python 3.12 · SQLite / PostgreSQL**

Ventoryx Academy est une application web de formation professionnelle aux métiers de l'aéronautique. Elle combine des parcours pédagogiques complets, un assistant IA spécialisé, un système de certification numérique et un tableau de bord complet pour chaque rôle.

---

## 🚀 Fonctionnalités principales

- **8 parcours aéronautiques** : Pilote de ligne, PNC, Ingénieur, Contrôleur aérien, Technicien, Mécanicien, Agent d'escale, Formation avancée
- **Assistant IA** (GPT-4o-mini) — accessible uniquement pendant les cours
- **Certification numérique** avec vérification publique par numéro de série ou hash
- **Paiements Stripe** (abonnements mensuel/annuel avec CGV obligatoires)
- **PWA** : installable sur iOS, Android et desktop
- **Tableau de bord** adapté à chaque rôle (apprenant, gestionnaire, coordinateur, DG)
- **Sécurité** : Argon2, CSRF, CSP, Axes, audit logs immutables

---

## 🏗️ Architecture

```
Framework    : Django 6.0.7
Base de données : SQLite (développement) · PostgreSQL (production)
Cache        : LocMemCache (dev) · Redis (prod)
Tâches async : Celery + Celery Beat
Statiques    : WhiteNoise
IA           : OpenAI GPT-4o-mini
Paiements    : Stripe Checkout + Webhooks
Auth         : django-allauth + Axes (brute-force protection)
Hachage      : Argon2
```

### Applications

| App | Rôle |
|-----|------|
| `core` | Pages publiques, chatbot IA, vault de documents |
| `users` | Authentification, dashboards par rôle, paiements |
| `parcours` | Formations : parcours, modules, cours, quiz |
| `blog` | Articles et actualités |
| `institution` | Candidatures, offres d'emploi, certificats |
| `messaging` | Messages de contact, notifications |
| `audit` | Logs d'audit immutables |
| `forum` | Forum communautaire par métier |
| `gestion` | Tâches, campagnes marketing, tickets support |

---

## 🔐 Rôles utilisateurs

| Rôle | Description | Dashboard |
|------|-------------|-----------|
| `etudiant` | Apprenant (rôle par défaut) | `/auth/dashboard/etudiant/` |
| `gestionnaire` | Gère son département | `/auth/dashboard/gestionnaire/<dept>/` |
| `coordinateur` | Supervise son département | `/auth/dashboard/coordinateur/<dept>/` |
| `dg` | Directeur Général (accès complet) | `/auth/dashboard/dg/` |

Départements : `pedagogie`, `technique`, `marketing`, `operations`, `qualite`, `support`, `design`

---

## ⚙️ Installation

```bash
# Cloner le projet
git clone <url-du-repo>
cd ventoryx-academy

# Installer les dépendances
pip install -r requirements.txt

# Configuration
cp .env.example .env
# → Remplir les variables dans Replit Secrets (jamais en dur dans .env)

# Base de données
python manage.py migrate

# Données initiales (utilisateurs de test + parcours + forums)
python manage.py init_test_data

# Lancer l'application
python manage.py runserver 0.0.0.0:5000
```

---

## 🔑 Variables d'environnement

> ⚠️ **Important** : toutes les clés sensibles doivent être dans **Replit Secrets**, jamais dans le fichier `.env`.

| Variable | Obligatoire | Description |
|----------|-------------|-------------|
| `DJANGO_SECRET_KEY` | ✅ | Clé secrète Django |
| `OPENAI_API_KEY` | ✅ | Clé API OpenAI (assistant IA) |
| `STRIPE_PUBLIC_KEY` | ✅ (prod) | Clé publique Stripe |
| `STRIPE_SECRET_KEY` | ✅ (prod) | Clé secrète Stripe |
| `STRIPE_WEBHOOK_SECRET` | ✅ (prod) | Secret webhook Stripe |
| `SENDGRID_API_KEY` | prod | Email transactionnel |
| `REDIS_URL` | prod | Cache + Celery |
| `SENTRY_DSN` | optionnel | Monitoring d'erreurs |
| `USE_SQLITE` | dev | `True` pour SQLite, `False` pour PostgreSQL |
| `DJANGO_DEBUG` | dev | `True` en développement |

---

## 👥 Comptes de test

> ⚠️ **Ces comptes sont à supprimer avant la mise en production.**

Mot de passe commun : `ChangeMe2026ChangeMe2026!`

| Rôle | Email |
|------|-------|
| **DG** | `dg@ventoryx-academy.com` |
| **Coord. Pédagogie** | `coord.pedagogie@ventoryx-academy.com` |
| **Coord. Technique** | `coord.technique@ventoryx-academy.com` |
| **Coord. Marketing** | `coord.marketing@ventoryx-academy.com` |
| **Coord. Opérations** | `coord.operations@ventoryx-academy.com` |
| **Coord. Qualité** | `coord.qualite@ventoryx-academy.com` |
| **Coord. Support** | `coord.support@ventoryx-academy.com` |
| **Coord. Design** | `coord.design@ventoryx-academy.com` |
| **Gest. Pédagogie** | `gest.pedagogie@ventoryx-academy.com` |
| **Gest. Technique** | `gest.technique@ventoryx-academy.com` |
| **Gest. Marketing** | `gest.marketing@ventoryx-academy.com` |
| **Gest. Opérations** | `gest.operations@ventoryx-academy.com` |
| **Gest. Qualité** | `gest.qualite@ventoryx-academy.com` |
| **Gest. Support** | `gest.support@ventoryx-academy.com` |
| **Gest. Design** | `gest.design@ventoryx-academy.com` |
| **Étudiant test** | `salifousmanesow4@gmail.com` |

---

## 🛡️ Sécurité

- **Mots de passe** : Argon2 (résistant aux attaques brute-force)
- **Formulaires** : Protection CSRF + honeypot anti-bot
- **Accès** : Blocage après 5 tentatives (django-axes)
- **Contenu** : CSP (Content Security Policy) + X-Frame-Options: DENY
- **Audit** : Logs immutables de toutes les actions sensibles
- **IA** : Filtre de contenu sur questions ET réponses
- **Rate limiting** : Sur les APIs publiques (contact, chatbot)

---

## 📦 Déploiement production

```bash
# Avant de déployer :
# 1. DJANGO_DEBUG=False dans Replit Secrets
# 2. Configurer PostgreSQL (USE_SQLITE=False)
# 3. Ajouter les vraies clés Stripe et OpenAI
# 4. Configurer ALLOWED_HOSTS avec votre domaine
# 5. Supprimer les données de test (python manage.py flush --no-input)
# 6. Configurer Redis pour Celery

python manage.py collectstatic --noinput
python manage.py migrate --noinput
gunicorn wsgi:application --bind 0.0.0.0:5000
```

---

## 📋 Pages et URLs principales

| URL | Description |
|-----|-------------|
| `/` | Page d'accueil |
| `/parcours/` | Sélection du parcours |
| `/auth/login/` | Connexion |
| `/auth/register/` | Inscription |
| `/auth/dashboard/etudiant/` | Espace apprenant |
| `/auth/dashboard/dg/` | Dashboard DG |
| `/auth/checkout/` | Page d'abonnement |
| `/verification-certificat/` | Vérification de certificat |
| `/api/chatbot/` | API assistant IA (POST) |
| `/admin/` | Administration Django |
| `/auth/documentation/` | Cette documentation |

---

*Ventoryx Academy — Protocole d'excellence aéronautique*
