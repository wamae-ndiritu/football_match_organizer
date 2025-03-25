from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='home'),
    path('register/', views.register_team, name='register'),
    path('login/', views.login, name='login'),
]
