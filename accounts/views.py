# views.py
from django.shortcuts import render, redirect
from .models import CustomUser
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout 
from .forms import SignupForm, LoginForm

# Home page
def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'home.html')

def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Retrieve form data
            username = form.cleaned_data['username']
            name = form.cleaned_data['name']
            n_id = form.cleaned_data['id']
            email = form.cleaned_data['email']
            company = form.cleaned_data['company']
            password1 = form.cleaned_data['password1']

            # Create CustomUser instance and save
            user = CustomUser.objects.create_user(username=username, password=password1)
            user.name = name
            user.n_id = n_id
            user.email = email
            user.company = company
            user.save()

            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('home_page')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# logout page
def user_logout(request):
    logout(request)
    return redirect('login')
