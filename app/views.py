from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import TeamRegistrationForm
from django.contrib.auth import authenticate, login, logout
import json
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import TeamUser

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
