from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('contacts/', views.contact_list, name='contact_list'),
    path('envoyer-dg/', views.envoyer_dg, name='envoyer_dg'),
    path('envoyer-coordinateur/', views.envoyer_coordinateur, name='envoyer_coordinateur'),
]
