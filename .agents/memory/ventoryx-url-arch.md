---
name: Ventoryx URL architecture
description: Namespaces d'URL valides et substitutions pour les apps inexistantes
---

## Namespaces valides
- `core:`, `users:`, `blog:`, `parcours:`, `forum:`, `institution:`, `messaging:`, `gestion:`, `audit:`, `admin:`

## Apps inexistantes (n'ont pas de urls.py enregistré)
- `entreprises:` → remplacer par `core:contact`, `core:premium`, `users:dashboard`
- `partenaires:` / `partners:` → remplacer par `core:partenariats` ou `core:contact`

## URL names manquants corrigés
- `core:cgv` → `core:page_legale 'cgu'`
- `core:formations` → `parcours:selection_metier`
- `core:legal` → `core:page_legale`
- `core:newsletter` → `core:index`
- `core:support:contact` → `core:contact`
- `admin:forum_topic_changelist` → `admin:forum_sujet_changelist` (le modèle est Sujet, pas Topic)

## Réunion virtuelle
- Vues ajoutées dans `apps/users/views.py`: `reunion_virtuelle`, `reunion_envoyer_message`
- URLs dans `apps/users/users_urls.py`: `auth/reunion/` et `auth/reunion/envoyer/`

**Why:** Les templates référençaient des namespaces d'apps qui n'existent pas dans urls.py racine.
