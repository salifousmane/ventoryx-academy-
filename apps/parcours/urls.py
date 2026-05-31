from django.urls import path
from . import views

app_name = 'parcours'

urlpatterns = [
    path('', views.parcours_list, name='list'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('test/<int:test_id>/', views.test_detail, name='test_detail'),
]