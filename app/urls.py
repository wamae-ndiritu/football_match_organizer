from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='home'),
    path('register/', views.register_team, name='register'),
    path('login/', views.login_team, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('teams/', views.teams, name='teams'),
    path('matches/', views.matches, name='matches'),
    path('friendly-match-request', views.create_friendly_match, name='friendly_match_request'),
    path('match/<int:match_id>/accept', views.accept_friendly_request, name='accept_friendly_match'),
    path('match/<int:match_id>/scores', views.update_match_scores, name='update_match_scores'),
]
