from django.shortcuts import render

# Create your views here.
def dashboard(request):
    return render(request, 'dashboard.html', {'page': {'title': 'Dashboard'}})

def register_team(request):
    return render(request, 'register.html', {'page': {'title': 'Register'}})

def login(request):
    return render(request, 'login.html', {'page': {'title': 'Login'}})