from django.urls import path
from forum_app import views

app_name = 'forum_app'

urlpatterns = [
    path('', views.index, name='index'),
]