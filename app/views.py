from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import TeamRegistrationForm, MatchForm
from django.contrib.auth import authenticate, login, logout
import json
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import TeamUser, Match
from django.utils.timezone import now


# Create your views here.
def dashboard(request):
    teams = TeamUser.objects.all()
    return render(request, 'dashboard.html', {'page': {'title': 'Dashboard'}, 'teams': teams})

def register_team(request):
    form = TeamRegistrationForm()
    if request.method == 'POST':
        form = TeamRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Signed up successfully')
                return redirect('home')
        else:
            messages.error(request, 'Invalid email or password')
        errors = json.loads(form.errors.as_json())
        for msg in errors:
            messages.error(request, f"{msg}: {errors[msg][0]['message']}")
        return render(request, 'register.html', {'page': {'title': 'Register'}, 'form': form})
    else:
        return render(request, 'register.html', {'page': {'title': 'Register'}, 'form': form})

def login_team(request):
    user = request.user
    return_url = request.GET.get('next')
    if user.is_authenticated:
        if return_url is not None:
            return HttpResponseRedirect(return_url)
        return redirect('home')
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = authenticate(request, email=email, password=password)
    if user is not None:
        login(request, user)
        messages.success(request, 'Signed in successfully')
        return_url = request.POST.get('return_url', None)
        if return_url and return_url != 'None':
            return HttpResponseRedirect(return_url)
        else:
            return redirect('home')
    else:
        messages.error(request, 'Invalid email or password')
        return render(request, 'login.html', {'page': {'title': 'Login'}, 'return_url': return_url})


def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out successfully')
    return redirect('login')

def teams(request):
    teams = TeamUser.objects.all()
    return render(request, 'teams.html', {'page': {'title': 'Teams'}, 'teams': teams})

def matches(request):
    friendly_requests = Match.objects.filter(
        away_team__isnull=True,
        # match_date__gt=now()
    )
    upcoming_matches = Match.objects.filter(
        match_date__gt=now(),
        home_team__isnull=False,
        away_team__isnull=False
    )
    previous_matches = Match.objects.filter(
        match_date__lt=now(),
        home_team__isnull=False,
        away_team__isnull=False
    )
    return render(request, 'matches.html', {'page': {'title': 'Matches'}, 'friendly_requests': friendly_requests, 'upcoming_matches': upcoming_matches, 'previous_matches': previous_matches})

@login_required(login_url='login')
def create_friendly_match(request):
    match = MatchForm()
    if request.method == 'POST':
        match_data = {
            'home_team': request.user.id,
            'match_date': request.POST.get('match_date'),
            'venue': request.POST.get('venue')
        }
        match = MatchForm(match_data)
        if match.is_valid():
            match.save()
            messages.success(request, 'Match created successfully')
            return redirect('matches')
        else:
            errors = json.loads(match.errors.as_json())
            for msg in errors:
                messages.error(request, f"{msg}: {errors[msg][0]['message']}")
            return redirect('matches')


@login_required(login_url='login')
def accept_friendly_request(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    if match.home_team == request.user:
        messages.error(request, "You cannot accept your own match request.")
        return redirect('matches')
    match.away_team = request.user
    match.save()
    messages.success(request, 'Match request accepted')
    return redirect('matches')