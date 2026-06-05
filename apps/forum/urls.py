from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:metier>/', views.metier, name='metier'),
    path('<str:metier>/<slug:slug>/', views.sous_forum, name='sous_forum'),
    path('<str:metier>/sujet/<int:sujet_id>/', views.sujet, name='sujet'),
    path('<str:metier>/nouveau/', views.nouveau_sujet, name='nouveau_sujet'),
    path('<str:metier>/<slug:slug>/nouveau/', views.nouveau_sujet, name='nouveau_sujet_sous_forum'),
    path('repondre/<int:sujet_id>/', views.repondre_sujet, name='repondre'),
    path('epingler/<int:sujet_id>/', views.epingler_sujet, name='epingler'),
    path('fermer/<int:sujet_id>/', views.fermer_sujet, name='fermer'),
]
