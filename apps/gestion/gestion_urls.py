from django.urls import path
from . import views

app_name = 'gestion'

urlpatterns = [
    # Pédagogie
    path('pedagogie/creer-module/', views.pedagogie_creer_module, name='pedagogie_creer_module'),
    path('pedagogie/creer-cours/', views.pedagogie_creer_cours, name='pedagogie_creer_cours'),
    path('pedagogie/creer-quiz/', views.pedagogie_creer_quiz, name='pedagogie_creer_quiz'),
    path('pedagogie/ajouter-question/', views.pedagogie_ajouter_question, name='pedagogie_ajouter_question'),
    path('pedagogie/gerer-parcours/', views.pedagogie_gerer_parcours, name='pedagogie_gerer_parcours'),

    # Technique
    path('technique/creer-tache/', views.technique_creer_tache, name='technique_creer_tache'),
    path('technique/signaler-bug/', views.technique_signaler_bug, name='technique_signaler_bug'),
    path('technique/liste-taches/', views.technique_liste_taches, name='technique_liste_taches'),

    # Marketing
    path('marketing/creer-campagne/', views.marketing_creer_campagne, name='marketing_creer_campagne'),
    path('marketing/creer-article/', views.marketing_creer_article, name='marketing_creer_article'),

    # Opérations
    path('operations/planifier-formation/', views.operations_planifier_formation, name='operations_planifier_formation'),
    path('operations/ajouter-partenaire/', views.operations_ajouter_partenaire, name='operations_ajouter_partenaire'),

    # Qualité
    path('qualite/proposer-innovation/', views.qualite_proposer_innovation, name='qualite_proposer_innovation'),
    path('qualite/signaler-nc/', views.qualite_signaler_nc, name='qualite_signaler_nc'),
    path('qualite/lancer-audit/', views.qualite_lancer_audit, name='qualite_lancer_audit'),

    # Support
    path('support/creer-ticket/', views.support_creer_ticket, name='support_creer_ticket'),
    path('support/envoyer-chat/', views.support_envoyer_chat, name='support_envoyer_chat'),
    path('support/repondre-message/', views.support_repondre_message, name='support_repondre_message'),

    # Design
    path('design/creer-maquette/', views.design_creer_maquette, name='design_creer_maquette'),
    path('design/creer-composant/', views.design_creer_composant, name='design_creer_composant'),

    # DG
    path('dg/exporter-messages/', views.dg_exporter_messages, name='dg_exporter_messages'),
    path('dg/exporter-candidatures/', views.dg_exporter_candidatures, name='dg_exporter_candidatures'),
    path('dg/rapport-hebdo/', views.dg_rapport_hebdo, name='dg_rapport_hebdo'),
    path('dg/message-coordinateurs/', views.dg_message_coordinateurs, name='dg_message_coordinateurs'),
    path('dg/archiver-messages/', views.dg_archiver_messages, name='dg_archiver_messages'),
    path('dg/auditer-departement/', views.dg_auditer_departement, name='dg_auditer_departement'),
    path('dg/valider-budget/', views.dg_valider_budget, name='dg_valider_budget'),
    path('dg/creer-alerte/', views.dg_creer_alerte, name='dg_creer_alerte'),
    path('dg/ajouter-partenaire/', views.dg_ajouter_partenaire, name='dg_ajouter_partenaire'),
    path('dg/vider-cache/', views.dg_vider_cache, name='dg_vider_cache'),
    path('dg/reunion-virtuelle/', views.dg_reunion_virtuelle, name='dg_reunion_virtuelle'),
    path('dg/admin-candidatures/', views.dg_admin_candidatures, name='dg_admin_candidatures'),
    path('dg/gerer-offres/', views.dg_gerer_offres, name='dg_gerer_offres'),
]
