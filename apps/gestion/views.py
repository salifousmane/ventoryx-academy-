# apps/gestion/views.py

# ============================================================
# IMPORTATION UNIQUE VERS LE FICHIER MAÎTRE
# ============================================================

from apps.gestion.gestion_views import *

# ============================================================
# RÉ-EXPORTATION EXPLICITE (POUR GARANTIR LA VISIBILITÉ)
# ============================================================

# DG
dg_exporter_messages = dg_exporter_messages
dg_exporter_candidatures = dg_exporter_candidatures
dg_rapport_hebdo = dg_rapport_hebdo
dg_auditer_departement = dg_auditer_departement
dg_message_coordinateurs = dg_message_coordinateurs
dg_archiver_messages = dg_archiver_messages
dg_valider_budget = dg_valider_budget
dg_creer_alerte = dg_creer_alerte
dg_ajouter_partenaire = dg_ajouter_partenaire
dg_vider_cache = dg_vider_cache
admin_candidatures = admin_candidatures

# Pédagogie
pedagogie_creer_module = pedagogie_creer_module
pedagogie_creer_cours = pedagogie_creer_cours
pedagogie_creer_quiz = pedagogie_creer_quiz
pedagogie_ajouter_question = pedagogie_ajouter_question
pedagogie_gerer_parcours = pedagogie_gerer_parcours

# Technique
technique_creer_tache = technique_creer_tache
technique_signaler_bug = technique_signaler_bug
technique_liste_taches = technique_liste_taches

# Marketing
marketing_creer_campagne = marketing_creer_campagne
marketing_creer_article = marketing_creer_article

# Opérations
operations_planifier_formation = operations_planifier_formation
operations_ajouter_partenaire = operations_ajouter_partenaire

# Qualité
qualite_proposer_innovation = qualite_proposer_innovation
qualite_signaler_nc = qualite_signaler_nc
qualite_lancer_audit = qualite_lancer_audit

# Support
support_creer_ticket = support_creer_ticket
support_envoyer_chat = support_envoyer_chat
support_repondre_message = support_repondre_message

# Design
design_creer_maquette = design_creer_maquette
design_creer_composant = design_creer_composant