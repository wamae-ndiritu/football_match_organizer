from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import TeamUser


class TeamRegistrationForm(UserCreationForm):
    class Meta:
        model = TeamUser
        fields = ['team_logo', 'team_name', 'email', 'location', 'coach_name', 'coach_contact', 'password1', 'password2']
