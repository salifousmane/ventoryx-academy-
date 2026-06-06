from django.urls import path
from . import views_recrutement

app_name = 'institution'

urlpatterns = [
    path('carriere/', views_recrutement.carriere, name='carriere'),
    path('postuler/', views_recrutement.postuler, name='postuler'),
    path('postuler/<int:offre_id>/', views_recrutement.postuler, name='postuler_offre'),
    path('espace-candidat/', views_recrutement.espace_candidat, name='espace_candidat'),
]
