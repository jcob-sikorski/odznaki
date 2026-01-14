# mountains/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # The main dashboard showing user progress and badges
    path('', views.profile, name='profile'),
    # The form page to upload a new summit photo
    path('upload/', views.upload_photo, name='upload'),
]