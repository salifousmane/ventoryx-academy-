from django.urls import path
from . import views

app_name = 'parcours'

urlpatterns = [
    path('', views.selection_metier, name='selection_metier'),
    path('<str:metier>/', views.accueil_parcours, name='accueil_parcours'),
    path('<str:metier>/module/<int:module_num>/cours/<int:cours_num>/', views.cours, name='cours'),
    path('<str:metier>/module/<int:module_num>/test/<int:test_num>/', views.test, name='test'),
    path('<str:metier>/test-global/', views.test_global, name='test_global'),
    path('terminer-cours/', views.terminer_cours, name='terminer_cours'),
]
