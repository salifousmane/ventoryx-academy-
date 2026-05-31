from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.forum_list, name='list'),
    path('topic/<int:topic_id>/', views.topic_detail, name='topic_detail'),
]