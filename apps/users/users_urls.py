from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<str:uidb64>/<str:token>/', views.reset_password, name='reset_password'),
    path('otp-verify/', views.otp_verify, name='otp_verify'),
    path('validation-secondaire/', views.validation_secondaire, name='validation_secondaire'),
    path('google/', views.google_login, name='google_login'),
    path('google/callback/', views.google_callback, name='google_callback'),
    path('dashboard/', views.dashboard_redirect, name='dashboard'),
    path('dashboard/dg/', views.dashboard_dg, name='dashboard_dg'),
    path('dashboard/coordinateur/<str:departement>/', views.dashboard_coordinateur, name='dashboard_coordinateur'),
    path('dashboard/gestionnaire/<str:departement>/', views.dashboard_gestionnaire, name='dashboard_gestionnaire'),
    path('dashboard/etudiant/', views.dashboard_etudiant, name='dashboard_etudiant'),
    path('checkout/', views.checkout, name='checkout'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    path('paiement/succes/', views.payment_success, name='payment_success'),
    path('paiement/annulation/', views.payment_cancel, name='payment_cancel'),
    path('paiement/webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('reunion/', views.reunion_virtuelle, name='reunion_virtuelle'),
    path('reunion/envoyer/', views.reunion_envoyer_message, name='reunion_envoyer_message'),
    path('equipe/', views.page_equipe, name='equipe'),
    path('rapports-transparence/', views.page_rapports_transparence, name='rapports_transparence'),
    path('documentation/', views.documentation, name='documentation'),
]
