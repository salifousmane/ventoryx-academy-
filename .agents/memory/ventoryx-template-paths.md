---
name: Ventoryx template paths
description: Template directory structure — most templates live under pages/ prefix, not at root of templates/
---

All app-specific templates are under `templates/pages/<app>/` not `templates/<app>/`.

**Rule:** render() calls must use `pages/` prefix for app templates.
- `pages/parcours/*.html` — NOT `parcours/*.html`
- `pages/utilisateur/*.html` — NOT `utilisateur/*.html`
- `pages/entreprise/*.html` — correct
- `templates/admin/*.html` — no pages/ prefix (admin templates are at root)
- `templates/auth/*.html` — no pages/ prefix

**Why:** The templates directory has a `pages/` subfolder that wraps all app-specific content. Admin and auth templates are at the root of `templates/`.

**Verified fixed views:** parcours_views.py (all 5 views), users/views.py (dashboard_etudiant), institution/views.py (index).
