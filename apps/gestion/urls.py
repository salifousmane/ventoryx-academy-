from django.urls import path
from . import views

app_name = 'gestion'

urlpatterns = [
    path('tasks/', views.task_list, name='tasks'),
    path('tickets/', views.ticket_list, name='tickets'),
]