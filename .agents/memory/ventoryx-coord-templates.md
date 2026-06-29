---
name: Ventoryx coordinator templates
description: Mapping des 7 départements coordinateurs vers leurs templates
---

## Mapping dans apps/users/views.py dashboard_coordinateur()
- `pedagogie` → `admin/coordinateur_pedagogie.html`
- `marketing` → `admin/coordinateur_marketing.html`
- `technique` → `admin/coordinateur_technique.html`
- `operations` → `admin/coordonnateur_operations.html` (double 'n' — cohérent avec fichier existant)
- `qualite` → `admin/coordinateur_qualite.html`
- `support` → `admin/coordinateur_support.html`
- `design` → `admin/coordinateur_design.html`

## Structure de chaque template coordinateur
- Hero avec badge rôle
- 5 KPI stat-cards
- 4 graphiques Chart.js (canvas)
- Actions rapides (boutons)
- Formulaires d'action POST vers gestion: URLs
- Section communication (envoyer_dg + envoyer_coordinateur)

## gestion: URLs par département
- qualite: lancer_audit, signaler_nc, proposer_innovation
- support: creer_ticket, envoyer_chat, repondre_message
- design: creer_maquette, creer_composant

**Why:** Les templates manquants (qualite, support, design) causaient des TemplateDoesNotExist erreurs au login coordinateur.
