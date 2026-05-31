from django.urls import path
from . import views

app_name = 'institution'

urlpatterns = [
    path('careers/', views.careers, name='careers'),
    path('verify-certificate/', views.verify_certificate, name='verify_certificate'),
]