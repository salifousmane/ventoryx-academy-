from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('contact/', views.contact, name='contact'),
    path('newsletter/', views.newsletter_inscription, name='newsletter'),
    path('notifications/', views.mes_notifications, name='notifications'),
    path('notifications/<int:notification_id>/lire/', views.marquer_notification_lue, name='notification_lire'),
    path('notifications/marquer-tout-lu/', views.marquer_tout_lu, name='marquer_tout_lu'),
    path('messages-contact/', views.messages_contact, name='messages_contact'),
    path('inbox/', views.inbox, name='inbox'),
    path('envoyer-dg/', views.envoyer_dg, name='envoyer_dg'),
    path('envoyer-equipe/', views.envoyer_equipe, name='envoyer_equipe'),
    path('envoyer-coordinateur/', views.envoyer_coordinateur, name='envoyer_coordinateur'),
]
