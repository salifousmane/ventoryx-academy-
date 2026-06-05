from django.urls import path
from . import views

app_name = 'audit'

urlpatterns = [
    path('journal/', views.journal_audit, name='journal'),
]
