from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('health/', views.health, name='health'),
    path('tableau-de-bord/', views.tableau_de_bord, name='tableau_de_bord'),
    path('faq/', views.faq, name='faq'),
    path('centre-aide/', views.centre_aide, name='centre_aide'),
    path('support-technique/', views.support_technique, name='support_technique'),
    path('telechargement/', views.telechargement, name='telechargement'),
    path('temoignages/', views.temoignages, name='temoignages'),
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog, name='blog'),
    path('programme/', views.programme, name='programme'),
    path('programme/<slug:metier>/', views.programme_metier, name='programme_metier'),
    path('a-propos/', views.a_propos, name='a_propos'),
    path('carriere/', views.carriere, name='carriere'),
    path('postuler/', views.postuler, name='postuler'),
    path('postuler/<int:offre_id>/', views.postuler, name='postuler_offre'),
    path('espace-candidat/', views.espace_candidat, name='espace_candidat'),
    path('premium/', views.premium, name='premium'),
    path('partenariats/', views.partenariats, name='partenariats'),
    path('verification-certificat/', views.verification_certificat, name='verification_certificat'),
    path('api/chatbot/', views.chatbot_api, name='chatbot_api'),
    path('langue/<str:langue>/', views.changer_langue, name='changer_langue'),
    path('vault/<int:fichier_id>/', views.servir_fichier_vault, name='vault_fichier'),
    path('legal/<slug:type_page>/', views.page_legale, name='page_legale'),
    path('gestion/pedagogie/', views.pedagogie_contenu, name='pedagogie_contenu'),
    path('gestion/technique/', views.developpement_technique, name='developpement_technique'),
    path('gestion/marketing/', views.marketing_communication, name='marketing_communication'),
    path('gestion/operations/', views.operations_logistique, name='operations_logistique'),
    path('gestion/qualite/', views.qualite_innovation, name='qualite_innovation'),
    path('gestion/support/', views.support_administration, name='support_administration'),
    path('gestion/design/', views.design_experience_utilisateur, name='design_experience_utilisateur'),
]
