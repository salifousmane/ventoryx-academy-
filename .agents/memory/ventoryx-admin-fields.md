---
name: Ventoryx admin.py model fields
description: Champs réels des modèles core pour l'admin Django
---

## PageStatique (apps/core/core_models.py)
- `type_page` — CharField choices
- `titre` — CharField
- `contenu` — TextField
- `derniere_modification` — DateTimeField auto_now (**PAS** date_modification)
- `modifie_par` — FK User
- `approuve_par_dg` — BooleanField
- `approuve_par_coordinateurs` — BooleanField
- `version` — IntegerField
- `archive` — BooleanField

## Admin enregistré dans apps/core/admin.py
- PageStatique, SiteConfig, DocumentVault

**Why:** Mettre `date_modification` dans ordering/list_display provoque une SystemCheckError qui empêche le démarrage.
