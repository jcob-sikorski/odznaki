# mountains/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('upload/', views.upload_photo, name='upload'),
]